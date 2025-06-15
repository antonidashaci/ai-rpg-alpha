"""
AI-RPG-Alpha: Test Suite for API Endpoints

Tests for the FastAPI endpoints to ensure proper functionality
of the game API, particularly the /turn endpoint.
"""

import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the modules to test
import sys
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from main import app

class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_openai_key(self):
        """Mock OpenAI API key for testing."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key-12345'}):
            yield
    
    def test_root_endpoint(self, client):
        """Test the root endpoint returns correct information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "AI-RPG-Alpha Backend" in data["message"]
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client, mock_openai_key):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["version"] == "0.1.0"
        assert "openai_configured" in data
        assert data["openai_configured"] is True
        assert "components" in data
    
    def test_health_endpoint_no_openai_key(self, client):
        """Test health endpoint when OpenAI key is not configured."""
        # Ensure no OpenAI key is set
        with patch.dict(os.environ, {}, clear=True):
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["openai_configured"] is False
    
    def test_turn_endpoint_missing_openai_key(self, client):
        """Test /turn endpoint returns error when OpenAI key is missing."""
        # Ensure no OpenAI key is set
        with patch.dict(os.environ, {}, clear=True):
            response = client.post("/turn", json={
                "player_id": "test_player",
                "choice": "test choice"
            })
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "OpenAI API key not configured" in data["detail"]
    
    def test_turn_endpoint_valid_request(self, client, mock_openai_key):
        """Test /turn endpoint with valid request."""
        response = client.post("/turn", json={
            "player_id": "test_player_123",
            "choice": "Begin my adventure"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "narrative" in data
        assert "choices" in data
        assert "metadata" in data
        
        # Check narrative content
        assert isinstance(data["narrative"], str)
        assert len(data["narrative"]) > 0
        assert "test_player_123" in data["narrative"]
        
        # Check choices
        assert isinstance(data["choices"], list)
        assert len(data["choices"]) == 4  # Should return 4 choices
        for choice in data["choices"]:
            assert isinstance(choice, str)
            assert len(choice) > 0
        
        # Check metadata
        assert isinstance(data["metadata"], dict)
        assert "risk_level" in data["metadata"]
        assert data["metadata"]["risk_level"] in ["calm", "mystery", "combat"]
        assert "location" in data["metadata"]
        assert "turn_number" in data["metadata"]
    
    def test_turn_endpoint_invalid_request_missing_player_id(self, client, mock_openai_key):
        """Test /turn endpoint with missing player_id."""
        response = client.post("/turn", json={
            "choice": "test choice"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_turn_endpoint_invalid_request_missing_choice(self, client, mock_openai_key):
        """Test /turn endpoint with missing choice."""
        response = client.post("/turn", json={
            "player_id": "test_player"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_turn_endpoint_empty_strings(self, client, mock_openai_key):
        """Test /turn endpoint with empty strings."""
        response = client.post("/turn", json={
            "player_id": "",
            "choice": ""
        })
        
        # Should still return 200 but handle empty strings gracefully
        assert response.status_code == 200
        data = response.json()
        assert "narrative" in data
        assert "choices" in data
    
    def test_turn_endpoint_long_choice(self, client, mock_openai_key):
        """Test /turn endpoint with very long choice text."""
        long_choice = "A" * 1000  # Very long choice
        
        response = client.post("/turn", json={
            "player_id": "test_player",
            "choice": long_choice
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "narrative" in data
        assert "choices" in data
    
    def test_turn_endpoint_special_characters(self, client, mock_openai_key):
        """Test /turn endpoint with special characters."""
        response = client.post("/turn", json={
            "player_id": "test_player_🎮",
            "choice": "I choose to explore the mystical forest! 🌲✨"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "narrative" in data
        assert "choices" in data
    
    def test_turn_endpoint_multiple_requests_same_player(self, client, mock_openai_key):
        """Test multiple requests for the same player."""
        player_id = "persistent_player_123"
        
        # First request
        response1 = client.post("/turn", json={
            "player_id": player_id,
            "choice": "Start my journey"
        })
        
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second request
        response2 = client.post("/turn", json={
            "player_id": player_id,
            "choice": "Continue exploring"
        })
        
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Both should be successful
        assert "narrative" in data1
        assert "narrative" in data2
        assert "choices" in data1
        assert "choices" in data2
    
    def test_turn_endpoint_different_players(self, client, mock_openai_key):
        """Test requests from different players."""
        # Player 1
        response1 = client.post("/turn", json={
            "player_id": "player_one",
            "choice": "Go north"
        })
        
        # Player 2
        response2 = client.post("/turn", json={
            "player_id": "player_two",
            "choice": "Go south"
        })
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Both should have valid responses
        assert "narrative" in data1
        assert "narrative" in data2
        assert "player_one" in data1["narrative"]
        assert "player_two" in data2["narrative"]

class TestAPIResponseStructure:
    """Test the structure and content of API responses."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_openai_key(self):
        """Mock OpenAI API key for testing."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key-12345'}):
            yield
    
    def test_turn_response_narrative_quality(self, client, mock_openai_key):
        """Test that narrative responses are of good quality."""
        response = client.post("/turn", json={
            "player_id": "quality_test_player",
            "choice": "Examine the ancient ruins"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        narrative = data["narrative"]
        
        # Check narrative quality
        assert len(narrative) > 50  # Should be substantial
        assert "quality_test_player" in narrative  # Should include player name
        assert not narrative.startswith(" ")  # Should not start with whitespace
        assert not narrative.endswith(" ")  # Should not end with whitespace
        
        # Should contain some descriptive content
        descriptive_words = ["you", "your", "the", "a", "an"]
        assert any(word in narrative.lower() for word in descriptive_words)
    
    def test_turn_response_choices_quality(self, client, mock_openai_key):
        """Test that choice responses are of good quality."""
        response = client.post("/turn", json={
            "player_id": "choice_test_player",
            "choice": "Look for treasure"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        choices = data["choices"]
        
        # Check choices quality
        assert len(choices) == 4  # Should have exactly 4 choices
        
        for choice in choices:
            assert len(choice) > 10  # Each choice should be substantial
            assert not choice.startswith(" ")  # No leading whitespace
            assert not choice.endswith(" ")  # No trailing whitespace
            assert choice[0].isupper() or choice[0].isdigit()  # Should start with capital or number
        
        # Choices should be different
        assert len(set(choices)) == len(choices)  # All choices should be unique
    
    def test_turn_response_metadata_structure(self, client, mock_openai_key):
        """Test that metadata has the correct structure."""
        response = client.post("/turn", json={
            "player_id": "metadata_test_player",
            "choice": "Cast a spell"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        metadata = data["metadata"]
        
        # Check required metadata fields
        assert "risk_level" in metadata
        assert metadata["risk_level"] in ["calm", "mystery", "combat"]
        
        assert "location" in metadata
        assert isinstance(metadata["location"], str)
        assert len(metadata["location"]) > 0
        
        assert "turn_number" in metadata
        assert isinstance(metadata["turn_number"], int)
        assert metadata["turn_number"] >= 1

class TestAPIErrorHandling:
    """Test error handling in API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    def test_invalid_json_request(self, client):
        """Test handling of invalid JSON in request."""
        response = client.post("/turn", 
                             data="invalid json",
                             headers={"Content-Type": "application/json"})
        
        assert response.status_code == 422
    
    def test_missing_content_type(self, client):
        """Test handling of missing content type."""
        response = client.post("/turn", data='{"player_id": "test", "choice": "test"}')
        
        # FastAPI should handle this gracefully
        assert response.status_code in [422, 415]  # Unprocessable Entity or Unsupported Media Type
    
    def test_get_request_to_post_endpoint(self, client):
        """Test GET request to POST-only endpoint."""
        response = client.get("/turn")
        
        assert response.status_code == 405  # Method Not Allowed
    
    def test_nonexistent_endpoint(self, client):
        """Test request to non-existent endpoint."""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404  # Not Found

class TestAPICORS:
    """Test CORS configuration."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/")
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        
    def test_options_request(self, client):
        """Test OPTIONS request for CORS preflight."""
        response = client.options("/turn", 
                                headers={
                                    "Origin": "http://localhost:3000",
                                    "Access-Control-Request-Method": "POST",
                                    "Access-Control-Request-Headers": "Content-Type"
                                })
        
        # Should handle OPTIONS request
        assert response.status_code in [200, 204]

