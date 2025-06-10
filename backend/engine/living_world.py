"""
AI-RPG-Alpha: Living World System

Dynamic world simulation that creates autonomous events, economic changes,
and evolving world states independent of player actions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random
from datetime import datetime, timedelta


class WorldEventType(Enum):
    """Types of autonomous world events"""
    ECONOMIC = "economic"
    POLITICAL = "political"
    NATURAL = "natural"
    SOCIAL = "social"
    MAGICAL = "magical"
    MILITARY = "military"
    CULTURAL = "cultural"


class EventSeverity(Enum):
    """Severity levels for world events"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"


@dataclass
class WorldEvent:
    """A dynamic world event that affects the game state"""
    id: str
    event_type: WorldEventType
    severity: EventSeverity
    title: str
    description: str
    
    # Geographic impact
    affected_locations: List[str] = field(default_factory=list)
    
    # Economic effects
    price_changes: Dict[str, float] = field(default_factory=dict)  # item -> multiplier
    trade_route_effects: Dict[str, str] = field(default_factory=dict)
    
    # Political effects
    faction_reputation_changes: Dict[str, int] = field(default_factory=dict)
    power_shifts: Dict[str, float] = field(default_factory=dict)
    
    # Social effects
    public_mood_changes: Dict[str, str] = field(default_factory=dict)
    migration_patterns: Dict[str, str] = field(default_factory=dict)
    
    # Narrative effects
    new_quest_opportunities: List[str] = field(default_factory=list)
    changed_character_behaviors: Dict[str, str] = field(default_factory=dict)
    
    # Temporal aspects
    start_time: datetime = field(default_factory=datetime.now)
    duration: int = 7  # days
    recurring: bool = False
    
    # Prerequisites and consequences
    required_conditions: List[str] = field(default_factory=list)
    triggered_events: List[str] = field(default_factory=list)


@dataclass
class EconomicMarket:
    """Dynamic economic market with supply/demand"""
    location: str
    goods: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    trade_routes: List[str] = field(default_factory=list)
    economic_health: float = 1.0  # 0.0 to 2.0 multiplier
    
    def __post_init__(self):
        if not self.goods:
            self.goods = {
                "food": {"base_price": 5, "supply": 100, "demand": 80, "volatility": 0.2},
                "weapons": {"base_price": 50, "supply": 30, "demand": 40, "volatility": 0.4},
                "magic_items": {"base_price": 200, "supply": 5, "demand": 15, "volatility": 0.8},
                "luxury_goods": {"base_price": 100, "supply": 20, "demand": 25, "volatility": 0.6},
                "raw_materials": {"base_price": 10, "supply": 150, "demand": 120, "volatility": 0.3}
            }


@dataclass
class WorldState:
    """Current state of the world"""
    current_season: str = "spring"
    weather_patterns: Dict[str, str] = field(default_factory=dict)
    faction_powers: Dict[str, float] = field(default_factory=dict)
    public_mood: Dict[str, str] = field(default_factory=dict)
    active_conflicts: List[str] = field(default_factory=list)
    technological_advancement: float = 1.0
    magical_saturation: float = 1.0
    
    # Time tracking
    current_day: int = 1
    current_year: int = 1485  # Fantasy year
    
    # Global events
    ongoing_crises: List[str] = field(default_factory=list)
    recent_major_events: List[str] = field(default_factory=list)


class LivingWorldEngine:
    """Autonomous world simulation engine"""
    
    def __init__(self):
        self.world_state = WorldState()
        self.active_events: List[WorldEvent] = []
        self.markets: Dict[str, EconomicMarket] = {}
        self.event_probabilities = self._initialize_event_probabilities()
        self.world_history: List[str] = []
        
        self._initialize_world()
    
    def _initialize_world(self):
        """Initialize the living world systems"""
        
        # Initialize markets
        locations = ["whispering_woods", "trading_post", "crystal_sanctum", "royal_capital", "border_town"]
        for location in locations:
            self.markets[location] = EconomicMarket(location=location)
        
        # Set initial faction powers
        self.world_state.faction_powers = {
            "royal_crown": 0.8,
            "merchant_guilds": 0.6,
            "order_of_dawn": 0.5,
            "shadow_covenant": 0.3,
            "rebel_factions": 0.2
        }
        
        # Set initial public mood
        self.world_state.public_mood = {
            "royal_capital": "cautiously_optimistic",
            "trading_post": "busy_and_prosperous", 
            "border_town": "anxious",
            "whispering_woods": "mysterious",
            "crystal_sanctum": "reverent"
        }
    
    def _initialize_event_probabilities(self) -> Dict[str, Dict[str, float]]:
        """Initialize base probabilities for different event types"""
        return {
            "economic": {
                "trade_boom": 0.1,
                "market_crash": 0.05,
                "new_trade_route": 0.08,
                "resource_discovery": 0.06,
                "merchant_war": 0.04
            },
            "political": {
                "diplomatic_breakthrough": 0.07,
                "succession_crisis": 0.03,
                "corruption_scandal": 0.06,
                "alliance_formed": 0.08,
                "border_dispute": 0.09
            },
            "natural": {
                "great_storm": 0.15,
                "drought": 0.08,
                "bumper_harvest": 0.12,
                "earthquake": 0.03,
                "plague_outbreak": 0.04
            },
            "social": {
                "cultural_festival": 0.2,
                "religious_awakening": 0.06,
                "social_unrest": 0.08,
                "migration_wave": 0.05,
                "technological_breakthrough": 0.04
            },
            "magical": {
                "magical_surge": 0.08,
                "reality_tear": 0.02,
                "ancient_awakening": 0.04,
                "spell_plague": 0.03,
                "divine_intervention": 0.02
            },
            "military": {
                "bandit_uprising": 0.12,
                "foreign_invasion": 0.03,
                "civil_war": 0.02,
                "military_coup": 0.03,
                "peace_treaty": 0.06
            }
        }
    
    def simulate_world_tick(self, days_passed: int = 1) -> Dict[str, Any]:
        """Simulate world changes over time"""
        
        changes = {
            "new_events": [],
            "resolved_events": [],
            "economic_changes": {},
            "political_shifts": {},
            "narrative_opportunities": []
        }
        
        # Advance time
        self.world_state.current_day += days_passed
        
        # Process seasonal changes
        self._process_seasonal_changes(changes)
        
        # Generate new events
        new_events = self._generate_autonomous_events()
        changes["new_events"] = new_events
        self.active_events.extend(new_events)
        
        # Process ongoing events
        self._process_ongoing_events(changes)
        
        # Update economic markets
        self._update_economic_markets(changes)
        
        # Process political dynamics
        self._process_political_dynamics(changes)
        
        # Generate narrative opportunities
        self._generate_narrative_opportunities(changes)
        
        # Update world history
        self._update_world_history(changes)
        
        return changes
    
    def _process_seasonal_changes(self, changes: Dict[str, Any]):
        """Process seasonal changes and their effects"""
        
        current_season = self._calculate_current_season()
        
        if current_season != self.world_state.current_season:
            self.world_state.current_season = current_season
            changes["seasonal_change"] = current_season
            
            # Seasonal economic effects
            seasonal_effects = {
                "spring": {"food": 0.9, "raw_materials": 1.1},
                "summer": {"luxury_goods": 1.2, "weapons": 1.1},
                "autumn": {"food": 0.8, "magic_items": 1.1},
                "winter": {"food": 1.3, "weapons": 1.2, "luxury_goods": 0.8}
            }
            
            if current_season in seasonal_effects:
                for location, market in self.markets.items():
                    for good, multiplier in seasonal_effects[current_season].items():
                        if good in market.goods:
                            market.goods[good]["base_price"] *= multiplier
    
    def _calculate_current_season(self) -> str:
        """Calculate current season based on day"""
        day_of_year = self.world_state.current_day % 365
        
        if day_of_year < 91:
            return "spring"
        elif day_of_year < 182:
            return "summer"
        elif day_of_year < 273:
            return "autumn"
        else:
            return "winter"
    
    def _generate_autonomous_events(self) -> List[WorldEvent]:
        """Generate new world events autonomously"""
        
        new_events = []
        
        # Check each event type
        for event_type, event_probs in self.event_probabilities.items():
            for event_name, base_probability in event_probs.items():
                
                # Modify probability based on world state
                adjusted_probability = self._adjust_event_probability(
                    event_type, event_name, base_probability
                )
                
                if random.random() < adjusted_probability:
                    event = self._create_specific_event(event_type, event_name)
                    if event:
                        new_events.append(event)
        
        return new_events
    
    def _adjust_event_probability(self, event_type: str, event_name: str, base_prob: float) -> float:
        """Adjust event probability based on current world state"""
        
        probability = base_prob
        
        # Adjust based on world conditions
        if event_type == "economic":
            economic_health = sum(market.economic_health for market in self.markets.values()) / len(self.markets)
            if economic_health < 0.7 and "crash" in event_name:
                probability *= 2.0
            elif economic_health > 1.3 and "boom" in event_name:
                probability *= 1.5
        
        elif event_type == "political":
            if len(self.world_state.active_conflicts) > 2:
                if "crisis" in event_name or "dispute" in event_name:
                    probability *= 1.8
                elif "peace" in event_name or "alliance" in event_name:
                    probability *= 0.5
        
        elif event_type == "natural":
            # Seasonal adjustments
            if self.world_state.current_season == "winter" and "storm" in event_name:
                probability *= 2.0
            elif self.world_state.current_season == "summer" and "drought" in event_name:
                probability *= 1.5
        
        elif event_type == "magical":
            if self.world_state.magical_saturation > 1.5:
                probability *= 1.8
            elif self.world_state.magical_saturation < 0.5:
                probability *= 0.3
        
        return min(probability, 0.5)  # Cap at 50% chance
    
    def _create_specific_event(self, event_type: str, event_name: str) -> Optional[WorldEvent]:
        """Create a specific world event"""
        
        event_templates = {
            "trade_boom": {
                "title": "Trade Boom Sweeps the Realm",
                "description": "A surge in trade activity brings prosperity to merchant routes",
                "severity": EventSeverity.MODERATE,
                "price_changes": {"luxury_goods": 0.8, "weapons": 0.9},
                "faction_reputation_changes": {"merchant_guilds": 15},
                "duration": 14
            },
            "market_crash": {
                "title": "Economic Turmoil Strikes Markets",
                "description": "A financial crisis causes widespread economic instability",
                "severity": EventSeverity.MAJOR,
                "price_changes": {"all": 1.3, "luxury_goods": 1.8},
                "public_mood_changes": {"all": "anxious"},
                "duration": 21
            },
            "great_storm": {
                "title": "The Great Storm",
                "description": "Massive storms ravage the countryside, disrupting travel and trade",
                "severity": EventSeverity.MAJOR,
                "affected_locations": ["whispering_woods", "border_town"],
                "price_changes": {"food": 1.4, "raw_materials": 1.2},
                "trade_route_effects": {"all": "disrupted"},
                "duration": 7
            },
            "diplomatic_breakthrough": {
                "title": "Historic Peace Accord Signed",
                "description": "Long-standing enemies agree to a groundbreaking peace treaty",
                "severity": EventSeverity.MODERATE,
                "faction_reputation_changes": {"royal_crown": 20, "order_of_dawn": 10},
                "public_mood_changes": {"royal_capital": "celebratory"},
                "new_quest_opportunities": ["diplomatic_mission", "peace_celebration"],
                "duration": 30
            },
            "magical_surge": {
                "title": "Arcane Energies Surge",
                "description": "Magical forces intensify across the realm, affecting spellcasters",
                "severity": EventSeverity.MODERATE,
                "price_changes": {"magic_items": 0.7},
                "changed_character_behaviors": {"mages": "more_powerful", "templars": "concerned"},
                "duration": 10
            },
            "bandit_uprising": {
                "title": "Bandit Lord Declares War",
                "description": "Organized bandits launch coordinated attacks on trade routes",
                "severity": EventSeverity.MAJOR,
                "affected_locations": ["trading_post", "border_town"],
                "price_changes": {"weapons": 0.8, "luxury_goods": 1.3},
                "new_quest_opportunities": ["bandit_hunting", "caravan_protection"],
                "duration": 21
            }
        }
        
        if event_name not in event_templates:
            return None
        
        template = event_templates[event_name]
        
        return WorldEvent(
            id=f"{event_name}_{self.world_state.current_day}",
            event_type=WorldEventType(event_type),
            severity=template["severity"],
            title=template["title"],
            description=template["description"],
            affected_locations=template.get("affected_locations", []),
            price_changes=template.get("price_changes", {}),
            trade_route_effects=template.get("trade_route_effects", {}),
            faction_reputation_changes=template.get("faction_reputation_changes", {}),
            public_mood_changes=template.get("public_mood_changes", {}),
            new_quest_opportunities=template.get("new_quest_opportunities", []),
            changed_character_behaviors=template.get("changed_character_behaviors", {}),
            duration=template.get("duration", 7)
        )
    
    def _process_ongoing_events(self, changes: Dict[str, Any]):
        """Process ongoing events and resolve expired ones"""
        
        current_time = datetime.now()
        resolved_events = []
        
        for event in self.active_events[:]:  # Copy list to avoid modification during iteration
            event_end_time = event.start_time + timedelta(days=event.duration)
            
            if current_time >= event_end_time:
                # Event has ended
                resolved_events.append(event)
                self.active_events.remove(event)
                
                # Apply resolution effects
                self._apply_event_resolution(event, changes)
                
                # Trigger follow-up events
                for triggered_event_id in event.triggered_events:
                    follow_up = self._create_follow_up_event(triggered_event_id, event)
                    if follow_up:
                        self.active_events.append(follow_up)
        
        changes["resolved_events"] = resolved_events
    
    def _apply_event_resolution(self, event: WorldEvent, changes: Dict[str, Any]):
        """Apply effects when an event resolves"""
        
        # Restore some price changes (markets adapt)
        for good, multiplier in event.price_changes.items():
            if good == "all":
                for location, market in self.markets.items():
                    for good_name in market.goods:
                        # Partial restoration - markets don't fully revert
                        current_price = market.goods[good_name]["base_price"]
                        restored_price = current_price / (1 + (multiplier - 1) * 0.5)
                        market.goods[good_name]["base_price"] = restored_price
            else:
                for location, market in self.markets.items():
                    if good in market.goods:
                        current_price = market.goods[good]["base_price"]
                        restored_price = current_price / (1 + (multiplier - 1) * 0.5)
                        market.goods[good]["base_price"] = restored_price
        
        # Update faction power based on how well they handled the event
        for faction, reputation_change in event.faction_reputation_changes.items():
            if faction in self.world_state.faction_powers:
                power_change = reputation_change * 0.01  # Convert reputation to power
                self.world_state.faction_powers[faction] += power_change
                self.world_state.faction_powers[faction] = max(0.1, min(2.0, self.world_state.faction_powers[faction]))
    
    def _create_follow_up_event(self, event_id: str, parent_event: WorldEvent) -> Optional[WorldEvent]:
        """Create follow-up events triggered by resolved events"""
        
        follow_up_templates = {
            "reconstruction_efforts": {
                "title": "Reconstruction Begins",
                "description": f"Communities begin rebuilding after {parent_event.title.lower()}",
                "severity": EventSeverity.MINOR,
                "duration": 14
            },
            "economic_recovery": {
                "title": "Economic Recovery Initiatives",
                "description": "New policies are implemented to restore economic stability",
                "severity": EventSeverity.MODERATE,
                "duration": 21
            },
            "political_consequences": {
                "title": "Political Ramifications Emerge",
                "description": f"The aftermath of {parent_event.title.lower()} reshapes the political landscape",
                "severity": EventSeverity.MODERATE,
                "duration": 30
            }
        }
        
        if event_id in follow_up_templates:
            template = follow_up_templates[event_id]
            return WorldEvent(
                id=f"{event_id}_{self.world_state.current_day}",
                event_type=parent_event.event_type,
                severity=template["severity"],
                title=template["title"],
                description=template["description"],
                duration=template["duration"]
            )
        
        return None
    
    def _update_economic_markets(self, changes: Dict[str, Any]):
        """Update economic markets with supply/demand dynamics"""
        
        market_changes = {}
        
        for location, market in self.markets.items():
            location_changes = {}
            
            for good_name, good_data in market.goods.items():
                # Simulate supply/demand fluctuations
                supply_change = random.uniform(-0.1, 0.1)
                demand_change = random.uniform(-0.1, 0.1)
                
                good_data["supply"] += supply_change * good_data["supply"]
                good_data["demand"] += demand_change * good_data["demand"]
                
                # Calculate price based on supply/demand
                supply_demand_ratio = good_data["demand"] / max(good_data["supply"], 1)
                volatility = good_data["volatility"]
                
                price_change = (supply_demand_ratio - 1) * volatility
                new_price = good_data["base_price"] * (1 + price_change)
                
                # Ensure reasonable price bounds
                good_data["base_price"] = max(new_price, good_data["base_price"] * 0.5)
                good_data["base_price"] = min(good_data["base_price"], good_data["base_price"] * 2.0)
                
                if abs(price_change) > 0.1:
                    location_changes[good_name] = {
                        "old_price": good_data["base_price"] / (1 + price_change),
                        "new_price": good_data["base_price"],
                        "change_percent": price_change * 100
                    }
            
            if location_changes:
                market_changes[location] = location_changes
        
        changes["economic_changes"] = market_changes
    
    def _process_political_dynamics(self, changes: Dict[str, Any]):
        """Process ongoing political dynamics"""
        
        political_shifts = {}
        
        # Faction power struggles
        for faction, power in self.world_state.faction_powers.items():
            # Random political events
            if random.random() < 0.05:  # 5% chance daily
                power_shift = random.uniform(-0.05, 0.05)
                self.world_state.faction_powers[faction] += power_shift
                self.world_state.faction_powers[faction] = max(0.1, min(2.0, self.world_state.faction_powers[faction]))
                
                if abs(power_shift) > 0.02:
                    political_shifts[faction] = {
                        "power_change": power_shift,
                        "new_power": self.world_state.faction_powers[faction],
                        "description": "Internal political maneuvering" if power_shift > 0 else "Setbacks in political influence"
                    }
        
        changes["political_shifts"] = political_shifts
    
    def _generate_narrative_opportunities(self, changes: Dict[str, Any]):
        """Generate new narrative opportunities based on world state"""
        
        opportunities = []
        
        # Check for economic opportunities
        for location, market_changes in changes.get("economic_changes", {}).items():
            for good, change_data in market_changes.items():
                if change_data["change_percent"] > 20:
                    opportunities.append({
                        "type": "economic_opportunity",
                        "location": location,
                        "description": f"High demand for {good} in {location}",
                        "quest_hook": f"Merchants in {location} are paying premium prices for {good}"
                    })
        
        # Check for political opportunities
        for faction, shift_data in changes.get("political_shifts", {}).items():
            if abs(shift_data["power_change"]) > 0.03:
                opportunities.append({
                    "type": "political_opportunity",
                    "faction": faction,
                    "description": f"{faction} experiencing significant power shifts",
                    "quest_hook": f"Political turbulence in {faction} creates opportunities for influence"
                })
        
        # Check event-based opportunities
        for event in changes.get("new_events", []):
            opportunities.extend([
                {
                    "type": "event_response",
                    "event_id": event.id,
                    "description": f"Respond to {event.title}",
                    "quest_hook": event.description
                }
                for quest_type in event.new_quest_opportunities
            ])
        
        changes["narrative_opportunities"] = opportunities
    
    def _update_world_history(self, changes: Dict[str, Any]):
        """Update world history with significant events"""
        
        for event in changes.get("new_events", []):
            if event.severity in [EventSeverity.MAJOR, EventSeverity.CATASTROPHIC]:
                history_entry = f"Day {self.world_state.current_day}: {event.title}"
                self.world_history.append(history_entry)
                self.world_state.recent_major_events.append(event.title)
        
        # Keep only recent major events (last 10)
        if len(self.world_state.recent_major_events) > 10:
            self.world_state.recent_major_events = self.world_state.recent_major_events[-10:]
    
    def get_current_world_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the current world state"""
        
        return {
            "world_state": {
                "day": self.world_state.current_day,
                "year": self.world_state.current_year,
                "season": self.world_state.current_season,
                "technological_level": self.world_state.technological_advancement,
                "magical_saturation": self.world_state.magical_saturation
            },
            "active_events": [
                {
                    "title": event.title,
                    "severity": event.severity.value,
                    "days_remaining": event.duration - (datetime.now() - event.start_time).days,
                    "affected_locations": event.affected_locations
                }
                for event in self.active_events
            ],
            "faction_powers": self.world_state.faction_powers,
            "public_mood": self.world_state.public_mood,
            "economic_summary": {
                location: {
                    "economic_health": market.economic_health,
                    "major_price_changes": {
                        good: data["base_price"]
                        for good, data in market.goods.items()
                        if abs(data.get("recent_change", 0)) > 0.2
                    }
                }
                for location, market in self.markets.items()
            },
            "recent_history": self.world_history[-5:],  # Last 5 major events
            "ongoing_crises": self.world_state.ongoing_crises
        }
    
    def get_location_specific_info(self, location: str) -> Dict[str, Any]:
        """Get detailed information about a specific location"""
        
        market = self.markets.get(location)
        if not market:
            return {"error": "Location not found"}
        
        # Find events affecting this location
        location_events = [
            event for event in self.active_events
            if location in event.affected_locations or not event.affected_locations
        ]
        
        return {
            "location": location,
            "economic_state": {
                "market_health": market.economic_health,
                "trade_routes": market.trade_routes,
                "current_prices": {
                    good: data["base_price"]
                    for good, data in market.goods.items()
                },
                "supply_demand": {
                    good: {
                        "supply": data["supply"],
                        "demand": data["demand"],
                        "trend": "high_demand" if data["demand"] > data["supply"] else "oversupply"
                    }
                    for good, data in market.goods.items()
                }
            },
            "current_events": [
                {
                    "title": event.title,
                    "description": event.description,
                    "severity": event.severity.value,
                    "days_remaining": event.duration - (datetime.now() - event.start_time).days
                }
                for event in location_events
            ],
            "public_mood": self.world_state.public_mood.get(location, "neutral"),
            "seasonal_effects": self._get_seasonal_effects(location)
        }
    
    def _get_seasonal_effects(self, location: str) -> Dict[str, Any]:
        """Get seasonal effects for a location"""
        
        season = self.world_state.current_season
        
        seasonal_descriptions = {
            "spring": {
                "description": "New growth and renewal bring hope",
                "economic_effects": "Agricultural goods become more affordable",
                "travel_conditions": "Roads improve as snow melts"
            },
            "summer": {
                "description": "Long days and warm weather encourage activity",
                "economic_effects": "Luxury trade flourishes",
                "travel_conditions": "Excellent travel conditions"
            },
            "autumn": {
                "description": "Harvest time brings abundance and preparation",
                "economic_effects": "Food prices drop, preparations for winter drive trade",
                "travel_conditions": "Good travel before winter sets in"
            },
            "winter": {
                "description": "Cold and hardship test community bonds",
                "economic_effects": "Food and fuel prices rise significantly",
                "travel_conditions": "Difficult and dangerous travel conditions"
            }
        }
        
        return seasonal_descriptions.get(season, {"description": "The season progresses normally"})
    
    def trigger_player_influenced_event(self, event_type: str, player_action: str, impact_level: str) -> Optional[WorldEvent]:
        """Trigger world events based on player actions"""
        
        # Player actions can influence world events
        influence_templates = {
            "economic": {
                "large_purchase": "Market disruption from major transaction",
                "trade_route_action": "Trade route security improves",
                "merchant_alliance": "New economic opportunities emerge"
            },
            "political": {
                "faction_alliance": "Political landscape shifts",
                "diplomatic_success": "Regional stability improves",
                "conflict_resolution": "Peace dividend affects economy"
            },
            "social": {
                "heroic_deed": "Public morale receives significant boost",
                "community_service": "Local community bonds strengthen",
                "scandal_exposure": "Public trust in institutions wavers"
            }
        }
        
        if event_type in influence_templates and player_action in influence_templates[event_type]:
            description = influence_templates[event_type][player_action]
            
            severity = {
                "minor": EventSeverity.MINOR,
                "moderate": EventSeverity.MODERATE,
                "major": EventSeverity.MAJOR
            }.get(impact_level, EventSeverity.MINOR)
            
            event = WorldEvent(
                id=f"player_triggered_{event_type}_{self.world_state.current_day}",
                event_type=WorldEventType(event_type),
                severity=severity,
                title=f"Consequences of {player_action.replace('_', ' ').title()}",
                description=description,
                duration=random.randint(7, 21)
            )
            
            self.active_events.append(event)
            return event
        
        return None 