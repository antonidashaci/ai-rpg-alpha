"""
Achievement System for The Northern Realms
==========================================

Complete achievement system featuring:
- Quest completion achievements
- Combat mastery achievements
- Magic specialization achievements
- Political and diplomatic achievements
- Exploration and discovery achievements
- Steam integration ready architecture
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
import time


class AchievementCategory(Enum):
    """Achievement categories"""
    QUEST = "quest"
    COMBAT = "combat"
    MAGIC = "magic"
    POLITICS = "politics"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    ECONOMICS = "economics"


class AchievementRarity(Enum):
    """Achievement rarity levels"""
    COMMON = "common"          # Easy to get
    UNCOMMON = "uncommon"      # Moderate difficulty
    RARE = "rare"             # Hard to achieve
    EPIC = "epic"             # Very difficult
    LEGENDARY = "legendary"   # Extremely rare


@dataclass
class Achievement:
    """
    Individual achievement definition

    Contains:
    - Achievement metadata
    - Unlock conditions
    - Rewards and descriptions
    """
    achievement_id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity

    # Unlock conditions
    quest_requirements: List[str] = field(default_factory=list)
    stat_requirements: Dict[str, int] = field(default_factory=dict)
    combat_requirements: Dict[str, int] = field(default_factory=dict)
    magic_requirements: Dict[str, int] = field(default_factory=dict)
    exploration_requirements: Dict[str, int] = field(default_factory=dict)

    # Rewards
    gold_reward: int = 0
    experience_reward: int = 0
    title_reward: str = ""
    special_reward: str = ""

    # Steam integration
    steam_achievement_id: str = ""

    # Hidden achievement (not shown until unlocked)
    is_hidden: bool = False

    def check_unlock_conditions(self, game_state: Dict[str, any]) -> bool:
        """Check if achievement should be unlocked"""
        # Check quest requirements
        if self.quest_requirements:
            completed_quests = game_state.get('completed_quests', set())
            if not all(quest in completed_quests for quest in self.quest_requirements):
                return False

        # Check stat requirements
        if self.stat_requirements:
            player_stats = game_state.get('player_stats', {})
            for stat, required_value in self.stat_requirements.items():
                if player_stats.get(stat, 0) < required_value:
                    return False

        # Check combat requirements
        if self.combat_requirements:
            combat_stats = game_state.get('combat_stats', {})
            for stat, required_value in self.combat_requirements.items():
                if combat_stats.get(stat, 0) < required_value:
                    return False

        # Check magic requirements
        if self.magic_requirements:
            magic_stats = game_state.get('magic_stats', {})
            for stat, required_value in self.magic_requirements.items():
                if magic_stats.get(stat, 0) < required_value:
                    return False

        # Check exploration requirements
        if self.exploration_requirements:
            exploration_stats = game_state.get('exploration_stats', {})
            for stat, required_value in self.exploration_requirements.items():
                if exploration_stats.get(stat, 0) < required_value:
                    return False

        return True


@dataclass
class AchievementProgress:
    """Player's achievement progress"""
    achievement_id: str
    unlocked: bool = False
    unlocked_at: Optional[float] = None
    progress: Dict[str, int] = field(default_factory=dict)
    notified: bool = False


class AchievementEngine:
    """
    Achievement system engine for The Northern Realms

    Manages:
    - Achievement definitions and tracking
    - Progress monitoring and unlocking
    - Reward distribution
    - Steam integration
    """

    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.player_progress: Dict[str, AchievementProgress] = {}
        self._initialize_achievements()

    def _initialize_achievements(self):
        """Initialize all achievements"""

        # ========================================================================
        # QUEST ACHIEVEMENTS
        # ========================================================================

        self.achievements.update({
            "first_quest": Achievement(
                achievement_id="first_quest",
                name="The Journey Begins",
                description="Complete your first quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.COMMON,
                quest_requirements=[],
                experience_reward=100,
                title_reward="Quest Initiate"
            ),

            "dragon_slayer": Achievement(
                achievement_id="dragon_slayer",
                name="Dragon Slayer",
                description="Complete the main Dragon Prophecy quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.RARE,
                quest_requirements=["northern_realms_dragon_prophecy"],
                gold_reward=1000,
                experience_reward=500,
                title_reward="Dragon's Bane",
                steam_achievement_id="DRAGON_SLAYER"
            ),

            "mage_academy": Achievement(
                achievement_id="mage_academy",
                name="Arcane Scholar",
                description="Complete the Mage Guild research quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.UNCOMMON,
                quest_requirements=["mage_guild_research"],
                experience_reward=300,
                title_reward="Academy Graduate"
            ),

            "master_craftsman": Achievement(
                achievement_id="master_craftsman",
                name="Master Craftsman",
                description="Complete the blacksmith's masterpiece quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.UNCOMMON,
                quest_requirements=["blacksmith_masterpiece"],
                gold_reward=500,
                experience_reward=250
            ),

            "political_master": Achievement(
                achievement_id="political_master",
                name="Master Diplomat",
                description="Complete the political conspiracy quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.RARE,
                quest_requirements=["political_conspiracy"],
                experience_reward=400,
                title_reward="Royal Advisor"
            ),

            "ancient_explorer": Achievement(
                achievement_id="ancient_explorer",
                name="Ancient Explorer",
                description="Complete the ancient ruins discovery quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.UNCOMMON,
                quest_requirements=["ancient_ruins_discovery"],
                experience_reward=350,
                title_reward="Ruins Raider"
            ),

            "dragon_friend": Achievement(
                achievement_id="dragon_friend",
                name="Dragon Friend",
                description="Complete the dragon diplomacy quest",
                category=AchievementCategory.QUEST,
                rarity=AchievementRarity.EPIC,
                quest_requirements=["dragon_diplomacy"],
                gold_reward=2000,
                experience_reward=1000,
                title_reward="Dragon Ambassador",
                steam_achievement_id="DRAGON_PEACE"
            ),

            # ========================================================================
            # COMBAT ACHIEVEMENTS
            # ========================================================================

            "first_blood": Achievement(
                achievement_id="first_blood",
                name="First Blood",
                description="Win your first combat encounter",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.COMMON,
                combat_requirements={"victories": 1},
                experience_reward=50
            ),

            "combat_master": Achievement(
                achievement_id="combat_master",
                name="Combat Master",
                description="Win 25 combat encounters",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.UNCOMMON,
                combat_requirements={"victories": 25},
                experience_reward=200,
                title_reward="Battle-Hardened"
            ),

            "tactical_genius": Achievement(
                achievement_id="tactical_genius",
                name="Tactical Genius",
                description="Win 10 combats using environmental features",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.RARE,
                combat_requirements={"environmental_victories": 10},
                experience_reward=300,
                title_reward="Master Tactician"
            ),

            "dragon_hunter": Achievement(
                achievement_id="dragon_hunter",
                name="Dragon Hunter",
                description="Defeat 5 dragon-type enemies",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.EPIC,
                combat_requirements={"dragons_defeated": 5},
                gold_reward=1500,
                experience_reward=750,
                title_reward="Dragonslayer",
                steam_achievement_id="DRAGON_HUNTER"
            ),

            "pacifist": Achievement(
                achievement_id="pacifist",
                name="Pacifist",
                description="Complete a quest without entering combat",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.RARE,
                quest_requirements=["mage_guild_research"],  # Example pacifist quest
                experience_reward=400,
                title_reward="Peaceful Resolver"
            ),

            # ========================================================================
            # MAGIC ACHIEVEMENTS
            # ========================================================================

            "first_spell": Achievement(
                achievement_id="first_spell",
                name="First Spell",
                description="Cast your first spell",
                category=AchievementCategory.MAGIC,
                rarity=AchievementRarity.COMMON,
                magic_requirements={"spells_cast": 1},
                experience_reward=50
            ),

            "spell_master": Achievement(
                achievement_id="spell_master",
                name="Spell Master",
                description="Learn 10 different spells",
                category=AchievementCategory.MAGIC,
                rarity=AchievementRarity.UNCOMMON,
                magic_requirements={"spells_known": 10},
                experience_reward=250,
                title_reward="Archmage"
            ),

            "destruction_master": Achievement(
                achievement_id="destruction_master",
                name="Master of Destruction",
                description="Reach maximum affinity in Destruction magic",
                category=AchievementCategory.MAGIC,
                rarity=AchievementRarity.RARE,
                magic_requirements={"destruction_affinity": 20},
                experience_reward=300,
                title_reward="Destroyer"
            ),

            "mana_efficient": Achievement(
                achievement_id="mana_efficient",
                name="Mana Efficient",
                description="Cast 50 spells without running out of mana",
                category=AchievementCategory.MAGIC,
                rarity=AchievementRarity.RARE,
                magic_requirements={"efficient_casts": 50},
                experience_reward=200,
                title_reward="Mana Conservator"
            ),

            # ========================================================================
            # POLITICS ACHIEVEMENTS
            # ========================================================================

            "first_alliance": Achievement(
                achievement_id="first_alliance",
                name="First Alliance",
                description="Form your first alliance with a kingdom",
                category=AchievementCategory.POLITICS,
                rarity=AchievementRarity.COMMON,
                stat_requirements={"alliances_formed": 1},
                experience_reward=100,
                title_reward="Diplomat"
            ),

            "kingdom_unifier": Achievement(
                achievement_id="kingdom_unifier",
                name="Kingdom Unifier",
                description="Form alliances with all three kingdoms",
                category=AchievementCategory.POLITICS,
                rarity=AchievementRarity.EPIC,
                stat_requirements={"alliances_formed": 3},
                gold_reward=2000,
                experience_reward=1000,
                title_reward="High Chancellor",
                steam_achievement_id="KINGDOM_UNIFIER"
            ),

            "political_mastermind": Achievement(
                achievement_id="political_mastermind",
                name="Political Mastermind",
                description="Successfully navigate 5 political events",
                category=AchievementCategory.POLITICS,
                rarity=AchievementRarity.RARE,
                stat_requirements={"political_events_navigated": 5},
                experience_reward=400,
                title_reward="Master Politician"
            ),

            # ========================================================================
            # EXPLORATION ACHIEVEMENTS
            # ========================================================================

            "first_discovery": Achievement(
                achievement_id="first_discovery",
                name="First Discovery",
                description="Discover your first point of interest",
                category=AchievementCategory.EXPLORATION,
                rarity=AchievementRarity.COMMON,
                exploration_requirements={"locations_discovered": 1},
                experience_reward=50
            ),

            "world_explorer": Achievement(
                achievement_id="world_explorer",
                name="World Explorer",
                description="Discover 20 different locations",
                category=AchievementCategory.EXPLORATION,
                rarity=AchievementRarity.UNCOMMON,
                exploration_requirements={"locations_discovered": 20},
                experience_reward=300,
                title_reward="Cartographer"
            ),

            "treasure_hunter": Achievement(
                achievement_id="treasure_hunter",
                name="Treasure Hunter",
                description="Find 10 hidden treasures or artifacts",
                category=AchievementCategory.EXPLORATION,
                rarity=AchievementRarity.RARE,
                exploration_requirements={"treasures_found": 10},
                gold_reward=1000,
                experience_reward=400,
                title_reward="Master Treasure Hunter"
            ),

            # ========================================================================
            # SOCIAL ACHIEVEMENTS
            # ========================================================================

            "first_friend": Achievement(
                achievement_id="first_friend",
                name="First Friend",
                description="Reach friendly reputation with an NPC",
                category=AchievementCategory.SOCIAL,
                rarity=AchievementRarity.COMMON,
                stat_requirements={"friendly_npcs": 1},
                experience_reward=100,
                title_reward="Friendly Face"
            ),

            "social_butterfly": Achievement(
                achievement_id="social_butterfly",
                name="Social Butterfly",
                description="Reach friendly reputation with 10 NPCs",
                category=AchievementCategory.SOCIAL,
                rarity=AchievementRarity.UNCOMMON,
                stat_requirements={"friendly_npcs": 10},
                experience_reward=250,
                title_reward="People Person"
            ),

            # ========================================================================
            # ECONOMICS ACHIEVEMENTS
            # ========================================================================

            "first_gold": Achievement(
                achievement_id="first_gold",
                name="First Gold",
                description="Earn your first 100 gold pieces",
                category=AchievementCategory.ECONOMICS,
                rarity=AchievementRarity.COMMON,
                stat_requirements={"total_gold_earned": 100},
                experience_reward=50
            ),

            "merchant_prince": Achievement(
                achievement_id="merchant_prince",
                name="Merchant Prince",
                description="Earn 10,000 gold pieces total",
                category=AchievementCategory.ECONOMICS,
                rarity=AchievementRarity.RARE,
                stat_requirements={"total_gold_earned": 10000},
                gold_reward=500,
                experience_reward=300,
                title_reward="Merchant Prince"
            )
        })

        # Initialize progress tracking for all achievements
        for achievement_id in self.achievements:
            self.player_progress[achievement_id] = AchievementProgress(
                achievement_id=achievement_id
            )

    def check_achievements(self, game_state: Dict[str, any]) -> List[Achievement]:
        """Check for newly unlocked achievements"""
        newly_unlocked = []

        for achievement in self.achievements.values():
            progress = self.player_progress[achievement.achievement_id]

            # Skip if already unlocked
            if progress.unlocked:
                continue

            # Check unlock conditions
            if achievement.check_unlock_conditions(game_state):
                progress.unlocked = True
                progress.unlocked_at = time.time()
                newly_unlocked.append(achievement)

        return newly_unlocked

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get all currently unlocked achievements"""
        return [
            self.achievements[progress.achievement_id]
            for progress in self.player_progress.values()
            if progress.unlocked
        ]

    def get_locked_achievements(self) -> List[Achievement]:
        """Get all currently locked achievements"""
        return [
            self.achievements[progress.achievement_id]
            for progress in self.player_progress.values()
            if not progress.unlocked
        ]

    def get_achievement_progress(self, achievement_id: str) -> AchievementProgress:
        """Get progress for specific achievement"""
        return self.player_progress.get(achievement_id, AchievementProgress(achievement_id))

    def calculate_completion_percentage(self) -> float:
        """Calculate overall achievement completion percentage"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return (unlocked / total) * 100 if total > 0 else 0

    def get_achievements_by_category(self, category: AchievementCategory) -> List[Achievement]:
        """Get achievements by category"""
        return [
            achievement for achievement in self.achievements.values()
            if achievement.category == category
        ]

    def get_achievements_by_rarity(self, rarity: AchievementRarity) -> List[Achievement]:
        """Get achievements by rarity"""
        return [
            achievement for achievement in self.achievements.values()
            if achievement.rarity == rarity
        ]

    def export_steam_achievements(self) -> Dict[str, Dict[str, any]]:
        """Export achievements in Steam-compatible format"""
        steam_data = {}

        for achievement in self.achievements.values():
            if achievement.steam_achievement_id:
                steam_data[achievement.steam_achievement_id] = {
                    "name": achievement.name,
                    "description": achievement.description,
                    "icon": f"achievement_{achievement.achievement_id}",
                    "hidden": achievement.is_hidden
                }

        return steam_data

    def get_achievement_summary(self) -> Dict[str, any]:
        """Get comprehensive achievement summary"""
        unlocked = self.get_unlocked_achievements()
        locked = self.get_locked_achievements()

        # Group by category
        category_stats = {}
        for category in AchievementCategory:
            category_achievements = self.get_achievements_by_category(category)
            unlocked_in_category = [
                a for a in unlocked if a.category == category
            ]
            category_stats[category.value] = {
                "total": len(category_achievements),
                "unlocked": len(unlocked_in_category),
                "percentage": (len(unlocked_in_category) / len(category_achievements)) * 100
            }

        # Group by rarity
        rarity_stats = {}
        for rarity in AchievementRarity:
            rarity_achievements = self.get_achievements_by_rarity(rarity)
            unlocked_in_rarity = [
                a for a in unlocked if a.rarity == rarity
            ]
            rarity_stats[rarity.value] = {
                "total": len(rarity_achievements),
                "unlocked": len(unlocked_in_rarity),
                "percentage": (len(unlocked_in_rarity) / len(rarity_achievements)) * 100
            }

        return {
            "total_achievements": len(self.achievements),
            "unlocked_achievements": len(unlocked),
            "locked_achievements": len(locked),
            "completion_percentage": self.calculate_completion_percentage(),
            "category_stats": category_stats,
            "rarity_stats": rarity_stats,
            "recent_unlocks": [
                {
                    "name": achievement.name,
                    "category": achievement.category.value,
                    "rarity": achievement.rarity.value,
                    "unlocked_at": self.player_progress[achievement.achievement_id].unlocked_at
                }
                for achievement in unlocked[-5:]  # Last 5 unlocks
            ]
        }


# ============================================================================
# ACHIEVEMENT NOTIFICATIONS
# ============================================================================

class AchievementNotification:
    """Achievement unlock notification"""

    def __init__(self, achievement: Achievement):
        self.achievement = achievement
        self.timestamp = time.time()

    def get_display_text(self) -> str:
        """Get text for displaying achievement unlock"""
        rarity_icons = {
            AchievementRarity.COMMON: "",
            AchievementRarity.UNCOMMON: "⭐",
            AchievementRarity.RARE: "🌟",
            AchievementRarity.EPIC: "💎",
            AchievementRarity.LEGENDARY: "👑"
        }

        icon = rarity_icons.get(self.achievement.rarity, "")

        return f"{icon} ACHIEVEMENT UNLOCKED!\n{self.achievement.name}\n{self.achievement.description}"

    def get_rewards_text(self) -> str:
        """Get text describing achievement rewards"""
        rewards = []

        if self.achievement.gold_reward > 0:
            rewards.append(f"💰 {self.achievement.gold_reward} gold")

        if self.achievement.experience_reward > 0:
            rewards.append(f"⭐ {self.achievement.experience_reward} experience")

        if self.achievement.title_reward:
            rewards.append(f"🏆 Title: {self.achievement.title_reward}")

        if self.achievement.special_reward:
            rewards.append(f"🎁 {self.achievement.special_reward}")

        return ", ".join(rewards) if rewards else "No rewards"

