"""
AI-RPG-Alpha: Game Master - System Integration Hub

The master orchestrator that brings together all advanced systems into
a unified, intelligent, and deeply interactive AI RPG experience.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import random
import json
from datetime import datetime

# Import all our advanced systems
from .engine.companion_system import CompanionSystem
from .engine.faction_politics import PoliticalSystem
from .engine.adaptive_ai import AdaptiveAIEngine
from .engine.enhanced_combat import EnhancedCombatEngine
from .engine.living_world import LivingWorldEngine
from .engine.dialogue_system import DialogueSystem
from .engine.narrative_advanced import AdvancedNarrativeEngine
from .engine.alignment_karma import AlignmentKarmaSystem, KarmaAction
from .world.main_story import WorldStoryEngine


@dataclass
class GameState:
    """Master game state containing all system states"""
    player_id: str
    session_id: str
    
    # Core progression
    player_level: int = 1
    experience: int = 0
    skills: Dict[str, int] = field(default_factory=dict)
    
    # Current context
    current_location: str = "whispering_woods"
    current_chapter: str = "prologue"
    active_quest: Optional[str] = None
    
    # Relationships and reputation
    companion_relationships: Dict[str, str] = field(default_factory=dict)
    faction_standings: Dict[str, int] = field(default_factory=dict)
    
    # Player choices and history
    major_decisions: List[str] = field(default_factory=list)
    moral_alignment: Dict[str, float] = field(default_factory=dict)
    
    # World state
    world_day: int = 1
    season: str = "spring"
    world_events: List[str] = field(default_factory=list)
    
    # Session tracking
    last_save: datetime = field(default_factory=datetime.now)
    play_time: int = 0  # minutes


class GameMaster:
    """The AI Game Master that orchestrates all systems"""
    
    def __init__(self):
        # Initialize all systems
        self.companion_system = CompanionSystem()
        self.political_system = PoliticalSystem()
        self.adaptive_ai = AdaptiveAIEngine()
        self.combat_engine = EnhancedCombatEngine()
        self.world_simulation = LivingWorldEngine()
        self.dialogue_system = DialogueSystem()
        self.narrative_engine = AdvancedNarrativeEngine()
        self.alignment_karma = AlignmentKarmaSystem()
        self.story_engine = WorldStoryEngine()
        
        # Cross-system integration
        self._integrate_systems()
        
        # Active game sessions
        self.active_sessions: Dict[str, GameState] = {}
        
        # AI decision-making
        self.action_history: List[Dict[str, Any]] = []
        self.player_patterns: Dict[str, Any] = {}
    
    def _integrate_systems(self):
        """Set up cross-system integrations"""
        
        # Story engine integration
        self.story_engine.integrate_systems(
            companion_system=self.companion_system,
            faction_system=self.political_system,
            world_simulation=self.world_simulation,
            adaptive_ai=self.adaptive_ai
        )
        
        # AI system integration
        for npc_id in ["lyralei_ranger", "thane_warrior", "zara_mage", "kael_rogue"]:
            self.adaptive_ai.initialize_npc_memory(
                npc_id, 
                npc_id.replace("_", " ").title(),
                ["knows_about_forest", "experienced_traveler", "has_personal_goals"]
            )
    
    def start_new_game(self, player_id: str, character_creation: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new game session"""
        
        session_id = f"{player_id}_{datetime.now().timestamp()}"
        
        # Create game state
        game_state = GameState(
            player_id=player_id,
            session_id=session_id,
            skills=character_creation.get("skills", {}),
            moral_alignment=character_creation.get("alignment", {})
        )
        
        self.active_sessions[session_id] = game_state
        
        # Generate opening scene
        opening_scene = self._generate_opening_scene(game_state)
        
        # Record in AI memory
        self.adaptive_ai.record_interaction(
            "game_master", player_id, "game_start",
            "Player begins their journey in the Whispering Woods",
            {"location": "whispering_woods", "character_creation": character_creation}
        )
        
        return {
            "session_id": session_id,
            "opening_scene": opening_scene,
            "game_state": self._get_public_game_state(game_state),
            "available_actions": self._get_available_actions(game_state)
        }
    
    def _generate_opening_scene(self, game_state: GameState) -> Dict[str, Any]:
        """Generate the opening scene of the game"""
        
        # Get story chapter
        story_status = self.story_engine.get_story_status()
        
        # Generate adaptive opening based on character
        opening_narrative = self.narrative_engine.generate_scene_description(
            location="whispering_woods",
            context={
                "time_of_day": "dawn",
                "weather": "misty",
                "player_background": "mysterious_awakening",
                "mood": "mysterious_discovery"
            }
        )
        
        return {
            "title": "The Dreamer Awakens",
            "narrative": opening_narrative,
            "environment": {
                "location": "whispering_woods",
                "description": "Ancient trees whisper secrets in the morning mist",
                "notable_features": ["ancient_oak", "crystal_stream", "hidden_path"],
                "atmosphere": "mysterious_and_peaceful"
            },
            "story_context": story_status
        }
    
    def process_player_action(
        self,
        session_id: str,
        action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process any player action through the integrated systems"""
        
        if session_id not in self.active_sessions:
            return {"error": "Invalid session"}
        
        game_state = self.active_sessions[session_id]
        action_type = action.get("type", "")
        
        # Route action to appropriate system
        if action_type == "dialogue":
            result = self._process_dialogue_action(game_state, action)
        elif action_type == "combat":
            result = self._process_combat_action(game_state, action)
        elif action_type == "story_choice":
            result = self._process_story_choice(game_state, action)
        elif action_type == "exploration":
            result = self._process_exploration_action(game_state, action)
        elif action_type == "companion_interaction":
            result = self._process_companion_action(game_state, action)
        elif action_type == "political_action":
            result = self._process_political_action(game_state, action)
        else:
            result = self._process_general_action(game_state, action)
        
        # Update world simulation
        world_changes = self.world_simulation.simulate_world_tick(1)
        result["world_changes"] = world_changes
        
        # Learn from player action
        self._learn_from_action(game_state, action, result)
        
        # Update game state
        self._update_game_state(game_state, action, result)
        
        # Check for story progression
        story_updates = self._check_story_progression(game_state)
        if story_updates:
            result["story_updates"] = story_updates
        
        # Get next available actions
        result["available_actions"] = self._get_available_actions(game_state)
        result["game_state"] = self._get_public_game_state(game_state)
        
        return result
    
    def _process_dialogue_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process dialogue through integrated systems"""
        
        npc_id = action.get("npc_id", "")
        dialogue_choice = action.get("choice", "")
        
        # Get AI memory context
        memory_context = self.adaptive_ai.get_npc_memory_context(
            npc_id, game_state.player_id, "dialogue"
        )
        
        # Generate adaptive dialogue
        dialogue_result = self.adaptive_ai.generate_adaptive_dialogue(
            npc_id, game_state.player_id, {
                "choice": dialogue_choice,
                "location": game_state.current_location,
                "story_context": self.story_engine.get_story_status()
            }
        )
        
        # Track karma for moral dialogue choices
        karma_event = None
        if "karma_action" in action:
            karma_event = self.alignment_karma.record_karma_action(
                game_state.player_id,
                action["karma_action"],
                f"Dialogue with {npc_id}: {dialogue_choice}",
                location=game_state.current_location,
                witnesses=[npc_id],
                context={
                    "present_companions": list(game_state.companion_relationships.keys()),
                    "npc_id": npc_id,
                    "dialogue_context": "social_interaction"
                }
            )
        
        # Record interaction
        self.adaptive_ai.record_interaction(
            npc_id, game_state.player_id, "dialogue_choice",
            f"Player chose: {dialogue_choice}",
            {"location": game_state.current_location}
        )
        
        # Check for companion recruitment
        if npc_id in self.companion_system.companions:
            recruitment_result = self.companion_system.attempt_recruitment(
                npc_id, [dialogue_choice], game_state.faction_standings
            )
            if recruitment_result.get("success"):
                dialogue_result["recruitment_success"] = recruitment_result
        
        # Get NPC reaction modifier based on player reputation
        reaction_modifier = self.alignment_karma.get_npc_reaction_modifier(
            game_state.player_id, 
            npc_id.split("_")[0],  # Extract NPC type (guard, commoner, etc.)
            "neutral"  # Default alignment, could be enhanced with NPC-specific alignments
        )
        
        return {
            "type": "dialogue_response",
            "npc_response": dialogue_result,
            "memory_context": memory_context,
            "relationship_changes": self._get_relationship_changes(npc_id, dialogue_choice),
            "karma_event": karma_event,
            "npc_reaction_modifier": reaction_modifier
        }
    
    def _process_combat_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process combat through enhanced combat system"""
        
        combat_action = action.get("action", "")
        target = action.get("target", "")
        approach = action.get("approach", "standard")
        
        # Execute combat action
        combat_result = self.combat_engine.execute_combat_action(
            combat_action, target, None, game_state.skills, approach
        )
        
        # Update companion morale based on combat style
        if self.companion_system:
            for companion_id in game_state.companion_relationships:
                if approach == "aggressive" and companion_id == "thane_warrior":
                    # Thane approves of honorable but firm combat
                    self.adaptive_ai.record_interaction(
                        companion_id, game_state.player_id, "combat_approval",
                        "Approves of your decisive combat approach"
                    )
                elif approach == "defensive" and companion_id == "lyralei_ranger":
                    # Lyralei appreciates tactical thinking
                    self.adaptive_ai.record_interaction(
                        companion_id, game_state.player_id, "combat_approval",
                        "Appreciates your thoughtful combat tactics"
                    )
        
        return {
            "type": "combat_result",
            "combat_outcome": combat_result,
            "experience_gained": combat_result.get("damage_dealt", 0) * 5,
            "companion_reactions": self._get_companion_combat_reactions(approach)
        }
    
    def _process_story_choice(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process major story choices"""
        
        choice_id = action.get("choice_id", "")
        choice_data = action.get("choice_data", {})
        
        # Process through story engine
        story_result = self.story_engine.make_story_choice(
            choice_id, choice_data, {
                "player_id": game_state.player_id,
                "current_location": game_state.current_location,
                "companion_relationships": game_state.companion_relationships,
                "faction_standings": game_state.faction_standings
            }
        )
        
        # Track karma for moral choices
        karma_event = None
        if "karma_action" in action:
            karma_event = self.alignment_karma.record_karma_action(
                game_state.player_id,
                action["karma_action"],
                f"Story choice: {choice_data.get('choice', '')}",
                location=game_state.current_location,
                context={
                    "present_companions": list(game_state.companion_relationships.keys()),
                    "involved_factions": list(story_result.get("faction_impacts", {}).keys()),
                    "story_context": choice_id
                }
            )
        
        # Update faction standings
        if "faction_impacts" in story_result:
            for faction, impact in story_result["faction_impacts"].items():
                current_standing = game_state.faction_standings.get(faction, 0)
                game_state.faction_standings[faction] = current_standing + impact
        
        # Record major decision
        game_state.major_decisions.append(choice_data.get("choice", ""))
        
        # Trigger political consequences
        political_changes = self.political_system.process_political_turn(1)
        
        # Get alignment summary for response
        morality_summary = self.alignment_karma.get_morality_summary(game_state.player_id)
        
        return {
            "type": "story_choice_result",
            "story_outcome": story_result,
            "political_consequences": political_changes,
            "karma_event": karma_event,
            "morality_summary": morality_summary,
            "world_impact": "Your choice reverberates through the realm..."
        }
    
    def _process_exploration_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process exploration and movement"""
        
        destination = action.get("destination", "")
        exploration_type = action.get("exploration_type", "travel")
        
        # Generate location description
        location_description = self.narrative_engine.generate_scene_description(
            destination, {
                "exploration_type": exploration_type,
                "player_background": game_state.moral_alignment,
                "time_of_day": self._get_time_of_day(game_state.world_day),
                "weather": self._get_weather(game_state.season)
            }
        )
        
        # Check for random encounters
        encounter_chance = 0.3 if exploration_type == "careful_exploration" else 0.5
        
        if random.random() < encounter_chance:
            encounter = self._generate_random_encounter(game_state, destination)
            location_description["encounter"] = encounter
        
        # Update location
        game_state.current_location = destination
        
        # Check world simulation for location-specific events
        location_info = self.world_simulation.get_location_specific_info(destination)
        
        return {
            "type": "exploration_result",
            "location_description": location_description,
            "location_info": location_info,
            "travel_narrative": f"You arrive at {destination.replace('_', ' ')}"
        }
    
    def _process_companion_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process companion interactions"""
        
        companion_id = action.get("companion_id", "")
        interaction_type = action.get("interaction_type", "")
        
        # Process through companion system
        interaction_result = self.companion_system.interact_with_companion(
            companion_id, interaction_type, {
                "location": game_state.current_location,
                "story_context": self.story_engine.get_story_status(),
                "recent_events": game_state.world_events[-5:]
            }
        )
        
        # Update relationship tracking
        if companion_id not in game_state.companion_relationships:
            game_state.companion_relationships[companion_id] = "acquaintance"
        
        return {
            "type": "companion_interaction_result",
            "interaction_outcome": interaction_result,
            "relationship_status": self._get_companion_relationship_status(companion_id)
        }
    
    def _process_political_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process political missions and actions"""
        
        mission_id = action.get("mission_id", "")
        approach = action.get("approach", "diplomatic")
        
        # Execute political mission
        mission_result = self.political_system.execute_political_mission(
            mission_id, game_state.skills, game_state.faction_standings, approach
        )
        
        # Update faction standings based on result
        if mission_result.get("success"):
            faction_changes = mission_result.get("rewards", {}).get("reputation", {})
            for faction, rep_change in faction_changes.items():
                current_rep = game_state.faction_standings.get(faction, 0)
                game_state.faction_standings[faction] = current_rep + rep_change
        
        return {
            "type": "political_action_result",
            "mission_outcome": mission_result,
            "political_narrative": self._generate_political_narrative(mission_result)
        }
    
    def _process_general_action(self, game_state: GameState, action: Dict[str, Any]) -> Dict[str, Any]:
        """Process general actions not handled by specific systems"""
        
        action_description = action.get("description", "")
        
        # Generate narrative response
        narrative_response = self.narrative_engine.generate_response(
            action_description, {
                "location": game_state.current_location,
                "player_context": game_state.moral_alignment,
                "story_context": self.story_engine.get_story_status()
            }
        )
        
        return {
            "type": "general_action_result",
            "narrative": narrative_response,
            "outcome": "Your action ripples through the world in ways yet unseen..."
        }
    
    def _learn_from_action(self, game_state: GameState, action: Dict[str, Any], result: Dict[str, Any]):
        """Learn from player action to improve AI responses"""
        
        # Record action pattern
        action_pattern = {
            "player_id": game_state.player_id,
            "action_type": action.get("type", ""),
            "context": {
                "location": game_state.current_location,
                "story_chapter": game_state.current_chapter,
                "companions_present": list(game_state.companion_relationships.keys())
            },
            "choice": action.get("choice", ""),
            "approach": action.get("approach", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        self.action_history.append(action_pattern)
        
        # Update player patterns
        player_id = game_state.player_id
        if player_id not in self.player_patterns:
            self.player_patterns[player_id] = {
                "preferred_approaches": {},
                "moral_tendencies": {},
                "relationship_style": {},
                "decision_speed": []
            }
        
        # Learn approach preferences
        approach = action.get("approach", "standard")
        current_count = self.player_patterns[player_id]["preferred_approaches"].get(approach, 0)
        self.player_patterns[player_id]["preferred_approaches"][approach] = current_count + 1
    
    def _update_game_state(self, game_state: GameState, action: Dict[str, Any], result: Dict[str, Any]):
        """Update game state based on action results"""
        
        # Advance world time
        game_state.world_day += random.choice([0, 0, 0, 1])  # Sometimes a day passes
        
        # Update season if needed
        if game_state.world_day % 91 == 0:  # Roughly every season
            seasons = ["spring", "summer", "autumn", "winter"]
            current_index = seasons.index(game_state.season)
            game_state.season = seasons[(current_index + 1) % 4]
        
        # Add to world events
        if result.get("type") in ["story_choice_result", "political_action_result"]:
            event_summary = f"Player {action.get('type', 'action')} in {game_state.current_location}"
            game_state.world_events.append(event_summary)
            
            # Keep only recent events
            if len(game_state.world_events) > 20:
                game_state.world_events = game_state.world_events[-20:]
        
        # Experience and progression
        exp_gained = result.get("experience_gained", 0)
        if exp_gained:
            game_state.experience += exp_gained
            
            # Check for level up
            exp_needed = game_state.player_level * 100
            if game_state.experience >= exp_needed:
                game_state.player_level += 1
                game_state.experience -= exp_needed
                result["level_up"] = True
    
    def _check_story_progression(self, game_state: GameState) -> Optional[Dict[str, Any]]:
        """Check if story should progress"""
        
        # Check for arc advancement
        arc_advancement = self.story_engine.advance_story_arc()
        
        if arc_advancement.get("arc_advanced"):
            game_state.current_chapter = "new_arc_beginning"
            return {
                "arc_progression": arc_advancement,
                "new_opportunities": self._get_new_story_opportunities(game_state)
            }
        
        return None
    
    def _get_available_actions(self, game_state: GameState) -> List[Dict[str, Any]]:
        """Get list of available actions based on current context and alignment"""
        
        base_actions = []
        
        # Always available actions
        base_actions.extend([
            {"type": "exploration", "description": "Explore your surroundings"},
            {"type": "dialogue", "description": "Talk to someone nearby"},
            {"type": "rest", "description": "Rest and recover"}
        ])
        
        # Story-specific actions
        current_chapter = self.story_engine.get_current_chapter()
        if current_chapter:
            for decision_point in current_chapter.decision_points:
                base_actions.append({
                    "type": "story_choice",
                    "description": f"Make a decision about {decision_point.replace('_', ' ')}",
                    "choice_id": decision_point
                })
        
        # Companion actions
        for companion_id in game_state.companion_relationships:
            base_actions.append({
                "type": "companion_interaction",
                "description": f"Interact with {companion_id.replace('_', ' ').title()}",
                "companion_id": companion_id
            })
        
        # Political actions
        political_summary = self.political_system.get_political_summary()
        for mission in political_summary.get("available_missions", [])[:3]:  # Limit to 3
            # Check if player can access this mission based on alignment
            mission_requirements = mission.get("requirements", {})
            if self.alignment_karma.can_start_quest(game_state.player_id, mission["id"], mission_requirements):
                base_actions.append({
                    "type": "political_action",
                    "description": f"Accept mission: {mission['title']}",
                    "mission_id": mission["id"]
                })
        
        # Combat actions (if in combat)
        combat_status = self.combat_engine.get_combat_status()
        if combat_status.get("status") == "combat_active":
            combat_actions = self.combat_engine.get_available_actions(game_state.skills)
            for combat_action in combat_actions[:5]:  # Limit to 5
                base_actions.append({
                    "type": "combat",
                    "description": f"Combat: {combat_action['name']}",
                    "action": combat_action["id"]
                })
        
        # Filter actions through alignment system to add moral choices
        actions = self.alignment_karma.get_available_choices_for_alignment(
            game_state.player_id, base_actions
        )
        
        return actions
    
    def _get_public_game_state(self, game_state: GameState) -> Dict[str, Any]:
        """Get public-facing game state (hide internal details)"""
        
        # Get morality summary
        morality_summary = self.alignment_karma.get_morality_summary(game_state.player_id)
        
        return {
            "player_level": game_state.player_level,
            "experience": game_state.experience,
            "current_location": game_state.current_location,
            "current_chapter": game_state.current_chapter,
            "companion_count": len(game_state.companion_relationships),
            "faction_standings": game_state.faction_standings,
            "world_day": game_state.world_day,
            "season": game_state.season,
            "major_decisions_made": len(game_state.major_decisions),
            "story_progress": self.story_engine.get_story_status(),
            "morality": {
                "alignment": morality_summary["alignment"],
                "moral_title": morality_summary["moral_title"],
                "karma": morality_summary["total_karma"],
                "corruption_level": morality_summary["corruption_level"],
                "reputation_summary": {
                    "authorities": morality_summary["reputation_levels"]["lawful_authorities"],
                    "common_folk": morality_summary["reputation_levels"]["common_folk"],
                    "criminals": morality_summary["reputation_levels"]["criminal_underworld"]
                }
            }
        }
    
    def _generate_random_encounter(self, game_state: GameState, location: str) -> Dict[str, Any]:
        """Generate random encounters based on location and context"""
        
        location_encounters = {
            "whispering_woods": ["friendly_woodland_creature", "lost_traveler", "ancient_ruins"],
            "trading_post": ["merchant_opportunity", "information_broker", "political_intrigue"],
            "crystal_sanctum": ["magical_phenomenon", "scholarly_debate", "divine_vision"]
        }
        
        possible_encounters = location_encounters.get(location, ["mysterious_stranger"])
        encounter_type = random.choice(possible_encounters)
        
        return {
            "type": encounter_type,
            "description": f"You encounter {encounter_type.replace('_', ' ')} in {location}",
            "options": ["investigate", "ignore", "approach_carefully"]
        }
    
    def _get_time_of_day(self, world_day: int) -> str:
        """Get current time of day"""
        times = ["dawn", "morning", "midday", "afternoon", "evening", "night"]
        return times[world_day % 6]
    
    def _get_weather(self, season: str) -> str:
        """Get weather based on season"""
        weather_by_season = {
            "spring": ["mild", "rainy", "fresh"],
            "summer": ["warm", "sunny", "hot"],
            "autumn": ["cool", "misty", "windy"],
            "winter": ["cold", "snowy", "harsh"]
        }
        return random.choice(weather_by_season.get(season, ["pleasant"]))
    
    def _get_relationship_changes(self, npc_id: str, dialogue_choice: str) -> Dict[str, Any]:
        """Get relationship changes from dialogue"""
        # This would integrate with companion system
        return {"relationship_shift": "positive" if "help" in dialogue_choice.lower() else "neutral"}
    
    def _get_companion_combat_reactions(self, approach: str) -> Dict[str, str]:
        """Get companion reactions to combat approach"""
        reactions = {}
        
        if approach == "aggressive":
            reactions["thane_warrior"] = "approves of decisive action"
            reactions["lyralei_ranger"] = "concerned about unnecessary violence"
        elif approach == "defensive":
            reactions["lyralei_ranger"] = "appreciates tactical thinking"
            reactions["kael_rogue"] = "suggests more creative approaches"
        
        return reactions
    
    def _get_companion_relationship_status(self, companion_id: str) -> Dict[str, Any]:
        """Get current relationship status with companion"""
        if companion_id in self.companion_system.companions:
            companion = self.companion_system.companions[companion_id]
            return {
                "relationship_type": companion.player_relationship.relationship_type.value,
                "trust": companion.player_relationship.trust,
                "affection": companion.player_relationship.affection
            }
        return {"status": "unknown"}
    
    def _generate_political_narrative(self, mission_result: Dict[str, Any]) -> str:
        """Generate narrative for political mission results"""
        if mission_result.get("success"):
            return f"Your diplomatic efforts in '{mission_result.get('mission_title', 'the mission')}' bear fruit, shifting the political landscape."
        else:
            return f"The mission '{mission_result.get('mission_title', 'political endeavor')}' faces complications, but provides valuable experience."
    
    def _get_new_story_opportunities(self, game_state: GameState) -> List[str]:
        """Get new story opportunities after arc progression"""
        return [
            "New faction missions become available",
            "Companion personal quests unlock", 
            "Ancient mysteries reveal themselves",
            "Political tensions create new challenges"
        ]
    
    def get_master_game_status(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive game status across all systems"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        game_state = self.active_sessions[session_id]
        
        return {
            "game_state": self._get_public_game_state(game_state),
            "story_status": self.story_engine.get_story_status(),
            "companion_status": self.companion_system.get_party_status(list(game_state.companion_relationships.keys())),
            "political_status": self.political_system.get_political_summary(),
            "world_status": self.world_simulation.get_world_status_summary(),
            "ai_status": self.adaptive_ai.get_ai_status(game_state.player_id),
            "combat_status": self.combat_engine.get_combat_status(),
            "alignment_status": self.alignment_karma.get_morality_summary(game_state.player_id),
            "session_info": {
                "session_id": session_id,
                "play_time": game_state.play_time,
                "last_save": game_state.last_save.isoformat()
            }
        }
    
    def save_game(self, session_id: str) -> Dict[str, Any]:
        """Save the current game state"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        game_state = self.active_sessions[session_id]
        game_state.last_save = datetime.now()
        
        # In a real implementation, this would save to persistent storage
        return {
            "save_successful": True,
            "save_time": game_state.last_save.isoformat(),
            "save_location": game_state.current_location
        } 