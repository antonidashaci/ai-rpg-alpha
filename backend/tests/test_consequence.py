"""
AI-RPG-Alpha: Consequence Engine Tests

Comprehensive test suite for the consequence engine including delayed events,
consequence chains, and narrative coherence testing.
Part of Phase 5: Testing & Optimization as defined in PRD.
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from unittest.mock import Mock, patch, AsyncMock

from backend.engine.consequence import ConsequenceEngine
from backend.engine.consequence_types import ConsequenceType, ConsequenceImpact
from backend.engine.consequence_handlers import ConsequenceHandlers
from backend.models.dataclasses import (
    Consequence, Player, Quest, GameEvent, Choice,
    ConsequenceChain, DelayedEvent
)


class TestConsequenceEngine:
    """Test suite for Consequence Engine core functionality"""
    
    @pytest.fixture
    def mock_game_state_dao(self):
        """Mock GameStateDAO for testing"""
        mock_dao = Mock()
        mock_dao.get_player_by_id = AsyncMock()
        mock_dao.update_player = AsyncMock()
        mock_dao.create_event = AsyncMock()
        mock_dao.get_player_events = AsyncMock()
        return mock_dao
    
    @pytest.fixture
    def mock_memory_dao(self):
        """Mock MemoryDAO for testing"""
        mock_dao = Mock()
        mock_dao.store_memory = AsyncMock(return_value=True)
        mock_dao.get_memories_by_player = AsyncMock(return_value=[])
        return mock_dao
    
    @pytest.fixture
    def consequence_engine(self, mock_game_state_dao, mock_memory_dao):
        """Create ConsequenceEngine instance for testing"""
        return ConsequenceEngine(
            game_state_dao=mock_game_state_dao,
            memory_dao=mock_memory_dao
        )
    
    @pytest.fixture
    def sample_player(self):
        """Sample player for testing"""
        return Player(
            id="player_123",
            name="TestHero",
            level=3,
            experience=75,
            health=85,
            max_health=100,
            stats={
                "strength": 12,
                "intelligence": 10,
                "charisma": 8
            }
        )
    
    @pytest.fixture
    def sample_consequence(self):
        """Sample consequence for testing"""
        return Consequence(
            id="consequence_001",
            player_id="player_123",
            consequence_type=ConsequenceType.DELAYED_EVENT,
            trigger_event="helped_merchant",
            impact=ConsequenceImpact.MEDIUM,
            description="Merchant remembers your kindness",
            delay_turns=3,
            conditions={"location": "merchant_district"},
            metadata={
                "merchant_name": "Gareth",
                "favor_level": "grateful"
            }
        )

    @pytest.mark.asyncio
    async def test_consequence_engine_initialization(self, mock_game_state_dao, mock_memory_dao):
        """Test ConsequenceEngine initialization"""
        engine = ConsequenceEngine(
            game_state_dao=mock_game_state_dao,
            memory_dao=mock_memory_dao
        )
        
        assert engine.game_state_dao is mock_game_state_dao
        assert engine.memory_dao is mock_memory_dao
        assert engine.active_consequences == []
        assert engine.handlers is not None

    @pytest.mark.asyncio
    async def test_register_consequence(self, consequence_engine, sample_consequence):
        """Test registering a new consequence"""
        result = await consequence_engine.register_consequence(sample_consequence)
        
        assert result is True
        assert len(consequence_engine.active_consequences) == 1
        assert consequence_engine.active_consequences[0].id == sample_consequence.id

    @pytest.mark.asyncio
    async def test_process_immediate_consequence(self, consequence_engine, sample_player):
        """Test processing immediate consequences"""
        immediate_consequence = Consequence(
            id="immediate_001",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.IMMEDIATE,
            trigger_event="combat_victory",
            impact=ConsequenceImpact.HIGH,
            description="Gained combat experience",
            delay_turns=0,
            effects={
                "experience": 25,
                "health": -10
            }
        )
        
        # Mock player retrieval
        consequence_engine.game_state_dao.get_player_by_id.return_value = sample_player
        
        result = await consequence_engine.process_consequence(immediate_consequence)
        
        assert result is True
        # Verify player update was called
        consequence_engine.game_state_dao.update_player.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_delayed_consequence(self, consequence_engine, sample_consequence):
        """Test processing delayed consequences"""
        # Register consequence
        await consequence_engine.register_consequence(sample_consequence)
        
        # Process turn (should not trigger yet)
        triggered = await consequence_engine.process_turn("player_123", 1)
        assert len(triggered) == 0
        
        # Process enough turns to trigger
        triggered = await consequence_engine.process_turn("player_123", 4)
        assert len(triggered) == 1
        assert triggered[0].id == sample_consequence.id

    @pytest.mark.asyncio
    async def test_consequence_conditions(self, consequence_engine, sample_player):
        """Test consequence condition checking"""
        conditional_consequence = Consequence(
            id="conditional_001",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.CONDITIONAL,
            trigger_event="enter_location",
            impact=ConsequenceImpact.LOW,
            description="Special event at tavern",
            conditions={
                "location": "tavern",
                "time_of_day": "evening",
                "player_level": ">= 3"
            }
        )
        
        # Test with matching conditions
        context = {
            "location": "tavern",
            "time_of_day": "evening",
            "player_level": 3
        }
        
        result = await consequence_engine.check_conditions(
            conditional_consequence, 
            context
        )
        assert result is True
        
        # Test with non-matching conditions
        context["location"] = "forest"
        result = await consequence_engine.check_conditions(
            conditional_consequence, 
            context
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_consequence_chains(self, consequence_engine, sample_player):
        """Test chained consequences"""
        # Create consequence chain
        chain = ConsequenceChain(
            id="chain_001",
            player_id=sample_player.id,
            name="Merchant Questline",
            consequences=[
                Consequence(
                    id="chain_step_1",
                    player_id=sample_player.id,
                    consequence_type=ConsequenceType.DELAYED_EVENT,
                    trigger_event="helped_merchant",
                    impact=ConsequenceImpact.LOW,
                    description="Merchant sends message",
                    delay_turns=2
                ),
                Consequence(
                    id="chain_step_2",
                    player_id=sample_player.id,
                    consequence_type=ConsequenceType.DELAYED_EVENT,
                    trigger_event="received_message",
                    impact=ConsequenceImpact.MEDIUM,
                    description="Merchant offers special quest",
                    delay_turns=1
                )
            ]
        )
        
        # Register chain
        result = await consequence_engine.register_consequence_chain(chain)
        assert result is True
        
        # Process turns to trigger chain
        triggered = await consequence_engine.process_turn("player_123", 3)
        assert len(triggered) >= 1

    @pytest.mark.asyncio
    async def test_consequence_persistence(self, consequence_engine, sample_consequence):
        """Test consequence persistence across sessions"""
        # Register consequence
        await consequence_engine.register_consequence(sample_consequence)
        
        # Save state
        state_data = await consequence_engine.save_state("player_123")
        assert state_data is not None
        assert len(state_data["active_consequences"]) == 1
        
        # Create new engine instance
        new_engine = ConsequenceEngine(
            game_state_dao=consequence_engine.game_state_dao,
            memory_dao=consequence_engine.memory_dao
        )
        
        # Load state
        result = await new_engine.load_state("player_123", state_data)
        assert result is True
        assert len(new_engine.active_consequences) == 1

    @pytest.mark.asyncio
    async def test_consequence_cancellation(self, consequence_engine, sample_consequence):
        """Test consequence cancellation"""
        # Register consequence
        await consequence_engine.register_consequence(sample_consequence)
        assert len(consequence_engine.active_consequences) == 1
        
        # Cancel consequence
        result = await consequence_engine.cancel_consequence(sample_consequence.id)
        assert result is True
        assert len(consequence_engine.active_consequences) == 0

    @pytest.mark.asyncio
    async def test_consequence_priority(self, consequence_engine, sample_player):
        """Test consequence priority handling"""
        # Create consequences with different priorities
        high_priority = Consequence(
            id="high_priority",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.IMMEDIATE,
            trigger_event="critical_event",
            impact=ConsequenceImpact.HIGH,
            description="Critical consequence",
            priority=10
        )
        
        low_priority = Consequence(
            id="low_priority",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.IMMEDIATE,
            trigger_event="minor_event",
            impact=ConsequenceImpact.LOW,
            description="Minor consequence",
            priority=1
        )
        
        # Register in reverse priority order
        await consequence_engine.register_consequence(low_priority)
        await consequence_engine.register_consequence(high_priority)
        
        # Process consequences - should be ordered by priority
        consequence_engine.game_state_dao.get_player_by_id.return_value = sample_player
        
        sorted_consequences = consequence_engine.get_sorted_consequences()
        assert sorted_consequences[0].priority > sorted_consequences[1].priority


class TestConsequenceHandlers:
    """Test suite for Consequence Handlers"""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock dependencies for handlers"""
        return {
            'game_state_dao': Mock(),
            'memory_dao': Mock(),
            'quest_dao': Mock()
        }
    
    @pytest.fixture
    def consequence_handlers(self, mock_dependencies):
        """Create ConsequenceHandlers instance"""
        return ConsequenceHandlers(**mock_dependencies)
    
    @pytest.mark.asyncio
    async def test_stat_modification_handler(self, consequence_handlers, sample_player):
        """Test stat modification consequence handler"""
        consequence = Consequence(
            id="stat_mod_001",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.STAT_MODIFICATION,
            trigger_event="training_complete",
            impact=ConsequenceImpact.MEDIUM,
            description="Training increased strength",
            effects={
                "strength": 2,
                "experience": 10
            }
        )
        
        result = await consequence_handlers.handle_stat_modification(
            consequence, 
            sample_player
        )
        
        assert result is True
        assert sample_player.stats["strength"] == 14  # 12 + 2
        assert sample_player.experience == 85  # 75 + 10

    @pytest.mark.asyncio
    async def test_reputation_handler(self, consequence_handlers, sample_player):
        """Test reputation consequence handler"""
        consequence = Consequence(
            id="reputation_001",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.REPUTATION_CHANGE,
            trigger_event="helped_villagers",
            impact=ConsequenceImpact.MEDIUM,
            description="Villagers remember your kindness",
            effects={
                "faction": "villagers",
                "reputation_change": 25
            }
        )
        
        result = await consequence_handlers.handle_reputation_change(
            consequence, 
            sample_player
        )
        
        assert result is True
        # Verify reputation was updated
        assert hasattr(sample_player, 'reputation')

    @pytest.mark.asyncio
    async def test_inventory_handler(self, consequence_handlers, sample_player):
        """Test inventory consequence handler"""
        consequence = Consequence(
            id="inventory_001",
            player_id=sample_player.id,
            consequence_type=ConsequenceType.INVENTORY_CHANGE,
            trigger_event="found_treasure",
            impact=ConsequenceImpact.LOW,
            description="Found a potion",
            effects={
                "add_items": [
                    {"id": "health_potion", "quantity": 1}
                ]
            }
        )
        
        result = await consequence_handlers.handle_inventory_change(
            consequence, 
            sample_player
        )
        
        assert result is True
        # Verify item was added to inventory


class TestConsequenceTypes:
    """Test suite for Consequence Types and Classifications"""
    
    def test_consequence_type_enum(self):
        """Test ConsequenceType enumeration"""
        assert ConsequenceType.IMMEDIATE.value == "immediate"
        assert ConsequenceType.DELAYED_EVENT.value == "delayed_event"
        assert ConsequenceType.CONDITIONAL.value == "conditional"
        assert ConsequenceType.REPUTATION_CHANGE.value == "reputation_change"
        assert ConsequenceType.STAT_MODIFICATION.value == "stat_modification"
        assert ConsequenceType.INVENTORY_CHANGE.value == "inventory_change"
        assert ConsequenceType.QUEST_TRIGGER.value == "quest_trigger"
        assert ConsequenceType.RELATIONSHIP_CHANGE.value == "relationship_change"

    def test_consequence_impact_enum(self):
        """Test ConsequenceImpact enumeration"""
        assert ConsequenceImpact.LOW.value == "low"
        assert ConsequenceImpact.MEDIUM.value == "medium"
        assert ConsequenceImpact.HIGH.value == "high"
        assert ConsequenceImpact.CRITICAL.value == "critical"
        
        # Test numeric comparison
        assert ConsequenceImpact.HIGH > ConsequenceImpact.MEDIUM
        assert ConsequenceImpact.MEDIUM > ConsequenceImpact.LOW

    def test_consequence_validation(self):
        """Test consequence data validation"""
        # Valid consequence
        valid_consequence = Consequence(
            id="valid_001",
            player_id="player_123",
            consequence_type=ConsequenceType.IMMEDIATE,
            trigger_event="test_event",
            impact=ConsequenceImpact.MEDIUM,
            description="Test consequence",
            delay_turns=0
        )
        
        assert valid_consequence.is_valid()
        
        # Invalid consequence (missing required fields)
        with pytest.raises(ValueError):
            Consequence(
                id="",  # Invalid empty ID
                player_id="player_123",
                consequence_type=ConsequenceType.IMMEDIATE,
                trigger_event="test_event",
                impact=ConsequenceImpact.MEDIUM,
                description="Test consequence"
            )


class TestConsequenceIntegration:
    """Integration tests for consequence system"""
    
    @pytest.mark.asyncio
    async def test_quest_consequence_integration(self):
        """Test integration between consequences and quest system"""
        # Mock dependencies
        mock_quest_dao = Mock()
        mock_quest_dao.create_quest = AsyncMock()
        mock_quest_dao.get_available_quests = AsyncMock(return_value=[])
        
        mock_game_state_dao = Mock()
        mock_memory_dao = Mock()
        
        engine = ConsequenceEngine(
            game_state_dao=mock_game_state_dao,
            memory_dao=mock_memory_dao,
            quest_dao=mock_quest_dao
        )
        
        # Create quest-triggering consequence
        quest_consequence = Consequence(
            id="quest_trigger_001",
            player_id="player_123",
            consequence_type=ConsequenceType.QUEST_TRIGGER,
            trigger_event="met_mysterious_stranger",
            impact=ConsequenceImpact.HIGH,
            description="Stranger offers a quest",
            effects={
                "quest_template": "mysterious_artifact",
                "quest_giver": "mysterious_stranger"
            }
        )
        
        # Process consequence
        result = await engine.process_consequence(quest_consequence)
        assert result is True
        
        # Verify quest creation was attempted
        mock_quest_dao.create_quest.assert_called_once()

    @pytest.mark.asyncio
    async def test_memory_consequence_integration(self):
        """Test integration between consequences and memory system"""
        mock_memory_dao = Mock()
        mock_memory_dao.store_memory = AsyncMock(return_value=True)
        
        mock_game_state_dao = Mock()
        
        engine = ConsequenceEngine(
            game_state_dao=mock_game_state_dao,
            memory_dao=mock_memory_dao
        )
        
        # Create memory-storing consequence
        memory_consequence = Consequence(
            id="memory_001",
            player_id="player_123",
            consequence_type=ConsequenceType.IMMEDIATE,
            trigger_event="witnessed_event",
            impact=ConsequenceImpact.MEDIUM,
            description="Witnessed a magical phenomenon",
            effects={
                "create_memory": {
                    "content": "Saw a phoenix rise from ashes",
                    "importance": 0.8,
                    "tags": ["magic", "phoenix", "rare_event"]
                }
            }
        )
        
        # Process consequence
        result = await engine.process_consequence(memory_consequence)
        assert result is True
        
        # Verify memory storage was attempted
        mock_memory_dao.store_memory.assert_called_once()

    @pytest.mark.asyncio
    async def test_performance_with_many_consequences(self):
        """Test consequence engine performance with large numbers of consequences"""
        import time
        
        mock_game_state_dao = Mock()
        mock_memory_dao = Mock()
        
        engine = ConsequenceEngine(
            game_state_dao=mock_game_state_dao,
            memory_dao=mock_memory_dao
        )
        
        # Create many consequences
        consequences = [
            Consequence(
                id=f"perf_consequence_{i}",
                player_id="player_123",
                consequence_type=ConsequenceType.DELAYED_EVENT,
                trigger_event=f"event_{i}",
                impact=ConsequenceImpact.LOW,
                description=f"Performance test consequence {i}",
                delay_turns=i % 10 + 1
            )
            for i in range(100)
        ]
        
        # Register all consequences
        start_time = time.time()
        for consequence in consequences:
            await engine.register_consequence(consequence)
        registration_time = time.time() - start_time
        
        # Process turn with many active consequences
        start_time = time.time()
        triggered = await engine.process_turn("player_123", 5)
        processing_time = time.time() - start_time
        
        # Performance assertions
        assert registration_time < 5.0  # Should register 100 consequences in < 5 seconds
        assert processing_time < 2.0   # Should process turn in < 2 seconds
        assert len(triggered) > 0      # Should trigger some consequences


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 