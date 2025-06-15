"""
AI-RPG-Alpha: Jinja Prompt Templates

This module contains Jinja2 templates for generating structured prompts
for the AI system. Templates help maintain consistency and allow for
dynamic content generation based on game state.
"""

from jinja2 import Environment, BaseLoader, Template
from typing import Dict, Any, List

class PromptTemplates:
    """
    Collection of Jinja2 templates for AI prompt generation.
    
    Provides structured templates for different types of AI interactions
    including narrative generation, choice evaluation, and quest creation.
    """
    
    def __init__(self):
        """Initialize the template environment"""
        self.env = Environment(loader=BaseLoader())
        self._load_templates()
    
    def _load_templates(self):
        """Load all prompt templates"""
        
        # Main narrative generation template
        self.narrative_template = self.env.from_string("""
You are the Game Master for "{{ game_title }}", an AI-driven text-based RPG.

PLAYER CONTEXT:
- Name: {{ player.name }}
- Level: {{ player.stats.level }}
- Location: {{ player.current_location }}
- Health: {{ player.stats.health }}/100
- Turn: {{ player.turn_number }}

RECENT MEMORY:
{% for memory in recent_memories %}
- {{ memory.content }}
{% endfor %}

CURRENT SITUATION:
{{ current_situation }}

PLAYER'S LAST CHOICE:
{{ player_choice }}

QUEST CONTEXT:
{% if active_quest %}
Active Quest: {{ active_quest.title }}
Objectives: {{ active_quest.objectives | join(', ') }}
{% else %}
No active quest
{% endif %}

INSTRUCTIONS:
Generate an engaging narrative response (2-3 paragraphs) that:
1. Acknowledges the player's choice
2. Describes the immediate consequences
3. Sets up the next decision point
4. Maintains consistency with the game world
5. Uses second person ("you") and present tense

Write in an immersive, descriptive style appropriate for a fantasy adventure.
        """.strip())
        
        # Choice generation template
        self.choices_template = self.env.from_string("""
Based on the current narrative situation, generate exactly {{ num_choices }} distinct player choices.

CURRENT NARRATIVE:
{{ narrative }}

PLAYER CONTEXT:
- Level: {{ player.stats.level }}
- Health: {{ player.stats.health }}/100
- Skills: Strength {{ player.stats.strength }}, Intelligence {{ player.stats.intelligence }}, Charisma {{ player.stats.charisma }}
- Inventory: {{ player.inventory | join(', ') if player.inventory else 'Empty' }}

REQUIREMENTS:
1. Each choice should be meaningfully different
2. Include varied approaches: combat, diplomacy, stealth, magic, etc.
3. Consider player's current stats and inventory
4. Make choices specific to the situation
5. Keep each choice to 1-2 sentences maximum

Format as a numbered list without additional text.
        """.strip())
        
        # Quest generation template
        self.quest_template = self.env.from_string("""
Generate a {{ difficulty }} difficulty {{ quest_type }} quest for {{ location }}.

WORLD CONTEXT:
{{ world_context }}

PLAYER LEVEL: {{ player_level }}

REQUIREMENTS:
- Title should be engaging and specific
- Introduction should hook the player
- 2-3 clear objectives
- Appropriate rewards for difficulty level
- Success/failure outcomes that affect the world
- Risk level: {{ risk_level }}

Respond with JSON in this exact format:
{
    "title": "Quest Title",
    "intro": "Engaging introduction that sets up the quest",
    "objectives": ["Clear objective 1", "Clear objective 2"],
    "success": "What happens when the quest succeeds",
    "failure": "What happens when the quest fails",
    "reward": {
        "gold": {{ 50 if difficulty == 'easy' else 100 if difficulty == 'medium' else 200 }},
        "items": ["reward item if applicable"],
        "experience": {{ 25 if difficulty == 'easy' else 50 if difficulty == 'medium' else 100 }}
    },
    "tags": ["{{ quest_type }}", "{{ location | lower }}"],
    "risk": "{{ risk_level }}"
}
        """.strip())
        
        # Combat resolution template
        self.combat_template = self.env.from_string("""
Resolve this combat encounter narratively.

PLAYER:
- Health: {{ player.stats.health }}/100
- Strength: {{ player.stats.strength }}
- Level: {{ player.stats.level }}
- Weapons: {{ player.inventory | select('match', '.*sword.*|.*bow.*|.*staff.*') | list | join(', ') or 'Bare hands' }}

ENEMY:
{{ enemy_description }}

PLAYER ACTION:
{{ player_action }}

COMBAT CONTEXT:
{{ combat_context }}

Generate a dramatic combat narrative (2-3 paragraphs) that:
1. Describes the action in vivid detail
2. Shows the consequences of the player's choice
3. Determines the outcome based on stats and strategy
4. Sets up the next combat round or resolution

Also provide outcome data:
OUTCOME: {{ 'SUCCESS' if player.stats.strength >= 12 else 'PARTIAL' if player.stats.strength >= 8 else 'FAILURE' }}
DAMAGE_TAKEN: {{ 0 if player.stats.strength >= 15 else 10 if player.stats.strength >= 10 else 20 }}
ENEMY_STATUS: {{ 'DEFEATED' if player.stats.strength >= 12 else 'WOUNDED' if player.stats.strength >= 8 else 'UNHARMED' }}
        """.strip())
        
        # Context building template
        self.context_template = self.env.from_string("""
Build comprehensive context for AI narrative generation.

PLAYER STATE:
{{ player | tojson(indent=2) }}

RELEVANT MEMORIES:
{% for memory in memories %}
Turn {{ memory.turn_number }}: {{ memory.content }}
{% endfor %}

ACTIVE QUESTS:
{% for quest in active_quests %}
- {{ quest.title }}: {{ quest.objectives | join(', ') }}
{% endfor %}

WORLD STATE:
- Current Location: {{ current_location }}
- Time of Day: {{ time_of_day }}
- Weather: {{ weather }}
- Notable NPCs Present: {{ npcs | join(', ') if npcs else 'None' }}

RECENT EVENTS:
{% for event in recent_events %}
- {{ event.description }}
{% endfor %}

CONSEQUENCE THREADS:
{% for consequence in pending_consequences %}
- Turn {{ consequence.trigger_turn }}: {{ consequence.event }}
{% endfor %}

This context should inform all narrative decisions and maintain consistency.
        """.strip())
        
        # Consequence evaluation template
        self.consequence_template = self.env.from_string("""
Evaluate the long-term consequences of this player action.

ACTION: {{ player_action }}
CONTEXT: {{ context }}

Consider:
1. Immediate effects (this turn)
2. Short-term consequences (next 2-3 turns)
3. Long-term implications (future quest availability, NPC relationships)
4. World state changes

Respond with JSON:
{
    "immediate": {
        "stat_changes": {"health": 0, "mana": 0, "gold": 0},
        "inventory_changes": {"add": [], "remove": []},
        "location_change": null
    },
    "delayed_consequences": [
        {
            "trigger_turn": {{ player.turn_number + 3 }},
            "event": "Description of what happens",
            "type": "positive/negative/neutral"
        }
    ],
    "world_changes": {
        "npc_relationships": {},
        "location_states": {},
        "available_quests": []
    },
    "narrative_flags": ["flag1", "flag2"]
}
        """.strip())
    
    def render_narrative_prompt(
        self, 
        player: Dict[str, Any], 
        current_situation: str,
        player_choice: str,
        recent_memories: List[Dict[str, Any]] = None,
        active_quest: Dict[str, Any] = None,
        game_title: str = "AI-RPG-Alpha"
    ) -> str:
        """
        Render the narrative generation prompt.
        
        Args:
            player: Player data dictionary
            current_situation: Description of current game situation
            player_choice: The player's last choice
            recent_memories: List of recent memory objects
            active_quest: Current active quest data
            game_title: Name of the game
            
        Returns:
            Rendered prompt string
        """
        return self.narrative_template.render(
            game_title=game_title,
            player=player,
            current_situation=current_situation,
            player_choice=player_choice,
            recent_memories=recent_memories or [],
            active_quest=active_quest
        )
    
    def render_choices_prompt(
        self, 
        narrative: str, 
        player: Dict[str, Any],
        num_choices: int = 4
    ) -> str:
        """
        Render the choice generation prompt.
        
        Args:
            narrative: Current narrative text
            player: Player data dictionary
            num_choices: Number of choices to generate
            
        Returns:
            Rendered prompt string
        """
        return self.choices_template.render(
            narrative=narrative,
            player=player,
            num_choices=num_choices
        )
    
    def render_quest_prompt(
        self,
        quest_type: str,
        location: str,
        difficulty: str = "medium",
        player_level: int = 1,
        world_context: str = "",
        risk_level: str = "mystery"
    ) -> str:
        """
        Render the quest generation prompt.
        
        Args:
            quest_type: Type of quest to generate
            location: Quest location
            difficulty: Quest difficulty level
            player_level: Current player level
            world_context: Additional world context
            risk_level: Risk level for the quest
            
        Returns:
            Rendered prompt string
        """
        return self.quest_template.render(
            quest_type=quest_type,
            location=location,
            difficulty=difficulty,
            player_level=player_level,
            world_context=world_context,
            risk_level=risk_level
        )
    
    def render_combat_prompt(
        self,
        player: Dict[str, Any],
        enemy_description: str,
        player_action: str,
        combat_context: str = ""
    ) -> str:
        """
        Render the combat resolution prompt.
        
        Args:
            player: Player data dictionary
            enemy_description: Description of the enemy
            player_action: Player's combat action
            combat_context: Additional combat context
            
        Returns:
            Rendered prompt string
        """
        return self.combat_template.render(
            player=player,
            enemy_description=enemy_description,
            player_action=player_action,
            combat_context=combat_context
        )
    
    def render_context_prompt(
        self,
        player: Dict[str, Any],
        memories: List[Dict[str, Any]] = None,
        active_quests: List[Dict[str, Any]] = None,
        current_location: str = "",
        time_of_day: str = "day",
        weather: str = "clear",
        npcs: List[str] = None,
        recent_events: List[Dict[str, Any]] = None,
        pending_consequences: List[Dict[str, Any]] = None
    ) -> str:
        """
        Render the context building prompt.
        
        Args:
            player: Player data dictionary
            memories: List of relevant memories
            active_quests: List of active quests
            current_location: Current location name
            time_of_day: Current time of day
            weather: Current weather
            npcs: List of NPCs present
            recent_events: List of recent game events
            pending_consequences: List of pending consequences
            
        Returns:
            Rendered prompt string
        """
        return self.context_template.render(
            player=player,
            memories=memories or [],
            active_quests=active_quests or [],
            current_location=current_location,
            time_of_day=time_of_day,
            weather=weather,
            npcs=npcs or [],
            recent_events=recent_events or [],
            pending_consequences=pending_consequences or []
        )
    
    def render_consequence_prompt(
        self,
        player_action: str,
        context: str,
        player: Dict[str, Any]
    ) -> str:
        """
        Render the consequence evaluation prompt.
        
        Args:
            player_action: The action taken by the player
            context: Current game context
            player: Player data dictionary
            
        Returns:
            Rendered prompt string
        """
        return self.consequence_template.render(
            player_action=player_action,
            context=context,
            player=player
        )

