"""
AI-RPG-Alpha: Advanced Companion System

Sophisticated companion system with recruitable characters, party dynamics,
deep relationships, romance options, and companion-specific questlines.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime


class CompanionType(Enum):
    """Types of companions"""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    HEALER = "healer"
    SCHOLAR = "scholar"
    RANGER = "ranger"
    BARD = "bard"
    MYSTIC = "mystic"


class RelationshipStatus(Enum):
    """Relationship status with companion"""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    ROMANTIC_INTEREST = "romantic_interest"
    LOVER = "lover"
    RIVAL = "rival"
    ENEMY = "enemy"


class CompanionMood(Enum):
    """Current mood of companion"""
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    ANNOYED = "annoyed"
    ANGRY = "angry"
    SAD = "sad"
    EXCITED = "excited"
    WORRIED = "worried"


@dataclass
class CompanionPersonality:
    """Companion's personality traits and preferences"""
    primary_traits: List[str] = field(default_factory=list)
    moral_alignment: str = "neutral"  # lawful_good, chaotic_evil, etc.
    
    # Preferences
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    
    # Values and beliefs
    core_values: List[str] = field(default_factory=list)
    prejudices: List[str] = field(default_factory=list)
    
    # Social preferences
    leadership_style: str = "collaborative"
    conflict_resolution: str = "diplomatic"
    humor_type: str = "witty"


@dataclass
class CompanionRelationship:
    """Relationship data between companion and player/other companions"""
    target_id: str
    relationship_type: RelationshipStatus = RelationshipStatus.STRANGER
    
    # Relationship metrics (0-100)
    trust: int = 50
    affection: int = 50
    respect: int = 50
    loyalty: int = 50
    
    # Romantic relationship specific
    romance_stage: int = 0  # 0-10 progression
    romance_locked: bool = False
    
    # History
    first_meeting: str = ""
    relationship_history: List[str] = field(default_factory=list)
    shared_experiences: List[str] = field(default_factory=list)
    
    # Current state
    recent_interactions: List[str] = field(default_factory=list)
    last_conversation: str = ""


@dataclass
class CompanionQuest:
    """Personal quest for a companion"""
    id: str
    companion_id: str
    title: str
    description: str
    
    # Quest details
    quest_type: str  # "personal_history", "family", "revenge", "redemption"
    current_stage: int = 0
    total_stages: int = 3
    
    # Requirements
    required_relationship: RelationshipStatus = RelationshipStatus.FRIEND
    location_requirements: List[str] = field(default_factory=list)
    
    # Story elements
    backstory_revealed: List[str] = field(default_factory=list)
    character_growth: List[str] = field(default_factory=list)
    
    # Outcomes
    possible_endings: List[str] = field(default_factory=list)
    relationship_impacts: Dict[str, int] = field(default_factory=dict)


@dataclass
class PartyDynamics:
    """Dynamics between party members"""
    tension_level: float = 0.0  # 0.0 to 1.0
    cohesion: float = 0.5
    leadership_conflicts: List[str] = field(default_factory=list)
    
    # Inter-companion relationships
    companion_relationships: Dict[str, Dict[str, int]] = field(default_factory=dict)
    
    # Group events
    bonding_moments: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)


@dataclass
class Companion:
    """A recruitable companion character"""
    id: str
    name: str
    companion_type: CompanionType
    
    # Basic info
    age: int
    background: str
    origin_location: str
    
    # Personality
    personality: CompanionPersonality = field(default_factory=CompanionPersonality)
    current_mood: CompanionMood = CompanionMood.NEUTRAL
    
    # Relationships
    player_relationship: CompanionRelationship = field(default_factory=lambda: CompanionRelationship("player"))
    
    # Stats and abilities
    level: int = 1
    skills: Dict[str, int] = field(default_factory=dict)
    special_abilities: List[str] = field(default_factory=list)
    
    # Story elements
    personal_quest: Optional[CompanionQuest] = None
    secrets: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    
    # Current state
    is_recruited: bool = False
    is_active: bool = False
    recruitment_requirements: List[str] = field(default_factory=list)
    
    # Dialogue and interactions
    dialogue_history: List[str] = field(default_factory=list)
    recent_comments: List[str] = field(default_factory=list)
    
    # Equipment and resources
    equipment: Dict[str, str] = field(default_factory=dict)
    personal_items: List[str] = field(default_factory=list)


class CompanionSystem:
    """Advanced companion management system"""
    
    def __init__(self):
        self.companions: Dict[str, Companion] = {}
        self.party_dynamics = PartyDynamics()
        self.companion_templates = self._initialize_companion_templates()
        self.relationship_events = self._initialize_relationship_events()
        self.party_banter = self._initialize_party_banter()
        
        self._create_default_companions()
    
    def _initialize_companion_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize companion character templates"""
        
        return {
            "lyralei_ranger": {
                "name": "Lyralei",
                "type": CompanionType.RANGER,
                "age": 28,
                "background": "Former royal scout turned wilderness guide",
                "origin": "whispering_woods",
                "personality": {
                    "primary_traits": ["independent", "loyal", "protective", "observant"],
                    "moral_alignment": "chaotic_good",
                    "likes": ["nature", "honest_people", "freedom", "archery_contests"],
                    "dislikes": ["cities", "lies", "cruelty_to_animals", "corrupt_nobles"],
                    "fears": ["losing_loved_ones", "being_trapped", "betrayal"],
                    "core_values": ["freedom", "loyalty", "protection_of_innocents"],
                    "leadership_style": "by_example",
                    "conflict_resolution": "direct_confrontation"
                },
                "skills": {"archery": 9, "tracking": 8, "survival": 9, "stealth": 7},
                "special_abilities": ["animal_companion", "perfect_shot", "forest_knowledge"],
                "secrets": ["witnessed_royal_conspiracy", "has_elven_heritage"],
                "goals": ["protect_the_forest", "expose_corruption", "find_missing_brother"],
                "recruitment_requirements": ["complete_forest_quest", "prove_trustworthiness"],
                "personal_quest": {
                    "type": "family",
                    "title": "The Lost Brother",
                    "description": "Help Lyralei find her missing brother who disappeared during a royal mission"
                }
            },
            "thane_warrior": {
                "name": "Thane",
                "type": CompanionType.WARRIOR,
                "age": 35,
                "background": "Disgraced knight seeking redemption",
                "origin": "royal_capital",
                "personality": {
                    "primary_traits": ["honorable", "guilt_ridden", "determined", "protective"],
                    "moral_alignment": "lawful_good",
                    "likes": ["honor", "justice", "helping_others", "training"],
                    "dislikes": ["injustice", "cowardice", "his_past_failures", "dark_magic"],
                    "fears": ["failing_again", "darkness_within", "harming_innocents"],
                    "core_values": ["honor", "redemption", "protection_of_weak"],
                    "leadership_style": "protective_commander",
                    "conflict_resolution": "structured_discussion"
                },
                "skills": {"swordsmanship": 9, "leadership": 7, "tactics": 8, "diplomacy": 6},
                "special_abilities": ["inspiring_presence", "defensive_stance", "honor_bound"],
                "secrets": ["caused_civilian_deaths", "haunted_by_nightmares"],
                "goals": ["find_redemption", "protect_innocents", "restore_honor"],
                "recruitment_requirements": ["show_mercy_to_enemies", "demonstrate_honor"],
                "personal_quest": {
                    "type": "redemption",
                    "title": "The Weight of Honor",
                    "description": "Help Thane confront his past mistakes and find true redemption"
                }
            },
            "zara_mage": {
                "name": "Zara",
                "type": CompanionType.MAGE,
                "age": 23,
                "background": "Brilliant but reckless magical researcher",
                "origin": "crystal_sanctum",
                "personality": {
                    "primary_traits": ["curious", "brilliant", "reckless", "ambitious"],
                    "moral_alignment": "chaotic_neutral",
                    "likes": ["magical_research", "ancient_mysteries", "intellectual_debates", "exotic_food"],
                    "dislikes": ["ignorance", "magical_restrictions", "boring_conversations", "physical_labor"],
                    "fears": ["magical_stagnation", "being_ordinary", "loss_of_intellect"],
                    "core_values": ["knowledge", "magical_advancement", "intellectual_freedom"],
                    "leadership_style": "intellectual_guidance",
                    "conflict_resolution": "logical_argument"
                },
                "skills": {"arcane_magic": 9, "research": 8, "ancient_languages": 7, "alchemy": 6},
                "special_abilities": ["spell_innovation", "magical_theory", "reality_sight"],
                "secrets": ["forbidden_research", "caused_magical_accident"],
                "goals": ["advance_magical_knowledge", "prove_theories", "unlock_ancient_secrets"],
                "recruitment_requirements": ["assist_magical_research", "show_intellectual_curiosity"],
                "personal_quest": {
                    "type": "personal_history",
                    "title": "The Forbidden Archive",
                    "description": "Help Zara access forbidden magical knowledge while avoiding dangerous consequences"
                }
            },
            "kael_rogue": {
                "name": "Kael",
                "type": CompanionType.ROGUE,
                "age": 26,
                "background": "Reformed thief with a heart of gold",
                "origin": "trading_post",
                "personality": {
                    "primary_traits": ["charming", "witty", "street_smart", "loyal"],
                    "moral_alignment": "chaotic_good",
                    "likes": ["clever_schemes", "helping_underdogs", "good_wine", "card_games"],
                    "dislikes": ["bullies", "the_wealthy_elite", "being_lectured", "formal_events"],
                    "fears": ["returning_to_poverty", "losing_friends", "being_abandoned"],
                    "core_values": ["loyalty_to_friends", "helping_the_poor", "personal_freedom"],
                    "leadership_style": "informal_guidance",
                    "conflict_resolution": "clever_solutions",
                    "humor_type": "sarcastic"
                },
                "skills": {"stealth": 9, "lockpicking": 8, "persuasion": 7, "acrobatics": 8},
                "special_abilities": ["master_thief", "silver_tongue", "escape_artist"],
                "secrets": ["noble_birth", "stole_from_corrupt_lord", "supports_orphanage"],
                "goals": ["help_the_downtrodden", "expose_corruption", "find_belonging"],
                "recruitment_requirements": ["help_poor_people", "show_you_trust_him"],
                "personal_quest": {
                    "type": "personal_history",
                    "title": "Sins of the Father",
                    "description": "Help Kael confront his noble heritage and corrupt family legacy"
                }
            }
        }
    
    def _create_default_companions(self):
        """Create the default companion characters"""
        
        for comp_id, template in self.companion_templates.items():
            companion = Companion(
                id=comp_id,
                name=template["name"],
                companion_type=template["type"],
                age=template["age"],
                background=template["background"],
                origin_location=template["origin"]
            )
            
            # Set personality
            personality_data = template["personality"]
            companion.personality = CompanionPersonality(
                primary_traits=personality_data["primary_traits"],
                moral_alignment=personality_data["moral_alignment"],
                likes=personality_data["likes"],
                dislikes=personality_data["dislikes"],
                fears=personality_data["fears"],
                core_values=personality_data["core_values"],
                leadership_style=personality_data.get("leadership_style", "collaborative"),
                conflict_resolution=personality_data.get("conflict_resolution", "diplomatic")
            )
            
            # Set skills and abilities
            companion.skills = template["skills"]
            companion.special_abilities = template["special_abilities"]
            companion.secrets = template["secrets"]
            companion.goals = template["goals"]
            companion.recruitment_requirements = template["recruitment_requirements"]
            
            # Create personal quest
            if "personal_quest" in template:
                quest_data = template["personal_quest"]
                companion.personal_quest = CompanionQuest(
                    id=f"{comp_id}_personal_quest",
                    companion_id=comp_id,
                    title=quest_data["title"],
                    description=quest_data["description"],
                    quest_type=quest_data["type"]
                )
            
            self.companions[comp_id] = companion
    
    def _initialize_relationship_events(self) -> Dict[str, Dict[str, Any]]:
        """Initialize relationship progression events"""
        
        return {
            "first_meeting": {
                "trust_change": 5,
                "respect_change": 0,
                "affection_change": 0,
                "dialogue_options": ["introduce_yourself", "ask_about_background", "be_friendly"]
            },
            "helped_in_combat": {
                "trust_change": 10,
                "respect_change": 8,
                "loyalty_change": 5,
                "mood_improvement": True,
                "comments": ["Thanks for having my back!", "I knew I could count on you."]
            },
            "shared_personal_story": {
                "trust_change": 15,
                "affection_change": 10,
                "relationship_deepening": True,
                "unlocks_romance": True,
                "comments": ["I don't usually share that with people...", "Thanks for listening."]
            },
            "moral_disagreement": {
                "trust_change": -5,
                "respect_change": -3,
                "tension_increase": True,
                "comments": ["I can't believe you did that.", "We need to talk about this."]
            },
            "gift_giving": {
                "affection_change": 8,
                "trust_change": 3,
                "mood_improvement": True,
                "comments": ["You thought of me!", "This is perfect, thank you."]
            },
            "romance_confession": {
                "relationship_status_change": "romantic_interest",
                "affection_change": 20,
                "romance_stage_increase": 2,
                "special_dialogue": True
            }
        }
    
    def _initialize_party_banter(self) -> Dict[str, List[str]]:
        """Initialize party banter between companions"""
        
        return {
            "lyralei_thane": [
                "Lyralei: 'Your honor is admirable, Thane, but sometimes rules need bending.'",
                "Thane: 'Honor isn't about rules, Lyralei. It's about doing what's right.'",
                "Lyralei: 'And what's right isn't always what's lawful.'"
            ],
            "zara_kael": [
                "Zara: 'Your sleight of hand is impressive, but can you manipulate magical energy?'",
                "Kael: 'Magic's just another lock to pick, scholar. Different tools, same principle.'",
                "Zara: 'Fascinating! Perhaps we could experiment with spell-enhanced thievery?'"
            ],
            "thane_kael": [
                "Thane: 'Your past doesn't define you, Kael. Your actions do.'",
                "Kael: 'Easy words from someone born to privilege.'",
                "Thane: 'Privilege doesn't shield you from making mistakes.'"
            ],
            "lyralei_zara": [
                "Lyralei: 'All that magical theory, but can you start a fire without it?'",
                "Zara: 'Why would I need to when I can summon flames with a thought?'",
                "Lyralei: 'Because magic isn't always reliable in the wild.'"
            ]
        }
    
    def attempt_recruitment(self, companion_id: str, player_actions: List[str], player_reputation: Dict[str, int]) -> Dict[str, Any]:
        """Attempt to recruit a companion"""
        
        if companion_id not in self.companions:
            return {"error": "Companion not found"}
        
        companion = self.companions[companion_id]
        
        if companion.is_recruited:
            return {"error": "Companion already recruited"}
        
        # Check recruitment requirements
        requirements_met = []
        requirements_failed = []
        
        for requirement in companion.recruitment_requirements:
            if requirement in player_actions:
                requirements_met.append(requirement)
            else:
                requirements_failed.append(requirement)
        
        # Check personality compatibility
        personality_score = 0
        for action in player_actions:
            if action in companion.personality.likes:
                personality_score += 2
            elif action in companion.personality.dislikes:
                personality_score -= 2
        
        # Check reputation requirements
        reputation_score = 0
        for faction, rep in player_reputation.items():
            if faction in companion.personality.core_values:
                reputation_score += rep * 0.1
        
        recruitment_result = {
            "companion_name": companion.name,
            "success": False,
            "requirements_met": requirements_met,
            "requirements_failed": requirements_failed,
            "personality_compatibility": personality_score,
            "reputation_impact": reputation_score
        }
        
        # Calculate recruitment success
        if len(requirements_failed) == 0:
            base_success = 0.7
            personality_bonus = personality_score * 0.05
            reputation_bonus = reputation_score * 0.1
            
            total_success = base_success + personality_bonus + reputation_bonus
            
            if random.random() <= total_success:
                companion.is_recruited = True
                companion.player_relationship.relationship_type = RelationshipStatus.ACQUAINTANCE
                companion.player_relationship.trust = 60
                companion.player_relationship.first_meeting = f"Recruited on day {datetime.now().day}"
                
                recruitment_result["success"] = True
                recruitment_result["message"] = f"{companion.name} has joined your party!"
                
                # Trigger first meeting event
                self._trigger_relationship_event("first_meeting", companion, "player")
        
        return recruitment_result
    
    def interact_with_companion(self, companion_id: str, interaction_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle player interaction with companion"""
        
        if companion_id not in self.companions:
            return {"error": "Companion not found"}
        
        companion = self.companions[companion_id]
        
        if not companion.is_recruited:
            return {"error": "Companion not recruited"}
        
        interaction_result = {
            "companion_name": companion.name,
            "interaction_type": interaction_type,
            "response": "",
            "relationship_changes": {},
            "mood_change": None,
            "unlocked_content": []
        }
        
        # Process different interaction types
        if interaction_type == "casual_conversation":
            response = self._generate_casual_conversation(companion, context)
            interaction_result["response"] = response
            
        elif interaction_type == "deep_conversation":
            if companion.player_relationship.relationship_type.value in ["friend", "close_friend", "romantic_interest", "lover"]:
                response = self._generate_deep_conversation(companion, context)
                interaction_result["response"] = response
                self._trigger_relationship_event("shared_personal_story", companion, "player")
            else:
                interaction_result["response"] = f"{companion.name} doesn't seem ready for deep conversation yet."
        
        elif interaction_type == "give_gift":
            gift_item = context.get("gift_item", "")
            response = self._handle_gift_giving(companion, gift_item)
            interaction_result["response"] = response
            self._trigger_relationship_event("gift_giving", companion, "player")
        
        elif interaction_type == "romance_attempt":
            if companion.player_relationship.romance_locked:
                response = self._handle_romance_interaction(companion, context)
                interaction_result["response"] = response
            else:
                interaction_result["response"] = f"{companion.name} doesn't seem interested in romance."
        
        elif interaction_type == "ask_about_quest":
            if companion.personal_quest:
                response = self._discuss_personal_quest(companion)
                interaction_result["response"] = response
                if companion.player_relationship.relationship_type.value in ["friend", "close_friend"]:
                    interaction_result["unlocked_content"].append("personal_quest_available")
        
        # Update recent interactions
        companion.dialogue_history.append(f"{interaction_type}: {interaction_result['response'][:50]}...")
        companion.player_relationship.recent_interactions.append(interaction_type)
        
        # Keep only recent interactions
        if len(companion.player_relationship.recent_interactions) > 10:
            companion.player_relationship.recent_interactions = companion.player_relationship.recent_interactions[-10:]
        
        return interaction_result
    
    def _generate_casual_conversation(self, companion: Companion, context: Dict[str, Any]) -> str:
        """Generate casual conversation response"""
        
        current_location = context.get("location", "unknown")
        recent_events = context.get("recent_events", [])
        
        # Base responses by companion type
        responses = {
            CompanionType.RANGER: [
                "The forest has been restless lately. Something's stirring.",
                "I prefer the open road to crowded places.",
                "My bow has served me well in these travels."
            ],
            CompanionType.WARRIOR: [
                "We should stay alert. Danger could be anywhere.",
                "Honor is earned through deeds, not words.",
                "I've seen too much conflict in my time."
            ],
            CompanionType.MAGE: [
                "The magical energies here are fascinating.",
                "I've been researching some interesting theories.",
                "Knowledge is the greatest treasure we can find."
            ],
            CompanionType.ROGUE: [
                "This place has potential for... opportunities.",
                "Keep your coin purse close around here.",
                "I know a shortcut through the back alleys."
            ]
        }
        
        base_response = random.choice(responses.get(companion.companion_type, ["Interesting..."]))
        
        # Add personality flavor
        if "witty" in companion.personality.primary_traits:
            base_response += " Though I suppose you already knew that."
        elif "protective" in companion.personality.primary_traits:
            base_response += " Stay close to me."
        
        return base_response
    
    def _generate_deep_conversation(self, companion: Companion, context: Dict[str, Any]) -> str:
        """Generate deep conversation response"""
        
        relationship_level = companion.player_relationship.relationship_type
        
        # Reveal secrets and backstory based on relationship level
        if relationship_level == RelationshipStatus.FRIEND:
            if companion.secrets and not companion.player_relationship.backstory_revealed:
                secret = random.choice(companion.secrets[:1])  # Reveal minor secrets first
                companion.player_relationship.backstory_revealed.append(secret)
                return f"I haven't told many people this, but... {secret.replace('_', ' ')}."
        
        elif relationship_level == RelationshipStatus.CLOSE_FRIEND:
            if len(companion.secrets) > 1:
                secret = companion.secrets[1] if len(companion.secrets) > 1 else companion.secrets[0]
                if secret not in companion.player_relationship.backstory_revealed:
                    companion.player_relationship.backstory_revealed.append(secret)
                    return f"You've become important to me, so I need to tell you... {secret.replace('_', ' ')}."
        
        # Default deep conversation
        goal = random.choice(companion.goals)
        return f"Sometimes I wonder if I'll ever achieve my goal of {goal.replace('_', ' ')}. What do you think?"
    
    def _handle_gift_giving(self, companion: Companion, gift_item: str) -> str:
        """Handle giving gifts to companions"""
        
        # Check if gift matches companion preferences
        if gift_item in companion.personality.likes:
            companion.current_mood = CompanionMood.HAPPY
            return f"This is wonderful! You remembered that I love {gift_item.replace('_', ' ')}!"
        
        elif gift_item in companion.personality.dislikes:
            companion.current_mood = CompanionMood.ANNOYED
            return f"I... appreciate the thought, but you know I don't care for {gift_item.replace('_', ' ')}."
        
        else:
            # Neutral gift
            return f"Thank you for thinking of me. This {gift_item.replace('_', ' ')} will be useful."
    
    def _handle_romance_interaction(self, companion: Companion, context: Dict[str, Any]) -> str:
        """Handle romantic interactions"""
        
        romance_stage = companion.player_relationship.romance_stage
        
        if romance_stage == 0:
            # First romantic approach
            if companion.player_relationship.relationship_type == RelationshipStatus.CLOSE_FRIEND:
                companion.player_relationship.romance_stage = 1
                companion.player_relationship.relationship_type = RelationshipStatus.ROMANTIC_INTEREST
                return "I... I've been feeling something between us too. Maybe we could explore this?"
            else:
                return "I think we should focus on our friendship first."
        
        elif romance_stage < 5:
            # Developing romance
            companion.player_relationship.romance_stage += 1
            return f"Being with you feels so natural. I'm glad we found each other."
        
        else:
            # Established romance
            return "I love you. Whatever comes next, we'll face it together."
    
    def _discuss_personal_quest(self, companion: Companion) -> str:
        """Discuss companion's personal quest"""
        
        if not companion.personal_quest:
            return "I don't have any personal matters that need attention right now."
        
        quest = companion.personal_quest
        
        if quest.current_stage == 0:
            return f"There's something I've been meaning to tell you about... {quest.description}"
        
        elif quest.current_stage < quest.total_stages:
            return f"We're making progress on {quest.title}, but there's still more to do."
        
        else:
            return f"Thanks for helping me with {quest.title}. It means everything to me."
    
    def _trigger_relationship_event(self, event_type: str, companion: Companion, target_id: str):
        """Trigger relationship event and apply effects"""
        
        if event_type not in self.relationship_events:
            return
        
        event = self.relationship_events[event_type]
        relationship = companion.player_relationship
        
        # Apply relationship changes
        if "trust_change" in event:
            relationship.trust = max(0, min(100, relationship.trust + event["trust_change"]))
        
        if "affection_change" in event:
            relationship.affection = max(0, min(100, relationship.affection + event["affection_change"]))
        
        if "respect_change" in event:
            relationship.respect = max(0, min(100, relationship.respect + event["respect_change"]))
        
        if "loyalty_change" in event:
            relationship.loyalty = max(0, min(100, relationship.loyalty + event["loyalty_change"]))
        
        # Update relationship status based on metrics
        self._update_relationship_status(companion)
        
        # Apply mood changes
        if event.get("mood_improvement"):
            positive_moods = [CompanionMood.HAPPY, CompanionMood.CONTENT, CompanionMood.EXCITED]
            companion.current_mood = random.choice(positive_moods)
        
        # Unlock romance if applicable
        if event.get("unlocks_romance") and relationship.trust > 70 and relationship.affection > 60:
            companion.player_relationship.romance_locked = True
        
        # Add to relationship history
        relationship.relationship_history.append(f"{event_type} - Day {datetime.now().day}")
    
    def _update_relationship_status(self, companion: Companion):
        """Update relationship status based on metrics"""
        
        rel = companion.player_relationship
        
        # Calculate overall relationship score
        avg_score = (rel.trust + rel.affection + rel.respect + rel.loyalty) / 4
        
        if avg_score >= 90:
            if rel.romance_stage > 3:
                rel.relationship_type = RelationshipStatus.LOVER
            else:
                rel.relationship_type = RelationshipStatus.CLOSE_FRIEND
        elif avg_score >= 70:
            if rel.romance_stage > 0:
                rel.relationship_type = RelationshipStatus.ROMANTIC_INTEREST
            else:
                rel.relationship_type = RelationshipStatus.FRIEND
        elif avg_score >= 50:
            rel.relationship_type = RelationshipStatus.ACQUAINTANCE
        elif avg_score < 30:
            if rel.trust < 20:
                rel.relationship_type = RelationshipStatus.ENEMY
            else:
                rel.relationship_type = RelationshipStatus.RIVAL
    
    def process_party_dynamics(self, active_companions: List[str], recent_events: List[str]) -> Dict[str, Any]:
        """Process interactions between party members"""
        
        dynamics_result = {
            "party_cohesion": self.party_dynamics.cohesion,
            "tension_events": [],
            "bonding_events": [],
            "banter": [],
            "leadership_changes": []
        }
        
        if len(active_companions) < 2:
            return dynamics_result
        
        # Generate inter-companion interactions
        for i, comp1_id in enumerate(active_companions):
            for comp2_id in active_companions[i+1:]:
                
                comp1 = self.companions[comp1_id]
                comp2 = self.companions[comp2_id]
                
                # Check for personality conflicts
                conflict_chance = self._calculate_conflict_chance(comp1, comp2)
                
                if random.random() < conflict_chance:
                    conflict = self._generate_companion_conflict(comp1, comp2)
                    dynamics_result["tension_events"].append(conflict)
                    self.party_dynamics.tension_level += 0.1
                
                # Check for bonding moments
                bonding_chance = self._calculate_bonding_chance(comp1, comp2)
                
                if random.random() < bonding_chance:
                    bonding = self._generate_bonding_moment(comp1, comp2)
                    dynamics_result["bonding_events"].append(bonding)
                    self.party_dynamics.cohesion += 0.05
                
                # Generate party banter
                banter_key = f"{comp1_id}_{comp2_id}"
                reverse_key = f"{comp2_id}_{comp1_id}"
                
                if banter_key in self.party_banter or reverse_key in self.party_banter:
                    banter_lines = self.party_banter.get(banter_key, self.party_banter.get(reverse_key, []))
                    if banter_lines and random.random() < 0.3:  # 30% chance
                        dynamics_result["banter"].append(random.choice(banter_lines))
        
        # Normalize party dynamics
        self.party_dynamics.tension_level = max(0.0, min(1.0, self.party_dynamics.tension_level))
        self.party_dynamics.cohesion = max(0.0, min(1.0, self.party_dynamics.cohesion))
        
        return dynamics_result
    
    def _calculate_conflict_chance(self, comp1: Companion, comp2: Companion) -> float:
        """Calculate chance of conflict between companions"""
        
        conflict_factors = 0.0
        
        # Moral alignment conflicts
        if comp1.personality.moral_alignment != comp2.personality.moral_alignment:
            if "lawful" in comp1.personality.moral_alignment and "chaotic" in comp2.personality.moral_alignment:
                conflict_factors += 0.2
            if "good" in comp1.personality.moral_alignment and "evil" in comp2.personality.moral_alignment:
                conflict_factors += 0.3
        
        # Personality trait conflicts
        conflicting_traits = [
            ("independent", "leadership_focused"),
            ("reckless", "cautious"),
            ("direct", "subtle")
        ]
        
        for trait1, trait2 in conflicting_traits:
            if trait1 in comp1.personality.primary_traits and trait2 in comp2.personality.primary_traits:
                conflict_factors += 0.1
        
        # Leadership conflicts
        if comp1.personality.leadership_style != comp2.personality.leadership_style:
            conflict_factors += 0.1
        
        return min(0.5, conflict_factors)  # Cap at 50%
    
    def _calculate_bonding_chance(self, comp1: Companion, comp2: Companion) -> float:
        """Calculate chance of bonding between companions"""
        
        bonding_factors = 0.0
        
        # Shared values
        shared_values = set(comp1.personality.core_values) & set(comp2.personality.core_values)
        bonding_factors += len(shared_values) * 0.1
        
        # Compatible traits
        compatible_traits = [
            ("loyal", "trustworthy"),
            ("protective", "caring"),
            ("brave", "courageous")
        ]
        
        for trait1, trait2 in compatible_traits:
            if trait1 in comp1.personality.primary_traits and trait2 in comp2.personality.primary_traits:
                bonding_factors += 0.15
        
        # Complementary skills
        if comp1.companion_type != comp2.companion_type:
            bonding_factors += 0.1  # Different roles complement each other
        
        return min(0.4, bonding_factors)  # Cap at 40%
    
    def _generate_companion_conflict(self, comp1: Companion, comp2: Companion) -> Dict[str, str]:
        """Generate conflict between companions"""
        
        conflict_scenarios = [
            f"{comp1.name} and {comp2.name} disagree about the best approach to a problem",
            f"{comp1.name} questions {comp2.name}'s methods",
            f"{comp1.name} and {comp2.name} have different ideas about leadership",
            f"{comp1.name} accidentally offends {comp2.name}"
        ]
        
        return {
            "type": "personality_conflict",
            "description": random.choice(conflict_scenarios),
            "participants": [comp1.name, comp2.name]
        }
    
    def _generate_bonding_moment(self, comp1: Companion, comp2: Companion) -> Dict[str, str]:
        """Generate bonding moment between companions"""
        
        bonding_scenarios = [
            f"{comp1.name} and {comp2.name} share stories around the campfire",
            f"{comp1.name} helps {comp2.name} with a personal problem",
            f"{comp1.name} and {comp2.name} work together perfectly in combat",
            f"{comp1.name} and {comp2.name} discover they have more in common than expected"
        ]
        
        return {
            "type": "bonding_moment",
            "description": random.choice(bonding_scenarios),
            "participants": [comp1.name, comp2.name]
        }
    
    def get_party_status(self, active_companions: List[str]) -> Dict[str, Any]:
        """Get comprehensive party status"""
        
        party_members = []
        for comp_id in active_companions:
            if comp_id in self.companions:
                companion = self.companions[comp_id]
                party_members.append({
                    "name": companion.name,
                    "type": companion.companion_type.value,
                    "mood": companion.current_mood.value,
                    "relationship_status": companion.player_relationship.relationship_type.value,
                    "trust": companion.player_relationship.trust,
                    "affection": companion.player_relationship.affection,
                    "loyalty": companion.player_relationship.loyalty,
                    "romance_stage": companion.player_relationship.romance_stage,
                    "personal_quest_available": companion.personal_quest is not None,
                    "recent_comments": companion.recent_comments[-3:] if companion.recent_comments else []
                })
        
        return {
            "party_members": party_members,
            "party_cohesion": self.party_dynamics.cohesion,
            "party_tension": self.party_dynamics.tension_level,
            "recent_bonding_moments": self.party_dynamics.bonding_moments[-3:],
            "recent_conflicts": self.party_dynamics.conflicts[-3:],
            "available_romance_options": [
                comp.name for comp in self.companions.values()
                if comp.player_relationship.romance_locked and comp.player_relationship.romance_stage < 5
            ]
        } 