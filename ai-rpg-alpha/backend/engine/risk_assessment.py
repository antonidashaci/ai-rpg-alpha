"""
AI-RPG-Alpha: Risk Assessment Engine

This module evaluates and calculates risk levels for encounters, quests, and player actions.
It provides dynamic difficulty scaling and helps determine appropriate content for players.
Part of Phase 3: Combat & Risk System as defined in PRD.
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import math

from models.dataclasses import Player, Quest, RiskLevel

class RiskFactor(Enum):
    """Different factors that contribute to risk assessment"""
    PLAYER_LEVEL = "player_level"
    PLAYER_HEALTH = "player_health" 
    PLAYER_EQUIPMENT = "player_equipment"
    LOCATION_DANGER = "location_danger"
    ENEMY_STRENGTH = "enemy_strength"
    QUEST_COMPLEXITY = "quest_complexity"
    TIME_PRESSURE = "time_pressure"
    RESOURCE_AVAILABILITY = "resource_availability"

class EncounterType(Enum):
    """Types of encounters for risk assessment"""
    COMBAT = "combat"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    PUZZLE = "puzzle"
    STEALTH = "stealth"
    SURVIVAL = "survival"

class RiskAssessmentEngine:
    """
    Evaluates risk levels for various game encounters and situations.
    
    Provides dynamic difficulty scaling and personalized risk assessment
    based on player capabilities, current state, and encounter characteristics.
    """
    
    def __init__(self):
        """Initialize the risk assessment engine with default configurations."""
        # Base risk weights for different factors
        self.risk_weights = {
            RiskFactor.PLAYER_LEVEL: 0.25,
            RiskFactor.PLAYER_HEALTH: 0.20,
            RiskFactor.PLAYER_EQUIPMENT: 0.15,
            RiskFactor.LOCATION_DANGER: 0.15,
            RiskFactor.ENEMY_STRENGTH: 0.15,
            RiskFactor.QUEST_COMPLEXITY: 0.10
        }
        
        # Location danger ratings
        self.location_danger_ratings = {
            "village": 0.1, "town": 0.2, "forest": 0.4, "mountain": 0.5,
            "cave": 0.6, "dungeon": 0.7, "ruins": 0.6, "swamp": 0.5,
            "desert": 0.4, "castle": 0.8, "tower": 0.7, "abyss": 0.9
        }
        
        # Enemy power ratings
        self.enemy_power_ratings = {
            "rat": 0.1, "goblin": 0.2, "orc": 0.4, "troll": 0.6,
            "dragon": 0.9, "demon": 0.8, "skeleton": 0.3, "zombie": 0.3,
            "bandit": 0.3, "wolf": 0.3, "bear": 0.5, "giant": 0.7
        }
    
    def assess_encounter_risk(
        self, 
        player: Player, 
        encounter_type: EncounterType,
        encounter_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess the risk level of a specific encounter for a player.
        
        Args:
            player: Player object with current stats and state
            encounter_type: Type of encounter being assessed
            encounter_data: Dictionary with encounter details
            
        Returns:
            Dictionary with risk assessment results
        """
        # Calculate individual risk factors
        risk_factors = self._calculate_risk_factors(player, encounter_type, encounter_data)
        
        # Calculate overall risk score
        overall_risk = self._calculate_weighted_risk(risk_factors)
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_risk)
        
        # Generate risk recommendations
        recommendations = self._generate_risk_recommendations(
            player, risk_factors, risk_level
        )
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(player, overall_risk)
        
        return {
            "risk_level": risk_level,
            "risk_score": overall_risk,
            "risk_factors": risk_factors,
            "success_probability": success_probability,
            "recommendations": recommendations,
            "encounter_type": encounter_type.value
        }
    
    def assess_quest_risk(self, player: Player, quest: Quest) -> Dict[str, Any]:
        """
        Assess the risk level of a quest for a player.
        
        Args:
            player: Player object
            quest: Quest object to assess
            
        Returns:
            Dictionary with quest risk assessment
        """
        # Build encounter data from quest
        encounter_data = {
            "location": quest.location,
            "objectives": quest.objectives,
            "recommended_level": getattr(quest, 'recommended_level', player.level),
            "tags": quest.tags,
            "rewards": quest.reward
        }
        
        # Determine primary encounter type from quest tags
        encounter_type = self._determine_encounter_type_from_quest(quest)
        
        # Assess risk
        risk_assessment = self.assess_encounter_risk(player, encounter_type, encounter_data)
        
        # Add quest-specific analysis
        quest_analysis = self._analyze_quest_requirements(player, quest)
        risk_assessment.update(quest_analysis)
        
        return risk_assessment
    
    def get_difficulty_recommendation(
        self, 
        player: Player, 
        base_difficulty: str = "medium"
    ) -> str:
        """
        Recommend an appropriate difficulty level for a player.
        
        Args:
            player: Player object
            base_difficulty: Base difficulty to adjust from
            
        Returns:
            Recommended difficulty level
        """
        player_power = self._calculate_player_power_level(player)
        
        # Adjust difficulty based on player power
        if player_power < 0.3:
            return "easy"
        elif player_power < 0.5:
            return "medium"
        elif player_power < 0.7:
            return "hard"
        else:
            return "epic"
    
    def calculate_dynamic_scaling(
        self, 
        player: Player, 
        base_encounter: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate dynamic scaling adjustments for an encounter.
        
        Args:
            player: Player object
            base_encounter: Base encounter data
            
        Returns:
            Dictionary with scaling adjustments
        """
        player_power = self._calculate_player_power_level(player)
        
        # Calculate scaling factors
        health_scaling = self._calculate_health_scaling(player)
        damage_scaling = self._calculate_damage_scaling(player)
        reward_scaling = self._calculate_reward_scaling(player)
        
        return {
            "health_multiplier": health_scaling,
            "damage_multiplier": damage_scaling,
            "reward_multiplier": reward_scaling,
            "player_power_level": player_power,
            "scaling_rationale": self._generate_scaling_rationale(
                health_scaling, damage_scaling, reward_scaling
            )
        }
    
    def _calculate_risk_factors(
        self, 
        player: Player, 
        encounter_type: EncounterType,
        encounter_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate individual risk factor scores."""
        factors = {}
        
        # Player level factor
        recommended_level = encounter_data.get("recommended_level", player.level)
        level_diff = recommended_level - player.level
        factors[RiskFactor.PLAYER_LEVEL] = min(1.0, max(0.0, (level_diff + 2) / 4))
        
        # Player health factor
        health_ratio = player.health / 100.0  # Assuming max health is 100
        factors[RiskFactor.PLAYER_HEALTH] = 1.0 - health_ratio
        
        # Equipment factor (simplified)
        equipment_score = len(player.inventory) / 10.0  # Assume 10 items = well equipped
        factors[RiskFactor.PLAYER_EQUIPMENT] = 1.0 - min(1.0, equipment_score)
        
        # Location danger factor
        location = encounter_data.get("location", "unknown")
        factors[RiskFactor.LOCATION_DANGER] = self.location_danger_ratings.get(location, 0.5)
        
        # Enemy strength factor
        enemy_type = encounter_data.get("enemy_type", "unknown")
        factors[RiskFactor.ENEMY_STRENGTH] = self.enemy_power_ratings.get(enemy_type, 0.5)
        
        # Quest complexity factor
        objectives_count = len(encounter_data.get("objectives", []))
        factors[RiskFactor.QUEST_COMPLEXITY] = min(1.0, objectives_count / 5.0)
        
        return factors
    
    def _calculate_weighted_risk(self, risk_factors: Dict[RiskFactor, float]) -> float:
        """Calculate overall weighted risk score."""
        total_risk = 0.0
        total_weight = 0.0
        
        for factor, score in risk_factors.items():
            weight = self.risk_weights.get(factor, 0.1)
            total_risk += score * weight
            total_weight += weight
        
        return total_risk / total_weight if total_weight > 0 else 0.5
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Convert risk score to risk level enum."""
        if risk_score <= 0.3:
            return RiskLevel.CALM
        elif risk_score <= 0.7:
            return RiskLevel.MYSTERY
        else:
            return RiskLevel.COMBAT
    
    def _generate_risk_recommendations(
        self, 
        player: Player, 
        risk_factors: Dict[RiskFactor, float],
        risk_level: RiskLevel
    ) -> List[str]:
        """Generate recommendations based on risk assessment."""
        recommendations = []
        
        # Health recommendations
        if risk_factors.get(RiskFactor.PLAYER_HEALTH, 0) > 0.5:
            recommendations.append("Consider healing before proceeding")
        
        # Equipment recommendations
        if risk_factors.get(RiskFactor.PLAYER_EQUIPMENT, 0) > 0.6:
            recommendations.append("Acquire better equipment before this encounter")
        
        # Level recommendations
        if risk_factors.get(RiskFactor.PLAYER_LEVEL, 0) > 0.7:
            recommendations.append("This encounter may be too challenging for your level")
        
        # Risk level specific recommendations
        if risk_level == RiskLevel.COMBAT:
            recommendations.append("High risk encounter - prepare for combat")
        elif risk_level == RiskLevel.MYSTERY:
            recommendations.append("Moderate risk - stay alert and be prepared")
        
        return recommendations
    
    def _calculate_success_probability(self, player: Player, risk_score: float) -> float:
        """Calculate probability of success based on player and risk."""
        player_power = self._calculate_player_power_level(player)
        
        # Base success probability inverse to risk
        base_probability = 1.0 - risk_score
        
        # Adjust based on player power
        power_adjustment = (player_power - 0.5) * 0.4  # -0.2 to +0.2 adjustment
        
        final_probability = base_probability + power_adjustment
        return max(0.1, min(0.9, final_probability))  # Clamp between 10% and 90%
    
    def _calculate_player_power_level(self, player: Player) -> float:
        """Calculate overall player power level (0.0 to 1.0)."""
        # Normalize different player attributes
        level_power = min(1.0, player.level / 10.0)  # Assuming max level 10
        health_power = player.health / 100.0  # Assuming max health 100
        equipment_power = min(1.0, len(player.inventory) / 10.0)  # 10 items = max
        
        # Weighted combination
        return (level_power * 0.5 + health_power * 0.3 + equipment_power * 0.2)
    
    def _determine_encounter_type_from_quest(self, quest: Quest) -> EncounterType:
        """Determine primary encounter type from quest tags."""
        if any(tag in quest.tags for tag in ["combat", "fight", "battle"]):
            return EncounterType.COMBAT
        elif any(tag in quest.tags for tag in ["stealth", "sneak", "infiltrate"]):
            return EncounterType.STEALTH
        elif any(tag in quest.tags for tag in ["social", "persuade", "negotiate"]):
            return EncounterType.SOCIAL
        elif any(tag in quest.tags for tag in ["puzzle", "riddle", "mystery"]):
            return EncounterType.PUZZLE
        elif any(tag in quest.tags for tag in ["explore", "discovery", "travel"]):
            return EncounterType.EXPLORATION
        else:
            return EncounterType.EXPLORATION  # Default
    
    def _analyze_quest_requirements(self, player: Player, quest: Quest) -> Dict[str, Any]:
        """Analyze if player meets quest requirements."""
        analysis = {
            "meets_requirements": True,
            "missing_requirements": [],
            "recommended_preparation": []
        }
        
        # Check level requirements
        if hasattr(quest, 'recommended_level'):
            if player.level < quest.recommended_level:
                analysis["meets_requirements"] = False
                analysis["missing_requirements"].append(f"Level {quest.recommended_level} required")
        
        # Check prerequisite quests
        if hasattr(quest, 'prerequisite_quests'):
            missing_prereqs = [
                prereq for prereq in quest.prerequisite_quests 
                if prereq not in player.completed_quests
            ]
            if missing_prereqs:
                analysis["meets_requirements"] = False
                analysis["missing_requirements"].extend(missing_prereqs)
        
        return analysis
    
    def _calculate_health_scaling(self, player: Player) -> float:
        """Calculate health scaling multiplier."""
        return 1.0 + (player.level - 1) * 0.1  # 10% per level above 1
    
    def _calculate_damage_scaling(self, player: Player) -> float:
        """Calculate damage scaling multiplier."""
        return 1.0 + (player.level - 1) * 0.15  # 15% per level above 1
    
    def _calculate_reward_scaling(self, player: Player) -> float:
        """Calculate reward scaling multiplier."""
        return 1.0 + (player.level - 1) * 0.05  # 5% per level above 1
    
    def _generate_scaling_rationale(
        self, 
        health_scaling: float, 
        damage_scaling: float, 
        reward_scaling: float
    ) -> str:
        """Generate explanation for scaling adjustments."""
        return (
            f"Encounter scaled: {health_scaling:.1f}x health, "
            f"{damage_scaling:.1f}x damage, {reward_scaling:.1f}x rewards"
        ) 