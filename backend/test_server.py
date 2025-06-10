#!/usr/bin/env python3
"""
Test script for AI-RPG-Alpha server
"""

import json
import requests
import time
from ai.gemini_client import GeminiClient

def test_gemini_client():
    """Test the Gemini client directly"""
    print("Testing Gemini Client...")
    try:
        client = GeminiClient()
        response = client.generate_story_response("TestPlayer", "start adventure")
        print("✓ Gemini client works!")
        print(f"Sample response: {response['narrative'][:100]}...")
        return True
    except Exception as e:
        print(f"✗ Gemini client failed: {e}")
        return False

def test_server_endpoints():
    """Test server endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("\nTesting Server Endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint works!")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")
        return False
    
    # Test turn endpoint
    try:
        data = {
            "player_id": "test_player",
            "choice": "start"
        }
        response = requests.post(f"{base_url}/turn", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✓ Turn endpoint works!")
            print(f"Sample narrative: {result['narrative'][:100]}...")
            return True
        else:
            print(f"✗ Turn endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Turn endpoint failed: {e}")
        return False

def main():
    print("AI-RPG-Alpha Server Test")
    print("=" * 40)
    
    # Test Gemini client
    gemini_ok = test_gemini_client()
    
    if not gemini_ok:
        print("\n❌ Gemini client not working - server will fail")
        return
    
    # Test server endpoints
    server_ok = test_server_endpoints()
    
    if server_ok:
        print("\n✅ All tests passed! Server is working correctly.")
    else:
        print("\n❌ Server tests failed. Check server startup.")

if __name__ == "__main__":
    main() 