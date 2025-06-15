"""
AI-RPG-Alpha: Character Progression System

This module handles character advancement, stats progression, and skill development.
Part of Phase 3: Combat & Risk System as defined in PRD.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

class StatType(Enum):
    """Types of character statistics"""
    STRENGTH = "strength"
    INTELLIGENCE = "intelligence"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    CHARISMA = "charisma"
    WISDOM = "wisdom"

class SkillType(Enum):
    """Types of character skills"""
    COMBAT = "combat"
    MAGIC = "magic"
    STEALTH = "stealth"
    PERSUASION = "persuasion"
    EXPLORATION = "exploration"
    SURVIVAL = "survival"

@dataclass
class CharacterStats:
    """Character statistics container"""
    strength: int = 10
    intelligence: int = 10
    dexterity: int = 10
    constitution: int = 10
    charisma: int = 10
    wisdom: int = 10
    
    def get_stat(self, stat_type: StatType) -> int:
        """Get a specific stat value"""
        return getattr(self, stat_type.value)
    
    def set_stat(self, stat_type: StatType, value: int):
        """Set a specific stat value"""
        setattr(self, stat_type.value, max(1, min(20, value)))  # Clamp between 1-20

@dataclass
class Skill:
    """Individual skill definition"""
    name: str
    level: int = 1
    experience: int = 0
    max_level: int = 10
    description: str = ""
    
    def add_experience(self, exp: int) -> bool:
        """Add experience and check for level up"""
        self.experience += exp
        return self._check_level_up()
    
    def _check_level_up(self) -> bool:
        """Check if skill should level up"""
        exp_needed = self._calculate_exp_for_level(self.level + 1)
        if self.experience >= exp_needed and self.level < self.max_level:
            self.level += 1
            return True
        return False
    
    def _calculate_exp_for_level(self, target_level: int) -> int:
        """Calculate experience needed for a target level"""
        return target_level * 100  # Simple linear progression

class CharacterProgression:
    """
    Manages character progression including stats, skills, and level advancement.
    
    Handles experience gain, stat distribution, skill development,
    and provides progression recommendations based on player actions.
    """
    
    def __init__(self):
        """Initialize the character progression system"""
        # Experience requirements for each level
        self.level_exp_requirements = {
            1: 0, 2: 100, 3: 250, 4: 450, 5: 700,
            6: 1000, 7: 1350, 8: 1750, 9: 2200, 10: 2700
        }
        
        # Stat point allocation per level
        self.stat_points_per_level = 2
        
        # Base health per constitution point
        self.health_per_constitution = 5
        
        # Base mana per intelligence point
        self.mana_per_intelligence = 3
    
    def calculate_level_from_experience(self, experience: int) -> int:
        """Calculate character level based on total experience"""
        for level in range(10, 0, -1):
            if experience >= self.level_exp_requirements[level]:
                return level
        return 1
    
    def get_experience_for_next_level(self, current_level: int) -> int:
        """Get experience required for next level"""
        if current_level >= 10:
            return 0  # Max level reached
        return self.level_exp_requirements[current_level + 1]
    
    def calculate_stat_bonuses(self, stats: CharacterStats) -> Dict[str, int]:
        """Calculate bonuses derived from stats"""
        bonuses = {}
        
        # Health bonus from constitution
        bonuses["max_health"] = 50 + (stats.constitution * self.health_per_constitution)
        
        # Mana bonus from intelligence
        bonuses["max_mana"] = 20 + (stats.intelligence * self.mana_per_intelligence)
        
        # Attack bonus from strength
        bonuses["attack_bonus"] = max(0, (stats.strength - 10) // 2)
        
        # Defense bonus from dexterity
        bonuses["defense_bonus"] = max(0, (stats.dexterity - 10) // 2)
        
        # Initiative bonus from dexterity
        bonuses["initiative_bonus"] = max(0, (stats.dexterity - 10) // 2)
        
        # Social bonus from charisma
        bonuses["social_bonus"] = max(0, (stats.charisma - 10) // 2)
        
        # Perception bonus from wisdom
        bonuses["perception_bonus"] = max(0, (stats.wisdom - 10) // 2)
        
        return bonuses
    
    def level_up_character(
        self, 
        current_stats: CharacterStats, 
        current_level: int,
        stat_choices: Dict[StatType, int] = None
    ) -> Dict[str, Any]:
        """
        Process character level up with stat allocation.
        
        Args:
            current_stats: Current character stats
            current_level: Current character level
            stat_choices: Player's chosen stat allocations
            
        Returns:
            Dictionary with level up results
        """
        # Calculate available stat points
        available_points = self.stat_points_per_level
        
        # Apply stat choices if provided
        if stat_choices:
            total_allocated = sum(stat_choices.values())
            if total_allocated <= available_points:
                for stat_type, points in stat_choices.items():
                    current_value = current_stats.get_stat(stat_type)
                    current_stats.set_stat(stat_type, current_value + points)
                    available_points -= points
        
        # Calculate new bonuses
        new_bonuses = self.calculate_stat_bonuses(current_stats)
        
        return {
            "new_level": current_level + 1,
            "stat_points_used": self.stat_points_per_level - available_points,
            "stat_points_remaining": available_points,
            "new_stats": current_stats,
            "stat_bonuses": new_bonuses,
            "level_up_message": f"Congratulations! You've reached level {current_level + 1}!"
        }
    
    def gain_skill_experience(
        self, 
        skills: Dict[str, Skill], 
        skill_type: SkillType, 
        experience: int
    ) -> Dict[str, Any]:
        """
        Add experience to a skill and handle potential level ups.
        
        Args:
            skills: Current skills dictionary
            skill_type: Type of skill gaining experience
            experience: Amount of experience to add
            
        Returns:
            Dictionary with skill progression results
        """
        skill_name = skill_type.value
        
        # Get or create skill
        if skill_name not in skills:
            skills[skill_name] = Skill(name=skill_name, description=f"{skill_name.title()} proficiency")
        
        skill = skills[skill_name]
        old_level = skill.level
        
        # Add experience and check for level up
        leveled_up = skill.add_experience(experience)
        
        result = {
            "skill_name": skill_name,
            "experience_gained": experience,
            "new_experience": skill.experience,
            "old_level": old_level,
            "new_level": skill.level,
            "leveled_up": leveled_up
        }
        
        if leveled_up:
            result["level_up_message"] = f"Your {skill_name} skill increased to level {skill.level}!"
        
        return result
    
    def get_skill_recommendations(
        self, 
        recent_actions: List[str], 
        current_skills: Dict[str, Skill]
    ) -> List[Dict[str, Any]]:
        """
        Recommend skills to focus on based on recent player actions.
        
        Args:
            recent_actions: List of recent player actions
            current_skills: Current skills dictionary
            
        Returns:
            List of skill recommendations
        """
        action_skill_mapping = {
            "attack": SkillType.COMBAT,
            "fight": SkillType.COMBAT,
            "cast": SkillType.MAGIC,
            "magic": SkillType.MAGIC,
            "sneak": SkillType.STEALTH,
            "hide": SkillType.STEALTH,
            "persuade": SkillType.PERSUASION,
            "convince": SkillType.PERSUASION,
            "explore": SkillType.EXPLORATION,
            "search": SkillType.EXPLORATION
        }
        
        # Count action types
        skill_usage = {}
        for action in recent_actions:
            action_lower = action.lower()
            for keyword, skill_type in action_skill_mapping.items():
                if keyword in action_lower:
                    skill_usage[skill_type] = skill_usage.get(skill_type, 0) + 1
        
        # Generate recommendations
        recommendations = []
        for skill_type, usage_count in skill_usage.items():
            skill_name = skill_type.value
            current_level = current_skills.get(skill_name, Skill(name=skill_name)).level
            
            if usage_count >= 3:  # Frequently used skills
                recommendations.append({
                    "skill": skill_name,
                    "reason": f"You've been using {skill_name} frequently",
                    "current_level": current_level,
                    "priority": "high" if usage_count >= 5 else "medium"
                })
        
        return recommendations
    
    def calculate_progression_stats(
        self, 
        player_level: int, 
        total_experience: int,
        skills: Dict[str, Skill]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive progression statistics.
        
        Args:
            player_level: Current player level
            total_experience: Total experience earned
            skills: Current skills dictionary
            
        Returns:
            Dictionary with progression statistics
        """
        # Experience to next level
        exp_to_next = self.get_experience_for_next_level(player_level)
        current_level_exp = self.level_exp_requirements[player_level]
        
        if player_level < 10:
            exp_progress = total_experience - current_level_exp
            exp_needed = exp_to_next - current_level_exp
            level_progress = exp_progress / exp_needed if exp_needed > 0 else 1.0
        else:
            level_progress = 1.0  # Max level
        
        # Calculate total skill levels
        total_skill_levels = sum(skill.level for skill in skills.values())
        max_possible_skill_levels = len(skills) * 10  # Assuming max skill level is 10
        
        return {
            "level": player_level,
            "total_experience": total_experience,
            "experience_to_next_level": exp_to_next - total_experience if player_level < 10 else 0,
            "level_progress_percentage": level_progress * 100,
            "total_skills": len(skills),
            "total_skill_levels": total_skill_levels,
            "skill_mastery_percentage": (total_skill_levels / max_possible_skill_levels * 100) if skills else 0,
            "highest_skill_level": max((skill.level for skill in skills.values()), default=0),
            "skills_summary": {name: {"level": skill.level, "experience": skill.experience} 
                             for name, skill in skills.items()}
        }
    
    def suggest_stat_allocation(
        self, 
        current_stats: CharacterStats, 
        available_points: int,
        play_style_hints: List[str] = None
    ) -> Dict[StatType, int]:
        """
        Suggest optimal stat point allocation based on play style.
        
        Args:
            current_stats: Current character stats
            available_points: Available stat points to allocate
            play_style_hints: Hints about player's preferred play style
            
        Returns:
            Dictionary mapping stat types to suggested point allocation
        """
        suggestions = {}
        
        if not play_style_hints:
            # Balanced allocation if no hints
            points_per_stat = available_points // 6
            remainder = available_points % 6
            
            for stat_type in StatType:
                suggestions[stat_type] = points_per_stat
            
            # Distribute remainder to constitution and strength (survivability)
            if remainder > 0:
                suggestions[StatType.CONSTITUTION] += 1
                remainder -= 1
            if remainder > 0:
                suggestions[StatType.STRENGTH] += 1
        else:
            # Allocate based on play style hints
            style_priorities = self._analyze_play_style(play_style_hints)
            total_priority = sum(style_priorities.values())
            
            for stat_type in StatType:
                priority = style_priorities.get(stat_type, 1)
                suggested_points = int((priority / total_priority) * available_points)
                suggestions[stat_type] = suggested_points
        
        return suggestions
    
    def _analyze_play_style(self, hints: List[str]) -> Dict[StatType, int]:
        """Analyze play style hints to determine stat priorities"""
        priorities = {stat: 1 for stat in StatType}  # Base priority
        
        for hint in hints:
            hint_lower = hint.lower()
            
            if any(word in hint_lower for word in ["fight", "combat", "attack", "warrior"]):
                priorities[StatType.STRENGTH] += 3
                priorities[StatType.CONSTITUTION] += 2
            
            if any(word in hint_lower for word in ["magic", "spell", "wizard", "mage"]):
                priorities[StatType.INTELLIGENCE] += 3
                priorities[StatType.WISDOM] += 2
            
            if any(word in hint_lower for word in ["sneak", "stealth", "thief", "rogue"]):
                priorities[StatType.DEXTERITY] += 3
                priorities[StatType.INTELLIGENCE] += 1
            
            if any(word in hint_lower for word in ["social", "persuade", "leader", "diplomat"]):
                priorities[StatType.CHARISMA] += 3
                priorities[StatType.WISDOM] += 1
        
        return priorities 