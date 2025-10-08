"""
Local LLM Client for AI-RPG-Alpha
=================================

This module handles communication with local LLMs through Ollama API.
Supports various local models for narrative generation and game logic.
"""

import requests
import json
import time
from typing import List, Dict, Any, Optional
import logging

class LocalLLMClient:
    """
    Client for interacting with local LLMs via Ollama API

    Supports:
    - Ollama API communication
    - Multiple model support (llama2, codellama, mistral, etc.)
    - Fallback responses when local LLM unavailable
    - Structured response parsing
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2",
        timeout: int = 30
    ):
        """
        Initialize the local LLM client

        Args:
            base_url: Ollama API base URL (default: localhost:11434)
            model: Default model to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.default_model = model
        self.timeout = timeout

        # Test connection on initialization
        self.connected = self._test_connection()

        if self.connected:
            logging.info(f"Local LLM client connected to {self.base_url} using model {model}")
        else:
            logging.warning(f"Local LLM client could not connect to {self.base_url}")

    def _test_connection(self) -> bool:
        """Test connection to Ollama API"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _make_request(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.8,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Make a request to the local LLM

        Args:
            prompt: The prompt to send
            model: Model to use (defaults to self.default_model)
            temperature: Creativity parameter
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if error
        """
        if not self.connected:
            return None

        model = model or self.default_model

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                logging.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logging.error(f"Error calling Ollama API: {e}")
            return None

    def generate_story_response(
        self,
        player_name: str,
        choice: str,
        context: Dict[str, Any] = None,
        scenario: str = "northern_realms"
    ) -> Dict[str, Any]:
        """
        Generate a story response using local LLM

        Args:
            player_name: Player character name
            choice: Player's chosen action
            context: Game context (location, stats, etc.)
            scenario: Current scenario

        Returns:
            Dict with narrative, choices, and metadata
        """
        try:
            # Build comprehensive prompt
            prompt = self._build_story_prompt(player_name, choice, context, scenario)

            # Generate response
            response_text = self._make_request(
                prompt,
                temperature=0.8,
                max_tokens=600
            )

            if response_text:
                return self._parse_llm_response(response_text, context, player_name)
            else:
                return self._get_fallback_response(player_name, choice)

        except Exception as e:
            logging.error(f"Error generating story response: {e}")
            return self._get_fallback_response(player_name, choice)

    def _build_story_prompt(
        self,
        player_name: str,
        choice: str,
        context: Dict[str, Any],
        scenario: str
    ) -> str:
        """Build comprehensive prompt for local LLM"""

        # Get context information
        location = context.get('location', 'starting_village')
        turn_number = context.get('turn_number', 1)
        risk_level = context.get('risk_level', 'calm')
        player_data = context.get('player_data', {})

        # Scenario-specific context
        scenario_context = self._get_scenario_context(scenario)

        # Player stats for context
        stats_info = ""
        if player_data:
            stats = player_data.get('stats', {})
            stats_info = f"""
Player Stats:
- Level: {stats.get('level', 1)}
- Health: {stats.get('health', 20)}/20
- Mana: {stats.get('mana', 10)}/10
- Strength: {stats.get('strength', 10)}
- Intelligence: {stats.get('intelligence', 10)}
- Charisma: {stats.get('charisma', 10)}"""

        prompt = f"""
You are an expert Game Master for {scenario_context["name"]} - a rich epic fantasy RPG.

{scenario_context["description"]}

CURRENT SITUATION:
- Player: {player_name}
- Turn: {turn_number}
- Location: {location.replace('_', ' ').title()}
- Risk Level: {risk_level}
- Player Action: "{choice}"

{stats_info}

GAME MASTER INSTRUCTIONS:
{scenario_context["instructions"]}

WRITING STYLE:
- Write in second person ("You...")
- Address player as "{player_name}"
- Keep responses 2-3 paragraphs, focused and engaging
- End with a situation that naturally leads to player choices
- Maintain consistency with established world and character

RESPONSE FORMAT - Return ONLY this JSON:
{{
    "narrative": "A compelling, immersive story continuation that fits the {scenario} setting. Focus on atmosphere, character development, and meaningful choices.",
    "choices": [
        "A tactical/combat option",
        "A diplomatic/social option",
        "An exploratory/investigative option",
        "A creative/magical option"
    ],
    "location": "current_location_name",
    "risk_level": "{risk_level}",
    "turn_number": {turn_number + 1},
    "metadata": {{
        "scenario": "{scenario}",
        "generated_at": "current_timestamp"
    }}
}}

Generate an engaging narrative that advances the story while maintaining immersion in the {scenario} world.
"""

        return prompt

    def _get_scenario_context(self, scenario: str) -> Dict[str, str]:
        """Get scenario-specific context for prompts"""

        scenarios = {
            "northern_realms": {
                "name": "The Northern Realms",
                "description": "An epic fantasy world of ancient prophecies, dragon threats, and kingdom politics. You control a hero marked by fate in a Skyrim/Tolkien-inspired setting.",
                "instructions": """
- Focus on epic fantasy elements: dragons, magic, medieval politics
- Include kingdom intrigue, noble houses, and ancient prophecies
- Balance combat, diplomacy, and magic in player choices
- Maintain a tone that's heroic but grounded in realistic consequences
- Reference the Dragon Prophecy and kingdom alliances when relevant
"""
            }
        }

        return scenarios.get(scenario, scenarios["northern_realms"])

    def _parse_llm_response(
        self,
        response_text: str,
        context: Dict[str, Any],
        player_name: str
    ) -> Dict[str, Any]:
        """Parse local LLM response into structured format"""

        try:
            # Clean response text
            response_text = response_text.strip()

            # Try to extract JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)

                # Validate required fields
                if all(key in parsed for key in ['narrative', 'choices']):
                    return {
                        'narrative': parsed['narrative'],
                        'choices': parsed['choices'][:4],  # Limit to 4 choices
                        'metadata': parsed.get('metadata', {})
                    }

        except Exception as e:
            logging.error(f"Error parsing LLM response: {e}")

        # Fallback parsing if JSON fails
        return self._create_structured_response(response_text, context, player_name)

    def _create_structured_response(
        self,
        text: str,
        context: Dict[str, Any],
        player_name: str
    ) -> Dict[str, Any]:
        """Create structured response from raw text"""

        # Clean narrative text
        narrative = text.replace('{', '').replace('}', '').strip()
        if len(narrative) > 500:
            narrative = narrative[:500] + "..."

        # Generate contextual choices
        risk_level = context.get('risk_level', 'calm')

        if risk_level == 'combat':
            default_choices = [
                "Fight with all your strength",
                "Try to find a tactical advantage",
                "Use magic or special abilities",
                "Attempt to negotiate or flee"
            ]
        elif risk_level == 'mystery':
            default_choices = [
                "Investigate the mystery further",
                "Proceed with caution",
                "Seek help from allies",
                "Trust your instincts"
            ]
        else:  # calm
            default_choices = [
                "Continue your journey",
                "Explore the surroundings",
                "Rest and plan ahead",
                "Seek information from locals"
            ]

        metadata = {
            'location': context.get('location', 'unknown'),
            'risk_level': risk_level,
            'turn_number': context.get('turn_number', 1) + 1,
            'generated_at': time.time()
        }

        return {
            'narrative': narrative,
            'choices': default_choices,
            'metadata': metadata
        }

    def _get_fallback_response(self, player_name: str, choice: str) -> Dict[str, Any]:
        """Fallback response when local LLM is unavailable"""

        narrative = f"""As {player_name}, you chose to {choice.lower()}.

The path ahead winds through ancient forests, where the trees whisper secrets of the old world. Sunlight filters through the canopy, casting dancing shadows on the forest floor. You feel the weight of destiny on your shoulders as you continue your journey through the Northern Realms.

The air carries the scent of pine and distant rain. Somewhere ahead, adventure awaits."""

        choices = [
            "Press deeper into the forest",
            "Follow a side trail you notice",
            "Rest beneath a large oak tree",
            "Check your map and bearings"
        ]

        metadata = {
            'location': 'ancient_forest',
            'risk_level': 'calm',
            'turn_number': 2
        }

        return {
            'narrative': narrative.strip(),
            'choices': choices,
            'metadata': metadata
        }

    def get_available_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        if not self.connected:
            return []

        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except:
            pass

        return []

    def test_model(self, model: str) -> bool:
        """Test if a specific model works"""
        test_prompt = "Write a single sentence about a brave adventurer:"

        response = self._make_request(
            test_prompt,
            model=model,
            temperature=0.7,
            max_tokens=50
        )

        return response is not None and len(response.strip()) > 10


class LocalLLMManager:
    """
    Manager for local LLM operations

    Handles:
    - Model selection and switching
    - Performance monitoring
    - Fallback strategies
    - Configuration management
    """

    def __init__(self):
        self.client = None
        self.current_model = "llama2"
        self.models_tested = {}
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client with best available model"""
        # Try common model names in order of preference
        preferred_models = [
            "llama2:13b", "llama2:7b", "llama2",
            "codellama", "mistral", "vicuna"
        ]

        for model in preferred_models:
            client = LocalLLMClient(model=model)
            if client.connected:
                self.client = client
                self.current_model = model
                logging.info(f"Using local model: {model}")
                break

        if not self.client:
            logging.warning("No local LLM available - using fallback responses only")

    def generate_response(self, *args, **kwargs) -> Dict[str, Any]:
        """Generate response using current client"""
        if self.client:
            return self.client.generate_story_response(*args, **kwargs)
        else:
            # Return fallback if no client available
            return self._get_no_llm_fallback(args[0] if args else "Adventurer", args[1] if len(args) > 1 else "continue")

    def _get_no_llm_fallback(self, player_name: str, choice: str) -> Dict[str, Any]:
        """Fallback when no LLM is available at all"""

        narrative = f"""As {player_name}, you decide to {choice.lower()}.

Your journey continues through the Northern Realms. The world around you is filled with wonder and danger, ancient magic and forgotten lore. Every choice you make shapes your destiny and the fate of the kingdoms.

The path ahead holds both promise and peril. What will you do next?"""

        choices = [
            "Continue your adventure",
            "Seek out allies",
            "Explore the mysteries",
            "Prepare for challenges ahead"
        ]

        metadata = {
            'location': 'northern_realms',
            'risk_level': 'calm',
            'turn_number': 1
        }

        return {
            'narrative': narrative.strip(),
            'choices': choices,
            'metadata': metadata
        }

    def is_available(self) -> bool:
        """Check if local LLM is available"""
        return self.client is not None and self.client.connected

    def get_status(self) -> Dict[str, Any]:
        """Get current LLM status"""
        if not self.client:
            return {
                "available": False,
                "model": None,
                "connection": "No client initialized"
            }

        return {
            "available": self.client.connected,
            "model": self.current_model,
            "base_url": self.client.base_url,
            "available_models": self.client.get_available_models()
        }

