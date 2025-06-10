"""
AI-RPG-Alpha: Faction & Politics System

Sophisticated political system with competing factions, diplomatic missions,
espionage networks, political intrigue, and player influence on power dynamics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime


class FactionType(Enum):
    """Types of political factions"""
    ROYAL_GOVERNMENT = "royal_government"
    MERCHANT_GUILD = "merchant_guild"
    RELIGIOUS_ORDER = "religious_order"
    NOBLE_HOUSE = "noble_house"
    REBEL_MOVEMENT = "rebel_movement"
    CRIMINAL_SYNDICATE = "criminal_syndicate"
    MILITARY_ORDER = "military_order"
    SCHOLARLY_INSTITUTION = "scholarly_institution"


class PoliticalAction(Enum):
    """Types of political actions"""
    DIPLOMACY = "diplomacy"
    ESPIONAGE = "espionage"
    MILITARY = "military"
    ECONOMIC = "economic"
    PROPAGANDA = "propaganda"
    SABOTAGE = "sabotage"
    ALLIANCE = "alliance"
    BETRAYAL = "betrayal"


class MissionType(Enum):
    """Types of political missions"""
    DIPLOMATIC_NEGOTIATION = "diplomatic_negotiation"
    SPY_INFILTRATION = "spy_infiltration"
    INTELLIGENCE_GATHERING = "intelligence_gathering"
    SABOTAGE_OPERATION = "sabotage_operation"
    ASSASSINATION_PLOT = "assassination_plot"
    ALLIANCE_BUILDING = "alliance_building"
    PROPAGANDA_CAMPAIGN = "propaganda_campaign"
    RESOURCE_ACQUISITION = "resource_acquisition"


@dataclass
class PoliticalRelationship:
    """Relationship between two factions"""
    faction_a: str
    faction_b: str
    
    # Relationship metrics (-100 to 100)
    trust: int = 0
    trade_relations: int = 0
    military_cooperation: int = 0
    
    # Current status
    relationship_status: str = "neutral"  # ally, enemy, neutral, suspicious, friendly
    treaties: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    
    # Historical context
    relationship_history: List[str] = field(default_factory=list)
    shared_interests: List[str] = field(default_factory=list)
    points_of_contention: List[str] = field(default_factory=list)


@dataclass
class PoliticalMission:
    """A political mission or operation"""
    id: str
    title: str
    description: str
    mission_type: MissionType
    
    # Mission details
    sponsor_faction: str
    target_faction: str
    objective: str
    
    # Requirements
    required_skills: Dict[str, int] = field(default_factory=dict)
    required_reputation: Dict[str, int] = field(default_factory=dict)
    resources_needed: Dict[str, int] = field(default_factory=dict)
    
    # Execution
    difficulty: int = 15
    time_limit: int = 30  # days
    secrecy_level: str = "confidential"  # public, confidential, secret, top_secret
    
    # Consequences
    success_rewards: Dict[str, Any] = field(default_factory=dict)
    failure_consequences: Dict[str, Any] = field(default_factory=dict)
    political_ramifications: Dict[str, int] = field(default_factory=dict)
    
    # Current status
    status: str = "available"  # available, in_progress, completed, failed, cancelled
    progress: float = 0.0
    complications: List[str] = field(default_factory=list)


@dataclass
class SpyNetwork:
    """Espionage network within a faction"""
    faction_id: str
    network_name: str
    
    # Network capabilities
    infiltration_level: Dict[str, int] = field(default_factory=dict)  # faction -> level
    intelligence_quality: int = 5  # 1-10
    operational_security: int = 5  # 1-10
    
    # Assets
    active_agents: List[str] = field(default_factory=list)
    safe_houses: List[str] = field(default_factory=list)
    informants: Dict[str, str] = field(default_factory=dict)  # name -> faction
    
    # Operations
    ongoing_operations: List[str] = field(default_factory=list)
    completed_operations: List[str] = field(default_factory=list)
    
    # Intelligence
    gathered_intelligence: Dict[str, List[str]] = field(default_factory=dict)
    faction_secrets: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class Faction:
    """A political faction with goals, resources, and relationships"""
    id: str
    name: str
    faction_type: FactionType
    
    # Basic info
    description: str
    leadership: str
    headquarters: str
    founded_year: int = 1400
    
    # Power and influence
    military_strength: int = 50  # 1-100
    economic_power: int = 50    # 1-100
    political_influence: int = 50  # 1-100
    popular_support: int = 50   # 1-100
    
    # Resources
    treasury: int = 10000
    territory_control: List[str] = field(default_factory=list)
    strategic_resources: List[str] = field(default_factory=list)
    
    # Goals and ideology
    primary_goals: List[str] = field(default_factory=list)
    secondary_goals: List[str] = field(default_factory=list)
    core_beliefs: List[str] = field(default_factory=list)
    
    # Relationships
    player_reputation: int = 0  # -100 to 100
    
    # Capabilities
    spy_network: Optional[SpyNetwork] = None
    diplomatic_corps: List[str] = field(default_factory=list)
    military_units: List[str] = field(default_factory=list)
    
    # Current state
    current_agenda: List[str] = field(default_factory=list)
    recent_actions: List[str] = field(default_factory=list)
    active_plots: List[str] = field(default_factory=list)


class PoliticalSystem:
    """Advanced faction and politics management system"""
    
    def __init__(self):
        self.factions: Dict[str, Faction] = {}
        self.relationships: Dict[str, PoliticalRelationship] = {}
        self.missions: Dict[str, PoliticalMission] = {}
        self.political_events: List[Dict[str, Any]] = []
        
        self.faction_templates = self._initialize_faction_templates()
        self.mission_templates = self._initialize_mission_templates()
        self.political_scenarios = self._initialize_political_scenarios()
        
        self._create_default_factions()
        self._establish_initial_relationships()
    
    def _initialize_faction_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize faction templates"""
        
        return {
            "royal_crown": {
                "name": "The Royal Crown",
                "type": FactionType.ROYAL_GOVERNMENT,
                "description": "The traditional monarchy seeking to maintain order and stability",
                "leadership": "King Aldric the Just",
                "headquarters": "royal_palace",
                "military_strength": 80,
                "economic_power": 70,
                "political_influence": 90,
                "popular_support": 60,
                "primary_goals": ["maintain_royal_authority", "preserve_stability", "expand_territory"],
                "secondary_goals": ["improve_trade", "strengthen_military", "suppress_rebellion"],
                "core_beliefs": ["divine_right_of_kings", "order_over_chaos", "traditional_values"],
                "territory_control": ["royal_capital", "northern_provinces", "eastern_fortresses"],
                "strategic_resources": ["royal_treasury", "standing_army", "noble_loyalty"]
            },
            "merchant_guilds": {
                "name": "United Merchant Guilds",
                "type": FactionType.MERCHANT_GUILD,
                "description": "Powerful trading consortiums seeking economic freedom and profit",
                "leadership": "Guildmaster Helena Goldweaver",
                "headquarters": "trading_post",
                "military_strength": 30,
                "economic_power": 95,
                "political_influence": 60,
                "popular_support": 70,
                "primary_goals": ["free_trade", "reduce_taxation", "expand_trade_routes"],
                "secondary_goals": ["weaken_royal_monopolies", "establish_merchant_courts", "fund_exploration"],
                "core_beliefs": ["economic_freedom", "merit_over_birth", "prosperity_through_trade"],
                "territory_control": ["trading_post", "merchant_quarter", "trade_routes"],
                "strategic_resources": ["vast_wealth", "trade_networks", "information_brokers"]
            },
            "order_of_dawn": {
                "name": "Order of the Dawn",
                "type": FactionType.RELIGIOUS_ORDER,
                "description": "Holy order dedicated to bringing light and justice to the world",
                "leadership": "High Paladin Seraphina",
                "headquarters": "crystal_sanctum",
                "military_strength": 70,
                "economic_power": 40,
                "political_influence": 50,
                "popular_support": 80,
                "primary_goals": ["spread_divine_light", "fight_corruption", "protect_innocents"],
                "secondary_goals": ["build_temples", "train_paladins", "purify_dark_magic"],
                "core_beliefs": ["divine_justice", "protection_of_weak", "redemption_possible"],
                "territory_control": ["crystal_sanctum", "holy_sites", "temple_towns"],
                "strategic_resources": ["divine_magic", "devoted_followers", "moral_authority"]
            },
            "shadow_covenant": {
                "name": "Shadow Covenant",
                "type": FactionType.CRIMINAL_SYNDICATE,
                "description": "Secretive criminal organization with fingers in every dark deal",
                "leadership": "The Hooded Council",
                "headquarters": "hidden_underground",
                "military_strength": 50,
                "economic_power": 60,
                "political_influence": 40,
                "popular_support": 20,
                "primary_goals": ["accumulate_power", "control_underworld", "eliminate_rivals"],
                "secondary_goals": ["corrupt_officials", "expand_operations", "acquire_forbidden_knowledge"],
                "core_beliefs": ["power_through_shadow", "ends_justify_means", "weakness_is_death"],
                "territory_control": ["underground_networks", "criminal_districts", "smuggling_routes"],
                "strategic_resources": ["blackmail_material", "assassins", "forbidden_magic"]
            },
            "peoples_liberation": {
                "name": "People's Liberation Front",
                "type": FactionType.REBEL_MOVEMENT,
                "description": "Revolutionary movement fighting for the common people's rights",
                "leadership": "Commander Elena Stormheart",
                "headquarters": "hidden_camps",
                "military_strength": 40,
                "economic_power": 20,
                "political_influence": 30,
                "popular_support": 85,
                "primary_goals": ["overthrow_monarchy", "establish_republic", "redistribute_wealth"],
                "secondary_goals": ["recruit_supporters", "sabotage_royal_forces", "gain_foreign_support"],
                "core_beliefs": ["power_to_people", "equality_for_all", "revolution_necessary"],
                "territory_control": ["rebel_strongholds", "sympathetic_villages", "forest_hideouts"],
                "strategic_resources": ["popular_support", "guerrilla_tactics", "passionate_fighters"]
            },
            "house_ravencrest": {
                "name": "House Ravencrest",
                "type": FactionType.NOBLE_HOUSE,
                "description": "Ancient noble house with ambitions for the throne",
                "leadership": "Duke Maximilian Ravencrest",
                "headquarters": "ravencrest_manor",
                "military_strength": 60,
                "economic_power": 75,
                "political_influence": 70,
                "popular_support": 40,
                "primary_goals": ["claim_throne", "restore_family_honor", "expand_influence"],
                "secondary_goals": ["weaken_current_king", "build_alliances", "eliminate_rivals"],
                "core_beliefs": ["noble_superiority", "rightful_inheritance", "strength_through_cunning"],
                "territory_control": ["ravencrest_lands", "allied_noble_estates", "strategic_castles"],
                "strategic_resources": ["ancient_bloodline", "noble_connections", "military_expertise"]
            }
        }
    
    def _create_default_factions(self):
        """Create default factions from templates"""
        
        for faction_id, template in self.faction_templates.items():
            faction = Faction(
                id=faction_id,
                name=template["name"],
                faction_type=template["type"],
                description=template["description"],
                leadership=template["leadership"],
                headquarters=template["headquarters"],
                military_strength=template["military_strength"],
                economic_power=template["economic_power"],
                political_influence=template["political_influence"],
                popular_support=template["popular_support"],
                primary_goals=template["primary_goals"],
                secondary_goals=template["secondary_goals"],
                core_beliefs=template["core_beliefs"],
                territory_control=template["territory_control"],
                strategic_resources=template["strategic_resources"]
            )
            
            # Create spy networks for appropriate factions
            if faction.faction_type in [FactionType.ROYAL_GOVERNMENT, FactionType.CRIMINAL_SYNDICATE, FactionType.NOBLE_HOUSE]:
                faction.spy_network = SpyNetwork(
                    faction_id=faction_id,
                    network_name=f"{faction.name} Intelligence",
                    intelligence_quality=random.randint(5, 8),
                    operational_security=random.randint(4, 7)
                )
            
            self.factions[faction_id] = faction
    
    def _establish_initial_relationships(self):
        """Establish initial relationships between factions"""
        
        # Define natural alliances and rivalries
        relationship_matrix = {
            ("royal_crown", "order_of_dawn"): {"trust": 60, "status": "friendly", "treaties": ["mutual_defense"]},
            ("royal_crown", "merchant_guilds"): {"trust": 30, "status": "neutral", "conflicts": ["taxation_disputes"]},
            ("royal_crown", "shadow_covenant"): {"trust": -80, "status": "enemy", "conflicts": ["law_and_order"]},
            ("royal_crown", "peoples_liberation"): {"trust": -70, "status": "enemy", "conflicts": ["revolutionary_war"]},
            ("royal_crown", "house_ravencrest"): {"trust": -40, "status": "suspicious", "conflicts": ["succession_dispute"]},
            
            ("merchant_guilds", "order_of_dawn"): {"trust": 20, "status": "neutral", "shared_interests": ["trade_protection"]},
            ("merchant_guilds", "shadow_covenant"): {"trust": -30, "status": "suspicious", "conflicts": ["protection_rackets"]},
            ("merchant_guilds", "peoples_liberation"): {"trust": -20, "status": "suspicious", "conflicts": ["wealth_redistribution"]},
            ("merchant_guilds", "house_ravencrest"): {"trust": 40, "status": "friendly", "shared_interests": ["economic_growth"]},
            
            ("order_of_dawn", "shadow_covenant"): {"trust": -90, "status": "enemy", "conflicts": ["light_vs_shadow"]},
            ("order_of_dawn", "peoples_liberation"): {"trust": 10, "status": "neutral", "shared_interests": ["helping_poor"]},
            ("order_of_dawn", "house_ravencrest"): {"trust": 20, "status": "neutral"},
            
            ("shadow_covenant", "peoples_liberation"): {"trust": -50, "status": "enemy", "conflicts": ["competing_underground"]},
            ("shadow_covenant", "house_ravencrest"): {"trust": 30, "status": "neutral", "shared_interests": ["destabilizing_crown"]},
            
            ("peoples_liberation", "house_ravencrest"): {"trust": -60, "status": "enemy", "conflicts": ["class_warfare"]},
        }
        
        for (faction_a, faction_b), relationship_data in relationship_matrix.items():
            rel_id = f"{faction_a}_{faction_b}"
            
            relationship = PoliticalRelationship(
                faction_a=faction_a,
                faction_b=faction_b,
                trust=relationship_data.get("trust", 0),
                relationship_status=relationship_data.get("status", "neutral"),
                treaties=relationship_data.get("treaties", []),
                conflicts=relationship_data.get("conflicts", []),
                shared_interests=relationship_data.get("shared_interests", [])
            )
            
            self.relationships[rel_id] = relationship
    
    def _initialize_mission_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mission templates"""
        
        return {
            "diplomatic_summit": {
                "title": "Diplomatic Summit",
                "type": MissionType.DIPLOMATIC_NEGOTIATION,
                "description": "Negotiate a peace treaty between warring factions",
                "required_skills": {"diplomacy": 7, "etiquette": 5},
                "difficulty": 15,
                "rewards": {"reputation": 20, "gold": 1000, "political_favor": "treaty_broker"},
                "complications": ["assassination_attempt", "sabotage", "information_leak"]
            },
            "spy_infiltration": {
                "title": "Deep Cover Operation",
                "type": MissionType.SPY_INFILTRATION,
                "description": "Infiltrate rival faction to gather intelligence",
                "required_skills": {"stealth": 8, "deception": 7, "investigation": 6},
                "difficulty": 18,
                "secrecy_level": "top_secret",
                "rewards": {"secret_information": True, "reputation": 15, "spy_contacts": 3},
                "complications": ["blown_cover", "double_agent", "ethical_dilemma"]
            },
            "sabotage_mission": {
                "title": "Strategic Sabotage",
                "type": MissionType.SABOTAGE_OPERATION,
                "description": "Disrupt enemy operations without being detected",
                "required_skills": {"stealth": 8, "explosives": 6, "planning": 7},
                "difficulty": 16,
                "secrecy_level": "secret",
                "rewards": {"enemy_weakened": True, "reputation": 10, "equipment": "advanced_tools"},
                "complications": ["civilian_casualties", "evidence_left_behind", "mission_escalation"]
            },
            "alliance_building": {
                "title": "Alliance Negotiations",
                "type": MissionType.ALLIANCE_BUILDING,
                "description": "Build alliance between compatible factions",
                "required_skills": {"diplomacy": 6, "persuasion": 7, "politics": 5},
                "difficulty": 14,
                "rewards": {"political_influence": 25, "new_allies": True, "trade_benefits": 500},
                "complications": ["rival_interference", "internal_opposition", "changing_demands"]
            }
        }
    
    def _initialize_political_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Initialize dynamic political scenarios"""
        
        return {
            "succession_crisis": {
                "trigger": "royal_leader_death",
                "description": "The death of a faction leader creates a power vacuum",
                "participants": ["royal_crown", "house_ravencrest", "peoples_liberation"],
                "duration": 60,  # days
                "consequences": {
                    "power_shifts": {"royal_crown": -20, "house_ravencrest": 15, "peoples_liberation": 10},
                    "new_missions": ["support_succession", "prevent_civil_war", "seize_opportunity"]
                }
            },
            "trade_war": {
                "trigger": "economic_dispute",
                "description": "Economic sanctions escalate into trade warfare",
                "participants": ["merchant_guilds", "royal_crown"],
                "duration": 45,
                "consequences": {
                    "economic_effects": {"market_instability": True, "price_changes": {"all": 1.2}},
                    "new_missions": ["negotiate_trade_deal", "economic_espionage", "black_market_operations"]
                }
            },
            "religious_schism": {
                "trigger": "theological_dispute",
                "description": "Religious disagreement splits the faithful",
                "participants": ["order_of_dawn"],
                "duration": 90,
                "consequences": {
                    "faction_split": {"order_of_dawn": ["orthodox_order", "reform_movement"]},
                    "new_missions": ["heal_schism", "choose_side", "exploit_division"]
                }
            }
        }
    
    def process_political_turn(self, days_passed: int) -> Dict[str, Any]:
        """Process political developments over time"""
        
        political_changes = {
            "faction_actions": [],
            "relationship_changes": [],
            "new_missions": [],
            "political_events": [],
            "power_shifts": {}
        }
        
        # Process faction actions
        for faction_id, faction in self.factions.items():
            faction_actions = self._process_faction_turn(faction, days_passed)
            if faction_actions:
                political_changes["faction_actions"].extend(faction_actions)
        
        # Update relationships based on recent actions
        relationship_changes = self._update_faction_relationships()
        political_changes["relationship_changes"] = relationship_changes
        
        # Generate new political missions
        new_missions = self._generate_political_missions()
        political_changes["new_missions"] = new_missions
        
        # Check for major political events
        political_events = self._check_political_events()
        political_changes["political_events"] = political_events
        
        # Calculate power shifts
        power_shifts = self._calculate_power_shifts()
        political_changes["power_shifts"] = power_shifts
        
        return political_changes
    
    def _process_faction_turn(self, faction: Faction, days_passed: int) -> List[Dict[str, Any]]:
        """Process actions for a single faction"""
        
        actions = []
        
        # Factions pursue their goals
        for goal in faction.primary_goals:
            if random.random() < 0.3:  # 30% chance per goal per turn
                action = self._generate_faction_action(faction, goal)
                if action:
                    actions.append(action)
                    faction.recent_actions.append(action["description"])
        
        # Spy networks gather intelligence
        if faction.spy_network:
            intelligence = self._process_spy_network(faction.spy_network)
            if intelligence:
                actions.append({
                    "type": "intelligence_gathering",
                    "faction": faction.name,
                    "description": f"{faction.name} gathers intelligence on rival factions",
                    "intelligence_gained": intelligence
                })
        
        # Resource management
        if random.random() < 0.2:  # 20% chance
            resource_action = self._manage_faction_resources(faction)
            if resource_action:
                actions.append(resource_action)
        
        return actions
    
    def _generate_faction_action(self, faction: Faction, goal: str) -> Optional[Dict[str, Any]]:
        """Generate specific action for faction goal"""
        
        action_templates = {
            "expand_territory": {
                "description": f"{faction.name} moves to expand territorial control",
                "type": "territorial_expansion",
                "effects": {"military_strength": 2, "political_influence": 3}
            },
            "increase_wealth": {
                "description": f"{faction.name} launches economic initiatives",
                "type": "economic_development",
                "effects": {"economic_power": 3, "treasury": 1000}
            },
            "build_alliances": {
                "description": f"{faction.name} seeks new political allies",
                "type": "diplomatic_outreach",
                "effects": {"political_influence": 2}
            },
            "weaken_enemies": {
                "description": f"{faction.name} moves against their enemies",
                "type": "hostile_action",
                "effects": {"enemy_weakening": True}
            },
            "maintain_order": {
                "description": f"{faction.name} enforces law and order in their territory",
                "type": "law_enforcement",
                "effects": {"popular_support": 2, "stability": 3}
            }
        }
        
        # Map goals to actions
        goal_to_action = {
            "expand_territory": "expand_territory",
            "accumulate_power": "weaken_enemies",
            "free_trade": "increase_wealth",
            "maintain_royal_authority": "maintain_order",
            "spread_divine_light": "build_alliances",
            "overthrow_monarchy": "weaken_enemies"
        }
        
        action_type = goal_to_action.get(goal)
        if not action_type or action_type not in action_templates:
            return None
        
        action = action_templates[action_type].copy()
        action["faction"] = faction.name
        action["goal"] = goal
        
        # Apply effects
        if "effects" in action:
            for effect, value in action["effects"].items():
                if effect == "military_strength":
                    faction.military_strength = min(100, faction.military_strength + value)
                elif effect == "economic_power":
                    faction.economic_power = min(100, faction.economic_power + value)
                elif effect == "political_influence":
                    faction.political_influence = min(100, faction.political_influence + value)
                elif effect == "popular_support":
                    faction.popular_support = min(100, faction.popular_support + value)
                elif effect == "treasury":
                    faction.treasury += value
        
        return action
    
    def _process_spy_network(self, spy_network: SpyNetwork) -> Optional[Dict[str, Any]]:
        """Process spy network activities"""
        
        if random.random() > 0.4:  # 40% chance of intelligence gathering
            return None
        
        # Select target faction
        target_factions = list(self.factions.keys())
        target_faction = random.choice([f for f in target_factions if f != spy_network.faction_id])
        
        # Determine intelligence type
        intelligence_types = [
            "military_movements", "economic_plans", "diplomatic_secrets",
            "internal_conflicts", "future_operations", "resource_locations"
        ]
        
        intelligence_type = random.choice(intelligence_types)
        
        # Store intelligence
        if target_faction not in spy_network.gathered_intelligence:
            spy_network.gathered_intelligence[target_faction] = []
        
        spy_network.gathered_intelligence[target_faction].append(intelligence_type)
        
        return {
            "target": target_faction,
            "intelligence_type": intelligence_type,
            "quality": spy_network.intelligence_quality
        }
    
    def _manage_faction_resources(self, faction: Faction) -> Optional[Dict[str, Any]]:
        """Handle faction resource management"""
        
        resource_actions = []
        
        # Economic investment
        if faction.treasury > 5000 and random.random() < 0.3:
            investment = min(2000, faction.treasury // 4)
            faction.treasury -= investment
            faction.economic_power += 1
            
            resource_actions.append({
                "type": "economic_investment",
                "faction": faction.name,
                "description": f"{faction.name} invests {investment} gold in economic development",
                "investment": investment
            })
        
        # Military recruitment
        if faction.military_strength < 70 and faction.treasury > 3000 and random.random() < 0.25:
            cost = 1500
            faction.treasury -= cost
            faction.military_strength += 3
            
            resource_actions.append({
                "type": "military_recruitment",
                "faction": faction.name,
                "description": f"{faction.name} recruits new military forces",
                "cost": cost
            })
        
        return resource_actions[0] if resource_actions else None
    
    def _update_faction_relationships(self) -> List[Dict[str, Any]]:
        """Update relationships based on recent faction actions"""
        
        relationship_changes = []
        
        for rel_id, relationship in self.relationships.items():
            faction_a = self.factions[relationship.faction_a]
            faction_b = self.factions[relationship.faction_b]
            
            # Check for conflicting actions
            conflicts = set(faction_a.recent_actions) & set(faction_b.recent_actions)
            if conflicts and random.random() < 0.3:
                relationship.trust = max(-100, relationship.trust - 10)
                relationship_changes.append({
                    "factions": [faction_a.name, faction_b.name],
                    "change": "trust_decreased",
                    "reason": "conflicting_actions"
                })
            
            # Natural relationship drift
            if random.random() < 0.1:  # 10% chance
                drift = random.randint(-2, 2)
                relationship.trust = max(-100, min(100, relationship.trust + drift))
                
                if abs(drift) > 0:
                    relationship_changes.append({
                        "factions": [faction_a.name, faction_b.name],
                        "change": "natural_drift",
                        "value": drift
                    })
            
            # Update relationship status based on trust
            if relationship.trust >= 60:
                relationship.relationship_status = "ally"
            elif relationship.trust >= 30:
                relationship.relationship_status = "friendly"
            elif relationship.trust >= -30:
                relationship.relationship_status = "neutral"
            elif relationship.trust >= -60:
                relationship.relationship_status = "suspicious"
            else:
                relationship.relationship_status = "enemy"
        
        return relationship_changes
    
    def _generate_political_missions(self) -> List[PoliticalMission]:
        """Generate new political missions"""
        
        new_missions = []
        
        # Generate missions based on faction relationships and goals
        for faction_id, faction in self.factions.items():
            if random.random() < 0.2:  # 20% chance per faction
                mission = self._create_faction_mission(faction)
                if mission:
                    new_missions.append(mission)
                    self.missions[mission.id] = mission
        
        return new_missions
    
    def _create_faction_mission(self, faction: Faction) -> Optional[PoliticalMission]:
        """Create a mission for a specific faction"""
        
        # Select mission type based on faction type and goals
        mission_preferences = {
            FactionType.ROYAL_GOVERNMENT: [MissionType.DIPLOMATIC_NEGOTIATION, MissionType.INTELLIGENCE_GATHERING],
            FactionType.MERCHANT_GUILD: [MissionType.ALLIANCE_BUILDING, MissionType.RESOURCE_ACQUISITION],
            FactionType.CRIMINAL_SYNDICATE: [MissionType.SPY_INFILTRATION, MissionType.SABOTAGE_OPERATION],
            FactionType.REBEL_MOVEMENT: [MissionType.SABOTAGE_OPERATION, MissionType.PROPAGANDA_CAMPAIGN],
            FactionType.RELIGIOUS_ORDER: [MissionType.ALLIANCE_BUILDING, MissionType.DIPLOMATIC_NEGOTIATION],
            FactionType.NOBLE_HOUSE: [MissionType.SPY_INFILTRATION, MissionType.ALLIANCE_BUILDING]
        }
        
        preferred_types = mission_preferences.get(faction.faction_type, [MissionType.DIPLOMATIC_NEGOTIATION])
        mission_type = random.choice(preferred_types)
        
        # Select target faction
        potential_targets = []
        for rel_id, relationship in self.relationships.items():
            if relationship.faction_a == faction.id:
                potential_targets.append(relationship.faction_b)
            elif relationship.faction_b == faction.id:
                potential_targets.append(relationship.faction_a)
        
        if not potential_targets:
            return None
        
        target_faction = random.choice(potential_targets)
        
        # Create mission based on type
        mission_id = f"{faction.id}_{mission_type.value}_{datetime.now().timestamp()}"
        
        mission_templates = {
            MissionType.DIPLOMATIC_NEGOTIATION: {
                "title": f"Diplomatic Mission to {self.factions[target_faction].name}",
                "description": f"Negotiate with {self.factions[target_faction].name} on behalf of {faction.name}",
                "objective": "improve_relations",
                "difficulty": 14,
                "required_skills": {"diplomacy": 6, "etiquette": 4}
            },
            MissionType.SPY_INFILTRATION: {
                "title": f"Infiltrate {self.factions[target_faction].name}",
                "description": f"Gather intelligence on {self.factions[target_faction].name}'s operations",
                "objective": "gather_intelligence",
                "difficulty": 17,
                "required_skills": {"stealth": 7, "deception": 6}
            },
            MissionType.ALLIANCE_BUILDING: {
                "title": f"Alliance with {self.factions[target_faction].name}",
                "description": f"Build strategic alliance between {faction.name} and {self.factions[target_faction].name}",
                "objective": "create_alliance",
                "difficulty": 15,
                "required_skills": {"diplomacy": 7, "persuasion": 6}
            }
        }
        
        template = mission_templates.get(mission_type)
        if not template:
            return None
        
        mission = PoliticalMission(
            id=mission_id,
            title=template["title"],
            description=template["description"],
            mission_type=mission_type,
            sponsor_faction=faction.id,
            target_faction=target_faction,
            objective=template["objective"],
            difficulty=template["difficulty"],
            required_skills=template["required_skills"]
        )
        
        # Set rewards and consequences
        mission.success_rewards = {
            "reputation": {faction.id: 15, target_faction: 10},
            "gold": random.randint(500, 2000),
            "political_favor": template["objective"]
        }
        
        mission.failure_consequences = {
            "reputation": {faction.id: -10, target_faction: -5},
            "political_tension": {faction.id: 5}
        }
        
        return mission
    
    def _check_political_events(self) -> List[Dict[str, Any]]:
        """Check for major political events"""
        
        events = []
        
        # Check for succession crises
        for faction_id, faction in self.factions.items():
            if faction.faction_type == FactionType.ROYAL_GOVERNMENT and random.random() < 0.02:  # 2% chance
                events.append({
                    "type": "succession_crisis",
                    "faction": faction.name,
                    "description": f"Leadership crisis emerges in {faction.name}",
                    "consequences": {"political_instability": True}
                })
        
        # Check for trade disputes
        merchant_factions = [f for f in self.factions.values() if f.faction_type == FactionType.MERCHANT_GUILD]
        if merchant_factions and random.random() < 0.05:  # 5% chance
            events.append({
                "type": "trade_dispute",
                "description": "Major trade dispute disrupts regional commerce",
                "consequences": {"economic_instability": True}
            })
        
        return events
    
    def _calculate_power_shifts(self) -> Dict[str, Dict[str, int]]:
        """Calculate power shifts between factions"""
        
        power_shifts = {}
        
        for faction_id, faction in self.factions.items():
            current_power = (
                faction.military_strength + 
                faction.economic_power + 
                faction.political_influence + 
                faction.popular_support
            ) / 4
            
            # Store previous power level if not exists
            if not hasattr(faction, 'previous_power'):
                faction.previous_power = current_power
            
            power_change = current_power - faction.previous_power
            
            if abs(power_change) > 2:  # Significant change
                power_shifts[faction_id] = {
                    "previous_power": int(faction.previous_power),
                    "current_power": int(current_power),
                    "change": int(power_change)
                }
            
            faction.previous_power = current_power
        
        return power_shifts
    
    def execute_political_mission(
        self,
        mission_id: str,
        player_skills: Dict[str, int],
        player_reputation: Dict[str, int],
        approach: str = "standard"
    ) -> Dict[str, Any]:
        """Execute a political mission"""
        
        if mission_id not in self.missions:
            return {"error": "Mission not found"}
        
        mission = self.missions[mission_id]
        
        if mission.status != "available":
            return {"error": "Mission not available"}
        
        # Check skill requirements
        skill_check_results = {}
        for skill, required_level in mission.required_skills.items():
            player_level = player_skills.get(skill, 0)
            skill_check_results[skill] = {
                "required": required_level,
                "player_level": player_level,
                "success": player_level >= required_level
            }
        
        # Check reputation requirements
        reputation_check = True
        for faction, required_rep in mission.required_reputation.items():
            if player_reputation.get(faction, 0) < required_rep:
                reputation_check = False
                break
        
        # Calculate success probability
        skill_bonus = sum(1 for check in skill_check_results.values() if check["success"])
        total_skills = len(skill_check_results)
        skill_success_rate = skill_bonus / total_skills if total_skills > 0 else 0.5
        
        reputation_bonus = 0.1 if reputation_check else -0.2
        
        approach_modifiers = {
            "aggressive": {"success": -0.1, "consequences": 1.5},
            "diplomatic": {"success": 0.1, "consequences": 0.8},
            "sneaky": {"success": 0.05, "consequences": 0.6}
        }
        
        approach_mod = approach_modifiers.get(approach, {"success": 0, "consequences": 1.0})
        
        final_success_rate = 0.3 + (skill_success_rate * 0.4) + reputation_bonus + approach_mod["success"]
        final_success_rate = max(0.05, min(0.95, final_success_rate))
        
        # Execute mission
        mission.status = "completed"
        success = random.random() <= final_success_rate
        
        result = {
            "mission_title": mission.title,
            "success": success,
            "approach": approach,
            "skill_checks": skill_check_results,
            "reputation_check": reputation_check,
            "rewards": {},
            "consequences": {},
            "political_impact": {}
        }
        
        if success:
            # Apply success rewards
            result["rewards"] = mission.success_rewards
            
            # Update faction relationships
            sponsor_faction = self.factions[mission.sponsor_faction]
            target_faction = self.factions[mission.target_faction]
            
            sponsor_faction.player_reputation += 15
            target_faction.player_reputation += 5
            
            # Update inter-faction relationship
            rel_key = f"{mission.sponsor_faction}_{mission.target_faction}"
            reverse_key = f"{mission.target_faction}_{mission.sponsor_faction}"
            
            if rel_key in self.relationships:
                self.relationships[rel_key].trust += 10
            elif reverse_key in self.relationships:
                self.relationships[reverse_key].trust += 10
            
            result["political_impact"]["relationship_improved"] = True
        
        else:
            # Apply failure consequences
            result["consequences"] = mission.failure_consequences
            
            # Negative reputation impact
            sponsor_faction = self.factions[mission.sponsor_faction]
            sponsor_faction.player_reputation -= 10
            
            # Potential political complications
            if random.random() < 0.3:
                result["complications"] = ["diplomatic_incident", "intelligence_leak", "faction_anger"]
        
        return result
    
    def get_political_summary(self) -> Dict[str, Any]:
        """Get comprehensive political situation summary"""
        
        faction_summary = {}
        for faction_id, faction in self.factions.items():
            faction_summary[faction_id] = {
                "name": faction.name,
                "type": faction.faction_type.value,
                "power_level": (faction.military_strength + faction.economic_power + 
                               faction.political_influence + faction.popular_support) / 4,
                "player_reputation": faction.player_reputation,
                "recent_actions": faction.recent_actions[-3:],
                "primary_goals": faction.primary_goals
            }
        
        relationship_summary = {}
        for rel_id, relationship in self.relationships.items():
            relationship_summary[rel_id] = {
                "factions": [relationship.faction_a, relationship.faction_b],
                "status": relationship.relationship_status,
                "trust": relationship.trust,
                "treaties": relationship.treaties,
                "conflicts": relationship.conflicts
            }
        
        available_missions = []
        for mission_id, mission in self.missions.items():
            if mission.status == "available":
                available_missions.append({
                    "id": mission_id,
                    "title": mission.title,
                    "sponsor": self.factions[mission.sponsor_faction].name,
                    "target": self.factions[mission.target_faction].name,
                    "type": mission.mission_type.value,
                    "difficulty": mission.difficulty
                })
        
        return {
            "factions": faction_summary,
            "relationships": relationship_summary,
            "available_missions": available_missions,
            "recent_political_events": self.political_events[-5:],
            "political_tension": self._calculate_overall_tension()
        }
    
    def _calculate_overall_tension(self) -> float:
        """Calculate overall political tension in the region"""
        
        total_tension = 0
        relationship_count = 0
        
        for relationship in self.relationships.values():
            if relationship.relationship_status == "enemy":
                total_tension += 0.8
            elif relationship.relationship_status == "suspicious":
                total_tension += 0.4
            elif relationship.relationship_status == "neutral":
                total_tension += 0.2
            
            relationship_count += 1
        
        return total_tension / relationship_count if relationship_count > 0 else 0.0 