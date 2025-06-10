"""
AI-RPG-Alpha: Memory System Tests

Comprehensive test suite for the memory system including ChromaDB integration,
vector operations, and context retrieval functionality.
Part of Phase 5: Testing & Optimization as defined in PRD.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import Mock, patch, AsyncMock

from backend.dao.memory import MemoryDAO
from backend.models.dataclasses import (
    MemoryEntry, Player, Quest, GameEvent, 
    ContextualMemory, MemorySearchResult
)


class TestMemoryDAO:
    """Test suite for Memory Data Access Object"""
    
    @pytest.fixture
    def temp_chromadb_path(self):
        """Create temporary ChromaDB path for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def memory_dao(self, temp_chromadb_path):
        """Create MemoryDAO instance for testing"""
        return MemoryDAO(db_path=temp_chromadb_path)
    
    @pytest.fixture
    def sample_memory_entry(self):
        """Sample memory entry for testing"""
        return MemoryEntry(
            id="test_memory_001",
            player_id="player_123",
            content="The hero rescued a merchant from bandits",
            memory_type="action",
            importance=0.8,
            context_tags=["combat", "merchant", "rescue"],
            location="forest_path",
            timestamp=1234567890
        )
    
    @pytest.fixture
    def sample_player(self):
        """Sample player for testing"""
        return Player(
            id="player_123",
            name="TestHero",
            level=5,
            experience=150,
            health=80,
            max_health=100
        )

    def test_memory_dao_initialization(self, temp_chromadb_path):
        """Test MemoryDAO initialization and database connection"""
        dao = MemoryDAO(db_path=temp_chromadb_path)
        assert dao is not None
        assert dao.client is not None
        assert dao.collection is not None

    @pytest.mark.asyncio
    async def test_store_memory_success(self, memory_dao, sample_memory_entry):
        """Test successful memory storage"""
        result = await memory_dao.store_memory(sample_memory_entry)
        
        assert result is True
        
        # Verify memory was stored by retrieving it
        memories = await memory_dao.get_memories_by_player(
            sample_memory_entry.player_id
        )
        assert len(memories) == 1
        assert memories[0].content == sample_memory_entry.content

    @pytest.mark.asyncio
    async def test_store_memory_duplicate_handling(self, memory_dao, sample_memory_entry):
        """Test handling of duplicate memory entries"""
        # Store same memory twice
        await memory_dao.store_memory(sample_memory_entry)
        result = await memory_dao.store_memory(sample_memory_entry)
        
        # Should handle gracefully
        assert result is True
        
        # Should not create duplicates
        memories = await memory_dao.get_memories_by_player(
            sample_memory_entry.player_id
        )
        assert len(memories) == 1

    @pytest.mark.asyncio
    async def test_get_memories_by_player(self, memory_dao, sample_player):
        """Test retrieving memories for a specific player"""
        # Store multiple memories for the player
        memories = [
            MemoryEntry(
                id=f"memory_{i}",
                player_id=sample_player.id,
                content=f"Test memory {i}",
                memory_type="action",
                importance=0.5 + i * 0.1,
                context_tags=[f"tag_{i}"],
                location="test_location",
                timestamp=1234567890 + i
            )
            for i in range(3)
        ]
        
        for memory in memories:
            await memory_dao.store_memory(memory)
        
        # Retrieve memories
        retrieved = await memory_dao.get_memories_by_player(sample_player.id)
        
        assert len(retrieved) == 3
        # Should be sorted by importance (descending)
        assert retrieved[0].importance >= retrieved[1].importance

    @pytest.mark.asyncio
    async def test_search_similar_memories(self, memory_dao, sample_memory_entry):
        """Test semantic search for similar memories"""
        # Store a memory
        await memory_dao.store_memory(sample_memory_entry)
        
        # Search for similar content
        results = await memory_dao.search_similar_memories(
            player_id=sample_memory_entry.player_id,
            query="hero helped merchant",
            limit=5
        )
        
        assert len(results) > 0
        assert isinstance(results[0], MemorySearchResult)
        assert results[0].memory.content == sample_memory_entry.content
        assert 0 <= results[0].similarity_score <= 1

    @pytest.mark.asyncio
    async def test_get_contextual_memories(self, memory_dao, sample_player):
        """Test retrieval of contextually relevant memories"""
        # Store memories with different contexts
        context_memories = [
            MemoryEntry(
                id="combat_memory",
                player_id=sample_player.id,
                content="Fought a dragon",
                memory_type="combat",
                importance=0.9,
                context_tags=["combat", "dragon"],
                location="mountain_peak",
                timestamp=1234567890
            ),
            MemoryEntry(
                id="dialogue_memory",
                player_id=sample_player.id,
                content="Talked with wise sage",
                memory_type="dialogue",
                importance=0.7,
                context_tags=["dialogue", "sage", "wisdom"],
                location="ancient_library",
                timestamp=1234567891
            )
        ]
        
        for memory in context_memories:
            await memory_dao.store_memory(memory)
        
        # Get contextual memories for combat situation
        contextual = await memory_dao.get_contextual_memories(
            player_id=sample_player.id,
            current_context=["combat", "danger"],
            limit=10
        )
        
        assert len(contextual) > 0
        # Combat memory should be more relevant
        combat_memory = next(
            (cm for cm in contextual if cm.memory.memory_type == "combat"), 
            None
        )
        assert combat_memory is not None

    @pytest.mark.asyncio
    async def test_update_memory_importance(self, memory_dao, sample_memory_entry):
        """Test updating memory importance scores"""
        # Store memory
        await memory_dao.store_memory(sample_memory_entry)
        
        # Update importance
        new_importance = 0.95
        result = await memory_dao.update_memory_importance(
            sample_memory_entry.id,
            new_importance
        )
        
        assert result is True
        
        # Verify update
        memories = await memory_dao.get_memories_by_player(
            sample_memory_entry.player_id
        )
        assert memories[0].importance == new_importance

    @pytest.mark.asyncio
    async def test_delete_memory(self, memory_dao, sample_memory_entry):
        """Test memory deletion"""
        # Store memory
        await memory_dao.store_memory(sample_memory_entry)
        
        # Verify it exists
        memories = await memory_dao.get_memories_by_player(
            sample_memory_entry.player_id
        )
        assert len(memories) == 1
        
        # Delete memory
        result = await memory_dao.delete_memory(sample_memory_entry.id)
        assert result is True
        
        # Verify deletion
        memories = await memory_dao.get_memories_by_player(
            sample_memory_entry.player_id
        )
        assert len(memories) == 0

    @pytest.mark.asyncio
    async def test_memory_cleanup(self, memory_dao, sample_player):
        """Test automatic cleanup of old/low-importance memories"""
        # Store many memories
        memories = [
            MemoryEntry(
                id=f"cleanup_memory_{i}",
                player_id=sample_player.id,
                content=f"Low importance memory {i}",
                memory_type="action",
                importance=0.1,  # Very low importance
                context_tags=[f"tag_{i}"],
                location="test_location",
                timestamp=1234567890 - i * 86400  # Older timestamps
            )
            for i in range(20)  # Store 20 memories
        ]
        
        for memory in memories:
            await memory_dao.store_memory(memory)
        
        # Perform cleanup (keep only top 10)
        result = await memory_dao.cleanup_memories(
            player_id=sample_player.id,
            max_memories=10
        )
        
        assert result is True
        
        # Verify cleanup worked
        remaining = await memory_dao.get_memories_by_player(sample_player.id)
        assert len(remaining) <= 10

    def test_memory_entry_validation(self):
        """Test MemoryEntry data validation"""
        # Valid memory entry
        valid_memory = MemoryEntry(
            id="valid_memory",
            player_id="player_123",
            content="Valid memory content",
            memory_type="action",
            importance=0.8,
            context_tags=["tag1", "tag2"],
            location="test_location",
            timestamp=1234567890
        )
        assert valid_memory.id == "valid_memory"
        assert valid_memory.importance == 0.8
        
        # Test importance bounds
        with pytest.raises(ValueError):
            MemoryEntry(
                id="invalid_memory",
                player_id="player_123",
                content="Invalid memory",
                memory_type="action",
                importance=1.5,  # Invalid: > 1.0
                context_tags=[],
                location="test_location",
                timestamp=1234567890
            )

    @pytest.mark.asyncio
    async def test_memory_search_performance(self, memory_dao, sample_player):
        """Test memory search performance with large dataset"""
        # Store large number of memories
        import time
        
        memories = [
            MemoryEntry(
                id=f"perf_memory_{i}",
                player_id=sample_player.id,
                content=f"Performance test memory {i} with various content",
                memory_type="action",
                importance=0.5,
                context_tags=[f"perf_{i % 10}"],
                location="test_location",
                timestamp=1234567890 + i
            )
            for i in range(100)
        ]
        
        # Batch store memories
        start_time = time.time()
        for memory in memories:
            await memory_dao.store_memory(memory)
        store_time = time.time() - start_time
        
        # Test search performance
        start_time = time.time()
        results = await memory_dao.search_similar_memories(
            player_id=sample_player.id,
            query="performance test content",
            limit=10
        )
        search_time = time.time() - start_time
        
        # Performance assertions
        assert store_time < 10.0  # Should store 100 memories in < 10 seconds
        assert search_time < 1.0  # Should search in < 1 second
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_concurrent_memory_operations(self, memory_dao, sample_player):
        """Test thread-safety of concurrent memory operations"""
        import asyncio
        
        async def store_memory_task(i):
            memory = MemoryEntry(
                id=f"concurrent_memory_{i}",
                player_id=sample_player.id,
                content=f"Concurrent memory {i}",
                memory_type="action",
                importance=0.5,
                context_tags=[f"concurrent_{i}"],
                location="test_location",
                timestamp=1234567890 + i
            )
            return await memory_dao.store_memory(memory)
        
        # Run concurrent operations
        tasks = [store_memory_task(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        assert all(results)
        
        # Verify all memories were stored
        memories = await memory_dao.get_memories_by_player(sample_player.id)
        assert len(memories) == 10

    @pytest.mark.asyncio
    async def test_memory_error_handling(self, memory_dao):
        """Test error handling in memory operations"""
        # Test with invalid player ID
        with pytest.raises(ValueError):
            await memory_dao.get_memories_by_player("")
        
        # Test with invalid memory data
        invalid_memory = MemoryEntry(
            id="",  # Invalid empty ID
            player_id="player_123",
            content="",  # Invalid empty content
            memory_type="action",
            importance=0.5,
            context_tags=[],
            location="test_location",
            timestamp=1234567890
        )
        
        result = await memory_dao.store_memory(invalid_memory)
        assert result is False  # Should fail gracefully

    @pytest.mark.asyncio
    async def test_memory_context_building(self, memory_dao, sample_player):
        """Test building context from memories for AI prompts"""
        # Store varied memories
        memories = [
            MemoryEntry(
                id="context_memory_1",
                player_id=sample_player.id,
                content="Found a magical sword in ancient ruins",
                memory_type="discovery",
                importance=0.9,
                context_tags=["weapon", "magic", "ruins"],
                location="ancient_ruins",
                timestamp=1234567890
            ),
            MemoryEntry(
                id="context_memory_2",
                player_id=sample_player.id,
                content="Made alliance with dwarf king",
                memory_type="social",
                importance=0.8,
                context_tags=["alliance", "dwarf", "politics"],
                location="mountain_kingdom",
                timestamp=1234567891
            )
        ]
        
        for memory in memories:
            await memory_dao.store_memory(memory)
        
        # Build context
        context = await memory_dao.build_context_for_ai(
            player_id=sample_player.id,
            current_situation="entering a dangerous dungeon",
            max_context_length=500
        )
        
        assert context is not None
        assert len(context) > 0
        assert "magical sword" in context or "dwarf king" in context


class TestMemoryIntegration:
    """Integration tests for memory system with other components"""
    
    @pytest.fixture
    def mock_game_state_dao(self):
        """Mock GameStateDAO for integration testing"""
        mock_dao = Mock()
        mock_dao.get_player_by_id = AsyncMock()
        mock_dao.get_player_events = AsyncMock()
        return mock_dao
    
    @pytest.mark.asyncio
    async def test_memory_game_state_integration(self, temp_chromadb_path, mock_game_state_dao):
        """Test integration between memory system and game state"""
        memory_dao = MemoryDAO(db_path=temp_chromadb_path)
        
        # Mock game state data
        mock_game_state_dao.get_player_by_id.return_value = Player(
            id="player_123",
            name="TestHero",
            level=5,
            experience=150,
            health=80,
            max_health=100
        )
        
        # Test memory creation from game events
        game_event = GameEvent(
            id="event_001",
            player_id="player_123",
            event_type="quest_completion",
            description="Completed rescue mission",
            location="forest_village",
            timestamp=1234567890
        )
        
        # Convert game event to memory
        memory = MemoryEntry.from_game_event(game_event)
        result = await memory_dao.store_memory(memory)
        
        assert result is True
        
        # Verify memory was created correctly
        memories = await memory_dao.get_memories_by_player("player_123")
        assert len(memories) == 1
        assert "rescue mission" in memories[0].content


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 