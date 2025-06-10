"""
AI-RPG-Alpha: Advanced Narrative Engine

Sophisticated narrative generation system that creates dynamic, character-driven
stories with branching narratives, character arcs, and emergent storytelling.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random
from datetime import datetime


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


@dataclass
class EnhancedQuest:
    """Sophisticated quest with multiple layers and branching narratives"""
    id: str
    title: str
    theme: NarrativeTheme
    complexity_level: float
    
    # Multi-layered objectives
    primary_objective: str
    secondary_objectives: List[str] = field(default_factory=list)
    hidden_objectives: List[str] = field(default_factory=list)
    
    # Branching narrative paths
    narrative_branches: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Character integration
    main_characters: List[str] = field(default_factory=list)
    character_arcs: Dict[str, List[str]] = field(default_factory=dict)
    
    # World building elements
    location_details: Dict[str, Any] = field(default_factory=dict)
    lore_elements: List[str] = field(default_factory=list)
    
    # Dynamic consequences
    immediate_consequences: Dict[str, Any] = field(default_factory=dict)
    long_term_consequences: Dict[str, Any] = field(default_factory=dict)
    
    # Narrative state
    current_chapter: int = 1
    plot_developments: List[str] = field(default_factory=list)
    unresolved_tensions: List[str] = field(default_factory=list)


class AdvancedNarrativeEngine:
    """Enhanced narrative generation system"""
    
    def __init__(self):
        self.active_themes = []
        self.character_relationships = {}
        self.world_lore = {}
        self.narrative_history = []
        
        # Initialize rich world building
        self._initialize_enhanced_world()
    
    def _initialize_enhanced_world(self):
        """Initialize rich world building elements"""
        self.world_lore = {
            "locations": {
                "whispering_woods": {
                    "name": "Whispering Woods",
                    "description": "An ancient forest where the trees themselves seem to remember old secrets",
                    "atmosphere": "mystical_foreboding",
                    "secrets": [
                        "Hidden grove of silver trees that grant visions",
                        "Ruins of an ancient druid circle",
                        "Portal network connecting to other realms"
                    ],
                    "inhabitants": {
                        "Elder Oakenheart": {
                            "role": "ancient_guardian",
                            "personality": "wise_but_cryptic",
                            "secret": "Was once human, transformed by forest magic"
                        },
                        "Shadow Wolves": {
                            "role": "mysterious_threat",
                            "personality": "intelligent_predators",
                            "secret": "Guardians of the portal network"
                        }
                    },
                    "mood_shifts": {
                        "day": "Peaceful but watchful",
                        "night": "Alive with ancient magic",
                        "storm": "Chaotic and dangerous"
                    }
                },
                "trading_post": {
                    "name": "Crossroads Trading Post",
                    "description": "A bustling hub where information is as valuable as gold",
                    "atmosphere": "lively_with_undercurrents",
                    "secrets": [
                        "Secret meeting place for spy networks",
                        "Hidden vault containing stolen artifacts",
                        "Innkeeper has connections to royal court"
                    ],
                    "inhabitants": {
                        "Mira Goldwhistle": {
                            "role": "innkeeper_information_broker",
                            "personality": "cheerful_but_calculating",
                            "secret": "Former royal spy maintaining intelligence network"
                        },
                        "The Hooded Stranger": {
                            "role": "mysterious_regular",
                            "personality": "ominous_but_helpful",
                            "secret": "Exiled noble seeking redemption"
                        }
                    }
                }
            },
            "factions": {
                "Order of the Crimson Dawn": {
                    "type": "religious_military",
                    "goals": ["Protect realm from dark magic", "Preserve ancient knowledge"],
                    "methods": ["Holy combat", "Magical research", "Political influence"],
                    "internal_conflicts": [
                        "Purists vs pragmatists on magic use",
                        "Young knights challenging old traditions",
                        "Resource allocation disputes"
                    ],
                    "key_figures": {
                        "Commander Lyara": "Idealistic leader struggling with harsh realities",
                        "Brother Marcus": "Scholar who discovered disturbing ancient texts",
                        "Sister Elena": "Healer questioning the order's violent methods"
                    }
                },
                "Shadowveil Collective": {
                    "type": "information_network",
                    "goals": ["Control information flow", "Profit from secrets", "Maintain balance of power"],
                    "methods": ["Espionage", "Blackmail", "Strategic manipulation"],
                    "internal_conflicts": [
                        "Power struggle between regional spymasters",
                        "Moral agents vs ruthless operatives",
                        "External pressure from government crackdowns"
                    ]
                }
            },
            "mysteries": {
                "The Vanishing Memories": {
                    "description": "People across the realm are losing specific memories",
                    "clues": {
                        "obvious": ["Memory gaps in similar timeframes", "Strange crystalline residue found"],
                        "hidden": ["Dreams shared between victims", "Ancient texts mention similar events"],
                        "red_herrings": ["Mind plague theory", "Political conspiracy theories"]
                    },
                    "truth": "Ancient artifact fragments affecting collective consciousness",
                    "implications": "Could either restore lost knowledge or erase history"
                }
            }
        }
    
    def generate_sophisticated_quest(
        self,
        player_context: Dict[str, Any],
        theme_preference: NarrativeTheme = None,
        complexity: float = 0.7
    ) -> EnhancedQuest:
        """Generate a sophisticated, multi-layered quest"""
        
        # Determine theme based on player context and preferences
        theme = theme_preference or self._select_optimal_theme(player_context)
        
        # Build quest foundation
        quest_foundation = self._build_quest_foundation(theme, player_context, complexity)
        
        # Generate branching narrative structure
        narrative_branches = self._create_branching_narrative(theme, quest_foundation)
        
        # Integrate character development
        character_integration = self._integrate_character_development(quest_foundation, player_context)
        
        # Add world-building elements
        world_elements = self._integrate_world_building(quest_foundation)
        
        # Design consequence system
        consequences = self._design_consequence_system(theme, complexity)
        
        return EnhancedQuest(
            id=f"enhanced_quest_{int(datetime.now().timestamp())}",
            title=quest_foundation["title"],
            theme=theme,
            complexity_level=complexity,
            primary_objective=quest_foundation["primary_objective"],
            secondary_objectives=quest_foundation["secondary_objectives"],
            hidden_objectives=quest_foundation["hidden_objectives"],
            narrative_branches=narrative_branches,
            main_characters=character_integration["main_characters"],
            character_arcs=character_integration["character_arcs"],
            location_details=world_elements["location_details"],
            lore_elements=world_elements["lore_elements"],
            immediate_consequences=consequences["immediate"],
            long_term_consequences=consequences["long_term"]
        )
    
    def _select_optimal_theme(self, player_context: Dict[str, Any]) -> NarrativeTheme:
        """Select the most appropriate theme based on player context"""
        
        # Analyze player preferences and history
        player_choices = player_context.get("recent_choices", [])
        player_stats = player_context.get("stats", {})
        
        theme_weights = {
            NarrativeTheme.HEROIC_JOURNEY: 0.3,
            NarrativeTheme.MYSTERY_INVESTIGATION: 0.3,
            NarrativeTheme.POLITICAL_INTRIGUE: 0.2,
            NarrativeTheme.SURVIVAL_ADVENTURE: 0.2
        }
        
        # Adjust weights based on player behavior
        for choice in player_choices:
            if "investigate" in choice.lower() or "examine" in choice.lower():
                theme_weights[NarrativeTheme.MYSTERY_INVESTIGATION] += 0.2
            elif "fight" in choice.lower() or "attack" in choice.lower():
                theme_weights[NarrativeTheme.HEROIC_JOURNEY] += 0.2
            elif "negotiate" in choice.lower() or "talk" in choice.lower():
                theme_weights[NarrativeTheme.POLITICAL_INTRIGUE] += 0.2
        
        # Select theme based on weighted random choice
        themes = list(theme_weights.keys())
        weights = list(theme_weights.values())
        
        return random.choices(themes, weights=weights)[0]
    
    def _build_quest_foundation(
        self, 
        theme: NarrativeTheme, 
        player_context: Dict[str, Any], 
        complexity: float
    ) -> Dict[str, Any]:
        """Build the foundation of the quest"""
        
        # Theme-specific quest templates
        quest_templates = {
            NarrativeTheme.HEROIC_JOURNEY: {
                "title_patterns": [
                    "The {adjective} {noun}",
                    "Quest for the {object}",
                    "{location}'s Champion"
                ],
                "primary_objectives": [
                    "Prove your heroism by {heroic_deed}",
                    "Defend {location} from {threat}",
                    "Restore {object} to its rightful place"
                ],
                "secondary_objectives": [
                    "Gather allies for the final confrontation",
                    "Master {skill} to overcome challenges",
                    "Uncover the truth behind {mystery}"
                ]
            },
            NarrativeTheme.MYSTERY_INVESTIGATION: {
                "title_patterns": [
                    "The Mystery of {mystery}",
                    "{location}'s Secret",
                    "The Case of the {adjective} {noun}"
                ],
                "primary_objectives": [
                    "Solve the mystery of {mystery}",
                    "Find the truth behind {event}",
                    "Expose the real {culprit}"
                ],
                "secondary_objectives": [
                    "Gather evidence from {location}",
                    "Interview {witness} about {event}",
                    "Follow the trail of {clue}"
                ]
            },
            NarrativeTheme.POLITICAL_INTRIGUE: {
                "title_patterns": [
                    "Shadows over {location}",
                    "The {faction} Conspiracy",
                    "Web of {emotion}"
                ],
                "primary_objectives": [
                    "Navigate the political maze of {location}",
                    "Uncover {faction}'s true agenda",
                    "Secure {resource} through diplomacy"
                ],
                "secondary_objectives": [
                    "Gain the trust of {ally}",
                    "Expose {enemy}'s weakness",
                    "Form alliance with {faction}"
                ]
            }
        }
        
        template = quest_templates[theme]
        
        # Generate title
        title_pattern = random.choice(template["title_patterns"])
        title = self._fill_template_variables(title_pattern, player_context)
        
        # Generate objectives
        primary_obj = random.choice(template["primary_objectives"])
        primary_objective = self._fill_template_variables(primary_obj, player_context)
        
        secondary_objectives = []
        for _ in range(int(1 + complexity * 2)):  # 1-3 secondary objectives
            sec_obj = random.choice(template["secondary_objectives"])
            secondary_objectives.append(self._fill_template_variables(sec_obj, player_context))
        
        # Generate hidden objectives based on complexity
        hidden_objectives = []
        if complexity > 0.6:
            hidden_objectives = self._generate_hidden_objectives(theme, complexity)
        
        return {
            "title": title,
            "primary_objective": primary_objective,
            "secondary_objectives": secondary_objectives,
            "hidden_objectives": hidden_objectives
        }
    
    def _fill_template_variables(self, template: str, context: Dict[str, Any]) -> str:
        """Fill template variables with contextual information"""
        
        current_location = context.get("location", "whispering_woods")
        
        variable_map = {
            "{adjective}": random.choice(["Ancient", "Lost", "Hidden", "Cursed", "Sacred", "Forgotten"]),
            "{noun}": random.choice(["Legacy", "Truth", "Crown", "Artifact", "Secret", "Power"]),
            "{object}": random.choice(["Sacred Relic", "Lost Crown", "Ancient Tome", "Magical Key"]),
            "{location}": self.world_lore["locations"][current_location]["name"],
            "{heroic_deed}": random.choice(["saving the innocent", "defeating ancient evil", "restoring balance"]),
            "{threat}": random.choice(["dark sorcerer", "corrupted guardian", "invading army"]),
            "{skill}": random.choice(["ancient magic", "diplomatic arts", "combat mastery"]),
            "{mystery}": random.choice(["vanishing memories", "cursed bloodline", "stolen artifact"]),
            "{event}": random.choice(["betrayal", "disappearance", "theft", "curse"]),
            "{culprit}": random.choice(["hidden mastermind", "corrupt official", "ancient enemy"]),
            "{witness}": random.choice(["traveling merchant", "village elder", "mysterious stranger"]),
            "{clue}": random.choice(["bloodstained letter", "magical residue", "witness testimony"]),
            "{faction}": random.choice(["Order of the Crimson Dawn", "Shadowveil Collective"]),
            "{emotion}": random.choice(["Betrayal", "Deception", "Ambition"]),
            "{resource}": random.choice(["ancient knowledge", "political favor", "magical artifact"]),
            "{ally}": random.choice(["faction leader", "influential noble", "wise sage"]),
            "{enemy}": random.choice(["political rival", "corrupt minister", "foreign agent"])
        }
        
        result = template
        for variable, replacement in variable_map.items():
            result = result.replace(variable, replacement)
        
        return result
    
    def _generate_hidden_objectives(self, theme: NarrativeTheme, complexity: float) -> List[str]:
        """Generate hidden objectives that add depth to the quest"""
        
        hidden_objective_pools = {
            NarrativeTheme.HEROIC_JOURNEY: [
                "Discover your true heritage",
                "Forge an unlikely alliance",
                "Overcome a personal fear or weakness",
                "Make a difficult moral choice"
            ],
            NarrativeTheme.MYSTERY_INVESTIGATION: [
                "Uncover a conspiracy within a conspiracy",
                "Protect a key witness from elimination",
                "Discover the investigator is connected to the case",
                "Realize the mystery was a distraction from a larger plot"
            ],
            NarrativeTheme.POLITICAL_INTRIGUE: [
                "Identify the puppet master behind the scenes",
                "Navigate a double agent's conflicted loyalties",
                "Prevent a war through secret negotiations",
                "Expose corruption at the highest levels"
            ]
        }
        
        pool = hidden_objective_pools.get(theme, hidden_objective_pools[NarrativeTheme.HEROIC_JOURNEY])
        num_hidden = int(complexity * 2)  # 0-2 hidden objectives
        
        return random.sample(pool, min(num_hidden, len(pool)))
    
    def _create_branching_narrative(self, theme: NarrativeTheme, foundation: Dict[str, Any]) -> Dict[str, Any]:
        """Create sophisticated branching narrative structure"""
        
        branches = {
            "diplomatic_approach": {
                "name": "The Diplomatic Path",
                "description": "Resolve conflicts through negotiation and compromise",
                "requirements": {"charisma": 12, "reputation": {"any_faction": 10}},
                "advantages": ["Preserves relationships", "Unlocks peaceful solutions"],
                "challenges": ["Time-consuming", "Requires careful word choice"],
                "exclusive_outcomes": ["peaceful_resolution", "improved_faction_relations"]
            },
            "direct_action": {
                "name": "The Direct Approach",
                "description": "Take decisive action to achieve objectives quickly",
                "requirements": {"combat_skill": 10, "courage": "high"},
                "advantages": ["Quick resolution", "Clear outcomes"],
                "challenges": ["Higher risk", "Potential collateral damage"],
                "exclusive_outcomes": ["reputation_for_boldness", "simplified_conflicts"]
            },
            "investigative_method": {
                "name": "The Investigative Path",
                "description": "Gather information and plan carefully before acting",
                "requirements": {"intelligence": 12, "patience": "high"},
                "advantages": ["Better understanding", "Prepared for complications"],
                "challenges": ["Time investment", "Analysis paralysis risk"],
                "exclusive_outcomes": ["deep_knowledge", "strategic_advantages"]
            }
        }
        
        # Add theme-specific branches
        if theme == NarrativeTheme.MYSTERY_INVESTIGATION:
            branches["red_herring_chase"] = {
                "name": "Following False Leads",
                "description": "Pursue initial evidence that leads to unexpected discoveries",
                "requirements": {"persistence": "high"},
                "advantages": ["Uncovers hidden plots", "Builds investigative reputation"],
                "challenges": ["Wastes initial time", "Creates confusion"],
                "exclusive_outcomes": ["bonus_mystery_solved", "investigator_reputation"]
            }
        
        elif theme == NarrativeTheme.POLITICAL_INTRIGUE:
            branches["manipulation_game"] = {
                "name": "The Manipulation Game",
                "description": "Use others' ambitions and weaknesses against them",
                "requirements": {"cunning": "high", "moral_flexibility": "high"},
                "advantages": ["Achieves goals with minimal personal risk", "Gains leverage"],
                "challenges": ["Moral complexity", "Risk of exposure"],
                "exclusive_outcomes": ["master_manipulator_reputation", "complex_web_of_debts"]
            }
        
        return branches
    
    def _integrate_character_development(
        self, 
        foundation: Dict[str, Any], 
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate rich character development into the quest"""
        
        # Select main characters for the quest
        available_characters = list(self.world_lore["locations"].values())
        main_characters = []
        character_arcs = {}
        
        # Add 1-3 main characters based on complexity
        for location_data in available_characters[:2]:
            for char_name, char_data in location_data.get("inhabitants", {}).items():
                if len(main_characters) < 3:
                    main_characters.append(char_name)
                    
                    # Create character arc based on their secret and role
                    arc_stages = self._create_character_arc(char_data)
                    character_arcs[char_name] = arc_stages
        
        return {
            "main_characters": main_characters,
            "character_arcs": character_arcs
        }
    
    def _create_character_arc(self, character_data: Dict[str, Any]) -> List[str]:
        """Create a character development arc"""
        
        role = character_data.get("role", "unknown")
        personality = character_data.get("personality", "neutral")
        secret = character_data.get("secret", "none")
        
        # Basic arc structure
        arc_templates = {
            "mentor_figure": [
                "Initial meeting - cryptic but helpful",
                "Provides guidance and wisdom",
                "Reveals deeper knowledge",
                "Makes personal sacrifice or revelation",
                "Legacy/influence continues"
            ],
            "ally_character": [
                "Suspicious or neutral first meeting",
                "Builds trust through shared challenges",
                "Reveals personal motivation",
                "Faces moment of loyalty test",
                "Becomes trusted companion"
            ],
            "complex_antagonist": [
                "Appears as obstacle or enemy",
                "Reveals understandable motivations",
                "Creates moral ambiguity",
                "Forces difficult choice",
                "Resolution - redemption or tragic end"
            ]
        }
        
        # Select appropriate template based on role
        if "guardian" in role or "elder" in role:
            template_key = "mentor_figure"
        elif "mysterious" in role or "stranger" in role:
            template_key = "complex_antagonist"
        else:
            template_key = "ally_character"
        
        arc_template = arc_templates[template_key]
        
        # Customize based on secret
        customized_arc = []
        for stage in arc_template:
            customized_stage = stage
            if secret != "none":
                customized_stage += f" (Secret: {secret})"
            customized_arc.append(customized_stage)
        
        return customized_arc
    
    def _integrate_world_building(self, foundation: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate world-building elements into the quest"""
        
        # Select relevant lore elements
        relevant_mysteries = random.sample(
            list(self.world_lore["mysteries"].keys()), 
            min(1, len(self.world_lore["mysteries"]))
        )
        
        lore_elements = []
        for mystery_key in relevant_mysteries:
            mystery = self.world_lore["mysteries"][mystery_key]
            lore_elements.extend([
                f"Mystery: {mystery['description']}",
                f"Truth: {mystery['truth']}",
                f"Implications: {mystery['implications']}"
            ])
        
        # Add faction lore
        faction_keys = random.sample(
            list(self.world_lore["factions"].keys()),
            min(1, len(self.world_lore["factions"]))
        )
        
        for faction_key in faction_keys:
            faction = self.world_lore["factions"][faction_key]
            lore_elements.append(f"Faction Conflict: {random.choice(faction['internal_conflicts'])}")
        
        # Enhanced location details
        location_details = {
            "environmental_storytelling": [
                "Ancient carvings hint at forgotten history",
                "Recent disturbances suggest ongoing activity",
                "Hidden passages reveal secret purposes"
            ],
            "atmospheric_elements": [
                "Shifting weather patterns reflect magical influences",
                "Unusual wildlife behavior indicates supernatural presence",
                "Local legends gain new relevance"
            ]
        }
        
        return {
            "lore_elements": lore_elements,
            "location_details": location_details
        }
    
    def _design_consequence_system(self, theme: NarrativeTheme, complexity: float) -> Dict[str, Any]:
        """Design meaningful consequences that ripple through the story"""
        
        immediate_consequences = {
            "reputation_changes": {},
            "relationship_shifts": {},
            "world_state_changes": [],
            "character_development": []
        }
        
        long_term_consequences = {
            "delayed_events": [],
            "cascade_effects": [],
            "story_flag_changes": [],
            "faction_power_shifts": []
        }
        
        # Theme-specific consequences
        if theme == NarrativeTheme.HEROIC_JOURNEY:
            immediate_consequences["reputation_changes"]["heroic"] = random.randint(10, 25)
            long_term_consequences["delayed_events"].append({
                "trigger_turns": random.randint(5, 10),
                "event": "Recognition leads to greater responsibilities",
                "description": "Your heroic deeds attract attention from powerful figures"
            })
        
        elif theme == NarrativeTheme.MYSTERY_INVESTIGATION:
            immediate_consequences["world_state_changes"].append("Truth partially revealed")
            long_term_consequences["cascade_effects"].append({
                "effect": "Other mysteries become more apparent",
                "probability": 0.7
            })
        
        elif theme == NarrativeTheme.POLITICAL_INTRIGUE:
            immediate_consequences["faction_relations"] = {}
            # Add random faction relation changes
            factions = list(self.world_lore["factions"].keys())
            affected_faction = random.choice(factions)
            immediate_consequences["faction_relations"][affected_faction] = random.randint(-15, 20)
            
            long_term_consequences["story_flag_changes"].append("political_player_recognized")
        
        # Complexity-based additional consequences
        if complexity > 0.7:
            long_term_consequences["delayed_events"].append({
                "trigger_turns": random.randint(8, 15),
                "event": "Unintended consequences manifest",
                "description": "Your actions have ramifications you didn't foresee"
            })
        
        return {
            "immediate": immediate_consequences,
            "long_term": long_term_consequences
        }
    
    def generate_dynamic_dialogue(
        self,
        character_name: str,
        context: Dict[str, Any],
        player_relationship: str = "neutral"
    ) -> Dict[str, Any]:
        """Generate dynamic, context-aware dialogue"""
        
        # Find character in world lore
        character_data = None
        for location_data in self.world_lore["locations"].values():
            if character_name in location_data.get("inhabitants", {}):
                character_data = location_data["inhabitants"][character_name]
                break
        
        if not character_data:
            return {"error": "Character not found"}
        
        personality = character_data.get("personality", "neutral")
        role = character_data.get("role", "unknown")
        secret = character_data.get("secret", "none")
        
        # Generate dialogue options based on context
        dialogue_options = []
        
        # Base options always available
        dialogue_options.extend([
            {
                "text": "Tell me about this place",
                "response_style": "informative",
                "unlocks": ["location_lore"],
                "requirements": {}
            },
            {
                "text": "What brings you here?",
                "response_style": "personal",
                "unlocks": ["character_background"],
                "requirements": {}
            }
        ])
        
        # Relationship-dependent options
        if player_relationship in ["friend", "ally"]:
            dialogue_options.append({
                "text": "I could use your advice",
                "response_style": "helpful",
                "unlocks": ["strategic_advice", "quest_hints"],
                "requirements": {"relationship": "positive"}
            })
        
        elif player_relationship == "suspicious":
            dialogue_options.append({
                "text": "I don't trust you",
                "response_style": "confrontational",
                "unlocks": ["character_defense", "potential_confession"],
                "requirements": {"courage": "high"}
            })
        
        # Secret-dependent options (only if player has discovered clues)
        if secret != "none" and context.get("knows_secret_clues", False):
            dialogue_options.append({
                "text": f"I know about {secret.split(' ')[0]}...",
                "response_style": "revelation",
                "unlocks": ["secret_revealed", "character_arc_advancement"],
                "requirements": {"evidence_gathered": True}
            })
        
        # Role-dependent options
        if "information_broker" in role:
            dialogue_options.append({
                "text": "What news from the road?",
                "response_style": "informative",
                "unlocks": ["world_news", "quest_opportunities"],
                "requirements": {"gold": 10}
            })
        
        return {
            "character_name": character_name,
            "current_mood": self._determine_character_mood(character_data, context),
            "dialogue_options": dialogue_options,
            "personality_influence": personality,
            "hidden_agenda": secret if context.get("player_perception", 0) > 15 else "unknown"
        }
    
    def _determine_character_mood(self, character_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Determine character's current mood based on context"""
        
        base_personality = character_data.get("personality", "neutral")
        
        # Mood modifiers based on context
        if context.get("recent_violence", False):
            if "peaceful" in base_personality:
                return "disturbed"
            elif "aggressive" in base_personality:
                return "excited"
        
        if context.get("mystery_deepening", False):
            if "curious" in base_personality:
                return "intrigued"
            elif "fearful" in base_personality:
                return "anxious"
        
        # Default mood based on personality
        mood_map = {
            "wise_but_cryptic": "thoughtful",
            "cheerful_but_calculating": "friendly_surface",
            "ominous_but_helpful": "mysteriously_benevolent"
        }
        
        return mood_map.get(base_personality, "neutral")
    
    def evolve_narrative_state(self, player_actions: List[str], outcomes: List[Dict[str, Any]]):
        """Evolve the narrative state based on player actions and outcomes"""
        
        # Track recurring themes in player choices
        action_themes = {}
        for action in player_actions:
            if "investigate" in action.lower():
                action_themes["investigative"] = action_themes.get("investigative", 0) + 1
            elif "help" in action.lower():
                action_themes["helpful"] = action_themes.get("helpful", 0) + 1
            elif "fight" in action.lower():
                action_themes["aggressive"] = action_themes.get("aggressive", 0) + 1
        
        # Adapt future narratives based on player tendencies
        dominant_theme = max(action_themes.items(), key=lambda x: x[1])[0] if action_themes else "balanced"
        
        # Update world state based on outcomes
        for outcome in outcomes:
            if "faction_relations" in outcome:
                for faction, change in outcome["faction_relations"].items():
                    if faction in self.world_lore["factions"]:
                        # Update faction power and influence
                        faction_data = self.world_lore["factions"][faction]
                        # In a real implementation, you'd persist these changes
        
        return {
            "player_archetype": dominant_theme,
            "narrative_adaptations": self._suggest_narrative_adaptations(dominant_theme),
            "world_state_changes": self._calculate_world_changes(outcomes)
        }
    
    def _suggest_narrative_adaptations(self, player_archetype: str) -> List[str]:
        """Suggest how future narratives should adapt to player behavior"""
        
        adaptations = {
            "investigative": [
                "Include more mystery elements",
                "Provide deeper lore and background information",
                "Add investigation-based skill checks"
            ],
            "helpful": [
                "Include more opportunities to help NPCs",
                "Add moral choice complexity",
                "Emphasize positive consequences of aid"
            ],
            "aggressive": [
                "Include more combat opportunities",
                "Add tactical combat scenarios",
                "Emphasize direct conflict resolution"
            ],
            "balanced": [
                "Maintain variety in quest types",
                "Provide multiple solution paths",
                "Keep narrative complexity moderate"
            ]
        }
        
        return adaptations.get(player_archetype, adaptations["balanced"])
    
    def _calculate_world_changes(self, outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate how the world state should change based on outcomes"""
        
        world_changes = {
            "power_shifts": {},
            "new_locations_available": [],
            "changed_relationships": {},
            "emerging_threats": [],
            "resolved_mysteries": []
        }
        
        # Analyze outcomes for world-changing events
        for outcome in outcomes:
            if "world_state_changes" in outcome:
                for change in outcome["world_state_changes"]:
                    if "truth_revealed" in change:
                        world_changes["resolved_mysteries"].append(change)
                    elif "power_shift" in change:
                        world_changes["power_shifts"]["general"] = change
        
        return world_changes 