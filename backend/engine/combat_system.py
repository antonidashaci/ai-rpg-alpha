"""
BG3-Style Tactical Combat System
==================================

Baldur's Gate 3-inspired combat mechanics with:
- Environmental interactions and tactical positioning
- Multiple solution paths for every encounter
- Failure-as-content narrative branching
- Resource management (stamina, action points)
- Smart adaptive enemy AI

Design Philosophy:
- Every combat has multiple solutions (combat, stealth, diplomacy, environment)
- Failure creates new narrative opportunities, not dead ends
- Environmental interaction is crucial to success
- Player preparation and positioning matter
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random


class CombatDifficulty(Enum):
    """Combat difficulty levels"""
    STORY = "story"           # Narrative focus, simplified combat
    BALANCED = "balanced"     # Classic RPG challenge
    TACTICAL = "tactical"     # Advanced AI, positioning crucial
    HONOR = "honor"          # Permanent consequences, maximum challenge


class CombatOutcome(Enum):
    """Possible combat outcomes"""
    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPE = "escape"
    NEGOTIATION = "negotiation"
    ENVIRONMENTAL_KILL = "environmental_kill"
    STEALTH_BYPASS = "stealth_bypass"


class ActionType(Enum):
    """Available combat action types"""
    ATTACK = "attack"
    DEFEND = "defend"
    USE_ENVIRONMENT = "use_environment"
    CAST_SPELL = "cast_spell"
    USE_ITEM = "use_item"
    NEGOTIATE = "negotiate"
    FLEE = "flee"
    STEALTH = "stealth"
    POSITION = "position"


class TerrainType(Enum):
    """Environmental terrain types"""
    OPEN = "open"
    ELEVATED = "elevated"
    COVER = "cover"
    HAZARDOUS = "hazardous"
    DESTRUCTIBLE = "destructible"


@dataclass
class CombatResources:
    """Player combat resources"""
    stamina: int = 100
    max_stamina: int = 100
    action_points: int = 2
    max_action_points: int = 2
    
    def use_stamina(self, amount: int) -> bool:
        """Use stamina, return True if successful"""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def use_action_point(self) -> bool:
        """Use one action point"""
        if self.action_points > 0:
            self.action_points -= 1
            return True
        return False
    
    def restore_action_points(self):
        """Restore all action points (new turn)"""
        self.action_points = self.max_action_points
    
    def restore_stamina(self, amount: int):
        """Restore stamina"""
        self.stamina = min(self.stamina + amount, self.max_stamina)


@dataclass
class EnvironmentalFeature:
    """Environmental feature in combat arena"""
    feature_type: TerrainType
    name: str
    description: str
    is_destructible: bool = False
    provides_cover: bool = False
    elevation_bonus: int = 0
    damage_potential: int = 0
    uses_remaining: Optional[int] = None
    
    def can_use(self) -> bool:
        """Check if feature can still be used"""
        if self.uses_remaining is None:
            return True
        return self.uses_remaining > 0
    
    def use(self) -> bool:
        """Use the environmental feature"""
        if self.can_use():
            if self.uses_remaining is not None:
                self.uses_remaining -= 1
            return True
        return False


@dataclass
class Enemy:
    """Enemy combatant"""
    name: str
    health: int
    max_health: int
    attack_power: int
    defense: int
    intelligence: int  # Affects AI tactical decisions
    morale: int = 100  # Can flee if morale drops
    position: str = "neutral"
    status_effects: List[str] = field(default_factory=list)
    
    def is_alive(self) -> bool:
        """Check if enemy is still alive"""
        return self.health > 0
    
    def take_damage(self, amount: int) -> int:
        """Apply damage to enemy, return actual damage dealt"""
        actual_damage = max(0, amount - self.defense)
        self.health -= actual_damage
        self.morale -= actual_damage // 2
        return actual_damage
    
    def should_flee(self) -> bool:
        """Check if enemy should attempt to flee"""
        health_percent = (self.health / self.max_health) * 100
        return health_percent < 30 or self.morale < 25


@dataclass
class CombatState:
    """Complete combat encounter state"""
    encounter_id: str
    player_health: int
    player_max_health: int
    resources: CombatResources
    enemies: List[Enemy]
    environment: List[EnvironmentalFeature]
    difficulty: CombatDifficulty
    turn_number: int = 1
    narrative_context: str = ""
    available_actions: List[ActionType] = field(default_factory=list)
    combat_log: List[str] = field(default_factory=list)
    
    def is_combat_over(self) -> Tuple[bool, Optional[CombatOutcome]]:
        """Check if combat has ended and determine outcome"""
        # All enemies defeated
        if not any(e.is_alive() for e in self.enemies):
            return True, CombatOutcome.VICTORY
        
        # Player defeated
        if self.player_health <= 0:
            return True, CombatOutcome.DEFEAT
        
        # All enemies fled
        if all(e.morale < 10 for e in self.enemies if e.is_alive()):
            return True, CombatOutcome.ESCAPE
        
        return False, None
    
    def add_to_log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(f"[Turn {self.turn_number}] {message}")


class TacticalCombatEngine:
    """
    BG3-Style Tactical Combat Engine
    
    Handles combat encounters with multiple solution paths:
    1. Direct combat with tactical positioning
    2. Environmental manipulation
    3. Stealth and avoidance
    4. Social/negotiation solutions
    5. Combination approaches
    """
    
    def __init__(self, difficulty: CombatDifficulty = CombatDifficulty.BALANCED):
        self.difficulty = difficulty
        self.action_costs = {
            ActionType.ATTACK: (1, 20),  # (action_points, stamina)
            ActionType.DEFEND: (1, 10),
            ActionType.USE_ENVIRONMENT: (1, 15),
            ActionType.CAST_SPELL: (1, 30),
            ActionType.USE_ITEM: (0, 5),
            ActionType.NEGOTIATE: (2, 0),
            ActionType.FLEE: (1, 30),
            ActionType.STEALTH: (1, 25),
            ActionType.POSITION: (0, 10),
        }
    
    def create_encounter(
        self,
        encounter_id: str,
        enemies: List[Enemy],
        environment: List[EnvironmentalFeature],
        player_health: int,
        player_max_health: int,
        narrative_context: str
    ) -> CombatState:
        """Create a new combat encounter"""
        state = CombatState(
            encounter_id=encounter_id,
            player_health=player_health,
            player_max_health=player_max_health,
            resources=CombatResources(),
            enemies=enemies,
            environment=environment,
            difficulty=self.difficulty,
            narrative_context=narrative_context,
            available_actions=self._determine_available_actions(enemies, environment)
        )
        
        state.add_to_log(f"Combat initiated: {encounter_id}")
        return state
    
    def _determine_available_actions(
        self, 
        enemies: List[Enemy], 
        environment: List[EnvironmentalFeature]
    ) -> List[ActionType]:
        """Determine which actions are available in this encounter"""
        actions = [ActionType.ATTACK, ActionType.DEFEND, ActionType.USE_ITEM, ActionType.FLEE]
        
        # Add environmental actions if features exist
        if any(e.can_use() for e in environment):
            actions.append(ActionType.USE_ENVIRONMENT)
        
        # Add negotiation if enemies are intelligent enough
        if any(e.intelligence > 5 for e in enemies):
            actions.append(ActionType.NEGOTIATE)
        
        # Add stealth if not already engaged
        actions.append(ActionType.STEALTH)
        
        # Positioning always available
        actions.append(ActionType.POSITION)
        
        return actions
    
    def execute_action(
        self,
        state: CombatState,
        action: ActionType,
        target_index: Optional[int] = None,
        environment_index: Optional[int] = None,
        player_stats: Optional[Dict] = None
    ) -> Tuple[CombatState, str, bool]:
        """
        Execute a combat action
        
        Returns:
            - Updated combat state
            - Narrative description of action result
            - Success boolean
        """
        ap_cost, stamina_cost = self.action_costs.get(action, (1, 10))
        
        # Check if player has resources
        if not state.resources.use_action_point():
            return state, "You don't have enough action points!", False
        
        if not state.resources.use_stamina(stamina_cost):
            state.resources.action_points += 1  # Refund AP
            return state, "You don't have enough stamina!", False
        
        # Execute specific action
        if action == ActionType.ATTACK:
            return self._execute_attack(state, target_index, player_stats)
        elif action == ActionType.USE_ENVIRONMENT:
            return self._execute_environmental_action(state, environment_index, target_index)
        elif action == ActionType.NEGOTIATE:
            return self._execute_negotiation(state, player_stats)
        elif action == ActionType.DEFEND:
            return self._execute_defend(state)
        elif action == ActionType.FLEE:
            return self._execute_flee(state)
        elif action == ActionType.STEALTH:
            return self._execute_stealth(state, player_stats)
        elif action == ActionType.POSITION:
            return self._execute_positioning(state)
        else:
            return state, "Action not yet implemented", False
    
    def _execute_attack(
        self, 
        state: CombatState, 
        target_index: Optional[int],
        player_stats: Optional[Dict]
    ) -> Tuple[CombatState, str, bool]:
        """Execute direct attack action"""
        if target_index is None or target_index >= len(state.enemies):
            return state, "Invalid target!", False
        
        target = state.enemies[target_index]
        if not target.is_alive():
            return state, "Target is already defeated!", False
        
        # Calculate damage
        base_damage = player_stats.get('strength', 10) if player_stats else 10
        roll = random.randint(1, 20)  # D20 roll
        
        critical = roll >= 18
        hit = roll + (player_stats.get('attack_bonus', 0) if player_stats else 0) > target.defense
        
        if critical:
            damage = base_damage * 2
            actual_damage = target.take_damage(damage)
            narrative = f"🎯 CRITICAL HIT! You strike {target.name} with devastating force, dealing {actual_damage} damage!"
        elif hit:
            damage = base_damage
            actual_damage = target.take_damage(damage)
            narrative = f"⚔️ You hit {target.name} for {actual_damage} damage!"
        else:
            narrative = f"❌ Your attack misses {target.name}!"
            actual_damage = 0
        
        state.add_to_log(narrative)
        
        if not target.is_alive():
            defeat_narrative = f"💀 {target.name} has been defeated!"
            state.add_to_log(defeat_narrative)
            narrative += f"\n{defeat_narrative}"
        
        return state, narrative, True
    
    def _execute_environmental_action(
        self,
        state: CombatState,
        environment_index: Optional[int],
        target_index: Optional[int]
    ) -> Tuple[CombatState, str, bool]:
        """Execute environmental manipulation"""
        if environment_index is None or environment_index >= len(state.environment):
            return state, "Invalid environmental feature!", False
        
        feature = state.environment[environment_index]
        if not feature.use():
            return state, f"{feature.name} can no longer be used!", False
        
        # Apply environmental effect
        narrative = f"🌍 You utilize the {feature.name}!\n{feature.description}"
        
        if feature.damage_potential > 0 and target_index is not None:
            if target_index < len(state.enemies):
                target = state.enemies[target_index]
                damage = feature.damage_potential
                actual_damage = target.take_damage(damage)
                narrative += f"\n💥 Environmental damage: {actual_damage} to {target.name}!"
                
                if not target.is_alive():
                    narrative += f"\n💀 {target.name} is eliminated by the environment!"
                    state.add_to_log(f"Environmental kill: {target.name}")
        
        state.add_to_log(f"Used environment: {feature.name}")
        return state, narrative, True
    
    def _execute_negotiation(
        self,
        state: CombatState,
        player_stats: Optional[Dict]
    ) -> Tuple[CombatState, str, bool]:
        """Attempt to negotiate with enemies"""
        charisma = player_stats.get('charisma', 10) if player_stats else 10
        intelligence = player_stats.get('intelligence', 10) if player_stats else 10
        
        roll = random.randint(1, 20)
        success_threshold = 15 - (charisma // 2) - (intelligence // 3)
        
        if roll >= success_threshold:
            # Successful negotiation
            for enemy in state.enemies:
                enemy.morale = 0  # Enemies stand down
            
            narrative = (
                f"🗣️ Your words cut through the tension (rolled {roll})!\n"
                f"Through clever diplomacy and persuasion, you've convinced your opponents "
                f"that fighting is not in their best interest. They lower their weapons."
            )
            state.add_to_log("Successful negotiation - combat avoided")
            return state, narrative, True
        else:
            # Failed negotiation
            narrative = (
                f"🗣️ Your attempt at negotiation falls flat (rolled {roll}).\n"
                f"Your words don't have the desired effect. Combat continues!"
            )
            state.add_to_log("Failed negotiation attempt")
            return state, narrative, False
    
    def _execute_defend(self, state: CombatState) -> Tuple[CombatState, str, bool]:
        """Take defensive stance"""
        state.resources.restore_stamina(20)
        narrative = (
            "🛡️ You take a defensive stance, catching your breath and preparing for the next move.\n"
            "Stamina restored: +20"
        )
        state.add_to_log("Defensive stance taken")
        return state, narrative, True
    
    def _execute_flee(self, state: CombatState) -> Tuple[CombatState, str, bool]:
        """Attempt to flee from combat"""
        roll = random.randint(1, 20)
        
        if roll >= 12:
            state.player_health = -999  # Flag for escape (not actual damage)
            narrative = (
                f"🏃 You successfully disengage and escape from combat! (rolled {roll})\n"
                f"While this isn't a glorious victory, living to fight another day has its merits."
            )
            state.add_to_log("Successful escape")
            return state, narrative, True
        else:
            narrative = (
                f"🏃 Your escape attempt fails! (rolled {roll})\n"
                f"The enemies block your path. You'll have to fight or find another way out."
            )
            state.add_to_log("Failed escape attempt")
            return state, narrative, False
    
    def _execute_stealth(
        self,
        state: CombatState,
        player_stats: Optional[Dict]
    ) -> Tuple[CombatState, str, bool]:
        """Attempt stealth approach"""
        dexterity = player_stats.get('dexterity', 10) if player_stats else 10
        roll = random.randint(1, 20)
        
        success_threshold = 14 - (dexterity // 3)
        
        if roll >= success_threshold:
            # Successful stealth - enemies lose track
            for enemy in state.enemies:
                enemy.attack_power = max(1, enemy.attack_power - 2)
            
            narrative = (
                f"🥷 You melt into the shadows! (rolled {roll})\n"
                f"Your enemies are confused and disoriented. Their effectiveness is reduced."
            )
            state.add_to_log("Successful stealth maneuver")
            return state, narrative, True
        else:
            narrative = (
                f"🥷 Your stealth attempt is noticed! (rolled {roll})\n"
                f"You're spotted before you can gain an advantage."
            )
            state.add_to_log("Failed stealth attempt")
            return state, narrative, False
    
    def _execute_positioning(self, state: CombatState) -> Tuple[CombatState, str, bool]:
        """Reposition for tactical advantage"""
        state.resources.restore_stamina(10)
        narrative = (
            "🎯 You carefully reposition yourself for a better tactical advantage.\n"
            "This movement may open up new opportunities. Stamina +10"
        )
        state.add_to_log("Tactical repositioning")
        return state, narrative, True
    
    def process_enemy_turn(self, state: CombatState) -> Tuple[CombatState, str]:
        """Process all enemy actions"""
        narratives = []
        
        for i, enemy in enumerate(state.enemies):
            if not enemy.is_alive():
                continue
            
            # Check if enemy should flee
            if enemy.should_flee():
                narratives.append(f"💨 {enemy.name} flees from battle!")
                enemy.morale = 0
                continue
            
            # AI decision making based on intelligence
            action_result = self._enemy_ai_decision(state, enemy, i)
            narratives.append(action_result)
        
        state.turn_number += 1
        state.resources.restore_action_points()
        
        combined_narrative = "\n\n".join(narratives) if narratives else "Enemies pause, reassessing the situation."
        return state, combined_narrative
    
    def _enemy_ai_decision(self, state: CombatState, enemy: Enemy, enemy_index: int) -> str:
        """AI decision making for enemy actions"""
        # Simple AI for now - can be enhanced with more sophisticated tactics
        
        if enemy.intelligence > 10:
            # Smart enemies may use environment or tactics
            if state.environment and random.random() < 0.3:
                return f"🧠 {enemy.name} uses the environment tactically!"
        
        # Basic attack
        damage = random.randint(1, enemy.attack_power)
        state.player_health -= damage
        
        return f"⚔️ {enemy.name} attacks you for {damage} damage! (Health: {state.player_health}/{state.player_max_health})"
    
    def generate_narrative_outcome(
        self,
        state: CombatState,
        outcome: CombatOutcome
    ) -> str:
        """Generate narrative text for combat outcome"""
        if outcome == CombatOutcome.VICTORY:
            return (
                "🎉 **VICTORY!**\n\n"
                "Your tactical prowess and combat skills have won the day. "
                "The battlefield falls silent as the last of your enemies is vanquished. "
                f"You catch your breath, bloodied but victorious. (Turn {state.turn_number})\n\n"
                "The consequences of this battle will ripple through your journey..."
            )
        elif outcome == CombatOutcome.DEFEAT:
            return (
                "💀 **DEFEAT...**\n\n"
                "The world fades to black as you fall to your knees. "
                "But this is not the end of your story—merely a dark chapter. "
                "Every defeat is a lesson, and this one will shape what comes next...\n\n"
                "**[Failure-as-Content: New narrative paths unlocked]**"
            )
        elif outcome == CombatOutcome.NEGOTIATION:
            return (
                "🤝 **DIPLOMATIC RESOLUTION**\n\n"
                "Through wit and words rather than steel and blood, you've found another path. "
                "Sometimes the greatest victories are those achieved without violence. "
                "Your reputation as a skilled negotiator grows..."
            )
        elif outcome == CombatOutcome.ENVIRONMENTAL_KILL:
            return (
                "🌍 **ENVIRONMENTAL MASTERY**\n\n"
                "You've used your surroundings to devastating effect! "
                "True warriors know that the battlefield itself can be their greatest weapon. "
                "Your tactical creativity has been rewarded."
            )
        elif outcome == CombatOutcome.ESCAPE:
            return (
                "🏃 **STRATEGIC RETREAT**\n\n"
                "Discretion is the better part of valor. You've escaped with your life, "
                "and sometimes that's the smartest move. This isn't over, but you'll "
                "face this challenge again on your own terms..."
            )
        else:
            return "The combat encounter concludes in an unexpected way..."


# ============================================================================
# ENCOUNTER TEMPLATES
# ============================================================================

class CombatEncounterLibrary:
    """Pre-designed combat encounters with multiple solution paths"""
    
    @staticmethod
    def get_fantasy_encounter(encounter_type: str = "bandit"):
        """Get fantasy encounter from library"""
        from .fantasy_encounters import FantasyEncounters
        
        encounters = {
            "dragon": FantasyEncounters.dragon_encounter,
            "orc": FantasyEncounters.orc_warband,
            "undead": FantasyEncounters.undead_legion,
            "assassin": FantasyEncounters.royal_assassins,
            "troll": FantasyEncounters.troll_bridge,
            "giant": FantasyEncounters.frost_giant_raid,
            "bandit": lambda: CombatEncounterLibrary.bandit_ambush()
        }
        
        return encounters.get(encounter_type, encounters["bandit"])()
    
    @staticmethod
    def bandit_ambush() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Classic bandit ambush encounter
        Solutions: Combat, negotiation (pay bribe), environmental (collapse bridge), stealth
        """
        enemies = [
            Enemy(
                name="Bandit Leader",
                health=30,
                max_health=30,
                attack_power=8,
                defense=3,
                intelligence=8,
                morale=80
            ),
            Enemy(
                name="Bandit Thug",
                health=20,
                max_health=20,
                attack_power=6,
                defense=2,
                intelligence=4,
                morale=60
            ),
            Enemy(
                name="Bandit Archer",
                health=15,
                max_health=15,
                attack_power=7,
                defense=1,
                intelligence=5,
                morale=50
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Rope Bridge",
                description="A rickety rope bridge spans a ravine. Cutting it could eliminate threats... or cut off escape.",
                is_destructible=True,
                damage_potential=20,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Large Boulders",
                description="Massive boulders provide excellent cover from ranged attacks.",
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.ELEVATED,
                name="Rocky Outcrop",
                description="Higher ground gives tactical advantage.",
                elevation_bonus=2
            )
        ]
        
        context = (
            "A group of bandits has ambushed you on a narrow mountain path! "
            "The Bandit Leader grins wickedly, while his thugs surround you. "
            "The rope bridge behind them sways in the wind..."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def cosmic_horror_cultists() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Cosmic horror scenario encounter
        Solutions: Combat, disrupt ritual, environmental (destroy altar), sanity attack
        """
        enemies = [
            Enemy(
                name="Cult Priest",
                health=25,
                max_health=25,
                attack_power=6,
                defense=2,
                intelligence=12,
                morale=100  # Fanatics don't flee
            ),
            Enemy(
                name="Cult Fanatic",
                health=18,
                max_health=18,
                attack_power=5,
                defense=1,
                intelligence=6,
                morale=100
            ),
            Enemy(
                name="Cult Fanatic",
                health=18,
                max_health=18,
                attack_power=5,
                defense=1,
                intelligence=6,
                morale=100
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Eldritch Altar",
                description="A pulsing altar radiates wrongness. Destroying it might end the ritual... or unleash something worse.",
                is_destructible=True,
                damage_potential=30,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Reality Distortion",
                description="The fabric of reality itself seems thin here. This could be weaponized by those brave (or foolish) enough.",
                damage_potential=25,
                uses_remaining=2
            )
        ]
        
        context = (
            "You stumble upon cultists mid-ritual. The air itself feels wrong. "
            "Reality bends and warps around their eldritch altar. Their eyes "
            "gleam with mad purpose. The chanting grows louder..."
        )
        
        return enemies, environment, context

