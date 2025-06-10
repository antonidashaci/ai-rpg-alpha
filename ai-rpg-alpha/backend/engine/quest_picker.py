"""
AI-RPG-Alpha: Quest Picker Engine (Refactored)

This module handles quest selection and filtering based on player state,
location, tags, and risk preferences. Refactored to use utility modules
and maintain the 500-line limit as specified in the PRD.
"""

from typing import List, Dict, Any, Optional
import random

from models.dataclasses import Quest, Player, RiskLevel, QuestStatus
from dao.game_state import GameStateDAO
from .quest_selection_criteria import QuestSelectionCriteria, QuestScoringUtils

class QuestPicker:
    """
    Handles intelligent quest selection and filtering.
    
    Selects appropriate quests based on player level, location, preferences,
    and story progression. Uses utility functions for scoring and evaluation.
    """
    
    def __init__(self, game_dao: GameStateDAO):
        """Initialize the quest picker with game data access."""
        self.game_dao = game_dao
        self.scoring_utils = QuestScoringUtils()
        
        # Quest difficulty mappings
        self.level_difficulty_map = {
            1: ["easy"], 2: ["easy", "medium"], 3: ["easy", "medium"],
            4: ["medium"], 5: ["medium", "hard"], 6: ["medium", "hard"],
            7: ["hard"], 8: ["hard", "epic"], 9: ["hard", "epic"], 10: ["epic"]
        }
        
        # Risk level preferences
        self.risk_preferences = {
            "combat_focused": [RiskLevel.COMBAT, RiskLevel.MYSTERY],
            "exploration_focused": [RiskLevel.MYSTERY, RiskLevel.CALM],
            "social_focused": [RiskLevel.CALM, RiskLevel.MYSTERY],
            "balanced": [RiskLevel.CALM, RiskLevel.MYSTERY, RiskLevel.COMBAT]
        }
    
    def select_quest_for_player(
        self, player: Player, preferred_tags: List[str] = None,
        max_risk: RiskLevel = RiskLevel.COMBAT, exclude_completed: bool = True
    ) -> Optional[Quest]:
        """Select the most appropriate quest for a player."""
        available_quests = self._get_available_quests(player, exclude_completed)
        if not available_quests:
            return None
        
        # Apply filters
        filtered_quests = self._apply_filters(available_quests, player, preferred_tags, max_risk)
        if not filtered_quests:
            filtered_quests = self._apply_relaxed_filters(available_quests, player, max_risk)
        
        if not filtered_quests:
            return None
        
        # Score and select
        scored_quests = self._score_quests(filtered_quests, player, preferred_tags)
        return self._select_from_scored_quests(scored_quests)
    
    def get_quests_by_location(self, location: str, player: Player, limit: int = 5) -> List[Quest]:
        """Get quests available at a specific location."""
        location_quests = self.game_dao.get_quests_by_location(location)
        suitable_quests = [
            quest for quest in location_quests 
            if self.scoring_utils.is_quest_suitable_for_player(quest, player)
        ]
        
        scored_quests = self._score_quests(suitable_quests, player)
        sorted_quests = sorted(scored_quests, key=lambda x: x[1], reverse=True)
        return [quest for quest, score in sorted_quests[:limit]]
    
    def filter_quests_by_tags(
        self, quests: List[Quest], required_tags: List[str] = None,
        excluded_tags: List[str] = None
    ) -> List[Quest]:
        """Filter quests by tag requirements."""
        filtered = []
        for quest in quests:
            if required_tags and not any(tag in quest.tags for tag in required_tags):
                continue
            if excluded_tags and any(tag in quest.tags for tag in excluded_tags):
                continue
            filtered.append(quest)
        return filtered
    
    def filter_quests_by_risk(
        self, quests: List[Quest], max_risk: RiskLevel, min_risk: RiskLevel = RiskLevel.CALM
    ) -> List[Quest]:
        """Filter quests by risk level range."""
        risk_order = [RiskLevel.CALM, RiskLevel.MYSTERY, RiskLevel.COMBAT]
        max_index = risk_order.index(max_risk)
        min_index = risk_order.index(min_risk)
        
        return [
            quest for quest in quests 
            if min_index <= risk_order.index(quest.risk) <= max_index
        ]
    
    def get_quest_recommendations(self, player: Player, count: int = 3) -> List[Dict[str, Any]]:
        """Get personalized quest recommendations for a player."""
        available_quests = self._get_available_quests(player)
        if not available_quests:
            return []
        
        scored_quests = self._score_quests(available_quests, player)
        sorted_quests = sorted(scored_quests, key=lambda x: x[1], reverse=True)[:count]
        
        return [
            {
                "quest": quest,
                "score": score,
                "reasoning": self.scoring_utils.generate_recommendation_reasoning(quest, player),
                "difficulty": self.scoring_utils.assess_quest_difficulty(quest, player),
                "estimated_duration": self.scoring_utils.estimate_quest_duration(quest),
                "risk_warning": self._generate_risk_warning(quest, player)
            }
            for quest, score in sorted_quests
        ]
    
    def _get_available_quests(self, player: Player, exclude_completed: bool = True) -> List[Quest]:
        """Get all quests available to the player."""
        all_quests = self.game_dao.get_all_quests()
        available = []
        
        for quest in all_quests:
            if exclude_completed and quest.id in player.completed_quests:
                continue
            if quest.id in player.active_quests:
                continue
            if self.scoring_utils.is_quest_suitable_for_player(quest, player):
                available.append(quest)
        
        return available
    
    def _apply_filters(
        self, quests: List[Quest], player: Player,
        preferred_tags: List[str] = None, max_risk: RiskLevel = RiskLevel.COMBAT
    ) -> List[Quest]:
        """Apply strict filtering criteria."""
        filtered = self.filter_quests_by_risk(quests, max_risk)
        
        if preferred_tags:
            filtered = self.filter_quests_by_tags(filtered, required_tags=preferred_tags)
        
        filtered = [q for q in filtered if self._is_location_accessible(q.location, player)]
        return filtered
    
    def _apply_relaxed_filters(
        self, quests: List[Quest], player: Player, max_risk: RiskLevel
    ) -> List[Quest]:
        """Apply relaxed filtering when strict filtering yields no results."""
        filtered = self.filter_quests_by_risk(quests, max_risk)
        return [q for q in filtered if not self.scoring_utils.is_quest_too_difficult(q, player)]
    
    def _score_quests(
        self, quests: List[Quest], player: Player, preferred_tags: List[str] = None
    ) -> List[tuple]:
        """Score quests based on suitability for player."""
        scored = []
        
        for quest in quests:
            score = (
                self.scoring_utils.calculate_level_score(quest, player) * 2.0 +
                self.scoring_utils.calculate_location_score(quest, player) * 1.5 +
                self.scoring_utils.calculate_risk_score(quest, player) * 1.2 +
                self.scoring_utils.calculate_story_score(quest, player) * 1.8 +
                self.scoring_utils.calculate_variety_bonus(quest, player) * 1.0
            )
            
            if preferred_tags:
                score += self.scoring_utils.calculate_tag_score(quest, preferred_tags) * 1.3
            
            scored.append((quest, score))
        
        return scored
    
    def _select_from_scored_quests(self, scored_quests: List[tuple]) -> Optional[Quest]:
        """Select quest from scored list with weighted randomness."""
        if not scored_quests:
            return None
        
        scored_quests.sort(key=lambda x: x[1], reverse=True)
        total_score = sum(max(score, 0.1) for _, score in scored_quests)
        
        if total_score <= 0:
            return random.choice(scored_quests)[0]
        
        # Weighted random selection
        rand_value = random.uniform(0, total_score)
        current_sum = 0
        
        for quest, score in scored_quests:
            current_sum += max(score, 0.1)
            if current_sum >= rand_value:
                return quest
        
        return scored_quests[0][0]  # Fallback to highest scored
    
    def _is_location_accessible(self, location: str, player: Player) -> bool:
        """Check if location is accessible to player."""
        # Simplified accessibility check
        return True
    
    def _generate_risk_warning(self, quest: Quest, player: Player) -> Optional[str]:
        """Generate warning message for high-risk quests."""
        if self.scoring_utils.is_quest_too_difficult(quest, player):
            return "Warning: This quest may be too challenging for your current level."
        
        if quest.risk == RiskLevel.COMBAT and player.health < 75:
            return "Warning: Combat quest - ensure you're well-prepared."
        
        return None 