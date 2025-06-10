"""
AI-RPG-Alpha: OpenAI Client Wrapper

This module provides a wrapper around the OpenAI API for generating narrative content,
handling conversations, and managing AI interactions within the game engine.
"""

import openai
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class OpenAIClient:
    """
    Wrapper class for OpenAI API interactions.
    
    Handles all AI-related operations including narrative generation,
    choice evaluation, and context-aware responses.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
            model: OpenAI model to use for completions
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        # Set the API key for the openai library
        openai.api_key = self.api_key
        
        # Default parameters for completions
        self.default_params = {
            "model": self.model,
            "temperature": 0.8,  # Creative but not too random
            "max_tokens": 500,   # Reasonable length for narrative segments
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
    
    def generate_narrative(
        self, 
        prompt: str, 
        context: Dict[str, Any] = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate narrative content based on a prompt and context.
        
        Args:
            prompt: The main prompt for narrative generation
            context: Additional context information
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated narrative text
        """
        try:
            params = self.default_params.copy()
            if temperature is not None:
                params["temperature"] = temperature
            if max_tokens is not None:
                params["max_tokens"] = max_tokens
            
            # Build the messages for the chat completion
            messages = [
                {
                    "role": "system",
                    "content": """You are a master storyteller and game master for an AI-driven text-based RPG. 
                    Your role is to create immersive, engaging narrative content that responds to player choices 
                    and maintains consistency with the game world. Always write in second person ("you") and 
                    present tense. Keep responses engaging but concise, around 2-3 paragraphs."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Add context if provided
            if context:
                context_str = f"Game Context: {json.dumps(context, indent=2)}"
                messages.insert(1, {
                    "role": "system",
                    "content": context_str
                })
            
            response = openai.ChatCompletion.create(
                messages=messages,
                **params
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating narrative: {e}")
            return "The mists of uncertainty cloud your vision. Perhaps try a different approach."
    
    def generate_choices(
        self, 
        narrative: str, 
        context: Dict[str, Any] = None,
        num_choices: int = 4
    ) -> List[str]:
        """
        Generate player choices based on the current narrative and context.
        
        Args:
            narrative: Current narrative text
            context: Game context information
            num_choices: Number of choices to generate
            
        Returns:
            List of choice strings
        """
        try:
            prompt = f"""
            Based on the following narrative, generate exactly {num_choices} meaningful player choices.
            Each choice should be distinct and lead to different potential outcomes.
            Format as a simple numbered list.
            
            Narrative: {narrative}
            """
            
            messages = [
                {
                    "role": "system",
                    "content": """You are generating player choices for a text-based RPG. 
                    Create choices that are:
                    1. Distinct and meaningful
                    2. Appropriate to the situation
                    3. Varied in approach (combat, diplomacy, exploration, etc.)
                    4. Concise but descriptive
                    
                    Format as a numbered list without any additional text."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            if context:
                context_str = f"Game Context: {json.dumps(context, indent=2)}"
                messages.insert(1, {
                    "role": "system",
                    "content": context_str
                })
            
            response = openai.ChatCompletion.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=200
            )
            
            # Parse the response to extract choices
            content = response.choices[0].message.content.strip()
            choices = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering and clean up
                    choice = line.split('.', 1)[-1].strip()
                    choice = choice.lstrip('- ').strip()
                    if choice:
                        choices.append(choice)
            
            # Ensure we have the right number of choices
            while len(choices) < num_choices:
                choices.append("Wait and observe the situation")
            
            return choices[:num_choices]
            
        except Exception as e:
            print(f"Error generating choices: {e}")
            return [
                "Continue forward cautiously",
                "Look around for more information",
                "Take a moment to think",
                "Try a different approach"
            ]
    
    def evaluate_choice_outcome(
        self, 
        choice: str, 
        context: Dict[str, Any],
        player_stats: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Evaluate the outcome of a player's choice.
        
        Args:
            choice: The player's chosen action
            context: Current game context
            player_stats: Player statistics for skill checks
            
        Returns:
            Dictionary containing outcome information
        """
        try:
            prompt = f"""
            Evaluate the outcome of this player choice in the context of the game situation.
            Provide a JSON response with the following structure:
            {{
                "success": true/false,
                "outcome_type": "success/partial_success/failure/critical_failure",
                "consequences": ["list", "of", "consequences"],
                "narrative_hints": ["hints", "for", "narrative"],
                "stat_changes": {{"health": 0, "mana": 0, "gold": 0}},
                "risk_level": "calm/mystery/combat"
            }}
            
            Player Choice: {choice}
            Game Context: {json.dumps(context, indent=2)}
            Player Stats: {json.dumps(player_stats or {}, indent=2)}
            """
            
            messages = [
                {
                    "role": "system",
                    "content": """You are a game master evaluating player actions. 
                    Consider the player's stats, the situation context, and the nature of their choice.
                    Provide realistic outcomes that maintain game balance and narrative consistency.
                    Always respond with valid JSON only."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = openai.ChatCompletion.create(
                messages=messages,
                model=self.model,
                temperature=0.6,
                max_tokens=300
            )
            
            # Parse JSON response
            content = response.choices[0].message.content.strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "success": True,
                    "outcome_type": "success",
                    "consequences": [],
                    "narrative_hints": ["Your action has an effect"],
                    "stat_changes": {},
                    "risk_level": "calm"
                }
            
        except Exception as e:
            print(f"Error evaluating choice outcome: {e}")
            return {
                "success": True,
                "outcome_type": "success",
                "consequences": [],
                "narrative_hints": ["Something happens"],
                "stat_changes": {},
                "risk_level": "calm"
            }
    
    def generate_quest_content(
        self, 
        quest_type: str, 
        location: str, 
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Generate dynamic quest content.
        
        Args:
            quest_type: Type of quest (exploration, combat, social, etc.)
            location: Quest location
            difficulty: Quest difficulty level
            
        Returns:
            Dictionary containing quest information
        """
        try:
            prompt = f"""
            Generate a {difficulty} difficulty {quest_type} quest for location: {location}.
            Provide a JSON response with this structure:
            {{
                "title": "Quest Title",
                "intro": "Quest introduction text",
                "objectives": ["objective 1", "objective 2"],
                "success": "Success outcome text",
                "failure": "Failure outcome text",
                "reward": {{"gold": 100, "items": ["item1"], "experience": 50}},
                "tags": ["tag1", "tag2"],
                "risk": "calm/mystery/combat"
            }}
            """
            
            messages = [
                {
                    "role": "system",
                    "content": """You are a quest designer for a fantasy RPG. 
                    Create engaging, balanced quests that fit the specified parameters.
                    Always respond with valid JSON only."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = openai.ChatCompletion.create(
                messages=messages,
                model=self.model,
                temperature=0.8,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback quest
                return {
                    "title": f"Adventure in {location}",
                    "intro": f"A mysterious opportunity awaits in {location}.",
                    "objectives": ["Explore the area", "Complete the challenge"],
                    "success": "You successfully complete your task.",
                    "failure": "Despite your efforts, you were unable to succeed.",
                    "reward": {"gold": 50, "items": [], "experience": 25},
                    "tags": [quest_type, location.lower()],
                    "risk": "mystery"
                }
            
        except Exception as e:
            print(f"Error generating quest content: {e}")
            return {
                "title": "Simple Task",
                "intro": "A simple task needs to be completed.",
                "objectives": ["Complete the task"],
                "success": "Task completed successfully.",
                "failure": "Task could not be completed.",
                "reward": {"gold": 25, "items": [], "experience": 10},
                "tags": ["simple"],
                "risk": "calm"
            }

