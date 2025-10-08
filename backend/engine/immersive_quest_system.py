"""
Immersive Quest System for The Northern Realms
==============================================

Redesigned quest system for book-like immersive storytelling:
- Organic story discovery through NPC relationships
- Natural life events that become adventures
- Character-driven narratives
- World exploration that reveals secrets
- Choices that feel like personal decisions, not mechanical tasks

Design Philosophy:
- Quests should feel like natural life events
- NPC relationships drive story progression
- Discovery happens through exploration and interaction
- Player feels like a character in a living world
- No mechanical "quest markers" or obvious objectives
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random


class ImmersiveQuestType(Enum):
    """Types of immersive quests"""
    RELATIONSHIP_DRIVEN = "relationship_driven"  # NPC relationships lead to quests
    EXPLORATION_DISCOVERY = "exploration_discovery"  # Natural discovery through exploration
    WORLD_EVENT = "world_event"  # Festivals, disasters, political events
    PERSONAL_GROWTH = "personal_growth"  # Character development quests
    MORAL_DILEMMA = "moral_dilemma"  # Natural conflicts that arise
    LEGACY_STORY = "legacy_story"  # Ancient mysteries and family histories


@dataclass
class ImmersiveQuestMilestone:
    """
    Immersive milestone that feels natural, not mechanical

    Instead of "Complete objective X", these are:
    - Natural conversation developments
    - Emotional turning points
    - Discovery moments
    - Relationship changes
    """
    milestone_id: str
    title: str
    description: str

    # Natural triggers (not mechanical objectives)
    trigger_conditions: Dict[str, any] = field(default_factory=dict)
    relationship_requirements: Dict[str, int] = field(default_factory=dict)  # NPC relationships needed
    exploration_requirements: List[str] = field(default_factory=list)  # Places visited

    # Natural outcomes
    relationship_changes: Dict[str, int] = field(default_factory=dict)
    world_state_changes: Dict[str, any] = field(default_factory=dict)
    personal_growth: Dict[str, int] = field(default_factory=dict)

    # Narrative style
    narrative_style: str = "conversational"  # conversational, reflective, dramatic, intimate
    emotional_tone: str = "neutral"  # hopeful, melancholic, tense, joyful

    def check_trigger_conditions(self, game_state: Dict[str, any]) -> bool:
        """Check if this milestone should naturally occur"""
        # Check relationship requirements
        for npc_id, required_level in self.relationship_requirements.items():
            current_level = game_state.get('npc_relationships', {}).get(npc_id, 0)
            if current_level < required_level:
                return False

        # Check exploration requirements
        for location in self.exploration_requirements:
            if location not in game_state.get('visited_locations', []):
                return False

        # Check trigger conditions
        for condition, value in self.trigger_conditions.items():
            if game_state.get(condition) != value:
                return False

        return True


@dataclass
class ImmersiveQuest:
    """
    Immersive quest that feels like a natural life story

    Instead of mechanical objectives, these quests:
    - Develop through natural NPC interactions
    - Emerge from character relationships
    - Grow from personal motivations
    - Feel like chapters in a character's life
    """
    quest_id: str
    title: str
    description: str
    quest_type: ImmersiveQuestType

    # Natural starting conditions
    starting_location: str
    trigger_npcs: List[str] = field(default_factory=list)
    world_context: str = ""  # Current world situation

    # Immersive milestones (not mechanical objectives)
    milestones: List[ImmersiveQuestMilestone] = field(default_factory=list)

    # Natural progression
    current_milestone_index: int = 0
    is_active: bool = False
    is_completed: bool = False

    # Character relationships that drive the quest
    key_relationships: Dict[str, str] = field(default_factory=dict)  # NPC -> relationship type
    emotional_arc: List[str] = field(default_factory=list)  # trust, doubt, friendship, etc.

    # World impact
    world_changes: Dict[str, any] = field(default_factory=dict)
    personal_growth: Dict[str, int] = field(default_factory=dict)

    def start_quest(self, game_state: Dict[str, any]) -> str:
        """Start the quest naturally"""
        if not self._can_start_quest(game_state):
            return ""

        self.is_active = True
        self.current_milestone_index = 0

        # Generate natural starting narrative
        return self._generate_starting_narrative(game_state)

    def _can_start_quest(self, game_state: Dict[str, any]) -> bool:
        """Check if quest can naturally begin"""
        # Check if player has visited starting location
        if self.starting_location not in game_state.get('visited_locations', []):
            return False

        # Check if key NPCs are available
        for npc_id in self.trigger_npcs:
            if npc_id not in game_state.get('known_npcs', []):
                return False

        return True

    def _generate_starting_narrative(self, game_state: Dict[str, any]) -> str:
        """Generate natural quest beginning"""
        player_name = game_state.get('player_name', 'You')

        if self.quest_type == ImmersiveQuestType.RELATIONSHIP_DRIVEN:
            npc_name = self.trigger_npcs[0] if self.trigger_npcs else "an old acquaintance"
            return (
                f"As {player_name} settles into {self.starting_location}, you notice {npc_name} "
                f"watching you with a mixture of recognition and concern. There's something "
                f"unsaid between you - a shared history that time hasn't erased."
            )

        elif self.quest_type == ImmersiveQuestType.EXPLORATION_DISCOVERY:
            return (
                f"The ancient stones of {self.starting_location} whisper secrets to those "
                f"who listen. As {player_name} explores the weathered ruins, you feel the "
                f"weight of untold stories pressing against the veil of time."
            )

        elif self.quest_type == ImmersiveQuestType.WORLD_EVENT:
            return (
                f"{self.starting_location} is alive with anticipation. Something is happening - "
                f"you can feel it in the air, in the way people hurry about their business, "
                f"in the unusual quiet that settles over normally bustling streets."
            )

        else:
            return (
                f"As {player_name} makes your way through {self.starting_location}, "
                f"you sense that your presence here is no accident. The world has a way "
                f"of drawing people together when their stories are meant to intersect."
            )

    def get_current_milestone(self) -> Optional[ImmersiveQuestMilestone]:
        """Get current milestone if conditions are met"""
        if not self.is_active or self.current_milestone_index >= len(self.milestones):
            return None

        current_milestone = self.milestones[self.current_milestone_index]

        # Check if milestone should naturally occur
        if current_milestone.check_trigger_conditions(self._get_quest_game_state()):
            return current_milestone

        return None

    def advance_milestone(self, game_state: Dict[str, any]) -> str:
        """Advance to next milestone naturally"""
        if self.current_milestone_index >= len(self.milestones):
            self.is_completed = True
            return self._generate_completion_narrative(game_state)

        current_milestone = self.milestones[self.current_milestone_index]

        # Apply milestone effects
        self._apply_milestone_effects(current_milestone, game_state)

        # Generate milestone narrative
        narrative = self._generate_milestone_narrative(current_milestone, game_state)

        # Advance to next milestone
        self.current_milestone_index += 1

        return narrative

    def _get_quest_game_state(self) -> Dict[str, any]:
        """Get relevant game state for this quest"""
        # This would be populated with actual game state
        return {
            'visited_locations': ['ironhold_village', 'frostmere_academy'],
            'known_npcs': ['grom_blacksmith', 'elara_mage'],
            'npc_relationships': {'grom_blacksmith': 5, 'elara_mage': 3},
            'player_level': 3,
            'player_name': 'You'
        }

    def _apply_milestone_effects(self, milestone: ImmersiveQuestMilestone, game_state: Dict[str, any]):
        """Apply natural effects of milestone progression"""
        # Update relationships
        for npc_id, change in milestone.relationship_changes.items():
            current = game_state.get('npc_relationships', {}).get(npc_id, 0)
            game_state['npc_relationships'][npc_id] = current + change

        # Apply world changes
        game_state.update(milestone.world_state_changes)

        # Apply personal growth
        for stat, change in milestone.personal_growth.items():
            current = game_state.get('player_stats', {}).get(stat, 0)
            game_state['player_stats'][stat] = current + change

    def _generate_milestone_narrative(self, milestone: ImmersiveQuestMilestone, game_state: Dict[str, any]) -> str:
        """Generate natural narrative for milestone"""
        player_name = game_state.get('player_name', 'You')

        # Different narrative styles based on milestone type
        if milestone.narrative_style == "conversational":
            return (
                f"As {player_name} shares a quiet moment with those around you, "
                f"the conversation naturally turns to {milestone.title.lower()}. "
                f"There's a shared understanding that passes between you - "
                f"no words are needed for what comes next."
            )

        elif milestone.narrative_style == "reflective":
            return (
                f"In a moment of quiet reflection, {player_name} realizes that "
                f"{milestone.title.lower()} has been building for some time. "
                f"The path ahead feels both inevitable and right."
            )

        elif milestone.narrative_style == "dramatic":
            return (
                f"The world seems to hold its breath as {player_name} faces "
                f"{milestone.title.lower()}. Every eye turns toward you, "
                f"every voice falls silent in anticipation."
            )

        else:  # intimate
            return (
                f"In the privacy of your thoughts, {player_name} acknowledges "
                f"that {milestone.title.lower()} has changed everything. "
                f"The person you were before this moment feels distant, "
                f"like a character from someone else's story."
            )

    def _generate_completion_narrative(self, game_state: Dict[str, any]) -> str:
        """Generate natural quest completion"""
        player_name = game_state.get('player_name', 'You')

        return (
            f"As {player_name} looks back on the path that brought you here, "
            f"you realize this journey has changed you in ways both subtle and profound. "
            f"The people you've met, the choices you've made, the moments of connection "
            f"and conflict - they've all woven themselves into the tapestry of your story."
        )

    def get_quest_status_text(self) -> str:
        """Get natural status description"""
        if not self.is_active:
            return "This story has not yet begun"

        if self.is_completed:
            return "This chapter has reached its natural conclusion"

        current_milestone = self.get_current_milestone()
        if current_milestone:
            return f"The story is building toward {current_milestone.title.lower()}"

        return "The story continues to unfold"


class ImmersiveQuestEngine:
    """
    Engine for managing immersive, organic quest progression

    Instead of mechanical quest tracking, this system:
    - Monitors natural story progression
    - Tracks character relationships
    - Responds to world state changes
    - Generates organic narrative flow
    """

    def __init__(self):
        self.active_quests: List[ImmersiveQuest] = []
        self.completed_quests: List[ImmersiveQuest] = []
        self.immersive_quests: Dict[str, ImmersiveQuest] = {}
        self._initialize_immersive_quests()

    def _initialize_immersive_quests(self):
        """Initialize all immersive quests"""

        # ========================================================================
        # RELATIONSHIP-DRIVEN QUESTS
        # ========================================================================

        # The Blacksmith's Sorrow
        blacksmith_quest = ImmersiveQuest(
            quest_id="blacksmith_sorrow",
            title="The Weight of Memory",
            description=(
                "Grom the blacksmith carries a burden that time hasn't lightened. "
                "His daughter Elara vanished into the ancient ruins, and the village "
                "has learned to look away from his grief."
            ),
            quest_type=ImmersiveQuestType.RELATIONSHIP_DRIVEN,
            starting_location="ironhold_village",
            trigger_npcs=["grom_blacksmith"],
            world_context="village_life",
            milestones=[
                ImmersiveQuestMilestone(
                    milestone_id="first_conversation",
                    title="A Shared Silence",
                    description="You notice Grom's haunted eyes and the way he stares at the mountains.",
                    trigger_conditions={"days_in_village": ">=3"},
                    relationship_requirements={"grom_blacksmith": 1},
                    narrative_style="conversational",
                    emotional_tone="melancholic",
                    relationship_changes={"grom_blacksmith": 2}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="shared_moment",
                    title="The Unspoken Bond",
                    description="Working at the forge together, you share a moment of understanding.",
                    trigger_conditions={"forge_visits": ">=2"},
                    relationship_requirements={"grom_blacksmith": 3},
                    narrative_style="intimate",
                    emotional_tone="hopeful",
                    relationship_changes={"grom_blacksmith": 3},
                    personal_growth={"empathy": 1}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="the_revelation",
                    title="The Name Spoken",
                    description="In a moment of quiet trust, Grom speaks his daughter's name.",
                    trigger_conditions={"trust_level": ">=5"},
                    relationship_requirements={"grom_blacksmith": 5},
                    narrative_style="reflective",
                    emotional_tone="bittersweet",
                    relationship_changes={"grom_blacksmith": 5},
                    world_state_changes={"elara_mentioned": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="the_decision",
                    title="The Path Chosen",
                    description="The ruins call to you now, carrying the weight of Grom's unspoken hope.",
                    trigger_conditions={"elara_mentioned": True},
                    exploration_requirements=["ancient_ruins"],
                    narrative_style="dramatic",
                    emotional_tone="determined",
                    relationship_changes={"grom_blacksmith": 10},
                    world_state_changes={"ruins_quest_active": True}
                )
            ],
            key_relationships={
                "grom_blacksmith": "mentor_figure",
                "elara_ghost": "lost_daughter"
            },
            emotional_arc=["grief", "connection", "hope", "determination"]
        )

        # ========================================================================
        # EXPLORATION DISCOVERY QUESTS
        # ========================================================================

        # The Whispering Mountains
        mountain_quest = ImmersiveQuest(
            quest_id="whispering_mountains",
            title="Echoes in Stone",
            description=(
                "The mountains around Ironhold seem to whisper when the wind blows just right. "
                "Ancient carvings on weathered stones suggest this place holds memories older than the kingdoms."
            ),
            quest_type=ImmersiveQuestType.EXPLORATION_DISCOVERY,
            starting_location="ironhold_mountains",
            trigger_npcs=["village_elder"],
            world_context="ancient_mysteries",
            milestones=[
                ImmersiveQuestMilestone(
                    milestone_id="first_carving",
                    title="The Stone's Secret",
                    description="You discover the first carved stone while hiking the mountain paths.",
                    trigger_conditions={"mountain_visits": ">=2"},
                    exploration_requirements=["mountain_trails"],
                    narrative_style="reflective",
                    emotional_tone="curious",
                    world_state_changes={"ancient_carvings_found": 1}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="pattern_emerges",
                    title="The Hidden Pattern",
                    description="The carvings form a map when viewed from the right angle.",
                    trigger_conditions={"ancient_carvings_found": ">=3"},
                    exploration_requirements=["mountain_peaks"],
                    narrative_style="dramatic",
                    emotional_tone="awed",
                    world_state_changes={"ancient_map_revealed": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="the_guardian",
                    title="The Mountain's Keeper",
                    description="A ancient spirit guardian appears, testing your worth to learn the mountain's secrets.",
                    trigger_conditions={"ancient_map_revealed": True},
                    exploration_requirements=["forgotten_shrine"],
                    narrative_style="dramatic",
                    emotional_tone="tense",
                    world_state_changes={"mountain_secrets_unlocked": True}
                )
            ],
            key_relationships={
                "mountain_spirit": "ancient_guardian",
                "village_elder": "storyteller"
            },
            emotional_arc=["curiosity", "wonder", "reverence", "understanding"]
        )

        # ========================================================================
        # WORLD EVENT QUESTS
        # ========================================================================

        # The Dragon Festival
        festival_quest = ImmersiveQuest(
            quest_id="dragon_festival",
            title="Wings Over Ironhold",
            description=(
                "Ironhold hosts an ancient festival celebrating the dragons that once shared the skies. "
                "This year feels different - the air carries whispers of change."
            ),
            quest_type=ImmersiveQuestType.WORLD_EVENT,
            starting_location="ironhold_castle",
            trigger_npcs=["king_alaric", "festival_organizer"],
            world_context="festival_season",
            milestones=[
                ImmersiveQuestMilestone(
                    milestone_id="festival_arrival",
                    title="The Celebration Begins",
                    description="The castle grounds come alive with music, food, and old traditions.",
                    trigger_conditions={"festival_day": True},
                    narrative_style="joyful",
                    emotional_tone="festive",
                    world_state_changes={"festival_spirits_high": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="ancient_ritual",
                    title="The Dragon Dance",
                    description="An ancient ritual connects the present to the dragon-filled past.",
                    trigger_conditions={"ritual_time": True},
                    relationship_requirements={"king_alaric": 3},
                    narrative_style="ceremonial",
                    emotional_tone="solemn",
                    world_state_changes={"dragon_ritual_completed": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="unexpected_visitor",
                    title="Wings in the Night",
                    description="A dragon appears during the festival, drawn by the ancient magic.",
                    trigger_conditions={"dragon_ritual_completed": True},
                    narrative_style="dramatic",
                    emotional_tone="awe",
                    world_state_changes={"dragon_contact_made": True}
                )
            ],
            key_relationships={
                "king_alaric": "ceremonial_host",
                "festival_crowd": "participants"
            },
            emotional_arc=["anticipation", "unity", "wonder", "transformation"]
        )

        # ========================================================================
        # PERSONAL GROWTH QUESTS
        # ========================================================================

        # The Mirror's Reflection
        reflection_quest = ImmersiveQuest(
            quest_id="mirror_reflection",
            title="The Face in the Mirror",
            description=(
                "Your dragon mark has begun to change you in subtle ways. "
                "The person staring back from still water looks both familiar and strange."
            ),
            quest_type=ImmersiveQuestType.PERSONAL_GROWTH,
            starting_location="anywhere",
            trigger_npcs=["self"],
            world_context="personal_journey",
            milestones=[
                ImmersiveQuestMilestone(
                    milestone_id="first_change",
                    title="The Mark Awakens",
                    description="Your dragon mark begins to feel warm, as if responding to your thoughts.",
                    trigger_conditions={"dragon_mark_level": ">=2"},
                    narrative_style="intimate",
                    emotional_tone="uncertain",
                    personal_growth={"self_awareness": 1}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="new_perspective",
                    title="Eyes of the Dragon",
                    description="Your vision sharpens, colors become more vivid, distances seem clearer.",
                    trigger_conditions={"dragon_mark_level": ">=4"},
                    narrative_style="reflective",
                    emotional_tone="wonder",
                    personal_growth={"perception": 2, "intuition": 1}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="inner_conflict",
                    title="The Dual Nature",
                    description="You feel the dragon's influence warring with your human heart.",
                    trigger_conditions={"dragon_mark_level": ">=6"},
                    narrative_style="dramatic",
                    emotional_tone="conflicted",
                    personal_growth={"wisdom": 2, "inner_conflict": 1}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="acceptance",
                    title="Embracing the Mark",
                    description="The dragon mark becomes part of you - not a curse, but a gift.",
                    trigger_conditions={"inner_conflict": ">=3"},
                    narrative_style="reflective",
                    emotional_tone="peaceful",
                    personal_growth={"harmony": 3, "dragon_affinity": 2}
                )
            ],
            key_relationships={
                "self": "inner_dialogue",
                "dragon_mark": "mysterious_ally"
            },
            emotional_arc=["confusion", "wonder", "conflict", "acceptance"]
        )

        # ========================================================================
        # MORAL DILEMMA QUESTS
        # ========================================================================

        # The Village's Secret
        village_quest = ImmersiveQuest(
            quest_id="village_secret",
            title="Shadows Beneath the Surface",
            description=(
                "The village of Eldridge seems too perfect, too peaceful. "
                "The smiles of the villagers don't quite reach their eyes."
            ),
            quest_type=ImmersiveQuestType.MORAL_DILEMMA,
            starting_location="eldridge_village",
            trigger_npcs=["village_mayor", "suspicious_villager"],
            world_context="hidden_darkness",
            milestones=[
                ImmersiveQuestMilestone(
                    milestone_id="surface_perfection",
                    title="The Perfect Village",
                    description="Eldridge seems idyllic - bountiful harvests, happy children, prosperous tradesmen.",
                    trigger_conditions={"village_visits": ">=2"},
                    narrative_style="conversational",
                    emotional_tone="pleasant",
                    world_state_changes={"village_surface_observed": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="cracks_appear",
                    title="The Hidden Truth",
                    description="A villager's slip of the tongue reveals that not everything is as it seems.",
                    trigger_conditions={"village_conversations": ">=5"},
                    relationship_requirements={"suspicious_villager": 2},
                    narrative_style="tense",
                    emotional_tone="suspicious",
                    world_state_changes={"village_secret_hinted": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="the_revelation",
                    title="The Terrible Choice",
                    description="You discover the village's dark secret - prosperity comes at a horrifying cost.",
                    trigger_conditions={"village_secret_hinted": True},
                    exploration_requirements=["village_underground"],
                    narrative_style="dramatic",
                    emotional_tone="horrified",
                    world_state_changes={"village_truth_revealed": True}
                ),

                ImmersiveQuestMilestone(
                    milestone_id="moral_crossroads",
                    title="The Decision",
                    description="You must choose: expose the truth and destroy the village, or remain silent.",
                    trigger_conditions={"village_truth_revealed": True},
                    narrative_style="dramatic",
                    emotional_tone="agonized",
                    world_state_changes={"village_fate_decided": True}
                )
            ],
            key_relationships={
                "village_mayor": "deceptive_leader",
                "suspicious_villager": "reluctant_confidant"
            },
            emotional_arc=["comfort", "doubt", "horror", "resolution"]
        )

        self.immersive_quests = {
            "blacksmith_sorrow": blacksmith_quest,
            "whispering_mountains": mountain_quest,
            "dragon_festival": festival_quest,
            "mirror_reflection": reflection_quest,
            "village_secret": village_quest
        }

    def check_for_natural_quest_triggers(self, game_state: Dict[str, any]) -> List[ImmersiveQuest]:
        """Check for quests that should naturally begin"""
        triggered_quests = []

        for quest in self.immersive_quests.values():
            if not quest.is_active and not quest.is_completed:
                if quest._can_start_quest(game_state):
                    triggered_quests.append(quest)

        return triggered_quests

    def process_immersive_turn(self, game_state: Dict[str, any]) -> Dict[str, any]:
        """Process natural quest progression"""
        response = {
            "new_quests_triggered": [],
            "milestone_advances": [],
            "quest_completions": [],
            "natural_narratives": []
        }

        # Check for new quest triggers
        new_quests = self.check_for_natural_quest_triggers(game_state)
        for quest in new_quests:
            quest.is_active = True
            response["new_quests_triggered"].append({
                "quest_id": quest.quest_id,
                "title": quest.title,
                "narrative": quest._generate_starting_narrative(game_state)
            })

        # Process active quests
        for quest in self.active_quests:
            if not quest.is_completed:
                current_milestone = quest.get_current_milestone()
                if current_milestone:
                    narrative = quest.advance_milestone(game_state)
                    response["milestone_advances"].append({
                        "quest_id": quest.quest_id,
                        "milestone_title": current_milestone.title,
                        "narrative": narrative,
                        "emotional_tone": current_milestone.emotional_tone
                    })

        return response

    def get_active_quest_narratives(self) -> List[str]:
        """Get natural narrative descriptions for active quests"""
        narratives = []

        for quest in self.active_quests:
            status_text = quest.get_quest_status_text()
            if status_text:
                narratives.append(f"{quest.title}: {status_text}")

        return narratives

    def get_quest_suggestions(self, game_state: Dict[str, any]) -> List[str]:
        """Get natural suggestions for what to do next"""
        suggestions = []

        # Location-based suggestions
        current_location = game_state.get('current_location', '')
        if current_location == 'ironhold_village':
            suggestions.extend([
                "Spend time at the blacksmith's forge",
                "Visit the village elder's home",
                "Explore the mountain trails nearby",
                "Attend the evening gathering at the tavern"
            ])
        elif current_location == 'frostmere_academy':
            suggestions.extend([
                "Study in the great library",
                "Observe a magical demonstration",
                "Speak with the archmage privately",
                "Explore the academy gardens"
            ])

        # Relationship-based suggestions
        for npc_id, relationship_level in game_state.get('npc_relationships', {}).items():
            if relationship_level >= 3:
                suggestions.append(f"Seek out {npc_id.replace('_', ' ').title()} for deeper conversation")

        return suggestions[:3]  # Return top 3 suggestions


# ============================================================================
# IMMERSIVE NARRATIVE TEMPLATES
# ============================================================================

class ImmersiveNarratives:
    """Templates for immersive, book-like narrative generation"""

    @staticmethod
    def generate_relationship_narrative(
        npc_name: str,
        relationship_level: int,
        context: str
    ) -> str:
        """Generate natural relationship-based narrative"""

        if relationship_level <= 1:
            return (
                f"{npc_name} regards you with cautious curiosity. There's a distance between you, "
                f"but also the potential for connection. {context} has brought you together, "
                f"but trust must be earned."
            )

        elif relationship_level <= 3:
            return (
                f"{npc_name} has come to trust you enough to share fragments of their story. "
                f"The barriers between strangers are crumbling, replaced by the first threads "
                f"of genuine connection. {context} feels more personal now."
            )

        elif relationship_level <= 5:
            return (
                f"{npc_name} sees you as a true friend and confidant. The masks have fallen away, "
                f"and you share in each other's vulnerabilities and hopes. {context} has become "
                f"a shared journey rather than individual paths."
            )

        else:
            return (
                f"{npc_name} has become family to you in spirit, if not blood. The bond between you "
                f"transcends ordinary friendship. {context} is no longer just circumstance - "
                f"it's the natural unfolding of lives intertwined by fate."
            )

    @staticmethod
    def generate_discovery_narrative(
        discovery_type: str,
        location: str,
        emotional_context: str = "wonder"
    ) -> str:
        """Generate natural discovery narrative"""

        if discovery_type == "ancient_ruins":
            return (
                f"The stones of {location} whisper of ages past, their weathered surfaces "
                f"holding secrets that time itself has tried to forget. As you trace the "
                f"ancient carvings, you feel a connection to those who walked these paths "
                f"centuries before you."
            )

        elif discovery_type == "hidden_knowledge":
            return (
                f"In the quiet corners of {location}, you find knowledge that was never "
                f"meant to be shared. The words on the page seem to pulse with their own "
                f"inner light, revealing truths that challenge everything you thought you knew."
            )

        elif discovery_type == "personal_insight":
            return (
                f"Amid the familiar surroundings of {location}, a moment of clarity strikes you. "
                f"The patterns of your life, once chaotic and random, suddenly reveal their "
                f"deeper purpose and meaning."
            )

        else:
            return (
                f"{location} reveals itself to you in a way it never has before. "
                f"What once seemed ordinary now holds layers of meaning and possibility."
            )

    @staticmethod
    def generate_emotional_moment(
        emotion: str,
        context: str,
        character_name: str = "You"
    ) -> str:
        """Generate natural emotional narrative"""

        emotion_narratives = {
            "hope": (
                f"Hope flickers in {character_name}'s heart like a candle in the darkness. "
                f"{context} reminds you that not all paths lead to despair."
            ),

            "doubt": (
                f"Doubt creeps into {character_name}'s thoughts like mist over water. "
                f"{context} makes you question choices that once seemed certain."
            ),

            "determination": (
                f"A quiet resolve settles over {character_name} like armor forged in fire. "
                f"{context} becomes not an obstacle, but a forge for your will."
            ),

            "melancholy": (
                f"A gentle sadness touches {character_name}'s spirit, like autumn leaves falling. "
                f"{context} reminds you of paths not taken and moments lost to time."
            ),

            "wonder": (
                f"Wonder fills {character_name}'s being like starlight in darkness. "
                f"{context} reveals the world's beauty in ways you never imagined."
            ),

            "fear": (
                f"Fear whispers in {character_name}'s ear like a shadow in the corner of vision. "
                f"{context} reminds you that some doors, once opened, cannot be closed."
            )
        }

        return emotion_narratives.get(emotion, f"{character_name} feels the weight of {context}.")

    @staticmethod
    def generate_world_reaction(
        player_action: str,
        world_context: str,
        affected_npcs: List[str] = None
    ) -> str:
        """Generate natural world reaction to player actions"""

        if not affected_npcs:
            affected_npcs = ["the people around you"]

        npc_text = " and ".join(affected_npcs)

        return (
            f"Your choice to {player_action.lower()} sends ripples through {world_context}. "
            f"{npc_text} watch you with new eyes, their opinions of you shifting like "
            f"sand beneath the tide. The world remembers, and the world judges."
        )

    @staticmethod
    def generate_organic_choice_prompt(
        current_situation: str,
        available_options: List[str],
        emotional_context: str = "thoughtful"
    ) -> str:
        """Generate natural choice presentation"""

        if emotional_context == "urgent":
            return (
                f"{current_situation}\n\n"
                f"The moment demands a choice. What do you do?"
            )

        elif emotional_context == "reflective":
            return (
                f"{current_situation}\n\n"
                f"You have time to consider your path forward. Each choice carries "
                f"its own weight and consequence."
            )

        else:  # thoughtful
            return (
                f"{current_situation}\n\n"
                f"The world continues around you, offering possibilities. "
                f"Your heart guides you toward certain paths more than others."
            )

