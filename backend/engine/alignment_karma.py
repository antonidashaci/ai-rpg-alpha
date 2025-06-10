from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
import random
import json


class MoralAlignment(Enum):
    """Classic D&D-style alignment system"""
    LAWFUL_GOOD = "lawful_good"
    NEUTRAL_GOOD = "neutral_good"
    CHAOTIC_GOOD = "chaotic_good"
    LAWFUL_NEUTRAL = "lawful_neutral"
    TRUE_NEUTRAL = "true_neutral"
    CHAOTIC_NEUTRAL = "chaotic_neutral"
    LAWFUL_EVIL = "lawful_evil"
    NEUTRAL_EVIL = "neutral_evil"
    CHAOTIC_EVIL = "chaotic_evil"


class KarmaAction(Enum):
    """Types of karma-affecting actions"""
    # Good Actions
    SAVE_INNOCENT = "save_innocent"
    HELP_POOR = "help_poor"
    SHOW_MERCY = "show_mercy"
    KEEP_PROMISE = "keep_promise"
    SELF_SACRIFICE = "self_sacrifice"
    PROTECT_WEAK = "protect_weak"
    HEAL_WOUNDED = "heal_wounded"
    DONATE_CHARITY = "donate_charity"
    
    # Evil Actions
    MURDER_INNOCENT = "murder_innocent"
    STEAL_FROM_POOR = "steal_from_poor"
    TORTURE = "torture"
    BREAK_PROMISE = "break_promise"
    BETRAY_ALLY = "betray_ally"
    EXTORT = "extort"
    DESECRATE = "desecrate"
    MASSACRE = "massacre"
    
    # Lawful Actions
    UPHOLD_LAW = "uphold_law"
    FOLLOW_ORDERS = "follow_orders"
    HONOR_CONTRACT = "honor_contract"
    RESPECT_AUTHORITY = "respect_authority"
    MAINTAIN_ORDER = "maintain_order"
    
    # Chaotic Actions
    BREAK_LAW = "break_law"
    DEFY_AUTHORITY = "defy_authority"
    ACT_IMPULSIVELY = "act_impulsively"
    CAUSE_CHAOS = "cause_chaos"
    REBEL = "rebel"
    
    # Neutral/Indifferent Actions
    IGNORE_SUFFERING = "ignore_suffering"
    SELFISH_CHOICE = "selfish_choice"
    PRAGMATIC_DECISION = "pragmatic_decision"
    AVOID_INVOLVEMENT = "avoid_involvement"


class ReputationLevel(Enum):
    """Player reputation levels with different groups"""
    REVERED = "revered"      # +80 to +100
    RESPECTED = "respected"   # +60 to +79
    LIKED = "liked"          # +40 to +59
    TRUSTED = "trusted"      # +20 to +39
    NEUTRAL = "neutral"      # -19 to +19
    DISLIKED = "disliked"    # -39 to -20
    MISTRUSTED = "mistrusted" # -59 to -40
    DESPISED = "despised"    # -79 to -60
    HATED = "hated"          # -100 to -80


@dataclass
class KarmaEvent:
    """Record of a karma-affecting action"""
    action: KarmaAction
    magnitude: int  # -100 to +100
    description: str
    location: str
    witnesses: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Impact on different groups
    faction_impact: Dict[str, int] = field(default_factory=dict)
    companion_impact: Dict[str, int] = field(default_factory=dict)
    
    # Long-term consequences
    unlocks_quests: List[str] = field(default_factory=list)
    locks_quests: List[str] = field(default_factory=list)
    story_flags: List[str] = field(default_factory=list)


@dataclass
class AlignmentShift:
    """Tracks gradual alignment changes"""
    old_alignment: MoralAlignment
    new_alignment: MoralAlignment
    trigger_event: str
    shift_magnitude: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PlayerReputation:
    """Player's reputation with different groups"""
    # General reputation categories
    lawful_authorities: int = 0    # Guards, nobles, officials
    common_folk: int = 0          # Peasants, merchants, civilians
    criminal_underworld: int = 0   # Thieves, assassins, smugglers
    religious_orders: int = 0      # Priests, paladins, clerics
    magical_community: int = 0     # Mages, scholars, magical beings
    
    # Faction-specific reputation
    faction_reputation: Dict[str, int] = field(default_factory=dict)
    
    # Location-specific reputation
    location_reputation: Dict[str, int] = field(default_factory=dict)
    
    # Individual NPC reputation
    npc_reputation: Dict[str, int] = field(default_factory=dict)


@dataclass
class PlayerMorality:
    """Complete moral profile of the player"""
    # Core alignment
    current_alignment: MoralAlignment = MoralAlignment.TRUE_NEUTRAL
    alignment_stability: float = 1.0  # How resistant to change (0.0 to 2.0)
    
    # Alignment axes (each -100 to +100)
    good_evil_axis: int = 0      # +100 = pure good, -100 = pure evil
    lawful_chaotic_axis: int = 0  # +100 = lawful, -100 = chaotic
    
    # Karma score
    total_karma: int = 0  # Running total of all karma actions
    recent_karma: int = 0  # Karma from last 10 actions (more impactful)
    
    # Action history
    karma_history: List[KarmaEvent] = field(default_factory=list)
    alignment_history: List[AlignmentShift] = field(default_factory=list)
    
    # Reputation
    reputation: PlayerReputation = field(default_factory=PlayerReputation)
    
    # Moral tendencies (learned patterns)
    moral_tendencies: Dict[str, float] = field(default_factory=dict)
    
    # Special states
    corruption_level: int = 0     # 0-100, affects available evil choices
    redemption_points: int = 0    # Can be earned to overcome past evil
    infamy_level: int = 0         # How well-known your evil deeds are
    
    # Tracking
    total_kills: int = 0
    innocent_kills: int = 0
    lives_saved: int = 0
    promises_kept: int = 0
    promises_broken: int = 0


class AlignmentKarmaSystem:
    """Core system managing player morality and karma"""
    
    def __init__(self):
        self.player_morality: Dict[str, PlayerMorality] = {}
        
        # Karma value mappings
        self.karma_values = {
            # Good actions
            KarmaAction.SAVE_INNOCENT: 15,
            KarmaAction.HELP_POOR: 8,
            KarmaAction.SHOW_MERCY: 12,
            KarmaAction.KEEP_PROMISE: 5,
            KarmaAction.SELF_SACRIFICE: 25,
            KarmaAction.PROTECT_WEAK: 10,
            KarmaAction.HEAL_WOUNDED: 7,
            KarmaAction.DONATE_CHARITY: 6,
            
            # Evil actions
            KarmaAction.MURDER_INNOCENT: -25,
            KarmaAction.STEAL_FROM_POOR: -12,
            KarmaAction.TORTURE: -20,
            KarmaAction.BREAK_PROMISE: -8,
            KarmaAction.BETRAY_ALLY: -18,
            KarmaAction.EXTORT: -10,
            KarmaAction.DESECRATE: -15,
            KarmaAction.MASSACRE: -40,
            
            # Lawful actions
            KarmaAction.UPHOLD_LAW: 3,
            KarmaAction.FOLLOW_ORDERS: 2,
            KarmaAction.HONOR_CONTRACT: 5,
            KarmaAction.RESPECT_AUTHORITY: 2,
            KarmaAction.MAINTAIN_ORDER: 4,
            
            # Chaotic actions
            KarmaAction.BREAK_LAW: -3,
            KarmaAction.DEFY_AUTHORITY: -2,
            KarmaAction.ACT_IMPULSIVELY: -1,
            KarmaAction.CAUSE_CHAOS: -8,
            KarmaAction.REBEL: -5,
            
            # Neutral/indifferent actions
            KarmaAction.IGNORE_SUFFERING: -5,
            KarmaAction.SELFISH_CHOICE: -3,
            KarmaAction.PRAGMATIC_DECISION: 0,
            KarmaAction.AVOID_INVOLVEMENT: -2,
        }
        
        # Faction reputation modifiers for different action types
        self.faction_karma_modifiers = {
            "royal_crown": {
                "lawful_good": 2.0,
                "lawful_neutral": 1.5,
                "lawful_evil": 0.5,
                "chaotic_good": -0.5,
                "chaotic_evil": -2.0
            },
            "peoples_liberation": {
                "chaotic_good": 2.0,
                "neutral_good": 1.5,
                "chaotic_neutral": 1.0,
                "lawful_good": -0.5,
                "lawful_evil": -2.0
            },
            "shadow_covenant": {
                "chaotic_evil": 2.0,
                "neutral_evil": 1.5,
                "lawful_evil": 1.0,
                "chaotic_good": -2.0,
                "lawful_good": -2.0
            },
            "order_of_dawn": {
                "lawful_good": 2.0,
                "neutral_good": 1.5,
                "chaotic_good": 1.0,
                "neutral_evil": -1.5,
                "chaotic_evil": -2.0
            }
        }
    
    def get_player_morality(self, player_id: str) -> PlayerMorality:
        """Get or create player morality profile"""
        if player_id not in self.player_morality:
            self.player_morality[player_id] = PlayerMorality()
        return self.player_morality[player_id]
    
    def record_karma_action(
        self,
        player_id: str,
        action: KarmaAction,
        description: str,
        location: str = "unknown",
        witnesses: List[str] = None,
        magnitude_modifier: float = 1.0,
        context: Dict[str, Any] = None
    ) -> KarmaEvent:
        """Record a karma-affecting action"""
        
        morality = self.get_player_morality(player_id)
        witnesses = witnesses or []
        context = context or {}
        
        # Calculate base karma value
        base_karma = self.karma_values.get(action, 0)
        final_karma = int(base_karma * magnitude_modifier)
        
        # Create karma event
        event = KarmaEvent(
            action=action,
            magnitude=final_karma,
            description=description,
            location=location,
            witnesses=witnesses
        )
        
        # Calculate faction impacts
        self._calculate_faction_impacts(event, morality, context)
        
        # Calculate companion impacts
        self._calculate_companion_impacts(event, context)
        
        # Determine quest impacts
        self._determine_quest_impacts(event, morality)
        
        # Update player karma
        morality.total_karma += final_karma
        morality.karma_history.append(event)
        
        # Update recent karma (last 10 actions)
        if len(morality.karma_history) > 10:
            morality.recent_karma = sum(
                e.magnitude for e in morality.karma_history[-10:]
            )
        else:
            morality.recent_karma = morality.total_karma
        
        # Update alignment axes
        self._update_alignment_axes(morality, action, final_karma)
        
        # Check for alignment shift
        self._check_alignment_shift(morality, event)
        
        # Update reputation
        self._update_reputation(morality, event)
        
        # Update tracking stats
        self._update_tracking_stats(morality, action, context)
        
        return event
    
    def _calculate_faction_impacts(self, event: KarmaEvent, morality: PlayerMorality, context: Dict[str, Any]):
        """Calculate how this action affects faction relationships"""
        
        current_alignment = morality.current_alignment.value
        
        for faction, modifiers in self.faction_karma_modifiers.items():
            if current_alignment in modifiers:
                base_impact = event.magnitude * modifiers[current_alignment]
                
                # Special context modifiers
                if faction in context.get("involved_factions", []):
                    base_impact *= 1.5  # Direct involvement amplifies impact
                
                if faction in context.get("opposed_factions", []):
                    base_impact *= -1   # Opposing factions react negatively
                
                event.faction_impact[faction] = int(base_impact)
    
    def _calculate_companion_impacts(self, event: KarmaEvent, context: Dict[str, Any]):
        """Calculate how companions react to this action"""
        
        # Companion alignment preferences (would be loaded from companion system)
        companion_alignments = {
            "lyralei_ranger": MoralAlignment.CHAOTIC_GOOD,
            "thane_warrior": MoralAlignment.LAWFUL_GOOD,
            "zara_mage": MoralAlignment.NEUTRAL_GOOD,
            "kael_rogue": MoralAlignment.CHAOTIC_GOOD
        }
        
        for companion_id, comp_alignment in companion_alignments.items():
            # Calculate compatibility between action and companion alignment
            compatibility = self._calculate_alignment_compatibility(
                event.action, comp_alignment
            )
            
            impact = int(event.magnitude * compatibility)
            
            # Present companions have stronger reactions
            if companion_id in context.get("present_companions", []):
                impact *= 2
            
            if abs(impact) >= 3:  # Only record significant impacts
                event.companion_impact[companion_id] = impact
    
    def _calculate_alignment_compatibility(self, action: KarmaAction, alignment: MoralAlignment) -> float:
        """Calculate how compatible an action is with an alignment"""
        
        alignment_preferences = {
            MoralAlignment.LAWFUL_GOOD: {
                "good_actions": 1.0,
                "lawful_actions": 0.8,
                "evil_actions": -1.0,
                "chaotic_actions": -0.5
            },
            MoralAlignment.CHAOTIC_GOOD: {
                "good_actions": 1.0,
                "chaotic_actions": 0.6,
                "evil_actions": -1.0,
                "lawful_actions": -0.3
            },
            MoralAlignment.LAWFUL_EVIL: {
                "evil_actions": 1.0,
                "lawful_actions": 0.8,
                "good_actions": -0.8,
                "chaotic_actions": -0.6
            },
            MoralAlignment.CHAOTIC_EVIL: {
                "evil_actions": 1.0,
                "chaotic_actions": 0.8,
                "good_actions": -1.0,
                "lawful_actions": -0.8
            },
            MoralAlignment.TRUE_NEUTRAL: {
                "good_actions": 0.2,
                "evil_actions": -0.3,
                "lawful_actions": 0.1,
                "chaotic_actions": 0.1
            }
        }
        
        # Categorize action
        action_categories = []
        if action in [KarmaAction.SAVE_INNOCENT, KarmaAction.HELP_POOR, KarmaAction.SHOW_MERCY,
                      KarmaAction.SELF_SACRIFICE, KarmaAction.PROTECT_WEAK, KarmaAction.HEAL_WOUNDED]:
            action_categories.append("good_actions")
        
        if action in [KarmaAction.MURDER_INNOCENT, KarmaAction.TORTURE, KarmaAction.BETRAY_ALLY,
                      KarmaAction.MASSACRE, KarmaAction.DESECRATE]:
            action_categories.append("evil_actions")
        
        if action in [KarmaAction.UPHOLD_LAW, KarmaAction.FOLLOW_ORDERS, KarmaAction.HONOR_CONTRACT,
                      KarmaAction.RESPECT_AUTHORITY, KarmaAction.MAINTAIN_ORDER]:
            action_categories.append("lawful_actions")
        
        if action in [KarmaAction.BREAK_LAW, KarmaAction.DEFY_AUTHORITY, KarmaAction.CAUSE_CHAOS,
                      KarmaAction.REBEL, KarmaAction.ACT_IMPULSIVELY]:
            action_categories.append("chaotic_actions")
        
        # Calculate compatibility
        if alignment not in alignment_preferences:
            return 0.0
        
        preferences = alignment_preferences[alignment]
        total_compatibility = 0.0
        
        for category in action_categories:
            if category in preferences:
                total_compatibility += preferences[category]
        
        return total_compatibility / max(len(action_categories), 1)
    
    def _determine_quest_impacts(self, event: KarmaEvent, morality: PlayerMorality):
        """Determine what quests are unlocked/locked by this action"""
        
        # Evil actions unlock dark quests
        if event.magnitude <= -15:
            if morality.corruption_level >= 50:
                event.unlocks_quests.extend([
                    "dark_ritual_quest", "assassination_contract", "soul_trading"
                ])
            event.locks_quests.extend([
                "temple_blessing_quest", "holy_pilgrimage", "redemption_arc"
            ])
        
        # Good actions unlock heroic quests
        if event.magnitude >= 15:
            event.unlocks_quests.extend([
                "heroic_rescue_mission", "divine_blessing_quest", "champion_trial"
            ])
            if morality.lives_saved >= 10:
                event.unlocks_quests.append("legendary_hero_quest")
        
        # Chaotic actions
        if event.action in [KarmaAction.REBEL, KarmaAction.CAUSE_CHAOS, KarmaAction.DEFY_AUTHORITY]:
            event.unlocks_quests.extend([
                "underground_resistance", "chaos_magic_quest", "freedom_fighter"
            ])
            event.locks_quests.extend([
                "royal_service_quest", "law_enforcement", "order_champion"
            ])
        
        # Set story flags
        if event.action == KarmaAction.MURDER_INNOCENT and morality.innocent_kills >= 5:
            event.story_flags.append("notorious_killer")
        
        if event.action == KarmaAction.SAVE_INNOCENT and morality.lives_saved >= 20:
            event.story_flags.append("legendary_savior")
    
    def _update_alignment_axes(self, morality: PlayerMorality, action: KarmaAction, karma: int):
        """Update the good/evil and lawful/chaotic axes"""
        
        # Good/Evil axis
        if action in [KarmaAction.SAVE_INNOCENT, KarmaAction.HELP_POOR, KarmaAction.SHOW_MERCY,
                      KarmaAction.SELF_SACRIFICE, KarmaAction.PROTECT_WEAK]:
            morality.good_evil_axis = min(100, morality.good_evil_axis + abs(karma))
        elif action in [KarmaAction.MURDER_INNOCENT, KarmaAction.TORTURE, KarmaAction.BETRAY_ALLY,
                        KarmaAction.MASSACRE]:
            morality.good_evil_axis = max(-100, morality.good_evil_axis + karma)
        
        # Lawful/Chaotic axis
        if action in [KarmaAction.UPHOLD_LAW, KarmaAction.FOLLOW_ORDERS, KarmaAction.HONOR_CONTRACT,
                      KarmaAction.RESPECT_AUTHORITY]:
            morality.lawful_chaotic_axis = min(100, morality.lawful_chaotic_axis + 5)
        elif action in [KarmaAction.BREAK_LAW, KarmaAction.DEFY_AUTHORITY, KarmaAction.CAUSE_CHAOS,
                        KarmaAction.REBEL]:
            morality.lawful_chaotic_axis = max(-100, morality.lawful_chaotic_axis - 5)
        
        # Update corruption level for evil actions
        if karma <= -10:
            morality.corruption_level = min(100, morality.corruption_level + abs(karma) // 2)
        
        # Good actions can reduce corruption (redemption)
        if karma >= 15:
            morality.corruption_level = max(0, morality.corruption_level - karma // 3)
            morality.redemption_points += karma // 5
    
    def _check_alignment_shift(self, morality: PlayerMorality, event: KarmaEvent):
        """Check if player's alignment should shift based on recent actions"""
        
        old_alignment = morality.current_alignment
        
        # Determine new alignment based on axes
        new_alignment = self._calculate_alignment_from_axes(
            morality.good_evil_axis, 
            morality.lawful_chaotic_axis
        )
        
        # Check if shift should occur (considering stability)
        shift_threshold = 20 * morality.alignment_stability
        
        recent_actions = morality.karma_history[-5:]  # Last 5 actions
        total_recent_karma = sum(e.magnitude for e in recent_actions)
        
        if abs(total_recent_karma) >= shift_threshold and new_alignment != old_alignment:
            # Alignment shift occurs
            shift = AlignmentShift(
                old_alignment=old_alignment,
                new_alignment=new_alignment,
                trigger_event=event.description,
                shift_magnitude=abs(total_recent_karma) / shift_threshold
            )
            
            morality.current_alignment = new_alignment
            morality.alignment_history.append(shift)
            
            # Reduce stability after shift (more likely to shift again)
            morality.alignment_stability = max(0.5, morality.alignment_stability - 0.1)
        else:
            # No shift, increase stability
            morality.alignment_stability = min(2.0, morality.alignment_stability + 0.05)
    
    def _calculate_alignment_from_axes(self, good_evil: int, lawful_chaotic: int) -> MoralAlignment:
        """Calculate alignment from axis values"""
        
        # Determine good/neutral/evil
        if good_evil >= 30:
            moral_axis = "good"
        elif good_evil <= -30:
            moral_axis = "evil"
        else:
            moral_axis = "neutral"
        
        # Determine lawful/neutral/chaotic
        if lawful_chaotic >= 30:
            order_axis = "lawful"
        elif lawful_chaotic <= -30:
            order_axis = "chaotic"
        else:
            order_axis = "neutral"
        
        # Combine to get alignment
        if moral_axis == "neutral" and order_axis == "neutral":
            return MoralAlignment.TRUE_NEUTRAL
        elif moral_axis == "good" and order_axis == "neutral":
            return MoralAlignment.NEUTRAL_GOOD
        elif moral_axis == "evil" and order_axis == "neutral":
            return MoralAlignment.NEUTRAL_EVIL
        elif moral_axis == "neutral" and order_axis == "lawful":
            return MoralAlignment.LAWFUL_NEUTRAL
        elif moral_axis == "neutral" and order_axis == "chaotic":
            return MoralAlignment.CHAOTIC_NEUTRAL
        else:
            alignment_name = f"{order_axis}_{moral_axis}"
            return MoralAlignment(alignment_name)
    
    def _update_reputation(self, morality: PlayerMorality, event: KarmaEvent):
        """Update reputation with various groups"""
        
        rep = morality.reputation
        
        # Update general reputation categories
        if event.action in [KarmaAction.UPHOLD_LAW, KarmaAction.RESPECT_AUTHORITY, KarmaAction.MAINTAIN_ORDER]:
            rep.lawful_authorities += abs(event.magnitude) // 2
        elif event.action in [KarmaAction.BREAK_LAW, KarmaAction.DEFY_AUTHORITY, KarmaAction.CAUSE_CHAOS]:
            rep.lawful_authorities -= abs(event.magnitude) // 2
            rep.criminal_underworld += abs(event.magnitude) // 3
        
        if event.action in [KarmaAction.HELP_POOR, KarmaAction.DONATE_CHARITY, KarmaAction.PROTECT_WEAK]:
            rep.common_folk += abs(event.magnitude)
        elif event.action in [KarmaAction.STEAL_FROM_POOR, KarmaAction.EXTORT]:
            rep.common_folk -= abs(event.magnitude) * 2
        
        if event.action in [KarmaAction.HEAL_WOUNDED, KarmaAction.SHOW_MERCY]:
            rep.religious_orders += abs(event.magnitude)
        elif event.action in [KarmaAction.DESECRATE, KarmaAction.TORTURE]:
            rep.religious_orders -= abs(event.magnitude) * 2
        
        # Criminal underworld likes evil acts
        if event.magnitude <= -10:
            rep.criminal_underworld += abs(event.magnitude) // 2
        
        # Update faction reputation
        for faction, impact in event.faction_impact.items():
            if faction not in rep.faction_reputation:
                rep.faction_reputation[faction] = 0
            rep.faction_reputation[faction] += impact
        
        # Cap reputation values
        for attr in ['lawful_authorities', 'common_folk', 'criminal_underworld', 
                     'religious_orders', 'magical_community']:
            current_val = getattr(rep, attr)
            setattr(rep, attr, max(-100, min(100, current_val)))
        
        for faction in rep.faction_reputation:
            rep.faction_reputation[faction] = max(-100, min(100, rep.faction_reputation[faction]))
    
    def _update_tracking_stats(self, morality: PlayerMorality, action: KarmaAction, context: Dict[str, Any]):
        """Update various tracking statistics"""
        
        if action == KarmaAction.MURDER_INNOCENT:
            morality.total_kills += 1
            morality.innocent_kills += 1
            
            # Increase infamy for public murders
            if len(context.get("witnesses", [])) > 0:
                morality.infamy_level += 10
        
        if action in [KarmaAction.SAVE_INNOCENT, KarmaAction.PROTECT_WEAK]:
            morality.lives_saved += 1
        
        if action == KarmaAction.KEEP_PROMISE:
            morality.promises_kept += 1
        elif action == KarmaAction.BREAK_PROMISE:
            morality.promises_broken += 1
    
    def get_reputation_level(self, reputation_value: int) -> ReputationLevel:
        """Convert reputation number to level"""
        if reputation_value >= 80:
            return ReputationLevel.REVERED
        elif reputation_value >= 60:
            return ReputationLevel.RESPECTED
        elif reputation_value >= 40:
            return ReputationLevel.LIKED
        elif reputation_value >= 20:
            return ReputationLevel.TRUSTED
        elif reputation_value >= -19:
            return ReputationLevel.NEUTRAL
        elif reputation_value >= -39:
            return ReputationLevel.DISLIKED
        elif reputation_value >= -59:
            return ReputationLevel.MISTRUSTED
        elif reputation_value >= -79:
            return ReputationLevel.DESPISED
        else:
            return ReputationLevel.HATED
    
    def get_available_choices_for_alignment(self, player_id: str, base_choices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter and add choices based on player alignment and corruption"""
        
        morality = self.get_player_morality(player_id)
        available_choices = base_choices.copy()
        
        # Add evil choices for corrupted characters
        if morality.corruption_level >= 25:
            evil_choices = [
                {
                    "id": "intimidate_threaten",
                    "text": "Threaten them with violence",
                    "karma_action": KarmaAction.EXTORT,
                    "alignment_requirement": ["evil"]
                },
                {
                    "id": "manipulate_deceive",
                    "text": "Lie and manipulate them",
                    "karma_action": KarmaAction.BREAK_PROMISE,
                    "alignment_requirement": ["evil", "chaotic_neutral"]
                }
            ]
            available_choices.extend(evil_choices)
        
        if morality.corruption_level >= 50:
            dark_choices = [
                {
                    "id": "torture_information",
                    "text": "Torture them for information",
                    "karma_action": KarmaAction.TORTURE,
                    "alignment_requirement": ["evil"]
                },
                {
                    "id": "kill_witnesses",
                    "text": "Kill them to silence them",
                    "karma_action": KarmaAction.MURDER_INNOCENT,
                    "alignment_requirement": ["chaotic_evil", "neutral_evil"]
                }
            ]
            available_choices.extend(dark_choices)
        
        # Add lawful choices for lawful characters
        if "lawful" in morality.current_alignment.value:
            lawful_choices = [
                {
                    "id": "follow_protocol",
                    "text": "Follow proper legal procedures",
                    "karma_action": KarmaAction.UPHOLD_LAW,
                    "alignment_requirement": ["lawful"]
                }
            ]
            available_choices.extend(lawful_choices)
        
        # Add chaotic choices for chaotic characters
        if "chaotic" in morality.current_alignment.value:
            chaotic_choices = [
                {
                    "id": "break_rules",
                    "text": "Ignore the rules and do what feels right",
                    "karma_action": KarmaAction.BREAK_LAW,
                    "alignment_requirement": ["chaotic"]
                }
            ]
            available_choices.extend(chaotic_choices)
        
        # Filter choices that don't match alignment
        filtered_choices = []
        for choice in available_choices:
            if "alignment_requirement" in choice:
                requirements = choice["alignment_requirement"]
                current_alignment = morality.current_alignment.value
                
                # Check if current alignment matches any requirement
                matches = False
                for req in requirements:
                    if req in current_alignment or req == "evil" and "evil" in current_alignment:
                        matches = True
                        break
                
                if matches:
                    filtered_choices.append(choice)
            else:
                # No alignment requirement, always available
                filtered_choices.append(choice)
        
        return filtered_choices
    
    def get_npc_reaction_modifier(self, player_id: str, npc_type: str, npc_alignment: str = "neutral") -> float:
        """Get NPC reaction modifier based on player reputation and alignment"""
        
        morality = self.get_player_morality(player_id)
        rep = morality.reputation
        
        # Base modifier from general reputation
        modifier = 0.0
        
        if npc_type == "guard" or npc_type == "official":
            modifier = rep.lawful_authorities / 100.0
        elif npc_type == "commoner" or npc_type == "merchant":
            modifier = rep.common_folk / 100.0
        elif npc_type == "criminal" or npc_type == "thief":
            modifier = rep.criminal_underworld / 100.0
        elif npc_type == "priest" or npc_type == "paladin":
            modifier = rep.religious_orders / 100.0
        elif npc_type == "mage" or npc_type == "scholar":
            modifier = rep.magical_community / 100.0
        
        # Alignment compatibility modifier
        player_alignment = morality.current_alignment.value
        if npc_alignment in player_alignment:
            modifier += 0.2  # Same alignment = slight bonus
        elif ("good" in player_alignment and "evil" in npc_alignment) or \
             ("evil" in player_alignment and "good" in npc_alignment):
            modifier -= 0.3  # Opposing alignments = penalty
        
        # Infamy penalty (everyone recognizes notorious villains)
        if morality.infamy_level >= 50:
            modifier -= 0.4
        elif morality.infamy_level >= 25:
            modifier -= 0.2
        
        return max(-1.0, min(1.0, modifier))
    
    def can_start_quest(self, player_id: str, quest_id: str, quest_requirements: Dict[str, Any]) -> bool:
        """Check if player can start a quest based on moral requirements"""
        
        morality = self.get_player_morality(player_id)
        
        # Check alignment requirements
        if "required_alignment" in quest_requirements:
            required = quest_requirements["required_alignment"]
            current = morality.current_alignment.value
            
            if isinstance(required, list):
                if not any(req in current for req in required):
                    return False
            else:
                if required not in current:
                    return False
        
        # Check karma requirements
        if "min_karma" in quest_requirements:
            if morality.total_karma < quest_requirements["min_karma"]:
                return False
        
        if "max_karma" in quest_requirements:
            if morality.total_karma > quest_requirements["max_karma"]:
                return False
        
        # Check corruption requirements
        if "min_corruption" in quest_requirements:
            if morality.corruption_level < quest_requirements["min_corruption"]:
                return False
        
        if "max_corruption" in quest_requirements:
            if morality.corruption_level > quest_requirements["max_corruption"]:
                return False
        
        # Check reputation requirements
        if "reputation_requirements" in quest_requirements:
            for group, min_rep in quest_requirements["reputation_requirements"].items():
                current_rep = getattr(morality.reputation, group, 0)
                if current_rep < min_rep:
                    return False
        
        # Check story flags
        if "required_flags" in quest_requirements:
            player_flags = set()
            for event in morality.karma_history:
                player_flags.update(event.story_flags)
            
            required_flags = set(quest_requirements["required_flags"])
            if not required_flags.issubset(player_flags):
                return False
        
        if "forbidden_flags" in quest_requirements:
            player_flags = set()
            for event in morality.karma_history:
                player_flags.update(event.story_flags)
            
            forbidden_flags = set(quest_requirements["forbidden_flags"])
            if forbidden_flags.intersection(player_flags):
                return False
        
        return True
    
    def get_morality_summary(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of player's moral state"""
        
        morality = self.get_player_morality(player_id)
        rep = morality.reputation
        
        # Calculate reputation levels
        reputation_levels = {
            "lawful_authorities": self.get_reputation_level(rep.lawful_authorities),
            "common_folk": self.get_reputation_level(rep.common_folk),
            "criminal_underworld": self.get_reputation_level(rep.criminal_underworld),
            "religious_orders": self.get_reputation_level(rep.religious_orders),
            "magical_community": self.get_reputation_level(rep.magical_community)
        }
        
        # Recent actions summary
        recent_actions = morality.karma_history[-5:]
        
        # Story flags
        story_flags = set()
        for event in morality.karma_history:
            story_flags.update(event.story_flags)
        
        return {
            "alignment": morality.current_alignment.value,
            "alignment_stability": morality.alignment_stability,
            "good_evil_axis": morality.good_evil_axis,
            "lawful_chaotic_axis": morality.lawful_chaotic_axis,
            "total_karma": morality.total_karma,
            "recent_karma": morality.recent_karma,
            "corruption_level": morality.corruption_level,
            "redemption_points": morality.redemption_points,
            "infamy_level": morality.infamy_level,
            "reputation_levels": {k: v.value for k, v in reputation_levels.items()},
            "faction_reputation": rep.faction_reputation,
            "stats": {
                "total_kills": morality.total_kills,
                "innocent_kills": morality.innocent_kills,
                "lives_saved": morality.lives_saved,
                "promises_kept": morality.promises_kept,
                "promises_broken": morality.promises_broken
            },
            "recent_actions": [
                {
                    "action": action.action.value,
                    "description": action.description,
                    "karma": action.magnitude,
                    "location": action.location
                }
                for action in recent_actions
            ],
            "story_flags": list(story_flags),
            "moral_title": self._get_moral_title(morality),
            "available_evil_options": morality.corruption_level >= 25,
            "available_dark_options": morality.corruption_level >= 50
        }
    
    def _get_moral_title(self, morality: PlayerMorality) -> str:
        """Get a descriptive title based on player's moral state"""
        
        alignment = morality.current_alignment.value
        karma = morality.total_karma
        corruption = morality.corruption_level
        infamy = morality.infamy_level
        
        # Special titles for extreme cases
        if morality.innocent_kills >= 10 and infamy >= 75:
            return "The Notorious Killer"
        elif morality.lives_saved >= 20 and karma >= 200:
            return "The Legendary Hero"
        elif corruption >= 90:
            return "The Utterly Corrupted"
        elif morality.redemption_points >= 50 and corruption <= 10:
            return "The Redeemed"
        
        # Alignment-based titles
        title_map = {
            "lawful_good": "The Righteous" if karma > 100 else "The Just",
            "neutral_good": "The Kind-Hearted" if karma > 100 else "The Good-Natured",
            "chaotic_good": "The Free Spirit" if karma > 100 else "The Wild Heart",
            "lawful_neutral": "The Lawkeeper" if rep.lawful_authorities > 50 else "The Dutiful",
            "true_neutral": "The Balanced" if abs(karma) < 50 else "The Indifferent",
            "chaotic_neutral": "The Unpredictable" if infamy > 25 else "The Free Agent",
            "lawful_evil": "The Tyrant" if corruption > 60 else "The Ruthless",
            "neutral_evil": "The Selfish" if corruption > 60 else "The Callous",
            "chaotic_evil": "The Destroyer" if corruption > 60 else "The Cruel"
        }
        
        return title_map.get(alignment, "The Wanderer")