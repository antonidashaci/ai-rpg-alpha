"""
AI-RPG-Alpha: The World Story - "The Shattered Crown Saga"

The epic overarching narrative that weaves together all game systems into
a cohesive, branching storyline with multiple endings and deep consequences.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime


class StoryArc(Enum):
    """Major story arcs"""
    AWAKENING = "awakening"
    RISING_SHADOWS = "rising_shadows"
    CROWN_AND_COVENANT = "crown_and_covenant"
    THE_GREAT_CONVERGENCE = "the_great_convergence"
    EPILOGUE = "epilogue"


class WorldThreat(Enum):
    """Types of threats to the world"""
    POLITICAL_COLLAPSE = "political_collapse"
    ANCIENT_EVIL = "ancient_evil"
    MAGICAL_CATASTROPHE = "magical_catastrophe"
    FOREIGN_INVASION = "foreign_invasion"
    SOCIAL_REVOLUTION = "social_revolution"


@dataclass
class StoryChapter:
    """Individual story chapter"""
    id: str
    title: str
    arc: StoryArc
    description: str
    
    # Prerequisites
    required_progress: Dict[str, Any] = field(default_factory=dict)
    required_choices: List[str] = field(default_factory=list)
    
    # Content
    main_events: List[str] = field(default_factory=list)
    character_moments: Dict[str, List[str]] = field(default_factory=dict)
    political_developments: List[str] = field(default_factory=list)
    
    # Branching
    decision_points: List[str] = field(default_factory=list)
    possible_outcomes: List[str] = field(default_factory=list)
    
    # Integration
    companion_reactions: Dict[str, str] = field(default_factory=dict)
    faction_impacts: Dict[str, int] = field(default_factory=dict)
    world_state_changes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorldState:
    """Current state of the world narrative"""
    current_arc: StoryArc = StoryArc.AWAKENING
    completed_chapters: List[str] = field(default_factory=list)
    active_threats: List[WorldThreat] = field(default_factory=list)
    
    # Player influence
    player_reputation: Dict[str, int] = field(default_factory=dict)
    major_choices: Dict[str, str] = field(default_factory=dict)
    relationships_formed: List[str] = field(default_factory=list)
    
    # World consequences
    faction_control: Dict[str, float] = field(default_factory=dict)
    regions_affected: Dict[str, str] = field(default_factory=dict)
    magical_balance: float = 1.0
    
    # Narrative threads
    active_plotlines: List[str] = field(default_factory=list)
    resolved_plotlines: List[str] = field(default_factory=list)
    character_arcs: Dict[str, str] = field(default_factory=dict)


class WorldStoryEngine:
    """Master storytelling engine that weaves all systems together"""
    
    def __init__(self):
        self.world_state = WorldState()
        self.story_chapters = self._initialize_story_chapters()
        self.story_branches = self._initialize_story_branches()
        self.ending_paths = self._initialize_ending_paths()
        
        # Integration with other systems
        self.companion_system = None  # Injected
        self.faction_system = None    # Injected
        self.world_simulation = None  # Injected
        self.adaptive_ai = None       # Injected
    
    def _initialize_story_chapters(self) -> Dict[str, StoryChapter]:
        """Initialize the main story chapters"""
        
        chapters = {}
        
        # ============= ARC 1: AWAKENING =============
        chapters["prologue"] = StoryChapter(
            id="prologue",
            title="The Dreamer Awakens",
            arc=StoryArc.AWAKENING,
            description="A mysterious awakening in the Whispering Woods begins your journey",
            main_events=[
                "awakening_in_forest",
                "first_magical_encounter", 
                "meeting_the_guide",
                "discovering_the_gift"
            ],
            decision_points=["accept_destiny", "seek_answers", "reject_calling"],
            companion_reactions={
                "lyralei_ranger": "intrigued_by_forest_connection",
                "thane_warrior": "concerned_about_responsibility"
            },
            world_state_changes={"magical_awakening": True, "player_marked": True}
        )
        
        chapters["first_steps"] = StoryChapter(
            id="first_steps",
            title="First Steps into a Larger World",
            arc=StoryArc.AWAKENING,
            description="Learn about the greater conflicts shaping the realm",
            required_progress={"prologue": "completed"},
            main_events=[
                "arrival_at_trading_post",
                "learning_about_factions",
                "first_political_intrigue",
                "choosing_initial_allies"
            ],
            decision_points=["royal_loyalty", "merchant_pragmatism", "rebel_sympathy"],
            faction_impacts={
                "royal_crown": 0,      # Modified by choice
                "merchant_guilds": 0,   # Modified by choice  
                "peoples_liberation": 0 # Modified by choice
            }
        )
        
        chapters["trials_of_worth"] = StoryChapter(
            id="trials_of_worth",
            title="Trials of Worth",
            arc=StoryArc.AWAKENING,
            description="Prove yourself through challenges that test character and ability",
            required_progress={"first_steps": "completed"},
            main_events=[
                "combat_trial",
                "wisdom_trial", 
                "compassion_trial",
                "leadership_trial"
            ],
            decision_points=["trial_approach", "trial_priorities", "trial_sacrifice"],
            character_moments={
                "player": ["moment_of_doubt", "discovery_of_strength", "glimpse_of_destiny"],
                "companions": ["loyalty_tested", "bonds_deepened", "true_nature_revealed"]
            }
        )
        
        # ============= ARC 2: RISING SHADOWS =============
        chapters["shadows_gather"] = StoryChapter(
            id="shadows_gather",
            title="Shadows Gather",
            arc=StoryArc.RISING_SHADOWS,
            description="Dark forces make their presence known across the realm",
            required_progress={"trials_of_worth": "completed"},
            main_events=[
                "shadow_covenant_revelation",
                "corrupted_magic_discovery",
                "first_major_threat",
                "alliance_necessity"
            ],
            political_developments=[
                "faction_tensions_escalate",
                "shadow_infiltration_discovered",
                "emergency_councils_called"
            ],
            decision_points=["alliance_strategy", "threat_response", "information_sharing"]
        )
        
        chapters["the_crown_conspiracy"] = StoryChapter(
            id="the_crown_conspiracy", 
            title="The Crown Conspiracy",
            arc=StoryArc.RISING_SHADOWS,
            description="Uncover a plot that threatens the very foundations of the realm",
            required_progress={"shadows_gather": "completed"},
            main_events=[
                "conspiracy_investigation",
                "infiltration_mission",
                "shocking_revelation",
                "betrayal_or_loyalty"
            ],
            decision_points=["expose_truth", "protect_innocents", "choose_sides"],
            possible_outcomes=[
                "conspiracy_exposed",
                "conspiracy_covered_up",
                "conspiracy_joined",
                "conspiracy_transformed"
            ]
        )
        
        chapters["magic_and_madness"] = StoryChapter(
            id="magic_and_madness",
            title="Magic and Madness", 
            arc=StoryArc.RISING_SHADOWS,
            description="The magical balance of the world begins to unravel",
            required_progress={"the_crown_conspiracy": "completed"},
            main_events=[
                "magical_catastrophe_begins",
                "reality_distortions",
                "ancient_seals_weakening", 
                "desperate_magical_research"
            ],
            character_moments={
                "zara_mage": ["magical_breakthrough", "dangerous_experimentation", "ethical_dilemma"],
                "order_of_dawn": ["faith_tested", "divine_intervention", "holy_mission"]
            }
        )
        
        # ============= ARC 3: CROWN AND COVENANT =============
        chapters["the_great_choice"] = StoryChapter(
            id="the_great_choice",
            title="The Great Choice",
            arc=StoryArc.CROWN_AND_COVENANT,
            description="A pivotal decision that will shape the future of the realm",
            required_progress={"magic_and_madness": "completed"},
            main_events=[
                "all_factions_converge",
                "ultimate_revelation",
                "impossible_decision",
                "point_of_no_return"
            ],
            decision_points=[
                "support_traditional_order",
                "embrace_revolutionary_change", 
                "forge_new_path",
                "sacrifice_for_greater_good"
            ],
            companion_reactions={
                "lyralei_ranger": "supports_freedom_choice",
                "thane_warrior": "supports_honor_choice",
                "zara_mage": "supports_knowledge_choice", 
                "kael_rogue": "supports_people_choice"
            }
        )
        
        chapters["war_of_shadows"] = StoryChapter(
            id="war_of_shadows",
            title="War of Shadows",
            arc=StoryArc.CROWN_AND_COVENANT,
            description="Open conflict erupts as all sides fight for their vision of the future",
            required_progress={"the_great_choice": "completed"},
            main_events=[
                "war_declaration",
                "major_battles",
                "shifting_alliances",
                "personal_sacrifices"
            ],
            political_developments=[
                "faction_warfare",
                "territory_control_changes",
                "civilian_impact",
                "foreign_intervention"
            ]
        )
        
        # ============= ARC 4: THE GREAT CONVERGENCE =============
        chapters["convergence"] = StoryChapter(
            id="convergence",
            title="The Great Convergence",
            arc=StoryArc.THE_GREAT_CONVERGENCE,
            description="All storylines converge in the final confrontation",
            required_progress={"war_of_shadows": "completed"},
            main_events=[
                "final_revelation",
                "ultimate_confrontation",
                "world_transformation",
                "new_beginning"
            ],
            decision_points=[
                "final_sacrifice",
                "ultimate_power_choice",
                "legacy_decision"
            ]
        )
        
        return chapters
    
    def _initialize_story_branches(self) -> Dict[str, Dict[str, Any]]:
        """Initialize major story branching paths"""
        
        return {
            "loyalist_path": {
                "description": "Support the established order and royal authority",
                "key_chapters": ["first_steps", "the_crown_conspiracy", "the_great_choice"],
                "faction_alignment": {"royal_crown": 50, "order_of_dawn": 30},
                "character_development": "duty_and_honor",
                "world_outcome": "stable_monarchy"
            },
            "revolutionary_path": {
                "description": "Fight for the people and revolutionary change",
                "key_chapters": ["first_steps", "shadows_gather", "war_of_shadows"],
                "faction_alignment": {"peoples_liberation": 50, "merchant_guilds": 20},
                "character_development": "freedom_and_justice",
                "world_outcome": "new_republic"
            },
            "shadow_path": {
                "description": "Embrace the darkness for power to save the world",
                "key_chapters": ["shadows_gather", "magic_and_madness", "convergence"],
                "faction_alignment": {"shadow_covenant": 40},
                "character_development": "power_and_sacrifice",
                "world_outcome": "dark_salvation"
            },
            "unity_path": {
                "description": "Unite all factions against a greater threat",
                "key_chapters": ["trials_of_worth", "the_great_choice", "convergence"],
                "faction_alignment": {"balanced": True},
                "character_development": "wisdom_and_leadership",
                "world_outcome": "united_realm"
            },
            "transcendence_path": {
                "description": "Transcend mortal politics through magical ascension",
                "key_chapters": ["magic_and_madness", "convergence"],
                "faction_alignment": {"crystal_sanctum": 60},
                "character_development": "magical_enlightenment",
                "world_outcome": "magical_transformation"
            }
        }
    
    def _initialize_ending_paths(self) -> Dict[str, Dict[str, Any]]:
        """Initialize possible world endings"""
        
        return {
            "golden_age": {
                "title": "The Golden Age",
                "description": "Peace and prosperity return to the realm through wisdom and unity",
                "requirements": {
                    "faction_unity": 0.8,
                    "companion_loyalty": 0.9,
                    "major_choices": ["unity_path", "peaceful_resolution"]
                },
                "world_state": {
                    "peace_level": 0.95,
                    "prosperity": 0.9,
                    "magical_balance": 1.2,
                    "technology_advancement": 1.1
                },
                "companion_fates": {
                    "lyralei_ranger": "becomes_nature_guardian",
                    "thane_warrior": "redeems_past_honored_leader",
                    "zara_mage": "establishes_magical_academy",
                    "kael_rogue": "becomes_peoples_champion"
                }
            },
            "iron_throne": {
                "title": "The Iron Throne",
                "description": "Order is restored through strength and unwavering authority",
                "requirements": {
                    "royal_loyalty": 0.8,
                    "military_strength": 0.9,
                    "major_choices": ["loyalist_path", "authoritarian_rule"]
                },
                "world_state": {
                    "order_level": 0.95,
                    "stability": 0.9,
                    "freedom": 0.4,
                    "technological_advancement": 0.8
                },
                "companion_fates": {
                    "thane_warrior": "becomes_royal_champion",
                    "lyralei_ranger": "reluctant_royal_scout",
                    "others": "conflicted_loyalty"
                }
            },
            "peoples_dawn": {
                "title": "The People's Dawn",
                "description": "A new age of freedom and equality rises from revolution",
                "requirements": {
                    "revolutionary_support": 0.8,
                    "popular_uprising": True,
                    "major_choices": ["revolutionary_path", "power_to_people"]
                },
                "world_state": {
                    "freedom_level": 0.95,
                    "equality": 0.9,
                    "stability": 0.6,
                    "innovation": 1.2
                },
                "companion_fates": {
                    "kael_rogue": "becomes_revolutionary_leader",
                    "lyralei_ranger": "free_protector_of_land",
                    "thane_warrior": "struggles_with_change"
                }
            },
            "shadow_dominion": {
                "title": "The Shadow Dominion",
                "description": "Darkness rules, but perhaps it was necessary to save the world",
                "requirements": {
                    "shadow_alliance": 0.7,
                    "dark_magic_mastery": 0.8,
                    "major_choices": ["shadow_path", "necessary_evil"]
                },
                "world_state": {
                    "order_level": 0.9,
                    "freedom": 0.2,
                    "magical_power": 1.5,
                    "hidden_protection": True
                },
                "companion_fates": {
                    "corrupted_or_redeemed": "depends_on_player_choices"
                }
            },
            "broken_world": {
                "title": "The Broken World",
                "description": "Chaos reigns as all attempts at salvation have failed",
                "requirements": {
                    "faction_warfare": True,
                    "companion_betrayals": 2,
                    "major_choices": ["destructive_path", "selfish_choices"]
                },
                "world_state": {
                    "chaos_level": 0.9,
                    "destruction": 0.8,
                    "hope": 0.1,
                    "survival_struggle": True
                },
                "companion_fates": {
                    "scattered_or_dead": "tragic_endings"
                }
            },
            "transcendent_realm": {
                "title": "The Transcendent Realm",
                "description": "Magic transforms the world into something beyond mortal understanding",
                "requirements": {
                    "magical_mastery": 0.95,
                    "reality_manipulation": 0.8,
                    "major_choices": ["transcendence_path", "magical_transformation"]
                },
                "world_state": {
                    "magical_saturation": 2.0,
                    "reality_stability": 0.5,
                    "transcendent_beings": True,
                    "mortal_politics": False
                },
                "companion_fates": {
                    "transcended_or_left_behind": "magical_transformation"
                }
            }
        }
    
    def get_current_chapter(self) -> Optional[StoryChapter]:
        """Get the current active chapter"""
        
        # Determine next chapter based on progress and choices
        for chapter_id, chapter in self.story_chapters.items():
            if chapter_id not in self.world_state.completed_chapters:
                # Check if prerequisites are met
                if self._check_chapter_prerequisites(chapter):
                    return chapter
        
        return None
    
    def _check_chapter_prerequisites(self, chapter: StoryChapter) -> bool:
        """Check if chapter prerequisites are satisfied"""
        
        # Check required progress
        for requirement, status in chapter.required_progress.items():
            if requirement not in self.world_state.completed_chapters:
                return False
        
        # Check required choices
        for choice in chapter.required_choices:
            if choice not in self.world_state.major_choices.values():
                return False
        
        return True
    
    def make_story_choice(
        self,
        choice_id: str,
        choice_data: Dict[str, Any],
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a major story choice and its consequences"""
        
        current_chapter = self.get_current_chapter()
        if not current_chapter:
            return {"error": "No active chapter"}
        
        # Record the choice
        self.world_state.major_choices[choice_id] = choice_data.get("choice", "")
        
        # Calculate consequences
        consequences = self._calculate_choice_consequences(
            choice_id, choice_data, current_chapter, player_context
        )
        
        # Apply faction impacts
        if current_chapter.faction_impacts:
            for faction, impact in current_chapter.faction_impacts.items():
                # Modify impact based on choice
                modified_impact = self._modify_faction_impact(faction, impact, choice_data)
                self.world_state.faction_control[faction] = (
                    self.world_state.faction_control.get(faction, 0.5) + modified_impact * 0.01
                )
        
        # Update companion relationships if integrated
        if self.companion_system:
            self._update_companion_reactions(current_chapter, choice_data)
        
        # Update world state
        if current_chapter.world_state_changes:
            for key, value in current_chapter.world_state_changes.items():
                setattr(self.world_state, key, value)
        
        # Generate narrative outcome
        narrative = self._generate_choice_narrative(choice_id, choice_data, consequences)
        
        return {
            "choice_processed": True,
            "consequences": consequences,
            "narrative": narrative,
            "world_changes": current_chapter.world_state_changes,
            "faction_impacts": self._get_faction_impact_summary(),
            "chapter_progress": self._get_chapter_progress()
        }
    
    def _calculate_choice_consequences(
        self,
        choice_id: str,
        choice_data: Dict[str, Any],
        chapter: StoryChapter,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate the full consequences of a story choice"""
        
        consequences = {
            "immediate": [],
            "long_term": [],
            "faction_relations": {},
            "companion_reactions": {},
            "world_state_changes": {},
            "narrative_threads": []
        }
        
        choice_type = choice_data.get("choice", "")
        
        # Choice-specific consequences
        if choice_type == "royal_loyalty":
            consequences["immediate"].append("Gained favor with Royal Crown")
            consequences["faction_relations"]["royal_crown"] = 20
            consequences["faction_relations"]["peoples_liberation"] = -15
            consequences["long_term"].append("Path toward supporting established order")
            
        elif choice_type == "rebel_sympathy":
            consequences["immediate"].append("Gained trust of revolutionary movement")
            consequences["faction_relations"]["peoples_liberation"] = 20
            consequences["faction_relations"]["royal_crown"] = -10
            consequences["long_term"].append("Path toward revolutionary change")
            
        elif choice_type == "unity_path":
            consequences["immediate"].append("Attempt to bridge factional divides")
            consequences["faction_relations"]["all"] = 5
            consequences["long_term"].append("Challenging path of unification")
            consequences["narrative_threads"].append("unity_storyline_activated")
        
        # Integrate companion reactions if available
        if self.companion_system and chapter.companion_reactions:
            for companion_id, reaction in chapter.companion_reactions.items():
                consequences["companion_reactions"][companion_id] = reaction
        
        return consequences
    
    def _modify_faction_impact(self, faction: str, base_impact: int, choice_data: Dict[str, Any]) -> int:
        """Modify faction impact based on specific choice"""
        
        choice = choice_data.get("choice", "")
        
        faction_choice_modifiers = {
            "royal_crown": {
                "royal_loyalty": 2.0,
                "rebel_sympathy": -1.5,
                "unity_path": 1.2
            },
            "peoples_liberation": {
                "royal_loyalty": -1.5,
                "rebel_sympathy": 2.0,
                "unity_path": 1.2
            },
            "merchant_guilds": {
                "economic_focus": 2.0,
                "unity_path": 1.5
            }
        }
        
        modifier = faction_choice_modifiers.get(faction, {}).get(choice, 1.0)
        return int(base_impact * modifier)
    
    def _update_companion_reactions(self, chapter: StoryChapter, choice_data: Dict[str, Any]):
        """Update companion relationships based on story choices"""
        
        if not self.companion_system:
            return
        
        choice = choice_data.get("choice", "")
        
        # Companion choice preferences
        companion_preferences = {
            "lyralei_ranger": {
                "likes": ["freedom_choice", "nature_protection", "rebel_sympathy"],
                "dislikes": ["authoritarian_rule", "environmental_destruction"]
            },
            "thane_warrior": {
                "likes": ["honor_choice", "protect_innocents", "royal_loyalty"],
                "dislikes": ["dishonorable_acts", "abandoning_duty"]
            },
            "zara_mage": {
                "likes": ["knowledge_seeking", "magical_research", "innovation"],
                "dislikes": ["anti_magic_stance", "willful_ignorance"]
            },
            "kael_rogue": {
                "likes": ["help_the_poor", "rebel_sympathy", "clever_solutions"],
                "dislikes": ["royal_loyalty", "elitist_choices"]
            }
        }
        
        for companion_id, prefs in companion_preferences.items():
            if choice in prefs["likes"]:
                # Positive reaction
                self.companion_system.record_interaction(
                    companion_id, "player", "story_choice_approval",
                    f"Approves of your choice to {choice.replace('_', ' ')}"
                )
            elif choice in prefs["dislikes"]:
                # Negative reaction
                self.companion_system.record_interaction(
                    companion_id, "player", "story_choice_disapproval", 
                    f"Disapproves of your choice to {choice.replace('_', ' ')}"
                )
    
    def _generate_choice_narrative(
        self,
        choice_id: str,
        choice_data: Dict[str, Any],
        consequences: Dict[str, Any]
    ) -> str:
        """Generate narrative text for choice outcome"""
        
        choice = choice_data.get("choice", "")
        
        narrative_templates = {
            "royal_loyalty": [
                "Your decision to support the Crown sends ripples through the political landscape.",
                "Traditional nobles nod approvingly, while revolutionaries exchange worried glances.",
                "The weight of royal authority settles on your shoulders like a gilded cloak."
            ],
            "rebel_sympathy": [
                "Your words of support for the common folk spark hope in downtrodden eyes.",
                "Revolutionary leaders mark you as a potential ally, while nobles whisper of treason.",
                "The fire of change begins to burn brighter in the hearts of the oppressed."
            ],
            "unity_path": [
                "Your call for unity resonates across factional lines, though many remain skeptical.",
                "Both sides watch you carefully, wondering if such idealism can survive reality.",
                "The path you've chosen is difficult, but perhaps necessary for true peace."
            ]
        }
        
        base_narrative = random.choice(narrative_templates.get(choice, ["Your choice reshapes the future."]))
        
        # Add consequence details
        if consequences["immediate"]:
            base_narrative += f" {random.choice(consequences['immediate'])}"
        
        return base_narrative
    
    def advance_story_arc(self) -> Dict[str, Any]:
        """Advance to the next story arc if conditions are met"""
        
        current_arc = self.world_state.current_arc
        
        # Check if current arc is complete
        arc_chapters = [ch for ch in self.story_chapters.values() if ch.arc == current_arc]
        completed_in_arc = [ch for ch in arc_chapters if ch.id in self.world_state.completed_chapters]
        
        if len(completed_in_arc) >= len(arc_chapters) * 0.8:  # 80% of arc chapters completed
            # Advance to next arc
            arc_order = [StoryArc.AWAKENING, StoryArc.RISING_SHADOWS, 
                        StoryArc.CROWN_AND_COVENANT, StoryArc.THE_GREAT_CONVERGENCE]
            
            current_index = arc_order.index(current_arc)
            if current_index < len(arc_order) - 1:
                new_arc = arc_order[current_index + 1]
                self.world_state.current_arc = new_arc
                
                # Trigger arc transition event
                return {
                    "arc_advanced": True,
                    "previous_arc": current_arc.value,
                    "new_arc": new_arc.value,
                    "transition_narrative": self._get_arc_transition_narrative(current_arc, new_arc)
                }
        
        return {"arc_advanced": False}
    
    def _get_arc_transition_narrative(self, from_arc: StoryArc, to_arc: StoryArc) -> str:
        """Get narrative for arc transitions"""
        
        transitions = {
            (StoryArc.AWAKENING, StoryArc.RISING_SHADOWS): 
                "The peaceful days of discovery are ending. Dark clouds gather on the horizon, and you sense that greater challenges await.",
            
            (StoryArc.RISING_SHADOWS, StoryArc.CROWN_AND_COVENANT):
                "The shadows have revealed their true nature. Now the fate of the Crown itself hangs in the balance, and your choices will determine the realm's future.",
            
            (StoryArc.CROWN_AND_COVENANT, StoryArc.THE_GREAT_CONVERGENCE):
                "All paths converge toward a single point of destiny. The final act begins, and the world itself awaits transformation."
        }
        
        return transitions.get((from_arc, to_arc), "A new chapter in your story begins.")
    
    def get_story_status(self) -> Dict[str, Any]:
        """Get comprehensive story status"""
        
        current_chapter = self.get_current_chapter()
        
        # Determine story path
        story_path = self._determine_current_path()
        
        # Calculate completion percentage
        total_chapters = len(self.story_chapters)
        completed_chapters = len(self.world_state.completed_chapters)
        completion_percentage = (completed_chapters / total_chapters) * 100
        
        return {
            "current_arc": self.world_state.current_arc.value,
            "current_chapter": current_chapter.title if current_chapter else "None",
            "story_path": story_path,
            "completion_percentage": completion_percentage,
            "active_threats": [threat.value for threat in self.world_state.active_threats],
            "major_choices_made": list(self.world_state.major_choices.values()),
            "faction_standings": self.world_state.faction_control,
            "active_plotlines": self.world_state.active_plotlines,
            "character_relationships": len(self.world_state.relationships_formed),
            "predicted_ending": self._predict_ending_path()
        }
    
    def _determine_current_path(self) -> str:
        """Determine which story path the player is currently on"""
        
        choices = list(self.world_state.major_choices.values())
        
        # Analyze choice patterns
        if "royal_loyalty" in choices and choices.count("royal_loyalty") > 1:
            return "loyalist_path"
        elif "rebel_sympathy" in choices and choices.count("rebel_sympathy") > 1:
            return "revolutionary_path"
        elif "unity_path" in choices:
            return "unity_path"
        elif "shadow_alliance" in choices:
            return "shadow_path"
        elif "magical_focus" in choices:
            return "transcendence_path"
        else:
            return "undetermined"
    
    def _predict_ending_path(self) -> str:
        """Predict which ending the player is heading toward"""
        
        # Analyze multiple factors
        story_path = self._determine_current_path()
        faction_unity = self._calculate_faction_unity()
        companion_loyalty = self._calculate_companion_loyalty()
        
        # Simple prediction logic
        if faction_unity > 0.8 and companion_loyalty > 0.8:
            return "golden_age"
        elif story_path == "loyalist_path":
            return "iron_throne"
        elif story_path == "revolutionary_path":
            return "peoples_dawn"
        elif story_path == "shadow_path":
            return "shadow_dominion"
        elif story_path == "transcendence_path":
            return "transcendent_realm"
        elif faction_unity < 0.3:
            return "broken_world"
        else:
            return "uncertain"
    
    def _calculate_faction_unity(self) -> float:
        """Calculate overall faction unity level"""
        
        if not self.world_state.faction_control:
            return 0.5
        
        # Calculate variance in faction power
        powers = list(self.world_state.faction_control.values())
        mean_power = sum(powers) / len(powers)
        variance = sum((p - mean_power) ** 2 for p in powers) / len(powers)
        
        # Lower variance = higher unity
        unity = max(0.0, 1.0 - variance)
        return unity
    
    def _calculate_companion_loyalty(self) -> float:
        """Calculate average companion loyalty"""
        
        if not self.companion_system:
            return 0.5
        
        # This would integrate with companion system
        # For now, return based on relationships formed
        relationship_count = len(self.world_state.relationships_formed)
        max_relationships = 4  # Assuming 4 main companions
        
        return min(1.0, relationship_count / max_relationships)
    
    def _get_faction_impact_summary(self) -> Dict[str, Any]:
        """Get summary of current faction standings"""
        
        return {
            faction: {
                "control_level": control,
                "player_reputation": self.world_state.player_reputation.get(faction, 0),
                "relationship": self._get_faction_relationship_status(faction, control)
            }
            for faction, control in self.world_state.faction_control.items()
        }
    
    def _get_faction_relationship_status(self, faction: str, control_level: float) -> str:
        """Get relationship status with faction"""
        
        reputation = self.world_state.player_reputation.get(faction, 0)
        
        if reputation > 50:
            return "trusted_ally"
        elif reputation > 20:
            return "friendly"
        elif reputation > -20:
            return "neutral"
        elif reputation > -50:
            return "suspicious"
        else:
            return "enemy"
    
    def _get_chapter_progress(self) -> Dict[str, Any]:
        """Get detailed chapter progress information"""
        
        current_chapter = self.get_current_chapter()
        
        if not current_chapter:
            return {"status": "story_complete"}
        
        return {
            "current_chapter": current_chapter.title,
            "chapter_id": current_chapter.id,
            "arc": current_chapter.arc.value,
            "description": current_chapter.description,
            "decision_points": current_chapter.decision_points,
            "possible_outcomes": current_chapter.possible_outcomes,
            "chapters_completed": len(self.world_state.completed_chapters),
            "total_chapters": len(self.story_chapters)
        }
    
    def integrate_systems(
        self,
        companion_system=None,
        faction_system=None, 
        world_simulation=None,
        adaptive_ai=None
    ):
        """Integrate with other game systems"""
        
        self.companion_system = companion_system
        self.faction_system = faction_system
        self.world_simulation = world_simulation
        self.adaptive_ai = adaptive_ai
        
        # Set up cross-system event triggers
        if world_simulation:
            world_simulation.story_integration = self
        
        if adaptive_ai:
            adaptive_ai.story_context = self 