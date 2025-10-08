"""
Political System for The Northern Realms
========================================

Kingdom-scale consequences and political intrigue featuring:
- Three kingdom relationships and alliances
- Player reputation across kingdoms
- Political events and consequences
- Faction politics and power struggles
- Diplomatic choices and their ripple effects

Design Philosophy:
- Player choices should affect entire kingdoms
- Alliances should be dynamic and fragile
- Political decisions should have long-term consequences
- Betrayal and loyalty should be meaningful
- Kingdom stability should affect gameplay
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class KingdomStatus(Enum):
    """Kingdom political stability"""
    STABLE = "stable"              # Peaceful and prosperous
    UNREST = "unrest"              # Growing discontent
    TURMOIL = "turmoil"            # Political instability
    CHAOS = "chaos"               # Complete breakdown
    WAR = "war"                   # Active warfare


class DiplomaticRelation(Enum):
    """Relations between kingdoms"""
    ALLIED = "allied"              # Strong alliance
    FRIENDLY = "friendly"          # Cooperative
    NEUTRAL = "neutral"            # No strong feelings
    TENSE = "tense"               # Suspicious
    HOSTILE = "hostile"           # Open hostility
    AT_WAR = "at_war"             # Active warfare


class PoliticalEventType(Enum):
    """Types of political events"""
    ALLIANCE_FORMATION = "alliance_formation"
    BETRAYAL = "betrayal"
    ASSASSINATION = "assassination"
    TRADE_DISPUTE = "trade_dispute"
    BORDER_CLASH = "border_clash"
    NOBLE_INTRIGUE = "noble_intrigue"
    DRAGON_ATTACK = "dragon_attack"


@dataclass
class KingdomState:
    """
    Complete state of a kingdom
    
    Tracks:
    - Political stability
    - Resources and military strength
    - Relations with other kingdoms
    - Internal factions and power struggles
    """
    kingdom_id: str
    name: str
    ruler: str
    status: KingdomStatus = KingdomStatus.STABLE
    
    # Resources
    treasury: int = 1000
    military_strength: int = 50
    population_loyalty: int = 70  # 0-100
    
    # Relations with other kingdoms
    relations: Dict[str, DiplomaticRelation] = field(default_factory=dict)
    
    # Internal politics
    noble_houses: Dict[str, int] = field(default_factory=dict)  # House name -> influence
    active_factions: List[str] = field(default_factory=list)
    
    # Player relationships
    player_reputation: int = 0
    player_alliance: bool = False
    
    def get_stability_score(self) -> int:
        """Calculate overall stability (0-100)"""
        base_stability = {
            KingdomStatus.STABLE: 80,
            KingdomStatus.UNREST: 50,
            KingdomStatus.TURMOIL: 30,
            KingdomStatus.CHAOS: 10,
            KingdomStatus.WAR: 5
        }.get(self.status, 50)
        
        # Modifiers
        loyalty_modifier = self.population_loyalty // 10
        treasury_modifier = min(20, self.treasury // 100)
        
        return min(100, base_stability + loyalty_modifier + treasury_modifier)
    
    def can_ally_with_player(self) -> bool:
        """Check if kingdom can form alliance with player"""
        return (
            self.player_reputation >= 20 and
            self.status != KingdomStatus.WAR and
            not self.player_alliance
        )
    
    def should_declare_war(self) -> bool:
        """Check if kingdom should declare war"""
        return (
            self.player_reputation <= -20 or
            self.status == KingdomStatus.CHAOS or
            random.random() < 0.1  # Small chance of random war
        )


@dataclass
class PoliticalEvent:
    """
    Political event that affects kingdoms
    
    Events can be:
    - Triggered by player actions
    - Random occurrences
    - Chain reactions from other events
    """
    event_id: str
    event_type: PoliticalEventType
    title: str
    description: str
    
    # Affected kingdoms
    primary_kingdom: str
    affected_kingdoms: List[str] = field(default_factory=list)
    
    # Effects
    reputation_changes: Dict[str, int] = field(default_factory=dict)
    status_changes: Dict[str, KingdomStatus] = field(default_factory=dict)
    relation_changes: Dict[Tuple[str, str], DiplomaticRelation] = field(default_factory=dict)
    
    # Requirements
    trigger_conditions: Dict[str, any] = field(default_factory=dict)
    
    # Duration and consequences
    duration_turns: int = 0  # 0 = permanent
    chain_events: List[str] = field(default_factory=list)  # Events this can trigger
    
    def can_trigger(self, game_state: Dict) -> bool:
        """Check if event can trigger"""
        for condition, required_value in self.trigger_conditions.items():
            if game_state.get(condition) != required_value:
                return False
        return True


class PoliticalEngine:
    """
    Political system engine for The Northern Realms
    
    Manages:
    - Kingdom relationships and alliances
    - Political events and consequences
    - Player reputation across kingdoms
    - Diplomatic choices and their effects
    """
    
    def __init__(self):
        self.kingdoms: Dict[str, KingdomState] = {}
        self.political_events: Dict[str, PoliticalEvent] = {}
        self.event_history: List[str] = []
        self._initialize_political_system()
    
    def _initialize_political_system(self):
        """Initialize complete political system"""
        
        # ========================================================================
        # KINGDOM DEFINITIONS
        # ========================================================================
        
        # Ironhold Kingdom
        ironhold = KingdomState(
            kingdom_id="ironhold",
            name="Ironhold",
            ruler="King Alaric Ironhold",
            treasury=1500,
            military_strength=70,
            population_loyalty=75,
            noble_houses={
                "House Ironfist": 30,
                "House Steelcrown": 25,
                "House Dragonheart": 20,
                "House Shadowblade": 15,
                "House Goldcoin": 10
            },
            active_factions=["traditionalists", "modernists", "dragon_cult"]
        )
        
        # Stormwatch Kingdom
        stormwatch = KingdomState(
            kingdom_id="stormwatch",
            name="Stormwatch",
            ruler="Queen Elara Stormwatch",
            treasury=1200,
            military_strength=60,
            population_loyalty=65,
            noble_houses={
                "House Stormrider": 35,
                "House Wavebreaker": 25,
                "House Thunderclap": 20,
                "House Mistwalker": 15,
                "House Seafarer": 5
            },
            active_factions=["naval_supremacists", "merchant_guild", "isolationists"]
        )
        
        # Frostmere Kingdom
        frostmere = KingdomState(
            kingdom_id="frostmere",
            name="Frostmere",
            ruler="Archmage Lirian Frostmere",
            treasury=800,
            military_strength=45,
            population_loyalty=80,
            noble_houses={
                "House Frostweaver": 40,
                "House Crystaleye": 25,
                "House Winterborn": 20,
                "House Iceheart": 10,
                "House Snowdrift": 5
            },
            active_factions=["arcane_supremacists", "researchers", "traditional_mages"]
        )
        
        self.kingdoms = {
            "ironhold": ironhold,
            "stormwatch": stormwatch,
            "frostmere": frostmere
        }
        
        # Initialize relations (neutral by default)
        for kingdom1 in self.kingdoms:
            for kingdom2 in self.kingdoms:
                if kingdom1 != kingdom2:
                    self.kingdoms[kingdom1].relations[kingdom2] = DiplomaticRelation.NEUTRAL
                    self.kingdoms[kingdom2].relations[kingdom1] = DiplomaticRelation.NEUTRAL
        
        # ========================================================================
        # POLITICAL EVENTS
        # ========================================================================
        
        # Alliance Formation Event
        alliance_event = PoliticalEvent(
            event_id="ironhold_stormwatch_alliance",
            event_type=PoliticalEventType.ALLIANCE_FORMATION,
            title="Ironhold-Stormwatch Alliance",
            description=(
                "King Alaric and Queen Elara have formed a historic alliance. "
                "Combined naval and land forces create a formidable defense against dragon threats."
            ),
            primary_kingdom="ironhold",
            affected_kingdoms=["stormwatch"],
            reputation_changes={"ironhold": 10, "stormwatch": 10, "frostmere": -5},
            relation_changes={
                ("ironhold", "stormwatch"): DiplomaticRelation.ALLIED,
                ("stormwatch", "ironhold"): DiplomaticRelation.ALLIED
            },
            trigger_conditions={"player_reputation_ironhold": ">=20", "dragon_threat_level": "high"}
        )
        
        # Betrayal Event
        betrayal_event = PoliticalEvent(
            event_id="stormwatch_betrayal",
            event_type=PoliticalEventType.BETRAYAL,
            title="Stormwatch Betrayal",
            description=(
                "Queen Elara's advisors have convinced her to abandon the alliance. "
                "Stormwatch withdraws its naval support, leaving Ironhold exposed."
            ),
            primary_kingdom="stormwatch",
            affected_kingdoms=["ironhold"],
            reputation_changes={"stormwatch": -15, "ironhold": -10},
            relation_changes={
                ("stormwatch", "ironhold"): DiplomaticRelation.HOSTILE,
                ("ironhold", "stormwatch"): DiplomaticRelation.TENSE
            },
            trigger_conditions={"player_reputation_stormwatch": "<= -10"}
        )
        
        # Dragon Attack Event
        dragon_attack_event = PoliticalEvent(
            event_id="dragon_attack_frostmere",
            event_type=PoliticalEventType.DRAGON_ATTACK,
            title="Dragon Assault on Frostmere",
            description=(
                "An ancient frost dragon attacks Frostmere Citadel. "
                "The mages' magical defenses are tested to their limits."
            ),
            primary_kingdom="frostmere",
            affected_kingdoms=["ironhold", "stormwatch"],
            reputation_changes={"frostmere": -20, "ironhold": -5, "stormwatch": -5},
            status_changes={"frostmere": KingdomStatus.UNREST},
            trigger_conditions={"dragon_activity": "high"}
        )
        
        self.political_events = {
            "ironhold_stormwatch_alliance": alliance_event,
            "stormwatch_betrayal": betrayal_event,
            "dragon_attack_frostmere": dragon_attack_event
        }
    
    def get_kingdom(self, kingdom_id: str) -> Optional[KingdomState]:
        """Get kingdom by ID"""
        return self.kingdoms.get(kingdom_id)
    
    def get_player_reputation(self, kingdom_id: str) -> int:
        """Get player's reputation in a kingdom"""
        kingdom = self.get_kingdom(kingdom_id)
        return kingdom.player_reputation if kingdom else 0
    
    def update_player_reputation(self, kingdom_id: str, change: int):
        """Update player's reputation in a kingdom"""
        kingdom = self.get_kingdom(kingdom_id)
        if kingdom:
            kingdom.player_reputation += change
            kingdom.player_reputation = max(-50, min(50, kingdom.player_reputation))  # Cap at -50 to 50
    
    def form_alliance(self, kingdom_id: str) -> Dict[str, any]:
        """Form alliance with a kingdom"""
        kingdom = self.get_kingdom(kingdom_id)
        if not kingdom:
            return {"success": False, "error": "Kingdom not found"}
        
        if not kingdom.can_ally_with_player():
            return {"success": False, "error": "Cannot form alliance - insufficient reputation or already allied"}
        
        kingdom.player_alliance = True
        
        # Update relations with other kingdoms
        for other_kingdom_id in self.kingdoms:
            if other_kingdom_id != kingdom_id:
                self.kingdoms[other_kingdom_id].relations[kingdom_id] = DiplomaticRelation.FRIENDLY
                kingdom.relations[other_kingdom_id] = DiplomaticRelation.FRIENDLY
        
        return {
            "success": True,
            "message": f"Alliance formed with {kingdom.name}!",
            "benefits": [
                "Military support in combat",
                "Trade benefits",
                "Information sharing",
                "Political influence"
            ]
        }
    
    def process_political_events(self, game_state: Dict) -> List[Dict[str, any]]:
        """Process and trigger political events"""
        triggered_events = []
        
        for event in self.political_events.values():
            if event.can_trigger(game_state) and event.event_id not in self.event_history:
                # Trigger the event
                triggered_events.append(self._trigger_political_event(event))
                self.event_history.append(event.event_id)
        
        return triggered_events
    
    def _trigger_political_event(self, event: PoliticalEvent) -> Dict[str, any]:
        """Trigger a political event and apply its effects"""
        
        # Apply reputation changes
        for kingdom_id, change in event.reputation_changes.items():
            self.update_player_reputation(kingdom_id, change)
        
        # Apply status changes
        for kingdom_id, new_status in event.status_changes.items():
            kingdom = self.get_kingdom(kingdom_id)
            if kingdom:
                kingdom.status = new_status
        
        # Apply relation changes
        for (kingdom1, kingdom2), new_relation in event.relation_changes.items():
            if kingdom1 in self.kingdoms and kingdom2 in self.kingdoms:
                self.kingdoms[kingdom1].relations[kingdom2] = new_relation
                self.kingdoms[kingdom2].relations[kingdom1] = new_relation
        
        return {
            "event_id": event.event_id,
            "title": event.title,
            "description": event.description,
            "affected_kingdoms": event.affected_kingdoms,
            "effects": {
                "reputation_changes": event.reputation_changes,
                "status_changes": {k: v.value for k, v in event.status_changes.items()},
                "relation_changes": {f"{k1}-{k2}": v.value for (k1, k2), v in event.relation_changes.items()}
            }
        }
    
    def get_kingdom_relations_summary(self) -> Dict[str, any]:
        """Get summary of all kingdom relations"""
        summary = {}
        
        for kingdom in self.kingdoms.values():
            summary[kingdom.kingdom_id] = {
                "name": kingdom.name,
                "status": kingdom.status.value,
                "stability": kingdom.get_stability_score(),
                "relations": {k: v.value for k, v in kingdom.relations.items()},
                "player_reputation": kingdom.player_reputation,
                "player_alliance": kingdom.player_alliance,
                "resources": {
                    "treasury": kingdom.treasury,
                    "military": kingdom.military_strength,
                    "loyalty": kingdom.population_loyalty
                }
            }
        
        return summary
    
    def calculate_diplomatic_difficulty(self, from_kingdom: str, to_kingdom: str) -> int:
        """Calculate difficulty for diplomatic actions between kingdoms"""
        kingdom1 = self.get_kingdom(from_kingdom)
        kingdom2 = self.get_kingdom(to_kingdom)
        
        if not kingdom1 or not kingdom2:
            return 50  # Neutral difficulty
        
        relation = kingdom1.relations.get(to_kingdom, DiplomaticRelation.NEUTRAL)
        
        # Base difficulty by relation
        difficulty_modifiers = {
            DiplomaticRelation.ALLIED: -20,
            DiplomaticRelation.FRIENDLY: -10,
            DiplomaticRelation.NEUTRAL: 0,
            DiplomaticRelation.TENSE: 10,
            DiplomaticRelation.HOSTILE: 20,
            DiplomaticRelation.AT_WAR: 30
        }
        
        base_difficulty = 50 + difficulty_modifiers.get(relation, 0)
        
        # Adjust by kingdom stability
        stability_modifier = (100 - kingdom2.get_stability_score()) // 10
        
        return min(90, max(10, base_difficulty + stability_modifier))


# ============================================================================
# DIPLOMATIC ACTIONS
# ============================================================================

class DiplomaticActions:
    """Available diplomatic actions player can take"""
    
    @staticmethod
    def negotiate_trade_agreement(kingdom1: str, kingdom2: str) -> Dict[str, any]:
        """Negotiate trade agreement between kingdoms"""
        return {
            "action": "trade_negotiation",
            "description": f"Negotiate trade agreement between {kingdom1} and {kingdom2}",
            "requirements": {"player_reputation_both": ">=10"},
            "effects": {
                "treasury_bonus": "+200 gold per kingdom",
                "relation_improvement": "+5 reputation both kingdoms"
            }
        }
    
    @staticmethod
    def broker_peace_treaty(kingdom1: str, kingdom2: str) -> Dict[str, any]:
        """Broker peace between warring kingdoms"""
        return {
            "action": "peace_treaty",
            "description": f"Broker peace between {kingdom1} and {kingdom2}",
            "requirements": {"player_reputation_both": ">=15", "kingdoms_at_war": True},
            "effects": {
                "end_war": "War ends immediately",
                "relation_reset": "Relations become neutral",
                "player_reputation": "+20 both kingdoms"
            }
        }
    
    @staticmethod
    def expose_political_plot(plot_type: str, target_kingdom: str) -> Dict[str, any]:
        """Expose political conspiracy"""
        return {
            "action": "expose_plot",
            "description": f"Expose {plot_type} in {target_kingdom}",
            "requirements": {"evidence": True, "player_reputation_target": ">=5"},
            "effects": {
                "kingdom_instability": "-20 stability",
                "player_reputation": "+15 in target kingdom",
                "noble_house_changes": "Plotters lose influence"
            }
        }

