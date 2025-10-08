"""
Magic System for The Northern Realms
=====================================

Complete magic system featuring:
- 6 magical schools (Destruction, Restoration, Alteration, Conjuration, Illusion, Enchantment)
- Mana management and spell casting
- Magical progression and learning
- Spell effects in combat and narrative
- Magical artifacts and enchanted items

Design Philosophy:
- Magic should be powerful but costly
- Spell casting adds tactical depth to combat
- Magic progression allows specialization
- Mana management prevents spam-casting
- Magical schools provide distinct playstyles
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random


class MagicSchool(Enum):
    """Six schools of magic"""
    DESTRUCTION = "destruction"      # Fire, ice, lightning damage
    RESTORATION = "restoration"      # Healing, protection, buffs
    ALTERATION = "alteration"        # Physical manipulation, utility
    CONJURATION = "conjuration"      # Summoning, teleportation
    ILLUSION = "illusion"           # Mind control, deception, fear
    ENCHANTMENT = "enchantment"     # Item enhancement, permanent effects


class SpellLevel(Enum):
    """Spell power levels"""
    NOVICE = "novice"        # Level 1-3 spells
    APPRENTICE = "apprentice" # Level 4-6 spells
    ADEPT = "adept"          # Level 7-9 spells
    EXPERT = "expert"        # Level 10-12 spells
    MASTER = "master"        # Level 13+ spells


class SpellTarget(Enum):
    """Spell target types"""
    SELF = "self"           # Target caster
    SINGLE = "single"       # Single target
    AREA = "area"          # Multiple targets
    ENVIRONMENT = "environment" # Affect surroundings


class SpellEffectType(Enum):
    """Types of magical effects"""
    DAMAGE = "damage"
    HEALING = "healing"
    BUFF = "buff"
    DEBUFF = "debuff"
    SUMMON = "summon"
    TELEPORT = "teleport"
    ILLUSION = "illusion"
    ENCHANTMENT = "enchantment"
    UTILITY = "utility"


@dataclass
class Spell:
    """
    Individual spell definition
    
    Contains all information needed for spell casting:
    - Mana cost and requirements
    - Effects and damage/healing
    - Targeting and duration
    - School and level
    """
    spell_id: str
    name: str
    description: str
    school: MagicSchool
    level: SpellLevel
    
    # Casting requirements
    mana_cost: int
    casting_time: int  # Turns to cast
    components: List[str] = field(default_factory=list)  # Verbal, somatic, material
    
    # Spell properties
    target_type: SpellTarget
    effect_type: SpellEffectType
    damage: int = 0
    healing: int = 0
    duration: int = 0  # Turns effect lasts
    range: int = 30  # Feet
    
    # Special effects
    requires_line_of_sight: bool = True
    can_be_resisted: bool = False
    save_dc: int = 10  # Difficulty for saving throws
    
    # Meta information
    is_ritual: bool = False  # Can be cast as ritual (no mana cost, longer time)
    is_concentration: bool = False  # Requires concentration to maintain
    
    def can_cast(self, caster_mana: int, caster_level: int) -> bool:
        """Check if spell can be cast"""
        if caster_mana < self.mana_cost:
            return False
        
        # Check spell level requirements
        level_requirements = {
            SpellLevel.NOVICE: 1,
            SpellLevel.APPRENTICE: 3,
            SpellLevel.ADEPT: 5,
            SpellLevel.EXPERT: 7,
            SpellLevel.MASTER: 9
        }
        
        return caster_level >= level_requirements.get(self.level, 0)
    
    def get_casting_narrative(self) -> str:
        """Generate narrative for spell casting"""
        components_text = ""
        if self.components:
            components_text = f" ({'/'.join(self.components)})"
        
        return f"You weave magical energy, casting {self.name}{components_text}!"


@dataclass
class MageStats:
    """Player's magical abilities"""
    level: int = 1
    mana: int = 10
    max_mana: int = 10
    
    # School affinities (0-20, higher = more skilled)
    destruction_affinity: int = 0
    restoration_affinity: int = 0
    alteration_affinity: int = 0
    conjuration_affinity: int = 0
    illusion_affinity: int = 0
    enchantment_affinity: int = 0
    
    # Known spells
    known_spells: List[str] = field(default_factory=list)
    
    # Concentration spell (only one at a time)
    concentration_spell: Optional[str] = None
    
    # Magical items
    equipped_artifacts: List[str] = field(default_factory=list)
    
    def get_total_affinity(self) -> int:
        """Get total magical power"""
        return (
            self.destruction_affinity + self.restoration_affinity +
            self.alteration_affinity + self.conjuration_affinity +
            self.illusion_affinity + self.enchantment_affinity
        )
    
    def get_primary_school(self) -> Optional[MagicSchool]:
        """Get the school with highest affinity"""
        affinities = {
            MagicSchool.DESTRUCTION: self.destruction_affinity,
            MagicSchool.RESTORATION: self.restoration_affinity,
            MagicSchool.ALTERATION: self.alteration_affinity,
            MagicSchool.CONJURATION: self.conjuration_affinity,
            MagicSchool.ILLUSION: self.illusion_affinity,
            MagicSchool.ENCHANTMENT: self.enchantment_affinity
        }
        
        max_affinity = max(affinities.values())
        if max_affinity == 0:
            return None
        
        return max(affinities, key=affinities.get)
    
    def use_mana(self, amount: int) -> bool:
        """Use mana, return True if successful"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount: int):
        """Restore mana"""
        self.mana = min(self.mana + amount, self.max_mana)
    
    def learn_spell(self, spell_id: str):
        """Learn a new spell"""
        if spell_id not in self.known_spells:
            self.known_spells.append(spell_id)
    
    def can_cast_spell(self, spell: Spell) -> bool:
        """Check if player can cast this spell"""
        return (
            spell.spell_id in self.known_spells and
            spell.can_cast(self.mana, self.level)
        )


@dataclass
class SpellCastResult:
    """Result of spell casting"""
    success: bool
    narrative: str
    effects: Dict[str, any] = field(default_factory=dict)
    mana_used: int = 0
    side_effects: List[str] = field(default_factory=list)
    
    def add_effect(self, effect_type: str, value: any, target: str = ""):
        """Add spell effect"""
        if effect_type not in self.effects:
            self.effects[effect_type] = []
        self.effects[effect_type].append({"value": value, "target": target})


class MagicEngine:
    """
    Magic system engine for The Northern Realms
    
    Handles:
    - Spell casting and mana management
    - Magical progression and learning
    - Spell effects in combat and narrative
    - Magical artifacts and enchantments
    """
    
    def __init__(self):
        self.spell_library: Dict[str, Spell] = {}
        self._initialize_spell_library()
    
    def _initialize_spell_library(self):
        """Initialize complete spell library"""
        
        # ========================================================================
        # DESTRUCTION SPELLS (Fire, Ice, Lightning)
        # ========================================================================
        
        self.spell_library.update({
            "firebolt": Spell(
                spell_id="firebolt",
                name="Fire Bolt",
                description="Hurl a mote of flame at a foe.",
                school=MagicSchool.DESTRUCTION,
                level=SpellLevel.NOVICE,
                mana_cost=2,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.DAMAGE,
                damage=8,
                range=120
            ),
            
            "ice_spike": Spell(
                spell_id="ice_spike",
                name="Ice Spike",
                description="Create a shard of ice that impales your target.",
                school=MagicSchool.DESTRUCTION,
                level=SpellLevel.NOVICE,
                mana_cost=3,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.DAMAGE,
                damage=10,
                range=60
            ),
            
            "lightning_bolt": Spell(
                spell_id="lightning_bolt",
                name="Lightning Bolt",
                description="A stroke of lightning dealing massive damage.",
                school=MagicSchool.DESTRUCTION,
                level=SpellLevel.ADEPT,
                mana_cost=8,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.DAMAGE,
                damage=25,
                range=100,
                requires_line_of_sight=True
            ),
            
            "fireball": Spell(
                spell_id="fireball",
                name="Fireball",
                description="An explosion of flame that damages multiple enemies.",
                school=MagicSchool.DESTRUCTION,
                level=SpellLevel.ADEPT,
                mana_cost=12,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.AREA,
                effect_type=SpellEffectType.DAMAGE,
                damage=15,
                range=150
            ),
            
            # ========================================================================
            # RESTORATION SPELLS (Healing, Protection)
            # ========================================================================
            
            "cure_wounds": Spell(
                spell_id="cure_wounds",
                name="Cure Wounds",
                description="A creature you touch regains hit points.",
                school=MagicSchool.RESTORATION,
                level=SpellLevel.NOVICE,
                mana_cost=3,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.HEALING,
                healing=8,
                range=0  # Touch
            ),
            
            "healing_word": Spell(
                spell_id="healing_word",
                name="Healing Word",
                description="A word of healing that restores hit points.",
                school=MagicSchool.RESTORATION,
                level=SpellLevel.NOVICE,
                mana_cost=2,
                casting_time=0,  # Bonus action
                components=["verbal"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.HEALING,
                healing=6,
                range=60
            ),
            
            "bless": Spell(
                spell_id="bless",
                name="Bless",
                description="You bless up to three creatures, improving their attacks and saves.",
                school=MagicSchool.RESTORATION,
                level=SpellLevel.NOVICE,
                mana_cost=4,
                casting_time=1,
                components=["verbal", "somatic", "material"],
                target_type=SpellTarget.AREA,
                effect_type=SpellEffectType.BUFF,
                duration=10,  # 1 minute
                range=30
            ),
            
            # ========================================================================
            # ALTERATION SPELLS (Physical Manipulation)
            # ========================================================================
            
            "mage_hand": Spell(
                spell_id="mage_hand",
                name="Mage Hand",
                description="A spectral hand appears to manipulate objects.",
                school=MagicSchool.ALTERATION,
                level=SpellLevel.NOVICE,
                mana_cost=1,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.ENVIRONMENT,
                effect_type=SpellEffectType.UTILITY,
                duration=10,
                range=30
            ),
            
            "levitate": Spell(
                spell_id="levitate",
                name="Levitate",
                description="A creature or object rises vertically into the air.",
                school=MagicSchool.ALTERATION,
                level=SpellLevel.ADEPT,
                mana_cost=6,
                casting_time=1,
                components=["verbal", "somatic", "material"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.UTILITY,
                duration=10,
                range=60,
                can_be_resisted=True,
                save_dc=15
            ),
            
            # ========================================================================
            # CONJURATION SPELLS (Summoning)
            # ========================================================================
            
            "summon_familiar": Spell(
                spell_id="summon_familiar",
                name="Find Familiar",
                description="You gain the service of a spirit that takes an animal form.",
                school=MagicSchool.CONJURATION,
                level=SpellLevel.NOVICE,
                mana_cost=10,
                casting_time=60,  # 1 hour ritual
                components=["verbal", "somatic", "material"],
                target_type=SpellTarget.ENVIRONMENT,
                effect_type=SpellEffectType.SUMMON,
                duration=0,  # Permanent until dismissed
                range=10,
                is_ritual=True
            ),
            
            # ========================================================================
            # ILLUSION SPELLS (Mind Control)
            # ========================================================================
            
            "minor_illusion": Spell(
                spell_id="minor_illusion",
                name="Minor Illusion",
                description="You create a sound or image of an object.",
                school=MagicSchool.ILLUSION,
                level=SpellLevel.NOVICE,
                mana_cost=1,
                casting_time=1,
                components=["somatic"],
                target_type=SpellTarget.ENVIRONMENT,
                effect_type=SpellEffectType.ILLUSION,
                duration=10,
                range=30
            ),
            
            "invisibility": Spell(
                spell_id="invisibility",
                name="Invisibility",
                description="A creature you touch becomes invisible.",
                school=MagicSchool.ILLUSION,
                level=SpellLevel.ADEPT,
                mana_cost=8,
                casting_time=1,
                components=["verbal", "somatic", "material"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.ILLUSION,
                duration=10,
                range=0,  # Touch
                is_concentration=True
            ),
            
            # ========================================================================
            # ENCHANTMENT SPELLS (Item Enhancement)
            # ========================================================================
            
            "magic_weapon": Spell(
                spell_id="magic_weapon",
                name="Magic Weapon",
                description="Make a weapon magical for enhanced combat effectiveness.",
                school=MagicSchool.ENCHANTMENT,
                level=SpellLevel.ADEPT,
                mana_cost=6,
                casting_time=1,
                components=["verbal", "somatic"],
                target_type=SpellTarget.SINGLE,
                effect_type=SpellEffectType.ENCHANTMENT,
                duration=10,
                range=0  # Touch
            )
        })
    
    def cast_spell(
        self,
        mage_stats: MageStats,
        spell_id: str,
        target: Optional[str] = None,
        combat_context: Optional[Dict] = None
    ) -> SpellCastResult:
        """
        Cast a spell with full mechanics
        
        Args:
            mage_stats: Player's magical abilities
            spell_id: Spell to cast
            target: Target of spell (if applicable)
            combat_context: Combat state for combat spells
            
        Returns:
            SpellCastResult with success, narrative, and effects
        """
        if spell_id not in self.spell_library:
            return SpellCastResult(
                success=False,
                narrative=f"Unknown spell: {spell_id}",
                mana_used=0
            )
        
        spell = self.spell_library[spell_id]
        
        # Check if player can cast this spell
        if not mage_stats.can_cast_spell(spell):
            return SpellCastResult(
                success=False,
                narrative=f"You cannot cast {spell.name}. You may need to learn it first or lack sufficient mana.",
                mana_used=0
            )
        
        # Use mana
        if not mage_stats.use_mana(spell.mana_cost):
            return SpellCastResult(
                success=False,
                narrative=f"Insufficient mana to cast {spell.name}.",
                mana_used=0
            )
        
        # Generate casting narrative
        narrative = spell.get_casting_narrative()
        
        # Apply spell effects
        effects = {}
        side_effects = []
        
        if spell.effect_type == SpellEffectType.DAMAGE:
            damage = spell.damage + (mage_stats.destruction_affinity // 2)
            effects["damage"] = [{"value": damage, "target": target or "enemy"}]
            narrative += f" It strikes for {damage} damage!"
            
        elif spell.effect_type == SpellEffectType.HEALING:
            healing = spell.healing + (mage_stats.restoration_affinity // 2)
            effects["healing"] = [{"value": healing, "target": target or "self"}]
            narrative += f" It heals {healing} hit points!"
            
        elif spell.effect_type == SpellEffectType.BUFF:
            effects["buff"] = [{"value": "bless", "target": target or "allies", "duration": spell.duration}]
            narrative += f" The blessing enhances combat effectiveness for {spell.duration} turns!"
            
        elif spell.effect_type == SpellEffectType.ILLUSION:
            effects["illusion"] = [{"value": spell.name, "target": target or "area", "duration": spell.duration}]
            narrative += f" The illusion takes hold for {spell.duration} turns!"
            
        # Check for magical mishaps (low chance for high-level spells)
        if spell.level in [SpellLevel.EXPERT, SpellLevel.MASTER] and random.random() < 0.1:
            side_effects.append("Magical backlash - you take minor damage")
            effects["self_damage"] = [{"value": spell.mana_cost // 2, "target": "self"}]
        
        return SpellCastResult(
            success=True,
            narrative=narrative,
            effects=effects,
            mana_used=spell.mana_cost,
            side_effects=side_effects
        )
    
    def get_spells_by_school(self, school: MagicSchool) -> List[Spell]:
        """Get all spells of a specific school"""
        return [
            spell for spell in self.spell_library.values()
            if spell.school == school
        ]
    
    def get_learnable_spells(self, mage_stats: MageStats) -> List[Spell]:
        """Get spells player can learn (level appropriate)"""
        return [
            spell for spell in self.spell_library.values()
            if spell.spell_id not in mage_stats.known_spells and
            mage_stats.level >= self._get_level_requirement(spell.level)
        ]
    
    def _get_level_requirement(self, spell_level: SpellLevel) -> int:
        """Get character level requirement for spell level"""
        return {
            SpellLevel.NOVICE: 1,
            SpellLevel.APPRENTICE: 3,
            SpellLevel.ADEPT: 5,
            SpellLevel.EXPERT: 7,
            SpellLevel.MASTER: 9
        }.get(spell_level, 1)
    
    def calculate_mana_regen(self, mage_stats: MageStats) -> int:
        """Calculate mana regeneration per turn"""
        base_regen = mage_stats.level // 3  # Level-based regen
        affinity_bonus = mage_stats.get_total_affinity() // 20  # Affinity bonus
        return max(1, base_regen + affinity_bonus)
    
    def process_mana_regeneration(self, mage_stats: MageStats):
        """Regenerate mana each turn"""
        regen_amount = self.calculate_mana_regen(mage_stats)
        mage_stats.restore_mana(regen_amount)


# ============================================================================
# MAGICAL ARTIFACTS
# ============================================================================

@dataclass
class MagicalArtifact:
    """Magical items that enhance spellcasting"""
    artifact_id: str
    name: str
    description: str
    
    # Enhancement effects
    mana_bonus: int = 0
    spell_power_bonus: int = 0
    school_affinity_bonus: Dict[MagicSchool, int] = field(default_factory=dict)
    
    # Special abilities
    spells_granted: List[str] = field(default_factory=list)
    passive_effects: List[str] = field(default_factory=list)
    
    # Rarity and value
    rarity: str = "common"
    gold_value: int = 0


class ArtifactLibrary:
    """Library of magical artifacts"""
    
    @staticmethod
    def get_artifacts() -> Dict[str, MagicalArtifact]:
        """Get all magical artifacts"""
        return {
            "staff_of_fire": MagicalArtifact(
                artifact_id="staff_of_fire",
                name="Staff of Fire",
                description="A gnarled staff topped with an eternal flame crystal.",
                mana_bonus=5,
                spell_power_bonus=3,
                school_affinity_bonus={MagicSchool.DESTRUCTION: 5},
                spells_granted=["firebolt", "fireball"],
                passive_effects=["Fire resistance"],
                rarity="uncommon",
                gold_value=500
            ),
            
            "robe_of_the_archmage": MagicalArtifact(
                artifact_id="robe_of_the_archmage",
                name="Robe of the Archmage",
                description="Flowing robes embroidered with arcane symbols.",
                mana_bonus=10,
                spell_power_bonus=5,
                passive_effects=["Mana regeneration +2", "Spell resistance"],
                rarity="rare",
                gold_value=2000
            ),
            
            "amulet_of_healing": MagicalArtifact(
                artifact_id="amulet_of_healing",
                name="Amulet of Healing",
                description="A golden amulet bearing the symbol of a healing hand.",
                school_affinity_bonus={MagicSchool.RESTORATION: 8},
                spells_granted=["cure_wounds", "healing_word"],
                passive_effects=["Healing spells +50% effective"],
                rarity="uncommon",
                gold_value=800
            )
        }


# ============================================================================
# MAGIC PROGRESSION
# ============================================================================

class MagicProgression:
    """Handles magical learning and advancement"""
    
    @staticmethod
    def calculate_spell_learning_cost(mage_level: int, spell_level: SpellLevel) -> int:
        """Calculate gold cost to learn a spell"""
        base_cost = {
            SpellLevel.NOVICE: 50,
            SpellLevel.APPRENTICE: 200,
            SpellLevel.ADEPT: 500,
            SpellLevel.EXPERT: 1000,
            SpellLevel.MASTER: 2000
        }.get(spell_level, 50)
        
        level_multiplier = max(1, mage_level // 2)
        return base_cost * level_multiplier
    
    @staticmethod
    def can_learn_spell(mage_level: int, spell_level: SpellLevel) -> bool:
        """Check if player can learn spell of this level"""
        level_requirements = {
            SpellLevel.NOVICE: 1,
            SpellLevel.APPRENTICE: 3,
            SpellLevel.ADEPT: 5,
            SpellLevel.EXPERT: 7,
            SpellLevel.MASTER: 9
        }
        return mage_level >= level_requirements.get(spell_level, 1)
    
    @staticmethod
    def get_level_up_benefits(current_level: int) -> Dict[str, int]:
        """Get benefits from leveling up magic"""
        return {
            "max_mana": 2,
            "spell_power": 1,
            "school_affinity": 1
        }

