"""
AI-RPG-Alpha: Advanced Magic & Crafting System

Sophisticated magical system with spell research, component gathering,
enchanting, alchemy, and meaningful magical consequences.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime


class MagicSchool(Enum):
    """Schools of magical study"""
    ELEMENTAL = "elemental"
    DIVINE = "divine"
    ARCANE = "arcane"
    NATURE = "nature"
    SHADOW = "shadow"
    TEMPORAL = "temporal"
    MIND = "mind"
    TRANSMUTATION = "transmutation"


class SpellComponent(Enum):
    """Types of spell components"""
    VERBAL = "verbal"
    SOMATIC = "somatic"
    MATERIAL = "material"
    FOCUS = "focus"
    DIVINE_FAVOR = "divine_favor"
    EMOTIONAL = "emotional"


class CraftingSkill(Enum):
    """Crafting skill types"""
    ALCHEMY = "alchemy"
    ENCHANTING = "enchanting"
    ARTIFICE = "artifice"
    HERBALISM = "herbalism"
    SMITHING = "smithing"
    COOKING = "cooking"
    SCRIBING = "scribing"


@dataclass
class MagicalComponent:
    """A magical component used in spells and crafting"""
    id: str
    name: str
    component_type: str  # "herb", "mineral", "essence", "artifact"
    rarity: str  # "common", "uncommon", "rare", "legendary"
    magical_schools: List[MagicSchool] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    
    # Gathering information
    locations: List[str] = field(default_factory=list)
    gathering_difficulty: int = 10
    seasonal_availability: List[str] = field(default_factory=list)
    
    # Economic data
    base_value: int = 10
    market_availability: float = 1.0  # 0.0 to 2.0
    
    # Magical properties
    potency: float = 1.0
    stability: float = 1.0
    side_effects: List[str] = field(default_factory=list)


@dataclass
class Spell:
    """A magical spell with components and effects"""
    id: str
    name: str
    school: MagicSchool
    level: int  # 1-9
    
    # Components required
    components: Dict[SpellComponent, List[str]] = field(default_factory=dict)
    material_components: List[str] = field(default_factory=list)
    
    # Casting requirements
    casting_time: str = "1 action"
    range_: str = "touch"
    duration: str = "instantaneous"
    
    # Effects
    primary_effect: str = ""
    secondary_effects: List[str] = field(default_factory=list)
    
    # Learning and mastery
    research_difficulty: int = 15
    prerequisite_spells: List[str] = field(default_factory=list)
    research_components: List[str] = field(default_factory=list)
    
    # Risks and consequences
    failure_consequences: List[str] = field(default_factory=list)
    magical_contamination: float = 0.0
    reality_strain: float = 0.0


@dataclass
class CraftingRecipe:
    """A recipe for creating items through crafting"""
    id: str
    name: str
    skill_required: CraftingSkill
    skill_level: int
    
    # Materials needed
    components: Dict[str, int] = field(default_factory=dict)  # component_id -> quantity
    tools_required: List[str] = field(default_factory=list)
    
    # Process
    crafting_time: int = 60  # minutes
    difficulty: int = 15
    
    # Results
    output_item: str = ""
    output_quantity: int = 1
    possible_bonuses: List[str] = field(default_factory=list)
    
    # Magical enhancement
    enchantment_slots: int = 0
    magical_requirements: List[str] = field(default_factory=list)


@dataclass
class MagicalKnowledge:
    """Player's magical knowledge and research progress"""
    known_spells: List[str] = field(default_factory=list)
    researching_spells: Dict[str, float] = field(default_factory=dict)  # spell_id -> progress %
    spell_mastery: Dict[str, int] = field(default_factory=dict)  # spell_id -> mastery level
    
    # Schools of study
    school_affinities: Dict[MagicSchool, float] = field(default_factory=dict)
    forbidden_knowledge: List[str] = field(default_factory=list)
    
    # Research capabilities
    research_bonus: int = 0
    magical_contamination: float = 0.0
    reality_awareness: float = 0.0


@dataclass
class CraftingSkills:
    """Player's crafting skills and progress"""
    skill_levels: Dict[CraftingSkill, int] = field(default_factory=dict)
    known_recipes: List[str] = field(default_factory=list)
    crafting_bonuses: Dict[str, int] = field(default_factory=dict)
    
    # Equipment and workspace
    owned_tools: List[str] = field(default_factory=list)
    workshop_quality: int = 1  # 1-5
    
    # Masterwork tracking
    masterwork_items: List[str] = field(default_factory=list)
    crafting_reputation: Dict[str, int] = field(default_factory=dict)


class MagicCraftingEngine:
    """Advanced magic and crafting system"""
    
    def __init__(self):
        self.components = self._initialize_components()
        self.spells = self._initialize_spells()
        self.recipes = self._initialize_recipes()
        self.magical_events = self._initialize_magical_events()
    
    def _initialize_components(self) -> Dict[str, MagicalComponent]:
        """Initialize magical components database"""
        
        components = {}
        
        # Elemental components
        components["fire_crystal"] = MagicalComponent(
            id="fire_crystal",
            name="Fire Crystal",
            component_type="mineral",
            rarity="uncommon",
            magical_schools=[MagicSchool.ELEMENTAL],
            properties=["heat_generation", "energy_amplification"],
            locations=["volcanic_caves", "crystal_sanctum"],
            gathering_difficulty=12,
            base_value=50,
            potency=1.3,
            side_effects=["heat_damage", "fire_attraction"]
        )
        
        components["moonwater"] = MagicalComponent(
            id="moonwater",
            name="Moonwater",
            component_type="essence",
            rarity="rare",
            magical_schools=[MagicSchool.DIVINE, MagicSchool.ARCANE],
            properties=["purification", "divination_enhancement"],
            locations=["sacred_springs"],
            gathering_difficulty=15,
            seasonal_availability=["autumn", "winter"],
            base_value=100,
            potency=1.5,
            stability=0.8
        )
        
        components["shadow_herb"] = MagicalComponent(
            id="shadow_herb",
            name="Shadow Herb",
            component_type="herb",
            rarity="rare",
            magical_schools=[MagicSchool.SHADOW],
            properties=["concealment", "illusion_enhancement"],
            locations=["whispering_woods", "dark_caves"],
            gathering_difficulty=14,
            seasonal_availability=["autumn", "winter"],
            base_value=75,
            potency=1.2,
            side_effects=["temporary_blindness", "shadow_corruption"]
        )
        
        components["phoenix_feather"] = MagicalComponent(
            id="phoenix_feather",
            name="Phoenix Feather",
            component_type="artifact",
            rarity="legendary",
            magical_schools=[MagicSchool.ELEMENTAL, MagicSchool.DIVINE],
            properties=["resurrection", "healing_amplification", "fire_immunity"],
            locations=["phoenix_nest"],
            gathering_difficulty=20,
            base_value=1000,
            potency=2.0,
            stability=1.5
        )
        
        components["temporal_dust"] = MagicalComponent(
            id="temporal_dust",
            name="Temporal Dust",
            component_type="essence",
            rarity="legendary",
            magical_schools=[MagicSchool.TEMPORAL],
            properties=["time_manipulation", "aging_effects"],
            locations=["time_rifts", "ancient_ruins"],
            gathering_difficulty=18,
            base_value=500,
            potency=1.8,
            stability=0.6,
            side_effects=["temporal_displacement", "aging_acceleration"]
        )
        
        # Common components
        components["silver_dust"] = MagicalComponent(
            id="silver_dust",
            name="Silver Dust",
            component_type="mineral",
            rarity="common",
            magical_schools=[MagicSchool.DIVINE, MagicSchool.ARCANE],
            properties=["purification", "undead_repelling"],
            locations=["trading_post", "mines"],
            gathering_difficulty=8,
            base_value=20,
            potency=1.0
        )
        
        return components
    
    def _initialize_spells(self) -> Dict[str, Spell]:
        """Initialize spell database"""
        
        spells = {}
        
        # Elemental spells
        spells["fireball"] = Spell(
            id="fireball",
            name="Fireball",
            school=MagicSchool.ELEMENTAL,
            level=3,
            components={
                SpellComponent.VERBAL: ["incantation_of_flame"],
                SpellComponent.SOMATIC: ["flame_gesture"],
                SpellComponent.MATERIAL: ["sulfur", "bat_guano"]
            },
            material_components=["fire_crystal"],
            casting_time="1 action",
            range_="150 feet",
            duration="instantaneous",
            primary_effect="Explosive fire damage in 20-foot radius",
            secondary_effects=["ignites flammable objects", "creates light"],
            research_difficulty=12,
            research_components=["fire_crystal", "spell_tome"],
            failure_consequences=["self_damage", "uncontrolled_fire"],
            magical_contamination=0.1
        )
        
        spells["healing_light"] = Spell(
            id="healing_light",
            name="Healing Light",
            school=MagicSchool.DIVINE,
            level=2,
            components={
                SpellComponent.VERBAL: ["prayer_of_healing"],
                SpellComponent.SOMATIC: ["blessing_gesture"],
                SpellComponent.DIVINE_FAVOR: ["divine_connection"]
            },
            material_components=["silver_dust", "moonwater"],
            casting_time="1 action",
            range_="touch",
            duration="instantaneous",
            primary_effect="Restores health and vitality",
            secondary_effects=["removes minor curses", "provides temporary blessing"],
            research_difficulty=10,
            research_components=["sacred_text", "moonwater"],
            failure_consequences=["divine_disfavor", "healing_reversal"]
        )
        
        spells["shadow_step"] = Spell(
            id="shadow_step",
            name="Shadow Step",
            school=MagicSchool.SHADOW,
            level=4,
            components={
                SpellComponent.VERBAL: ["whisper_of_darkness"],
                SpellComponent.SOMATIC: ["shadow_weaving"],
                SpellComponent.MATERIAL: ["shadow_herb"]
            },
            material_components=["shadow_herb", "obsidian_shard"],
            casting_time="1 bonus action",
            range_="60 feet",
            duration="instantaneous",
            primary_effect="Teleport through shadows",
            secondary_effects=["brief_invisibility", "shadow_trail"],
            research_difficulty=15,
            prerequisite_spells=["minor_illusion"],
            research_components=["shadow_herb", "shadow_creature_essence"],
            failure_consequences=["shadow_corruption", "stuck_in_shadows"],
            magical_contamination=0.2,
            reality_strain=0.1
        )
        
        spells["time_stop"] = Spell(
            id="time_stop",
            name="Time Stop",
            school=MagicSchool.TEMPORAL,
            level=9,
            components={
                SpellComponent.VERBAL: ["words_of_temporal_binding"],
                SpellComponent.SOMATIC: ["time_weaving_gestures"],
                SpellComponent.MATERIAL: ["temporal_dust", "diamond"]
            },
            material_components=["temporal_dust", "perfect_diamond", "chronometer"],
            casting_time="1 action",
            range_="self",
            duration="1d4+1 rounds",
            primary_effect="Stop time for all but caster",
            secondary_effects=["temporal_echo", "reality_strain"],
            research_difficulty=25,
            prerequisite_spells=["haste", "slow", "temporal_manipulation"],
            research_components=["temporal_dust", "ancient_chronometer", "master_wizard_notes"],
            failure_consequences=["temporal_displacement", "aging", "reality_tear"],
            magical_contamination=0.8,
            reality_strain=0.5
        )
        
        return spells
    
    def _initialize_recipes(self) -> Dict[str, CraftingRecipe]:
        """Initialize crafting recipes"""
        
        recipes = {}
        
        # Alchemy recipes
        recipes["healing_potion"] = CraftingRecipe(
            id="healing_potion",
            name="Healing Potion",
            skill_required=CraftingSkill.ALCHEMY,
            skill_level=3,
            components={"moonwater": 1, "silver_dust": 2, "healing_herbs": 3},
            tools_required=["alchemist_kit", "distillation_apparatus"],
            crafting_time=120,
            difficulty=12,
            output_item="healing_potion",
            output_quantity=1,
            possible_bonuses=["enhanced_potency", "additional_effects"]
        )
        
        recipes["fire_resistance_potion"] = CraftingRecipe(
            id="fire_resistance_potion",
            name="Fire Resistance Potion",
            skill_required=CraftingSkill.ALCHEMY,
            skill_level=5,
            components={"fire_crystal": 1, "salamander_scale": 2, "cooling_herbs": 4},
            tools_required=["alchemist_kit", "heat_resistant_vessel"],
            crafting_time=180,
            difficulty=15,
            output_item="fire_resistance_potion",
            output_quantity=1,
            possible_bonuses=["extended_duration", "fire_immunity"]
        )
        
        # Enchanting recipes
        recipes["enchanted_weapon"] = CraftingRecipe(
            id="enchanted_weapon",
            name="Enchanted Weapon",
            skill_required=CraftingSkill.ENCHANTING,
            skill_level=6,
            components={"base_weapon": 1, "enchanting_dust": 3, "focusing_crystal": 1},
            tools_required=["enchanting_table", "runic_tools"],
            crafting_time=480,  # 8 hours
            difficulty=16,
            output_item="enchanted_weapon",
            output_quantity=1,
            enchantment_slots=2,
            magical_requirements=["arcane_knowledge", "weapon_affinity"],
            possible_bonuses=["additional_enchantment", "masterwork_quality"]
        )
        
        # Artifice recipes
        recipes["magical_focus"] = CraftingRecipe(
            id="magical_focus",
            name="Magical Focus",
            skill_required=CraftingSkill.ARTIFICE,
            skill_level=4,
            components={"focusing_crystal": 1, "precious_metal": 2, "binding_agent": 1},
            tools_required=["jeweler_tools", "magical_forge"],
            crafting_time=360,  # 6 hours
            difficulty=14,
            output_item="magical_focus",
            output_quantity=1,
            enchantment_slots=1,
            possible_bonuses=["spell_power_bonus", "mana_efficiency"]
        )
        
        return recipes
    
    def _initialize_magical_events(self) -> Dict[str, Dict[str, Any]]:
        """Initialize magical events and consequences"""
        
        return {
            "wild_magic_surge": {
                "trigger": "high_magical_contamination",
                "description": "Uncontrolled magical energies cause unpredictable effects",
                "effects": ["random_spell_cast", "magical_mutation", "reality_distortion"],
                "severity_levels": {
                    "minor": ["color_change", "sparkles", "minor_illusion"],
                    "moderate": ["teleport", "polymorph", "summon_creature"],
                    "major": ["plane_shift", "time_dilation", "reality_tear"]
                }
            },
            "spell_feedback": {
                "trigger": "spell_failure",
                "description": "Failed spell energies backlash against the caster",
                "effects": ["mana_drain", "temporary_disability", "magical_marking"],
                "mitigation": ["magical_focus", "protective_ward", "spell_preparation"]
            },
            "divine_intervention": {
                "trigger": "divine_magic_overuse",
                "description": "Divine powers respond to excessive requests",
                "effects": ["blessing", "quest_assignment", "divine_test"],
                "responses": ["acceptance", "negotiation", "defiance"]
            },
            "shadow_corruption": {
                "trigger": "shadow_magic_use",
                "description": "Shadow magic slowly corrupts the user's essence",
                "effects": ["personality_change", "shadow_affinity", "light_sensitivity"],
                "progression": ["mild", "moderate", "severe", "consumed"],
                "remedies": ["divine_blessing", "purification_ritual", "light_therapy"]
            }
        }
    
    def research_spell(
        self,
        player_knowledge: MagicalKnowledge,
        spell_id: str,
        research_time: int,
        components_available: List[str],
        library_quality: int = 1
    ) -> Dict[str, Any]:
        """Research a new spell"""
        
        if spell_id not in self.spells:
            return {"error": "Spell not found"}
        
        spell = self.spells[spell_id]
        
        # Check prerequisites
        for prereq in spell.prerequisite_spells:
            if prereq not in player_knowledge.known_spells:
                return {"error": f"Prerequisite spell '{prereq}' not known"}
        
        # Check research components
        missing_components = []
        for component in spell.research_components:
            if component not in components_available:
                missing_components.append(component)
        
        if missing_components:
            return {"error": f"Missing components: {missing_components}"}
        
        # Calculate research progress
        base_progress = research_time / 60  # hours of research
        
        # Apply bonuses
        school_affinity = player_knowledge.school_affinities.get(spell.school, 1.0)
        library_bonus = library_quality * 0.2
        knowledge_bonus = player_knowledge.research_bonus * 0.1
        
        total_progress = base_progress * school_affinity * (1 + library_bonus + knowledge_bonus)
        
        # Update research progress
        current_progress = player_knowledge.researching_spells.get(spell_id, 0.0)
        new_progress = min(100.0, current_progress + total_progress)
        player_knowledge.researching_spells[spell_id] = new_progress
        
        # Check if research is complete
        research_result = {
            "spell_id": spell_id,
            "progress": new_progress,
            "progress_gained": total_progress,
            "completed": False
        }
        
        if new_progress >= 100.0:
            # Research complete
            player_knowledge.known_spells.append(spell_id)
            player_knowledge.spell_mastery[spell_id] = 1
            del player_knowledge.researching_spells[spell_id]
            
            research_result["completed"] = True
            research_result["message"] = f"Successfully learned {spell.name}!"
            
            # Increase school affinity
            current_affinity = player_knowledge.school_affinities.get(spell.school, 1.0)
            player_knowledge.school_affinities[spell.school] = min(2.0, current_affinity + 0.1)
        
        # Apply magical contamination from research
        contamination_gain = spell.magical_contamination * 0.1  # Reduced for research
        player_knowledge.magical_contamination += contamination_gain
        
        research_result["contamination_gained"] = contamination_gain
        
        return research_result
    
    def cast_spell(
        self,
        player_knowledge: MagicalKnowledge,
        spell_id: str,
        components_available: List[str],
        casting_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cast a spell with component consumption and consequences"""
        
        if spell_id not in self.spells:
            return {"error": "Spell not found"}
        
        if spell_id not in player_knowledge.known_spells:
            return {"error": "Spell not known"}
        
        spell = self.spells[spell_id]
        
        # Check material components
        missing_components = []
        for component in spell.material_components:
            if component not in components_available:
                missing_components.append(component)
        
        if missing_components:
            return {"error": f"Missing components: {missing_components}"}
        
        # Calculate casting success
        mastery_level = player_knowledge.spell_mastery.get(spell_id, 1)
        school_affinity = player_knowledge.school_affinities.get(spell.school, 1.0)
        contamination_penalty = player_knowledge.magical_contamination * 0.1
        
        success_chance = (mastery_level * 0.2 + school_affinity * 0.3 + 0.5) - contamination_penalty
        success_chance = max(0.1, min(0.95, success_chance))  # Clamp between 10% and 95%
        
        casting_result = {
            "spell_name": spell.name,
            "success": False,
            "effects": [],
            "consequences": [],
            "components_consumed": spell.material_components.copy()
        }
        
        # Determine success
        if random.random() <= success_chance:
            # Successful casting
            casting_result["success"] = True
            casting_result["effects"] = [spell.primary_effect] + spell.secondary_effects
            
            # Gain mastery
            if random.random() < 0.1:  # 10% chance to gain mastery
                player_knowledge.spell_mastery[spell_id] = min(5, mastery_level + 1)
                casting_result["mastery_gained"] = True
        
        else:
            # Failed casting
            casting_result["effects"] = ["Spell fails to manifest properly"]
            
            # Apply failure consequences
            for consequence in spell.failure_consequences:
                casting_result["consequences"].append(consequence)
            
            # Trigger spell feedback event
            if random.random() < 0.3:  # 30% chance of feedback
                feedback = self._trigger_magical_event("spell_feedback", player_knowledge)
                casting_result["magical_event"] = feedback
        
        # Apply magical contamination
        contamination_gain = spell.magical_contamination
        if not casting_result["success"]:
            contamination_gain *= 1.5  # Failed spells cause more contamination
        
        player_knowledge.magical_contamination += contamination_gain
        casting_result["contamination_gained"] = contamination_gain
        
        # Check for wild magic surge
        if player_knowledge.magical_contamination > 1.0:
            if random.random() < player_knowledge.magical_contamination * 0.2:
                wild_magic = self._trigger_magical_event("wild_magic_surge", player_knowledge)
                casting_result["wild_magic_surge"] = wild_magic
                # Reset contamination after surge
                player_knowledge.magical_contamination *= 0.5
        
        # Apply reality strain
        if spell.reality_strain > 0:
            player_knowledge.reality_awareness += spell.reality_strain
            if player_knowledge.reality_awareness > 2.0:
                casting_result["reality_warning"] = "The fabric of reality feels strained..."
        
        return casting_result
    
    def craft_item(
        self,
        player_skills: CraftingSkills,
        recipe_id: str,
        components_available: Dict[str, int],
        workspace_quality: int = 1,
        time_investment: int = 100  # percentage of normal time
    ) -> Dict[str, Any]:
        """Craft an item using components and skills"""
        
        if recipe_id not in self.recipes:
            return {"error": "Recipe not found"}
        
        if recipe_id not in player_skills.known_recipes:
            return {"error": "Recipe not known"}
        
        recipe = self.recipes[recipe_id]
        
        # Check skill level
        current_skill = player_skills.skill_levels.get(recipe.skill_required, 0)
        if current_skill < recipe.skill_level:
            return {"error": f"Insufficient {recipe.skill_required.value} skill"}
        
        # Check components
        missing_components = {}
        for component, required in recipe.components.items():
            available = components_available.get(component, 0)
            if available < required:
                missing_components[component] = required - available
        
        if missing_components:
            return {"error": f"Missing components: {missing_components}"}
        
        # Check tools
        missing_tools = []
        for tool in recipe.tools_required:
            if tool not in player_skills.owned_tools:
                missing_tools.append(tool)
        
        if missing_tools:
            return {"error": f"Missing tools: {missing_tools}"}
        
        # Calculate crafting success
        skill_bonus = (current_skill - recipe.skill_level) * 0.1
        workspace_bonus = workspace_quality * 0.1
        time_bonus = (time_investment - 100) * 0.002  # Bonus for extra time investment
        
        success_chance = 0.7 + skill_bonus + workspace_bonus + time_bonus
        success_chance = max(0.1, min(0.98, success_chance))
        
        crafting_result = {
            "recipe_name": recipe.name,
            "success": False,
            "output": {},
            "components_consumed": recipe.components.copy(),
            "quality": "standard",
            "bonuses": []
        }
        
        # Determine success and quality
        roll = random.random()
        
        if roll <= success_chance:
            # Successful crafting
            crafting_result["success"] = True
            crafting_result["output"] = {
                recipe.output_item: recipe.output_quantity
            }
            
            # Determine quality
            quality_roll = random.random()
            if quality_roll > 0.9:
                crafting_result["quality"] = "masterwork"
                player_skills.masterwork_items.append(f"{recipe.output_item}_{datetime.now().timestamp()}")
            elif quality_roll > 0.7:
                crafting_result["quality"] = "superior"
            elif quality_roll > 0.3:
                crafting_result["quality"] = "standard"
            else:
                crafting_result["quality"] = "inferior"
            
            # Check for bonuses
            for bonus in recipe.possible_bonuses:
                if random.random() < 0.2:  # 20% chance for each bonus
                    crafting_result["bonuses"].append(bonus)
            
            # Gain skill experience
            skill_gain = max(1, recipe.skill_level - current_skill + 1)
            player_skills.skill_levels[recipe.skill_required] = current_skill + skill_gain
            crafting_result["skill_gained"] = skill_gain
        
        else:
            # Failed crafting
            crafting_result["output"] = {}
            # Partial component loss on failure
            consumed = {}
            for component, amount in recipe.components.items():
                consumed[component] = max(1, amount // 2)  # Lose half components
            crafting_result["components_consumed"] = consumed
        
        return crafting_result
    
    def _trigger_magical_event(self, event_type: str, player_knowledge: MagicalKnowledge) -> Dict[str, Any]:
        """Trigger a magical event with consequences"""
        
        if event_type not in self.magical_events:
            return {"error": "Unknown magical event"}
        
        event = self.magical_events[event_type]
        
        # Determine severity based on player's magical contamination
        contamination = player_knowledge.magical_contamination
        
        if contamination < 0.5:
            severity = "minor"
        elif contamination < 1.0:
            severity = "moderate"
        else:
            severity = "major"
        
        # Select random effect based on severity
        if event_type == "wild_magic_surge":
            effects = event["severity_levels"][severity]
            selected_effect = random.choice(effects)
        else:
            selected_effect = random.choice(event["effects"])
        
        event_result = {
            "event_type": event_type,
            "description": event["description"],
            "severity": severity,
            "effect": selected_effect,
            "consequences": []
        }
        
        # Apply specific effects
        if event_type == "wild_magic_surge":
            if selected_effect == "teleport":
                event_result["consequences"].append("Randomly teleported to nearby location")
            elif selected_effect == "polymorph":
                event_result["consequences"].append("Temporarily transformed into animal")
            elif selected_effect == "reality_tear":
                event_result["consequences"].append("Small tear in reality fabric created")
                player_knowledge.reality_awareness += 0.5
        
        elif event_type == "shadow_corruption":
            # Progressive corruption effects
            corruption_level = player_knowledge.magical_contamination * 2  # Shadow magic causes more corruption
            
            if corruption_level > 3.0:
                event_result["consequences"].append("Severe shadow corruption - seeking light causes pain")
            elif corruption_level > 2.0:
                event_result["consequences"].append("Moderate shadow corruption - appearance becomes darker")
            else:
                event_result["consequences"].append("Mild shadow corruption - minor personality shift")
        
        return event_result
    
    def get_available_components(self, location: str, season: str, gathering_skill: int) -> List[Dict[str, Any]]:
        """Get components available for gathering at a location"""
        
        available = []
        
        for component_id, component in self.components.items():
            if location in component.locations:
                # Check seasonal availability
                if component.seasonal_availability and season not in component.seasonal_availability:
                    continue
                
                # Check if player can gather this component
                if gathering_skill >= component.gathering_difficulty:
                    success_chance = min(0.9, (gathering_skill - component.gathering_difficulty + 10) * 0.1)
                    
                    available.append({
                        "component": component,
                        "success_chance": success_chance,
                        "base_quantity": max(1, (gathering_skill - component.gathering_difficulty) // 3 + 1)
                    })
        
        return available
    
    def gather_component(self, component_id: str, gathering_skill: int, tools: List[str]) -> Dict[str, Any]:
        """Attempt to gather a magical component"""
        
        if component_id not in self.components:
            return {"error": "Component not found"}
        
        component = self.components[component_id]
        
        # Calculate success chance
        base_chance = max(0.1, (gathering_skill - component.gathering_difficulty + 10) * 0.1)
        
        # Tool bonuses
        tool_bonus = 0
        if "gathering_tools" in tools:
            tool_bonus += 0.1
        if "magical_detector" in tools:
            tool_bonus += 0.15
        
        success_chance = min(0.95, base_chance + tool_bonus)
        
        result = {
            "component_name": component.name,
            "success": False,
            "quantity": 0,
            "quality": "standard"
        }
        
        if random.random() <= success_chance:
            result["success"] = True
            result["quantity"] = max(1, (gathering_skill - component.gathering_difficulty) // 3 + 1)
            
            # Quality determination
            quality_roll = random.random()
            if quality_roll > 0.85:
                result["quality"] = "exceptional"
                result["quantity"] += 1
            elif quality_roll > 0.6:
                result["quality"] = "high"
            elif quality_roll < 0.2:
                result["quality"] = "poor"
            
            # Check for side effects
            if component.side_effects and random.random() < 0.1:
                result["side_effect"] = random.choice(component.side_effects)
        
        return result
    
    def calculate_component_market_value(self, component_id: str, quality: str = "standard") -> int:
        """Calculate current market value of a component"""
        
        if component_id not in self.components:
            return 0
        
        component = self.components[component_id]
        base_value = component.base_value
        
        # Quality modifiers
        quality_multipliers = {
            "poor": 0.5,
            "standard": 1.0,
            "high": 1.5,
            "exceptional": 2.0
        }
        
        quality_mod = quality_multipliers.get(quality, 1.0)
        
        # Market availability affects price
        availability_mod = 2.0 - component.market_availability  # Scarcity increases price
        
        # Rarity affects base value
        rarity_multipliers = {
            "common": 1.0,
            "uncommon": 2.0,
            "rare": 4.0,
            "legendary": 8.0
        }
        
        rarity_mod = rarity_multipliers.get(component.rarity, 1.0)
        
        final_value = int(base_value * quality_mod * availability_mod * rarity_mod)
        
        return final_value 