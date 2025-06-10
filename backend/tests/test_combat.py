"""
AI-RPG-Alpha: Combat System Tests

Comprehensive test suite for the narrative combat system including
combat resolution, risk assessment, and character progression.
Part of Phase 5: Testing & Optimization as defined in PRD.
"""

import pytest
import asyncio
import json
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, patch, AsyncMock

from backend.engine.combat import CombatResolver
from backend.engine.risk_assessment import RiskAssessment
from backend.models.character import Character, CharacterStats, Equipment
from backend.models.dataclasses import (
    Player, Quest, GameEvent, CombatEvent, CombatResult,
    Enemy, CombatAction, CombatOutcome
)


class TestCombatResolver:
    """Test suite for Combat Resolution System"""
    
    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client for testing"""
        mock_client = Mock()
        mock_client.generate_narrative = AsyncMock()
        mock_client.analyze_combat_situation = AsyncMock()
        return mock_client
    
    @pytest.fixture
    def mock_risk_assessment(self):
        """Mock risk assessment for testing"""
        mock_risk = Mock()
        mock_risk.calculate_encounter_risk = AsyncMock()
        mock_risk.assess_combat_difficulty = AsyncMock()
        return mock_risk
    
    @pytest.fixture
    def combat_resolver(self, mock_ai_client, mock_risk_assessment):
        """Create CombatResolver instance for testing"""
        return CombatResolver(
            ai_client=mock_ai_client,
            risk_assessment=mock_risk_assessment
        )
    
    @pytest.fixture
    def sample_player(self):
        """Sample player character for testing"""
        return Player(
            id="player_123",
            name="TestWarrior",
            level=5,
            experience=200,
            health=85,
            max_health=100,
            stats={
                "strength": 15,
                "dexterity": 12,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 11,
                "charisma": 9
            },
            equipment={
                "weapon": {
                    "name": "Iron Sword",
                    "damage": 8,
                    "type": "melee"
                },
                "armor": {
                    "name": "Leather Armor",
                    "defense": 3,
                    "type": "light"
                }
            }
        )
    
    @pytest.fixture
    def sample_enemy(self):
        """Sample enemy for testing"""
        return Enemy(
            id="goblin_001",
            name="Goblin Warrior",
            level=3,
            health=25,
            max_health=25,
            stats={
                "strength": 8,
                "dexterity": 14,
                "constitution": 10,
                "intelligence": 6,
                "wisdom": 8,
                "charisma": 4
            },
            abilities=["quick_strike", "dodge"],
            loot_table={
                "gold": (5, 15),
                "items": ["rusty_dagger", "goblin_ear"]
            }
        )

    @pytest.mark.asyncio
    async def test_combat_resolver_initialization(self, mock_ai_client, mock_risk_assessment):
        """Test CombatResolver initialization"""
        resolver = CombatResolver(
            ai_client=mock_ai_client,
            risk_assessment=mock_risk_assessment
        )
        
        assert resolver.ai_client is mock_ai_client
        assert resolver.risk_assessment is mock_risk_assessment
        assert resolver.combat_log == []

    @pytest.mark.asyncio
    async def test_initiate_combat(self, combat_resolver, sample_player, sample_enemy):
        """Test combat initiation"""
        # Mock AI response
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "A goblin warrior emerges from the shadows!",
            "combat_options": [
                "Attack with sword",
                "Attempt to dodge",
                "Try to intimidate"
            ]
        }
        
        # Mock risk assessment
        combat_resolver.risk_assessment.assess_combat_difficulty.return_value = {
            "difficulty": "medium",
            "player_advantage": 0.3,
            "suggested_strategy": "aggressive"
        }
        
        result = await combat_resolver.initiate_combat(
            player=sample_player,
            enemy=sample_enemy,
            context="forest_ambush"
        )
        
        assert result is not None
        assert "narrative" in result
        assert "combat_options" in result
        assert len(combat_resolver.combat_log) > 0

    @pytest.mark.asyncio
    async def test_resolve_combat_action(self, combat_resolver, sample_player, sample_enemy):
        """Test resolving a combat action"""
        # Start combat
        await combat_resolver.initiate_combat(sample_player, sample_enemy, "test")
        
        # Mock AI narrative generation
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "Your sword strikes true, wounding the goblin!",
            "damage_dealt": 12,
            "damage_taken": 3,
            "enemy_response": "The goblin counter-attacks with its claws!"
        }
        
        action = CombatAction(
            type="attack",
            target="enemy",
            weapon="sword",
            modifier="power_attack"
        )
        
        result = await combat_resolver.resolve_action(
            player=sample_player,
            enemy=sample_enemy,
            action=action
        )
        
        assert result is not None
        assert "narrative" in result
        assert "damage_dealt" in result
        assert result["damage_dealt"] > 0

    @pytest.mark.asyncio
    async def test_combat_outcome_victory(self, combat_resolver, sample_player, sample_enemy):
        """Test combat ending in player victory"""
        # Set enemy to low health
        sample_enemy.health = 1
        
        # Mock finishing blow
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "Your final strike defeats the goblin!",
            "damage_dealt": 10,
            "damage_taken": 0,
            "combat_ended": True,
            "victory": True
        }
        
        action = CombatAction(type="attack", target="enemy", weapon="sword")
        
        result = await combat_resolver.resolve_action(
            player=sample_player,
            enemy=sample_enemy,
            action=action
        )
        
        assert result["combat_ended"] is True
        assert result["victory"] is True
        
        # Check combat outcome
        outcome = await combat_resolver.get_combat_outcome()
        assert outcome.victory is True
        assert outcome.experience_gained > 0

    @pytest.mark.asyncio
    async def test_combat_outcome_defeat(self, combat_resolver, sample_player, sample_enemy):
        """Test combat ending in player defeat"""
        # Set player to low health
        sample_player.health = 1
        
        # Mock fatal enemy attack
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "The goblin's attack proves fatal!",
            "damage_dealt": 0,
            "damage_taken": 15,
            "combat_ended": True,
            "victory": False
        }
        
        action = CombatAction(type="defend", target="self")
        
        result = await combat_resolver.resolve_action(
            player=sample_player,
            enemy=sample_enemy,
            action=action
        )
        
        assert result["combat_ended"] is True
        assert result["victory"] is False
        
        # Check combat outcome
        outcome = await combat_resolver.get_combat_outcome()
        assert outcome.victory is False
        assert outcome.experience_gained == 0

    @pytest.mark.asyncio
    async def test_combat_escape(self, combat_resolver, sample_player, sample_enemy):
        """Test successful combat escape"""
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "You successfully flee from combat!",
            "escape_successful": True,
            "combat_ended": True,
            "victory": None
        }
        
        action = CombatAction(type="escape", target="self")
        
        result = await combat_resolver.resolve_action(
            player=sample_player,
            enemy=sample_enemy,
            action=action
        )
        
        assert result["combat_ended"] is True
        assert result["escape_successful"] is True

    @pytest.mark.asyncio
    async def test_stat_based_combat_modifiers(self, combat_resolver, sample_player, sample_enemy):
        """Test combat modifiers based on character stats"""
        # High strength player should get damage bonus
        sample_player.stats["strength"] = 18
        
        modifiers = combat_resolver.calculate_combat_modifiers(sample_player)
        
        assert modifiers["damage_bonus"] > 0
        assert modifiers["hit_chance_bonus"] > 0
        
        # High dexterity should affect dodge chance
        sample_player.stats["dexterity"] = 16
        modifiers = combat_resolver.calculate_combat_modifiers(sample_player)
        
        assert modifiers["dodge_chance"] > 0.1

    @pytest.mark.asyncio
    async def test_equipment_effects(self, combat_resolver, sample_player):
        """Test equipment effects on combat"""
        # Test weapon damage
        weapon_damage = combat_resolver.calculate_weapon_damage(
            sample_player.equipment["weapon"]
        )
        assert weapon_damage == 8
        
        # Test armor defense
        armor_defense = combat_resolver.calculate_armor_defense(
            sample_player.equipment["armor"]
        )
        assert armor_defense == 3

    @pytest.mark.asyncio
    async def test_multi_enemy_combat(self, combat_resolver, sample_player):
        """Test combat against multiple enemies"""
        enemies = [
            Enemy(
                id="goblin_001",
                name="Goblin Scout",
                level=2,
                health=15,
                max_health=15,
                stats={"strength": 6, "dexterity": 12}
            ),
            Enemy(
                id="goblin_002", 
                name="Goblin Archer",
                level=3,
                health=20,
                max_health=20,
                stats={"strength": 8, "dexterity": 14}
            )
        ]
        
        # Mock multi-enemy combat
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "You face multiple goblins!",
            "combat_options": [
                "Focus on scout",
                "Attack archer",
                "Defensive stance"
            ]
        }
        
        result = await combat_resolver.initiate_multi_combat(
            player=sample_player,
            enemies=enemies,
            context="ambush"
        )
        
        assert result is not None
        assert len(result["enemies"]) == 2

    @pytest.mark.asyncio
    async def test_special_abilities(self, combat_resolver, sample_player, sample_enemy):
        """Test special ability usage in combat"""
        # Add special ability to player
        sample_player.abilities = ["power_strike", "healing_potion"]
        
        action = CombatAction(
            type="special_ability",
            target="enemy",
            ability="power_strike"
        )
        
        # Mock special ability effects
        combat_resolver.ai_client.generate_narrative.return_value = {
            "narrative": "You unleash a powerful strike!",
            "damage_dealt": 18,  # Higher than normal
            "damage_taken": 0,
            "ability_used": "power_strike"
        }
        
        result = await combat_resolver.resolve_action(
            player=sample_player,
            enemy=sample_enemy,
            action=action
        )
        
        assert result["damage_dealt"] > 10  # Should be higher than normal attack
        assert result["ability_used"] == "power_strike"

    @pytest.mark.asyncio
    async def test_environmental_effects(self, combat_resolver, sample_player, sample_enemy):
        """Test environmental effects on combat"""
        environment = {
            "type": "swamp",
            "effects": {
                "movement_penalty": 0.3,
                "visibility": "poor",
                "terrain_bonus": {"dexterity": -2}
            }
        }
        
        modifiers = combat_resolver.calculate_environmental_modifiers(environment)
        
        assert modifiers["movement_penalty"] == 0.3
        assert modifiers["terrain_bonus"]["dexterity"] == -2


class TestRiskAssessment:
    """Test suite for Risk Assessment System"""
    
    @pytest.fixture
    def risk_assessment(self):
        """Create RiskAssessment instance for testing"""
        return RiskAssessment()
    
    @pytest.fixture
    def low_level_player(self):
        """Low level player for risk testing"""
        return Player(
            id="newbie_001",
            name="Newbie",
            level=1,
            experience=0,
            health=50,
            max_health=50,
            stats={
                "strength": 8,
                "dexterity": 10,
                "constitution": 12,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 8
            }
        )

    def test_calculate_player_power_level(self, risk_assessment, sample_player):
        """Test player power level calculation"""
        power_level = risk_assessment.calculate_player_power_level(sample_player)
        
        assert power_level > 0
        assert isinstance(power_level, (int, float))
        
        # Higher level player should have higher power level
        high_level_player = Player(
            id="veteran_001",
            name="Veteran",
            level=10,
            experience=1000,
            health=150,
            max_health=150,
            stats={stat: 18 for stat in sample_player.stats.keys()}
        )
        
        high_power = risk_assessment.calculate_player_power_level(high_level_player)
        assert high_power > power_level

    def test_calculate_enemy_threat_level(self, risk_assessment, sample_enemy):
        """Test enemy threat level calculation"""
        threat_level = risk_assessment.calculate_enemy_threat_level(sample_enemy)
        
        assert threat_level > 0
        assert isinstance(threat_level, (int, float))

    @pytest.mark.asyncio
    async def test_assess_combat_difficulty(self, risk_assessment, sample_player, sample_enemy):
        """Test combat difficulty assessment"""
        assessment = await risk_assessment.assess_combat_difficulty(
            player=sample_player,
            enemy=sample_enemy
        )
        
        assert "difficulty" in assessment
        assert assessment["difficulty"] in ["trivial", "easy", "medium", "hard", "deadly"]
        assert "player_advantage" in assessment
        assert -1.0 <= assessment["player_advantage"] <= 1.0

    @pytest.mark.asyncio
    async def test_risk_scaling(self, risk_assessment, low_level_player, sample_enemy):
        """Test risk scaling for different player levels"""
        # Assess same enemy vs low level player
        low_assessment = await risk_assessment.assess_combat_difficulty(
            player=low_level_player,
            enemy=sample_enemy
        )
        
        # Should be more difficult for low level player
        assert low_assessment["difficulty"] in ["hard", "deadly"]
        assert low_assessment["player_advantage"] < 0

    def test_environmental_risk_factors(self, risk_assessment):
        """Test environmental risk factor calculation"""
        dangerous_environment = {
            "type": "volcanic_cave",
            "hazards": ["lava", "toxic_gas", "unstable_ground"],
            "visibility": "very_poor"
        }
        
        risk_factors = risk_assessment.calculate_environmental_risk(dangerous_environment)
        
        assert risk_factors["total_risk"] > 0
        assert "hazard_effects" in risk_factors

    @pytest.mark.asyncio
    async def test_encounter_recommendation(self, risk_assessment, sample_player):
        """Test encounter difficulty recommendations"""
        recommendations = await risk_assessment.recommend_encounter_difficulty(
            player=sample_player,
            context="random_encounter"
        )
        
        assert "recommended_difficulty" in recommendations
        assert "enemy_level_range" in recommendations
        assert "encounter_types" in recommendations


class TestCharacterProgression:
    """Test suite for Character Progression System"""
    
    @pytest.fixture
    def character(self):
        """Create Character instance for testing"""
        return Character(
            player_id="player_123",
            stats=CharacterStats(
                strength=10,
                dexterity=12,
                constitution=14,
                intelligence=11,
                wisdom=13,
                charisma=9
            ),
            level=1,
            experience=0
        )

    def test_experience_gain(self, character):
        """Test experience point gain and level up"""
        initial_level = character.level
        
        # Add experience
        character.gain_experience(150)
        
        assert character.experience == 150
        
        # Should level up if enough experience
        if character.experience >= character.experience_for_next_level():
            assert character.level > initial_level

    def test_stat_progression(self, character):
        """Test stat increases on level up"""
        initial_stats = character.stats.copy()
        
        # Force level up
        character.level_up()
        
        # At least one stat should have increased
        current_stats = character.stats
        stat_increased = any(
            getattr(current_stats, stat) > getattr(initial_stats, stat)
            for stat in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        )
        assert stat_increased

    def test_combat_experience_calculation(self, character):
        """Test experience calculation from combat"""
        enemy_level = 3
        victory_type = "standard"
        
        exp_gained = character.calculate_combat_experience(
            enemy_level=enemy_level,
            victory_type=victory_type,
            difficulty_modifier=1.0
        )
        
        assert exp_gained > 0
        
        # Harder enemies should give more experience
        hard_exp = character.calculate_combat_experience(
            enemy_level=enemy_level + 2,
            victory_type=victory_type,
            difficulty_modifier=1.5
        )
        
        assert hard_exp > exp_gained

    def test_equipment_requirements(self, character):
        """Test equipment level requirements"""
        high_level_weapon = Equipment(
            name="Legendary Sword",
            type="weapon",
            level_requirement=10,
            stats_bonus={"strength": 5, "damage": 15}
        )
        
        # Low level character shouldn't be able to equip
        can_equip = character.can_equip(high_level_weapon)
        assert can_equip is False
        
        # Level up character
        character.level = 10
        can_equip = character.can_equip(high_level_weapon)
        assert can_equip is True


class TestCombatIntegration:
    """Integration tests for combat system components"""
    
    @pytest.mark.asyncio
    async def test_full_combat_sequence(self):
        """Test complete combat sequence from start to finish"""
        # Mock dependencies
        mock_ai_client = Mock()
        mock_ai_client.generate_narrative = AsyncMock()
        
        risk_assessment = RiskAssessment()
        combat_resolver = CombatResolver(
            ai_client=mock_ai_client,
            risk_assessment=risk_assessment
        )
        
        # Create test characters
        player = Player(
            id="player_123",
            name="TestHero",
            level=3,
            experience=100,
            health=60,
            max_health=60,
            stats={"strength": 12, "dexterity": 10, "constitution": 12}
        )
        
        enemy = Enemy(
            id="orc_001",
            name="Orc Warrior",
            level=2,
            health=30,
            max_health=30,
            stats={"strength": 14, "dexterity": 8, "constitution": 16}
        )
        
        # Mock AI responses for full combat
        mock_ai_client.generate_narrative.side_effect = [
            # Combat initiation
            {
                "narrative": "An orc warrior blocks your path!",
                "combat_options": ["Attack", "Defend", "Escape"]
            },
            # First attack
            {
                "narrative": "You strike the orc with your weapon!",
                "damage_dealt": 8,
                "damage_taken": 5,
                "enemy_response": "The orc retaliates!"
            },
            # Second attack
            {
                "narrative": "Your follow-up attack is decisive!",
                "damage_dealt": 12,
                "damage_taken": 0,
                "combat_ended": True,
                "victory": True
            }
        ]
        
        # Start combat
        result = await combat_resolver.initiate_combat(player, enemy, "road_encounter")
        assert result is not None
        
        # Execute combat actions
        action1 = CombatAction(type="attack", target="enemy", weapon="sword")
        result1 = await combat_resolver.resolve_action(player, enemy, action1)
        assert result1["damage_dealt"] > 0
        
        # Update health
        enemy.health -= result1["damage_dealt"]
        player.health -= result1["damage_taken"]
        
        # Final attack
        action2 = CombatAction(type="attack", target="enemy", weapon="sword")
        result2 = await combat_resolver.resolve_action(player, enemy, action2)
        
        assert result2["combat_ended"] is True
        assert result2["victory"] is True
        
        # Get final outcome
        outcome = await combat_resolver.get_combat_outcome()
        assert outcome.victory is True
        assert outcome.experience_gained > 0

    @pytest.mark.asyncio
    async def test_combat_performance(self):
        """Test combat system performance with multiple encounters"""
        import time
        
        # Setup
        mock_ai_client = Mock()
        mock_ai_client.generate_narrative = AsyncMock(return_value={
            "narrative": "Quick combat resolution",
            "damage_dealt": 5,
            "damage_taken": 2,
            "combat_ended": True,
            "victory": True
        })
        
        risk_assessment = RiskAssessment()
        combat_resolver = CombatResolver(
            ai_client=mock_ai_client,
            risk_assessment=risk_assessment
        )
        
        player = Player(
            id="speed_test",
            name="SpeedTester",
            level=5,
            experience=200,
            health=100,
            max_health=100,
            stats={"strength": 15, "dexterity": 12, "constitution": 14}
        )
        
        # Run multiple combat encounters
        start_time = time.time()
        
        for i in range(10):
            enemy = Enemy(
                id=f"enemy_{i}",
                name=f"Test Enemy {i}",
                level=3,
                health=20,
                max_health=20,
                stats={"strength": 10, "dexterity": 10, "constitution": 12}
            )
            
            await combat_resolver.initiate_combat(player, enemy, "speed_test")
            action = CombatAction(type="attack", target="enemy")
            await combat_resolver.resolve_action(player, enemy, action)
        
        total_time = time.time() - start_time
        
        # Performance assertion
        assert total_time < 5.0  # Should complete 10 combats in < 5 seconds


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 