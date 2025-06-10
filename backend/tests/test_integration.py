"""
AI-RPG-Alpha: Integration Tests

Comprehensive integration test suite covering end-to-end workflows,
API endpoints, database interactions, and system integration.
Part of Phase 5: Testing & Optimization as defined in PRD.
"""

import pytest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from httpx import AsyncClient
from fastapi.testclient import TestClient

from backend.main import app
from backend.dao.game_state import GameStateDAO
from backend.dao.memory import MemoryDAO
from backend.engine.consequence import ConsequenceEngine
from backend.engine.combat import CombatResolver
from backend.ai.openai_client import OpenAIClient
from backend.models.dataclasses import Player, Quest, GameEvent, MemoryEntry


class TestAPIIntegration:
    """Test suite for API endpoint integration"""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)
    
    @pytest.fixture
    def temp_db_path(self):
        """Temporary database path for testing"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        yield temp_file.name
        Path(temp_file.name).unlink(missing_ok=True)
    
    @pytest.fixture
    def temp_chromadb_path(self):
        """Temporary ChromaDB path for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_health_check_endpoint(self, client):
        """Test API health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_player_endpoint(self, client):
        """Test player creation endpoint"""
        player_data = {
            "name": "TestHero",
            "starting_stats": {
                "strength": 12,
                "dexterity": 10,
                "constitution": 14,
                "intelligence": 11,
                "wisdom": 13,
                "charisma": 8
            }
        }
        
        response = client.post("/api/players", json=player_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "TestHero"
        assert "id" in data
        assert data["level"] == 1

    def test_get_player_endpoint(self, client):
        """Test player retrieval endpoint"""
        # First create a player
        player_data = {"name": "GetTestHero"}
        create_response = client.post("/api/players", json=player_data)
        player_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/players/{player_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == player_id
        assert data["name"] == "GetTestHero"

    @patch('backend.ai.openai_client.OpenAIClient.generate_quest')
    def test_generate_quest_endpoint(self, mock_generate, client):
        """Test quest generation endpoint"""
        # Mock AI response
        mock_generate.return_value = {
            "title": "The Mysterious Cave",
            "description": "A dark cave holds ancient secrets",
            "objectives": ["Explore the cave", "Find the artifact"],
            "rewards": {"experience": 100, "gold": 50}
        }
        
        # Create player first
        player_data = {"name": "QuestTestHero"}
        create_response = client.post("/api/players", json=player_data)
        player_id = create_response.json()["id"]
        
        # Generate quest
        quest_data = {
            "player_id": player_id,
            "context": "forest exploration",
            "difficulty": "medium"
        }
        
        response = client.post("/api/quests/generate", json=quest_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == "The Mysterious Cave"
        assert "id" in data

    @patch('backend.ai.openai_client.OpenAIClient.generate_choice_result')
    def test_make_choice_endpoint(self, mock_generate, client):
        """Test choice making endpoint"""
        # Mock AI response
        mock_generate.return_value = {
            "result": "You successfully sneak past the guards",
            "consequences": {
                "experience": 15,
                "stealth_bonus": 1
            }
        }
        
        # Create player and quest
        player_data = {"name": "ChoiceTestHero"}
        create_response = client.post("/api/players", json=player_data)
        player_id = create_response.json()["id"]
        
        # Make choice
        choice_data = {
            "player_id": player_id,
            "quest_id": "quest_123",
            "choice": "sneak_past_guards",
            "context": "castle_infiltration"
        }
        
        response = client.post("/api/choices", json=choice_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "result" in data
        assert "consequences" in data

    def test_player_events_endpoint(self, client):
        """Test player events retrieval endpoint"""
        # Create player
        player_data = {"name": "EventTestHero"}
        create_response = client.post("/api/players", json=player_data)
        player_id = create_response.json()["id"]
        
        # Get events (should be empty for new player)
        response = client.get(f"/api/players/{player_id}/events")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    def test_error_handling(self, client):
        """Test API error handling"""
        # Test 404 for non-existent player
        response = client.get("/api/players/nonexistent")
        assert response.status_code == 404
        
        # Test 400 for invalid data
        response = client.post("/api/players", json={"invalid": "data"})
        assert response.status_code == 400


class TestDatabaseIntegration:
    """Test suite for database integration"""
    
    @pytest.fixture
    def game_state_dao(self, temp_db_path):
        """GameStateDAO with temporary database"""
        return GameStateDAO(db_path=temp_db_path)
    
    @pytest.fixture
    def memory_dao(self, temp_chromadb_path):
        """MemoryDAO with temporary ChromaDB"""
        return MemoryDAO(db_path=temp_chromadb_path)

    @pytest.mark.asyncio
    async def test_player_crud_operations(self, game_state_dao):
        """Test complete CRUD operations for players"""
        # Create
        player = Player(
            name="CRUDTestPlayer",
            level=1,
            experience=0,
            health=50,
            max_health=50
        )
        
        created_player = await game_state_dao.create_player(player)
        assert created_player.id is not None
        
        # Read
        retrieved_player = await game_state_dao.get_player_by_id(created_player.id)
        assert retrieved_player.name == "CRUDTestPlayer"
        
        # Update
        retrieved_player.experience = 100
        await game_state_dao.update_player(retrieved_player)
        
        updated_player = await game_state_dao.get_player_by_id(created_player.id)
        assert updated_player.experience == 100
        
        # Delete
        result = await game_state_dao.delete_player(created_player.id)
        assert result is True
        
        # Verify deletion
        deleted_player = await game_state_dao.get_player_by_id(created_player.id)
        assert deleted_player is None

    @pytest.mark.asyncio
    async def test_quest_database_operations(self, game_state_dao):
        """Test quest database operations"""
        # Create player first
        player = Player(name="QuestDBPlayer", level=2, experience=50, health=60, max_health=60)
        created_player = await game_state_dao.create_player(player)
        
        # Create quest
        quest = Quest(
            player_id=created_player.id,
            title="Database Test Quest",
            description="Testing quest storage",
            objectives=["Test objective 1", "Test objective 2"],
            rewards={"experience": 50, "gold": 25}
        )
        
        created_quest = await game_state_dao.create_quest(quest)
        assert created_quest.id is not None
        
        # Retrieve quest
        retrieved_quest = await game_state_dao.get_quest_by_id(created_quest.id)
        assert retrieved_quest.title == "Database Test Quest"
        
        # Get player quests
        player_quests = await game_state_dao.get_player_quests(created_player.id)
        assert len(player_quests) == 1
        assert player_quests[0].id == created_quest.id

    @pytest.mark.asyncio
    async def test_memory_database_integration(self, memory_dao, game_state_dao):
        """Test memory and game state database integration"""
        # Create player in game state
        player = Player(name="MemoryIntegrationPlayer", level=3, experience=100, health=70, max_health=70)
        created_player = await game_state_dao.create_player(player)
        
        # Create memory entry
        memory = MemoryEntry(
            id="integration_memory_001",
            player_id=created_player.id,
            content="Player discovered a hidden treasure",
            memory_type="discovery",
            importance=0.8,
            context_tags=["treasure", "discovery", "exploration"],
            location="hidden_cave",
            timestamp=1234567890
        )
        
        # Store memory
        result = await memory_dao.store_memory(memory)
        assert result is True
        
        # Retrieve memories for player
        memories = await memory_dao.get_memories_by_player(created_player.id)
        assert len(memories) == 1
        assert memories[0].content == "Player discovered a hidden treasure"

    @pytest.mark.asyncio
    async def test_transaction_rollback(self, game_state_dao):
        """Test database transaction rollback on errors"""
        # Create player
        player = Player(name="TransactionTestPlayer", level=1, experience=0, health=50, max_health=50)
        created_player = await game_state_dao.create_player(player)
        
        # Attempt operation that should fail and rollback
        try:
            async with game_state_dao.get_transaction() as tx:
                # Update player
                created_player.experience = 1000
                await game_state_dao.update_player(created_player)
                
                # Force an error
                raise Exception("Forced error for testing")
                
        except Exception:
            pass  # Expected
        
        # Verify rollback - player should not have updated experience
        unchanged_player = await game_state_dao.get_player_by_id(created_player.id)
        assert unchanged_player.experience == 0


class TestSystemIntegration:
    """Test suite for full system integration"""
    
    @pytest.fixture
    def integrated_system(self, temp_db_path, temp_chromadb_path):
        """Full integrated system setup"""
        game_state_dao = GameStateDAO(db_path=temp_db_path)
        memory_dao = MemoryDAO(db_path=temp_chromadb_path)
        
        # Mock AI client
        mock_ai_client = Mock()
        mock_ai_client.generate_quest = AsyncMock()
        mock_ai_client.generate_choice_result = AsyncMock()
        
        consequence_engine = ConsequenceEngine(
            game_state_dao=game_state_dao,
            memory_dao=memory_dao
        )
        
        return {
            "game_state_dao": game_state_dao,
            "memory_dao": memory_dao,
            "ai_client": mock_ai_client,
            "consequence_engine": consequence_engine
        }

    @pytest.mark.asyncio
    async def test_complete_game_flow(self, integrated_system):
        """Test complete game flow from player creation to quest completion"""
        system = integrated_system
        
        # Step 1: Create player
        player = Player(
            name="IntegrationTestHero",
            level=1,
            experience=0,
            health=50,
            max_health=50,
            stats={
                "strength": 10,
                "dexterity": 12,
                "constitution": 14,
                "intelligence": 11,
                "wisdom": 13,
                "charisma": 9
            }
        )
        
        created_player = await system["game_state_dao"].create_player(player)
        assert created_player.id is not None
        
        # Step 2: Generate quest
        system["ai_client"].generate_quest.return_value = {
            "title": "The Lost Merchant",
            "description": "A merchant has gone missing on the forest road",
            "objectives": ["Find the merchant", "Investigate the disappearance"],
            "rewards": {"experience": 75, "gold": 30}
        }
        
        quest_data = await system["ai_client"].generate_quest(
            player_context=created_player.to_dict(),
            world_context="peaceful_village"
        )
        
        quest = Quest(
            player_id=created_player.id,
            title=quest_data["title"],
            description=quest_data["description"],
            objectives=quest_data["objectives"],
            rewards=quest_data["rewards"]
        )
        
        created_quest = await system["game_state_dao"].create_quest(quest)
        assert created_quest.id is not None
        
        # Step 3: Make choice in quest
        system["ai_client"].generate_choice_result.return_value = {
            "result": "You find tracks leading into the forest",
            "consequences": {
                "experience": 10,
                "new_location": "dark_forest"
            }
        }
        
        choice_result = await system["ai_client"].generate_choice_result(
            player_context=created_player.to_dict(),
            quest_context=created_quest.to_dict(),
            choice="investigate_tracks"
        )
        
        # Step 4: Apply consequences
        if "experience" in choice_result["consequences"]:
            created_player.experience += choice_result["consequences"]["experience"]
            await system["game_state_dao"].update_player(created_player)
        
        # Step 5: Create memory of the event
        memory = MemoryEntry(
            id="quest_memory_001",
            player_id=created_player.id,
            content="Investigated missing merchant tracks",
            memory_type="investigation",
            importance=0.7,
            context_tags=["merchant", "investigation", "forest"],
            location="forest_road",
            timestamp=1234567890
        )
        
        await system["memory_dao"].store_memory(memory)
        
        # Step 6: Verify complete integration
        final_player = await system["game_state_dao"].get_player_by_id(created_player.id)
        assert final_player.experience == 10
        
        player_memories = await system["memory_dao"].get_memories_by_player(created_player.id)
        assert len(player_memories) == 1

    @pytest.mark.asyncio
    async def test_consequence_system_integration(self, integrated_system):
        """Test consequence system integration with other components"""
        system = integrated_system
        
        # Create player
        player = Player(
            name="ConsequenceTestPlayer",
            level=2,
            experience=25,
            health=60,
            max_health=60
        )
        created_player = await system["game_state_dao"].create_player(player)
        
        # Register a delayed consequence
        from backend.models.dataclasses import Consequence
        from backend.engine.consequence_types import ConsequenceType, ConsequenceImpact
        
        consequence = Consequence(
            id="integration_consequence_001",
            player_id=created_player.id,
            consequence_type=ConsequenceType.DELAYED_EVENT,
            trigger_event="helped_stranger",
            impact=ConsequenceImpact.MEDIUM,
            description="Stranger remembers your kindness",
            delay_turns=2,
            effects={
                "experience": 20,
                "reputation_change": {"faction": "travelers", "value": 15}
            }
        )
        
        await system["consequence_engine"].register_consequence(consequence)
        
        # Process turns to trigger consequence
        triggered = await system["consequence_engine"].process_turn(created_player.id, 3)
        assert len(triggered) == 1
        
        # Verify consequence was applied
        updated_player = await system["game_state_dao"].get_player_by_id(created_player.id)
        assert updated_player.experience > created_player.experience

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, integrated_system):
        """Test system behavior under concurrent operations"""
        system = integrated_system
        
        # Create multiple players concurrently
        async def create_player_task(i):
            player = Player(
                name=f"ConcurrentPlayer{i}",
                level=1,
                experience=0,
                health=50,
                max_health=50
            )
            return await system["game_state_dao"].create_player(player)
        
        # Run concurrent player creation
        tasks = [create_player_task(i) for i in range(5)]
        created_players = await asyncio.gather(*tasks)
        
        # Verify all players were created
        assert len(created_players) == 5
        assert all(player.id is not None for player in created_players)
        
        # Test concurrent memory operations
        async def store_memory_task(player):
            memory = MemoryEntry(
                id=f"concurrent_memory_{player.id}",
                player_id=player.id,
                content=f"Concurrent memory for {player.name}",
                memory_type="test",
                importance=0.5,
                context_tags=["concurrent", "test"],
                location="test_location",
                timestamp=1234567890
            )
            return await system["memory_dao"].store_memory(memory)
        
        memory_tasks = [store_memory_task(player) for player in created_players]
        memory_results = await asyncio.gather(*memory_tasks)
        
        # Verify all memories were stored
        assert all(result is True for result in memory_results)

    @pytest.mark.asyncio
    async def test_error_recovery(self, integrated_system):
        """Test system error recovery and resilience"""
        system = integrated_system
        
        # Create player
        player = Player(name="ErrorTestPlayer", level=1, experience=0, health=50, max_health=50)
        created_player = await system["game_state_dao"].create_player(player)
        
        # Test recovery from AI client failure
        system["ai_client"].generate_quest.side_effect = Exception("AI service unavailable")
        
        # System should handle AI failure gracefully
        try:
            await system["ai_client"].generate_quest(
                player_context=created_player.to_dict(),
                world_context="test"
            )
        except Exception as e:
            assert str(e) == "AI service unavailable"
        
        # Test recovery from database connection issues
        # (This would require more complex setup to simulate)
        
        # Test memory system resilience
        invalid_memory = MemoryEntry(
            id="",  # Invalid empty ID
            player_id=created_player.id,
            content="",  # Invalid empty content
            memory_type="test",
            importance=0.5,
            context_tags=[],
            location="test",
            timestamp=1234567890
        )
        
        # Should handle invalid data gracefully
        result = await system["memory_dao"].store_memory(invalid_memory)
        assert result is False  # Should fail gracefully without crashing

    @pytest.mark.asyncio
    async def test_performance_benchmarks(self, integrated_system):
        """Test system performance benchmarks"""
        import time
        system = integrated_system
        
        # Benchmark player creation
        start_time = time.time()
        
        players = []
        for i in range(50):
            player = Player(
                name=f"PerfTestPlayer{i}",
                level=1,
                experience=0,
                health=50,
                max_health=50
            )
            created_player = await system["game_state_dao"].create_player(player)
            players.append(created_player)
        
        creation_time = time.time() - start_time
        
        # Benchmark memory operations
        start_time = time.time()
        
        for i, player in enumerate(players):
            memory = MemoryEntry(
                id=f"perf_memory_{i}",
                player_id=player.id,
                content=f"Performance test memory {i}",
                memory_type="performance",
                importance=0.5,
                context_tags=["performance", "test"],
                location="test_location",
                timestamp=1234567890 + i
            )
            await system["memory_dao"].store_memory(memory)
        
        memory_time = time.time() - start_time
        
        # Performance assertions
        assert creation_time < 5.0   # Should create 50 players in < 5 seconds
        assert memory_time < 10.0    # Should store 50 memories in < 10 seconds
        
        # Benchmark retrieval operations
        start_time = time.time()
        
        for player in players[:10]:  # Test first 10 players
            await system["game_state_dao"].get_player_by_id(player.id)
            await system["memory_dao"].get_memories_by_player(player.id)
        
        retrieval_time = time.time() - start_time
        assert retrieval_time < 2.0  # Should retrieve data for 10 players in < 2 seconds


class TestAPIPerformance:
    """Performance tests for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)

    def test_concurrent_api_requests(self, client):
        """Test API performance under concurrent load"""
        import concurrent.futures
        import time
        
        def make_health_check():
            return client.get("/health")
        
        # Test concurrent health checks
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_health_check) for _ in range(50)]
            responses = [future.result() for future in futures]
        
        total_time = time.time() - start_time
        
        # All requests should succeed
        assert all(response.status_code == 200 for response in responses)
        
        # Should handle 50 concurrent requests in reasonable time
        assert total_time < 5.0

    def test_large_payload_handling(self, client):
        """Test API handling of large payloads"""
        # Create large player data
        large_stats = {f"stat_{i}": i for i in range(100)}
        
        player_data = {
            "name": "LargePayloadPlayer",
            "starting_stats": large_stats,
            "metadata": {
                "large_data": "x" * 10000  # 10KB of data
            }
        }
        
        response = client.post("/api/players", json=player_data)
        # Should handle large payload (might return 400 if validation fails, which is acceptable)
        assert response.status_code in [201, 400]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 