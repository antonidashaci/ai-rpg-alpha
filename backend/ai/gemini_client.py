"""
Gemini AI Client for AI-RPG-Alpha

This module handles communication with Google's Gemini AI API for story generation.
"""

import google.generativeai as genai
from typing import List, Dict, Any
import os

class GeminiClient:
    """Client for interacting with Google's Gemini AI API"""
    
    def __init__(self, api_key: str = None):
        """Initialize the Gemini client with API key"""
        self.api_key = api_key or ""
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (try different model names)
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except:
                try:
                    self.model = genai.GenerativeModel('gemini-pro')
                except:
                    print("Warning: Could not initialize Gemini model - using fallback responses")
                    self.model = None
        
    def generate_story_response(self, player_name: str, choice: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a story response based on player choice and context
        
        Args:
            player_name: The player's character name
            choice: The player's chosen action
            context: Additional context (location, stats, etc.)
            
        Returns:
            Dict with narrative, choices, and metadata
        """
        try:
            # Check if model is available
            if self.model is None:
                raise Exception("Gemini model not available")
                
            # Build the prompt for story generation
            prompt = self._build_story_prompt(player_name, choice, context)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response into structured format
            return self._parse_gemini_response(response.text, context, player_name)
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback response if API fails
            return self._get_fallback_response(player_name, choice)
    
    def _build_story_prompt(self, player_name: str, choice: str, context: Dict[str, Any] = None) -> str:
        """Build a comprehensive prompt for the AI"""
        
        if context is None:
            context = {}
            
        location = context.get('location', 'forest_entrance')
        turn_number = context.get('turn_number', 1)
        risk_level = context.get('risk_level', 'calm')
        player_data = context.get('player_data', {})
        
        # Get player stats if available
        stats_info = ""
        if player_data and 'stats' in player_data:
            stats = player_data['stats']
            stats_info = f"""
- Level: {stats.get('level', 1)}
- Health: {stats.get('health', 100)}/100
- Mana: {stats.get('mana', 50)}/50
- Strength: {stats.get('strength', 10)}
- Intelligence: {stats.get('intelligence', 10)}
- Charisma: {stats.get('charisma', 10)}"""

        # Create story prompts based on turn number for better pacing
        if turn_number <= 3:
            story_phase = "introduction"
        elif turn_number <= 8:
            story_phase = "exploration"
        else:
            story_phase = "adventure"
            
        prompt = f"""
You are writing a realistic, immersive story. This is {story_phase} phase.

CHARACTER: {player_name} - Turn {turn_number}
LOCATION: {self._format_location(location)}
PLAYER'S ACTION: "{choice}"

WRITING GUIDELINES FOR {story_phase.upper()} PHASE:

{"INTRODUCTION (Turns 1-3): Start slowly and realistically. " + player_name + " is just beginning their journey. Focus on: realistic everyday situations, gradual world-building, character establishment, simple choices. NO magic, quests, or dramatic events yet." if story_phase == "introduction" else ""}

{"EXPLORATION (Turns 4-8): " + player_name + " is getting familiar with the world. Introduce: mild mysteries, interesting locations, hints of larger story, character development. Keep magic/fantasy elements subtle." if story_phase == "exploration" else ""}

{"ADVENTURE (Turn 9+): Now " + player_name + " can face larger challenges, magic, quests. But still keep it grounded in established world." if story_phase == "adventure" else ""}

WRITING STYLE:
- Write in second person ("You...")
- Address the player as "{player_name}"
- Be realistic and immersive
- {"Start simple - " + player_name + " might be in a village, on a road, or resting somewhere normal" if story_phase == "introduction" else "Build naturally on established elements"}
- Keep responses 1-2 paragraphs, focused
- End with a situation that leads to realistic choices

RESPONSE FORMAT - Return ONLY this JSON:
{{
    "narrative": "A realistic, immersive story continuation. {"Start with everyday situations for " + player_name + ". Gradually build the world." if story_phase == "introduction" else "Continue building naturally on what's established."}",
    "choices": [
        "A practical/realistic option",
        "A cautious/observant option", 
        "A social/communicative option",
        "A creative/different approach"
    ],
    "location": "simple_location_name",
    "risk_level": "{"calm" if story_phase == "introduction" else "calm/mystery"}"
}}

Write a compelling but realistic story that makes {player_name} feel immersed in a believable world.
"""
        return prompt
    
    def _format_location(self, location: str) -> str:
        """Format location name for better readability"""
        return location.replace('_', ' ').title()
    
    def _parse_gemini_response(self, response_text: str, context: Dict[str, Any], player_name: str) -> Dict[str, Any]:
        """Parse Gemini's response into structured format"""
        try:
            import json
            
            # Clean the response text
            response_text = response_text.strip()
            
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                # Validate required fields
                if all(key in parsed for key in ['narrative', 'choices']):
                    # Ensure we have metadata
                    metadata = {
                        'location': parsed.get('location', context.get('location', 'unknown')),
                        'risk_level': parsed.get('risk_level', context.get('risk_level', 'calm')),
                        'turn_number': context.get('turn_number', 1) + 1
                    }
                    
                    return {
                        'narrative': parsed['narrative'],
                        'choices': parsed['choices'][:4],  # Limit to 4 choices
                        'metadata': metadata
                    }
            
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response: {response_text[:200]}...")
        
        # If parsing fails, create a structured response from the raw text
        return self._create_structured_response(response_text, context, player_name)
    
    def _create_structured_response(self, text: str, context: Dict[str, Any], player_name: str) -> Dict[str, Any]:
        """Create a structured response from raw text"""
        
        # Clean and limit narrative (reduce by 15%)
        narrative = text.replace('{', '').replace('}', '').strip()
        if len(narrative) > 400:
            narrative = narrative[:400] + "..."
        
        # Create contextual choices based on risk level
        risk_level = context.get('risk_level', 'calm')
        
        if risk_level == 'combat':
            default_choices = [
                "Attack with full force",
                "Defend and look for an opening",
                "Try to flee to safety", 
                "Use magic or special ability"
            ]
        elif risk_level == 'mystery':
            default_choices = [
                "Investigate more closely",
                "Proceed with caution",
                "Search for another way",
                "Trust your instincts"
            ]
        else:  # calm or other
            default_choices = [
                "Continue forward confidently",
                "Look around carefully",
                "Rest and plan your next move",
                "Try a creative approach"
            ]
        
        metadata = {
            'location': context.get('location', 'unknown_realm'),
            'risk_level': context.get('risk_level', 'calm'),
            'turn_number': context.get('turn_number', 1) + 1
        }
        
        return {
            'narrative': narrative,
            'choices': default_choices,
            'metadata': metadata
        }
    
    def _get_fallback_response(self, player_name: str, choice: str) -> Dict[str, Any]:
        """Fallback response when API is unavailable"""
        
        narrative = f"""{player_name}, you continue your journey.
        
You chose: "{choice}"
        
As you walk along the dusty path, you notice the sun casting long shadows through the trees. The road ahead curves gently to the right, and you can hear the distant sound of a stream. A small village might be just beyond the next hill.

What would you like to do?"""
        
        choices = [
            "Follow the path toward the village",
            "Stop to rest by the stream", 
            "Look around for other travelers",
            "Check your belongings"
        ]
        
        metadata = {
            'location': 'country_road',
            'risk_level': 'calm',
            'turn_number': 2
        }
        
        return {
            'narrative': narrative.strip(),
            'choices': choices,
            'metadata': metadata
        } 
