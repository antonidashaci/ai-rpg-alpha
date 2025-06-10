"""
AI-RPG-Alpha: Quest Selection Criteria

This module contains the criteria and utility functions for quest selection.
Separated from the main quest picker to maintain the 500-line limit.
"""

from enum import Enum
from typing import List, Dict, Any
from models.dataclasses import Quest, Player, RiskLevel

class QuestSelectionCriteria(Enum):
    """Criteria for quest selection"""
    LEVEL_APPROPRIATE = "level_appropriate"
    LOCATION_BASED = "location_based"
    TAG_MATCHING = "tag_matching"
    RISK_SUITABLE = "risk_suitable"
    STORY_PROGRESSION = "story_progression"

class QuestScoringUtils:
    """
    Utility class for quest scoring and evaluation functions.
    
    Contains helper methods for calculating various quest scores
    and determining quest suitability for players.
    """
    
    @staticmethod
    def calculate_level_score(quest: Quest, player: Player) -> float:
        """Calculate level appropriateness score for a quest"""
        level_diff = abs(quest.recommended_level - player.level)
        if level_diff == 0:
            return 1.0
        elif level_diff <= 2:
            return 0.8 - (level_diff * 0.1)
        else:
            return max(0.1, 0.6 - (level_diff * 0.1))
    
    @staticmethod
    def calculate_location_score(quest: Quest, player: Player) -> float:
        """Calculate location relevance score for a quest"""
        if quest.location == player.location:
            return 1.0
        elif quest.location == "any":
            return 0.8
        else:
            return 0.3
    
    @staticmethod
    def calculate_tag_score(quest: Quest, preferred_tags: List[str]) -> float:
        """Calculate tag matching score for a quest"""
        if not preferred_tags:
            return 0.5
        
        matches = sum(1 for tag in preferred_tags if tag in quest.tags)
        return min(1.0, matches / len(preferred_tags))
    
    @staticmethod
    def calculate_risk_score(quest: Quest, player: Player) -> float:
        """Calculate risk appropriateness score for a quest"""
        risk_order = [RiskLevel.CALM, RiskLevel.MYSTERY, RiskLevel.COMBAT]
        
        # Get player's preferred risk level based on their play style
        player_risk_preference = QuestScoringUtils._get_player_risk_preference(player)
        preferred_index = risk_order.index(player_risk_preference)
        quest_index = risk_order.index(quest.risk)
        
        # Score based on how close the quest risk is to player preference
        diff = abs(preferred_index - quest_index)
        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.7
        else:
            return 0.4
    
    @staticmethod
    def calculate_story_score(quest: Quest, player: Player) -> float:
        """Calculate story progression relevance score"""
        # Check if quest continues current storylines
        story_bonus = 0.0
        
        # Bonus for quests that continue active storylines
        for active_quest_id in player.active_quests:
            if quest.prerequisite_quests and active_quest_id in quest.prerequisite_quests:
                story_bonus += 0.3
        
        # Bonus for quests in the same location as recent activity
        if quest.location == player.location:
            story_bonus += 0.2
        
        return min(1.0, 0.5 + story_bonus)
    
    @staticmethod
    def calculate_variety_bonus(quest: Quest, player: Player) -> float:
        """Calculate variety bonus to encourage diverse quest selection"""
        # Check how many similar quests the player has completed recently
        recent_similar_count = 0
        
        # Count quests with similar tags in recent history
        for completed_quest_id in player.completed_quests[-5:]:  # Last 5 quests
            # In a full implementation, we'd look up the quest details
            # For now, assume some variety is good
            if any(tag in quest.tags for tag in ["combat", "mystery", "social"]):
                recent_similar_count += 1
        
        # Return bonus for variety (inverse of similarity)
        return max(0.2, 1.0 - (recent_similar_count * 0.15))
    
    @staticmethod
    def _get_player_risk_preference(player: Player) -> RiskLevel:
        """Determine player's risk preference based on their history and stats"""
        # Analyze player's combat vs non-combat quest completion ratio
        # For now, return a default based on level
        if player.level <= 3:
            return RiskLevel.CALM
        elif player.level <= 6:
            return RiskLevel.MYSTERY
        else:
            return RiskLevel.COMBAT
    
    @staticmethod
    def is_quest_suitable_for_player(quest: Quest, player: Player) -> bool:
        """Check if a quest is suitable for the player"""
        # Level check
        if not QuestScoringUtils._is_level_appropriate(quest, player):
            return False
        
        # Prerequisite check
        if quest.prerequisite_quests:
            for prereq in quest.prerequisite_quests:
                if prereq not in player.completed_quests:
                    return False
        
        # Already completed check
        if quest.id in player.completed_quests:
            return False
        
        # Already active check
        if quest.id in player.active_quests:
            return False
        
        return True
    
    @staticmethod
    def _is_level_appropriate(quest: Quest, player: Player) -> bool:
        """Check if quest is appropriate for player level"""
        level_diff = abs(quest.recommended_level - player.level)
        return level_diff <= 3  # Allow quests within 3 levels
    
    @staticmethod
    def is_quest_too_difficult(quest: Quest, player: Player) -> bool:
        """Check if quest is too difficult for the player"""
        return quest.recommended_level > player.level + 2
    
    @staticmethod
    def get_risk_level_value(risk: RiskLevel) -> int:
        """Convert risk level to numeric value for comparison"""
        risk_values = {
            RiskLevel.CALM: 1,
            RiskLevel.MYSTERY: 2,
            RiskLevel.COMBAT: 3
        }
        return risk_values.get(risk, 2)
    
    @staticmethod
    def generate_recommendation_reasoning(quest: Quest, player: Player) -> str:
        """Generate a text explanation for why this quest is recommended"""
        reasons = []
        
        # Level appropriateness
        level_diff = quest.recommended_level - player.level
        if level_diff == 0:
            reasons.append("perfect level match")
        elif level_diff == 1:
            reasons.append("slightly challenging")
        elif level_diff == -1:
            reasons.append("good for building confidence")
        
        # Location relevance
        if quest.location == player.location:
            reasons.append("available in your current location")
        
        # Risk level
        if quest.risk == RiskLevel.CALM:
            reasons.append("low risk encounter")
        elif quest.risk == RiskLevel.MYSTERY:
            reasons.append("intriguing mystery")
        elif quest.risk == RiskLevel.COMBAT:
            reasons.append("combat challenge")
        
        # Story progression
        if any(tag in ["main", "story"] for tag in quest.tags):
            reasons.append("advances main storyline")
        
        if reasons:
            return f"Recommended because: {', '.join(reasons)}"
        else:
            return "Standard quest recommendation"
    
    @staticmethod
    def assess_quest_difficulty(quest: Quest, player: Player) -> str:
        """Assess the difficulty of a quest for the player"""
        level_diff = quest.recommended_level - player.level
        
        if level_diff <= -2:
            return "Very Easy"
        elif level_diff == -1:
            return "Easy"
        elif level_diff == 0:
            return "Appropriate"
        elif level_diff == 1:
            return "Challenging"
        elif level_diff == 2:
            return "Hard"
        else:
            return "Very Hard"
    
    @staticmethod
    def estimate_quest_duration(quest: Quest) -> str:
        """Estimate quest completion time based on complexity"""
        complexity_indicators = len(quest.objectives) + len(quest.tags)
        
        if complexity_indicators <= 2:
            return "Short (5-10 minutes)"
        elif complexity_indicators <= 4:
            return "Medium (10-20 minutes)"
        else:
            return "Long (20+ minutes)" 