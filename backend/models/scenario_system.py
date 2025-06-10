"""
Scenario System for AI-RPG-Alpha
Implements the three-scenario framework from PRD
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum

class ScenarioType(Enum):
    NORTHERN_REALMS = "northern_realms"
    WHISPERING_TOWN = "whispering_town"
    NEO_TOKYO = "neo_tokyo"

@dataclass
class ScenarioData:
    """Core scenario configuration"""
    id: str
    name: str
    genre: str
    description: str
    starting_location: str
    starting_stats: Dict[str, int]
    unique_mechanics: List[str]
    progression_focus: str
    risk_factors: List[str]

class ScenarioConfig:
    """Configuration for all three scenarios"""
    
    @staticmethod
    def get_scenario_data() -> Dict[str, ScenarioData]:
        return {
            "northern_realms": ScenarioData(
                id="northern_realms",
                name="The Northern Realms",
                genre="Epic Fantasy",
                description="Ancient dragons stir in forgotten mountain peaks. Magic flows through mystical ley lines.",
                starting_location="ironhold_village",
                starting_stats={
                    "health": 100,
                    "mana": 60,
                    "stamina": 80,
                    "strength": 12,
                    "intelligence": 10,
                    "charisma": 8,
                    "magic_affinity": 15,
                    "honor": 50
                },
                unique_mechanics=["magic_system", "political_intrigue", "dragon_encounters"],
                progression_focus="epic_heroism",
                risk_factors=["magical_corruption", "political_enemies", "ancient_curses"]
            ),
            
            "whispering_town": ScenarioData(
                id="whispering_town",
                name="The Whispering Town",
                genre="Cosmic Horror",
                description="Reality grows thin in this forgotten New England town.",
                starting_location="arkham_outskirts",
                starting_stats={
                    "health": 80,
                    "sanity": 100,
                    "willpower": 70,
                    "strength": 8,
                    "intelligence": 14,
                    "charisma": 6,
                    "cosmic_knowledge": 0,
                    "reality_anchor": 100
                },
                unique_mechanics=["sanity_system", "reality_distortion", "forbidden_knowledge"],
                progression_focus="survival_horror",
                risk_factors=["sanity_loss", "reality_breakdown", "cosmic_entities"]
            ),
            
            "neo_tokyo": ScenarioData(
                id="neo_tokyo", 
                name="Neo-Tokyo 2087",
                genre="Cyberpunk Dystopia",
                description="Neon lights pierce through acid rain as corporate overlords control humanity's digital souls.",
                starting_location="shibuya_undercity",
                starting_stats={
                    "health": 90,
                    "data": 50,
                    "tech_rating": 60,
                    "strength": 6,
                    "intelligence": 16,
                    "charisma": 10,
                    "cyber_compatibility": 20,
                    "corp_standing": 0
                },
                unique_mechanics=["cybernetics", "data_warfare", "corporate_politics"],
                progression_focus="tech_enhancement",
                risk_factors=["corporate_retaliation", "cyber_virus", "memory_corruption"]
            )
        }

class CombatSystem:
    """BG3-style combat system with environmental interaction"""
    
    @dataclass
    class CombatResources:
        stamina: int = 100
        action_points: int = 2
        tactical_advantage: int = 0
        environmental_factors: List[str] = None
        
        def __post_init__(self):
            if self.environmental_factors is None:
                self.environmental_factors = []

    @staticmethod
    def get_tactical_options(scenario: str, location: str, resources: CombatResources) -> List[Dict[str, Any]]:
        """Generate BG3-style tactical combat options"""
        
        base_options = [
            {
                "action": "Direct Attack",
                "stamina_cost": 20,
                "action_points": 1,
                "success_chance": 70,
                "description": "A straightforward assault"
            },
            {
                "action": "Defensive Stance", 
                "stamina_cost": 10,
                "action_points": 1,
                "success_chance": 85,
                "description": "Focus on defense and positioning"
            }
        ]
        
        # Scenario-specific tactical options
        if scenario == "northern_realms":
            base_options.extend([
                {
                    "action": "Invoke Ancient Magic",
                    "stamina_cost": 30,
                    "action_points": 2,
                    "success_chance": 60,
                    "description": "Channel mystical energies for devastating effect"
                },
                {
                    "action": "Rally Allies",
                    "stamina_cost": 15,
                    "action_points": 1,
                    "success_chance": 80,
                    "description": "Inspire nearby allies to fight harder"
                }
            ])
        elif scenario == "whispering_town":
            base_options.extend([
                {
                    "action": "Forbidden Ritual",
                    "stamina_cost": 25,
                    "action_points": 2,
                    "success_chance": 50,
                    "description": "Use cursed knowledge (sanity risk)",
                    "sanity_cost": 15
                },
                {
                    "action": "Flee in Terror",
                    "stamina_cost": 40,
                    "action_points": 1,
                    "success_chance": 90,
                    "description": "Sometimes running is the wisest choice"
                }
            ])
        elif scenario == "neo_tokyo":
            base_options.extend([
                {
                    "action": "Cyber Hack",
                    "stamina_cost": 20,
                    "action_points": 1,
                    "success_chance": 75,
                    "description": "Exploit digital vulnerabilities"
                },
                {
                    "action": "Corporate Leverage",
                    "stamina_cost": 10,
                    "action_points": 1,
                    "success_chance": 65,
                    "description": "Use your corporate connections"
                }
            ])
        
        return base_options

class QuestProgression:
    """Long-form quest framework with 30-40 turn progression"""
    
    @dataclass
    class QuestArc:
        title: str
        description: str
        current_act: int = 1
        total_acts: int = 3
        turn_count: int = 0
        milestones: List[Dict[str, Any]] = None
        choices_made: List[Dict[str, Any]] = None
        
        def __post_init__(self):
            if self.milestones is None:
                self.milestones = []
            if self.choices_made is None:
                self.choices_made = []
    
    @staticmethod
    def get_scenario_quest_arc(scenario: str) -> QuestArc:
        """Initialize quest arc for scenario"""
        
        quest_configs = {
            "northern_realms": QuestArc(
                title="The Dragon's Legacy",
                description="Ancient dragon stirrings threaten the realm's stability",
                milestones=[
                    {"act": 1, "turn": 8, "event": "dragon_awakening"},
                    {"act": 2, "turn": 20, "event": "kingdom_alliance"},
                    {"act": 3, "turn": 35, "event": "final_confrontation"}
                ]
            ),
            "whispering_town": QuestArc(
                title="The Whispering Truth",
                description="Uncover the cosmic horror lurking beneath small-town normalcy",
                milestones=[
                    {"act": 1, "turn": 6, "event": "first_whispers"},
                    {"act": 2, "turn": 18, "event": "reality_fractures"},
                    {"act": 3, "turn": 32, "event": "cosmic_revelation"}
                ]
            ),
            "neo_tokyo": QuestArc(
                title="The Memory War",
                description="Fight for control of humanity's digital consciousness",
                milestones=[
                    {"act": 1, "turn": 7, "event": "corporate_discovery"},
                    {"act": 2, "turn": 22, "event": "data_heist"},
                    {"act": 3, "turn": 38, "event": "system_liberation"}
                ]
            )
        }
        
        return quest_configs.get(scenario, quest_configs["northern_realms"])

class SanitySystem:
    """Cosmic horror sanity and reality distortion mechanics"""
    
    @dataclass
    class SanityState:
        current_sanity: int = 100
        reality_anchor: int = 100
        cosmic_knowledge: int = 0
        corruption_level: int = 0
        
        def lose_sanity(self, amount: int, reason: str = "") -> str:
            """Lose sanity and return narrative effect"""
            self.current_sanity = max(0, self.current_sanity - amount)
            
            if self.current_sanity < 20:
                return "Reality fragments around you. The boundaries between possible and impossible blur."
            elif self.current_sanity < 50:
                return "Your mind struggles to process what you're experiencing."
            elif self.current_sanity < 80:
                return "A chill runs down your spine as something feels fundamentally wrong."
            else:
                return "You feel slightly unsettled."
        
        def gain_cosmic_knowledge(self, amount: int) -> str:
            """Gain forbidden knowledge with potential sanity cost"""
            self.cosmic_knowledge += amount
            
            if self.cosmic_knowledge > 50:
                sanity_loss = amount * 2
                self.current_sanity = max(0, self.current_sanity - sanity_loss)
                return f"The truth burns in your mind. You understand too much. (Sanity: -{sanity_loss})"
            else:
                return "You glimpse forbidden truths at the edge of understanding."
        
        def distort_reality(self, narrative: str) -> str:
            """Apply reality distortion effects to narrative text"""
            if self.current_sanity < 30:
                # Heavy distortion
                return narrative.replace("you", "ỵ̴̈o̵̤͝u̷̹̓").replace("the", "t̷̰̄h̶̰̋e̷̜͋")
            elif self.current_sanity < 60:
                # Medium distortion
                return narrative.replace(".", "...").replace("!", "?!")
            else:
                return narrative

# Scenario integration helper
class ScenarioManager:
    """Main interface for scenario-specific game mechanics"""
    
    def __init__(self, scenario_type: str):
        self.scenario_type = scenario_type
        self.scenario_data = ScenarioConfig.get_scenario_data()[scenario_type]
        self.quest_arc = QuestProgression.get_scenario_quest_arc(scenario_type)
        self.combat_resources = CombatSystem.CombatResources()
        
        # Initialize scenario-specific systems
        if scenario_type == "whispering_town":
            self.sanity_state = SanitySystem.SanityState()
        else:
            self.sanity_state = None
    
    def get_context_for_ai(self) -> Dict[str, Any]:
        """Provide scenario context to AI generation"""
        context = {
            "scenario": self.scenario_data.name,
            "genre": self.scenario_data.genre,
            "current_location": self.scenario_data.starting_location,
            "quest_arc": {
                "title": self.quest_arc.title,
                "act": self.quest_arc.current_act,
                "turn": self.quest_arc.turn_count
            },
            "combat_resources": {
                "stamina": self.combat_resources.stamina,
                "action_points": self.combat_resources.action_points
            }
        }
        
        if self.sanity_state:
            context["sanity"] = {
                "current": self.sanity_state.current_sanity,
                "cosmic_knowledge": self.sanity_state.cosmic_knowledge
            }
        
        return context 