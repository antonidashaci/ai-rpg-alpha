"""
AI-RPG-Alpha: Narrative Combat Resolver

This module handles combat resolution through narrative generation rather than
traditional turn-based mechanics. It uses AI to create engaging combat stories
based on player stats, choices, and enemy characteristics.
"""

from typing import Dict, Any, List, Optional, Tuple
import random
from enum import Enum

from models.dataclasses import Player, PlayerStats
from ai.openai_client import OpenAIClient
from ai.templates import PromptTemplates

class CombatOutcome(Enum):
    """Possible combat outcomes"""
    CRITICAL_SUCCESS = "critical_success"
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    CRITICAL_FAILURE = "critical_failure"

class CombatType(Enum):
    """Types of combat encounters"""
    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    STEALTH = "stealth"
    SOCIAL = "social"  # Verbal sparring, intimidation, etc.

class NarrativeCombatResolver:
    """
    Resolves combat encounters through AI-generated narratives.
    
    Instead of traditional dice rolls and hit points, this system uses
    player stats and AI creativity to generate engaging combat stories
    with meaningful outcomes.
    """
    
    def __init__(self, ai_client: OpenAIClient):
        """
        Initialize the combat resolver.
        
        Args:
            ai_client: OpenAI client for narrative generation
        """
        self.ai_client = ai_client
        self.templates = PromptTemplates()
        
        # Combat difficulty modifiers
        self.difficulty_modifiers = {
            "trivial": {"stat_bonus": 5, "damage_reduction": 0.5},
            "easy": {"stat_bonus": 2, "damage_reduction": 0.7},
            "medium": {"stat_bonus": 0, "damage_reduction": 1.0},
            "hard": {"stat_bonus": -2, "damage_reduction": 1.3},
            "epic": {"stat_bonus": -5, "damage_reduction": 1.5}
        }
        
        # Enemy archetypes with stat requirements
        self.enemy_archetypes = {
            "goblin": {
                "required_strength": 8,
                "required_intelligence": 5,
                "weakness": "light",
                "resistance": "none",
                "tactics": "swarm"
            },
            "orc_warrior": {
                "required_strength": 12,
                "required_intelligence": 6,
                "weakness": "magic",
                "resistance": "physical",
                "tactics": "aggressive"
            },
            "skeleton": {
                "required_strength": 10,
                "required_intelligence": 8,
                "weakness": "holy",
                "resistance": "piercing",
                "tactics": "relentless"
            },
            "bandit": {
                "required_strength": 9,
                "required_intelligence": 10,
                "weakness": "surprise",
                "resistance": "none",
                "tactics": "cunning"
            },
            "wolf": {
                "required_strength": 11,
                "required_intelligence": 7,
                "weakness": "fire",
                "resistance": "cold",
                "tactics": "pack"
            },
            "dragon": {
                "required_strength": 18,
                "required_intelligence": 15,
                "weakness": "ancient_magic",
                "resistance": "most_attacks",
                "tactics": "overwhelming"
            }
        }
    
    def resolve_combat(
        self, 
        player: Player,
        enemy_description: str,
        player_action: str,
        combat_context: str = "",
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Resolve a combat encounter narratively.
        
        Args:
            player: Player object with current stats
            enemy_description: Description of the enemy
            player_action: Player's chosen combat action
            combat_context: Additional context about the combat situation
            difficulty: Combat difficulty level
            
        Returns:
            Dictionary containing combat results and narrative
        """
        # Determine combat type from player action
        combat_type = self._determine_combat_type(player_action)
        
        # Calculate base outcome probability
        outcome_probability = self._calculate_outcome_probability(
            player, enemy_description, combat_type, difficulty
        )
        
        # Determine outcome
        outcome = self._determine_outcome(outcome_probability)
        
        # Generate narrative using AI
        narrative = self._generate_combat_narrative(
            player, enemy_description, player_action, combat_context, outcome
        )
        
        # Calculate consequences
        consequences = self._calculate_combat_consequences(
            player, outcome, combat_type, difficulty
        )
        
        # Determine if combat continues
        combat_continues = self._should_combat_continue(outcome, consequences)
        
        return {
            "narrative": narrative,
            "outcome": outcome.value,
            "consequences": consequences,
            "combat_continues": combat_continues,
            "combat_type": combat_type.value,
            "difficulty": difficulty,
            "player_action": player_action
        }
    
    def generate_enemy_encounter(
        self, 
        location: str, 
        player_level: int,
        encounter_type: str = "random"
    ) -> Dict[str, Any]:
        """
        Generate a random enemy encounter appropriate for the location and player level.
        
        Args:
            location: Current location
            player_level: Player's current level
            encounter_type: Type of encounter (random, boss, ambush, etc.)
            
        Returns:
            Dictionary describing the enemy encounter
        """
        # Select appropriate enemy based on location and level
        enemy_type = self._select_enemy_type(location, player_level, encounter_type)
        
        # Generate enemy description using AI
        enemy_prompt = f"""
        Generate a detailed description of a {enemy_type} encounter in {location}.
        The encounter should be appropriate for a level {player_level} player.
        Include the enemy's appearance, behavior, and immediate threat level.
        Keep the description to 2-3 sentences and make it atmospheric.
        """
        
        enemy_description = self.ai_client.generate_narrative(
            enemy_prompt,
            context={"location": location, "player_level": player_level},
            temperature=0.8
        )
        
        # Determine difficulty
        difficulty = self._determine_encounter_difficulty(player_level, encounter_type)
        
        return {
            "enemy_type": enemy_type,
            "description": enemy_description,
            "difficulty": difficulty,
            "location": location,
            "encounter_type": encounter_type,
            "suggested_actions": self._generate_combat_suggestions(enemy_type)
        }
    
    def _determine_combat_type(self, player_action: str) -> CombatType:
        """Determine combat type from player action"""
        action_lower = player_action.lower()
        
        if any(word in action_lower for word in ["sword", "axe", "club", "punch", "kick", "melee"]):
            return CombatType.MELEE
        elif any(word in action_lower for word in ["bow", "arrow", "throw", "sling", "ranged"]):
            return CombatType.RANGED
        elif any(word in action_lower for word in ["spell", "magic", "cast", "enchant", "fireball"]):
            return CombatType.MAGIC
        elif any(word in action_lower for word in ["sneak", "stealth", "hide", "backstab", "ambush"]):
            return CombatType.STEALTH
        elif any(word in action_lower for word in ["talk", "negotiate", "intimidate", "persuade", "bluff"]):
            return CombatType.SOCIAL
        else:
            return CombatType.MELEE  # Default to melee
    
    def _calculate_outcome_probability(
        self, 
        player: Player, 
        enemy_description: str,
        combat_type: CombatType,
        difficulty: str
    ) -> Dict[str, float]:
        """Calculate probability of different outcomes"""
        # Base probabilities
        base_probs = {
            CombatOutcome.CRITICAL_SUCCESS: 0.05,
            CombatOutcome.SUCCESS: 0.35,
            CombatOutcome.PARTIAL_SUCCESS: 0.35,
            CombatOutcome.FAILURE: 0.20,
            CombatOutcome.CRITICAL_FAILURE: 0.05
        }
        
        # Adjust based on relevant player stats
        stat_modifier = self._get_stat_modifier(player, combat_type)
        
        # Adjust based on difficulty
        difficulty_mod = self.difficulty_modifiers.get(difficulty, {"stat_bonus": 0})
        total_modifier = stat_modifier + difficulty_mod["stat_bonus"]
        
        # Apply modifier to probabilities
        adjusted_probs = {}
        for outcome, prob in base_probs.items():
            if outcome in [CombatOutcome.CRITICAL_SUCCESS, CombatOutcome.SUCCESS]:
                # Positive outcomes benefit from higher stats
                adjusted_probs[outcome] = max(0, prob + (total_modifier * 0.02))
            elif outcome in [CombatOutcome.FAILURE, CombatOutcome.CRITICAL_FAILURE]:
                # Negative outcomes reduced by higher stats
                adjusted_probs[outcome] = max(0, prob - (total_modifier * 0.02))
            else:
                adjusted_probs[outcome] = prob
        
        # Normalize probabilities
        total_prob = sum(adjusted_probs.values())
        if total_prob > 0:
            adjusted_probs = {k: v / total_prob for k, v in adjusted_probs.items()}
        
        return adjusted_probs
    
    def _get_stat_modifier(self, player: Player, combat_type: CombatType) -> int:
        """Get stat modifier based on combat type"""
        if combat_type == CombatType.MELEE:
            return player.stats.strength - 10
        elif combat_type == CombatType.RANGED:
            return (player.stats.strength + player.stats.intelligence) // 2 - 10
        elif combat_type == CombatType.MAGIC:
            return player.stats.intelligence - 10
        elif combat_type == CombatType.STEALTH:
            return (player.stats.intelligence + player.stats.charisma) // 2 - 10
        elif combat_type == CombatType.SOCIAL:
            return player.stats.charisma - 10
        else:
            return 0
    
    def _determine_outcome(self, probabilities: Dict[CombatOutcome, float]) -> CombatOutcome:
        """Determine outcome based on probabilities"""
        rand_value = random.random()
        cumulative_prob = 0
        
        for outcome, prob in probabilities.items():
            cumulative_prob += prob
            if rand_value <= cumulative_prob:
                return outcome
        
        return CombatOutcome.PARTIAL_SUCCESS  # Fallback
    
    def _generate_combat_narrative(
        self,
        player: Player,
        enemy_description: str,
        player_action: str,
        combat_context: str,
        outcome: CombatOutcome
    ) -> str:
        """Generate combat narrative using AI"""
        # Build context for narrative generation
        context = {
            "player_stats": player.stats.__dict__,
            "player_inventory": player.inventory,
            "outcome": outcome.value,
            "combat_context": combat_context
        }
        
        # Use template to build prompt
        prompt = self.templates.render_combat_prompt(
            player=player.to_dict(),
            enemy_description=enemy_description,
            player_action=player_action,
            combat_context=combat_context
        )
        
        # Add outcome guidance to prompt
        outcome_guidance = self._get_outcome_guidance(outcome)
        full_prompt = f"{prompt}\n\nOutcome Guidance: {outcome_guidance}"
        
        return self.ai_client.generate_narrative(
            full_prompt,
            context=context,
            temperature=0.8,
            max_tokens=400
        )
    
    def _get_outcome_guidance(self, outcome: CombatOutcome) -> str:
        """Get narrative guidance based on outcome"""
        guidance = {
            CombatOutcome.CRITICAL_SUCCESS: "The player achieves spectacular success with minimal risk or effort. Describe a heroic, impressive victory.",
            CombatOutcome.SUCCESS: "The player succeeds in their action with good results. Describe a solid, competent victory.",
            CombatOutcome.PARTIAL_SUCCESS: "The player partially succeeds but with complications or costs. Describe mixed results.",
            CombatOutcome.FAILURE: "The player's action fails but without catastrophic consequences. Describe a setback that can be recovered from.",
            CombatOutcome.CRITICAL_FAILURE: "The player fails badly with serious consequences. Describe a significant setback or danger."
        }
        return guidance.get(outcome, "Describe the outcome of the combat action.")
    
    def _calculate_combat_consequences(
        self,
        player: Player,
        outcome: CombatOutcome,
        combat_type: CombatType,
        difficulty: str
    ) -> Dict[str, Any]:
        """Calculate the consequences of combat"""
        consequences = {
            "health_change": 0,
            "mana_change": 0,
            "experience_gain": 0,
            "status_effects": [],
            "loot": [],
            "story_flags": []
        }
        
        # Base consequences by outcome
        if outcome == CombatOutcome.CRITICAL_SUCCESS:
            consequences["health_change"] = 0
            consequences["experience_gain"] = 30
            consequences["loot"] = ["minor_treasure"]
            consequences["story_flags"] = ["heroic_victory"]
        elif outcome == CombatOutcome.SUCCESS:
            consequences["health_change"] = -5
            consequences["experience_gain"] = 20
            consequences["loot"] = ["small_reward"]
        elif outcome == CombatOutcome.PARTIAL_SUCCESS:
            consequences["health_change"] = -15
            consequences["experience_gain"] = 10
            consequences["status_effects"] = ["minor_injury"]
        elif outcome == CombatOutcome.FAILURE:
            consequences["health_change"] = -25
            consequences["experience_gain"] = 5
            consequences["status_effects"] = ["wounded"]
        elif outcome == CombatOutcome.CRITICAL_FAILURE:
            consequences["health_change"] = -40
            consequences["experience_gain"] = 0
            consequences["status_effects"] = ["seriously_wounded"]
            consequences["story_flags"] = ["combat_trauma"]
        
        # Adjust for difficulty
        difficulty_mod = self.difficulty_modifiers.get(difficulty, {"damage_reduction": 1.0})
        consequences["health_change"] = int(consequences["health_change"] * difficulty_mod["damage_reduction"])
        
        # Adjust for combat type
        if combat_type == CombatType.MAGIC:
            consequences["mana_change"] = -10  # Magic costs mana
        elif combat_type == CombatType.STEALTH and outcome in [CombatOutcome.SUCCESS, CombatOutcome.CRITICAL_SUCCESS]:
            consequences["health_change"] = max(consequences["health_change"], -5)  # Stealth reduces damage taken
        
        return consequences
    
    def _should_combat_continue(
        self, 
        outcome: CombatOutcome, 
        consequences: Dict[str, Any]
    ) -> bool:
        """Determine if combat should continue"""
        # Combat ends on critical success (enemy defeated)
        if outcome == CombatOutcome.CRITICAL_SUCCESS:
            return False
        
        # Combat might end on regular success (depends on enemy)
        if outcome == CombatOutcome.SUCCESS:
            return random.random() < 0.3  # 30% chance to continue
        
        # Combat usually continues on other outcomes
        return True
    
    def _select_enemy_type(
        self, 
        location: str, 
        player_level: int, 
        encounter_type: str
    ) -> str:
        """Select appropriate enemy type"""
        location_enemies = {
            "starting_village": ["bandit", "wolf"],
            "forest_entrance": ["wolf", "goblin", "bandit"],
            "ancient_ruins": ["skeleton", "goblin", "orc_warrior"],
            "deep_forest": ["wolf", "orc_warrior", "dragon"],
            "mountain_pass": ["orc_warrior", "dragon"],
            "dungeon": ["skeleton", "orc_warrior", "dragon"]
        }
        
        # Get enemies for location
        possible_enemies = location_enemies.get(location, ["goblin", "bandit"])
        
        # Filter by player level appropriateness
        suitable_enemies = []
        for enemy in possible_enemies:
            enemy_data = self.enemy_archetypes.get(enemy, {})
            required_strength = enemy_data.get("required_strength", 8)
            
            # Allow enemies that are challenging but not impossible
            if player_level * 3 + 5 >= required_strength:
                suitable_enemies.append(enemy)
        
        if not suitable_enemies:
            suitable_enemies = ["goblin"]  # Fallback
        
        # Special handling for boss encounters
        if encounter_type == "boss" and "dragon" in suitable_enemies:
            return "dragon"
        
        return random.choice(suitable_enemies)
    
    def _determine_encounter_difficulty(self, player_level: int, encounter_type: str) -> str:
        """Determine encounter difficulty"""
        if encounter_type == "boss":
            return "epic"
        elif encounter_type == "ambush":
            return "hard"
        elif player_level <= 2:
            return "easy"
        elif player_level <= 5:
            return "medium"
        else:
            return "hard"
    
    def _generate_combat_suggestions(self, enemy_type: str) -> List[str]:
        """Generate suggested combat actions for enemy type"""
        enemy_data = self.enemy_archetypes.get(enemy_type, {})
        weakness = enemy_data.get("weakness", "none")
        tactics = enemy_data.get("tactics", "standard")
        
        suggestions = [
            "Attack with your weapon",
            "Try to find a tactical advantage",
            "Attempt to negotiate or intimidate",
            "Look for an escape route"
        ]
        
        # Add specific suggestions based on enemy
        if weakness == "light":
            suggestions.append("Use bright light or fire against this creature")
        elif weakness == "magic":
            suggestions.append("Cast a spell if you know magic")
        elif weakness == "holy":
            suggestions.append("Use blessed items or holy symbols")
        elif weakness == "fire":
            suggestions.append("Use fire-based attacks")
        
        if tactics == "swarm":
            suggestions.append("Try to separate them or find high ground")
        elif tactics == "cunning":
            suggestions.append("Be wary of tricks and traps")
        elif tactics == "pack":
            suggestions.append("Watch for coordinated attacks")
        
        return suggestions[:4]  # Return top 4 suggestions

