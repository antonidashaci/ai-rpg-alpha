"""
AI-RPG-Alpha: Test Suite for Database Seeding

Tests for the database seeding functionality to ensure quest data
is properly loaded and stored in the SQLite database.
"""

import pytest
import tempfile
import os
import json
from pathlib import Path

# Import the modules to test
import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from data.seed_db import DatabaseSeeder
from dao.game_state import GameStateDAO
from models.dataclasses import Quest, RiskLevel, QuestStatus

class TestDatabaseSeeder:
    """Test cases for the DatabaseSeeder class."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        yield db_path
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def sample_quest_data(self):
        """Sample quest data for testing."""
        return [
            {
                "id": "test_quest_1",
                "title": "Test Quest One",
                "location": "test_location",
                "tags": ["test", "combat"],
                "intro": "This is a test quest introduction.",
                "objectives": ["Complete objective 1", "Complete objective 2"],
                "success": "You succeeded in the test quest!",
                "failure": "You failed the test quest.",
                "reward": {
                    "gold": 100,
                    "items": ["Test Sword"],
                    "experience": 50
                },
                "risk": "combat",
                "consequence_thread": {
                    "trigger_turn": 5,
                    "event": "test_consequence",
                    "description": "A test consequence occurs"
                }
            },
            {
                "id": "test_quest_2",
                "title": "Test Quest Two",
                "location": "test_location_2",
                "tags": ["test", "mystery"],
                "intro": "This is another test quest.",
                "objectives": ["Investigate the mystery"],
                "success": "Mystery solved!",
                "failure": "Mystery remains unsolved.",
                "reward": {
                    "gold": 75,
                    "items": ["Magnifying Glass"],
                    "experience": 40
                },
                "risk": "mystery"
            }
        ]
    
    @pytest.fixture
    def temp_quest_file(self, sample_quest_data):
        """Create a temporary quest data file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_quest_data, f)
            quest_file_path = f.name
        
        yield quest_file_path
        
        # Cleanup
        if os.path.exists(quest_file_path):
            os.unlink(quest_file_path)
    
    def test_database_seeder_initialization(self, temp_db):
        """Test that DatabaseSeeder initializes correctly."""
        seeder = DatabaseSeeder(temp_db)
        
        assert seeder.db_path == temp_db
        assert isinstance(seeder.dao, GameStateDAO)
        assert seeder.data_dir.exists()
    
    def test_json_to_quest_conversion(self, temp_db, sample_quest_data):
        """Test conversion of JSON data to Quest objects."""
        seeder = DatabaseSeeder(temp_db)
        quest_json = sample_quest_data[0]
        
        quest = seeder._json_to_quest(quest_json)
        
        assert isinstance(quest, Quest)
        assert quest.id == "test_quest_1"
        assert quest.title == "Test Quest One"
        assert quest.location == "test_location"
        assert quest.tags == ["test", "combat"]
        assert quest.risk == RiskLevel.COMBAT
        assert quest.status == QuestStatus.AVAILABLE
        assert quest.reward.gold == 100
        assert quest.reward.items == ["Test Sword"]
        assert quest.reward.experience == 50
        assert quest.consequence_thread is not None
        assert quest.consequence_thread.trigger_turn == 5
    
    def test_json_to_quest_without_consequence(self, temp_db, sample_quest_data):
        """Test conversion of JSON data without consequence thread."""
        seeder = DatabaseSeeder(temp_db)
        quest_json = sample_quest_data[1]  # This one has no consequence_thread
        
        quest = seeder._json_to_quest(quest_json)
        
        assert isinstance(quest, Quest)
        assert quest.id == "test_quest_2"
        assert quest.consequence_thread is None
    
    def test_has_existing_data_empty_database(self, temp_db):
        """Test has_existing_data returns False for empty database."""
        seeder = DatabaseSeeder(temp_db)
        
        assert not seeder._has_existing_data()
    
    def test_has_existing_data_with_data(self, temp_db, sample_quest_data):
        """Test has_existing_data returns True when data exists."""
        seeder = DatabaseSeeder(temp_db)
        
        # Add a quest manually
        quest = seeder._json_to_quest(sample_quest_data[0])
        seeder.dao.create_quest(quest)
        
        assert seeder._has_existing_data()
    
    def test_seed_quests_success(self, temp_db, temp_quest_file):
        """Test successful quest seeding."""
        seeder = DatabaseSeeder(temp_db)
        
        # Temporarily replace the data directory to use our test file
        original_data_dir = seeder.data_dir
        seeder.data_dir = Path(temp_quest_file).parent
        
        # Rename the temp file to match expected name
        expected_file = seeder.data_dir / "quests_seed.json"
        os.rename(temp_quest_file, expected_file)
        
        try:
            result = seeder.seed_quests()
            
            assert result is True
            
            # Verify quests were added to database
            quests = seeder.dao.get_all_quests()
            assert len(quests) == 2
            
            quest_ids = [q.id for q in quests]
            assert "test_quest_1" in quest_ids
            assert "test_quest_2" in quest_ids
            
        finally:
            # Restore original data directory
            seeder.data_dir = original_data_dir
            # Cleanup
            if expected_file.exists():
                os.unlink(expected_file)
    
    def test_seed_quests_missing_file(self, temp_db):
        """Test quest seeding with missing file."""
        seeder = DatabaseSeeder(temp_db)
        
        # Use a non-existent data directory
        seeder.data_dir = Path("/non/existent/path")
        
        result = seeder.seed_quests()
        
        assert result is False
    
    def test_seed_all_success(self, temp_db, temp_quest_file):
        """Test successful seeding of all data."""
        seeder = DatabaseSeeder(temp_db)
        
        # Setup test file
        original_data_dir = seeder.data_dir
        seeder.data_dir = Path(temp_quest_file).parent
        expected_file = seeder.data_dir / "quests_seed.json"
        os.rename(temp_quest_file, expected_file)
        
        try:
            result = seeder.seed_all(force=True)
            
            assert result is True
            
            # Verify data was seeded
            quests = seeder.dao.get_all_quests()
            assert len(quests) == 2
            
        finally:
            seeder.data_dir = original_data_dir
            if expected_file.exists():
                os.unlink(expected_file)
    
    def test_seed_all_existing_data_no_force(self, temp_db, sample_quest_data):
        """Test that seed_all respects existing data without force flag."""
        seeder = DatabaseSeeder(temp_db)
        
        # Add existing data
        quest = seeder._json_to_quest(sample_quest_data[0])
        seeder.dao.create_quest(quest)
        
        result = seeder.seed_all(force=False)
        
        assert result is False
    
    def test_clear_data(self, temp_db, sample_quest_data):
        """Test clearing database data."""
        seeder = DatabaseSeeder(temp_db)
        
        # Add some data first
        quest = seeder._json_to_quest(sample_quest_data[0])
        seeder.dao.create_quest(quest)
        
        # Verify data exists
        assert seeder._has_existing_data()
        
        # Clear data
        result = seeder.clear_data(confirm=True)
        
        assert result is True
        assert not seeder._has_existing_data()

class TestDatabaseSeedingIntegration:
    """Integration tests for database seeding."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        yield db_path
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_full_seeding_workflow(self, temp_db):
        """Test the complete seeding workflow with real quest data."""
        seeder = DatabaseSeeder(temp_db)
        
        # Check if the real quest file exists
        quest_file = seeder.data_dir / "quests_seed.json"
        if not quest_file.exists():
            pytest.skip("Real quest data file not found")
        
        # Seed the database
        result = seeder.seed_all(force=True)
        
        assert result is True
        
        # Verify quests were loaded
        quests = seeder.dao.get_all_quests()
        assert len(quests) > 0
        
        # Verify quest structure
        for quest in quests:
            assert isinstance(quest, Quest)
            assert quest.id
            assert quest.title
            assert quest.location
            assert isinstance(quest.risk, RiskLevel)
            assert isinstance(quest.status, QuestStatus)
    
    def test_quest_retrieval_after_seeding(self, temp_db):
        """Test that seeded quests can be properly retrieved."""
        seeder = DatabaseSeeder(temp_db)
        
        # Create sample quest data
        sample_quest = {
            "id": "retrieval_test",
            "title": "Retrieval Test Quest",
            "location": "test_area",
            "tags": ["test"],
            "intro": "Test intro",
            "objectives": ["Test objective"],
            "success": "Test success",
            "failure": "Test failure",
            "reward": {"gold": 50, "items": [], "experience": 25},
            "risk": "calm"
        }
        
        # Convert and store quest
        quest = seeder._json_to_quest(sample_quest)
        seeder.dao.create_quest(quest)
        
        # Retrieve and verify
        retrieved_quest = seeder.dao.get_quest("retrieval_test")
        
        assert retrieved_quest is not None
        assert retrieved_quest.id == "retrieval_test"
        assert retrieved_quest.title == "Retrieval Test Quest"
        assert retrieved_quest.location == "test_area"
        assert retrieved_quest.risk == RiskLevel.CALM
        assert retrieved_quest.reward.gold == 50

