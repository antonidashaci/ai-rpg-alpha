"""
AI-RPG-Alpha: Enhanced Character System

Advanced character modeling including personalities, relationships, dialogue systems,
and dynamic character development. Creates deep, memorable NPCs and rich player characters.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from enum import Enum
import random


class PersonalityTrait(Enum):
    """Core personality traits that affect NPC behavior and dialogue"""
    BRAVE = "brave"
    COWARDLY = "cowardly"
    WISE = "wise"
    FOOLISH = "foolish"
    KIND = "kind"
    CRUEL = "cruel"
    HONEST = "honest"
    DECEPTIVE = "deceptive"
    AMBITIOUS = "ambitious"
    CONTENT = "content"
    CURIOUS = "curious"
    INDIFFERENT = "indifferent"
    LOYAL = "loyal"
    TREACHEROUS = "treacherous"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"


class EmotionalState(Enum):
    """Current emotional state affecting interactions"""
    JOYFUL = "joyful"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SAD = "sad"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CONTENT = "content"


class RelationshipType(Enum):
    """Types of relationships between characters"""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    ALLY = "ally"
    ENEMY = "enemy"
    RIVAL = "rival"
    MENTOR = "mentor"
    STUDENT = "student"
    FAMILY = "family"
    ROMANTIC = "romantic"


class SocialClass(Enum):
    """Social class affecting interactions and opportunities"""
    PEASANT = "peasant"
    MERCHANT = "merchant"
    ARTISAN = "artisan"
    SOLDIER = "soldier"
    NOBLE = "noble"
    ROYALTY = "royalty"
    CLERGY = "clergy"
    SCHOLAR = "scholar"
    OUTLAW = "outlaw"
    EXILE = "exile"


@dataclass
class Personality:
    """Complex personality system for characters"""
    traits: Set[PersonalityTrait] = field(default_factory=set)
    dominant_trait: Optional[PersonalityTrait] = None
    values: Dict[str, int] = field(default_factory=dict)  # -100 to 100 scale
    quirks: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    desires: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize default values if not provided"""
        if not self.values:
            self.values = {
                "honor": random.randint(-50, 50),
                "justice": random.randint(-50, 50),
                "freedom": random.randint(-50, 50),
                "knowledge": random.randint(-50, 50),
                "power": random.randint(-50, 50),
                "wealth": random.randint(-50, 50),
                "family": random.randint(-50, 50),
                "tradition": random.randint(-50, 50)
            }
    
    def get_trait_influence(self, situation: str) -> float:
        """Calculate how personality traits influence reactions to situations"""
        influence = 0.0
        
        # Map situations to relevant traits
        trait_map = {
            "combat": [PersonalityTrait.BRAVE, PersonalityTrait.COWARDLY],
            "negotiation": [PersonalityTrait.HONEST, PersonalityTrait.DECEPTIVE],
            "helping": [PersonalityTrait.KIND, PersonalityTrait.CRUEL],
            "learning": [PersonalityTrait.CURIOUS, PersonalityTrait.WISE]
        }
        
        relevant_traits = trait_map.get(situation, [])
        for trait in relevant_traits:
            if trait in self.traits:
                if trait.value in ["brave", "wise", "kind", "honest", "curious"]:
                    influence += 0.3
                else:
                    influence -= 0.3
        
        return max(-1.0, min(1.0, influence))


@dataclass
class Relationship:
    """Relationship between two characters"""
    character_id: str
    relationship_type: RelationshipType = RelationshipType.STRANGER
    trust_level: int = 50  # 0-100
    affection: int = 50    # 0-100
    respect: int = 50      # 0-100
    fear: int = 0          # 0-100
    shared_history: List[str] = field(default_factory=list)
    last_interaction: Optional[datetime] = None
    
    def get_overall_standing(self) -> float:
        """Calculate overall relationship standing"""
        positive = (self.trust_level + self.affection + self.respect) / 3
        negative = self.fear
        return (positive - negative) / 100


@dataclass
class DialogueOption:
    """A dialogue choice with contextual information"""
    text: str
    required_stats: Dict[str, int] = field(default_factory=dict)
    required_items: List[str] = field(default_factory=list)
    required_relationships: Dict[str, int] = field(default_factory=dict)
    consequences: Dict[str, Any] = field(default_factory=dict)
    unlocks: List[str] = field(default_factory=list)
    personality_influence: float = 0.0


@dataclass
class DialogueTree:
    """Complex dialogue system with branching conversations"""
    id: str
    speaker_id: str
    opening_line: str
    options: List[DialogueOption] = field(default_factory=list)
    context_requirements: Dict[str, Any] = field(default_factory=dict)
    repeatable: bool = True
    cooldown_turns: int = 0
    last_used: Optional[int] = None


@dataclass
class CharacterBackground:
    """Rich character background and history"""
    origin: str = "Unknown"
    occupation: str = "Wanderer"
    social_class: SocialClass = SocialClass.PEASANT
    family_status: str = "Unknown"
    education: str = "Self-taught"
    major_events: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    motivations: List[str] = field(default_factory=list)


@dataclass
class CharacterAppearance:
    """Physical description and distinctive features"""
    age_category: str = "Adult"  # Child, Young Adult, Adult, Middle-aged, Elder
    height: str = "Average"
    build: str = "Average"
    hair_color: str = "Brown"
    eye_color: str = "Brown"
    skin_tone: str = "Fair"
    distinctive_features: List[str] = field(default_factory=list)
    clothing_style: str = "Practical"
    mannerisms: List[str] = field(default_factory=list)


@dataclass
class Character:
    """Enhanced character with full personality, relationships, and depth"""
    id: str
    name: str
    title: Optional[str] = None
    personality: Personality = field(default_factory=Personality)
    background: CharacterBackground = field(default_factory=CharacterBackground)
    appearance: CharacterAppearance = field(default_factory=CharacterAppearance)
    current_location: str = "unknown"
    current_emotion: EmotionalState = EmotionalState.NEUTRAL
    
    # Relationships with other characters
    relationships: Dict[str, Relationship] = field(default_factory=dict)
    
    # Dialogue and interaction
    dialogue_trees: List[DialogueTree] = field(default_factory=list)
    known_information: Set[str] = field(default_factory=set)
    
    # Character development
    character_arc: List[str] = field(default_factory=list)
    development_stage: str = "introduction"
    
    # Game mechanics
    reputation: Dict[str, int] = field(default_factory=dict)  # faction reputation
    available_quests: List[str] = field(default_factory=list)
    
    # Temporal aspects
    last_seen: Optional[datetime] = None
    schedule: Dict[str, str] = field(default_factory=dict)  # time -> activity
    
    def get_relationship_with(self, character_id: str) -> Relationship:
        """Get relationship with specific character"""
        if character_id not in self.relationships:
            self.relationships[character_id] = Relationship(character_id=character_id)
        return self.relationships[character_id]
    
    def update_relationship(
        self, 
        character_id: str, 
        trust_delta: int = 0,
        affection_delta: int = 0,
        respect_delta: int = 0,
        fear_delta: int = 0,
        interaction_type: str = "neutral"
    ):
        """Update relationship based on interaction"""
        rel = self.get_relationship_with(character_id)
        
        rel.trust_level = max(0, min(100, rel.trust_level + trust_delta))
        rel.affection = max(0, min(100, rel.affection + affection_delta))
        rel.respect = max(0, min(100, rel.respect + respect_delta))
        rel.fear = max(0, min(100, rel.fear + fear_delta))
        
        rel.shared_history.append(f"{datetime.now().isoformat()}: {interaction_type}")
        rel.last_interaction = datetime.now()
        
        # Update relationship type based on standings
        overall = rel.get_overall_standing()
        if overall > 0.8:
            rel.relationship_type = RelationshipType.ALLY
        elif overall > 0.6:
            rel.relationship_type = RelationshipType.FRIEND
        elif overall < -0.6:
            rel.relationship_type = RelationshipType.ENEMY
        elif overall < -0.3:
            rel.relationship_type = RelationshipType.RIVAL
        else:
            rel.relationship_type = RelationshipType.ACQUAINTANCE
    
    def get_available_dialogue_options(
        self, 
        player_stats: Dict[str, Any],
        player_inventory: List[str],
        player_relationships: Dict[str, Relationship],
        context: Dict[str, Any]
    ) -> List[DialogueOption]:
        """Get available dialogue options based on current context"""
        available_options = []
        
        for tree in self.dialogue_trees:
            # Check context requirements
            if self._meets_context_requirements(tree.context_requirements, context):
                # Check cooldown
                if tree.last_used is None or context.get("turn_number", 0) - tree.last_used >= tree.cooldown_turns:
                    for option in tree.options:
                        if self._can_select_option(option, player_stats, player_inventory, player_relationships):
                            available_options.append(option)
        
        return available_options
    
    def _meets_context_requirements(self, requirements: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if context requirements are met"""
        for key, required_value in requirements.items():
            if key not in context or context[key] != required_value:
                return False
        return True
    
    def _can_select_option(
        self, 
        option: DialogueOption,
        player_stats: Dict[str, Any],
        player_inventory: List[str],
        player_relationships: Dict[str, Relationship]
    ) -> bool:
        """Check if player can select this dialogue option"""
        # Check stat requirements
        for stat, required_value in option.required_stats.items():
            if player_stats.get(stat, 0) < required_value:
                return False
        
        # Check item requirements
        for item in option.required_items:
            if item not in player_inventory:
                return False
        
        # Check relationship requirements
        for char_id, required_standing in option.required_relationships.items():
            if char_id not in player_relationships:
                return False
            if player_relationships[char_id].get_overall_standing() * 100 < required_standing:
                return False
        
        return True
    
    def generate_contextual_greeting(self, player_character: 'Character', context: Dict[str, Any]) -> str:
        """Generate a contextual greeting based on relationship and situation"""
        relationship = self.get_relationship_with(player_character.id)
        
        # Base greeting on relationship
        greetings = {
            RelationshipType.STRANGER: [
                "I don't believe we've met.",
                "You're not from around here, are you?",
                "Can I help you with something?"
            ],
            RelationshipType.FRIEND: [
                f"Good to see you again, {player_character.name}!",
                f"Hello there, {player_character.name}. How have you been?",
                f"{player_character.name}! What brings you here today?"
            ],
            RelationshipType.ALLY: [
                f"My trusted friend {player_character.name}!",
                f"Ah, {player_character.name}. I'm glad you're here.",
                f"Always a pleasure, {player_character.name}."
            ],
            RelationshipType.ENEMY: [
                f"What do you want, {player_character.name}?",
                "I have nothing to say to you.",
                "You have some nerve showing your face here."
            ]
        }
        
        base_greetings = greetings.get(relationship.relationship_type, greetings[RelationshipType.STRANGER])
        greeting = random.choice(base_greetings)
        
        # Modify based on emotion
        if self.current_emotion == EmotionalState.ANGRY:
            greeting = greeting.replace("!", ".").replace("Good", "").strip()
            if not greeting.endswith("?"):
                greeting += " What do you want?"
        elif self.current_emotion == EmotionalState.FEARFUL:
            greeting = greeting.replace("!", "...") + " I... I hope you're not here to cause trouble."
        elif self.current_emotion == EmotionalState.JOYFUL:
            greeting += " What a wonderful day!"
        
        return greeting
    
    def advance_character_arc(self, event: str):
        """Advance character development based on significant events"""
        self.character_arc.append(f"{datetime.now().isoformat()}: {event}")
        
        # Update development stage based on arc progression
        arc_length = len(self.character_arc)
        if arc_length >= 10:
            self.development_stage = "resolution"
        elif arc_length >= 5:
            self.development_stage = "climax"
        elif arc_length >= 2:
            self.development_stage = "development"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "personality": {
                "traits": [trait.value for trait in self.personality.traits],
                "dominant_trait": self.personality.dominant_trait.value if self.personality.dominant_trait else None,
                "values": self.personality.values,
                "quirks": self.personality.quirks,
                "fears": self.personality.fears,
                "desires": self.personality.desires
            },
            "background": {
                "origin": self.background.origin,
                "occupation": self.background.occupation,
                "social_class": self.background.social_class.value,
                "family_status": self.background.family_status,
                "education": self.background.education,
                "major_events": self.background.major_events,
                "secrets": self.background.secrets,
                "goals": self.background.goals,
                "motivations": self.background.motivations
            },
            "appearance": {
                "age_category": self.appearance.age_category,
                "height": self.appearance.height,
                "build": self.appearance.build,
                "hair_color": self.appearance.hair_color,
                "eye_color": self.appearance.eye_color,
                "skin_tone": self.appearance.skin_tone,
                "distinctive_features": self.appearance.distinctive_features,
                "clothing_style": self.appearance.clothing_style,
                "mannerisms": self.appearance.mannerisms
            },
            "current_location": self.current_location,
            "current_emotion": self.current_emotion.value,
            "relationships": {
                char_id: {
                    "relationship_type": rel.relationship_type.value,
                    "trust_level": rel.trust_level,
                    "affection": rel.affection,
                    "respect": rel.respect,
                    "fear": rel.fear,
                    "shared_history": rel.shared_history[-5:],  # Last 5 interactions
                    "last_interaction": rel.last_interaction.isoformat() if rel.last_interaction else None
                }
                for char_id, rel in self.relationships.items()
            },
            "known_information": list(self.known_information),
            "character_arc": self.character_arc[-10:],  # Last 10 developments
            "development_stage": self.development_stage,
            "reputation": self.reputation,
            "available_quests": self.available_quests,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "schedule": self.schedule
        }


class CharacterGenerator:
    """Generate rich, unique characters with coherent personalities and backgrounds"""
    
    @staticmethod
    def generate_random_personality() -> Personality:
        """Generate a random but coherent personality"""
        # Select 2-4 random traits that work together
        positive_traits = [
            PersonalityTrait.BRAVE, PersonalityTrait.WISE, PersonalityTrait.KIND,
            PersonalityTrait.HONEST, PersonalityTrait.AMBITIOUS, PersonalityTrait.CURIOUS,
            PersonalityTrait.LOYAL, PersonalityTrait.OPTIMISTIC
        ]
        
        negative_traits = [
            PersonalityTrait.COWARDLY, PersonalityTrait.FOOLISH, PersonalityTrait.CRUEL,
            PersonalityTrait.DECEPTIVE, PersonalityTrait.TREACHEROUS, PersonalityTrait.PESSIMISTIC
        ]
        
        neutral_traits = [
            PersonalityTrait.CONTENT, PersonalityTrait.INDIFFERENT
        ]
        
        # Bias toward positive traits for more likeable characters
        trait_pool = positive_traits * 3 + negative_traits + neutral_traits
        selected_traits = set(random.sample(trait_pool, k=random.randint(2, 4)))
        
        dominant_trait = random.choice(list(selected_traits))
        
        # Generate quirks and characteristics
        quirks = [
            "Always carries a lucky charm", "Speaks in proverbs", "Has a nervous laugh",
            "Collector of rare books", "Never removes their gloves", "Hums when thinking",
            "Always knows the time without looking", "Remembers everyone's birthday",
            "Can't resist a good puzzle", "Talks to animals"
        ]
        
        fears = [
            "spiders", "heights", "dark magic", "betrayal", "failure", "being forgotten",
            "confined spaces", "deep water", "public speaking", "losing loved ones"
        ]
        
        desires = [
            "to find true love", "to become famous", "to discover ancient knowledge",
            "to protect family", "to gain power", "to explore the world", "to find peace",
            "to right past wrongs", "to create something lasting", "to understand the divine"
        ]
        
        return Personality(
            traits=selected_traits,
            dominant_trait=dominant_trait,
            quirks=random.sample(quirks, k=random.randint(1, 3)),
            fears=random.sample(fears, k=random.randint(1, 2)),
            desires=random.sample(desires, k=random.randint(1, 2))
        )
    
    @staticmethod
    def generate_character(
        name: str,
        occupation: str = None,
        location: str = "unknown",
        social_class: SocialClass = None
    ) -> Character:
        """Generate a complete character with coherent traits"""
        
        personality = CharacterGenerator.generate_random_personality()
        
        # Generate background based on occupation and social class
        if social_class is None:
            social_class = random.choice(list(SocialClass))
        
        if occupation is None:
            occupations_by_class = {
                SocialClass.PEASANT: ["farmer", "laborer", "servant"],
                SocialClass.MERCHANT: ["trader", "shopkeeper", "caravan leader"],
                SocialClass.ARTISAN: ["blacksmith", "carpenter", "tailor"],
                SocialClass.SOLDIER: ["guard", "mercenary", "knight"],
                SocialClass.NOBLE: ["lord", "courtier", "diplomat"],
                SocialClass.CLERGY: ["priest", "monk", "temple guardian"],
                SocialClass.SCHOLAR: ["sage", "librarian", "alchemist"],
                SocialClass.OUTLAW: ["bandit", "smuggler", "rebel"]
            }
            occupation = random.choice(occupations_by_class.get(social_class, ["wanderer"]))
        
        background = CharacterBackground(
            occupation=occupation,
            social_class=social_class,
            origin=f"Born in {random.choice(['the capital', 'a small village', 'the borderlands', 'foreign lands'])}",
            family_status=random.choice(["single", "married", "widowed", "has children", "orphaned"]),
            education=random.choice(["self-taught", "apprenticed", "formally educated", "street-smart"])
        )
        
        # Generate appearance
        appearance = CharacterAppearance(
            age_category=random.choice(["Young Adult", "Adult", "Middle-aged", "Elder"]),
            height=random.choice(["Short", "Average", "Tall"]),
            build=random.choice(["Slim", "Average", "Stocky", "Muscular"]),
            hair_color=random.choice(["Black", "Brown", "Blonde", "Red", "Gray", "White"]),
            eye_color=random.choice(["Brown", "Blue", "Green", "Gray", "Hazel"]),
            distinctive_features=random.sample([
                "scar across cheek", "unusual eye color", "always smiling", "deep voice",
                "elegant hands", "weathered appearance", "distinctive jewelry", "missing finger"
            ], k=random.randint(0, 2))
        )
        
        return Character(
            id=f"{name.lower().replace(' ', '_')}_{random.randint(1000, 9999)}",
            name=name,
            personality=personality,
            background=background,
            appearance=appearance,
            current_location=location,
            current_emotion=random.choice(list(EmotionalState))
        ) 