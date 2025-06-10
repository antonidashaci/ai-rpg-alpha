"""
AI-RPG-Alpha: Consequence Types and Enums

This module contains the type definitions and enums used by the consequence system.
Separated from the main consequence scheduler to maintain the 500-line limit.
"""

from enum import Enum

class ConsequenceTrigger(Enum):
    """Types of consequence triggers"""
    TURN_BASED = "turn_based"          # Triggers after X turns
    LOCATION_BASED = "location_based"  # Triggers when entering location
    QUEST_BASED = "quest_based"        # Triggers on quest completion/failure
    STAT_BASED = "stat_based"          # Triggers when stat reaches threshold
    TIME_BASED = "time_based"          # Triggers after real time delay
    CHOICE_BASED = "choice_based"      # Triggers on specific choice

class ConsequenceType(Enum):
    """Types of consequences"""
    NARRATIVE = "narrative"            # Story event
    STAT_CHANGE = "stat_change"        # Modify player stats
    INVENTORY = "inventory"            # Add/remove items
    QUEST_UNLOCK = "quest_unlock"      # Make new quest available
    LOCATION_CHANGE = "location_change" # Force location change
    NPC_INTERACTION = "npc_interaction" # Trigger NPC event
    WORLD_STATE = "world_state"        # Change world state 