"""
AI-RPG-Alpha: Consequence Scheduler

This module handles delayed consequences and event scheduling.
It manages events that trigger after certain conditions are met,
such as turn-based delays, location changes, or story progression.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from models.dataclasses import Player, ConsequenceThread, GameEvent
from dao.game_state import GameStateDAO
from .consequence_types import ConsequenceTrigger, ConsequenceType
from .consequence_handlers import ConsequenceHandlers

class ConsequenceScheduler:
    """
    Manages delayed consequences and event scheduling.
    
    Handles the scheduling, tracking, and execution of consequences
    that should trigger based on various game conditions.
    """
    
    def __init__(self, game_dao: GameStateDAO):
        """
        Initialize the consequence scheduler.
        
        Args:
            game_dao: Game state data access object
        """
        self.game_dao = game_dao
        self.active_consequences = {}  # player_id -> list of consequences
        self.handlers = ConsequenceHandlers(game_dao)
        self.consequence_handlers = {
            ConsequenceType.NARRATIVE: self.handlers.handle_narrative_consequence,
            ConsequenceType.STAT_CHANGE: self.handlers.handle_stat_change_consequence,
            ConsequenceType.INVENTORY: self.handlers.handle_inventory_consequence,
            ConsequenceType.QUEST_UNLOCK: self.handlers.handle_quest_unlock_consequence,
            ConsequenceType.LOCATION_CHANGE: self.handlers.handle_location_change_consequence,
            ConsequenceType.NPC_INTERACTION: self.handlers.handle_npc_interaction_consequence,
            ConsequenceType.WORLD_STATE: self.handlers.handle_world_state_consequence
        }
    
    def schedule_consequence(
        self,
        player_id: str,
        consequence_data: Dict[str, Any],
        trigger_type: ConsequenceTrigger,
        trigger_condition: Any,
        consequence_type: ConsequenceType,
        priority: int = 1
    ) -> str:
        """
        Schedule a new consequence.
        
        Args:
            player_id: ID of the player this consequence affects
            consequence_data: Data describing the consequence
            trigger_type: Type of trigger condition
            trigger_condition: Specific trigger condition
            consequence_type: Type of consequence to execute
            priority: Priority level (higher = more important)
            
        Returns:
            Unique consequence ID
        """
        consequence_id = f"{player_id}_{datetime.now().timestamp()}_{priority}"
        
        consequence = {
            "id": consequence_id,
            "player_id": player_id,
            "consequence_data": consequence_data,
            "trigger_type": trigger_type.value,
            "trigger_condition": trigger_condition,
            "consequence_type": consequence_type.value,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "executed": False,
            "execution_count": 0,
            "max_executions": consequence_data.get("max_executions", 1)
        }
        
        # Add to active consequences
        if player_id not in self.active_consequences:
            self.active_consequences[player_id] = []
        
        self.active_consequences[player_id].append(consequence)
        
        # Sort by priority
        self.active_consequences[player_id].sort(key=lambda x: x["priority"], reverse=True)
        
        return consequence_id
    
    def check_and_execute_consequences(
        self,
        player: Player,
        current_context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Check for and execute any triggered consequences.
        
        Args:
            player: Current player object
            current_context: Current game context
            
        Returns:
            List of executed consequences with their results
        """
        if player.id not in self.active_consequences:
            return []
        
        executed_consequences = []
        remaining_consequences = []
        
        for consequence in self.active_consequences[player.id]:
            if consequence["executed"] and consequence["execution_count"] >= consequence["max_executions"]:
                continue  # Skip fully executed consequences
            
            # Check if trigger condition is met
            if self._check_trigger_condition(consequence, player, current_context):
                # Execute the consequence
                result = self._execute_consequence(consequence, player, current_context)
                
                if result:
                    consequence["executed"] = True
                    consequence["execution_count"] += 1
                    consequence["last_executed"] = datetime.now().isoformat()
                    executed_consequences.append({
                        "consequence": consequence,
                        "result": result
                    })
                    
                    # Log the consequence execution
                    self._log_consequence_execution(consequence, player, result)
            
            # Keep consequence if it can still be executed
            if consequence["execution_count"] < consequence["max_executions"]:
                remaining_consequences.append(consequence)
        
        # Update active consequences
        self.active_consequences[player.id] = remaining_consequences
        
        return executed_consequences
    
    def schedule_turn_based_consequence(
        self,
        player_id: str,
        turns_delay: int,
        consequence_type: ConsequenceType,
        consequence_data: Dict[str, Any],
        priority: int = 1
    ) -> str:
        """
        Schedule a consequence to trigger after a certain number of turns.
        
        Args:
            player_id: ID of the player
            turns_delay: Number of turns to wait
            consequence_type: Type of consequence
            consequence_data: Consequence data
            priority: Priority level
            
        Returns:
            Consequence ID
        """
        player = self.game_dao.get_player(player_id)
        if not player:
            return ""
        
        trigger_turn = player.turn_number + turns_delay
        
        return self.schedule_consequence(
            player_id=player_id,
            consequence_data=consequence_data,
            trigger_type=ConsequenceTrigger.TURN_BASED,
            trigger_condition=trigger_turn,
            consequence_type=consequence_type,
            priority=priority
        )
    
    def schedule_location_based_consequence(
        self,
        player_id: str,
        target_location: str,
        consequence_type: ConsequenceType,
        consequence_data: Dict[str, Any],
        priority: int = 1
    ) -> str:
        """
        Schedule a consequence to trigger when player enters a location.
        
        Args:
            player_id: ID of the player
            target_location: Location that triggers the consequence
            consequence_type: Type of consequence
            consequence_data: Consequence data
            priority: Priority level
            
        Returns:
            Consequence ID
        """
        return self.schedule_consequence(
            player_id=player_id,
            consequence_data=consequence_data,
            trigger_type=ConsequenceTrigger.LOCATION_BASED,
            trigger_condition=target_location,
            consequence_type=consequence_type,
            priority=priority
        )
    
    def schedule_quest_based_consequence(
        self,
        player_id: str,
        quest_id: str,
        quest_outcome: str,  # "completed", "failed", "started"
        consequence_type: ConsequenceType,
        consequence_data: Dict[str, Any],
        priority: int = 1
    ) -> str:
        """
        Schedule a consequence to trigger on quest events.
        
        Args:
            player_id: ID of the player
            quest_id: ID of the quest
            quest_outcome: Quest outcome that triggers consequence
            consequence_type: Type of consequence
            consequence_data: Consequence data
            priority: Priority level
            
        Returns:
            Consequence ID
        """
        trigger_condition = {"quest_id": quest_id, "outcome": quest_outcome}
        
        return self.schedule_consequence(
            player_id=player_id,
            consequence_data=consequence_data,
            trigger_type=ConsequenceTrigger.QUEST_BASED,
            trigger_condition=trigger_condition,
            consequence_type=consequence_type,
            priority=priority
        )
    
    def get_pending_consequences(self, player_id: str) -> List[Dict[str, Any]]:
        """
        Get all pending consequences for a player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            List of pending consequences
        """
        return self.active_consequences.get(player_id, [])
    
    def cancel_consequence(self, consequence_id: str) -> bool:
        """
        Cancel a scheduled consequence.
        
        Args:
            consequence_id: ID of the consequence to cancel
            
        Returns:
            True if cancelled, False if not found
        """
        for player_id, consequences in self.active_consequences.items():
            for i, consequence in enumerate(consequences):
                if consequence["id"] == consequence_id:
                    del consequences[i]
                    return True
        return False
    
    def _check_trigger_condition(
        self,
        consequence: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> bool:
        """Check if a consequence's trigger condition is met"""
        trigger_type = ConsequenceTrigger(consequence["trigger_type"])
        trigger_condition = consequence["trigger_condition"]
        
        if trigger_type == ConsequenceTrigger.TURN_BASED:
            return player.turn_number >= trigger_condition
        
        elif trigger_type == ConsequenceTrigger.LOCATION_BASED:
            return player.current_location == trigger_condition
        
        elif trigger_type == ConsequenceTrigger.QUEST_BASED:
            quest_id = trigger_condition["quest_id"]
            outcome = trigger_condition["outcome"]
            
            if outcome == "completed":
                return quest_id in player.completed_quests
            elif outcome == "started":
                return quest_id in player.active_quests
            elif outcome == "failed":
                # Would need to track failed quests separately
                return False
        
        elif trigger_type == ConsequenceTrigger.STAT_BASED:
            stat_name = trigger_condition["stat"]
            threshold = trigger_condition["threshold"]
            operator = trigger_condition.get("operator", ">=")
            
            stat_value = getattr(player.stats, stat_name, 0)
            
            if operator == ">=":
                return stat_value >= threshold
            elif operator == "<=":
                return stat_value <= threshold
            elif operator == "==":
                return stat_value == threshold
        
        elif trigger_type == ConsequenceTrigger.CHOICE_BASED:
            if context and "last_choice" in context:
                return trigger_condition in context["last_choice"].lower()
        
        return False
    
    def _execute_consequence(
        self,
        consequence: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """Execute a consequence and return the result"""
        consequence_type = ConsequenceType(consequence["consequence_type"])
        consequence_data = consequence["consequence_data"]
        
        handler = self.consequence_handlers.get(consequence_type)
        if handler:
            return handler(consequence_data, player, context)
        
        return None
    

    
    def _log_consequence_execution(
        self,
        consequence: Dict[str, Any],
        player: Player,
        result: Dict[str, Any]
    ):
        """Log the execution of a consequence"""
        event = GameEvent(
            id=f"consequence_{consequence['id']}_{datetime.now().timestamp()}",
            player_id=player.id,
            event_type="consequence_executed",
            description=f"Consequence {consequence['consequence_type']} executed",
            data={
                "consequence_id": consequence["id"],
                "consequence_type": consequence["consequence_type"],
                "trigger_type": consequence["trigger_type"],
                "result": result
            },
            turn_number=player.turn_number
        )
        
        self.game_dao.log_event(event)

