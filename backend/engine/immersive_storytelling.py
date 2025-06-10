"""
AI-RPG-Alpha: Immersive Storytelling Engine

The heart of our text-based RPG experience. Creates authentic, believable
character interactions and vivid world descriptions that fully immerse
players in a living, breathing fantasy world.

Key Principles:
- Every NPC has authentic personality and behavior patterns
- Dialogue reflects character background, mood, and situation
- No "video game speak" - characters talk like real people in their world
- Rich sensory details in every description
- Dynamic world that reacts to player actions
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

class NPCPersonality(Enum):
    """Core personality archetypes that drive authentic behavior"""
    GRUFF_MERCHANT = "gruff_merchant"
    WISE_ELDER = "wise_elder"
    NERVOUS_GUARD = "nervous_guard"
    ARROGANT_NOBLE = "arrogant_noble"
    FRIENDLY_INNKEEPER = "friendly_innkeeper"
    SUSPICIOUS_THIEF = "suspicious_thief"
    DEVOUT_PRIEST = "devout_priest"
    BITTER_VETERAN = "bitter_veteran"
    CURIOUS_SCHOLAR = "curious_scholar"
    DESPERATE_BEGGAR = "desperate_beggar"
    AMBITIOUS_APPRENTICE = "ambitious_apprentice"
    WORLD_WEARY_TRAVELER = "world_weary_traveler"

class MoodState(Enum):
    """Current emotional state affecting behavior"""
    CONTENT = "content"
    IRRITATED = "irritated"
    EXCITED = "excited"
    FEARFUL = "fearful"
    ANGRY = "angry"
    MELANCHOLY = "melancholy"
    SUSPICIOUS = "suspicious"
    JOVIAL = "jovial"
    FOCUSED = "focused"
    DISTRACTED = "distracted"

class SocialClass(Enum):
    """Social standing affects speech patterns"""
    PEASANT = "peasant"
    MERCHANT = "merchant"
    ARTISAN = "artisan"
    NOBLE = "noble"
    CLERGY = "clergy"
    MILITARY = "military"
    CRIMINAL = "criminal"
    SCHOLAR = "scholar"

@dataclass
class ImmersiveCharacter:
    """A fully realized character with authentic personality"""
    name: str
    personality: NPCPersonality
    social_class: SocialClass
    current_mood: MoodState
    background_story: str
    speech_patterns: List[str]
    likes: List[str]
    dislikes: List[str]
    fears: List[str]
    goals: List[str]
    current_concerns: List[str]
    relationship_with_player: str = "stranger"
    reputation_knowledge: Dict[str, str] = field(default_factory=dict)
    recent_events_affecting_mood: List[str] = field(default_factory=list)

@dataclass
class SceneAtmosphere:
    """Immersive environmental context"""
    location: str
    time_of_day: str
    weather: str
    lighting: str
    sounds: List[str]
    smells: List[str]
    notable_details: List[str]
    mood: str
    activity_level: str
    danger_level: str

class ImmersiveStorytellingEngine:
    """
    Creates authentic, immersive storytelling experiences through:
    - Realistic character dialogue
    - Rich environmental descriptions
    - Dynamic world reactions
    - Authentic personality-driven interactions
    """
    
    def __init__(self):
        self.character_database = self._build_character_database()
        self.dialogue_patterns = self._build_dialogue_patterns()
        self.atmosphere_library = self._build_atmosphere_library()
        self.reaction_templates = self._build_reaction_templates()
        
    def _build_character_database(self) -> Dict[str, ImmersiveCharacter]:
        """Create a database of authentic NPCs"""
        
        characters = {}
        
        # Gruff Merchant - Marcus the Trader
        characters["marcus_trader"] = ImmersiveCharacter(
            name="Marcus",
            personality=NPCPersonality.GRUFF_MERCHANT,
            social_class=SocialClass.MERCHANT,
            current_mood=MoodState.IRRITATED,
            background_story="A veteran trader who's seen too many time-wasters and hagglers",
            speech_patterns=["direct", "impatient", "business-focused", "slightly rude"],
            likes=["quick transactions", "serious buyers", "gold coins"],
            dislikes=["window shoppers", "hagglers", "time wasters", "thieves"],
            fears=["bandits", "bad investments", "economic collapse"],
            goals=["make profit", "retire comfortably", "expand trade routes"],
            current_concerns=["recent bandit attacks", "slow business", "spoiled goods"]
        )
        
        # Wise Elder - Elder Miriam
        characters["elder_miriam"] = ImmersiveCharacter(
            name="Elder Miriam",
            personality=NPCPersonality.WISE_ELDER,
            social_class=SocialClass.PEASANT,
            current_mood=MoodState.CONTENT,
            background_story="Village elder who has lived through wars, famines, and good times",
            speech_patterns=["measured", "thoughtful", "uses old sayings", "speaks slowly"],
            likes=["young people seeking wisdom", "peace", "village traditions"],
            dislikes=["rashness", "disrespect for tradition", "violence"],
            fears=["village being destroyed", "losing cultural memory"],
            goals=["guide the young", "preserve village history", "peaceful resolution"],
            current_concerns=["recent troubles", "youth leaving for adventure"]
        )
        
        # Nervous Guard - Corporal Tim
        characters["guard_tim"] = ImmersiveCharacter(
            name="Corporal Tim",
            personality=NPCPersonality.NERVOUS_GUARD,
            social_class=SocialClass.MILITARY,
            current_mood=MoodState.FEARFUL,
            background_story="Young guard on his first posting, eager but inexperienced",
            speech_patterns=["stammers occasionally", "formal speech", "apologetic", "uncertain"],
            likes=["clear orders", "peaceful shifts", "approval from superiors"],
            dislikes=["trouble", "making decisions", "confrontation"],
            fears=["making mistakes", "combat", "disappointing superiors"],
            goals=["do his duty", "avoid trouble", "prove himself"],
            current_concerns=["strange sounds at night", "rumors of danger", "unclear orders"]
        )
        
        # Arrogant Noble - Lord Blackwood
        characters["lord_blackwood"] = ImmersiveCharacter(
            name="Lord Blackwood",
            personality=NPCPersonality.ARROGANT_NOBLE,
            social_class=SocialClass.NOBLE,
            current_mood=MoodState.CONTENT,
            background_story="Born to privilege, believes he's inherently superior to commoners",
            speech_patterns=["condescending", "formal", "uses big words", "expects deference"],
            likes=["flattery", "luxury", "being acknowledged", "fine things"],
            dislikes=["commoners", "dirt", "manual labor", "being questioned"],
            fears=["losing status", "peasant revolts", "public embarrassment"],
            goals=["maintain status", "increase wealth", "be respected"],
            current_concerns=["estate management", "political rivals", "maintaining image"]
        )
        
        # Friendly Innkeeper - Martha Goodbrew
        characters["martha_innkeeper"] = ImmersiveCharacter(
            name="Martha",
            personality=NPCPersonality.FRIENDLY_INNKEEPER,
            social_class=SocialClass.MERCHANT,
            current_mood=MoodState.JOVIAL,
            background_story="Runs the village inn, loves meeting travelers and hearing stories",
            speech_patterns=["warm", "chatty", "welcoming", "uses endearments"],
            likes=["travelers", "good stories", "busy inn", "laughter"],
            dislikes=["rude customers", "empty inn", "troublemakers"],
            fears=["losing the inn", "bad reputation", "violent customers"],
            goals=["successful business", "happy customers", "village gathering place"],
            current_concerns=["new competitors", "supply costs", "maintaining quality"]
        )
        
        # Suspicious Thief - Shadow
        characters["shadow_thief"] = ImmersiveCharacter(
            name="Shadow",
            personality=NPCPersonality.SUSPICIOUS_THIEF,
            social_class=SocialClass.CRIMINAL,
            current_mood=MoodState.SUSPICIOUS,
            background_story="Professional thief who trusts no one and always looks for angles",
            speech_patterns=["whispers", "vague", "evasive", "street slang"],
            likes=["profitable opportunities", "fellow outcasts", "shadows"],
            dislikes=["guards", "nosy people", "bright lights", "honest folk"],
            fears=["capture", "torture", "betrayal", "execution"],
            goals=["big score", "safe retirement", "revenge on enemies"],
            current_concerns=["heat from recent job", "rival thieves", "informants"]
        )
        
        return characters
    
    def _build_dialogue_patterns(self) -> Dict[NPCPersonality, Dict[str, List[str]]]:
        """Build authentic dialogue patterns for each personality type"""
        
        patterns = {}
        
        # Gruff Merchant
        patterns[NPCPersonality.GRUFF_MERCHANT] = {
            "greeting_stranger": [
                "Yeah? You buying or just looking?",
                "What do you want? Make it quick.",
                "Either buy something or move along.",
                "I haven't got all day. What'll it be?"
            ],
            "greeting_customer": [
                "Back again? Good. What do you need?",
                "Ah, a paying customer. What can I get you?",
                "You're one of the smart ones. What'll you have?"
            ],
            "refusing_haggle": [
                "My prices are fair. Take it or leave it.",
                "I'm not running a charity here.",
                "You want cheap? Go to the market stalls.",
                "That's the price. I don't negotiate with penny-pinchers."
            ],
            "item_not_available": [
                "Don't carry that. Never have, never will.",
                "You're asking for the wrong things in the wrong place.",
                "I'm a trader, not a miracle worker."
            ]
        }
        
        # Wise Elder
        patterns[NPCPersonality.WISE_ELDER] = {
            "greeting_stranger": [
                "Welcome, young one. What brings you to our humble village?",
                "I see a new face. Come, sit and tell me of your travels.",
                "Another seeker comes to us. What wisdom do you seek?",
                "The road brings many to our doorstep. What is your story?"
            ],
            "giving_advice": [
                "Listen well, child, for these old bones have seen much.",
                "In my years, I've learned that patience often succeeds where haste fails.",
                "The wise know that patience often succeeds where haste fails."
            ],
            "warning_about_danger": [
                "I fear dark times are coming, young one.",
                "The signs are troubling for those who know how to read them.",
                "Be careful, child. The world beyond our village grows dangerous."
            ]
        }
        
        # Nervous Guard
        patterns[NPCPersonality.NERVOUS_GUARD] = {
            "checking_credentials": [
                "Uh, excuse me... I need to see your, um, papers?",
                "S-sorry, but I have to ask... do you have business here?",
                "Please don't make this difficult. I'm just doing my job.",
                "The captain says I need to check everyone, so..."
            ],
            "reporting_problem": [
                "I don't know what to do about this...",
                "Maybe I should get my sergeant? This seems... complicated.",
                "I'm not sure I'm qualified to handle this situation.",
                "The manual doesn't cover anything like this..."
            ],
            "nervous_small_talk": [
                "It's been quiet tonight. Too quiet, if you ask me.",
                "I keep hearing strange noises. Probably just the wind... right?",
                "This job seemed easier during training.",
                "Do you think everything's... normal around here?"
            ]
        }
        
        # Arrogant Noble
        patterns[NPCPersonality.ARROGANT_NOBLE] = {
            "addressing_commoner": [
                "You may speak, but be brief and respectful.",
                "I suppose you have some trivial matter to discuss?",
                "Make your business known quickly. My time is valuable.",
                "Yes? What pressing concern brings a commoner to my attention?"
            ],
            "showing_disdain": [
                "How... pedestrian.",
                "I shouldn't be surprised by such... simplicity.",
                "The common folk never cease to disappoint.",
                "Such matters are beneath my consideration."
            ],
            "dismissing_someone": [
                "That will be all. You may go.",
                "I have more important matters to attend to.",
                "This conversation has run its course.",
                "Surely you have duties elsewhere?"
            ]
        }
        
        # Friendly Innkeeper
        patterns[NPCPersonality.FRIENDLY_INNKEEPER] = {
            "welcoming_guest": [
                "Welcome to the Sleepy Griffin, dearie! Come in, come in!",
                "Well hello there, traveler! What can old Martha do for you?",
                "Another weary soul finds their way to us! You're most welcome!",
                "Come in from the cold, love. Let's get you sorted out."
            ],
            "offering_food": [
                "You look like you could use a good meal, sweetheart.",
                "The stew's fresh and the bread's still warm. Perfect for travelers!",
                "I've got just the thing to fill that empty belly of yours.",
                "Sit yourself down and let Martha take care of you."
            ],
            "asking_for_news": [
                "What news from the road, dear? We don't get many visitors.",
                "Tell me, love, what's happening in the wide world?",
                "Any interesting tales from your travels? I do love a good story!",
                "The village gets so quiet. What excitement have you seen?"
            ]
        }
        
        # Suspicious Thief
        patterns[NPCPersonality.SUSPICIOUS_THIEF] = {
            "initial_contact": [
                "*looks around nervously* What do you want?",
                "I don't know you. Move along.",
                "*shifts uncomfortably* You're drawing attention.",
                "Wrong place for an honest conversation, if you catch my meaning."
            ],
            "potential_business": [
                "Maybe we have something to discuss... somewhere private.",
                "Depends what you're looking for, and what you're offering.",
                "*leans closer* There might be opportunities for the right person.",
                "I might know someone who knows someone... for a price."
            ],
            "warning_off": [
                "Walk away. This isn't your kind of business.",
                "You're asking dangerous questions, friend.",
                "Some doors are better left unopened.",
                "*glares* You didn't see me here. Understood?"
            ]
        }
        
        return patterns
    
    def generate_authentic_dialogue(
        self, 
        character_id: str, 
        dialogue_context: str,
        player_reputation: Dict[str, Any],
        recent_events: List[str],
        relationship_status: str = "stranger"
    ) -> str:
        """Generate authentic dialogue based on character personality and context"""
        
        if character_id not in self.character_database:
            return "The character looks at you silently."
        
        character = self.character_database[character_id]
        personality = character.personality
        mood = self._determine_current_mood(character, recent_events, player_reputation)
        
        # Get appropriate dialogue patterns
        patterns = self.dialogue_patterns.get(personality, {})
        
        # Choose specific dialogue based on context
        if dialogue_context == "first_meeting":
            base_dialogue = self._get_greeting_dialogue(patterns, relationship_status)
        elif dialogue_context == "business_inquiry":
            base_dialogue = self._get_business_dialogue(patterns, character, player_reputation)
        elif dialogue_context == "information_request":
            base_dialogue = self._get_information_dialogue(patterns, character, player_reputation)
        elif dialogue_context == "casual_conversation":
            base_dialogue = self._get_casual_dialogue(patterns, character, mood)
        else:
            base_dialogue = self._get_default_dialogue(patterns, character)
        
        # Apply mood and personality modifiers
        final_dialogue = self._apply_personality_modifiers(
            base_dialogue, character, mood, player_reputation
        )
        
        return final_dialogue
    
    def generate_immersive_scene_description(
        self,
        location: str,
        time_of_day: str,
        weather: str,
        activity_level: str,
        player_actions_context: List[str]
    ) -> str:
        """Generate rich, immersive scene descriptions"""
        
        atmosphere = self._get_location_atmosphere(location, time_of_day, weather)
        
        # Build layered description
        base_description = self._get_base_location_description(location)
        atmospheric_details = self._get_atmospheric_details(atmosphere)
        sensory_details = self._generate_sensory_details(atmosphere)
        activity_description = self._describe_current_activity(location, activity_level, time_of_day)
        
        # Weave together for immersive experience
        full_description = f"""
{base_description}

{atmospheric_details} {sensory_details}

{activity_description}
""".strip()
        
        return full_description
    
    def _determine_current_mood(
        self, 
        character: ImmersiveCharacter, 
        recent_events: List[str],
        player_reputation: Dict[str, Any]
    ) -> MoodState:
        """Determine character's current mood based on events and player reputation"""
        
        base_mood = character.current_mood
        
        # Recent events affect mood
        if "good_business" in recent_events:
            if character.personality == NPCPersonality.GRUFF_MERCHANT:
                return MoodState.CONTENT
        
        if "robbery_nearby" in recent_events:
            if character.personality in [NPCPersonality.NERVOUS_GUARD, NPCPersonality.FRIENDLY_INNKEEPER]:
                return MoodState.FEARFUL
        
        if "festival_day" in recent_events:
            if character.personality == NPCPersonality.FRIENDLY_INNKEEPER:
                return MoodState.EXCITED
        
        # Player reputation affects mood
        player_karma = player_reputation.get("karma", 0)
        
        if player_karma < -50:  # Evil reputation
            if character.personality in [NPCPersonality.DEVOUT_PRIEST, NPCPersonality.WISE_ELDER]:
                return MoodState.SUSPICIOUS
            elif character.personality == NPCPersonality.SUSPICIOUS_THIEF:
                return MoodState.CONTENT
        
        return base_mood
    
    def _get_greeting_dialogue(self, patterns: Dict[str, List[str]], relationship: str) -> str:
        """Get appropriate greeting based on relationship"""
        
        if relationship == "stranger":
            greetings = patterns.get("greeting_stranger", ["Hello there."])
        else:
            greetings = patterns.get("greeting_customer", patterns.get("greeting_friendly", ["Hello again."]))
        
        return random.choice(greetings)
    
    def _get_business_dialogue(
        self, 
        patterns: Dict[str, List[str]], 
        character: ImmersiveCharacter,
        player_reputation: Dict[str, Any]
    ) -> str:
        """Generate business-related dialogue"""
        
        if character.personality == NPCPersonality.GRUFF_MERCHANT:
            if player_reputation.get("karma", 0) < -30:
                return "I don't do business with troublemakers. Move along."
            else:
                business_lines = patterns.get("business_inquiry", [
                    "What are you looking to buy?",
                    "I've got quality goods. What do you need?"
                ])
                return random.choice(business_lines)
        
        elif character.personality == NPCPersonality.SUSPICIOUS_THIEF:
            if player_reputation.get("thieves_guild", 0) > 20:
                return random.choice(patterns.get("potential_business", ["Maybe we can talk business."]))
            else:
                return random.choice(patterns.get("warning_off", ["This isn't your kind of place."]))
        
        return "I'm not sure how I can help you with that."
    
    def _get_information_dialogue(
        self, 
        patterns: Dict[str, List[str]], 
        character: ImmersiveCharacter,
        player_reputation: Dict[str, Any]
    ) -> str:
        """Generate information-sharing dialogue"""
        
        if character.personality == NPCPersonality.WISE_ELDER:
            info_lines = patterns.get("giving_advice", [
                "Listen well, child, for these old bones have seen much.",
                "In my years, I've learned that patience often succeeds where haste fails."
            ])
            return random.choice(info_lines)
        
        elif character.personality == NPCPersonality.NERVOUS_GUARD:
            info_lines = patterns.get("nervous_small_talk", [
                "It's been quiet tonight. Too quiet, if you ask me.",
                "I keep hearing strange noises. Probably just the wind... right?"
            ])
            return random.choice(info_lines)
        
        return "I'm not sure I can help you with that information."
    
    def _get_casual_dialogue(
        self, 
        patterns: Dict[str, List[str]], 
        character: ImmersiveCharacter, 
        mood: MoodState
    ) -> str:
        """Generate casual conversation dialogue"""
        
        if character.personality == NPCPersonality.FRIENDLY_INNKEEPER:
            casual_lines = patterns.get("asking_for_news", [
                "What news from the road, dear? We don't get many visitors.",
                "Any interesting tales from your travels? I do love a good story!"
            ])
            return random.choice(casual_lines)
        
        elif character.personality == NPCPersonality.GRUFF_MERCHANT:
            if mood == MoodState.CONTENT:
                return "Business has been decent lately. Not that it's any of your concern."
            else:
                return "I don't have time for small talk. Either buy something or move along."
        
        return "I suppose we could chat for a moment."
    
    def _get_default_dialogue(
        self, 
        patterns: Dict[str, List[str]], 
        character: ImmersiveCharacter
    ) -> str:
        """Generate default dialogue when no specific context matches"""
        
        default_responses = {
            NPCPersonality.GRUFF_MERCHANT: "What do you want now?",
            NPCPersonality.WISE_ELDER: "Is there something you need, young one?",
            NPCPersonality.NERVOUS_GUARD: "Um, is everything alright here?",
            NPCPersonality.ARROGANT_NOBLE: "Yes? What is it?",
            NPCPersonality.FRIENDLY_INNKEEPER: "How can I help you today, dear?",
            NPCPersonality.SUSPICIOUS_THIEF: "*eyes you warily* What's your business?"
        }
        
        return default_responses.get(character.personality, "The character looks at you silently.")
    
    def _build_atmosphere_library(self) -> Dict[str, Any]:
        """Build library of atmospheric elements (placeholder for now)"""
        return {}
    
    def _build_reaction_templates(self) -> Dict[str, Any]:
        """Build templates for world reactions (placeholder for now)"""
        return {}
    
    def _get_base_location_description(self, location: str) -> str:
        """Get base description for a location"""
        
        descriptions = {
            "Village of Millbrook": """The peaceful village of Millbrook sits nestled in a valley surrounded by rolling green hills. Thatched-roof cottages line the cobblestone main street, their gardens bursting with colorful flowers and herbs. The village well stands at the center of the square, surrounded by a few market stalls and the welcoming facade of the Sleepy Griffin inn.""",
            
            "Thieves' Quarter": """Dark, narrow alleyways twist between crumbling tenements and abandoned buildings. The architecture here speaks of better times long past, but now broken shutters hang askew and shadows pool in every doorway. The few people you see move with purpose, keeping their heads down and their business to themselves."""
        }
        
        return descriptions.get(location, f"You find yourself in {location}, a place with its own unique character and atmosphere.")
    
    def _get_atmospheric_details(self, atmosphere: SceneAtmosphere) -> str:
        """Get atmospheric details based on time and weather"""
        
        time_details = {
            "day": "The sun hangs overhead, casting long shadows and warming the air.",
            "night": "Darkness has settled over the area, broken only by flickering torchlight.",
            "dawn": "The first light of dawn creeps across the sky, painting everything in soft hues.",
            "dusk": "The sun sets on the horizon, bathing the world in golden twilight.",
            "evening": "Evening has arrived, bringing with it a sense of quiet anticipation."
        }
        
        weather_details = {
            "clear": "The sky is clear and bright.",
            "cloudy": "Heavy clouds drift overhead, casting shifting shadows.",
            "rainy": "A gentle rain falls, creating puddles and filling the air with the scent of wet earth.",
            "misty": "A light mist hangs in the air, softening the edges of everything you see."
        }
        
        time_desc = time_details.get(atmosphere.time_of_day, "The time of day creates its own atmosphere.")
        weather_desc = weather_details.get(atmosphere.weather, "The weather adds its own character to the scene.")
        
        return f"{time_desc} {weather_desc}"
    
    def _describe_current_activity(self, location: str, activity_level: str, time_of_day: str) -> str:
        """Describe current activity in the location"""
        
        if location == "Village of Millbrook":
            if time_of_day == "day":
                if activity_level == "moderate":
                    return "Villagers go about their daily routines - children play in the streets, merchants hawk their wares, and the sound of hammering echoes from the blacksmith's shop."
                elif activity_level == "quiet":
                    return "Only a few villagers are out and about, moving quietly through their daily tasks."
            elif time_of_day == "night":
                return "Most villagers have retired for the evening, though warm light glows from cottage windows and the inn remains lively."
        
        elif location == "Thieves' Quarter":
            if time_of_day == "night":
                return "This is when the Quarter truly comes alive - shadowy figures slip between buildings, hushed conversations echo from doorways, and the scent of illicit dealings hangs heavy in the air."
            else:
                return "During daylight hours, the Quarter seems almost abandoned, though you sense watchful eyes tracking your movements."
        
        return "The area shows signs of life appropriate to the time and place."
    
    def _get_location_atmosphere(self, location: str, time_of_day: str, weather: str) -> SceneAtmosphere:
        """Get atmospheric details for location"""
        
        base_atmospheres = {
            "Village of Millbrook": SceneAtmosphere(
                location="Village of Millbrook",
                time_of_day=time_of_day,
                weather=weather,
                lighting="soft" if time_of_day == "day" else "dim",
                sounds=["chickens clucking", "distant conversation", "cart wheels on cobblestone"],
                smells=["baking bread", "wood smoke", "fresh hay"],
                notable_details=["flower boxes on windows", "children playing", "merchants setting up stalls"],
                mood="peaceful",
                activity_level="moderate",
                danger_level="minimal"
            ),
            "Thieves' Quarter": SceneAtmosphere(
                location="Thieves' Quarter",
                time_of_day=time_of_day,
                weather=weather,
                lighting="dim" if time_of_day == "day" else "shadowy",
                sounds=["whispered conversations", "footsteps in alleyways", "distant arguments"],
                smells=["stale ale", "unwashed bodies", "damp stone"],
                notable_details=["hooded figures", "graffiti on walls", "broken windows"],
                mood="tense",
                activity_level="secretive",
                danger_level="moderate"
            )
        }
        
        return base_atmospheres.get(location, SceneAtmosphere(
            location=location,
            time_of_day=time_of_day,
            weather=weather,
            lighting="natural",
            sounds=["ambient noise"],
            smells=["fresh air"],
            notable_details=["local features"],
            mood="neutral",
            activity_level="normal",
            danger_level="low"
        ))
    
    def _generate_sensory_details(self, atmosphere: SceneAtmosphere) -> str:
        """Generate rich sensory descriptions"""
        
        sensory_description = ""
        
        # Sounds
        if atmosphere.sounds:
            sound_desc = f"You hear {', '.join(atmosphere.sounds[:2])}"
            if len(atmosphere.sounds) > 2:
                sound_desc += f", and the distant {atmosphere.sounds[2]}"
            sensory_description += f"{sound_desc}. "
        
        # Smells
        if atmosphere.smells:
            smell_desc = f"The air carries the scent of {atmosphere.smells[0]}"
            if len(atmosphere.smells) > 1:
                smell_desc += f" mixed with {atmosphere.smells[1]}"
            sensory_description += f"{smell_desc}. "
        
        # Lighting
        lighting_descriptions = {
            "soft": "Gentle sunlight filters through the area",
            "dim": "Shadows gather in the corners",
            "shadowy": "Deep shadows dominate the scene",
            "bright": "Brilliant light illuminates everything",
            "flickering": "Torchlight flickers and dances"
        }
        
        lighting_desc = lighting_descriptions.get(atmosphere.lighting, "The light is natural")
        sensory_description += f"{lighting_desc}."
        
        return sensory_description
    
    def create_dynamic_world_reaction(
        self,
        player_action: str,
        location: str,
        witnesses: List[str],
        player_reputation: Dict[str, Any]
    ) -> str:
        """Create authentic world reactions to player actions"""
        
        reaction = ""
        
        # Analyze action type
        if "steal" in player_action.lower():
            if witnesses:
                reaction = "Gasps and shocked whispers ripple through the crowd. "
                reaction += "Someone shouts 'Thief!' and you hear the sound of people backing away from you."
            else:
                reaction = "You complete the deed unnoticed, though your heart pounds with the adrenaline of the risk."
        
        elif "help" in player_action.lower():
            reaction = "Your kindness doesn't go unnoticed. "
            if location == "Village of Millbrook":
                reaction += "The villagers exchange approving glances and nod respectfully in your direction."
            else:
                reaction += "Even in this rough place, your good deed earns a few grudging nods of respect."
        
        elif "attack" in player_action.lower():
            if location == "Village of Millbrook":
                reaction = "Screams of terror fill the air as peaceful villagers flee in panic. "
                reaction += "You've shattered the tranquility of this place, and the fear in their eyes will haunt you."
            else:
                reaction = "Violence erupts suddenly, drawing a crowd of onlookers who watch with morbid fascination."
        
        # Add reputation-based reactions
        karma = player_reputation.get("karma", 0)
        if karma < -50:
            reaction += " Some recognize you as a person of ill repute and give you a wide berth."
        elif karma > 50:
            reaction += " Your good reputation precedes you, and people seem more at ease in your presence."
        
        return reaction

# Global instance for easy access
storytelling_engine = ImmersiveStorytellingEngine()