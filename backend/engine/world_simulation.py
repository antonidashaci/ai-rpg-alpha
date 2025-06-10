"""
AI-RPG-Alpha: Dynamic World Simulation

Living world system that creates autonomous events, economic changes,
and evolving world states independent of player actions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random
from datetime import datetime


class WorldEventType(Enum):
    """Types of autonomous world events"""
    ECONOMIC = "economic"
    POLITICAL = "political"
    NATURAL = "natural"
    MAGICAL = "magical"
    SOCIAL = "social"


@dataclass
class WorldEvent:
    """A dynamic world event that affects the game state"""
    id: str
    title: str
    description: str
    event_type: WorldEventType
    severity: str  # minor, moderate, major, catastrophic
    
    # Effects
    price_changes: Dict[str, float] = field(default_factory=dict)
    faction_changes: Dict[str, int] = field(default_factory=dict)
    location_effects: Dict[str, str] = field(default_factory=dict)
    
    # Duration and timing
    duration_days: int = 7
    start_day: int = 0
    
    # Narrative impact
    quest_opportunities: List[str] = field(default_factory=list)
    character_reactions: Dict[str, str] = field(default_factory=dict)


@dataclass
class LivingWorld:
    """Dynamic world state that evolves autonomously"""
    current_day: int = 1
    current_season: str = "spring"
    
    # Economic state
    market_prices: Dict[str, Dict[str, float]] = field(default_factory=dict)
    trade_routes: Dict[str, str] = field(default_factory=dict)  # route -> status
    
    # Political state
    faction_power: Dict[str, float] = field(default_factory=dict)
    political_tension: float = 0.5
    
    # Environmental state
    weather_patterns: Dict[str, str] = field(default_factory=dict)
    magical_saturation: float = 1.0
    
    # Social state
    public_mood: Dict[str, str] = field(default_factory=dict)
    
    # Active events
    active_events: List[WorldEvent] = field(default_factory=list)
    event_history: List[str] = field(default_factory=list)


class WorldSimulationEngine:
    """Engine for autonomous world simulation"""
    
    def __init__(self):
        self.world = LivingWorld()
        self._initialize_world_state()
        self.event_templates = self._load_event_templates()
    
    def _initialize_world_state(self):
        """Initialize the starting world state"""
        
        # Initialize market prices
        self.world.market_prices = {
            "whispering_woods": {
                "food": 5, "weapons": 50, "magic_items": 200, "herbs": 15
            },
            "trading_post": {
                "food": 4, "weapons": 45, "magic_items": 180, "luxury_goods": 100
            },
            "crystal_sanctum": {
                "food": 8, "weapons": 70, "magic_items": 150, "crystals": 300
            }
        }
        
        # Initialize faction power
        self.world.faction_power = {
            "royal_crown": 0.8,
            "merchant_guild": 0.6,
            "order_of_dawn": 0.5,
            "shadow_covenant": 0.3
        }
        
        # Initialize public mood
        self.world.public_mood = {
            "whispering_woods": "cautious",
            "trading_post": "optimistic", 
            "crystal_sanctum": "mystical"
        }
    
    def _load_event_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load templates for world events"""
        
        return {
            "trade_boom": {
                "title": "Trade Boom Sweeps the Region",
                "description": "Increased trade activity brings prosperity to merchants and travelers",
                "type": WorldEventType.ECONOMIC,
                "severity": "moderate",
                "price_changes": {"all_locations": {"luxury_goods": 0.8, "weapons": 0.9}},
                "faction_changes": {"merchant_guild": 15},
                "duration": 14,
                "quest_opportunities": ["escort_valuable_cargo", "establish_trade_route"]
            },
            "magical_storm": {
                "title": "Arcane Storm Rages",
                "description": "Powerful magical energies disrupt the natural order",
                "type": WorldEventType.MAGICAL,
                "severity": "major",
                "price_changes": {"all_locations": {"magic_items": 1.5}},
                "location_effects": {"whispering_woods": "unstable_magic", "crystal_sanctum": "enhanced_power"},
                "duration": 5,
                "quest_opportunities": ["investigate_magical_disturbance", "protect_civilians"]
            },
            "bandit_uprising": {
                "title": "Bandits Threaten Trade Routes",
                "description": "Organized bandits have begun attacking merchant caravans",
                "type": WorldEventType.SOCIAL,
                "severity": "major",
                "price_changes": {"trading_post": {"weapons": 0.8, "food": 1.2}},
                "trade_routes": {"main_road": "dangerous", "forest_path": "blocked"},
                "duration": 21,
                "quest_opportunities": ["hunt_bandit_leader", "escort_merchant_caravan", "negotiate_safe_passage"]
            },
            "harvest_festival": {
                "title": "Harvest Festival Begins",
                "description": "Communities celebrate the autumn harvest with joy and festivities",
                "type": WorldEventType.SOCIAL,
                "severity": "minor",
                "price_changes": {"all_locations": {"food": 0.7}},
                "public_mood_changes": {"all_locations": "celebratory"},
                "duration": 3,
                "quest_opportunities": ["festival_performance", "solve_festival_mystery"]
            },
            "political_crisis": {
                "title": "Succession Crisis Emerges",
                "description": "Disputed claims to noble titles create political instability",
                "type": WorldEventType.POLITICAL,
                "severity": "major",
                "faction_changes": {"royal_crown": -10, "shadow_covenant": 5},
                "public_mood_changes": {"all_locations": "anxious"},
                "duration": 30,
                "quest_opportunities": ["support_rightful_heir", "investigate_conspiracy", "mediate_dispute"]
            },
            "dragon_sighting": {
                "title": "Ancient Dragon Spotted",
                "description": "A mighty dragon has been seen flying over the mountains",
                "type": WorldEventType.NATURAL,
                "severity": "catastrophic",
                "price_changes": {"all_locations": {"weapons": 0.7, "magic_items": 0.8}},
                "public_mood_changes": {"all_locations": "fearful"},
                "duration": 7,
                "quest_opportunities": ["investigate_dragon_lair", "seek_dragon_wisdom", "prepare_defenses"]
            }
        }
    
    def simulate_world_progression(self, days_passed: int = 1) -> Dict[str, Any]:
        """Simulate world changes over time"""
        
        changes = {
            "new_events": [],
            "resolved_events": [],
            "market_changes": {},
            "political_changes": {},
            "social_changes": {},
            "quest_opportunities": []
        }
        
        # Advance time
        self.world.current_day += days_passed
        
        # Update season
        self._update_season()
        
        # Process ongoing events
        self._process_ongoing_events(changes)
        
        # Generate new random events
        self._generate_random_events(changes)
        
        # Update market dynamics
        self._update_market_dynamics(changes)
        
        # Update political dynamics
        self._update_political_dynamics(changes)
        
        # Update social dynamics
        self._update_social_dynamics(changes)
        
        return changes
    
    def _update_season(self):
        """Update current season based on day"""
        
        day_of_year = self.world.current_day % 365
        
        if day_of_year < 91:
            new_season = "spring"
        elif day_of_year < 182:
            new_season = "summer"
        elif day_of_year < 273:
            new_season = "autumn"
        else:
            new_season = "winter"
        
        if new_season != self.world.current_season:
            self.world.current_season = new_season
            self._apply_seasonal_effects()
    
    def _apply_seasonal_effects(self):
        """Apply seasonal effects to the world"""
        
        seasonal_effects = {
            "spring": {"food": 0.9, "herbs": 0.8},
            "summer": {"luxury_goods": 1.1, "food": 0.8},
            "autumn": {"food": 0.7, "weapons": 1.1},
            "winter": {"food": 1.3, "herbs": 1.5, "weapons": 1.2}
        }
        
        effects = seasonal_effects.get(self.world.current_season, {})
        
        for location in self.world.market_prices:
            for item, multiplier in effects.items():
                if item in self.world.market_prices[location]:
                    self.world.market_prices[location][item] *= multiplier
    
    def _process_ongoing_events(self, changes: Dict[str, Any]):
        """Process active events and remove expired ones"""
        
        resolved_events = []
        
        for event in self.world.active_events[:]:  # Copy to avoid modification during iteration
            event_age = self.world.current_day - event.start_day
            
            if event_age >= event.duration_days:
                # Event has ended
                resolved_events.append(event)
                self.world.active_events.remove(event)
                self._apply_event_resolution_effects(event)
        
        changes["resolved_events"] = resolved_events
    
    def _apply_event_resolution_effects(self, event: WorldEvent):
        """Apply effects when an event resolves"""
        
        # Gradual price restoration (markets adapt)
        for location, price_changes in event.price_changes.items():
            if location == "all_locations":
                for loc in self.world.market_prices:
                    for item, multiplier in price_changes.items():
                        if item in self.world.market_prices[loc]:
                            # Partial restoration
                            current_price = self.world.market_prices[loc][item]
                            restored_price = current_price / (1 + (multiplier - 1) * 0.5)
                            self.world.market_prices[loc][item] = restored_price
    
    def _generate_random_events(self, changes: Dict[str, Any]):
        """Generate random world events"""
        
        # Base probability of events per day
        event_chance = 0.15  # 15% chance per day
        
        if random.random() < event_chance:
            # Select random event type
            event_types = list(self.event_templates.keys())
            
            # Adjust probabilities based on world state
            weights = []
            for event_type in event_types:
                weight = 1.0
                
                # Adjust based on current conditions
                if event_type == "trade_boom" and self.world.faction_power.get("merchant_guild", 0) > 0.7:
                    weight *= 1.5
                elif event_type == "political_crisis" and self.world.political_tension > 0.7:
                    weight *= 2.0
                elif event_type == "bandit_uprising" and any("dangerous" in status for status in self.world.trade_routes.values()):
                    weight *= 0.5  # Less likely if already dangerous
                
                weights.append(weight)
            
            # Select event
            selected_event_type = random.choices(event_types, weights=weights)[0]
            new_event = self._create_event_from_template(selected_event_type)
            
            if new_event:
                self.world.active_events.append(new_event)
                changes["new_events"].append(new_event)
                self._apply_event_start_effects(new_event)
    
    def _create_event_from_template(self, template_name: str) -> Optional[WorldEvent]:
        """Create a world event from a template"""
        
        template = self.event_templates.get(template_name)
        if not template:
            return None
        
        event = WorldEvent(
            id=f"{template_name}_{self.world.current_day}",
            title=template["title"],
            description=template["description"],
            event_type=template["type"],
            severity=template["severity"],
            duration_days=template["duration"],
            start_day=self.world.current_day,
            quest_opportunities=template.get("quest_opportunities", [])
        )
        
        # Apply template effects
        if "price_changes" in template:
            event.price_changes = template["price_changes"]
        
        if "faction_changes" in template:
            event.faction_changes = template["faction_changes"]
        
        if "location_effects" in template:
            event.location_effects = template["location_effects"]
        
        return event
    
    def _apply_event_start_effects(self, event: WorldEvent):
        """Apply immediate effects when an event starts"""
        
        # Apply price changes
        for location, price_changes in event.price_changes.items():
            if location == "all_locations":
                for loc in self.world.market_prices:
                    for item, multiplier in price_changes.items():
                        if item in self.world.market_prices[loc]:
                            self.world.market_prices[loc][item] *= multiplier
            elif location in self.world.market_prices:
                for item, multiplier in price_changes.items():
                    if item in self.world.market_prices[location]:
                        self.world.market_prices[location][item] *= multiplier
        
        # Apply faction changes
        for faction, change in event.faction_changes.items():
            if faction in self.world.faction_power:
                self.world.faction_power[faction] += change * 0.01  # Convert to decimal
                self.world.faction_power[faction] = max(0.1, min(2.0, self.world.faction_power[faction]))
    
    def _update_market_dynamics(self, changes: Dict[str, Any]):
        """Update market prices with natural fluctuations"""
        
        market_changes = {}
        
        for location, prices in self.world.market_prices.items():
            location_changes = {}
            
            for item, price in prices.items():
                # Small random fluctuations
                change_factor = random.uniform(0.95, 1.05)
                new_price = price * change_factor
                
                # Ensure reasonable bounds
                base_prices = {
                    "food": 5, "weapons": 50, "magic_items": 200, 
                    "herbs": 15, "luxury_goods": 100, "crystals": 300
                }
                
                min_price = base_prices.get(item, 10) * 0.5
                max_price = base_prices.get(item, 10) * 3.0
                
                new_price = max(min_price, min(max_price, new_price))
                
                if abs(new_price - price) > price * 0.1:  # Significant change (>10%)
                    location_changes[item] = {
                        "old_price": price,
                        "new_price": new_price,
                        "change_percent": ((new_price - price) / price) * 100
                    }
                
                self.world.market_prices[location][item] = new_price
            
            if location_changes:
                market_changes[location] = location_changes
        
        changes["market_changes"] = market_changes
    
    def _update_political_dynamics(self, changes: Dict[str, Any]):
        """Update political power dynamics"""
        
        political_changes = {}
        
        # Faction power struggles
        for faction, power in self.world.faction_power.items():
            # Small random political fluctuations
            if random.random() < 0.1:  # 10% chance per day
                change = random.uniform(-0.02, 0.02)
                new_power = max(0.1, min(2.0, power + change))
                
                if abs(change) > 0.01:
                    political_changes[faction] = {
                        "old_power": power,
                        "new_power": new_power,
                        "change": change,
                        "description": "Political maneuvering" if change > 0 else "Setbacks in influence"
                    }
                
                self.world.faction_power[faction] = new_power
        
        # Update overall political tension
        power_variance = max(self.world.faction_power.values()) - min(self.world.faction_power.values())
        self.world.political_tension = min(1.0, power_variance)
        
        changes["political_changes"] = political_changes
    
    def _update_social_dynamics(self, changes: Dict[str, Any]):
        """Update social dynamics and public mood"""
        
        social_changes = {}
        
        for location, mood in self.world.public_mood.items():
            # Mood can gradually change based on events and conditions
            if random.random() < 0.05:  # 5% chance per day
                mood_options = ["joyful", "optimistic", "cautious", "anxious", "fearful", "angry"]
                
                # Current mood influences next mood
                if mood in ["joyful", "optimistic"]:
                    new_mood = random.choice(["joyful", "optimistic", "cautious"])
                elif mood in ["anxious", "fearful"]:
                    new_mood = random.choice(["anxious", "fearful", "cautious"])
                else:
                    new_mood = random.choice(mood_options)
                
                if new_mood != mood:
                    social_changes[location] = {
                        "old_mood": mood,
                        "new_mood": new_mood,
                        "description": f"Public sentiment shifts from {mood} to {new_mood}"
                    }
                    
                    self.world.public_mood[location] = new_mood
        
        changes["social_changes"] = social_changes
    
    def get_world_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive world status summary"""
        
        return {
            "time": {
                "day": self.world.current_day,
                "season": self.world.current_season
            },
            "active_events": [
                {
                    "title": event.title,
                    "type": event.event_type.value,
                    "severity": event.severity,
                    "days_remaining": event.duration_days - (self.world.current_day - event.start_day)
                }
                for event in self.world.active_events
            ],
            "faction_power": self.world.faction_power,
            "political_tension": self.world.political_tension,
            "public_mood": self.world.public_mood,
            "trade_status": self.world.trade_routes,
            "available_quests": self._get_available_quest_opportunities()
        }
    
    def get_location_status(self, location: str) -> Dict[str, Any]:
        """Get detailed status for a specific location"""
        
        if location not in self.world.market_prices:
            return {"error": "Location not found"}
        
        # Find events affecting this location
        affecting_events = []
        for event in self.world.active_events:
            if location in event.location_effects or "all_locations" in event.price_changes:
                affecting_events.append({
                    "title": event.title,
                    "description": event.description,
                    "effect": event.location_effects.get(location, "Economic impact")
                })
        
        return {
            "location": location,
            "market_prices": self.world.market_prices[location],
            "public_mood": self.world.public_mood.get(location, "neutral"),
            "active_events": affecting_events,
            "seasonal_effect": self._get_seasonal_description(),
            "trade_opportunities": self._get_location_trade_opportunities(location)
        }
    
    def _get_available_quest_opportunities(self) -> List[Dict[str, Any]]:
        """Get quest opportunities from active events"""
        
        opportunities = []
        
        for event in self.world.active_events:
            for quest_type in event.quest_opportunities:
                opportunities.append({
                    "quest_type": quest_type,
                    "source_event": event.title,
                    "urgency": event.severity,
                    "description": f"Respond to {event.title.lower()}"
                })
        
        return opportunities
    
    def _get_seasonal_description(self) -> str:
        """Get description of current seasonal effects"""
        
        descriptions = {
            "spring": "New growth brings hope and opportunity",
            "summer": "Long days favor trade and adventure",
            "autumn": "Harvest time brings abundance but preparation urgency",
            "winter": "Cold weather makes travel difficult but creates unique opportunities"
        }
        
        return descriptions.get(self.world.current_season, "The season progresses normally")
    
    def _get_location_trade_opportunities(self, location: str) -> List[str]:
        """Get trade opportunities specific to a location"""
        
        opportunities = []
        prices = self.world.market_prices[location]
        
        # High-priced items suggest selling opportunities
        for item, price in prices.items():
            base_prices = {
                "food": 5, "weapons": 50, "magic_items": 200,
                "herbs": 15, "luxury_goods": 100, "crystals": 300
            }
            
            base_price = base_prices.get(item, 50)
            
            if price > base_price * 1.3:
                opportunities.append(f"High demand for {item} - good selling opportunity")
            elif price < base_price * 0.7:
                opportunities.append(f"Low prices on {item} - good buying opportunity")
        
        return opportunities
    
    def trigger_player_influenced_event(self, event_type: str, magnitude: str) -> Optional[WorldEvent]:
        """Trigger world events based on significant player actions"""
        
        player_influence_events = {
            "economic_boom": {
                "title": "Economic Prosperity Spreads",
                "description": "Player actions have stimulated economic growth across the region",
                "type": WorldEventType.ECONOMIC,
                "price_changes": {"all_locations": {"luxury_goods": 0.9}},
                "duration": 10
            },
            "political_stability": {
                "title": "Political Tensions Ease",
                "description": "Diplomatic efforts have reduced regional conflicts",
                "type": WorldEventType.POLITICAL,
                "faction_changes": {"royal_crown": 10},
                "duration": 15
            },
            "magical_disturbance": {
                "title": "Magical Energies Fluctuate",
                "description": "Recent magical events have caused widespread arcane instability",
                "type": WorldEventType.MAGICAL,
                "price_changes": {"all_locations": {"magic_items": 1.2}},
                "duration": 7
            }
        }
        
        if event_type in player_influence_events:
            template = player_influence_events[event_type]
            
            event = WorldEvent(
                id=f"player_{event_type}_{self.world.current_day}",
                title=template["title"],
                description=template["description"],
                event_type=template["type"],
                severity=magnitude,
                duration_days=template["duration"],
                start_day=self.world.current_day
            )
            
            # Apply template effects
            event.price_changes = template.get("price_changes", {})
            event.faction_changes = template.get("faction_changes", {})
            
            self.world.active_events.append(event)
            self._apply_event_start_effects(event)
            
            return event
        
        return None 