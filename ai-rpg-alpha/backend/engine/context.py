"""
AI-RPG-Alpha: Game Context Builder

This module builds comprehensive context for AI narrative generation.
It aggregates player state, memories, quests, and world information
to provide rich context for consistent storytelling.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from models.dataclasses import Player, Quest, Memory, GameEvent
from dao.game_state import GameStateDAO
from dao.memory import MemoryDAO
from ai.templates import PromptTemplates

class GameContextBuilder:
    """
    Builds comprehensive context for AI narrative generation.
    
    Aggregates all relevant game state information including player data,
    memories, quests, events, and world state to provide rich context
    for consistent AI-generated narratives.
    """
    
    def __init__(self, game_dao: GameStateDAO, memory_dao: MemoryDAO):
        """
        Initialize the context builder with data access objects.
        
        Args:
            game_dao: Game state data access object
            memory_dao: Memory data access object
        """
        self.game_dao = game_dao
        self.memory_dao = memory_dao
        self.templates = PromptTemplates()
        
        # World state configuration
        self.world_config = {
            "locations": {
                "starting_village": {
                    "name": "Millbrook Village",
                    "description": "A peaceful farming village surrounded by rolling hills",
                    "npcs": ["Village Elder", "Merchant", "Blacksmith"],
                    "available_quests": ["village_defense", "lost_livestock"]
                },
                "forest_entrance": {
                    "name": "Whispering Woods Entrance",
                    "description": "The edge of an ancient forest filled with mystery",
                    "npcs": ["Forest Ranger"],
                    "available_quests": ["forest_exploration", "herb_gathering"]
                },
                "ancient_ruins": {
                    "name": "Forgotten Temple Ruins",
                    "description": "Crumbling stone structures from a lost civilization",
                    "npcs": ["Archaeologist", "Guardian Spirit"],
                    "available_quests": ["artifact_recovery", "spirit_communion"]
                }
            },
            "time_progression": {
                "dawn": "The first light of dawn breaks across the horizon",
                "morning": "The morning sun climbs steadily in the clear sky",
                "midday": "The sun reaches its zenith, casting short shadows",
                "afternoon": "The afternoon sun begins its descent westward",
                "evening": "Golden evening light bathes the landscape",
                "night": "Stars twinkle in the dark sky above"
            },
            "weather_patterns": [
                "clear", "cloudy", "light rain", "heavy rain", "fog", "windy"
            ]
        }
    
    def build_full_context(
        self, 
        player_id: str, 
        current_choice: str = "",
        include_memories: bool = True,
        memory_limit: int = 5
    ) -> Dict[str, Any]:
        """
        Build comprehensive context for AI narrative generation.
        
        Args:
            player_id: ID of the player
            current_choice: Player's current choice/action
            include_memories: Whether to include memory context
            memory_limit: Maximum number of memories to include
            
        Returns:
            Dictionary containing all context information
        """
        # Get player data
        player = self.game_dao.get_player(player_id)
        if not player:
            return self._get_default_context()
        
        # Get relevant memories
        memories = []
        if include_memories:
            if current_choice:
                # Get memories similar to current choice
                memories = self.memory_dao.retrieve_memories(
                    current_choice, player_id, memory_limit
                )
            else:
                # Get recent memories
                memories = self.memory_dao.get_recent_memories(
                    player_id, memory_limit
                )
        
        # Get active quests
        active_quests = []
        for quest_id in player.active_quests:
            quest = self.game_dao.get_quest(quest_id)
            if quest:
                active_quests.append(quest)
        
        # Get recent events
        recent_events = self.game_dao.get_player_events(player_id, limit=10)
        
        # Get location information
        location_info = self.world_config["locations"].get(
            player.current_location, 
            {"name": player.current_location, "description": "An unknown place"}
        )
        
        # Determine time and weather
        time_of_day = self._get_time_of_day(player.turn_number)
        weather = self._get_weather(player.turn_number, player.current_location)
        
        # Build context dictionary
        context = {
            "player": {
                "id": player.id,
                "name": player.name,
                "stats": player.stats.__dict__,
                "inventory": player.inventory,
                "active_quests": player.active_quests,
                "completed_quests": player.completed_quests,
                "current_location": player.current_location,
                "turn_number": player.turn_number,
                "last_choice": player.last_choice
            },
            "memories": [
                {
                    "content": memory.content,
                    "turn_number": memory.turn_number,
                    "importance": memory.importance
                } for memory in memories
            ],
            "active_quests": [
                {
                    "id": quest.id,
                    "title": quest.title,
                    "objectives": quest.objectives,
                    "status": quest.status.value,
                    "risk": quest.risk.value
                } for quest in active_quests
            ],
            "recent_events": [
                {
                    "event_type": event.event_type,
                    "description": event.description,
                    "turn_number": event.turn_number
                } for event in recent_events[-5:]  # Last 5 events
            ],
            "location": {
                "name": location_info["name"],
                "description": location_info["description"],
                "npcs": location_info.get("npcs", []),
                "available_quests": location_info.get("available_quests", [])
            },
            "world_state": {
                "time_of_day": time_of_day,
                "weather": weather,
                "turn_number": player.turn_number
            },
            "current_choice": current_choice
        }
        
        return context
    
    def build_narrative_context(
        self, 
        player_id: str, 
        situation_description: str,
        player_choice: str
    ) -> str:
        """
        Build context specifically for narrative generation.
        
        Args:
            player_id: ID of the player
            situation_description: Description of current situation
            player_choice: Player's chosen action
            
        Returns:
            Formatted context string for AI prompt
        """
        context = self.build_full_context(player_id, player_choice)
        
        # Get active quest for template
        active_quest = None
        if context["active_quests"]:
            active_quest = context["active_quests"][0]  # Primary active quest
        
        # Render using template
        return self.templates.render_narrative_prompt(
            player=context["player"],
            current_situation=situation_description,
            player_choice=player_choice,
            recent_memories=context["memories"],
            active_quest=active_quest
        )
    
    def build_choice_context(self, player_id: str, narrative: str) -> str:
        """
        Build context for choice generation.
        
        Args:
            player_id: ID of the player
            narrative: Current narrative text
            
        Returns:
            Formatted context string for choice generation
        """
        context = self.build_full_context(player_id, include_memories=False)
        
        return self.templates.render_choices_prompt(
            narrative=narrative,
            player=context["player"]
        )
    
    def get_location_context(self, location: str) -> Dict[str, Any]:
        """
        Get detailed context for a specific location.
        
        Args:
            location: Location identifier
            
        Returns:
            Location context dictionary
        """
        return self.world_config["locations"].get(
            location,
            {
                "name": location,
                "description": "An unexplored area",
                "npcs": [],
                "available_quests": []
            }
        )
    
    def update_world_state(
        self, 
        player_id: str, 
        changes: Dict[str, Any]
    ) -> bool:
        """
        Update world state based on player actions.
        
        Args:
            player_id: ID of the player
            changes: Dictionary of changes to apply
            
        Returns:
            True if successful, False otherwise
        """
        try:
            player = self.game_dao.get_player(player_id)
            if not player:
                return False
            
            # Apply stat changes
            if "stats" in changes:
                for stat, change in changes["stats"].items():
                    if hasattr(player.stats, stat):
                        current_value = getattr(player.stats, stat)
                        setattr(player.stats, stat, max(0, current_value + change))
            
            # Apply inventory changes
            if "inventory" in changes:
                if "add" in changes["inventory"]:
                    player.inventory.extend(changes["inventory"]["add"])
                if "remove" in changes["inventory"]:
                    for item in changes["inventory"]["remove"]:
                        if item in player.inventory:
                            player.inventory.remove(item)
            
            # Apply location change
            if "location" in changes:
                player.current_location = changes["location"]
            
            # Update player in database
            return self.game_dao.update_player(player)
            
        except Exception as e:
            print(f"Error updating world state: {e}")
            return False
    
    def _get_time_of_day(self, turn_number: int) -> str:
        """
        Determine time of day based on turn number.
        
        Args:
            turn_number: Current turn number
            
        Returns:
            Time of day string
        """
        time_cycle = ["dawn", "morning", "midday", "afternoon", "evening", "night"]
        return time_cycle[turn_number % len(time_cycle)]
    
    def _get_weather(self, turn_number: int, location: str) -> str:
        """
        Determine weather based on turn number and location.
        
        Args:
            turn_number: Current turn number
            location: Current location
            
        Returns:
            Weather description string
        """
        # Simple weather system based on turn number and location
        weather_patterns = self.world_config["weather_patterns"]
        
        # Different locations have different weather tendencies
        location_modifiers = {
            "forest_entrance": 1,  # More likely to be foggy/rainy
            "ancient_ruins": 2,    # More mysterious weather
            "starting_village": 0  # Generally clear
        }
        
        modifier = location_modifiers.get(location, 0)
        weather_index = (turn_number + modifier) % len(weather_patterns)
        return weather_patterns[weather_index]
    
    def _get_default_context(self) -> Dict[str, Any]:
        """
        Get default context when player is not found.
        
        Returns:
            Default context dictionary
        """
        return {
            "player": {
                "id": "unknown",
                "name": "Unknown Adventurer",
                "stats": {"health": 100, "level": 1},
                "inventory": [],
                "current_location": "starting_village",
                "turn_number": 0
            },
            "memories": [],
            "active_quests": [],
            "recent_events": [],
            "location": {
                "name": "Unknown Location",
                "description": "You find yourself in an unfamiliar place",
                "npcs": [],
                "available_quests": []
            },
            "world_state": {
                "time_of_day": "morning",
                "weather": "clear",
                "turn_number": 0
            },
            "current_choice": ""
        }

