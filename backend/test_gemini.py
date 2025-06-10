#!/usr/bin/env python3
"""
Simple test script for Gemini AI integration
"""

from ai.gemini_client import GeminiClient

def test_gemini():
    """Test the Gemini client"""
    print("Testing Gemini AI Client...")
    
    try:
        # Initialize client
        client = GeminiClient()
        print("✓ Gemini client initialized")
        
        # Test story generation
        response = client.generate_story_response(
            player_name="TestPlayer",
            choice="start the adventure",
            context={'location': 'starting_village', 'turn_number': 1, 'risk_level': 'calm'}
        )
        
        print("✓ Story response generated")
        print(f"Narrative length: {len(response['narrative'])} characters")
        print(f"Number of choices: {len(response['choices'])}")
        print(f"Metadata: {response['metadata']}")
        
        print("\n--- SAMPLE NARRATIVE ---")
        print(response['narrative'][:200] + "..." if len(response['narrative']) > 200 else response['narrative'])
        
        print("\n--- SAMPLE CHOICES ---")
        for i, choice in enumerate(response['choices'], 1):
            print(f"{i}. {choice}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini()
    print(f"\nTest {'PASSED' if success else 'FAILED'}") 