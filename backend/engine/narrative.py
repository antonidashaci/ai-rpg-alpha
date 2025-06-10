"""
AI-RPG-Alpha: Advanced Narrative Engine

Sophisticated narrative generation system that creates dynamic, character-driven
stories with branching narratives, character arcs, and emergent storytelling.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
import json
from datetime import datetime

from backend.models.character import Character, PersonalityTrait, EmotionalState, RelationshipType
from backend.dao.memory import MemoryDAO
from backend.dao.game_state import GameStateDAO
from backend.ai.openai_client import OpenAIClient


class NarrativeTheme(Enum):
    """Overarching narrative themes that guide story generation"""
    HEROIC_JOURNEY = "heroic_journey"
    MYSTERY_INVESTIGATION = "mystery_investigation"
    POLITICAL_INTRIGUE = "political_intrigue"
    SURVIVAL_ADVENTURE = "survival_adventure"
    ROMANTIC_SUBPLOT = "romantic_subplot"
    REVENGE_STORY = "revenge_story"
    REDEMPTION_ARC = "redemption_arc"
    COMING_OF_AGE = "coming_of_age"
    COSMIC_HORROR = "cosmic_horror"
    SLICE_OF_LIFE = "slice_of_life"


class NarrativeTone(Enum):
    """Emotional tone that influences how events are presented"""
    EPIC = "epic"
    DARK = "dark"
    HUMOROUS = "humorous"
    MYSTERIOUS = "mysterious"
    ROMANTIC = "romantic"
    MELANCHOLIC = "melancholic"
    INSPIRING = "inspiring"
    TENSE = "tense"
    WHIMSICAL = "whimsical"
    GRITTY = "gritty"


class PlotPoint(Enum):
    """Key plot structure points for story development"""
    INCITING_INCIDENT = "inciting_incident"
    FIRST_PLOT_POINT = "first_plot_point"
    FIRST_PINCH_POINT = "first_pinch_point"
    MIDPOINT = "midpoint"
    SECOND_PINCH_POINT = "second_pinch_point"
    THIRD_PLOT_POINT = "third_plot_point"
    CLIMAX = "climax"
    RESOLUTION = "resolution"


@dataclass
class NarrativeArc:
    """A complete narrative arc with theme, characters, and progression"""
    id: str
    title: str
    theme: NarrativeTheme
    tone: NarrativeTone
    main_characters: List[str] = field(default_factory=list)
    current_act: int = 1
    current_plot_point: PlotPoint = PlotPoint.INCITING_INCIDENT
    story_threads: List[str] = field(default_factory=list)
    unresolved_tensions: List[str] = field(default_factory=list)
    foreshadowing_elements: List[str] = field(default_factory=list)
    completed: bool = False
    
    def advance_plot(self) -> bool:
        """Advance to next plot point"""
        plot_progression = [
            PlotPoint.INCITING_INCIDENT,
            PlotPoint.FIRST_PLOT_POINT,
            PlotPoint.FIRST_PINCH_POINT,
            PlotPoint.MIDPOINT,
            PlotPoint.SECOND_PINCH_POINT,
            PlotPoint.THIRD_PLOT_POINT,
            PlotPoint.CLIMAX,
            PlotPoint.RESOLUTION
        ]
        
        current_index = plot_progression.index(self.current_plot_point)
        if current_index < len(plot_progression) - 1:
            self.current_plot_point = plot_progression[current_index + 1]
            
            # Advance act at certain points
            if self.current_plot_point in [PlotPoint.FIRST_PLOT_POINT]:
                self.current_act = 2
            elif self.current_plot_point in [PlotPoint.THIRD_PLOT_POINT]:
                self.current_act = 3
            
            return True
        else:
            self.completed = True
            return False


@dataclass
class StoryElement:
    """Individual story elements that can be woven into narratives"""
    id: str
    element_type: str  # "character_introduction", "conflict", "revelation", etc.
    content: str
    characters_involved: List[str] = field(default_factory=list)
    emotional_weight: float = 0.5  # 0.0 to 1.0
    requires_setup: List[str] = field(default_factory=list)
    payoff_for: List[str] = field(default_factory=list)
    used: bool = False


@dataclass
class WorldBuilding:
    """Dynamic world building information"""
    locations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    factions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    history_events: List[Dict[str, Any]] = field(default_factory=list)
    cultural_elements: Dict[str, Any] = field(default_factory=dict)
    mysteries: List[Dict[str, Any]] = field(default_factory=list)
    legends: List[Dict[str, Any]] = field(default_factory=list)


class NarrativeEngine:
    """Advanced narrative generation and management system"""
    
    def __init__(
        self, 
        ai_client: OpenAIClient,
        memory_dao: MemoryDAO,
        game_state_dao: GameStateDAO
    ):
        self.ai_client = ai_client
        self.memory_dao = memory_dao
        self.game_state_dao = game_state_dao
        
        # Narrative state
        self.active_arcs: List[NarrativeArc] = []
        self.story_elements: List[StoryElement] = []
        self.world_building = WorldBuilding()
        
        # Generation settings
        self.narrative_complexity = 0.7  # 0.0 to 1.0
        self.character_focus = 0.8
        self.world_building_detail = 0.6
        
        self._initialize_world_building()
        self._load_story_elements()
    
    def _initialize_world_building(self):
        """Initialize rich world building elements"""
        # Detailed locations with atmosphere and secrets
        self.world_building.locations = {
            "whispering_woods": {
                "name": "Whispering Woods",
                "description": "Ancient forest where the trees murmur forgotten secrets",
                "atmosphere": "mystical",
                "notable_features": ["heartwood_tree", "moonstone_shrine", "silver_brook"],
                "inhabitants": ["dryad_spirits", "elder_hermit", "shadow_deer"],
                "dangers": ["phantom_wolves", "memory_mist", "twisting_paths"],
                "secrets": ["lost_civilization", "portal_network", "nature_magic"],
                "mood_modifiers": {"mystery": 0.8, "danger": 0.4, "magic": 0.9}
            },
            "ravens_hollow": {
                "name": "Raven's Hollow",
                "description": "A windswept mountain village shrouded in perpetual mist",
                "atmosphere": "foreboding",
                "notable_features": ["weathered_tower", "ancient_cemetery", "iron_bridge"],
                "inhabitants": ["village_elder", "mysterious_blacksmith", "lonely_innkeeper"],
                "dangers": ["mountain_spirits", "avalanche_risk", "cursed_artifacts"],
                "secrets": ["buried_treasure", "family_curses", "hidden_passages"],
                "mood_modifiers": {"mystery": 0.7, "danger": 0.6, "isolation": 0.8}
            },
            "crystal_sanctum": {
                "name": "Crystal Sanctum",
                "description": "Underground caverns filled with singing crystals",
                "atmosphere": "ethereal",
                "notable_features": ["resonance_chamber", "crystal_pools", "light_prisms"],
                "inhabitants": ["crystal_keeper", "echo_spirits", "stone_guardians"],
                "dangers": ["crystal_storms", "sonic_traps", "guardian_awakening"],
                "secrets": ["ancient_knowledge", "power_source", "dimensional_gateway"],
                "mood_modifiers": {"wonder": 0.9, "magic": 0.8, "ancient": 0.7}
            }
        }
        
        # Complex factions with relationships and agendas
        self.world_building.factions = {
            "dawn_sentinels": {
                "name": "Dawn Sentinels",
                "type": "holy_order",
                "goals": ["protect_realm", "preserve_knowledge", "battle_corruption"],
                "methods": ["righteous_combat", "divine_magic", "strategic_alliances"],
                "reputation": {"common_folk": 80, "nobility": 60, "outlaws": 20},
                "resources": "moderate",
                "key_figures": ["commander_lyara", "sage_aldwin", "healer_miranda"],
                "internal_conflicts": ["rigid_doctrine", "resource_shortage", "political_pressure"]
            },
            "shadow_covenant": {
                "name": "Shadow Covenant",
                "type": "secret_society",
                "goals": ["acquire_power", "manipulate_events", "preserve_secrets"],
                "methods": ["espionage", "blackmail", "subtle_influence"],
                "reputation": {"common_folk": 10, "nobility": 40, "underworld": 70},
                "resources": "extensive",
                "key_figures": ["shadowmaster_vex", "information_broker", "master_assassin"],
                "internal_conflicts": ["power_struggles", "conflicting_interests", "exposure_risk"]
            },
            "merchant_guild": {
                "name": "Gilded Path Trading Company",
                "type": "merchant_guild",
                "goals": ["maximize_profit", "expand_trade", "maintain_stability"],
                "methods": ["economic_pressure", "diplomatic_negotiation", "hired_protection"],
                "reputation": {"common_folk": 60, "nobility": 70, "travelers": 85},
                "resources": "vast",
                "key_figures": ["guild_master_thorn", "caravan_captain", "master_appraiser"],
                "internal_conflicts": ["competition", "corruption", "external_threats"]
            }
        }
        
        # Rich mysteries with interconnected clues
        self.world_building.mysteries = [
            {
                "id": "vanishing_memories",
                "title": "The Stolen Memories",
                "description": "People across the realm are losing specific memories",
                "complexity": "high",
                "clues": {
                    "primary": ["memory_gaps", "crystal_residue", "shared_dreams"],
                    "secondary": ["ancient_texts", "witness_accounts", "magical_traces"]
                },
                "red_herrings": ["mind_plague", "curse_theory", "mass_hysteria"],
                "suspects": ["rogue_mage", "artifact_influence", "dimensional_breach"],
                "resolution_paths": ["destroy_source", "reverse_spell", "embrace_change"],
                "story_impact": "world_changing"
            },
            {
                "id": "crown_of_storms",
                "title": "The Storm Crown Mystery",
                "description": "An ancient crown that controls weather has been stolen",
                "complexity": "medium",
                "clues": {
                    "primary": ["weather_anomalies", "theft_evidence", "royal_secrets"],
                    "secondary": ["historical_records", "witness_testimonies", "magical_signatures"]
                },
                "red_herrings": ["natural_phenomena", "political_conspiracy", "divine_intervention"],
                "suspects": ["ambitious_noble", "weather_cult", "foreign_agent"],
                "resolution_paths": ["recover_crown", "destroy_artifact", "negotiate_return"],
                "story_impact": "regional"
            }
        ]
    
    def _load_story_elements(self):
        """Load sophisticated story elements for narrative weaving"""
        # Character development elements
        character_elements = [
            StoryElement(
                id="mysterious_benefactor",
                element_type="character_development",
                content="A hooded figure has been helping you from the shadows",
                emotional_weight=0.7,
                requires_setup=["multiple_encounters"]
            ),
            StoryElement(
                id="rival_appears",
                element_type="character_introduction",
                content="Your past catches up as an old rival confronts you",
                emotional_weight=0.8,
                requires_setup=["established_reputation"]
            ),
            StoryElement(
                id="mentor_sacrifice",
                element_type="character_development",
                content="Your mentor makes a significant sacrifice for your growth",
                emotional_weight=0.95,
                requires_setup=["mentor_relationship"],
                payoff_for=["character_growth"]
            )
        ]
        
        # Plot development elements
        plot_elements = [
            StoryElement(
                id="hidden_agenda",
                element_type="plot_twist",
                content="Someone you trusted reveals their hidden agenda",
                emotional_weight=0.9,
                requires_setup=["trusted_ally"]
            ),
            StoryElement(
                id="ancient_prophecy",
                element_type="revelation",
                content="An ancient prophecy begins to make sense",
                emotional_weight=0.8,
                payoff_for=["mysterious_signs"]
            ),
            StoryElement(
                id="moral_crossroads",
                element_type="conflict",
                content="You face a decision that will define who you are",
                emotional_weight=0.95
            )
        ]
        
        # World expansion elements
        world_elements = [
            StoryElement(
                id="lost_civilization",
                element_type="world_building",
                content="Evidence of a lost civilization emerges",
                emotional_weight=0.6,
                payoff_for=["ancient_mysteries"]
            ),
            StoryElement(
                id="faction_conflict",
                element_type="political",
                content="Long-standing tensions between factions reach a breaking point",
                emotional_weight=0.7
            ),
            StoryElement(
                id="magical_discovery",
                element_type="world_building",
                content="A new form of magic is discovered",
                emotional_weight=0.8
            )
        ]
        
        self.story_elements.extend(character_elements + plot_elements + world_elements)
    
    def generate_enhanced_quest(
        self,
        theme: NarrativeTheme,
        location: str,
        characters_involved: List[str] = None,
        complexity_level: float = 0.7
    ) -> Dict[str, Any]:
        """Generate a sophisticated, multi-layered quest"""
        
        characters_involved = characters_involved or []
        
        # Select appropriate story elements for the quest
        quest_elements = self._select_quest_elements(theme, complexity_level)
        
        # Build the quest structure
        quest_structure = self._build_quest_structure(theme, quest_elements)
        
        # Generate dynamic objectives
        objectives = self._generate_dynamic_objectives(theme, location, characters_involved)
        
        # Create branching narrative paths
        narrative_branches = self._create_narrative_branches(quest_structure, characters_involved)
        
        # Add meaningful consequences
        consequences = self._design_meaningful_consequences(theme, quest_elements)
        
        # Generate rich descriptions
        descriptions = self._generate_rich_descriptions(theme, location, quest_elements)
        
        return {
            "id": f"quest_{datetime.now().timestamp()}",
            "title": descriptions["title"],
            "theme": theme.value,
            "complexity": complexity_level,
            "location": location,
            "characters_involved": characters_involved,
            "main_objective": descriptions["main_objective"],
            "sub_objectives": objectives,
            "narrative_branches": narrative_branches,
            "story_elements": [e.id for e in quest_elements],
            "consequences": consequences,
            "descriptions": descriptions,
            "estimated_duration": self._estimate_quest_duration(complexity_level, len(objectives)),
            "prerequisite_flags": self._determine_prerequisites(quest_elements),
            "unlocks": self._determine_unlocks(theme, quest_elements)
        }
    
    def _select_quest_elements(self, theme: NarrativeTheme, complexity: float) -> List[StoryElement]:
        """Select appropriate story elements for quest theme and complexity"""
        element_count = int(2 + complexity * 3)  # 2-5 elements based on complexity
        
        # Filter elements by theme compatibility
        compatible_elements = []
        for element in self.story_elements:
            if not element.used and self._is_element_compatible(element, theme):
                compatible_elements.append(element)
        
        # Select diverse elements
        selected = []
        element_types_used = set()
        
        for element in compatible_elements:
            if len(selected) >= element_count:
                break
            
            # Ensure diversity in element types
            if element.element_type not in element_types_used or len(selected) < 2:
                selected.append(element)
                element_types_used.add(element.element_type)
        
        return selected
    
    def _is_element_compatible(self, element: StoryElement, theme: NarrativeTheme) -> bool:
        """Check if story element is compatible with quest theme"""
        compatibility_map = {
            NarrativeTheme.HEROIC_JOURNEY: ["character_development", "conflict", "revelation"],
            NarrativeTheme.MYSTERY_INVESTIGATION: ["revelation", "plot_twist", "world_building"],
            NarrativeTheme.POLITICAL_INTRIGUE: ["political", "plot_twist", "character_development"],
            NarrativeTheme.SURVIVAL_ADVENTURE: ["conflict", "world_building", "character_development"],
            NarrativeTheme.REDEMPTION_ARC: ["character_development", "conflict", "revelation"]
        }
        
        compatible_types = compatibility_map.get(theme, ["any"])
        return "any" in compatible_types or element.element_type in compatible_types
    
    def _build_quest_structure(self, theme: NarrativeTheme, elements: List[StoryElement]) -> Dict[str, Any]:
        """Build the overall structure of the quest"""
        structure_templates = {
            NarrativeTheme.HEROIC_JOURNEY: {
                "acts": ["call_to_adventure", "trials", "transformation", "return"],
                "pacing": "escalating",
                "climax_type": "heroic_confrontation"
            },
            NarrativeTheme.MYSTERY_INVESTIGATION: {
                "acts": ["discovery", "investigation", "revelation", "resolution"],
                "pacing": "puzzle_solving",
                "climax_type": "truth_revealed"
            },
            NarrativeTheme.POLITICAL_INTRIGUE: {
                "acts": ["introduction", "maneuvering", "betrayal", "power_shift"],
                "pacing": "tension_building",
                "climax_type": "dramatic_confrontation"
            }
        }
        
        return structure_templates.get(theme, structure_templates[NarrativeTheme.HEROIC_JOURNEY])
    
    def _generate_dynamic_objectives(
        self, 
        theme: NarrativeTheme, 
        location: str, 
        characters: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate dynamic objectives that adapt to the story"""
        objectives = []
        
        # Theme-specific objective templates
        objective_templates = {
            NarrativeTheme.HEROIC_JOURNEY: [
                "Prove your worth through {challenge}",
                "Protect {target} from {threat}",
                "Discover the truth about {mystery}",
                "Master {skill} to overcome {obstacle}"
            ],
            NarrativeTheme.MYSTERY_INVESTIGATION: [
                "Gather clues about {mystery}",
                "Interview {witness} about {event}",
                "Examine {evidence} for {information}",
                "Uncover the connection between {element1} and {element2}"
            ],
            NarrativeTheme.POLITICAL_INTRIGUE: [
                "Gain the trust of {faction}",
                "Expose {villain}'s true motives",
                "Navigate the politics of {location}",
                "Secure {resource} without detection"
            ]
        }
        
        templates = objective_templates.get(theme, objective_templates[NarrativeTheme.HEROIC_JOURNEY])
        
        # Generate 2-4 objectives
        for i in range(random.randint(2, 4)):
            template = random.choice(templates)
            
            # Fill in template variables
            objective_text = self._fill_objective_template(template, location, characters)
            
            objectives.append({
                "id": f"obj_{i+1}",
                "description": objective_text,
                "type": "main" if i == 0 else "secondary",
                "optional": i > 2,
                "completion_criteria": self._generate_completion_criteria(objective_text),
                "rewards": self._generate_objective_rewards(i == 0)
            })
        
        return objectives
    
    def _fill_objective_template(self, template: str, location: str, characters: List[str]) -> str:
        """Fill in objective template with contextual information"""
        # Simple template filling - in real implementation, use more sophisticated NLG
        replacements = {
            "{challenge}": random.choice(["a trial of courage", "a test of wisdom", "a feat of strength"]),
            "{target}": random.choice(characters) if characters else "the innocent",
            "{threat}": random.choice(["ancient evil", "corrupted guardian", "political conspiracy"]),
            "{mystery}": random.choice(["the vanishing memories", "the stolen artifact", "the cursed bloodline"]),
            "{skill}": random.choice(["ancient magic", "diplomatic finesse", "combat mastery"]),
            "{obstacle}": random.choice(["the guardian's trial", "the political maze", "the cursed barrier"]),
            "{witness}": random.choice(characters) if characters else "a mysterious informant",
            "{event}": random.choice(["the theft", "the disappearance", "the betrayal"]),
            "{evidence}": random.choice(["the torn cloak", "the cryptic message", "the bloodstained weapon"]),
            "{information}": random.choice(["the culprit's identity", "the hidden motive", "the secret location"]),
            "{element1}": random.choice(["the missing person", "the stolen item", "the strange phenomenon"]),
            "{element2}": random.choice(["the ancient prophecy", "the political upheaval", "the family curse"]),
            "{faction}": random.choice(["the Dawn Sentinels", "the Shadow Covenant", "the Merchant Guild"]),
            "{villain}": random.choice(characters) if characters else "the hidden mastermind",
            "{location}": location,
            "{resource}": random.choice(["critical information", "a powerful artifact", "political leverage"])
        }
        
        result = template
        for placeholder, replacement in replacements.items():
            result = result.replace(placeholder, replacement)
        
        return result
    
    def _generate_completion_criteria(self, objective_text: str) -> List[str]:
        """Generate specific completion criteria for objectives"""
        # Extract key verbs and nouns to create criteria
        criteria = []
        
        if "gather" in objective_text.lower():
            criteria.append("collect_minimum_clues")
        if "interview" in objective_text.lower():
            criteria.append("successful_conversation")
        if "protect" in objective_text.lower():
            criteria.append("prevent_harm_to_target")
        if "discover" in objective_text.lower():
            criteria.append("reveal_hidden_information")
        if "master" in objective_text.lower():
            criteria.append("demonstrate_skill_proficiency")
        
        return criteria or ["complete_associated_task"]
    
    def _generate_objective_rewards(self, is_main_objective: bool) -> Dict[str, Any]:
        """Generate rewards for objective completion"""
        base_xp = 50 if is_main_objective else 25
        base_gold = 30 if is_main_objective else 15
        
        rewards = {
            "experience": base_xp + random.randint(-10, 20),
            "gold": base_gold + random.randint(-5, 15),
            "reputation": {}
        }
        
        # Add faction reputation changes
        if random.random() < 0.6:
            faction = random.choice(["dawn_sentinels", "shadow_covenant", "merchant_guild"])
            rewards["reputation"][faction] = random.randint(5, 15)
        
        # Add special rewards for main objectives
        if is_main_objective and random.random() < 0.4:
            rewards["special_items"] = [
                random.choice(["Enchanted Pendant", "Ancient Map", "Sealed Letter", "Mystical Tome"])
            ]
        
        return rewards
    
    def _create_narrative_branches(
        self, 
        quest_structure: Dict[str, Any], 
        characters: List[str]
    ) -> Dict[str, Any]:
        """Create branching narrative paths within the quest"""
        branches = {
            "main_path": {
                "description": "The straightforward approach to completing the quest",
                "difficulty": "medium",
                "requirements": [],
                "consequences": {"reputation": {"general": 10}}
            }
        }
        
        # Add alternative approaches
        if random.random() < 0.7:
            branches["diplomatic_path"] = {
                "description": "Resolve the situation through negotiation and diplomacy",
                "difficulty": "easy",
                "requirements": ["charisma >= 12"],
                "consequences": {"reputation": {"nobles": 15}, "gold": -50}
            }
        
        if random.random() < 0.6:
            branches["stealth_path"] = {
                "description": "Complete the quest through cunning and stealth",
                "difficulty": "hard",
                "requirements": ["stealth_skill", "appropriate_equipment"],
                "consequences": {"reputation": {"underworld": 10}, "secrecy_maintained": True}
            }
        
        if random.random() < 0.5:
            branches["aggressive_path"] = {
                "description": "Take a direct, forceful approach to the problem",
                "difficulty": "medium",
                "requirements": ["combat_ready"],
                "consequences": {"reputation": {"military": 10}, "collateral_damage": True}
            }
        
        return branches
    
    def _design_meaningful_consequences(
        self, 
        theme: NarrativeTheme, 
        elements: List[StoryElement]
    ) -> Dict[str, Any]:
        """Design consequences that have lasting impact on the story"""
        consequences = {
            "immediate": {},
            "delayed": {},
            "story_flags": [],
            "world_changes": []
        }
        
        # Theme-based consequences
        if theme == NarrativeTheme.HEROIC_JOURNEY:
            consequences["story_flags"].extend(["hero_reputation", "call_to_greater_destiny"])
            consequences["world_changes"].append("hero_legend_begins")
        elif theme == NarrativeTheme.MYSTERY_INVESTIGATION:
            consequences["story_flags"].extend(["truth_seeker", "mystery_solver_reputation"])
            consequences["world_changes"].append("mystery_partially_solved")
        elif theme == NarrativeTheme.POLITICAL_INTRIGUE:
            consequences["story_flags"].extend(["political_player", "faction_attention"])
            consequences["world_changes"].append("political_landscape_shifts")
        
        # Element-based consequences
        for element in elements:
            if element.element_type == "character_development":
                consequences["story_flags"].append("character_growth")
            elif element.element_type == "plot_twist":
                consequences["story_flags"].append("plot_revealed")
                consequences["world_changes"].append("truth_changes_everything")
        
        # Add delayed consequences
        if random.random() < 0.4:
            consequences["delayed"]["turn_trigger"] = random.randint(3, 8)
            consequences["delayed"]["event"] = random.choice([
                "unexpected_ally_appears",
                "consequences_return",
                "new_opportunity_emerges",
                "past_actions_remembered"
            ])
        
        return consequences
    
    def _generate_rich_descriptions(
        self, 
        theme: NarrativeTheme, 
        location: str, 
        elements: List[StoryElement]
    ) -> Dict[str, str]:
        """Generate rich, atmospheric descriptions for the quest"""
        
        # Theme-based title templates
        title_templates = {
            NarrativeTheme.HEROIC_JOURNEY: [
                "The {adjective} {noun}",
                "{location}'s {challenge}",
                "The Quest for {object}"
            ],
            NarrativeTheme.MYSTERY_INVESTIGATION: [
                "The Mystery of {mystery}",
                "{location}'s Secret",
                "The Case of the {adjective} {noun}"
            ],
            NarrativeTheme.POLITICAL_INTRIGUE: [
                "Shadows over {location}",
                "The {adjective} Conspiracy",
                "{faction}'s Gambit"
            ]
        }
        
        # Generate title
        templates = title_templates.get(theme, title_templates[NarrativeTheme.HEROIC_JOURNEY])
        title_template = random.choice(templates)
        
        # Fill in title variables
        title_vars = {
            "{adjective}": random.choice(["Ancient", "Lost", "Hidden", "Forgotten", "Cursed", "Sacred"]),
            "{noun}": random.choice(["Legacy", "Truth", "Power", "Secret", "Destiny", "Crown"]),
            "{location}": location.replace("_", " ").title(),
            "{challenge}": random.choice(["Trial", "Test", "Challenge", "Ordeal"]),
            "{object}": random.choice(["Crown", "Artifact", "Tome", "Key", "Relic"]),
            "{mystery}": random.choice(["Vanishing", "Betrayal", "Disappearance", "Curse"]),
            "{faction}": random.choice(["Shadow", "Dawn", "Ancient"])
        }
        
        title = title_template
        for var, replacement in title_vars.items():
            title = title.replace(var, replacement)
        
        # Generate main objective description
        main_objective = self._generate_main_objective_description(theme, location, elements)
        
        # Generate atmospheric intro
        intro = self._generate_atmospheric_intro(theme, location)
        
        return {
            "title": title,
            "main_objective": main_objective,
            "intro": intro,
            "location_description": self._get_enhanced_location_description(location),
            "atmosphere": random.choice(["tense", "mysterious", "epic", "melancholic", "hopeful"])
        }
    
    def _generate_main_objective_description(
        self, 
        theme: NarrativeTheme, 
        location: str, 
        elements: List[StoryElement]
    ) -> str:
        """Generate the main objective description"""
        
        objective_templates = {
            NarrativeTheme.HEROIC_JOURNEY: [
                "Embark on a heroic quest to {goal} and prove your worth as a true champion.",
                "Rise to meet the challenge that will define your destiny in {location}.",
                "Accept the call to adventure and become the hero this land needs."
            ],
            NarrativeTheme.MYSTERY_INVESTIGATION: [
                "Unravel the mystery that has shrouded {location} in secrets and shadows.",
                "Investigate the strange events and discover the truth behind {mystery}.",
                "Follow the clues to solve a puzzle that has confounded others for years."
            ],
            NarrativeTheme.POLITICAL_INTRIGUE: [
                "Navigate the treacherous waters of politics in {location}.",
                "Uncover the conspiracy that threatens to upset the balance of power.",
                "Play the game of politics to achieve your goals without being destroyed."
            ]
        }
        
        templates = objective_templates.get(theme, objective_templates[NarrativeTheme.HEROIC_JOURNEY])
        template = random.choice(templates)
        
        # Fill in variables
        return template.replace("{location}", location.replace("_", " ").title()).replace(
            "{goal}", "restore balance"
        ).replace("{mystery}", "the vanishing memories")
    
    def _generate_atmospheric_intro(self, theme: NarrativeTheme, location: str) -> str:
        """Generate an atmospheric introduction to the quest"""
        
        intro_templates = {
            NarrativeTheme.HEROIC_JOURNEY: [
                "The call to adventure echoes through {location}, and destiny awaits your answer.",
                "In {location}, heroes are born from ordinary souls who dare to act.",
                "The realm needs a champion, and fate has chosen you to answer that need."
            ],
            NarrativeTheme.MYSTERY_INVESTIGATION: [
                "Something is amiss in {location}, and only the truth can set things right.",
                "Whispers and rumors swirl around {location} like morning mist.",
                "The answers you seek lie hidden in the shadows of {location}."
            ],
            NarrativeTheme.POLITICAL_INTRIGUE: [
                "In {location}, every smile hides a dagger and every word carries weight.",
                "The political landscape of {location} shifts like quicksand beneath your feet.",
                "Power plays and hidden agendas shape the fate of {location}."
            ]
        }
        
        templates = intro_templates.get(theme, intro_templates[NarrativeTheme.HEROIC_JOURNEY])
        template = random.choice(templates)
        
        return template.replace("{location}", location.replace("_", " ").title())
    
    def _get_enhanced_location_description(self, location: str) -> str:
        """Get enhanced description of the location"""
        location_info = self.world_building.locations.get(location, {})
        
        if not location_info:
            return f"The area known as {location.replace('_', ' ').title()}"
        
        description = location_info.get("description", "A mysterious place")
        atmosphere = location_info.get("atmosphere", "neutral")
        
        # Enhance with atmospheric details
        atmospheric_additions = {
            "mysterious": "Shadows seem to dance at the edge of your vision",
            "foreboding": "An oppressive weight hangs in the air",
            "ethereal": "Reality feels thin and malleable here",
            "mystical": "Magic thrums in the very air around you"
        }
        
        enhancement = atmospheric_additions.get(atmosphere, "")
        
        return f"{description}. {enhancement}".strip()
    
    def _estimate_quest_duration(self, complexity: float, objective_count: int) -> str:
        """Estimate how long the quest will take"""
        base_time = objective_count * 2  # 2 turns per objective
        complexity_modifier = complexity * 3
        
        total_turns = int(base_time + complexity_modifier)
        
        if total_turns <= 3:
            return "short"
        elif total_turns <= 6:
            return "medium"
        else:
            return "long"
    
    def _determine_prerequisites(self, elements: List[StoryElement]) -> List[str]:
        """Determine what prerequisites the quest requires"""
        prerequisites = []
        
        for element in elements:
            prerequisites.extend(element.requires_setup)
        
        # Remove duplicates
        return list(set(prerequisites))
    
    def _determine_unlocks(self, theme: NarrativeTheme, elements: List[StoryElement]) -> List[str]:
        """Determine what the quest unlocks upon completion"""
        unlocks = []
        
        # Theme-based unlocks
        theme_unlocks = {
            NarrativeTheme.HEROIC_JOURNEY: ["hero_reputation", "advanced_training"],
            NarrativeTheme.MYSTERY_INVESTIGATION: ["investigator_skills", "hidden_knowledge"],
            NarrativeTheme.POLITICAL_INTRIGUE: ["political_connections", "diplomatic_immunity"]
        }
        
        unlocks.extend(theme_unlocks.get(theme, []))
        
        # Element-based unlocks
        for element in elements:
            unlocks.extend(element.payoff_for)
        
        return list(set(unlocks))  # Remove duplicates 