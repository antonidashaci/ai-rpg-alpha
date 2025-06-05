"""
AI-RPG-Alpha: Quest Picker Engine

This module handles quest selection and filtering based on player state,
location, tags, and risk preferences. It ensures appropriate quest
difficulty and content matching for the current game context.
"""

from typing import List, Dict, Any, Optional
import random
from enum import Enum

from models.dataclasses import Quest, Player, RiskLevel, QuestStatus
from dao.game_state import GameStateDAO

class QuestSelectionCriteria(Enum):
    """Criteria for quest selection"""
    LEVEL_APPROPRIATE = "level_appropriate"
    LOCATION_BASED = "location_based"
    TAG_MATCHING = "tag_matching"
    RISK_SUITABLE = "risk_suitable"
    STORY_PROGRESSION = "story_progression"

class QuestPicker:
    """
    Handles intelligent quest selection and filtering.
    
    Selects appropriate quests based on player level, location, preferences,
    and story progression. Ensures balanced difficulty and engaging content.
    """
    
    def __init__(self, game_dao: GameStateDAO):
        """
        Initialize the quest picker with game data access.
        
        Args:
            game_dao: Game state data access object
        """
        self.game_dao = game_dao
        
        # Quest difficulty mappings
        self.level_difficulty_map = {
            1: ["easy"],
            2: ["easy", "medium"],
            3: ["easy", "medium"],
            4: ["medium"],
            5: ["medium", "hard"],
            6: ["medium", "hard"],
            7: ["hard"],
            8: ["hard", "epic"],
            9: ["hard", "epic"],
            10: ["epic"]
        }
        
        # Risk level preferences based on player stats
        self.risk_preferences = {
            "combat_focused": [RiskLevel.COMBAT, RiskLevel.MYSTERY],
            "exploration_focused": [RiskLevel.MYSTERY, RiskLevel.CALM],
            "social_focused": [RiskLevel.CALM, RiskLevel.MYSTERY],
            "balanced": [RiskLevel.CALM, RiskLevel.MYSTERY, RiskLevel.COMBAT]
        }
    
    def select_quest_for_player(
        self, 
        player: Player, 
        preferred_tags: List[str] = None,
        max_risk: RiskLevel = RiskLevel.COMBAT,
        exclude_completed: bool = True
    ) -> Optional[Quest]:
        """
        Select the most appropriate quest for a player.
        
        Args:
            player: Player object
            preferred_tags: List of preferred quest tags
            max_risk: Maximum acceptable risk level
            exclude_completed: Whether to exclude completed quests
            
        Returns:
            Selected Quest object or None if no suitable quest found
        """
        # Get all available quests
        available_quests = self._get_available_quests(player, exclude_completed)
        
        if not available_quests:
            return None
        
        # Apply filters
        filtered_quests = self._apply_filters(
            available_quests, 
            player, 
            preferred_tags, 
            max_risk
        )
        
        if not filtered_quests:
            # If no quests match strict criteria, relax some constraints
            filtered_quests = self._apply_relaxed_filters(
                available_quests, 
                player, 
                max_risk
            )
        
        if not filtered_quests:
            return None
        
        # Score and rank quests
        scored_quests = self._score_quests(filtered_quests, player, preferred_tags)
        
        # Select best quest (with some randomness for variety)
        return self._select_from_scored_quests(scored_quests)
    
    def get_quests_by_location(
        self, 
        location: str, 
        player: Player,
        limit: int = 5
    ) -> List[Quest]:
        """
        Get quests available at a specific location.
        
        Args:
            location: Location identifier
            player: Player object
            limit: Maximum number of quests to return
            
        Returns:
            List of Quest objects
        """
        location_quests = self.game_dao.get_quests_by_location(location)
        
        # Filter by player level and status
        suitable_quests = []
        for quest in location_quests:
            if self._is_quest_suitable_for_player(quest, player):
                suitable_quests.append(quest)
        
        # Sort by appropriateness score
        scored_quests = self._score_quests(suitable_quests, player)
        sorted_quests = sorted(scored_quests, key=lambda x: x[1], reverse=True)
        
        return [quest for quest, score in sorted_quests[:limit]]
    
    def filter_quests_by_tags(
        self, 
        quests: List[Quest], 
        required_tags: List[str] = None,
        excluded_tags: List[str] = None
    ) -> List[Quest]:
        """
        Filter quests by tag requirements.
        
        Args:
            quests: List of quests to filter
            required_tags: Tags that must be present
            excluded_tags: Tags that must not be present
            
        Returns:
            Filtered list of quests
        """
        filtered = []
        
        for quest in quests:
            # Check required tags
            if required_tags:
                if not any(tag in quest.tags for tag in required_tags):
                    continue
            
            # Check excluded tags
            if excluded_tags:
                if any(tag in quest.tags for tag in excluded_tags):
                    continue
            
            filtered.append(quest)
        
        return filtered
    
    def filter_quests_by_risk(
        self, 
        quests: List[Quest], 
        max_risk: RiskLevel,
        min_risk: RiskLevel = RiskLevel.CALM
    ) -> List[Quest]:
        """
        Filter quests by risk level range.
        
        Args:
            quests: List of quests to filter
            max_risk: Maximum acceptable risk level
            min_risk: Minimum acceptable risk level
            
        Returns:
            Filtered list of quests
        """
        risk_order = [RiskLevel.CALM, RiskLevel.MYSTERY, RiskLevel.COMBAT]
        max_index = risk_order.index(max_risk)
        min_index = risk_order.index(min_risk)
        
        return [
            quest for quest in quests 
            if min_index <= risk_order.index(quest.risk) <= max_index
        ]
    
    def get_quest_recommendations(
        self, 
        player: Player, 
        count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get quest recommendations with reasoning.
        
        Args:
            player: Player object
            count: Number of recommendations to return
            
        Returns:
            List of quest recommendation dictionaries
        """
        available_quests = self._get_available_quests(player)
        
        if not available_quests:
            return []
        
        # Score all quests
        scored_quests = self._score_quests(available_quests, player)
        
        # Sort by score and take top recommendations
        sorted_quests = sorted(scored_quests, key=lambda x: x[1], reverse=True)
        top_quests = sorted_quests[:count]
        
        recommendations = []
        for quest, score in top_quests:
            recommendation = {
                "quest": quest,
                "score": score,
                "reasoning": self._generate_recommendation_reasoning(quest, player),
                "difficulty_assessment": self._assess_quest_difficulty(quest, player),
                "estimated_duration": self._estimate_quest_duration(quest),
                "risk_warning": self._generate_risk_warning(quest, player)
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_available_quests(
        self, 
        player: Player, 
        exclude_completed: bool = True
    ) -> List[Quest]:
        """Get all quests available to the player"""
        all_quests = self.game_dao.get_all_quests()
        
        available = []
        for quest in all_quests:
            # Skip if already active
            if quest.id in player.active_quests:
                continue
            
            # Skip if completed and exclusion is enabled
            if exclude_completed and quest.id in player.completed_quests:
                continue
            
            # Skip if quest status is not available
            if quest.status != QuestStatus.AVAILABLE:
                continue
            
            available.append(quest)
        
        return available
    
    def _apply_filters(
        self, 
        quests: List[Quest], 
        player: Player,
        preferred_tags: List[str] = None,
        max_risk: RiskLevel = RiskLevel.COMBAT
    ) -> List[Quest]:
        """Apply strict filtering criteria"""
        filtered = []
        
        for quest in quests:
            # Level appropriateness
            if not self._is_level_appropriate(quest, player):
                continue
            
            # Risk level check
            if self._get_risk_level_value(quest.risk) > self._get_risk_level_value(max_risk):
                continue
            
            # Location accessibility (basic check)
            if not self._is_location_accessible(quest.location, player):
                continue
            
            filtered.append(quest)
        
        # Apply tag preferences if specified
        if preferred_tags:
            tag_filtered = self.filter_quests_by_tags(filtered, required_tags=preferred_tags)
            if tag_filtered:  # Only use tag filtering if it doesn't eliminate all quests
                filtered = tag_filtered
        
        return filtered
    
    def _apply_relaxed_filters(
        self, 
        quests: List[Quest], 
        player: Player,
        max_risk: RiskLevel
    ) -> List[Quest]:
        """Apply relaxed filtering when strict filtering yields no results"""
        filtered = []
        
        for quest in quests:
            # Only apply essential filters
            if self._get_risk_level_value(quest.risk) > self._get_risk_level_value(max_risk):
                continue
            
            # Allow slightly higher level quests
            if self._is_quest_too_difficult(quest, player):
                continue
            
            filtered.append(quest)
        
        return filtered
    
    def _score_quests(
        self, 
        quests: List[Quest], 
        player: Player,
        preferred_tags: List[str] = None
    ) -> List[tuple]:
        """Score quests based on suitability for player"""
        scored = []
        
        for quest in quests:
            score = 0
            
            # Level appropriateness score
            score += self._calculate_level_score(quest, player)
            
            # Location score
            score += self._calculate_location_score(quest, player)
            
            # Tag preference score
            if preferred_tags:
                score += self._calculate_tag_score(quest, preferred_tags)
            
            # Risk appropriateness score
            score += self._calculate_risk_score(quest, player)
            
            # Story progression score
            score += self._calculate_story_score(quest, player)
            
            # Variety bonus (avoid repetitive quest types)
            score += self._calculate_variety_bonus(quest, player)
            
            scored.append((quest, score))
        
        return scored
    
    def _select_from_scored_quests(self, scored_quests: List[tuple]) -> Optional[Quest]:
        """Select quest from scored list with weighted randomness"""
        if not scored_quests:
            return None
        
        # Sort by score
        scored_quests.sort(key=lambda x: x[1], reverse=True)
        
        # Use weighted selection favoring higher scores
        total_score = sum(score for _, score in scored_quests)
        
        if total_score <= 0:
            return random.choice(scored_quests)[0]
        
        # Weighted random selection
        rand_value = random.uniform(0, total_score)
        current_sum = 0
        
        for quest, score in scored_quests:
            current_sum += max(score, 0.1)  # Ensure minimum weight
            if current_sum >= rand_value:
                return quest
        
        return scored_quests[0][0]  # Fallback to highest scored
    
    def _is_quest_suitable_for_player(self, quest: Quest, player: Player) -> bool:
        """Check if quest is generally suitable for player"""
        return (
            self._is_level_appropriate(quest, player) and
            not self._is_quest_too_difficult(quest, player) and
            quest.status == QuestStatus.AVAILABLE
        )
    
    def _is_level_appropriate(self, quest: Quest, player: Player) -> bool:
        """Check if quest level is appropriate for player"""
        # This is a simplified check - in a full implementation,
        # quests would have explicit level requirements
        risk_level_requirements = {
            RiskLevel.CALM: 1,
            RiskLevel.MYSTERY: 2,
            RiskLevel.COMBAT: 3
        }
        
        min_level = risk_level_requirements.get(quest.risk, 1)
        return player.stats.level >= min_level
    
    def _is_quest_too_difficult(self, quest: Quest, player: Player) -> bool:
        """Check if quest is too difficult for player"""
        # Simple difficulty check based on risk and player stats
        if quest.risk == RiskLevel.COMBAT and player.stats.health < 50:
            return True
        
        if quest.risk == RiskLevel.MYSTERY and player.stats.intelligence < 8:
            return True
        
        return False
    
    def _is_location_accessible(self, location: str, player: Player) -> bool:
        """Check if location is accessible to player"""
        # Simplified accessibility check
        # In a full implementation, this would check travel requirements,
        # prerequisites, etc.
        return True
    
    def _get_risk_level_value(self, risk: RiskLevel) -> int:
        """Convert risk level to numeric value for comparison"""
        risk_values = {
            RiskLevel.CALM: 1,
            RiskLevel.MYSTERY: 2,
            RiskLevel.COMBAT: 3
        }
        return risk_values.get(risk, 1)
    
    def _calculate_level_score(self, quest: Quest, player: Player) -> float:
        """Calculate score based on level appropriateness"""
        if self._is_level_appropriate(quest, player):
            return 10.0
        return 0.0
    
    def _calculate_location_score(self, quest: Quest, player: Player) -> float:
        """Calculate score based on location relevance"""
        if quest.location == player.current_location:
            return 15.0  # Bonus for current location
        return 5.0
    
    def _calculate_tag_score(self, quest: Quest, preferred_tags: List[str]) -> float:
        """Calculate score based on tag preferences"""
        matching_tags = set(quest.tags) & set(preferred_tags)
        return len(matching_tags) * 5.0
    
    def _calculate_risk_score(self, quest: Quest, player: Player) -> float:
        """Calculate score based on risk appropriateness"""
        # Prefer moderate risk that matches player capabilities
        player_power = (player.stats.level + player.stats.strength + player.stats.intelligence) / 3
        
        if quest.risk == RiskLevel.CALM and player_power < 5:
            return 8.0
        elif quest.risk == RiskLevel.MYSTERY and 5 <= player_power < 10:
            return 8.0
        elif quest.risk == RiskLevel.COMBAT and player_power >= 10:
            return 8.0
        
        return 3.0
    
    def _calculate_story_score(self, quest: Quest, player: Player) -> float:
        """Calculate score based on story progression"""
        # Bonus for quests that advance main storyline
        if "main_story" in quest.tags:
            return 12.0
        elif "side_story" in quest.tags:
            return 6.0
        return 3.0
    
    def _calculate_variety_bonus(self, quest: Quest, player: Player) -> float:
        """Calculate bonus for quest variety"""
        # Simple variety check - avoid repeating recent quest types
        recent_events = self.game_dao.get_player_events(player.id, limit=5)
        recent_quest_types = [
            event.data.get("quest_type", "") 
            for event in recent_events 
            if event.event_type == "quest_complete"
        ]
        
        quest_type = quest.tags[0] if quest.tags else "unknown"
        if quest_type not in recent_quest_types:
            return 5.0
        
        return 0.0
    
    def _generate_recommendation_reasoning(self, quest: Quest, player: Player) -> str:
        """Generate human-readable reasoning for quest recommendation"""
        reasons = []
        
        if quest.location == player.current_location:
            reasons.append("available at your current location")
        
        if self._is_level_appropriate(quest, player):
            reasons.append("appropriate for your level")
        
        if quest.risk == RiskLevel.CALM:
            reasons.append("low risk")
        elif quest.risk == RiskLevel.MYSTERY:
            reasons.append("moderate challenge")
        elif quest.risk == RiskLevel.COMBAT:
            reasons.append("high adventure")
        
        if "main_story" in quest.tags:
            reasons.append("advances main storyline")
        
        return "Recommended because it is " + ", ".join(reasons) + "."
    
    def _assess_quest_difficulty(self, quest: Quest, player: Player) -> str:
        """Assess quest difficulty relative to player"""
        player_power = (player.stats.level + player.stats.strength + player.stats.intelligence) / 3
        
        if quest.risk == RiskLevel.CALM:
            return "Easy"
        elif quest.risk == RiskLevel.MYSTERY:
            if player_power >= 8:
                return "Moderate"
            else:
                return "Challenging"
        elif quest.risk == RiskLevel.COMBAT:
            if player_power >= 12:
                return "Moderate"
            elif player_power >= 8:
                return "Hard"
            else:
                return "Very Hard"
        
        return "Unknown"
    
    def _estimate_quest_duration(self, quest: Quest) -> str:
        """Estimate quest completion time"""
        objective_count = len(quest.objectives)
        
        if objective_count <= 1:
            return "Short (2-3 turns)"
        elif objective_count <= 3:
            return "Medium (4-6 turns)"
        else:
            return "Long (7+ turns)"
    
    def _generate_risk_warning(self, quest: Quest, player: Player) -> Optional[str]:
        """Generate risk warning if quest might be dangerous"""
        if quest.risk == RiskLevel.COMBAT and player.stats.health < 75:
            return "Warning: Combat quest with low health - consider healing first"
        
        if quest.risk == RiskLevel.MYSTERY and player.stats.intelligence < 10:
            return "Note: This quest may require puzzle-solving or investigation skills"
        
        return None

