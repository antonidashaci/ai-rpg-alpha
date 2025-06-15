"""
AI-RPG-Alpha: Consequence Handlers

This module contains the handler methods for different types of consequences.
Separated from the main consequence scheduler to maintain the 500-line limit.
"""

from typing import Dict, Any, Optional
from models.dataclasses import Player
from dao.game_state import GameStateDAO

class ConsequenceHandlers:
    """
    Handles the execution of different types of consequences.
    
    Contains methods for processing narrative, stat changes, inventory,
    quest unlocks, location changes, NPC interactions, and world state changes.
    """
    
    def __init__(self, game_dao: GameStateDAO):
        """
        Initialize the consequence handlers.
        
        Args:
            game_dao: Game state data access object
        """
        self.game_dao = game_dao
    
    def handle_narrative_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle narrative consequences (story events).
        
        Args:
            data: Consequence data containing narrative information
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with narrative content
        """
        return {
            "type": "narrative",
            "content": data.get("narrative_text", "A consequence unfolds..."),
            "title": data.get("title", "Consequence"),
            "priority": data.get("display_priority", "normal")
        }
    
    def handle_stat_change_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle stat change consequences.
        
        Args:
            data: Consequence data containing stat changes
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with stat change information
        """
        changes_made = {}
        
        # Apply stat changes
        for stat_name, change_value in data.get("stats", {}).items():
            if hasattr(player, stat_name):
                old_value = getattr(player, stat_name)
                new_value = max(0, old_value + change_value)  # Prevent negative stats
                setattr(player, stat_name, new_value)
                changes_made[stat_name] = {
                    "old": old_value,
                    "new": new_value,
                    "change": change_value
                }
        
        # Update player in database
        self.game_dao.update_player(player)
        
        return {
            "type": "stat_change",
            "changes": changes_made,
            "message": data.get("message", "Your stats have changed.")
        }
    
    def handle_inventory_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle inventory consequences (add/remove items).
        
        Args:
            data: Consequence data containing inventory changes
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with inventory change information
        """
        items_added = []
        items_removed = []
        
        # Add items
        for item in data.get("add_items", []):
            if isinstance(item, str):
                player.inventory.append(item)
                items_added.append(item)
            elif isinstance(item, dict):
                item_name = item.get("name", "unknown_item")
                quantity = item.get("quantity", 1)
                for _ in range(quantity):
                    player.inventory.append(item_name)
                items_added.append(f"{item_name} x{quantity}")
        
        # Remove items
        for item in data.get("remove_items", []):
            if item in player.inventory:
                player.inventory.remove(item)
                items_removed.append(item)
        
        # Update player in database
        self.game_dao.update_player(player)
        
        return {
            "type": "inventory",
            "added": items_added,
            "removed": items_removed,
            "message": data.get("message", "Your inventory has changed.")
        }
    
    def handle_quest_unlock_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle quest unlock consequences.
        
        Args:
            data: Consequence data containing quest information
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with quest unlock information
        """
        quest_id = data.get("quest_id")
        if not quest_id:
            return {"type": "quest_unlock", "success": False, "error": "No quest ID provided"}
        
        # Check if quest exists and is not already unlocked
        quest = self.game_dao.get_quest(quest_id)
        if not quest:
            return {"type": "quest_unlock", "success": False, "error": "Quest not found"}
        
        # Add quest to player's available quests if not already present
        if quest_id not in player.available_quests:
            player.available_quests.append(quest_id)
            self.game_dao.update_player(player)
            
            return {
                "type": "quest_unlock",
                "success": True,
                "quest_title": quest.title,
                "quest_id": quest_id,
                "message": data.get("message", f"New quest available: {quest.title}")
            }
        
        return {"type": "quest_unlock", "success": False, "error": "Quest already available"}
    
    def handle_location_change_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle location change consequences.
        
        Args:
            data: Consequence data containing location information
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with location change information
        """
        new_location = data.get("location")
        if not new_location:
            return {"type": "location_change", "success": False, "error": "No location provided"}
        
        old_location = player.location
        player.location = new_location
        
        # Update player in database
        self.game_dao.update_player(player)
        
        return {
            "type": "location_change",
            "success": True,
            "old_location": old_location,
            "new_location": new_location,
            "message": data.get("message", f"You have been moved to {new_location}")
        }
    
    def handle_npc_interaction_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle NPC interaction consequences.
        
        Args:
            data: Consequence data containing NPC information
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with NPC interaction information
        """
        npc_id = data.get("npc_id")
        interaction_type = data.get("interaction_type", "dialogue")
        
        return {
            "type": "npc_interaction",
            "npc_id": npc_id,
            "interaction_type": interaction_type,
            "dialogue": data.get("dialogue", "An NPC approaches you."),
            "message": data.get("message", f"Interaction with {npc_id}")
        }
    
    def handle_world_state_consequence(
        self,
        data: Dict[str, Any],
        player: Player,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Handle world state consequences.
        
        Args:
            data: Consequence data containing world state changes
            player: Player object
            context: Current game context
            
        Returns:
            Result dictionary with world state change information
        """
        state_changes = data.get("state_changes", {})
        
        # Apply world state changes
        for state_key, state_value in state_changes.items():
            # Store world state changes in game state
            # This would typically update a world state table
            pass
        
        return {
            "type": "world_state",
            "changes": state_changes,
            "message": data.get("message", "The world around you changes.")
        } 