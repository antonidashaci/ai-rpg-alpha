"""
Game Orchestrator
=================

Master controller that orchestrates all game systems:
- Long-form quest progression
- BG3-style combat encounters
- Cosmic horror sanity mechanics
- AI narrative generation
- Database persistence
- Turn-by-turn game flow

This is the main brain that coordinates everything.
"""

from typing import Dict, Any, Optional, Tuple, List
from dataclasses import asdict
import random

from .quest_framework import (
    QuestFrameworkEngine, LongFormQuest, QuestLibrary,
    QuestChoice, ChoiceImpact
)
from .combat_system import (
    TacticalCombatEngine, CombatState, CombatOutcome,
    CombatEncounterLibrary, CombatDifficulty, ActionType
)
from .sanity_system import SanityEngine, SanityLevel
from ..dao.game_database import GameDatabase


class GameOrchestrator:
    """
    Master game controller
    
    Coordinates:
    - Quest progression (30-40 turns)
    - Combat encounters (every 8-10 turns)
    - Sanity mechanics (cosmic horror)
    - AI narrative generation
    - Database persistence
    """
    
    def __init__(self, db_path: str = "game_data.db"):
        self.db = GameDatabase(db_path)
        self.quest_engine = QuestFrameworkEngine()
        self.combat_engine = TacticalCombatEngine()
        self.sanity_engine = SanityEngine()
        
        # Current game state
        self.player_id: Optional[str] = None
        self.current_combat: Optional[CombatState] = None
        self.combat_db_id: Optional[int] = None
        
    # ========================================================================
    # GAME INITIALIZATION
    # ========================================================================
    
    def start_new_game(
        self,
        player_name: str,
        scenario: str,
        abilities: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Start a new game
        
        Args:
            player_name: Player character name
            scenario: "northern_realms", "whispering_town", or "neo_tokyo"
            abilities: Optional D&D ability scores
        
        Returns:
            Game initialization data with opening narrative
        """
        # Generate player ID
        import uuid
        player_id = str(uuid.uuid4())
        self.player_id = player_id
        
        # Create player in database
        self.db.create_player(player_id, player_name, scenario, abilities)
        
        # Load appropriate quest based on scenario
        quest = self._load_scenario_quest(scenario)
        self.quest_engine.load_quest(quest)
        
        # Create quest state in database
        self.db.create_quest_state(player_id, quest.quest_id, scenario, quest.total_turns)
        
        # Start the quest
        opening_narrative = self.quest_engine.start_quest()
        
        # Get player data
        player_data = self.db.get_player(player_id)
        
        # Log initial event
        self.db.log_game_event(
            player_id=player_id,
            turn_number=1,
            event_type="game_start",
            player_action="Begin Adventure",
            ai_response=opening_narrative,
            quest_id=quest.quest_id
        )
        
        return {
            "success": True,
            "player_id": player_id,
            "player_name": player_name,
            "scenario": scenario,
            "quest_title": quest.title,
            "narrative": opening_narrative,
            "player_stats": player_data,
            "quest_state": self.quest_engine.get_quest_state(),
            "sanity_state": self.sanity_engine.get_sanity_state_summary() if scenario == "whispering_town" else None
        }
    
    def _load_scenario_quest(self, scenario: str) -> LongFormQuest:
        """Load appropriate quest for scenario"""
        if scenario == "whispering_town":
            return QuestLibrary.the_whispering_town_quest()
        elif scenario == "northern_realms":
            return QuestLibrary.northern_realms_quest()
        else:
            # Default to whispering town
            return QuestLibrary.the_whispering_town_quest()
    
    # ========================================================================
    # TURN PROCESSING
    # ========================================================================
    
    def process_turn(
        self,
        player_id: str,
        player_action: str,
        choice_index: int = 0,
        ai_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Process a single game turn
        
        This is the main game loop entry point. Handles:
        - Quest progression
        - Combat triggers
        - Sanity effects
        - AI narrative generation
        - Database updates
        
        Returns:
            Complete turn result with narrative, choices, and state updates
        """
        self.player_id = player_id
        
        # Get player data
        player_data = self.db.get_player(player_id)
        if not player_data:
            return {"error": "Player not found"}
        
        # Check if in combat
        if self.current_combat:
            return self._process_combat_turn(player_action, choice_index)
        
        # Process quest turn
        quest_result = self.quest_engine.process_turn(
            player_action,
            choice_index,
            additional_context={"player_data": player_data}
        )
        
        # Update quest state in database
        self._update_quest_database(player_id, quest_result)
        
        # Check if combat should trigger
        if quest_result.get('combat_trigger', False):
            combat_result = self._initiate_combat(player_data)
            
            # Merge quest and combat results
            return {
                **quest_result,
                "combat_initiated": True,
                "combat_narrative": combat_result['narrative'],
                "combat_choices": combat_result['choices']
            }
        
        # Generate AI narrative for this turn
        narrative = self._generate_turn_narrative(
            player_data,
            player_action,
            quest_result,
            ai_client
        )
        
        # Apply sanity effects if cosmic horror scenario
        if player_data['scenario'] == 'whispering_town':
            narrative = self._apply_sanity_effects(narrative, player_data)
        
        # Get next choices
        choices = self._generate_choices(quest_result, player_data)
        
        # Log game event
        self.db.log_game_event(
            player_id=player_id,
            turn_number=quest_result['turn_number'],
            event_type="story_progression",
            player_action=player_action,
            ai_response=narrative,
            quest_id=self.quest_engine.active_quest.quest_id if self.quest_engine.active_quest else None
        )
        
        # Update player last played
        self.db.update_player_stats(player_id, {'last_played': 'CURRENT_TIMESTAMP'})
        
        return {
            "success": True,
            "narrative": narrative,
            "choices": choices,
            "quest_state": quest_result,
            "player_stats": self.db.get_player(player_id),
            "sanity_state": self.sanity_engine.get_sanity_state_summary() if player_data['scenario'] == 'whispering_town' else None
        }
    
    # ========================================================================
    # COMBAT MANAGEMENT
    # ========================================================================
    
    def _initiate_combat(self, player_data: Dict) -> Dict[str, Any]:
        """Initiate a combat encounter"""
        scenario = player_data['scenario']
        
        # Select appropriate encounter based on scenario
        if scenario == 'whispering_town':
            enemies, environment, context = CombatEncounterLibrary.cosmic_horror_cultists()
        else:
            enemies, environment, context = CombatEncounterLibrary.bandit_ambush()
        
        # Create combat state
        encounter_id = f"combat_{random.randint(1000, 9999)}"
        self.current_combat = self.combat_engine.create_encounter(
            encounter_id=encounter_id,
            enemies=enemies,
            environment=environment,
            player_health=player_data['health'],
            player_max_health=player_data['max_health'],
            narrative_context=context
        )
        
        # Record in database
        self.combat_db_id = self.db.create_combat_encounter(
            player_id=player_data['player_id'],
            encounter_id=encounter_id,
            difficulty=self.combat_engine.difficulty.value,
            player_health=player_data['health'],
            enemies_data=[asdict(e) for e in enemies],
            environment_data=[asdict(env) for env in environment],
            quest_id=self.quest_engine.active_quest.quest_id if self.quest_engine.active_quest else None
        )
        
        # Generate combat choices
        choices = self._generate_combat_choices(self.current_combat)
        
        return {
            "narrative": f"⚔️ **COMBAT INITIATED**\n\n{context}",
            "choices": choices,
            "combat_state": {
                "enemies": [{"name": e.name, "health": e.health, "max_health": e.max_health} for e in enemies],
                "environment": [{"name": env.name, "description": env.description} for env in environment],
                "resources": {
                    "stamina": self.current_combat.resources.stamina,
                    "action_points": self.current_combat.resources.action_points
                }
            }
        }
    
    def _process_combat_turn(self, player_action: str, choice_index: int) -> Dict[str, Any]:
        """Process a combat turn"""
        if not self.current_combat:
            return {"error": "No active combat"}
        
        # Parse action from choice
        action_type, target_idx, env_idx = self._parse_combat_action(player_action, choice_index)
        
        # Get player stats
        player_data = self.db.get_player(self.player_id)
        player_stats = {
            'strength': player_data['strength'],
            'dexterity': player_data['dexterity'],
            'intelligence': player_data['intelligence'],
            'charisma': player_data['charisma'],
            'attack_bonus': (player_data['strength'] - 10) // 2
        }
        
        # Execute player action
        state, narrative, success = self.combat_engine.execute_action(
            self.current_combat,
            action_type,
            target_idx,
            env_idx,
            player_stats
        )
        
        self.current_combat = state
        
        # Check if combat ended
        is_over, outcome = state.is_combat_over()
        
        if is_over:
            return self._end_combat(outcome, narrative)
        
        # Process enemy turn
        state, enemy_narrative = self.combat_engine.process_enemy_turn(state)
        self.current_combat = state
        
        # Update player health in database
        self.db.update_player_stats(self.player_id, {'health': state.player_health})
        
        # Check again if combat ended
        is_over, outcome = state.is_combat_over()
        
        if is_over:
            combined_narrative = f"{narrative}\n\n{enemy_narrative}"
            return self._end_combat(outcome, combined_narrative)
        
        # Generate next combat choices
        choices = self._generate_combat_choices(state)
        
        return {
            "success": True,
            "narrative": f"{narrative}\n\n{enemy_narrative}",
            "choices": choices,
            "in_combat": True,
            "combat_state": {
                "turn": state.turn_number,
                "player_health": state.player_health,
                "enemies": [
                    {"name": e.name, "health": e.health, "is_alive": e.is_alive()} 
                    for e in state.enemies
                ],
                "resources": {
                    "stamina": state.resources.stamina,
                    "action_points": state.resources.action_points
                }
            }
        }
    
    def _end_combat(self, outcome: CombatOutcome, final_narrative: str) -> Dict[str, Any]:
        """End combat and clean up"""
        if not self.current_combat:
            return {"error": "No active combat"}
        
        # Generate outcome narrative
        outcome_narrative = self.combat_engine.generate_narrative_outcome(
            self.current_combat,
            outcome
        )
        
        # Update database
        if self.combat_db_id:
            self.db.update_combat_encounter(
                encounter_db_id=self.combat_db_id,
                outcome=outcome.value,
                turns_taken=self.current_combat.turn_number,
                player_health_end=self.current_combat.player_health,
                combat_log=self.current_combat.combat_log
            )
        
        # Update quest progression (combat completed)
        if self.quest_engine.active_quest:
            self.quest_engine.active_quest.progression.combat_encounters_completed += 1
        
        # Handle defeat
        if outcome == CombatOutcome.DEFEAT:
            # Failure-as-content: Player survives but with consequences
            self.db.update_player_stats(self.player_id, {'health': 1})  # Barely alive
            
            # Cosmic horror scenario: lose sanity on defeat
            player_data = self.db.get_player(self.player_id)
            if player_data['scenario'] == 'whispering_town':
                sanity_result = self.sanity_engine.process_sanity_loss(
                    amount=15,
                    cause="Combat defeat trauma"
                )
                self.db.record_sanity_event(
                    player_id=self.player_id,
                    event_type="combat_defeat",
                    sanity_change=-15,
                    old_sanity=sanity_result['current_sanity'] + 15,
                    new_sanity=sanity_result['current_sanity'],
                    old_level=sanity_result.get('old_level', 'stable'),
                    new_level=sanity_result['sanity_level'],
                    cause="Combat defeat trauma"
                )
                
                outcome_narrative += f"\n\n{sanity_result['narrative']}"
        
        # Clear combat state
        self.current_combat = None
        self.combat_db_id = None
        
        return {
            "success": True,
            "combat_ended": True,
            "outcome": outcome.value,
            "narrative": f"{final_narrative}\n\n{outcome_narrative}",
            "choices": ["Continue your journey", "Rest and recover", "Examine the aftermath"],
            "player_stats": self.db.get_player(self.player_id)
        }
    
    # ========================================================================
    # SANITY MECHANICS (Cosmic Horror)
    # ========================================================================
    
    def trigger_sanity_loss(
        self,
        player_id: str,
        amount: int,
        cause: str
    ) -> Dict[str, Any]:
        """Trigger sanity loss event"""
        result = self.sanity_engine.process_sanity_loss(amount, cause)
        
        # Update player sanity in database
        self.db.update_player_stats(
            player_id,
            {
                'sanity': result['current_sanity'],
                'corruption_level': int(result['corruption_level'])
            }
        )
        
        # Record sanity event
        self.db.record_sanity_event(
            player_id=player_id,
            event_type="sanity_loss",
            sanity_change=-amount,
            old_sanity=result['current_sanity'] + amount,
            new_sanity=result['current_sanity'],
            old_level=result.get('old_level', 'stable'),
            new_level=result['sanity_level'],
            cause=cause,
            hallucination_triggered=result.get('hallucination') is not None,
            distortions_added=result.get('new_distortions', [])
        )
        
        return result
    
    def learn_forbidden_knowledge(
        self,
        player_id: str,
        knowledge_id: str
    ) -> Dict[str, Any]:
        """Player learns forbidden knowledge"""
        result = self.sanity_engine.learn_forbidden_knowledge(knowledge_id)
        
        if 'error' in result:
            return result
        
        # Update player stats
        self.db.update_player_stats(
            player_id,
            {
                'sanity': result['current_sanity'],
                'corruption_level': int(result['corruption_level'])
            }
        )
        
        # Record knowledge acquisition
        knowledge = self.sanity_engine.knowledge_library[knowledge_id]
        self.db.record_forbidden_knowledge(
            player_id=player_id,
            knowledge_id=knowledge_id,
            title=knowledge.title,
            knowledge_type=knowledge.knowledge_type.value,
            sanity_cost=knowledge.sanity_cost,
            power_gain=knowledge.power_gain,
            corruption_level=knowledge.corruption_level
        )
        
        # Record sanity event
        self.db.record_sanity_event(
            player_id=player_id,
            event_type="knowledge_gained",
            sanity_change=-knowledge.sanity_cost,
            old_sanity=result['current_sanity'] + knowledge.sanity_cost,
            new_sanity=result['current_sanity'],
            old_level=result.get('old_level', 'stable'),
            new_level=result['sanity_level'],
            cause=f"Learning: {knowledge.title}",
            is_voluntary=True,
            hallucination_triggered=result.get('hallucination') is not None,
            distortions_added=result.get('new_distortions', [])
        )
        
        return result
    
    def _apply_sanity_effects(self, narrative: str, player_data: Dict) -> str:
        """Apply sanity-based text corruption to narrative"""
        return self.sanity_engine.apply_text_corruption(narrative)
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _update_quest_database(self, player_id: str, quest_result: Dict):
        """Update quest state in database"""
        if not self.quest_engine.active_quest:
            return
        
        quest = self.quest_engine.active_quest
        
        updates = {
            'current_turn': quest_result['turn_number'],
            'current_act': quest_result['current_act'],
            'status': quest_result['quest_status'],
            'milestones_completed': quest.progression.milestones_completed,
            'combat_encounters': quest.progression.combat_encounters_completed,
            'major_choices': len(quest.progression.get_major_choices()),
            'information_revealed': quest.progression.information_revealed
        }
        
        if quest_result.get('quest_completed'):
            updates['completed_at'] = 'CURRENT_TIMESTAMP'
        
        self.db.update_quest_state(player_id, quest.quest_id, updates)
    
    def _generate_turn_narrative(
        self,
        player_data: Dict,
        player_action: str,
        quest_result: Dict,
        ai_client: Optional[Any]
    ) -> str:
        """Generate AI narrative for turn (placeholder for AI integration)"""
        # TODO: Integrate with AI client for dynamic narrative generation
        # For now, return milestone narrative if available
        
        if quest_result.get('milestone_reached'):
            milestone = quest_result.get('milestone', {})
            return f"**{milestone.get('title', 'Next Step')}**\n\n{milestone.get('description', '')}"
        
        # Default narrative
        return f"You {player_action.lower()}. Your journey continues through turn {quest_result['turn_number']}."
    
    def _generate_choices(self, quest_result: Dict, player_data: Dict) -> List[str]:
        """Generate available choices for player"""
        if quest_result.get('milestone_reached'):
            milestone = quest_result.get('milestone', {})
            return milestone.get('choices', ["Continue", "Investigate", "Rest"])
        
        # Default choices
        return [
            "Continue forward",
            "Explore the area",
            "Rest and recover",
            "Check your surroundings"
        ]
    
    def _generate_combat_choices(self, combat_state: CombatState) -> List[str]:
        """Generate combat action choices"""
        choices = []
        
        # Add attack options for each living enemy
        for i, enemy in enumerate(combat_state.enemies):
            if enemy.is_alive():
                choices.append(f"⚔️ Attack {enemy.name}")
        
        # Add environmental options
        for i, env in enumerate(combat_state.environment):
            if env.can_use():
                choices.append(f"🌍 Use {env.name}")
        
        # Add standard actions
        choices.extend([
            "🛡️ Take defensive stance",
            "🗣️ Attempt negotiation",
            "🏃 Try to flee"
        ])
        
        return choices
    
    def _parse_combat_action(
        self,
        player_action: str,
        choice_index: int
    ) -> Tuple[ActionType, Optional[int], Optional[int]]:
        """Parse player combat action"""
        action_lower = player_action.lower()
        
        if "attack" in action_lower:
            # Extract target index from choice
            return ActionType.ATTACK, choice_index if choice_index < len(self.current_combat.enemies) else 0, None
        elif "use" in action_lower:
            return ActionType.USE_ENVIRONMENT, None, 0
        elif "defend" in action_lower or "defensive" in action_lower:
            return ActionType.DEFEND, None, None
        elif "negoti" in action_lower:
            return ActionType.NEGOTIATE, None, None
        elif "flee" in action_lower:
            return ActionType.FLEE, None, None
        else:
            return ActionType.ATTACK, 0, None
    
    # ========================================================================
    # SAVE/LOAD
    # ========================================================================
    
    def save_game(self, player_id: str, slot_number: int, save_name: str) -> bool:
        """Save complete game state"""
        player_data = self.db.get_player(player_id)
        if not player_data:
            return False
        
        quest_state = None
        if self.quest_engine.active_quest:
            quest_state = self.quest_engine.get_quest_state()
        
        game_state = {
            'scenario': player_data['scenario'],
            'turn_number': quest_state.get('turn_number', 0) if quest_state else 0,
            'player_state': player_data,
            'quest_state': quest_state,
            'sanity_state': self.sanity_engine.get_sanity_state_summary() if player_data['scenario'] == 'whispering_town' else None
        }
        
        return self.db.create_save(player_id, slot_number, save_name, game_state)
    
    def load_game(self, player_id: str, slot_number: int) -> Optional[Dict]:
        """Load complete game state"""
        return self.db.load_save(player_id, slot_number)

