"""
AI-RPG-Alpha: Enhanced Combat & Skills System

Sophisticated combat system with tactical positioning, environmental interactions,
deep skill specialization trees, and narrative-driven combat outcomes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime


class CombatStyle(Enum):
    """Combat style preferences"""
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    TACTICAL = "tactical"
    STEALTH = "stealth"
    MAGICAL = "magical"
    SUPPORT = "support"


class EnvironmentType(Enum):
    """Types of combat environments"""
    FOREST = "forest"
    DUNGEON = "dungeon"
    URBAN = "urban"
    MOUNTAIN = "mountain"
    SWAMP = "swamp"
    DESERT = "desert"
    UNDERGROUND = "underground"
    MAGICAL_REALM = "magical_realm"


class SkillTree(Enum):
    """Skill specialization trees"""
    WARRIOR = "warrior"
    ROGUE = "rogue"
    MAGE = "mage"
    RANGER = "ranger"
    PALADIN = "paladin"
    BARD = "bard"
    MONK = "monk"
    WARLOCK = "warlock"


@dataclass
class EnvironmentalFeature:
    """Environmental feature that can be used in combat"""
    id: str
    name: str
    description: str
    
    # Usage properties
    usable: bool = True
    destructible: bool = False
    moveable: bool = False
    
    # Effects
    cover_bonus: int = 0
    height_advantage: int = 0
    special_actions: List[str] = field(default_factory=list)
    
    # Requirements
    required_skills: Dict[str, int] = field(default_factory=dict)
    required_items: List[str] = field(default_factory=list)
    
    # Consequences
    destruction_effects: List[str] = field(default_factory=list)
    usage_consequences: List[str] = field(default_factory=list)


@dataclass
class CombatPosition:
    """Position in combat with tactical properties"""
    x: int
    y: int
    elevation: int = 0
    
    # Tactical properties
    cover_level: int = 0  # 0-3
    concealment: int = 0  # 0-3
    mobility_restriction: int = 0  # 0-3
    
    # Environmental features
    features: List[str] = field(default_factory=list)
    hazards: List[str] = field(default_factory=list)
    
    # Line of sight
    visible_positions: List[Tuple[int, int]] = field(default_factory=list)
    blocked_positions: List[Tuple[int, int]] = field(default_factory=list)


@dataclass
class Skill:
    """Individual skill with progression"""
    id: str
    name: str
    description: str
    skill_tree: SkillTree
    
    # Progression
    current_level: int = 1
    experience: int = 0
    max_level: int = 10
    
    # Requirements
    prerequisites: List[str] = field(default_factory=list)
    attribute_requirements: Dict[str, int] = field(default_factory=dict)
    
    # Effects
    passive_bonuses: Dict[str, float] = field(default_factory=dict)
    active_abilities: List[str] = field(default_factory=list)
    
    # Usage
    cooldown_remaining: int = 0
    uses_per_day: int = 0
    uses_remaining: int = 0


@dataclass
class CombatAction:
    """A combat action with tactical and narrative elements"""
    id: str
    name: str
    description: str
    action_type: str  # attack, defend, move, special, environmental
    
    # Mechanics
    accuracy_bonus: int = 0
    damage_dice: str = "1d6"
    damage_bonus: int = 0
    
    # Requirements
    required_skills: Dict[str, int] = field(default_factory=dict)
    required_position: Optional[str] = None
    required_environment: Optional[str] = None
    
    # Tactical effects
    positioning_effects: Dict[str, Any] = field(default_factory=dict)
    area_of_effect: Dict[str, Any] = field(default_factory=dict)
    
    # Narrative elements
    success_narrative: List[str] = field(default_factory=list)
    failure_narrative: List[str] = field(default_factory=list)
    environmental_narrative: Dict[str, List[str]] = field(default_factory=dict)
    
    # Consequences
    environmental_changes: List[str] = field(default_factory=list)
    status_effects: List[str] = field(default_factory=list)


@dataclass
class CombatEncounter:
    """Complete combat encounter with narrative context"""
    id: str
    title: str
    description: str
    
    # Environment
    environment_type: EnvironmentType
    battlefield_size: Tuple[int, int] = (10, 10)
    environmental_features: Dict[str, EnvironmentalFeature] = field(default_factory=dict)
    
    # Participants
    player_position: CombatPosition = field(default_factory=lambda: CombatPosition(0, 0))
    enemy_positions: Dict[str, CombatPosition] = field(default_factory=dict)
    ally_positions: Dict[str, CombatPosition] = field(default_factory=dict)
    
    # Objectives
    primary_objective: str = "defeat_all_enemies"
    secondary_objectives: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)
    
    # Narrative context
    combat_setup: str = ""
    stakes: List[str] = field(default_factory=list)
    potential_consequences: Dict[str, List[str]] = field(default_factory=dict)
    
    # Dynamic elements
    turn_count: int = 0
    environmental_changes: List[str] = field(default_factory=list)
    narrative_beats: List[str] = field(default_factory=list)


class EnhancedCombatEngine:
    """Advanced combat system with tactical depth and narrative integration"""
    
    def __init__(self):
        self.skill_trees = self._initialize_skill_trees()
        self.environmental_features = self._initialize_environmental_features()
        self.combat_actions = self._initialize_combat_actions()
        self.encounter_templates = self._initialize_encounter_templates()
        
        # Combat state
        self.active_encounter: Optional[CombatEncounter] = None
        self.combat_history: List[Dict[str, Any]] = []
    
    def _initialize_skill_trees(self) -> Dict[str, Dict[str, Skill]]:
        """Initialize skill trees and specializations"""
        
        skill_trees = {}
        
        # Warrior skill tree
        skill_trees[SkillTree.WARRIOR] = {
            "weapon_mastery": Skill(
                id="weapon_mastery",
                name="Weapon Mastery",
                description="Enhanced proficiency with weapons",
                skill_tree=SkillTree.WARRIOR,
                passive_bonuses={"attack_bonus": 1.0, "damage_bonus": 0.5},
                active_abilities=["power_attack", "disarming_strike"]
            ),
            "tactical_awareness": Skill(
                id="tactical_awareness",
                name="Tactical Awareness",
                description="Superior battlefield positioning and timing",
                skill_tree=SkillTree.WARRIOR,
                passive_bonuses={"initiative_bonus": 2.0, "positioning_bonus": 1.0},
                active_abilities=["battlefield_control", "opportunity_strike"]
            ),
            "defensive_stance": Skill(
                id="defensive_stance",
                name="Defensive Mastery",
                description="Advanced defensive techniques and armor usage",
                skill_tree=SkillTree.WARRIOR,
                passive_bonuses={"armor_bonus": 2.0, "damage_reduction": 1.0},
                active_abilities=["shield_wall", "counter_attack"]
            ),
            "berserker_rage": Skill(
                id="berserker_rage",
                name="Berserker's Fury",
                description="Channel inner rage for devastating attacks",
                skill_tree=SkillTree.WARRIOR,
                prerequisites=["weapon_mastery"],
                active_abilities=["rage_mode", "whirlwind_attack"],
                uses_per_day=3
            )
        }
        
        # Rogue skill tree
        skill_trees[SkillTree.ROGUE] = {
            "stealth_mastery": Skill(
                id="stealth_mastery",
                name="Master of Shadows",
                description="Expert stealth and concealment abilities",
                skill_tree=SkillTree.ROGUE,
                passive_bonuses={"stealth_bonus": 3.0, "surprise_attack_bonus": 2.0},
                active_abilities=["vanish", "shadow_step"]
            ),
            "precision_strikes": Skill(
                id="precision_strikes",
                name="Precision Strikes",
                description="Target vital points for maximum effect",
                skill_tree=SkillTree.ROGUE,
                passive_bonuses={"critical_chance": 0.2, "critical_damage": 1.5},
                active_abilities=["sneak_attack", "vital_strike"]
            ),
            "agility_training": Skill(
                id="agility_training",
                name="Enhanced Agility",
                description="Superior speed and evasion capabilities",
                skill_tree=SkillTree.ROGUE,
                passive_bonuses={"dodge_bonus": 2.0, "movement_bonus": 1.0},
                active_abilities=["evasive_maneuver", "lightning_reflexes"]
            ),
            "dirty_fighting": Skill(
                id="dirty_fighting",
                name="Dirty Fighting",
                description="Unconventional combat techniques",
                skill_tree=SkillTree.ROGUE,
                prerequisites=["precision_strikes"],
                active_abilities=["cheap_shot", "disorienting_attack", "environmental_weapon"],
                uses_per_day=5
            )
        }
        
        # Mage skill tree
        skill_trees[SkillTree.MAGE] = {
            "elemental_mastery": Skill(
                id="elemental_mastery",
                name="Elemental Mastery",
                description="Command over elemental forces",
                skill_tree=SkillTree.MAGE,
                passive_bonuses={"spell_damage": 1.5, "elemental_resistance": 1.0},
                active_abilities=["fireball", "ice_shard", "lightning_bolt"]
            ),
            "arcane_knowledge": Skill(
                id="arcane_knowledge",
                name="Arcane Scholar",
                description="Deep understanding of magical theory",
                skill_tree=SkillTree.MAGE,
                passive_bonuses={"mana_bonus": 2.0, "spell_accuracy": 1.0},
                active_abilities=["dispel_magic", "counterspell", "magical_analysis"]
            ),
            "battle_magic": Skill(
                id="battle_magic",
                name="Battle Magic",
                description="Combat-focused spellcasting techniques",
                skill_tree=SkillTree.MAGE,
                prerequisites=["elemental_mastery"],
                passive_bonuses={"casting_speed": 1.0, "spell_penetration": 1.0},
                active_abilities=["quickcast", "spell_combo", "magical_shield"]
            ),
            "reality_manipulation": Skill(
                id="reality_manipulation",
                name="Reality Manipulation",
                description="Advanced magic that bends reality itself",
                skill_tree=SkillTree.MAGE,
                prerequisites=["arcane_knowledge", "battle_magic"],
                active_abilities=["time_stop", "teleport", "reality_tear"],
                uses_per_day=2
            )
        }
        
        # Ranger skill tree
        skill_trees[SkillTree.RANGER] = {
            "nature_bond": Skill(
                id="nature_bond",
                name="Bond with Nature",
                description="Deep connection to natural environments",
                skill_tree=SkillTree.RANGER,
                passive_bonuses={"nature_environments_bonus": 2.0, "animal_handling": 2.0},
                active_abilities=["animal_companion", "nature_guidance", "weather_sense"]
            ),
            "archery_mastery": Skill(
                id="archery_mastery",
                name="Master Archer",
                description="Unparalleled skill with ranged weapons",
                skill_tree=SkillTree.RANGER,
                passive_bonuses={"ranged_accuracy": 3.0, "ranged_damage": 1.0},
                active_abilities=["perfect_shot", "multi_shot", "piercing_arrow"]
            ),
            "survival_expert": Skill(
                id="survival_expert",
                name="Survival Expert",
                description="Master of wilderness survival and tracking",
                skill_tree=SkillTree.RANGER,
                passive_bonuses={"tracking_bonus": 3.0, "endurance_bonus": 2.0},
                active_abilities=["track_quarry", "wilderness_healing", "camouflage"]
            ),
            "beast_master": Skill(
                id="beast_master",
                name="Beast Master",
                description="Command powerful animal allies",
                skill_tree=SkillTree.RANGER,
                prerequisites=["nature_bond", "survival_expert"],
                active_abilities=["summon_pack", "beast_charge", "coordinated_attack"],
                uses_per_day=3
            )
        }
        
        return skill_trees
    
    def _initialize_environmental_features(self) -> Dict[str, EnvironmentalFeature]:
        """Initialize environmental features for tactical combat"""
        
        features = {}
        
        # Forest features
        features["tall_tree"] = EnvironmentalFeature(
            id="tall_tree",
            name="Tall Tree",
            description="A large tree that can be climbed for height advantage",
            cover_bonus=2,
            height_advantage=3,
            special_actions=["climb_tree", "swing_on_branches", "drop_attack"],
            required_skills={"climbing": 5},
            destruction_effects=["falling_tree_damage", "blocks_path"]
        )
        
        features["dense_undergrowth"] = EnvironmentalFeature(
            id="dense_undergrowth",
            name="Dense Undergrowth",
            description="Thick bushes that provide concealment but slow movement",
            cover_bonus=1,
            special_actions=["hide_in_bushes", "set_ambush", "rustle_distraction"],
            usage_consequences=["movement_penalty", "noise_when_moving"]
        )
        
        # Dungeon features
        features["stone_pillar"] = EnvironmentalFeature(
            id="stone_pillar",
            name="Stone Pillar",
            description="Ancient stone pillar providing solid cover",
            cover_bonus=3,
            destructible=True,
            special_actions=["take_cover", "push_pillar", "ricochet_shot"],
            required_skills={"strength": 8},
            destruction_effects=["rubble_blocks_area", "dust_cloud"]
        )
        
        features["magical_crystal"] = EnvironmentalFeature(
            id="magical_crystal",
            name="Magical Crystal",
            description="Glowing crystal that amplifies magical energy",
            special_actions=["channel_energy", "overload_crystal", "absorb_magic"],
            required_skills={"arcane_knowledge": 6},
            destruction_effects=["magical_explosion", "energy_feedback"]
        )
        
        # Urban features
        features["market_stall"] = EnvironmentalFeature(
            id="market_stall",
            name="Market Stall",
            description="Wooden stall with various goods and improvised weapons",
            cover_bonus=1,
            destructible=True,
            moveable=True,
            special_actions=["throw_goods", "use_improvised_weapon", "create_barricade"],
            destruction_effects=["scattered_goods", "angry_merchant"]
        )
        
        features["rooftop"] = EnvironmentalFeature(
            id="rooftop",
            name="Rooftop",
            description="High vantage point overlooking the street",
            height_advantage=4,
            special_actions=["rain_arrows", "leap_between_buildings", "drop_objects"],
            required_skills={"climbing": 6, "acrobatics": 5},
            usage_consequences=["exposed_position", "fall_risk"]
        )
        
        return features
    
    def _initialize_combat_actions(self) -> Dict[str, CombatAction]:
        """Initialize available combat actions"""
        
        actions = {}
        
        # Basic attacks
        actions["weapon_strike"] = CombatAction(
            id="weapon_strike",
            name="Weapon Strike",
            description="Standard weapon attack",
            action_type="attack",
            damage_dice="1d8",
            success_narrative=["delivers a solid blow", "strikes true", "finds its mark"],
            failure_narrative=["swing goes wide", "attack is parried", "misses the target"]
        )
        
        # Environmental actions
        actions["use_cover"] = CombatAction(
            id="use_cover",
            name="Take Cover",
            description="Use environmental features for protection",
            action_type="defensive",
            positioning_effects={"cover_bonus": 2, "mobility_penalty": 1},
            success_narrative=["ducks behind cover", "finds protective position"],
            environmental_narrative={
                "forest": ["hides behind a large tree", "uses undergrowth for concealment"],
                "urban": ["takes cover behind a wall", "ducks into an alley"],
                "dungeon": ["shelters behind a pillar", "uses the shadows"]
            }
        )
        
        actions["environmental_attack"] = CombatAction(
            id="environmental_attack",
            name="Environmental Attack",
            description="Use the environment as a weapon",
            action_type="environmental",
            required_skills={"tactics": 5},
            damage_dice="2d6",
            environmental_changes=["feature_destroyed", "area_affected"],
            success_narrative=["cleverly uses the environment", "turns surroundings into weapon"],
            environmental_narrative={
                "forest": ["drops a heavy branch", "uses thorny vines", "causes rockslide"],
                "urban": ["topples market stall", "throws cobblestones", "uses rope trap"],
                "dungeon": ["triggers ancient trap", "collapses weak ceiling", "redirects magical energy"]
            }
        )
        
        # Tactical maneuvers
        actions["flanking_maneuver"] = CombatAction(
            id="flanking_maneuver",
            name="Flanking Maneuver",
            description="Move to attack from an advantageous angle",
            action_type="move",
            required_skills={"tactics": 4},
            positioning_effects={"flanking_bonus": 3, "expose_to_counterattack": True},
            success_narrative=["outmaneuvers the enemy", "gains superior position"],
            failure_narrative=["movement is anticipated", "fails to find opening"]
        )
        
        actions["feint_attack"] = CombatAction(
            id="feint_attack",
            name="Feint Attack",
            description="Deceive enemy with false attack to create opening",
            action_type="special",
            required_skills={"deception": 6},
            damage_dice="1d6",
            damage_bonus=2,
            success_narrative=["expertly deceives the enemy", "creates perfect opening"],
            failure_narrative=["feint is seen through", "enemy doesn't fall for trick"]
        )
        
        # Magic-enhanced actions
        actions["spell_strike"] = CombatAction(
            id="spell_strike",
            name="Spell-Enhanced Strike",
            description="Combine weapon attack with magical energy",
            action_type="attack",
            required_skills={"weapon_skill": 5, "magic": 4},
            damage_dice="1d8",
            damage_bonus=3,
            status_effects=["magical_burn", "elemental_weakness"],
            success_narrative=["weapon crackles with magical energy", "spell and steel unite"],
            failure_narrative=["magic dissipates harmlessly", "spell misfires"]
        )
        
        return actions
    
    def _initialize_encounter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize combat encounter templates"""
        
        return {
            "bandit_ambush": {
                "title": "Bandit Ambush",
                "description": "Bandits attack from forest concealment",
                "environment": EnvironmentType.FOREST,
                "primary_objective": "survive_ambush",
                "secondary_objectives": ["capture_bandit_leader", "protect_innocent_travelers"],
                "stakes": ["reputation_with_merchants", "safety_of_trade_routes"],
                "setup_narrative": "The forest suddenly erupts with hostile shouts as bandits emerge from hiding!"
            },
            "noble_duel": {
                "title": "Honor Duel",
                "description": "Formal duel with a noble over honor",
                "environment": EnvironmentType.URBAN,
                "primary_objective": "win_duel",
                "secondary_objectives": ["maintain_honor", "avoid_killing"],
                "stakes": ["social_standing", "political_consequences"],
                "setup_narrative": "Steel rings against steel as the formal duel begins in the city square."
            },
            "ancient_guardian": {
                "title": "Ancient Guardian",
                "description": "Face an awakened magical guardian",
                "environment": EnvironmentType.DUNGEON,
                "primary_objective": "defeat_guardian",
                "secondary_objectives": ["preserve_ancient_artifacts", "uncover_guardian_purpose"],
                "stakes": ["ancient_knowledge", "magical_artifacts"],
                "setup_narrative": "Stone and magic come alive as the ancient guardian awakens to defend its charge."
            }
        }
    
    def initiate_combat(
        self,
        encounter_type: str,
        participants: Dict[str, Any],
        environment_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Initiate a combat encounter"""
        
        if encounter_type not in self.encounter_templates:
            return {"error": "Unknown encounter type"}
        
        template = self.encounter_templates[encounter_type]
        
        # Create encounter
        encounter = CombatEncounter(
            id=f"{encounter_type}_{datetime.now().timestamp()}",
            title=template["title"],
            description=template["description"],
            environment_type=template["environment"],
            primary_objective=template["primary_objective"],
            secondary_objectives=template["secondary_objectives"],
            combat_setup=template["setup_narrative"]
        )
        
        # Set up battlefield
        self._setup_battlefield(encounter, environment_context or {})
        
        # Position participants
        self._position_participants(encounter, participants)
        
        self.active_encounter = encounter
        
        return {
            "encounter_id": encounter.id,
            "title": encounter.title,
            "description": encounter.description,
            "setup_narrative": encounter.combat_setup,
            "environment": encounter.environment_type.value,
            "objectives": {
                "primary": encounter.primary_objective,
                "secondary": encounter.secondary_objectives
            },
            "battlefield": self._get_battlefield_description(encounter)
        }
    
    def _setup_battlefield(self, encounter: CombatEncounter, context: Dict[str, Any]):
        """Set up the battlefield with environmental features"""
        
        environment_features = {
            EnvironmentType.FOREST: ["tall_tree", "dense_undergrowth"],
            EnvironmentType.URBAN: ["market_stall", "rooftop"],
            EnvironmentType.DUNGEON: ["stone_pillar", "magical_crystal"]
        }
        
        features_for_env = environment_features.get(encounter.environment_type, [])
        
        # Place features randomly on battlefield
        for feature_id in features_for_env:
            if feature_id in self.environmental_features:
                x = random.randint(1, encounter.battlefield_size[0] - 2)
                y = random.randint(1, encounter.battlefield_size[1] - 2)
                
                feature = self.environmental_features[feature_id]
                encounter.environmental_features[f"{feature_id}_{x}_{y}"] = feature
    
    def _position_participants(self, encounter: CombatEncounter, participants: Dict[str, Any]):
        """Position all combat participants"""
        
        # Position player
        encounter.player_position = CombatPosition(
            x=random.randint(0, 2),
            y=random.randint(0, encounter.battlefield_size[1] - 1)
        )
        
        # Position enemies
        for enemy_id, enemy_data in participants.get("enemies", {}).items():
            encounter.enemy_positions[enemy_id] = CombatPosition(
                x=random.randint(encounter.battlefield_size[0] - 3, encounter.battlefield_size[0] - 1),
                y=random.randint(0, encounter.battlefield_size[1] - 1)
            )
        
        # Position allies
        for ally_id, ally_data in participants.get("allies", {}).items():
            encounter.ally_positions[ally_id] = CombatPosition(
                x=random.randint(0, 2),
                y=random.randint(0, encounter.battlefield_size[1] - 1)
            )
    
    def execute_combat_action(
        self,
        action_id: str,
        target: Optional[str] = None,
        position: Optional[Tuple[int, int]] = None,
        player_skills: Dict[str, int] = None,
        approach: str = "standard"
    ) -> Dict[str, Any]:
        """Execute a combat action"""
        
        if not self.active_encounter:
            return {"error": "No active combat encounter"}
        
        if action_id not in self.combat_actions:
            return {"error": "Unknown combat action"}
        
        action = self.combat_actions[action_id]
        player_skills = player_skills or {}
        
        # Check requirements
        requirements_met = True
        missing_requirements = []
        
        for skill, required_level in action.required_skills.items():
            if player_skills.get(skill, 0) < required_level:
                requirements_met = False
                missing_requirements.append(f"{skill}: {required_level}")
        
        if not requirements_met:
            return {
                "error": "Requirements not met",
                "missing_requirements": missing_requirements
            }
        
        # Calculate success probability
        success_chance = self._calculate_action_success(action, player_skills, approach)
        
        # Execute action
        success = random.random() <= success_chance
        
        result = {
            "action_name": action.name,
            "success": success,
            "approach": approach,
            "narrative": "",
            "effects": [],
            "environmental_changes": [],
            "position_changes": {},
            "damage_dealt": 0
        }
        
        # Generate narrative
        if success:
            result["narrative"] = self._generate_success_narrative(action, approach)
            
            # Apply damage if applicable
            if action.damage_dice:
                damage = self._roll_damage(action.damage_dice, action.damage_bonus)
                result["damage_dealt"] = damage
            
            # Apply positioning effects
            if action.positioning_effects:
                result["position_changes"] = action.positioning_effects
                self._apply_positioning_effects(action.positioning_effects)
            
            # Apply environmental changes
            if action.environmental_changes:
                result["environmental_changes"] = action.environmental_changes
                self._apply_environmental_changes(action.environmental_changes)
            
            # Apply status effects
            if action.status_effects:
                result["effects"] = action.status_effects
        
        else:
            result["narrative"] = self._generate_failure_narrative(action, approach)
        
        # Advance combat turn
        self.active_encounter.turn_count += 1
        
        # Check for dynamic events
        dynamic_events = self._check_dynamic_events()
        if dynamic_events:
            result["dynamic_events"] = dynamic_events
        
        return result
    
    def _calculate_action_success(
        self,
        action: CombatAction,
        player_skills: Dict[str, int],
        approach: str
    ) -> float:
        """Calculate probability of action success"""
        
        base_success = 0.6
        
        # Skill bonuses
        skill_bonus = 0
        for skill, required_level in action.required_skills.items():
            player_level = player_skills.get(skill, 0)
            if player_level >= required_level:
                skill_bonus += (player_level - required_level) * 0.05
        
        # Approach modifiers
        approach_modifiers = {
            "aggressive": {"success": -0.1, "damage": 1.2},
            "defensive": {"success": 0.1, "damage": 0.8},
            "tactical": {"success": 0.15, "damage": 1.0},
            "reckless": {"success": -0.2, "damage": 1.5}
        }
        
        approach_mod = approach_modifiers.get(approach, {"success": 0})["success"]
        
        # Environmental factors
        env_modifier = self._get_environmental_modifier(action)
        
        total_success = base_success + skill_bonus + approach_mod + env_modifier
        return max(0.05, min(0.95, total_success))
    
    def _get_environmental_modifier(self, action: CombatAction) -> float:
        """Get environmental modifier for action success"""
        
        if not self.active_encounter:
            return 0.0
        
        environment = self.active_encounter.environment_type
        
        # Environmental advantages/disadvantages by action type
        env_modifiers = {
            EnvironmentType.FOREST: {
                "stealth": 0.2,
                "ranged": -0.1,
                "environmental": 0.3
            },
            EnvironmentType.URBAN: {
                "social": 0.2,
                "environmental": 0.1,
                "stealth": -0.1
            },
            EnvironmentType.DUNGEON: {
                "magic": 0.2,
                "ranged": -0.2,
                "environmental": 0.2
            }
        }
        
        action_category = self._categorize_action(action)
        return env_modifiers.get(environment, {}).get(action_category, 0.0)
    
    def _categorize_action(self, action: CombatAction) -> str:
        """Categorize action for environmental modifiers"""
        
        if "stealth" in action.required_skills:
            return "stealth"
        elif "magic" in action.required_skills:
            return "magic"
        elif action.action_type == "environmental":
            return "environmental"
        elif "ranged" in action.name.lower():
            return "ranged"
        else:
            return "melee"
    
    def _generate_success_narrative(self, action: CombatAction, approach: str) -> str:
        """Generate narrative for successful action"""
        
        base_narrative = random.choice(action.success_narrative) if action.success_narrative else "succeeds"
        
        # Add environmental context
        if self.active_encounter and action.environmental_narrative:
            env_narratives = action.environmental_narrative.get(self.active_encounter.environment_type.value, [])
            if env_narratives:
                env_narrative = random.choice(env_narratives)
                return f"{base_narrative} - {env_narrative}"
        
        # Add approach flavor
        approach_flavors = {
            "aggressive": " with fierce determination",
            "defensive": " while maintaining careful guard",
            "tactical": " with calculated precision",
            "reckless": " with wild abandon"
        }
        
        flavor = approach_flavors.get(approach, "")
        return base_narrative + flavor
    
    def _generate_failure_narrative(self, action: CombatAction, approach: str) -> str:
        """Generate narrative for failed action"""
        
        base_narrative = random.choice(action.failure_narrative) if action.failure_narrative else "fails"
        
        # Add approach-specific failure reasons
        approach_failures = {
            "aggressive": " due to overcommitment",
            "defensive": " while being too cautious",
            "tactical": " as the plan doesn't unfold as expected",
            "reckless": " from lack of proper preparation"
        }
        
        failure_reason = approach_failures.get(approach, "")
        return base_narrative + failure_reason
    
    def _apply_positioning_effects(self, effects: Dict[str, Any]):
        """Apply positioning effects to current combat state"""
        
        if not self.active_encounter:
            return
        
        # Update player position based on effects
        player_pos = self.active_encounter.player_position
        
        if "cover_bonus" in effects:
            player_pos.cover_level += effects["cover_bonus"]
        
        if "height_advantage" in effects:
            player_pos.elevation += effects["height_advantage"]
        
        if "mobility_penalty" in effects:
            player_pos.mobility_restriction += effects["mobility_penalty"]
    
    def _apply_environmental_changes(self, changes: List[str]):
        """Apply environmental changes to the battlefield"""
        
        if not self.active_encounter:
            return
        
        for change in changes:
            self.active_encounter.environmental_changes.append(change)
            
            # Remove destroyed features
            if change == "feature_destroyed":
                # Find and remove a random destructible feature
                destructible_features = [
                    k for k, v in self.active_encounter.environmental_features.items()
                    if v.destructible
                ]
                if destructible_features:
                    feature_to_remove = random.choice(destructible_features)
                    destroyed_feature = self.active_encounter.environmental_features.pop(feature_to_remove)
                    
                    # Apply destruction effects
                    for effect in destroyed_feature.destruction_effects:
                        self.active_encounter.environmental_changes.append(effect)
    
    def _check_dynamic_events(self) -> List[Dict[str, Any]]:
        """Check for dynamic events during combat"""
        
        events = []
        
        if not self.active_encounter:
            return events
        
        # Environmental events based on turn count
        if self.active_encounter.turn_count == 3:
            if self.active_encounter.environment_type == EnvironmentType.FOREST:
                events.append({
                    "type": "environmental",
                    "description": "A wild animal, startled by the combat, crashes through the undergrowth!",
                    "effect": "distraction"
                })
        
        if self.active_encounter.turn_count == 5:
            events.append({
                "type": "reinforcements",
                "description": "Additional combatants arrive on the scene!",
                "effect": "new_participants"
            })
        
        # Random environmental events
        if random.random() < 0.1:  # 10% chance per turn
            environmental_events = {
                EnvironmentType.FOREST: ["sudden_fog", "falling_branch", "animal_distraction"],
                EnvironmentType.URBAN: ["crowd_gathers", "city_guard_patrol", "merchant_interruption"],
                EnvironmentType.DUNGEON: ["magical_surge", "structural_collapse", "ancient_trap_triggers"]
            }
            
            possible_events = environmental_events.get(self.active_encounter.environment_type, [])
            if possible_events:
                event_type = random.choice(possible_events)
                events.append({
                    "type": "random_environmental",
                    "description": f"Unexpected event: {event_type.replace('_', ' ')}",
                    "effect": event_type
                })
        
        return events
    
    def _roll_damage(self, dice_string: str, bonus: int) -> int:
        """Roll damage dice and apply bonus"""
        
        # Simple dice rolling - parse dice string like "2d6"
        if 'd' not in dice_string:
            return bonus
        
        parts = dice_string.split('d')
        num_dice = int(parts[0])
        die_size = int(parts[1])
        
        total = sum(random.randint(1, die_size) for _ in range(num_dice))
        return total + bonus
    
    def _get_battlefield_description(self, encounter: CombatEncounter) -> Dict[str, Any]:
        """Get description of current battlefield state"""
        
        return {
            "size": encounter.battlefield_size,
            "environment": encounter.environment_type.value,
            "features": [
                {
                    "name": feature.name,
                    "description": feature.description,
                    "position": key.split('_')[-2:]  # Extract x, y from key
                }
                for key, feature in encounter.environmental_features.items()
            ],
            "player_position": {
                "x": encounter.player_position.x,
                "y": encounter.player_position.y,
                "cover": encounter.player_position.cover_level,
                "elevation": encounter.player_position.elevation
            },
            "environmental_changes": encounter.environmental_changes
        }
    
    def get_available_actions(
        self,
        player_skills: Dict[str, int],
        current_position: Optional[Tuple[int, int]] = None
    ) -> List[Dict[str, Any]]:
        """Get list of available combat actions for current situation"""
        
        available_actions = []
        
        for action_id, action in self.combat_actions.items():
            # Check skill requirements
            requirements_met = all(
                player_skills.get(skill, 0) >= required_level
                for skill, required_level in action.required_skills.items()
            )
            
            if requirements_met:
                available_actions.append({
                    "id": action_id,
                    "name": action.name,
                    "description": action.description,
                    "type": action.action_type,
                    "requirements": action.required_skills,
                    "estimated_success": self._calculate_action_success(action, player_skills, "standard")
                })
        
        return available_actions
    
    def get_combat_status(self) -> Dict[str, Any]:
        """Get current combat status and state"""
        
        if not self.active_encounter:
            return {"status": "no_active_combat"}
        
        encounter = self.active_encounter
        
        return {
            "status": "combat_active",
            "encounter_id": encounter.id,
            "title": encounter.title,
            "turn_count": encounter.turn_count,
            "objectives": {
                "primary": encounter.primary_objective,
                "secondary": encounter.secondary_objectives,
                "completed": []  # Would track completed objectives
            },
            "battlefield": self._get_battlefield_description(encounter),
            "recent_events": encounter.narrative_beats[-5:] if encounter.narrative_beats else [],
            "environmental_changes": encounter.environmental_changes
        }
    
    def resolve_combat(self, outcome: str, narrative: str = "") -> Dict[str, Any]:
        """Resolve the current combat encounter"""
        
        if not self.active_encounter:
            return {"error": "No active combat to resolve"}
        
        encounter = self.active_encounter
        
        # Record combat in history
        combat_record = {
            "encounter_id": encounter.id,
            "title": encounter.title,
            "outcome": outcome,
            "turns_taken": encounter.turn_count,
            "environment": encounter.environment_type.value,
            "narrative": narrative,
            "timestamp": datetime.now().isoformat()
        }
        
        self.combat_history.append(combat_record)
        
        # Clear active encounter
        self.active_encounter = None
        
        return {
            "combat_resolved": True,
            "outcome": outcome,
            "encounter_summary": combat_record,
            "experience_gained": self._calculate_experience_gain(encounter, outcome),
            "narrative_conclusion": narrative or f"The {encounter.title.lower()} concludes with {outcome}."
        }
    
    def _calculate_experience_gain(self, encounter: CombatEncounter, outcome: str) -> Dict[str, int]:
        """Calculate experience gained from combat"""
        
        base_experience = 100
        
        # Outcome modifiers
        outcome_multipliers = {
            "victory": 1.0,
            "tactical_victory": 1.2,
            "pyrrhic_victory": 0.8,
            "defeat": 0.3,
            "escape": 0.5
        }
        
        multiplier = outcome_multipliers.get(outcome, 1.0)
        
        # Turn efficiency bonus
        efficiency_bonus = max(0, (20 - encounter.turn_count) * 5)
        
        total_experience = int((base_experience * multiplier) + efficiency_bonus)
        
        return {
            "combat_experience": total_experience,
            "tactical_experience": encounter.turn_count * 2,
            "environmental_experience": len(encounter.environmental_changes) * 5
        } 