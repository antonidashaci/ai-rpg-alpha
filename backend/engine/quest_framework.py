"""
Long-Form Quest Framework
==========================

Bethesda-quality quest progression system with:
- 30-40 turn quest structure
- Multi-act progression (Setup, Pursuit, Climax)
- Meaningful choices every 3-5 turns
- Combat integration at appropriate intervals
- Consequence propagation across the narrative

Design Philosophy:
- Quests are long-form narratives, not quick tasks
- Every 3-5 turns provides meaningful choice or revelation
- Combat encounters integrated naturally at 8-10 turn intervals
- Major revelations every 15 turns
- Climax at turn 30+ with multiple solution paths
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class QuestAct(Enum):
    """Quest progression acts"""
    SETUP = "setup"              # Turns 1-15: Mystery setup, investigation
    PURSUIT = "pursuit"          # Turns 16-30: Deeper revelations, complications
    CLIMAX = "climax"           # Turns 31-40: High-stakes resolution
    AFTERMATH = "aftermath"      # Post-resolution consequences


class QuestStatus(Enum):
    """Quest status"""
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class ChoiceImpact(Enum):
    """Impact level of player choices"""
    MINOR = "minor"              # Small immediate effect
    MODERATE = "moderate"        # Affects current quest arc
    MAJOR = "major"             # Changes quest direction
    CRITICAL = "critical"        # Determines ending and consequences


@dataclass
class QuestMilestone:
    """
    Key milestone in quest progression
    
    Milestones occur every 3-5 turns and represent meaningful
    progression points where player choices matter.
    """
    turn_number: int
    title: str
    description: str
    choices: List[str]
    choice_impacts: Dict[int, ChoiceImpact]
    triggers_combat: bool = False
    reveals_information: bool = False
    narrative_weight: int = 1  # 1-5, affects story importance
    
    def is_major_milestone(self) -> bool:
        """Check if this is a major story milestone"""
        return self.narrative_weight >= 4 or self.reveals_information


@dataclass
class QuestChoice:
    """Player choice and its consequences"""
    turn_number: int
    choice_text: str
    choice_index: int
    impact_level: ChoiceImpact
    immediate_consequence: str
    delayed_consequences: List[str] = field(default_factory=list)
    affects_ending: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class QuestProgression:
    """Tracks player progression through quest"""
    current_turn: int = 1
    current_act: QuestAct = QuestAct.SETUP
    milestones_completed: List[int] = field(default_factory=list)
    choices_made: List[QuestChoice] = field(default_factory=list)
    combat_encounters_completed: int = 0
    information_revealed: List[str] = field(default_factory=list)
    
    def advance_turn(self):
        """Advance to next turn and update act if needed"""
        self.current_turn += 1
        
        # Update act based on turn number
        if self.current_turn <= 15:
            self.current_act = QuestAct.SETUP
        elif self.current_turn <= 30:
            self.current_act = QuestAct.PURSUIT
        elif self.current_turn <= 40:
            self.current_act = QuestAct.CLIMAX
        else:
            self.current_act = QuestAct.AFTERMATH
    
    def complete_milestone(self, turn: int):
        """Mark milestone as completed"""
        if turn not in self.milestones_completed:
            self.milestones_completed.append(turn)
    
    def record_choice(self, choice: QuestChoice):
        """Record player choice"""
        self.choices_made.append(choice)
    
    def reveal_information(self, info: str):
        """Add revealed information"""
        if info not in self.information_revealed:
            self.information_revealed.append(info)
    
    def get_major_choices(self) -> List[QuestChoice]:
        """Get all major and critical choices"""
        return [
            c for c in self.choices_made 
            if c.impact_level in [ChoiceImpact.MAJOR, ChoiceImpact.CRITICAL]
        ]


@dataclass
class LongFormQuest:
    """
    Complete long-form quest definition
    
    Represents a 30-40 turn quest with multi-act structure,
    meaningful choices, and integrated combat encounters.
    """
    quest_id: str
    title: str
    description: str
    scenario: str  # "northern_realms", "whispering_town", "neo_tokyo"
    total_turns: int = 40
    milestones: List[QuestMilestone] = field(default_factory=list)
    progression: QuestProgression = field(default_factory=QuestProgression)
    status: QuestStatus = QuestStatus.NOT_STARTED
    
    # Narrative elements
    opening_narrative: str = ""
    act_transitions: Dict[QuestAct, str] = field(default_factory=dict)
    possible_endings: List[str] = field(default_factory=list)
    
    # Quest metadata
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"
    estimated_playtime_minutes: int = 120
    
    def start_quest(self) -> str:
        """Initialize quest and return opening narrative"""
        self.status = QuestStatus.ACTIVE
        self.progression = QuestProgression()
        return self.opening_narrative
    
    def get_current_milestone(self) -> Optional[QuestMilestone]:
        """Get milestone for current turn if exists"""
        return next(
            (m for m in self.milestones if m.turn_number == self.progression.current_turn),
            None
        )
    
    def should_trigger_combat(self) -> bool:
        """Check if combat should be triggered on current turn"""
        # Combat every 8-10 turns
        turn = self.progression.current_turn
        return turn % 9 == 0 or turn % 10 == 0
    
    def get_act_progress_percentage(self) -> float:
        """Get progress through current act as percentage"""
        turn = self.progression.current_turn
        
        if self.progression.current_act == QuestAct.SETUP:
            return (turn / 15) * 100
        elif self.progression.current_act == QuestAct.PURSUIT:
            return ((turn - 15) / 15) * 100
        elif self.progression.current_act == QuestAct.CLIMAX:
            return ((turn - 30) / 10) * 100
        else:
            return 100.0
    
    def get_overall_progress_percentage(self) -> float:
        """Get overall quest progress"""
        return (self.progression.current_turn / self.total_turns) * 100
    
    def determine_ending(self) -> str:
        """Determine quest ending based on player choices"""
        major_choices = self.progression.get_major_choices()
        
        # Simple ending determination (can be enhanced with more sophisticated logic)
        if not major_choices:
            return self.possible_endings[0] if self.possible_endings else "default_ending"
        
        # Count critical choices
        critical_count = sum(
            1 for c in major_choices 
            if c.impact_level == ChoiceImpact.CRITICAL
        )
        
        # Determine ending based on critical choices
        ending_index = min(critical_count, len(self.possible_endings) - 1)
        return self.possible_endings[ending_index] if self.possible_endings else "default_ending"


class QuestFrameworkEngine:
    """
    Engine for managing long-form quest progression
    
    Handles turn-based progression, milestone tracking,
    choice recording, and narrative pacing.
    """
    
    def __init__(self):
        self.active_quest: Optional[LongFormQuest] = None
    
    def load_quest(self, quest: LongFormQuest):
        """Load a quest into the engine"""
        self.active_quest = quest
    
    def start_quest(self) -> str:
        """Start the loaded quest"""
        if not self.active_quest:
            return "No quest loaded!"
        
        return self.active_quest.start_quest()
    
    def process_turn(
        self,
        player_choice: str,
        choice_index: int,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a turn in the active quest
        
        Returns:
            Dictionary with narrative, choices, metadata, and combat trigger
        """
        if not self.active_quest:
            return {"error": "No active quest"}
        
        quest = self.active_quest
        
        # Record player choice if at a milestone
        current_milestone = quest.get_current_milestone()
        if current_milestone:
            impact = current_milestone.choice_impacts.get(choice_index, ChoiceImpact.MINOR)
            choice_record = QuestChoice(
                turn_number=quest.progression.current_turn,
                choice_text=player_choice,
                choice_index=choice_index,
                impact_level=impact
            )
            quest.progression.record_choice(choice_record)
            quest.progression.complete_milestone(quest.progression.current_turn)
        
        # Advance turn
        quest.progression.advance_turn()
        
        # Check for act transition
        act_transitioned = self._check_act_transition()
        
        # Check if combat should trigger
        combat_trigger = quest.should_trigger_combat()
        
        # Get next milestone
        next_milestone = quest.get_current_milestone()
        
        # Build response
        response = {
            "turn_number": quest.progression.current_turn,
            "current_act": quest.progression.current_act.value,
            "act_progress": quest.get_act_progress_percentage(),
            "overall_progress": quest.get_overall_progress_percentage(),
            "combat_trigger": combat_trigger,
            "act_transitioned": act_transitioned,
            "milestone_reached": next_milestone is not None,
            "quest_status": quest.status.value
        }
        
        # Add milestone data if present
        if next_milestone:
            response["milestone"] = {
                "title": next_milestone.title,
                "description": next_milestone.description,
                "choices": next_milestone.choices,
                "is_major": next_milestone.is_major_milestone()
            }
        
        # Check if quest should end
        if quest.progression.current_turn >= quest.total_turns:
            ending = quest.determine_ending()
            quest.status = QuestStatus.COMPLETED
            response["quest_completed"] = True
            response["ending"] = ending
        
        return response
    
    def _check_act_transition(self) -> bool:
        """Check if act has transitioned and return transition narrative if so"""
        if not self.active_quest:
            return False
        
        turn = self.active_quest.progression.current_turn
        
        # Act transitions happen at specific turns
        if turn == 16:  # Setup -> Pursuit
            return True
        elif turn == 31:  # Pursuit -> Climax
            return True
        
        return False
    
    def get_quest_state(self) -> Dict[str, Any]:
        """Get complete quest state for UI/save system"""
        if not self.active_quest:
            return {"error": "No active quest"}
        
        quest = self.active_quest
        
        return {
            "quest_id": quest.quest_id,
            "title": quest.title,
            "status": quest.status.value,
            "turn_number": quest.progression.current_turn,
            "current_act": quest.progression.current_act.value,
            "total_turns": quest.total_turns,
            "progress_percentage": quest.get_overall_progress_percentage(),
            "milestones_completed": len(quest.progression.milestones_completed),
            "total_milestones": len(quest.milestones),
            "choices_made": len(quest.progression.choices_made),
            "major_choices": len(quest.progression.get_major_choices()),
            "combat_encounters": quest.progression.combat_encounters_completed,
            "information_revealed": quest.progression.information_revealed
        }


# ============================================================================
# QUEST TEMPLATES
# ============================================================================

class QuestLibrary:
    """Pre-designed long-form quests for The Northern Realms"""
    
    @staticmethod
    def northern_realms_quest() -> LongFormQuest:
        """
        Main quest for The Northern Realms (Epic Fantasy)
        Import from dedicated quest file for better organization
        """
        from .northern_realms_quest import create_northern_realms_quest
        return create_northern_realms_quest()
    
    # Legacy placeholder - not used
    @staticmethod
    def _old_incomplete_quest() -> LongFormQuest:
        """Old incomplete quest template"""
        milestones = [
            # ACT I: SETUP (Turns 1-15)
            QuestMilestone(
                turn_number=1,
                title="Arrival in Ashmouth",
                description="You arrive in the coastal town of Ashmouth. Something feels... wrong.",
                choices=[
                    "Investigate the abandoned lighthouse",
                    "Visit the local tavern to gather information",
                    "Explore the old library"
                ],
                choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MAJOR},
                narrative_weight=3
            ),
            QuestMilestone(
                turn_number=5,
                title="First Whispers",
                description="You begin to hear whispers that others don't. The townsfolk avoid certain topics.",
                choices=[
                    "Confront the mayor about the whispers",
                    "Research the town's history secretly",
                    "Try to ignore the whispers and focus on your mission"
                ],
                choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.CRITICAL},
                reveals_information=True,
                narrative_weight=4
            ),
            QuestMilestone(
                turn_number=9,
                title="The Cult Discovery",
                description="You've discovered evidence of a cult operating in the town.",
                choices=[
                    "Infiltrate the cult meeting",
                    "Alert the authorities",
                    "Gather more evidence before acting"
                ],
                choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.MAJOR},
                triggers_combat=True,
                narrative_weight=5
            ),
            QuestMilestone(
                turn_number=15,
                title="Reality Fractures",
                description="Reality itself begins to warp. You've seen too much. [ACT I FINALE]",
                choices=[
                    "Embrace the knowledge, no matter the cost",
                    "Fight to maintain your sanity",
                    "Seek the forbidden texts for answers"
                ],
                choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
                reveals_information=True,
                narrative_weight=5
            ),
            
            # ACT II: PURSUIT (Turns 16-30)
            QuestMilestone(
                turn_number=18,
                title="The Deep Truth",
                description="You've learned what lies beneath Ashmouth. The truth is worse than you imagined.",
                choices=[
                    "Plan to destroy the source",
                    "Attempt to negotiate with the entities",
                    "Document everything for the outside world"
                ],
                choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
                narrative_weight=4
            ),
            QuestMilestone(
                turn_number=22,
                title="Allies or Enemies?",
                description="Other investigators have arrived. Can they be trusted?",
                choices=[
                    "Share everything you know",
                    "Test their loyalty with partial truths",
                    "Work alone - trust no one"
                ],
                choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MAJOR},
                triggers_combat=True,
                narrative_weight=3
            ),
            QuestMilestone(
                turn_number=28,
                title="The Ritual Begins",
                description="The cult is preparing for something catastrophic. Time is running out.",
                choices=[
                    "Disrupt the ritual immediately",
                    "Let it begin to understand their true purpose",
                    "Attempt to use the ritual for your own ends"
                ],
                choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
                triggers_combat=True,
                reveals_information=True,
                narrative_weight=5
            ),
            
            # ACT III: CLIMAX (Turns 31-40)
            QuestMilestone(
                turn_number=31,
                title="The Entity Awakens",
                description="What you've feared has come to pass. An eldritch being stirs. [CLIMAX BEGINS]",
                choices=[
                    "Fight the impossible",
                    "Offer yourself as a vessel",
                    "Attempt the forbidden counter-ritual"
                ],
                choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
                triggers_combat=True,
                narrative_weight=5
            ),
            QuestMilestone(
                turn_number=35,
                title="Sanity's Edge",
                description="You stand at the precipice of madness. Your final choice approaches.",
                choices=[
                    "Cling to your humanity",
                    "Embrace transcendence",
                    "Sacrifice everything to seal the breach"
                ],
                choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
                reveals_information=True,
                narrative_weight=5
            ),
            QuestMilestone(
                turn_number=40,
                title="The End... or Beginning?",
                description="The culmination of your journey. The fate of Ashmouth and your soul hangs in the balance.",
                choices=[
                    "Seal the entity and save the town",
                    "Become the new herald",
                    "Destroy everything - town, entity, and self"
                ],
                choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
                triggers_combat=True,
                reveals_information=True,
                narrative_weight=5
            )
        ]
        
        quest = LongFormQuest(
            quest_id="whispering_town_main",
            title="The Whispering Town",
            description="Investigate strange occurrences in the coastal town of Ashmouth, where reality itself seems to be unraveling.",
            scenario="whispering_town",
            total_turns=40,
            milestones=milestones,
            opening_narrative=(
                "The bus drops you off at the edge of Ashmouth as fog rolls in from the sea. "
                "The driver gives you a strange look but says nothing. As you walk into town, "
                "the whispers begin—too faint to understand, too persistent to ignore.\n\n"
                "Your contact was supposed to meet you here. She sent you cryptic warnings about "
                "'the truth beneath' and 'the price of knowledge.' Now she's vanished.\n\n"
                "The town feels wrong. Not dangerous, not yet—but wrong, like reality is slightly "
                "out of focus here. You've investigated strange phenomena before, but this... "
                "this is different.\n\n"
                "The fog thickens. The whispers grow louder. Your investigation begins."
            ),
            possible_endings=[
                "sealed_victory",      # Saved town, maintained sanity
                "pyrrhic_victory",     # Saved town, lost sanity
                "dark_ascension",      # Became herald, transcended humanity
                "total_destruction",   # Destroyed everything
                "eternal_prisoner"     # Trapped by entity
            ],
            tags=["cosmic_horror", "mystery", "sanity", "long_form"],
            difficulty="hard",
            estimated_playtime_minutes=180
        )
        
        return quest
    
    @staticmethod
    def northern_realms_quest() -> LongFormQuest:
        """
        Main quest for The Northern Realms (Epic Fantasy Scenario)
        
        A 40-turn epic fantasy quest involving ancient prophecies,
        dragon threats, and political intrigue.
        """
        # Similar structure for fantasy quest
        # (Abbreviated for space - follows same pattern)
        
        quest = LongFormQuest(
            quest_id="northern_realms_main",
            title="The Dragon's Prophecy",
            description="Ancient prophecies speak of a chosen one who will unite the kingdoms against the rising dragon threat.",
            scenario="northern_realms",
            total_turns=40,
            opening_narrative=(
                "The northern winds carry tales of dragons awakening from their ancient slumber. "
                "You, a humble adventurer, have been marked by fate—a dragon's symbol burns on your hand. "
                "The kingdoms are divided, the dragons are rising, and only you can prevent the coming cataclysm."
            ),
            possible_endings=[
                "united_kingdoms",
                "dragon_alliance",
                "lone_hero_sacrifice",
                "new_order"
            ],
            tags=["fantasy", "epic", "dragons", "politics"],
            difficulty="medium",
            estimated_playtime_minutes=150
        )
        
        return quest

