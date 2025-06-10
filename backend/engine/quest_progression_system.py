"""
AI-RPG-Alpha: Bethesda-Style Quest Progression System

This module implements proper quest level gating and progression mechanics
inspired by Skyrim and Fallout games. Ensures players get appropriate
quests for their level and progression state.

Design Principles:
- Level 1-3: Tutorial quests, basic tasks (delivery, gathering, simple combat)
- Level 4-6: Local problems, minor faction work, exploration
- Level 7-10: Regional threats, faction advancement, dungeon delving
- Level 11-15: Major faction quests, significant story arcs
- Level 16-20: Leadership roles, world-changing decisions, epic threats

Story Structure:
- Every location has detailed descriptions
- Quests build naturally from previous actions
- No massive leaps in responsibility or power
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random

class ProgessionTier(Enum):
    """Quest progression tiers following Bethesda design"""
    NOVICE = "novice"          # Level 1-3: Basic tasks
    APPRENTICE = "apprentice"  # Level 4-6: Local problems
    JOURNEYMAN = "journeyman"  # Level 7-10: Regional threats
    EXPERT = "expert"          # Level 11-15: Major faction work
    MASTER = "master"          # Level 16-20: Leadership roles

class QuestComplexity(Enum):
    """Quest complexity levels"""
    SIMPLE = "simple"          # Single objective, one location
    MODERATE = "moderate"      # Multiple objectives, few locations
    COMPLEX = "complex"        # Multi-stage, multiple locations
    EPIC = "epic"             # Major storylines, world impact

@dataclass
class QuestProgression:
    """Defines how quests unlock and progress"""
    id: str
    title: str
    tier: ProgessionTier
    complexity: QuestComplexity
    min_level: int
    max_level: int
    prerequisite_quests: List[str] = field(default_factory=list)
    prerequisite_level: int = 1
    unlock_conditions: Dict[str, Any] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)
    location_type: str = "any"
    story_weight: int = 1  # How important for main progression

class QuestProgressionSystem:
    """
    Manages quest availability and progression following Bethesda's design.
    
    Key Features:
    - Level-appropriate content
    - Natural story progression
    - Meaningful location descriptions
    - Proper difficulty scaling
    """
    
    def __init__(self):
        self.progression_tree = self._build_progression_tree()
        self.location_descriptions = self._build_location_descriptions()
        self.current_location = "Village of Millbrook"
        
    def _build_progression_tree(self) -> Dict[str, QuestProgression]:
        """Build the complete quest progression tree"""
        
        progressions = {}
        
        # ================ NOVICE TIER (Level 1-3) ================
        # Tutorial and basic tasks only
        
        progressions["letter_delivery"] = QuestProgression(
            id="letter_delivery",
            title="Village Messenger",
            tier=ProgessionTier.NOVICE,
            complexity=QuestComplexity.SIMPLE,
            min_level=1,
            max_level=3,
            categories=["tutorial", "social"],
            location_type="village",
            story_weight=1
        )
        
        progressions["herb_gathering"] = QuestProgression(
            id="herb_gathering",
            title="Gathering Herbs",
            tier=ProgessionTier.NOVICE,
            complexity=QuestComplexity.SIMPLE,
            min_level=1,
            max_level=3,
            categories=["gathering", "tutorial"],
            location_type="village",
            story_weight=1
        )
        
        progressions["lost_cat"] = QuestProgression(
            id="lost_cat",
            title="Finding Whiskers",
            tier=ProgessionTier.NOVICE,
            complexity=QuestComplexity.SIMPLE,
            min_level=1,
            max_level=4,
            categories=["rescue", "social"],
            location_type="village",
            story_weight=1
        )
        
        progressions["apple_thief"] = QuestProgression(
            id="apple_thief",
            title="The Apple Thief",
            tier=ProgessionTier.NOVICE,
            complexity=QuestComplexity.SIMPLE,
            min_level=2,
            max_level=4,
            prerequisite_quests=["letter_delivery"],
            categories=["mystery", "social"],
            location_type="village",
            story_weight=1
        )
        
        progressions["first_rat"] = QuestProgression(
            id="first_rat",
            title="Cellar Rats",
            tier=ProgessionTier.NOVICE,
            complexity=QuestComplexity.SIMPLE,
            min_level=2,
            max_level=4,
            prerequisite_quests=["herb_gathering"],
            categories=["combat", "pest_control"],
            location_type="village",
            story_weight=1
        )
        
        # ================ APPRENTICE TIER (Level 4-6) ================
        # Local problems and minor responsibilities
        
        progressions["bandits_road"] = QuestProgression(
            id="bandits_road",
            title="Bandits on the Trade Road",
            tier=ProgessionTier.APPRENTICE,
            complexity=QuestComplexity.MODERATE,
            min_level=4,
            max_level=7,
            prerequisite_quests=["first_rat", "apple_thief"],
            categories=["combat", "protection"],
            location_type="road",
            story_weight=2
        )
        
        progressions["merchant_escort"] = QuestProgression(
            id="merchant_escort",
            title="Merchant Escort",
            tier=ProgessionTier.APPRENTICE,
            complexity=QuestComplexity.MODERATE,
            min_level=4,
            max_level=7,
            prerequisite_quests=["bandits_road"],
            categories=["escort", "trade"],
            location_type="road",
            story_weight=2
        )
        
        progressions["missing_miners"] = QuestProgression(
            id="missing_miners",
            title="The Missing Miners",
            tier=ProgessionTier.APPRENTICE,
            complexity=QuestComplexity.MODERATE,
            min_level=5,
            max_level=8,
            prerequisite_quests=["merchant_escort"],
            categories=["mystery", "rescue"],
            location_type="mines",
            story_weight=2
        )
        
        progressions["corrupt_guard"] = QuestProgression(
            id="corrupt_guard",
            title="The Corrupt Guard",
            tier=ProgessionTier.APPRENTICE,
            complexity=QuestComplexity.MODERATE,
            min_level=5,
            max_level=8,
            prerequisite_quests=["bandits_road"],
            categories=["investigation", "justice"],
            location_type="town",
            story_weight=2,
            unlock_conditions={"karma": ">50"}
        )
        
        progressions["small_time_smuggling"] = QuestProgression(
            id="small_time_smuggling",
            title="Contraband Runner",
            tier=ProgessionTier.APPRENTICE,
            complexity=QuestComplexity.MODERATE,
            min_level=5,
            max_level=8,
            prerequisite_quests=["bandits_road"],
            categories=["criminal", "stealth"],
            location_type="town",
            story_weight=2,
            unlock_conditions={"karma": "<-20"}
        )
        
        # ================ JOURNEYMAN TIER (Level 7-10) ================
        # Regional threats and faction work
        
        progressions["wolf_pack_leader"] = QuestProgression(
            id="wolf_pack_leader",
            title="The Alpha Wolf",
            tier=ProgessionTier.JOURNEYMAN,
            complexity=QuestComplexity.COMPLEX,
            min_level=7,
            max_level=11,
            prerequisite_quests=["missing_miners"],
            categories=["combat", "nature"],
            location_type="wilderness",
            story_weight=3
        )
        
        progressions["thieves_guild_contact"] = QuestProgression(
            id="thieves_guild_contact",
            title="A Whisper in the Dark",
            tier=ProgessionTier.JOURNEYMAN,
            complexity=QuestComplexity.COMPLEX,
            min_level=7,
            max_level=11,
            prerequisite_quests=["small_time_smuggling"],
            categories=["criminal", "faction"],
            location_type="city",
            story_weight=3,
            unlock_conditions={"karma": "<-30", "stealth_kills": ">2"}
        )
        
        progressions["temple_acolyte"] = QuestProgression(
            id="temple_acolyte",
            title="Temple Acolyte",
            tier=ProgessionTier.JOURNEYMAN,
            complexity=QuestComplexity.COMPLEX,
            min_level=7,
            max_level=11,
            prerequisite_quests=["corrupt_guard"],
            categories=["religious", "faction"],
            location_type="temple",
            story_weight=3,
            unlock_conditions={"karma": ">80", "temple_donations": ">100"}
        )
        
        progressions["ancient_tomb"] = QuestProgression(
            id="ancient_tomb",
            title="The Forgotten Tomb",
            tier=ProgessionTier.JOURNEYMAN,
            complexity=QuestComplexity.COMPLEX,
            min_level=8,
            max_level=12,
            prerequisite_quests=["wolf_pack_leader"],
            categories=["exploration", "dungeon"],
            location_type="ruins",
            story_weight=3
        )
        
        # ================ EXPERT TIER (Level 11-15) ================
        # Major faction advancement and significant responsibilities
        
        progressions["guild_lieutenant"] = QuestProgression(
            id="guild_lieutenant",
            title="Guild Lieutenant",
            tier=ProgessionTier.EXPERT,
            complexity=QuestComplexity.COMPLEX,
            min_level=11,
            max_level=16,
            prerequisite_quests=["thieves_guild_contact"],
            categories=["criminal", "leadership"],
            location_type="city",
            story_weight=4,
            unlock_conditions={"faction_thieves": ">60", "successful_heists": ">3"}
        )
        
        progressions["temple_priest"] = QuestProgression(
            id="temple_priest",
            title="Ordained Priest",
            tier=ProgessionTier.EXPERT,
            complexity=QuestComplexity.COMPLEX,
            min_level=11,
            max_level=16,
            prerequisite_quests=["temple_acolyte"],
            categories=["religious", "leadership"],
            location_type="temple",
            story_weight=4,
            unlock_conditions={"faction_temple": ">70", "blessed_items": ">5"}
        )
        
        progressions["regional_threat"] = QuestProgression(
            id="regional_threat",
            title="The Necromancer's Tower",
            tier=ProgessionTier.EXPERT,
            complexity=QuestComplexity.EPIC,
            min_level=12,
            max_level=17,
            prerequisite_quests=["ancient_tomb"],
            categories=["combat", "main_story"],
            location_type="tower",
            story_weight=5
        )
        
        progressions["trade_war"] = QuestProgression(
            id="trade_war",
            title="The Trade War",
            tier=ProgessionTier.EXPERT,
            complexity=QuestComplexity.COMPLEX,
            min_level=13,
            max_level=18,
            prerequisite_quests=["guild_lieutenant", "temple_priest"],
            categories=["politics", "faction"],
            location_type="city",
            story_weight=4
        )
        
        # ================ MASTER TIER (Level 16-20) ================
        # Leadership roles and world-changing decisions
        
        progressions["crime_lord"] = QuestProgression(
            id="crime_lord",
            title="Shadow Throne",
            tier=ProgessionTier.MASTER,
            complexity=QuestComplexity.EPIC,
            min_level=16,
            max_level=20,
            prerequisite_quests=["trade_war"],
            categories=["criminal", "ultimate"],
            location_type="city",
            story_weight=6,
            unlock_conditions={
                "faction_thieves": ">80", 
                "corruption": ">60",
                "karma": "<-100",
                "guild_reputation": ">90"
            }
        )
        
        progressions["high_priest"] = QuestProgression(
            id="high_priest",
            title="Divine Ascension",
            tier=ProgessionTier.MASTER,
            complexity=QuestComplexity.EPIC,
            min_level=16,
            max_level=20,
            prerequisite_quests=["trade_war"],
            categories=["religious", "ultimate"],
            location_type="cathedral",
            story_weight=6,
            unlock_conditions={
                "faction_temple": ">90", 
                "karma": ">150",
                "divine_favor": ">80"
            }
        )
        
        progressions["archmage_path"] = QuestProgression(
            id="archmage_path",
            title="Master of Mysteries",
            tier=ProgessionTier.MASTER,
            complexity=QuestComplexity.EPIC,
            min_level=17,
            max_level=20,
            prerequisite_quests=["regional_threat"],
            categories=["magic", "ultimate"],
            location_type="academy",
            story_weight=6,
            unlock_conditions={
                "magic_skill": ">80",
                "artifacts_found": ">10",
                "ancient_knowledge": ">50"
            }
        )
        
        return progressions
    
    def _build_location_descriptions(self) -> Dict[str, Dict[str, str]]:
        """Build detailed location descriptions for immersive storytelling"""
        
        return {
            "Village of Millbrook": {
                "arrival": "You arrive at the small village of Millbrook, nestled in a valley between rolling green hills. Smoke rises from cottage chimneys, and you can hear the gentle lowing of cattle in nearby pastures. The village consists of perhaps two dozen homes, a modest inn, a blacksmith's shop, and a small temple dedicated to the harvest goddess.",
                "description": "Millbrook is a peaceful farming community where everyone knows their neighbors. The main dirt road runs through the center of town, lined with well-tended gardens and whitewashed cottages. Children play in the streets while their parents tend to daily chores.",
                "atmosphere": "peaceful and rural"
            },
            "Crossroads Inn": {
                "arrival": "The Crossroads Inn sits at the intersection of two major trade routes. It's a large, two-story building with a stable attached, clearly built to accommodate traveling merchants and their wagons. Lanterns hang from the eaves, casting a warm glow in the evening light.",
                "description": "The inn is bustling with activity - merchants comparing goods, travelers sharing tales of distant lands, and local farmers selling produce. The common room is filled with the sounds of conversation, clinking mugs, and the occasional burst of laughter.",
                "atmosphere": "busy and commercial"
            },
            "Darkwood Forest": {
                "arrival": "You enter the edge of Darkwood Forest, where ancient oaks and towering pines create a thick canopy overhead. Shafts of sunlight filter through the leaves, creating patterns of light and shadow on the forest floor. The air is cool and filled with the scent of moss and fallen leaves.",
                "description": "The forest stretches for miles in all directions, a vast wilderness where few dare to venture alone. Game trails wind between the massive tree trunks, and you occasionally hear the distant call of woodland creatures echoing through the trees.",
                "atmosphere": "mysterious and wild"
            },
            "Riverside Town": {
                "arrival": "Riverside Town sprawls along both banks of the Silver River, connected by an ancient stone bridge. The town is larger than Millbrook, with cobblestone streets, a proper market square, and buildings rising two or three stories high.",
                "description": "The river serves as the town's lifeblood, powering mills and providing a route for river barges laden with goods. Fishermen cast their nets from small boats while children skip stones along the riverbank. The air carries the sound of water wheels and the calls of merchants in the market.",
                "atmosphere": "prosperous and connected"
            },
            "Abandoned Mines": {
                "arrival": "The entrance to the old copper mines yawns before you like a wound in the hillside. Rusted mining equipment lies scattered around the entrance, and the wooden supports visible in the tunnel mouth look weathered and unstable.",
                "description": "These mines were once the pride of the region, producing high-quality copper for trade. Now they lie abandoned after a series of cave-ins and mysterious disappearances. Local folk whisper that strange lights can sometimes be seen deep in the tunnels.",
                "atmosphere": "ominous and abandoned"
            },
            "Thieves' Quarter": {
                "arrival": "You enter the shadowy maze of narrow alleys and cramped buildings known as the Thieves' Quarter. Here, legitimate businesses operate alongside more questionable establishments, and the city watch patrols in groups of three or more.",
                "description": "This district operates by its own rules, where information is currency and loyalty can be bought. Taverns with no names serve customers who prefer anonymity, while coded messages are passed through a network of street children and dock workers.",
                "atmosphere": "dangerous and secretive"
            },
            "Temple District": {
                "arrival": "The Temple District rises on higher ground than the rest of the city, its white marble buildings gleaming in the sunlight. The main temple's spires reach toward the heavens, while smaller shrines and monasteries cluster around it like devoted followers.",
                "description": "Pilgrims from across the realm come here to seek blessing, healing, and spiritual guidance. The air is filled with the sound of prayer bells and burning incense. Priests in white robes move between the temples, tending to the faithful and maintaining the sacred grounds.",
                "atmosphere": "holy and serene"
            }
        }
    
    def get_current_location_description(self, location: str, time_of_day: str = "day") -> str:
        """Get detailed description of current location"""
        
        if location not in self.location_descriptions:
            return f"You find yourself in {location}, a place unlike any you've seen before."
        
        loc_data = self.location_descriptions[location]
        
        description = f"{loc_data['arrival']}\n\n{loc_data['description']}"
        
        # Add time-of-day variations
        if time_of_day == "night" and loc_data['atmosphere'] in ["peaceful", "holy"]:
            description += "\n\nAs night falls, the area takes on a more mysterious quality, with shadows lengthening and sounds carrying further in the still air."
        elif time_of_day == "dawn":
            description += "\n\nThe early morning light gives everything a fresh, hopeful quality as the day begins anew."
        
        return description
    
    def get_available_quests_for_level(self, player_level: int, completed_quests: List[str], 
                                     player_stats: Dict[str, Any]) -> List[QuestProgression]:
        """Get all quests available for the current player level and progression"""
        
        available = []
        
        for quest_id, progression in self.progression_tree.items():
            # Skip if already completed
            if quest_id in completed_quests:
                continue
            
            # Check level requirements
            if player_level < progression.min_level or player_level > progression.max_level:
                continue
            
            # Check prerequisites
            if progression.prerequisite_quests:
                if not all(prereq in completed_quests for prereq in progression.prerequisite_quests):
                    continue
            
            # Check unlock conditions
            if progression.unlock_conditions:
                if not self._check_unlock_conditions(progression.unlock_conditions, player_stats):
                    continue
            
            available.append(progression)
        
        # Sort by story weight and level appropriateness
        available.sort(key=lambda q: (q.story_weight, abs(q.min_level - player_level)))
        
        return available
    
    def _check_unlock_conditions(self, conditions: Dict[str, Any], player_stats: Dict[str, Any]) -> bool:
        """Check if unlock conditions are met"""
        
        for condition, required_value in conditions.items():
            if condition not in player_stats:
                return False
            
            current_value = player_stats[condition]
            
            if isinstance(required_value, str):
                if required_value.startswith(">"):
                    threshold = int(required_value[1:])
                    if current_value <= threshold:
                        return False
                elif required_value.startswith("<"):
                    threshold = int(required_value[1:])
                    if current_value >= threshold:
                        return False
            else:
                if current_value != required_value:
                    return False
        
        return True
    
    def get_quest_tier_for_level(self, level: int) -> ProgessionTier:
        """Get the appropriate quest tier for a given level"""
        
        if level <= 3:
            return ProgessionTier.NOVICE
        elif level <= 6:
            return ProgessionTier.APPRENTICE
        elif level <= 10:
            return ProgessionTier.JOURNEYMAN
        elif level <= 15:
            return ProgessionTier.EXPERT
        else:
            return ProgessionTier.MASTER
    
    def get_progression_recommendations(self, player_level: int, completed_quests: List[str]) -> Dict[str, Any]:
        """Get recommendations for quest progression"""
        
        current_tier = self.get_quest_tier_for_level(player_level)
        available_quests = self.get_available_quests_for_level(player_level, completed_quests, {})
        
        recommendations = {
            "current_tier": current_tier.value,
            "level_range": f"{player_level}",
            "available_count": len(available_quests),
            "next_tier_level": self._get_next_tier_level(current_tier),
            "progression_advice": self._get_progression_advice(player_level, available_quests)
        }
        
        return recommendations
    
    def _get_next_tier_level(self, current_tier: ProgessionTier) -> int:
        """Get the level when next tier unlocks"""
        
        tier_levels = {
            ProgessionTier.NOVICE: 4,
            ProgessionTier.APPRENTICE: 7,
            ProgessionTier.JOURNEYMAN: 11,
            ProgessionTier.EXPERT: 16,
            ProgessionTier.MASTER: 20
        }
        
        return tier_levels.get(current_tier, 20)
    
    def _get_progression_advice(self, player_level: int, available_quests: List[QuestProgression]) -> str:
        """Generate progression advice for the player"""
        
        if player_level <= 3:
            return "Focus on learning the basics - complete simple tasks in your village to gain experience and build your reputation."
        elif player_level <= 6:
            return "You're ready for more responsibility. Help solve local problems and begin building relationships with factions."
        elif player_level <= 10:
            return "Take on regional challenges and commit to faction storylines. Your actions now will shape your future opportunities."
        elif player_level <= 15:
            return "You're becoming a person of influence. Major factions will offer you leadership roles and important responsibilities."
        else:
            return "You're ready for the greatest challenges - decisions that will reshape the world around you."
    
    def validate_quest_progression(self, quest_id: str, player_level: int, 
                                 completed_quests: List[str]) -> Tuple[bool, str]:
        """Validate if a quest can be started based on progression rules"""
        
        if quest_id not in self.progression_tree:
            return False, "Quest not found in progression system"
        
        progression = self.progression_tree[quest_id]
        
        # Level check
        if player_level < progression.min_level:
            return False, f"You need to be at least level {progression.min_level} for this quest"
        
        if player_level > progression.max_level:
            return False, f"This quest is no longer available (max level {progression.max_level})"
        
        # Prerequisites check
        if progression.prerequisite_quests:
            missing = [q for q in progression.prerequisite_quests if q not in completed_quests]
            if missing:
                return False, f"You must complete these quests first: {', '.join(missing)}"
        
        return True, "Quest is available"
    
    def get_quest_difficulty_explanation(self, quest_id: str, player_level: int) -> str:
        """Get explanation of quest difficulty relative to player level"""
        
        if quest_id not in self.progression_tree:
            return "Unknown quest"
        
        progression = self.progression_tree[quest_id]
        level_diff = progression.min_level - player_level
        
        if level_diff > 3:
            return "Far too dangerous - you would likely die attempting this"
        elif level_diff > 1:
            return "Very challenging - significant risk of failure"
        elif level_diff == 1:
            return "Challenging but achievable - good for growth"
        elif level_diff == 0:
            return "Appropriate difficulty for your level"
        elif level_diff == -1:
            return "Slightly below your level - good for building confidence"
        elif level_diff <= -3:
            return "Too easy - minimal challenge and rewards"
        else:
            return "Moderate challenge" 