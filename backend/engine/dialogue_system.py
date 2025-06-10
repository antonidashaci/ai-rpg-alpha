"""
AI-RPG-Alpha: Advanced Dialogue System

Sophisticated dialogue generation with personality-driven conversations,
relationship dynamics, and emergent character interactions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime


class DialogueType(Enum):
    """Types of dialogue interactions"""
    GREETING = "greeting"
    INFORMATION = "information"
    QUEST_RELATED = "quest_related"
    PERSONAL = "personal"
    CONFRONTATION = "confrontation"
    FAREWELL = "farewell"
    AMBIENT = "ambient"


class EmotionalTone(Enum):
    """Emotional tones for dialogue"""
    FRIENDLY = "friendly"
    HOSTILE = "hostile"
    NEUTRAL = "neutral"
    SUSPICIOUS = "suspicious"
    EXCITED = "excited"
    MELANCHOLIC = "melancholic"
    ANXIOUS = "anxious"
    CONFIDENT = "confident"
    MYSTERIOUS = "mysterious"
    COMPASSIONATE = "compassionate"


@dataclass
class DialogueContext:
    """Context information for dialogue generation"""
    location: str
    time_of_day: str
    weather: str = "clear"
    recent_events: List[str] = field(default_factory=list)
    player_reputation: Dict[str, int] = field(default_factory=dict)
    relationship_history: List[str] = field(default_factory=list)
    current_quest: Optional[str] = None
    danger_level: str = "low"
    mystery_level: str = "none"


@dataclass
class DialogueResponse:
    """A character's dialogue response with metadata"""
    text: str
    emotional_tone: EmotionalTone
    reveals_information: List[str] = field(default_factory=list)
    advances_relationship: int = 0  # -10 to +10
    unlocks_options: List[str] = field(default_factory=list)
    requires_follow_up: bool = False
    character_development: List[str] = field(default_factory=list)


class AdvancedDialogueSystem:
    """Sophisticated dialogue system with personality-driven conversations"""
    
    def __init__(self):
        self.personality_dialogue_patterns = self._initialize_personality_patterns()
        self.relationship_modifiers = self._initialize_relationship_modifiers()
        self.contextual_responses = self._initialize_contextual_responses()
        self.conversation_memory = {}  # Track ongoing conversations
    
    def _initialize_personality_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize dialogue patterns for different personality types"""
        return {
            "wise_mentor": {
                "speech_patterns": [
                    "In my experience, {topic}",
                    "The ancient texts speak of {topic}",
                    "As I have learned through many years, {topic}",
                    "Wisdom suggests that {topic}"
                ],
                "vocabulary": {
                    "positive": ["enlightening", "profound", "meaningful", "significant"],
                    "negative": ["troubling", "concerning", "unfortunate", "grave"],
                    "neutral": ["interesting", "notable", "worthy of consideration"]
                },
                "greeting_styles": [
                    "Ah, young {name}. What brings you to seek wisdom today?",
                    "I sense purpose in your step, {name}. How may I guide you?",
                    "The winds of change follow you, {name}. What wisdom do you seek?"
                ]
            },
            "jovial_merchant": {
                "speech_patterns": [
                    "Business is about {topic}, my friend!",
                    "I've traded across many lands, and {topic}",
                    "A wise merchant knows that {topic}",
                    "Gold and goods have taught me that {topic}"
                ],
                "vocabulary": {
                    "positive": ["profitable", "excellent", "valuable", "golden opportunity"],
                    "negative": ["costly", "unfortunate", "bad for business", "unprofitable"],
                    "neutral": ["fair trade", "reasonable", "worth considering"]
                },
                "greeting_styles": [
                    "Welcome, welcome! {name}, isn't it? What can I do for you?",
                    "Ah, a potential customer! Good day, {name}!",
                    "Business has been slow, but you look like someone with coin. How can I help?"
                ]
            },
            "suspicious_rogue": {
                "speech_patterns": [
                    "In the shadows, I've learned that {topic}",
                    "Trust me when I say {topic}",
                    "The streets have taught me that {topic}",
                    "If you know what's good for you, remember that {topic}"
                ],
                "vocabulary": {
                    "positive": ["profitable", "smart", "advantageous", "useful"],
                    "negative": ["dangerous", "foolish", "risky", "deadly"],
                    "neutral": ["interesting", "worth knowing", "typical"]
                },
                "greeting_styles": [
                    "Well, well... {name}. What brings you to my corner of the world?",
                    "Didn't expect to see you here, {name}. Looking for something specific?",
                    "You're either very brave or very foolish, {name}. Which is it?"
                ]
            },
            "noble_aristocrat": {
                "speech_patterns": [
                    "As one of noble birth, I understand that {topic}",
                    "The court has taught me that {topic}",
                    "In refined society, we know that {topic}",
                    "My position has shown me that {topic}"
                ],
                "vocabulary": {
                    "positive": ["distinguished", "refined", "proper", "dignified"],
                    "negative": ["unseemly", "inappropriate", "beneath one's station", "vulgar"],
                    "neutral": ["acceptable", "appropriate", "worthy of consideration"]
                },
                "greeting_styles": [
                    "Good day, {name}. I trust you are conducting yourself appropriately?",
                    "Ah, {name}. How... unexpected to encounter you here.",
                    "I suppose even commoners such as yourself have business in these parts."
                ]
            },
            "mysterious_stranger": {
                "speech_patterns": [
                    "The mysteries of this world reveal that {topic}",
                    "Those who see beyond the veil know that {topic}",
                    "Hidden truths whisper that {topic}",
                    "The initiated understand that {topic}"
                ],
                "vocabulary": {
                    "positive": ["enlightening", "revealing", "significant", "meaningful"],
                    "negative": ["troubling", "ominous", "concerning", "foreboding"],
                    "neutral": ["curious", "intriguing", "worth pondering"]
                },
                "greeting_styles": [
                    "We meet again, {name}. Or perhaps... this is our first meeting?",
                    "The threads of fate have brought you here, {name}.",
                    "I wondered when our paths would cross, {name}."
                ]
            }
        }
    
    def _initialize_relationship_modifiers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize how relationships affect dialogue"""
        return {
            "stranger": {
                "formality_level": "high",
                "information_sharing": "minimal",
                "trust_level": "none",
                "emotional_openness": "guarded"
            },
            "acquaintance": {
                "formality_level": "medium",
                "information_sharing": "basic",
                "trust_level": "cautious",
                "emotional_openness": "polite"
            },
            "friend": {
                "formality_level": "low",
                "information_sharing": "generous",
                "trust_level": "high",
                "emotional_openness": "warm"
            },
            "ally": {
                "formality_level": "variable",
                "information_sharing": "strategic",
                "trust_level": "high",
                "emotional_openness": "mission_focused"
            },
            "enemy": {
                "formality_level": "cold",
                "information_sharing": "deceptive",
                "trust_level": "hostile",
                "emotional_openness": "antagonistic"
            },
            "romantic": {
                "formality_level": "intimate",
                "information_sharing": "personal",
                "trust_level": "deep",
                "emotional_openness": "vulnerable"
            }
        }
    
    def _initialize_contextual_responses(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize context-specific response templates"""
        return {
            "weather_comments": {
                "rain": [
                    "This rain brings both blessing and burden.",
                    "The heavens weep today, as do many hearts.",
                    "Rain washes away sins, they say. I wonder if it's true."
                ],
                "storm": [
                    "The storm mirrors the turmoil in men's hearts.",
                    "Such tempests often herald great changes.",
                    "Even the weather seems angry today."
                ],
                "clear": [
                    "A beautiful day, though appearances can deceive.",
                    "Clear skies often hide the coming storm.",
                    "Such pleasant weather makes one hopeful."
                ]
            },
            "location_comments": {
                "tavern": [
                    "Taverns are where truth and lies flow equally freely.",
                    "More deals are made over ale than in any counting house.",
                    "Listen carefully here - you never know what you might learn."
                ],
                "market": [
                    "The market tells the true health of a community.",
                    "Here you can buy anything... if you know who to ask.",
                    "Commerce makes strange bedfellows of enemies."
                ],
                "temple": [
                    "Sacred spaces hold power, whether you believe or not.",
                    "Gods and mortals have always had complicated relationships.",
                    "Faith can move mountains, but so can good engineering."
                ]
            },
            "quest_reactions": {
                "heroic_quest": [
                    "Heroes are made in moments like these.",
                    "The realm needs more souls willing to stand for others.",
                    "Glory awaits, but so does danger. Choose wisely."
                ],
                "mystery_quest": [
                    "Truth has a way of hiding in the most unexpected places.",
                    "Some mysteries are better left unsolved.",
                    "Knowledge comes with a price. Are you willing to pay it?"
                ],
                "political_quest": [
                    "Politics is war by other means.",
                    "In the game of thrones, everyone is both player and pawn.",
                    "Choose your allies carefully - today's friend is tomorrow's enemy."
                ]
            }
        }
    
    def generate_dialogue_interaction(
        self,
        character_data: Dict[str, Any],
        player_data: Dict[str, Any],
        context: DialogueContext,
        dialogue_type: DialogueType,
        relationship_status: str = "stranger"
    ) -> DialogueResponse:
        """Generate a complete dialogue interaction"""
        
        personality_type = character_data.get("personality_type", "mysterious_stranger")
        character_name = character_data.get("name", "Unknown")
        player_name = player_data.get("name", "Traveler")
        
        # Determine emotional tone based on personality and relationship
        emotional_tone = self._determine_emotional_tone(
            personality_type, relationship_status, context
        )
        
        # Generate appropriate dialogue text
        dialogue_text = self._generate_dialogue_text(
            character_data, player_data, context, dialogue_type, 
            emotional_tone, relationship_status
        )
        
        # Determine what information is revealed
        information_revealed = self._determine_information_reveal(
            character_data, relationship_status, dialogue_type, context
        )
        
        # Calculate relationship impact
        relationship_change = self._calculate_relationship_impact(
            personality_type, dialogue_type, emotional_tone, context
        )
        
        # Determine unlocked options
        unlocked_options = self._determine_unlocked_options(
            character_data, relationship_status, information_revealed
        )
        
        # Check if follow-up is needed
        needs_follow_up = self._check_follow_up_needed(
            dialogue_type, emotional_tone, information_revealed
        )
        
        # Track character development
        character_development = self._track_character_development(
            character_data, dialogue_type, emotional_tone
        )
        
        return DialogueResponse(
            text=dialogue_text,
            emotional_tone=emotional_tone,
            reveals_information=information_revealed,
            advances_relationship=relationship_change,
            unlocks_options=unlocked_options,
            requires_follow_up=needs_follow_up,
            character_development=character_development
        )
    
    def _determine_emotional_tone(
        self,
        personality_type: str,
        relationship_status: str,
        context: DialogueContext
    ) -> EmotionalTone:
        """Determine the emotional tone of the dialogue"""
        
        # Base tone from personality
        personality_base_tones = {
            "wise_mentor": EmotionalTone.COMPASSIONATE,
            "jovial_merchant": EmotionalTone.FRIENDLY,
            "suspicious_rogue": EmotionalTone.SUSPICIOUS,
            "noble_aristocrat": EmotionalTone.CONFIDENT,
            "mysterious_stranger": EmotionalTone.MYSTERIOUS
        }
        
        base_tone = personality_base_tones.get(personality_type, EmotionalTone.NEUTRAL)
        
        # Modify based on relationship
        if relationship_status == "enemy":
            return EmotionalTone.HOSTILE
        elif relationship_status == "friend":
            return EmotionalTone.FRIENDLY
        elif relationship_status == "romantic":
            return random.choice([EmotionalTone.FRIENDLY, EmotionalTone.EXCITED])
        
        # Modify based on context
        if context.danger_level == "high":
            return random.choice([EmotionalTone.ANXIOUS, EmotionalTone.SUSPICIOUS])
        elif context.mystery_level == "high":
            return EmotionalTone.MYSTERIOUS
        
        # Random variation
        if random.random() < 0.2:  # 20% chance for emotional variation
            all_tones = list(EmotionalTone)
            return random.choice(all_tones)
        
        return base_tone
    
    def _generate_dialogue_text(
        self,
        character_data: Dict[str, Any],
        player_data: Dict[str, Any],
        context: DialogueContext,
        dialogue_type: DialogueType,
        emotional_tone: EmotionalTone,
        relationship_status: str
    ) -> str:
        """Generate the actual dialogue text"""
        
        personality_type = character_data.get("personality_type", "mysterious_stranger")
        character_name = character_data.get("name", "Unknown")
        player_name = player_data.get("name", "Traveler")
        
        patterns = self.personality_dialogue_patterns.get(personality_type, {})
        
        # Handle different dialogue types
        if dialogue_type == DialogueType.GREETING:
            return self._generate_greeting(patterns, player_name, relationship_status, emotional_tone)
        
        elif dialogue_type == DialogueType.INFORMATION:
            return self._generate_information_dialogue(patterns, context, emotional_tone)
        
        elif dialogue_type == DialogueType.QUEST_RELATED:
            return self._generate_quest_dialogue(patterns, context, emotional_tone)
        
        elif dialogue_type == DialogueType.PERSONAL:
            return self._generate_personal_dialogue(patterns, character_data, relationship_status, emotional_tone)
        
        elif dialogue_type == DialogueType.CONFRONTATION:
            return self._generate_confrontation_dialogue(patterns, context, emotional_tone)
        
        elif dialogue_type == DialogueType.FAREWELL:
            return self._generate_farewell(patterns, player_name, relationship_status, emotional_tone)
        
        elif dialogue_type == DialogueType.AMBIENT:
            return self._generate_ambient_dialogue(patterns, context, emotional_tone)
        
        else:
            return f"{character_name} looks at you thoughtfully."
    
    def _generate_greeting(
        self,
        patterns: Dict[str, Any],
        player_name: str,
        relationship_status: str,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate greeting dialogue"""
        
        greeting_templates = patterns.get("greeting_styles", [
            "Hello there, {name}.",
            "Good day, {name}.",
            "Well met, {name}."
        ])
        
        base_greeting = random.choice(greeting_templates).format(name=player_name)
        
        # Modify based on emotional tone
        if emotional_tone == EmotionalTone.HOSTILE:
            base_greeting = base_greeting.replace("Good", "").replace("Well met", "So we meet again")
            base_greeting += " What do you want?"
        
        elif emotional_tone == EmotionalTone.EXCITED:
            base_greeting += " What excellent timing!"
        
        elif emotional_tone == EmotionalTone.SUSPICIOUS:
            base_greeting += " What brings you here at this hour?"
        
        elif emotional_tone == EmotionalTone.MYSTERIOUS:
            base_greeting += " I wondered when you would arrive."
        
        return base_greeting
    
    def _generate_information_dialogue(
        self,
        patterns: Dict[str, Any],
        context: DialogueContext,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate information-sharing dialogue"""
        
        speech_patterns = patterns.get("speech_patterns", ["I know that {topic}"])
        vocabulary = patterns.get("vocabulary", {"neutral": ["interesting"]})
        
        # Select topic based on context
        if context.current_quest:
            topic = f"your current quest {context.current_quest}"
        elif context.recent_events:
            topic = f"the recent {random.choice(context.recent_events)}"
        else:
            topic = f"the current situation in {context.location}"
        
        base_pattern = random.choice(speech_patterns)
        
        # Select appropriate vocabulary based on emotional tone
        if emotional_tone in [EmotionalTone.FRIENDLY, EmotionalTone.EXCITED]:
            descriptors = vocabulary.get("positive", ["good"])
        elif emotional_tone in [EmotionalTone.HOSTILE, EmotionalTone.ANXIOUS]:
            descriptors = vocabulary.get("negative", ["bad"])
        else:
            descriptors = vocabulary.get("neutral", ["notable"])
        
        descriptor = random.choice(descriptors)
        
        response = base_pattern.format(topic=f"{topic} is quite {descriptor}")
        
        # Add contextual comments
        if context.weather in self.contextual_responses["weather_comments"]:
            weather_comment = random.choice(self.contextual_responses["weather_comments"][context.weather])
            response += f" {weather_comment}"
        
        return response
    
    def _generate_quest_dialogue(
        self,
        patterns: Dict[str, Any],
        context: DialogueContext,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate quest-related dialogue"""
        
        if not context.current_quest:
            return "I'm afraid I don't know anything about your current endeavors."
        
        # Determine quest type from name/context
        quest_type = "heroic_quest"  # Default
        if "mystery" in context.current_quest.lower():
            quest_type = "mystery_quest"
        elif "political" in context.current_quest.lower() or "court" in context.current_quest.lower():
            quest_type = "political_quest"
        
        quest_reactions = self.contextual_responses["quest_reactions"].get(quest_type, [])
        
        if quest_reactions:
            base_response = random.choice(quest_reactions)
        else:
            base_response = "Your quest is a worthy endeavor."
        
        # Modify based on emotional tone
        if emotional_tone == EmotionalTone.ANXIOUS:
            base_response += " Though I fear the dangers that await you."
        elif emotional_tone == EmotionalTone.CONFIDENT:
            base_response += " I have no doubt you will succeed."
        elif emotional_tone == EmotionalTone.MYSTERIOUS:
            base_response += " But all is not as it seems."
        
        return base_response
    
    def _generate_personal_dialogue(
        self,
        patterns: Dict[str, Any],
        character_data: Dict[str, Any],
        relationship_status: str,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate personal dialogue based on relationship"""
        
        character_secret = character_data.get("secret", "I prefer to keep my past private")
        character_motivation = character_data.get("motivation", "I have my reasons for being here")
        
        relationship_modifiers = self.relationship_modifiers.get(relationship_status, {})
        information_sharing = relationship_modifiers.get("information_sharing", "minimal")
        
        if information_sharing == "minimal":
            return "I prefer not to discuss personal matters with strangers."
        
        elif information_sharing == "basic":
            return "There's not much to tell about my life here."
        
        elif information_sharing == "generous":
            if emotional_tone == EmotionalTone.FRIENDLY:
                return f"Since you ask, I can tell you that {character_motivation.lower()}."
            else:
                return f"I suppose I can share that {character_motivation.lower()}."
        
        elif information_sharing == "personal":
            return f"I trust you enough to tell you: {character_secret.lower()}."
        
        else:
            return "My past is complicated, but perhaps that's a story for another time."
    
    def _generate_confrontation_dialogue(
        self,
        patterns: Dict[str, Any],
        context: DialogueContext,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate confrontational dialogue"""
        
        confrontation_templates = [
            "You dare accuse me of such things?",
            "I don't appreciate your tone.",
            "You're treading on dangerous ground.",
            "Choose your next words carefully.",
            "I think this conversation is over."
        ]
        
        base_response = random.choice(confrontation_templates)
        
        # Modify based on emotional tone
        if emotional_tone == EmotionalTone.HOSTILE:
            base_response += " Get out of my sight."
        elif emotional_tone == EmotionalTone.ANXIOUS:
            base_response += " You're making me very uncomfortable."
        elif emotional_tone == EmotionalTone.CONFIDENT:
            base_response += " But I suppose I can address your concerns."
        
        return base_response
    
    def _generate_farewell(
        self,
        patterns: Dict[str, Any],
        player_name: str,
        relationship_status: str,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate farewell dialogue"""
        
        farewell_templates = {
            "friendly": [
                f"Farewell, {player_name}. May fortune smile upon you.",
                f"Until we meet again, {player_name}.",
                f"Safe travels, my friend."
            ],
            "neutral": [
                f"Goodbye, {player_name}.",
                f"Until next time.",
                f"Farewell."
            ],
            "hostile": [
                f"Don't let me see you again, {player_name}.",
                f"Good riddance.",
                f"Stay out of my way."
            ]
        }
        
        if emotional_tone in [EmotionalTone.FRIENDLY, EmotionalTone.COMPASSIONATE]:
            template_set = "friendly"
        elif emotional_tone == EmotionalTone.HOSTILE:
            template_set = "hostile"
        else:
            template_set = "neutral"
        
        return random.choice(farewell_templates[template_set])
    
    def _generate_ambient_dialogue(
        self,
        patterns: Dict[str, Any],
        context: DialogueContext,
        emotional_tone: EmotionalTone
    ) -> str:
        """Generate ambient/atmospheric dialogue"""
        
        ambient_templates = [
            "The wind carries strange whispers today.",
            "There's something different in the air.",
            "Times are changing, I can feel it.",
            "The old ways are not forgotten by all.",
            "Interesting times we live in."
        ]
        
        base_response = random.choice(ambient_templates)
        
        # Add location-specific comments
        if context.location in self.contextual_responses["location_comments"]:
            location_comment = random.choice(self.contextual_responses["location_comments"][context.location])
            base_response += f" {location_comment}"
        
        return base_response
    
    def _determine_information_reveal(
        self,
        character_data: Dict[str, Any],
        relationship_status: str,
        dialogue_type: DialogueType,
        context: DialogueContext
    ) -> List[str]:
        """Determine what information the character reveals"""
        
        revealed_info = []
        
        # Base information sharing on relationship
        relationship_modifiers = self.relationship_modifiers.get(relationship_status, {})
        sharing_level = relationship_modifiers.get("information_sharing", "minimal")
        
        if sharing_level == "minimal":
            if dialogue_type == DialogueType.INFORMATION and random.random() < 0.3:
                revealed_info.append("basic_location_info")
        
        elif sharing_level == "basic":
            if dialogue_type in [DialogueType.INFORMATION, DialogueType.QUEST_RELATED]:
                revealed_info.extend(["location_details", "general_rumors"])
        
        elif sharing_level == "generous":
            if dialogue_type == DialogueType.INFORMATION:
                revealed_info.extend(["detailed_knowledge", "useful_tips", "character_opinions"])
            elif dialogue_type == DialogueType.QUEST_RELATED:
                revealed_info.extend(["quest_hints", "potential_allies", "warnings"])
        
        elif sharing_level == "personal":
            revealed_info.extend(["personal_history", "secrets", "deep_knowledge"])
        
        # Special reveals based on character secrets
        character_secret = character_data.get("secret", "")
        if "knows_hidden_truth" in character_secret and relationship_status in ["friend", "ally"]:
            revealed_info.append("hidden_truth")
        
        return revealed_info
    
    def _calculate_relationship_impact(
        self,
        personality_type: str,
        dialogue_type: DialogueType,
        emotional_tone: EmotionalTone,
        context: DialogueContext
    ) -> int:
        """Calculate how this dialogue affects the relationship"""
        
        impact = 0
        
        # Base impact from dialogue type
        if dialogue_type == DialogueType.PERSONAL:
            impact += 2  # Personal conversations build relationships
        elif dialogue_type == DialogueType.CONFRONTATION:
            impact -= 3  # Confrontations damage relationships
        elif dialogue_type == DialogueType.INFORMATION:
            impact += 1  # Sharing information builds mild trust
        
        # Modify based on emotional tone
        if emotional_tone == EmotionalTone.FRIENDLY:
            impact += 2
        elif emotional_tone == EmotionalTone.HOSTILE:
            impact -= 4
        elif emotional_tone == EmotionalTone.COMPASSIONATE:
            impact += 3
        elif emotional_tone == EmotionalTone.SUSPICIOUS:
            impact -= 1
        
        # Personality-specific modifiers
        if personality_type == "jovial_merchant" and emotional_tone == EmotionalTone.FRIENDLY:
            impact += 1  # Merchants appreciate friendliness
        elif personality_type == "suspicious_rogue" and dialogue_type == DialogueType.CONFRONTATION:
            impact -= 1  # Rogues expect confrontation
        elif personality_type == "wise_mentor" and dialogue_type == DialogueType.PERSONAL:
            impact += 1  # Mentors value personal connection
        
        return max(-10, min(10, impact))  # Clamp between -10 and +10
    
    def _determine_unlocked_options(
        self,
        character_data: Dict[str, Any],
        relationship_status: str,
        information_revealed: List[str]
    ) -> List[str]:
        """Determine what new dialogue options are unlocked"""
        
        unlocked = []
        
        # Based on information revealed
        if "hidden_truth" in information_revealed:
            unlocked.append("ask_about_truth")
        if "quest_hints" in information_revealed:
            unlocked.append("request_specific_help")
        if "personal_history" in information_revealed:
            unlocked.append("discuss_past_events")
        
        # Based on relationship improvements
        if relationship_status == "friend":
            unlocked.extend(["ask_personal_favor", "share_secret"])
        elif relationship_status == "ally":
            unlocked.extend(["request_alliance", "strategic_planning"])
        
        # Based on character role
        character_role = character_data.get("role", "")
        if "merchant" in character_role:
            unlocked.extend(["discuss_trade", "ask_about_goods"])
        elif "guard" in character_role:
            unlocked.extend(["ask_about_security", "report_suspicious_activity"])
        elif "scholar" in character_role:
            unlocked.extend(["ask_about_lore", "request_research"])
        
        return unlocked
    
    def _check_follow_up_needed(
        self,
        dialogue_type: DialogueType,
        emotional_tone: EmotionalTone,
        information_revealed: List[str]
    ) -> bool:
        """Check if this dialogue requires a follow-up"""
        
        # Confrontations often need follow-up
        if dialogue_type == DialogueType.CONFRONTATION:
            return True
        
        # Emotional conversations might need follow-up
        if emotional_tone in [EmotionalTone.ANXIOUS, EmotionalTone.MELANCHOLIC]:
            return random.random() < 0.6
        
        # Information reveals might need clarification
        if "hidden_truth" in information_revealed:
            return True
        
        return False
    
    def _track_character_development(
        self,
        character_data: Dict[str, Any],
        dialogue_type: DialogueType,
        emotional_tone: EmotionalTone
    ) -> List[str]:
        """Track character development based on dialogue"""
        
        development = []
        
        # Track based on dialogue type
        if dialogue_type == DialogueType.PERSONAL:
            development.append("opened_up_personally")
        elif dialogue_type == DialogueType.CONFRONTATION:
            development.append("showed_defensive_side")
        
        # Track based on emotional tone
        if emotional_tone == EmotionalTone.COMPASSIONATE:
            development.append("displayed_empathy")
        elif emotional_tone == EmotionalTone.HOSTILE:
            development.append("showed_aggression")
        elif emotional_tone == EmotionalTone.MYSTERIOUS:
            development.append("maintained_secrets")
        
        # Character-specific development
        personality_type = character_data.get("personality_type", "")
        if personality_type == "wise_mentor" and dialogue_type == DialogueType.INFORMATION:
            development.append("shared_wisdom")
        elif personality_type == "suspicious_rogue" and emotional_tone == EmotionalTone.FRIENDLY:
            development.append("showed_unexpected_warmth")
        
        return development
    
    def get_conversation_history(self, character_id: str, player_id: str) -> List[Dict[str, Any]]:
        """Get the conversation history between character and player"""
        
        conversation_key = f"{character_id}_{player_id}"
        return self.conversation_memory.get(conversation_key, [])
    
    def add_to_conversation_history(
        self,
        character_id: str,
        player_id: str,
        dialogue_response: DialogueResponse,
        player_choice: str
    ):
        """Add an interaction to the conversation history"""
        
        conversation_key = f"{character_id}_{player_id}"
        
        if conversation_key not in self.conversation_memory:
            self.conversation_memory[conversation_key] = []
        
        self.conversation_memory[conversation_key].append({
            "timestamp": datetime.now().isoformat(),
            "player_choice": player_choice,
            "character_response": dialogue_response.text,
            "emotional_tone": dialogue_response.emotional_tone.value,
            "relationship_change": dialogue_response.advances_relationship,
            "information_revealed": dialogue_response.reveals_information
        })
        
        # Keep only last 20 interactions to prevent memory bloat
        if len(self.conversation_memory[conversation_key]) > 20:
            self.conversation_memory[conversation_key] = self.conversation_memory[conversation_key][-20:] 