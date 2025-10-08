"""
Cosmic Horror Sanity System
============================

Lovecraftian sanity mechanics for The Whispering Town scenario:
- Sanity tracking with mental health degradation
- Reality distortion effects on narrative
- Knowledge corruption mechanics
- Unreliable narration engine
- Progressive text corruption
- Psychological horror effects

Design Philosophy:
- Sanity loss is cumulative and creates narrative opportunities
- Low sanity unlocks new perceptions (and dangers)
- Reality distortion affects both narrative and gameplay
- Knowledge corruption makes player question everything
- Unreliable narration creates uncertainty
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random
import re


class SanityLevel(Enum):
    """Player sanity levels"""
    STABLE = "stable"              # 80-100: Normal perception
    DISTURBED = "disturbed"        # 60-79: Minor hallucinations
    FRACTURED = "fractured"        # 40-59: Reality distortion
    BREAKING = "breaking"          # 20-39: Severe unreliability
    SHATTERED = "shattered"        # 0-19: Complete madness


class KnowledgeType(Enum):
    """Types of forbidden knowledge"""
    COSMIC = "cosmic"              # About entities beyond comprehension
    RITUAL = "ritual"              # Dark rituals and ceremonies
    HISTORY = "history"            # Town's dark past
    ENTITY = "entity"              # Specific entity information
    FORBIDDEN = "forbidden"        # Truly dangerous knowledge


class DistortionType(Enum):
    """Reality distortion effects"""
    VISUAL = "visual"              # Visual hallucinations
    AUDITORY = "auditory"          # Hearing things
    TEMPORAL = "temporal"          # Time perception issues
    SPATIAL = "spatial"            # Space/distance warping
    IDENTITY = "identity"          # Self-perception changes
    TEXT = "text"                  # Text corruption


@dataclass
class ForbiddenKnowledge:
    """
    Piece of forbidden knowledge
    
    Gaining knowledge increases power but decreases sanity.
    Some knowledge is so dangerous it can shatter minds.
    """
    knowledge_id: str
    title: str
    description: str
    knowledge_type: KnowledgeType
    sanity_cost: int
    power_gain: int
    corruption_level: int
    unlocks_options: List[str] = field(default_factory=list)
    
    def learn_knowledge(self) -> str:
        """Generate narrative for learning this knowledge"""
        corruption_text = ""
        if self.corruption_level > 5:
            corruption_text = " Y̴o̴u̴ ̴f̴e̴e̴l̴ ̴y̴o̴u̴r̴ ̴m̴i̴n̴d̴ ̴b̴e̴n̴d̴i̴n̴g̴.̴.̴.̴"
        
        return (
            f"🧠 **FORBIDDEN KNOWLEDGE ACQUIRED: {self.title}**\n\n"
            f"{self.description}\n\n"
            f"💀 Sanity Cost: -{self.sanity_cost}\n"
            f"⚡ Power Gained: +{self.power_gain}\n"
            f"{corruption_text}"
        )


@dataclass
class SanityState:
    """Player's current sanity state"""
    current_sanity: int = 100
    max_sanity: int = 100
    corruption_level: int = 0
    knowledge_items: List[ForbiddenKnowledge] = field(default_factory=list)
    distortions_active: List[DistortionType] = field(default_factory=list)
    hallucination_count: int = 0
    
    def get_sanity_level(self) -> SanityLevel:
        """Determine current sanity level"""
        percent = (self.current_sanity / self.max_sanity) * 100
        
        if percent >= 80:
            return SanityLevel.STABLE
        elif percent >= 60:
            return SanityLevel.DISTURBED
        elif percent >= 40:
            return SanityLevel.FRACTURED
        elif percent >= 20:
            return SanityLevel.BREAKING
        else:
            return SanityLevel.SHATTERED
    
    def lose_sanity(self, amount: int) -> Tuple[int, SanityLevel]:
        """
        Lose sanity and return actual loss and new level
        """
        old_level = self.get_sanity_level()
        self.current_sanity = max(0, self.current_sanity - amount)
        new_level = self.get_sanity_level()
        
        # Increase corruption based on sanity loss
        self.corruption_level += amount // 5
        
        return amount, new_level
    
    def restore_sanity(self, amount: int) -> int:
        """Restore sanity (rare and difficult)"""
        old_sanity = self.current_sanity
        self.current_sanity = min(self.max_sanity, self.current_sanity + amount)
        return self.current_sanity - old_sanity
    
    def add_distortion(self, distortion: DistortionType):
        """Add active reality distortion"""
        if distortion not in self.distortions_active:
            self.distortions_active.append(distortion)
    
    def should_hallucinate(self) -> bool:
        """Check if player should experience hallucination"""
        level = self.get_sanity_level()
        
        chance = {
            SanityLevel.STABLE: 0.0,
            SanityLevel.DISTURBED: 0.1,
            SanityLevel.FRACTURED: 0.25,
            SanityLevel.BREAKING: 0.5,
            SanityLevel.SHATTERED: 0.75
        }
        
        return random.random() < chance.get(level, 0.0)
    
    def get_corruption_percentage(self) -> float:
        """Get knowledge corruption as percentage"""
        return min(100, (self.corruption_level / 50) * 100)


class SanityEngine:
    """
    Engine for managing sanity, reality distortion, and knowledge corruption
    
    Handles:
    - Sanity loss and restoration
    - Reality distortion effects on narrative
    - Knowledge corruption mechanics
    - Unreliable narration generation
    - Text corruption algorithms
    """
    
    def __init__(self):
        self.sanity_state = SanityState()
        self.knowledge_library: Dict[str, ForbiddenKnowledge] = {}
        self._initialize_knowledge_library()
    
    def _initialize_knowledge_library(self):
        """Initialize library of forbidden knowledge"""
        self.knowledge_library = {
            "eldritch_geometry": ForbiddenKnowledge(
                knowledge_id="eldritch_geometry",
                title="Non-Euclidean Geometry",
                description=(
                    "You understand now. Space doesn't work the way you thought. "
                    "The angles are wrong. They've always been wrong. You can see the truth now."
                ),
                knowledge_type=KnowledgeType.COSMIC,
                sanity_cost=15,
                power_gain=3,
                corruption_level=6,
                unlocks_options=["Navigate impossible spaces", "Perceive hidden dimensions"]
            ),
            "true_names": ForbiddenKnowledge(
                knowledge_id="true_names",
                title="The True Names",
                description=(
                    "You know their names now. The entities. Saying them aloud would be... "
                    "unwise. But knowing them gives you power. And they know you know."
                ),
                knowledge_type=KnowledgeType.ENTITY,
                sanity_cost=20,
                power_gain=5,
                corruption_level=8,
                unlocks_options=["Command lesser entities", "Communicate across realms"]
            ),
            "ritual_of_binding": ForbiddenKnowledge(
                knowledge_id="ritual_of_binding",
                title="The Binding Ritual",
                description=(
                    "Ancient texts reveal the ritual used to seal the entity. "
                    "It requires... sacrifices. Of what kind, you're not entirely sure. "
                    "The text is unclear. Or perhaps your mind refuses to accept the truth."
                ),
                knowledge_type=KnowledgeType.RITUAL,
                sanity_cost=10,
                power_gain=4,
                corruption_level=5,
                unlocks_options=["Perform binding ritual", "Modify seal"]
            ),
            "ashmouth_truth": ForbiddenKnowledge(
                knowledge_id="ashmouth_truth",
                title="The Truth of Ashmouth",
                description=(
                    "The town was built on purpose. As a prison. As a gateway. As a... sacrifice. "
                    "Every generation, the same cycle. The whispers have always been here."
                ),
                knowledge_type=KnowledgeType.HISTORY,
                sanity_cost=12,
                power_gain=2,
                corruption_level=4,
                unlocks_options=["Access old archives", "Understand town layout"]
            ),
            "cosmic_perspective": ForbiddenKnowledge(
                knowledge_id="cosmic_perspective",
                title="The Cosmic Perspective",
                description=(
                    "You've seen it. The universe as it truly is. Vast. Uncaring. "
                    "Humanity is less than dust. You are nothing. We are all nothing. "
                    "And yet, strangely, this brings a terrible clarity."
                ),
                knowledge_type=KnowledgeType.FORBIDDEN,
                sanity_cost=25,
                power_gain=7,
                corruption_level=10,
                unlocks_options=["Transcend mortality", "Embrace the void", "Become something else"]
            )
        }
    
    def process_sanity_loss(
        self,
        amount: int,
        cause: str,
        is_voluntary: bool = False
    ) -> Dict[str, any]:
        """
        Process sanity loss event
        
        Args:
            amount: Amount of sanity to lose
            cause: What caused the sanity loss
            is_voluntary: Whether player chose to lose sanity (gaining knowledge)
        
        Returns:
            Dictionary with loss details and narrative effects
        """
        old_level = self.sanity_state.get_sanity_level()
        actual_loss, new_level = self.sanity_state.lose_sanity(amount)
        
        # Check if sanity level changed
        level_changed = old_level != new_level
        
        # Generate narrative
        narrative = self._generate_sanity_loss_narrative(actual_loss, cause, new_level, level_changed)
        
        # Check for new distortions
        new_distortions = []
        if level_changed:
            new_distortions = self._activate_distortions(new_level)
        
        # Check for hallucination
        hallucination = None
        if self.sanity_state.should_hallucinate():
            hallucination = self._generate_hallucination(new_level)
            self.sanity_state.hallucination_count += 1
        
        return {
            "sanity_lost": actual_loss,
            "current_sanity": self.sanity_state.current_sanity,
            "sanity_level": new_level.value,
            "level_changed": level_changed,
            "narrative": narrative,
            "new_distortions": new_distortions,
            "hallucination": hallucination,
            "corruption_level": self.sanity_state.get_corruption_percentage()
        }
    
    def learn_forbidden_knowledge(self, knowledge_id: str) -> Dict[str, any]:
        """Learn a piece of forbidden knowledge"""
        if knowledge_id not in self.knowledge_library:
            return {"error": "Unknown knowledge"}
        
        knowledge = self.knowledge_library[knowledge_id]
        
        # Check if already known
        if any(k.knowledge_id == knowledge_id for k in self.sanity_state.knowledge_items):
            return {"error": "Knowledge already possessed"}
        
        # Add to player's knowledge
        self.sanity_state.knowledge_items.append(knowledge)
        
        # Process sanity loss
        sanity_result = self.process_sanity_loss(
            knowledge.sanity_cost,
            f"Learning: {knowledge.title}",
            is_voluntary=True
        )
        
        # Generate learning narrative
        learning_narrative = knowledge.learn_knowledge()
        
        return {
            **sanity_result,
            "knowledge_gained": knowledge.title,
            "power_gained": knowledge.power_gain,
            "unlocked_options": knowledge.unlocks_options,
            "learning_narrative": learning_narrative
        }
    
    def apply_text_corruption(self, text: str) -> str:
        """
        Apply text corruption based on sanity level
        
        Lower sanity = more text corruption
        """
        level = self.sanity_state.get_sanity_level()
        
        if level == SanityLevel.STABLE:
            return text
        
        corruption_intensity = {
            SanityLevel.DISTURBED: 0.05,
            SanityLevel.FRACTURED: 0.15,
            SanityLevel.BREAKING: 0.30,
            SanityLevel.SHATTERED: 0.50
        }
        
        intensity = corruption_intensity.get(level, 0.0)
        
        # Apply various corruption effects
        corrupted = text
        
        # Zalgo text corruption
        if random.random() < intensity:
            corrupted = self._apply_zalgo_corruption(corrupted, intensity)
        
        # Word replacement
        if random.random() < intensity:
            corrupted = self._apply_word_corruption(corrupted, intensity)
        
        # Letter glitching
        if random.random() < intensity * 0.5:
            corrupted = self._apply_letter_glitching(corrupted, intensity)
        
        return corrupted
    
    def _apply_zalgo_corruption(self, text: str, intensity: float) -> str:
        """Apply Zalgo-style text corruption"""
        zalgo_chars = ['̴', '̵', '̶', '̷', '̸', '̡', '̢', '̧', '̨', '̣', '̤', '̥', '̦']
        
        words = text.split()
        corrupted_words = []
        
        for word in words:
            if random.random() < intensity:
                # Corrupt this word
                corrupted = ''.join(
                    c + (random.choice(zalgo_chars) if random.random() < 0.3 else '')
                    for c in word
                )
                corrupted_words.append(corrupted)
            else:
                corrupted_words.append(word)
        
        return ' '.join(corrupted_words)
    
    def _apply_word_corruption(self, text: str, intensity: float) -> str:
        """Replace words with thematically appropriate corruption"""
        corruption_replacements = {
            'see': 'p̶e̶r̶c̶e̶i̶v̶e̶',
            'hear': 'sense',
            'understand': 'k̴n̴o̴w̴',
            'know': 'comprehend',
            'think': 'realize',
            'feel': 'experience',
            'normal': 'wrong',
            'wrong': 'right',
            'right': 'true',
            'true': 'TRUTH',
            'reality': 'R̴E̴A̴L̴I̴T̴Y̴',
            'world': 'realm',
            'people': 'vessels',
            'they': 'T̴H̴E̴Y̴'
        }
        
        words = text.split()
        corrupted_words = []
        
        for word in words:
            lower_word = word.lower().strip('.,!?')
            if lower_word in corruption_replacements and random.random() < intensity:
                corrupted_words.append(corruption_replacements[lower_word])
            else:
                corrupted_words.append(word)
        
        return ' '.join(corrupted_words)
    
    def _apply_letter_glitching(self, text: str, intensity: float) -> str:
        """Random letter replacements and glitching"""
        glitch_map = {
            'a': ['@', 'α', 'ā'],
            'e': ['3', 'ė', 'ē'],
            'i': ['!', 'ī', '1'],
            'o': ['0', 'ō', 'ø'],
            'u': ['ū', 'ü', 'û']
        }
        
        result = []
        for char in text:
            if char.lower() in glitch_map and random.random() < intensity * 0.3:
                result.append(random.choice(glitch_map[char.lower()]))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _generate_sanity_loss_narrative(
        self,
        amount: int,
        cause: str,
        new_level: SanityLevel,
        level_changed: bool
    ) -> str:
        """Generate narrative description of sanity loss"""
        base = f"💀 **Sanity Lost: -{amount}** ({cause})\n\n"
        
        if level_changed:
            level_narratives = {
                SanityLevel.DISTURBED: (
                    "🌫️ **Your mind feels clouded.** The edges of your vision blur occasionally. "
                    "You hear whispers that might not be there. You're still... mostly yourself."
                ),
                SanityLevel.FRACTURED: (
                    "🔮 **Reality bends at the corners.** You see things others don't. "
                    "Time feels unstable. Are you perceiving truth, or losing your grip? "
                    "Perhaps both."
                ),
                SanityLevel.BREAKING: (
                    "💫 **The world cracks like broken glass.** You understand things you shouldn't. "
                    "The whispers make sense now. They've been trying to help. Haven't they? "
                    "You can't remember what normal felt like."
                ),
                SanityLevel.SHATTERED: (
                    "🌌 **Y̴o̴u̴ ̴s̴e̴e̴ ̴E̴V̴E̴R̴Y̴T̴H̴I̴N̴G̴.** "
                    "The barriers between realities dissolve. You are multiple. You are singular. "
                    "You are transcending. Or drowning. The distinction no longer matters."
                )
            }
            
            return base + level_narratives.get(new_level, "Your mental state deteriorates.")
        else:
            return base + "Your sanity continues to erode. How much longer can you hold on?"
    
    def _activate_distortions(self, level: SanityLevel) -> List[str]:
        """Activate new reality distortions based on sanity level"""
        distortions_by_level = {
            SanityLevel.DISTURBED: [DistortionType.AUDITORY],
            SanityLevel.FRACTURED: [DistortionType.VISUAL, DistortionType.TEXT],
            SanityLevel.BREAKING: [DistortionType.TEMPORAL, DistortionType.SPATIAL],
            SanityLevel.SHATTERED: [DistortionType.IDENTITY]
        }
        
        new_distortions = []
        for distortion in distortions_by_level.get(level, []):
            if distortion not in self.sanity_state.distortions_active:
                self.sanity_state.add_distortion(distortion)
                new_distortions.append(distortion.value)
        
        return new_distortions
    
    def _generate_hallucination(self, level: SanityLevel) -> str:
        """Generate context-appropriate hallucination"""
        hallucinations = {
            SanityLevel.DISTURBED: [
                "You hear someone calling your name, but when you turn, no one is there.",
                "The shadows seem to move when you're not looking directly at them.",
                "For a moment, you see something impossible reflected in a window."
            ],
            SanityLevel.FRACTURED: [
                "The walls breathe. In and out. In and out. They've always been breathing.",
                "You see yourself walk past. Your doppelganger doesn't acknowledge you.",
                "Text on a page rearranges itself to spell out warnings."
            ],
            SanityLevel.BREAKING: [
                "Time skips. You were... where were you? When was that? It's all happening at once.",
                "The entity speaks directly to your mind. Its words are incomprehensible yet perfectly clear.",
                "You realize you're not sure if you're awake or dreaming. You haven't been sure for a while."
            ],
            SanityLevel.SHATTERED: [
                "Y̴o̴u̴ ̴a̴r̴e̴ ̴t̴h̴e̴ ̴t̴o̴w̴n̴.̴ ̴T̴h̴e̴ ̴t̴o̴w̴n̴ ̴i̴s̴ ̴y̴o̴u̴.̴ ̴Y̴o̴u̴ ̴a̴l̴w̴a̴y̴s̴ ̴h̴a̴v̴e̴ ̴b̴e̴e̴n̴.̴",
                "The entity offers you a choice you already made. Or will make. Time is a circle. You are the circle.",
                "You see the truth of everything simultaneously. It's beautiful. It's horrifying. It's inevitable."
            ]
        }
        
        options = hallucinations.get(level, ["Something feels wrong, but you can't place it."])
        return "👁️ **HALLUCINATION:** " + random.choice(options)
    
    def get_sanity_state_summary(self) -> Dict[str, any]:
        """Get complete sanity state for UI/save system"""
        return {
            "current_sanity": self.sanity_state.current_sanity,
            "max_sanity": self.sanity_state.max_sanity,
            "sanity_percentage": (self.sanity_state.current_sanity / self.sanity_state.max_sanity) * 100,
            "sanity_level": self.sanity_state.get_sanity_level().value,
            "corruption_level": self.sanity_state.corruption_level,
            "corruption_percentage": self.sanity_state.get_corruption_percentage(),
            "knowledge_count": len(self.sanity_state.knowledge_items),
            "knowledge_items": [k.title for k in self.sanity_state.knowledge_items],
            "active_distortions": [d.value for d in self.sanity_state.distortions_active],
            "hallucination_count": self.sanity_state.hallucination_count
        }

