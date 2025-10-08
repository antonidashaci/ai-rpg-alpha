"""
NPC Dialogue System for The Northern Realms
===========================================

Complete dialogue system featuring:
- Fantasy NPCs with distinct personalities
- Dynamic dialogue based on player choices
- Kingdom politics and faction relationships
- Quest-related conversations
- Reputation and relationship tracking

Design Philosophy:
- NPCs should feel alive and responsive
- Dialogue should reflect fantasy setting
- Player choices should affect NPC attitudes
- Conversations should advance quests and story
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random


class NPCRole(Enum):
    """NPC roles in the fantasy world"""
    KING = "king"
    GUARD = "guard"
    MERCHANT = "merchant"
    INNKEEPER = "innkeeper"
    MAGE = "mage"
    PRIEST = "priest"
    BLACKSMITH = "blacksmith"
    FARMER = "farmer"
    NOBLE = "noble"
    THIEF = "thief"
    DRAGON = "dragon"  # Special NPCs


class NPCPersonality(Enum):
    """NPC personality types"""
    NOBLE = "noble"          # Honorable, formal
    GRUFF = "gruff"          # Rough, straightforward
    MYSTERIOUS = "mysterious" # Cryptic, secretive
    FRIENDLY = "friendly"    # Warm, helpful
    SUSPICIOUS = "suspicious" # Distrustful, paranoid
    SCHOLARLY = "scholarly"  # Intelligent, analytical
    RELIGIOUS = "religious"  # Devout, moralistic
    GREEDY = "greedy"        # Self-serving, opportunistic


class DialogueMood(Enum):
    """NPC current mood affecting responses"""
    HOSTILE = "hostile"      # Angry, aggressive
    NEUTRAL = "neutral"      # Indifferent
    FRIENDLY = "friendly"    # Warm, cooperative
    FEARFUL = "fearful"      # Scared, submissive
    RESPECTFUL = "respectful" # Admiring, deferential


@dataclass
class DialogueNode:
    """
    Single dialogue node in conversation tree
    
    Contains:
    - NPC response text
    - Available player choices
    - Consequences of choices
    - Mood changes
    """
    node_id: str
    npc_text: str
    player_choices: List[str] = field(default_factory=list)
    
    # Consequences
    mood_change: Optional[DialogueMood] = None
    reputation_change: int = 0  # -10 to +10
    information_revealed: List[str] = field(default_factory=list)
    quest_progression: Optional[str] = None
    
    # Requirements
    required_reputation: int = 0
    required_quest_progress: Optional[str] = None
    
    def can_access(self, player_reputation: int, quest_state: Optional[str] = None) -> bool:
        """Check if player can access this dialogue node"""
        if player_reputation < self.required_reputation:
            return False
        
        if self.required_quest_progress and quest_state != self.required_quest_progress:
            return False
        
        return True


@dataclass
class NPCDefinition:
    """
    Complete NPC definition
    
    Contains personality, dialogue trees, and behavior
    """
    npc_id: str
    name: str
    role: NPCRole
    personality: NPCPersonality
    
    # Location and status
    location: str
    kingdom: str  # "ironhold", "stormwatch", "frostmere"
    
    # Relationships and reputation
    base_reputation: int = 0
    current_mood: DialogueMood = DialogueMood.NEUTRAL
    
    # Dialogue system
    dialogue_tree: Dict[str, DialogueNode] = field(default_factory=dict)
    current_node_id: str = "greeting"
    
    # Knowledge and secrets
    known_secrets: List[str] = field(default_factory=list)
    quest_knowledge: List[str] = field(default_factory=list)
    
    # Special abilities
    is_quest_giver: bool = False
    is_merchant: bool = False
    is_trainer: bool = False
    
    def get_greeting(self) -> str:
        """Get appropriate greeting based on personality and mood"""
        greetings = {
            NPCPersonality.NOBLE: {
                DialogueMood.HOSTILE: "What business do you have here, stranger?",
                DialogueMood.NEUTRAL: "Greetings, traveler. How may I assist you?",
                DialogueMood.FRIENDLY: "Ah, a welcome visitor! Please, make yourself comfortable.",
                DialogueMood.FEARFUL: "P-please, don't hurt me. I'll tell you anything!",
                DialogueMood.RESPECTFUL: "My lord/lady, it is an honor to speak with you."
            },
            NPCPersonality.GRUFF: {
                DialogueMood.HOSTILE: "What do you want? Make it quick.",
                DialogueMood.NEUTRAL: "Yeah? What can I do for you?",
                DialogueMood.FRIENDLY: "Good to see you! What brings you around?",
                DialogueMood.FEARFUL: "Easy there! I ain't lookin' for trouble.",
                DialogueMood.RESPECTFUL: "Sir/Ma'am, happy to help however I can."
            },
            NPCPersonality.MYSTERIOUS: {
                DialogueMood.HOSTILE: "You shouldn't be here. Leave before you regret it.",
                DialogueMood.NEUTRAL: "Interesting... what secrets do you carry?",
                DialogueMood.FRIENDLY: "You have the look of someone who understands deeper truths.",
                DialogueMood.FEARFUL: "The shadows whisper warnings about you...",
                DialogueMood.RESPECTFUL: "Your wisdom is evident. I shall share what I know."
            }
        }
        
        return greetings.get(self.personality, {}).get(
            self.current_mood,
            "Hello there."
        )
    
    def get_dialogue_options(self, player_reputation: int, quest_state: str = "") -> List[str]:
        """Get available dialogue choices for current node"""
        current_node = self.dialogue_tree.get(self.current_node_id)
        if not current_node:
            return ["Goodbye"]
        
        # Filter choices based on requirements
        available_choices = []
        for choice in current_node.player_choices:
            # Check if this is a simple response or a node reference
            if choice.startswith("->"):
                node_id = choice[2:]
                if node_id in self.dialogue_tree:
                    node = self.dialogue_tree[node_id]
                    if node.can_access(player_reputation, quest_state):
                        available_choices.append(f"\"{node.npc_text[:50]}...\"")
            else:
                available_choices.append(choice)
        
        return available_choices
    
    def process_choice(self, choice: str, player_reputation: int) -> Dict[str, any]:
        """Process player dialogue choice"""
        current_node = self.dialogue_tree.get(self.current_node_id)
        if not current_node:
            return {
                "npc_response": "I have nothing more to say.",
                "choices": ["Goodbye"],
                "reputation_change": 0,
                "mood_change": None
            }
        
        # Handle special choices
        if choice == "Goodbye":
            return {
                "npc_response": "Farewell, traveler.",
                "choices": [],
                "reputation_change": 0,
                "mood_change": None,
                "conversation_ended": True
            }
        
        # Find matching dialogue node
        next_node_id = None
        for node_choice in current_node.player_choices:
            if node_choice.startswith("->"):
                node_id = node_choice[2:]
                if node_id in self.dialogue_tree:
                    node = self.dialogue_tree[node_id]
                    if node.can_access(player_reputation):
                        next_node_id = node_id
                        break
        
        if not next_node_id:
            return {
                "npc_response": "I'm not sure I understand.",
                "choices": current_node.player_choices,
                "reputation_change": -1,
                "mood_change": DialogueMood.HOSTILE
            }
        
        next_node = self.dialogue_tree[next_node_id]
        
        # Update NPC mood if specified
        if next_node.mood_change:
            self.current_mood = next_node.mood_change
        
        return {
            "npc_response": next_node.npc_text,
            "choices": next_node.player_choices,
            "reputation_change": next_node.reputation_change,
            "mood_change": next_node.mood_change,
            "information_revealed": next_node.information_revealed,
            "quest_progression": next_node.quest_progression
        }


class DialogueEngine:
    """
    Engine for managing NPC conversations and relationships
    
    Handles:
    - Dynamic dialogue based on player reputation and quest state
    - NPC relationship management
    - Quest-related conversations
    - Kingdom politics and faction relationships
    """
    
    def __init__(self):
        self.npc_library: Dict[str, NPCDefinition] = {}
        self._initialize_npc_library()
    
    def _initialize_npc_library(self):
        """Initialize complete NPC library for The Northern Realms"""
        
        # ========================================================================
        # IRONHOLD KINGDOM NPCs
        # ========================================================================
        
        # King Alaric Ironhold - The ruler of Ironhold
        king_alaric = NPCDefinition(
            npc_id="king_alaric",
            name="King Alaric Ironhold",
            role=NPCRole.KING,
            personality=NPCPersonality.NOBLE,
            location="Ironhold Castle",
            kingdom="ironhold",
            base_reputation=5,
            current_mood=DialogueMood.RESPECTFUL,
            is_quest_giver=True,
            known_secrets=["dragon_prophecy", "kingdom_betrayal"],
            quest_knowledge=["dragon_threat"]
        )
        
        # Build dialogue tree for King Alaric
        king_alaric.dialogue_tree = {
            "greeting": DialogueNode(
                node_id="greeting",
                npc_text="Welcome to Ironhold Castle, chosen one. I have awaited your arrival.",
                player_choices=[
                    "->prophecy_discussion",
                    "->kingdom_status",
                    "->dragon_threat",
                    "Goodbye"
                ]
            ),
            
            "prophecy_discussion": DialogueNode(
                node_id="prophecy_discussion",
                npc_text=(
                    "The prophecy speaks of you—the marked one who will unite the kingdoms. "
                    "The dragons stir in their ancient lairs, and old grudges threaten to doom us all."
                ),
                player_choices=[
                    "->pledge_allegiance",
                    "->ask_about_dragons",
                    "->discuss_unification"
                ],
                mood_change=DialogueMood.RESPECTFUL,
                reputation_change=2,
                information_revealed=["prophecy_details"]
            ),
            
            "pledge_allegiance": DialogueNode(
                node_id="pledge_allegiance",
                npc_text=(
                    "I pledge Ironhold's full support to your cause. Our armies, our mages, "
                    "our resources—they are yours to command. Together, we shall face the dragon threat."
                ),
                player_choices=[
                    "->request_military_aid",
                    "->ask_about_allies"
                ],
                mood_change=DialogueMood.FRIENDLY,
                reputation_change=5,
                quest_progression="ironhold_allied"
            ),
            
            "kingdom_status": DialogueNode(
                node_id="kingdom_status",
                npc_text=(
                    "Ironhold stands strong, but our people grow restless. "
                    "Trade caravans have been attacked, and whispers of dragon sightings grow louder."
                ),
                player_choices=[
                    "->offer_help",
                    "->inquire_about_trade"
                ],
                reputation_change=1
            ),
            
            "dragon_threat": DialogueNode(
                node_id="dragon_threat",
                npc_text=(
                    "The dragons are no mere beasts. They are ancient, intelligent creatures "
                    "who remember the betrayals of five centuries past. They will not be easily defeated."
                ),
                player_choices=[
                    "->ask_about_history",
                    "->discuss_strategy"
                ],
                information_revealed=["dragon_intelligence"],
                reputation_change=1
            )
        }
        
        # ========================================================================
        # STORMWATCH NPCs
        # ========================================================================
        
        # Captain Thorne - Stormwatch Guard Captain
        captain_thorne = NPCDefinition(
            npc_id="captain_thorne",
            name="Captain Thorne",
            role=NPCRole.GUARD,
            personality=NPCPersonality.GRUFF,
            location="Stormwatch Keep",
            kingdom="stormwatch",
            base_reputation=0,
            current_mood=DialogueMood.SUSPICIOUS,
            known_secrets=["stormwatch_plot"],
            quest_knowledge=["dragon_attacks"]
        )
        
        captain_thorne.dialogue_tree = {
            "greeting": DialogueNode(
                node_id="greeting",
                npc_text="State your business here, stranger. Stormwatch doesn't take kindly to outsiders.",
                player_choices=[
                    "->explain_quest",
                    "->mention_prophecy",
                    "->offer_help",
                    "Goodbye"
                ]
            ),
            
            "explain_quest": DialogueNode(
                node_id="explain_quest",
                npc_text=(
                    "The prophecy? I've heard tales, but I don't put much stock in old legends. "
                    "We deal with real threats here—bandits, monsters, and the occasional dragon sighting."
                ),
                player_choices=[
                    "->report_dragon_sighting",
                    "->ask_about_defenses"
                ],
                reputation_change=1
            )
        }
        
        # ========================================================================
        # FROSTMERE NPCs
        # ========================================================================
        
        # High Mage Elara - Frostmere Court Mage
        mage_elara = NPCDefinition(
            npc_id="mage_elara",
            name="High Mage Elara",
            role=NPCRole.MAGE,
            personality=NPCPersonality.SCHOLARLY,
            location="Frostmere Citadel",
            kingdom="frostmere",
            base_reputation=3,
            current_mood=DialogueMood.NEUTRAL,
            is_trainer=True,
            known_secrets=["ancient_magic", "dragon_weaknesses"],
            quest_knowledge=["prophecy_truth"]
        )
        
        mage_elara.dialogue_tree = {
            "greeting": DialogueNode(
                node_id="greeting",
                npc_text=(
                    "Greetings, traveler. I am High Mage Elara of Frostmere. "
                    "Your magical aura is... interesting. How may the arcane arts serve you?"
                ),
                player_choices=[
                    "->ask_about_magic",
                    "->inquire_about_dragons",
                    "->request_training",
                    "Goodbye"
                ]
            ),
            
            "ask_about_magic": DialogueNode(
                node_id="ask_about_magic",
                npc_text=(
                    "Magic is the foundation of reality itself. In Frostmere, we specialize in "
                    "cryomancy and protective wards. The dragons fear our ice magic above all else."
                ),
                player_choices=[
                    "->learn_ice_magic",
                    "->discuss_dragon_weaknesses"
                ],
                information_revealed=["ice_magic_lore"],
                reputation_change=2
            ),
            
            "request_training": DialogueNode(
                node_id="request_training",
                npc_text=(
                    "You show promise in the arcane arts. I can teach you spells of frost and protection, "
                    "but such knowledge comes at a price. Are you willing to learn?"
                ),
                player_choices=[
                    "->accept_training",
                    "->decline_politely"
                ],
                required_reputation=5
            )
        }
        
        # ========================================================================
        # DRAGON NPCs (Special)
        # ========================================================================
        
        # Crimsonwing - Ancient Red Dragon
        crimsonwing = NPCDefinition(
            npc_id="crimsonwing",
            name="Crimsonwing",
            role=NPCRole.DRAGON,
            personality=NPCPersonality.MYSTERIOUS,
            location="Dragon's Lair",
            kingdom="none",
            base_reputation=-10,
            current_mood=DialogueMood.HOSTILE,
            known_secrets=["dragon_history", "human_betrayal"],
            quest_knowledge=["prophecy_truth"]
        )
        
        crimsonwing.dialogue_tree = {
            "greeting": DialogueNode(
                node_id="greeting",
                npc_text=(
                    "So... the marked one finally comes. I have waited centuries for this moment. "
                    "Your kind betrayed us once. Will you repeat history?"
                ),
                player_choices=[
                    "->negotiate_peace",
                    "->challenge_dragon",
                    "->ask_about_history"
                ],
                required_reputation=-5  # Only accessible after certain quest progress
            ),
            
            "negotiate_peace": DialogueNode(
                node_id="negotiate_peace",
                npc_text=(
                    "Peace? After what your ancestors did to us? The burning, the slaughter, "
                    "the broken oaths? You would ask for peace now?"
                ),
                player_choices=[
                    "->offer_compensation",
                    "->propose_alliance"
                ],
                required_reputation=5
            )
        }
        
        # ========================================================================
        # COMMON NPCs
        # ========================================================================
        
        # Village Blacksmith - Generic helpful NPC
        blacksmith = NPCDefinition(
            npc_id="blacksmith_grom",
            name="Grom the Blacksmith",
            role=NPCRole.BLACKSMITH,
            personality=NPCPersonality.GRUFF,
            location="Ironhold Village",
            kingdom="ironhold",
            base_reputation=2,
            current_mood=DialogueMood.FRIENDLY,
            is_merchant=True
        )
        
        blacksmith.dialogue_tree = {
            "greeting": DialogueNode(
                node_id="greeting",
                npc_text="Well met, traveler! Grom's the name, and hammerin' metal's my game.",
                player_choices=[
                    "->ask_about_weapons",
                    "->inquire_about_armor",
                    "->village_gossip",
                    "Goodbye"
                ]
            ),
            
            "ask_about_weapons": DialogueNode(
                node_id="ask_about_weapons",
                npc_text=(
                    "Weapons? Aye, I forge the finest blades in Ironhold. "
                    "But for dragon-slaying, you'll need something special..."
                ),
                player_choices=[
                    "->commission_weapon",
                    "->ask_about_materials"
                ]
            )
        }
        
        # Store NPCs in library
        self.npc_library = {
            "king_alaric": king_alaric,
            "captain_thorne": captain_thorne,
            "mage_elara": mage_elara,
            "crimsonwing": crimsonwing,
            "blacksmith_grom": blacksmith
        }
    
    def get_npc(self, npc_id: str) -> Optional[NPCDefinition]:
        """Get NPC by ID"""
        return self.npc_library.get(npc_id)
    
    def get_npcs_by_location(self, location: str) -> List[NPCDefinition]:
        """Get all NPCs in a location"""
        return [
            npc for npc in self.npc_library.values()
            if npc.location == location
        ]
    
    def get_npcs_by_kingdom(self, kingdom: str) -> List[NPCDefinition]:
        """Get all NPCs in a kingdom"""
        return [
            npc for npc in self.npc_library.values()
            if npc.kingdom == kingdom
        ]
    
    def get_quest_givers(self) -> List[NPCDefinition]:
        """Get NPCs who can give quests"""
        return [
            npc for npc in self.npc_library.values()
            if npc.is_quest_giver
        ]
    
    def process_conversation(
        self,
        npc_id: str,
        player_choice: str,
        player_reputation: int,
        quest_state: str = ""
    ) -> Dict[str, any]:
        """Process a complete conversation turn"""
        npc = self.get_npc(npc_id)
        if not npc:
            return {"error": "NPC not found"}
        
        # Get NPC response to choice
        result = npc.process_choice(player_choice, player_reputation)
        
        # Update NPC mood if changed
        if result.get("mood_change"):
            npc.current_mood = result["mood_change"]
        
        # Add NPC context to response
        result.update({
            "npc_id": npc_id,
            "npc_name": npc.name,
            "npc_mood": npc.current_mood.value,
            "location": npc.location,
            "kingdom": npc.kingdom
        })
        
        return result
    
    def update_npc_relationship(self, npc_id: str, reputation_change: int):
        """Update relationship with NPC"""
        npc = self.get_npc(npc_id)
        if npc:
            npc.current_mood = self._calculate_new_mood(
                npc.current_mood,
                npc.base_reputation + reputation_change
            )
    
    def _calculate_new_mood(self, current_mood: DialogueMood, reputation: int) -> DialogueMood:
        """Calculate new mood based on reputation"""
        if reputation >= 15:
            return DialogueMood.FRIENDLY
        elif reputation >= 5:
            return DialogueMood.RESPECTFUL
        elif reputation >= -5:
            return DialogueMood.NEUTRAL
        elif reputation >= -15:
            return DialogueMood.FEARFUL
        else:
            return DialogueMood.HOSTILE


# ============================================================================
# DIALOGUE UTILITIES
# ============================================================================

class DialogueUtils:
    """Utility functions for dialogue system"""
    
    @staticmethod
    def format_npc_name(npc: NPCDefinition) -> str:
        """Format NPC name with title based on role"""
        titles = {
            NPCRole.KING: "King",
            NPCRole.GUARD: "Captain",
            NPCRole.MAGE: "High Mage",
            NPCRole.PRIEST: "High Priest",
            NPCRole.BLACKSMITH: "Master",
            NPCRole.NOBLE: "Lord/Lady"
        }
        
        title = titles.get(npc.role, "")
        return f"{title} {npc.name}" if title else npc.name
    
    @staticmethod
    def get_personality_greeting(personality: NPCPersonality) -> str:
        """Get appropriate greeting for personality"""
        greetings = {
            NPCPersonality.NOBLE: "Well met, traveler.",
            NPCPersonality.GRUFF: "What do you want?",
            NPCPersonality.MYSTERIOUS: "You seek knowledge...",
            NPCPersonality.FRIENDLY: "Hello there, friend!",
            NPCPersonality.SUSPICIOUS: "Who are you?",
            NPCPersonality.SCHOLARLY: "Fascinating specimen...",
            NPCPersonality.RELIGIOUS: "May the gods bless you.",
            NPCPersonality.GREEDY: "What can you offer me?"
        }
        
        return greetings.get(personality, "Hello.")

