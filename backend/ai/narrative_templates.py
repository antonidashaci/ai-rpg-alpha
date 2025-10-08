"""
AI Narrative Templates
======================

Comprehensive prompt templates for AI narrative generation:
- Combat scenarios with tactical descriptions
- Cosmic horror narration with sanity effects
- Long-form quest progression
- Scenario-specific storytelling styles
"""

from typing import Dict, Any, Optional


class NarrativeTemplates:
    """AI prompt templates for different narrative contexts"""
    
    @staticmethod
    def combat_narrative_prompt(
        combat_state: Dict[str, Any],
        player_action: str,
        player_stats: Dict[str, int],
        scenario: str
    ) -> str:
        """Generate combat narrative prompt"""
        
        base_prompt = f"""You are an expert Game Master narrating a tactical combat encounter in a {scenario} setting.

COMBAT SITUATION:
- Turn: {combat_state.get('turn', 1)}
- Player Health: {combat_state.get('player_health')}/{combat_state.get('player_max_health')}
- Player Action: {player_action}
- Player Stats: STR {player_stats.get('strength', 10)}, DEX {player_stats.get('dexterity', 10)}, INT {player_stats.get('intelligence', 10)}

ENEMIES:
{NarrativeTemplates._format_enemies(combat_state.get('enemies', []))}

ENVIRONMENT:
{NarrativeTemplates._format_environment(combat_state.get('environment', []))}

INSTRUCTIONS:
- Describe the action in vivid, tactical detail
- Emphasize environmental factors and positioning
- Make combat feel dynamic and consequential
- Use Baldur's Gate 3-style tactical descriptions
- Keep response to 2-3 paragraphs
- End with the immediate result of the action

Generate an engaging combat narrative:"""
        
        return base_prompt
    
    @staticmethod
    def cosmic_horror_prompt(
        quest_state: Dict[str, Any],
        player_action: str,
        sanity_level: str,
        corruption_percentage: float
    ) -> str:
        """Generate cosmic horror narrative prompt"""
        
        sanity_instructions = {
            "stable": "Describe reality normally with subtle wrongness.",
            "disturbed": "Add minor hallucinations and unsettling details.",
            "fractured": "Reality bends. Time and space feel unstable.",
            "breaking": "Severe reality distortion. Narrator becomes unreliable.",
            "shattered": "Complete madness. Reality itself is questionable."
        }
        
        return f"""You are narrating a Lovecraftian cosmic horror story in the style of H.P. Lovecraft.

CURRENT STATE:
- Turn: {quest_state.get('turn_number', 1)}
- Act: {quest_state.get('current_act', 'setup')}
- Sanity Level: {sanity_level} ({100 - corruption_percentage:.1f}% sanity remaining)
- Player Action: {player_action}

SANITY EFFECTS:
{sanity_instructions.get(sanity_level, "Normal perception")}

THE WHISPERING TOWN:
You are in Ashmouth, a coastal town where reality is breaking down. The whispers are constant.
An eldritch entity lurks beneath the town. Forbidden knowledge corrupts the mind.

INSTRUCTIONS:
- Emphasize psychological horror over physical threats
- Use cosmic horror themes: forbidden knowledge, reality distortion, insignificance
- Build dread and tension through implication
- As sanity decreases, make narration increasingly unreliable
- Include "the whispers" subtly in the narrative
- Never explain everything - maintain mystery
- 2-3 paragraphs maximum
- End with choices that matter

Generate the narrative for this turn:"""
    
    @staticmethod
    def long_form_quest_prompt(
        quest_state: Dict[str, Any],
        player_action: str,
        scenario: str,
        milestone_info: Optional[Dict] = None
    ) -> str:
        """Generate long-form quest narrative prompt"""
        
        act_descriptions = {
            "setup": "This is the SETUP act (Turns 1-15). Establish mystery, introduce characters, create intrigue. Build foundation for the story.",
            "pursuit": "This is the PURSUIT act (Turns 16-30). Complications arise, stakes increase, deeper revelations emerge. Tension builds.",
            "climax": "This is the CLIMAX act (Turns 31-40). High-stakes decisions, consequences manifest, story rushes toward resolution.",
            "aftermath": "This is the AFTERMATH. Deal with consequences of all choices made."
        }
        
        milestone_text = ""
        if milestone_info:
            milestone_text = f"""
MILESTONE REACHED: {milestone_info.get('title', '')}
{milestone_info.get('description', '')}
This is a MAJOR narrative moment. Make it impactful.
"""
        
        return f"""You are an expert Game Master running a 40-turn epic quest in the {scenario} setting.

QUEST PROGRESS:
- Turn: {quest_state.get('turn_number', 1)} of {quest_state.get('total_turns', 40)}
- Current Act: {quest_state.get('current_act', 'setup')}
- Overall Progress: {quest_state.get('progress_percentage', 0):.1f}%
- Player Action: {player_action}

ACT CONTEXT:
{act_descriptions.get(quest_state.get('current_act', 'setup'), '')}

{milestone_text}

QUEST PRINCIPLES:
- This is LONG-FORM storytelling - pace accordingly
- Meaningful choices should emerge every 3-5 turns
- Build consequences that ripple forward
- Not every turn needs major revelations
- Sometimes the journey matters more than action
- Create memorable NPCs and relationships
- World should feel alive and reactive

INSTRUCTIONS:
- Generate narrative that fits the current act and pacing
- If at a milestone, make it feel significant
- Otherwise, provide engaging progression
- Always present meaningful choices
- 2-3 paragraphs for regular turns, 3-4 for milestones
- End with 3-4 distinct choice options

Generate the quest narrative:"""
    
    @staticmethod
    def scenario_specific_prompt(scenario: str) -> str:
        """Get scenario-specific style guidelines"""
        
        scenarios = {
            "northern_realms": """
NORTHERN REALMS (Epic Fantasy):
Style: Tolkien meets Skyrim. Epic, heroic, mythological.
Themes: Ancient prophecies, dragon threats, political intrigue, heroic destiny.
Tone: Grand and sweeping, but grounded in personal stakes.
NPCs: Medieval fantasy archetypes - wizards, knights, rogues, priests.
Language: Slightly archaic but accessible. Use "thee/thou" sparingly.
Combat: Swords, magic, dragons. Epic but tactical.
""",
            "whispering_town": """
THE WHISPERING TOWN (Cosmic Horror):
Style: H.P. Lovecraft meets modern psychological horror.
Themes: Forbidden knowledge, reality breakdown, insignificance, madness.
Tone: Dread, mystery, building tension. Never fully explain.
NPCs: Cultists, investigators, townsfolk with secrets, unreliable narrators.
Language: Dense, academic when describing knowledge. Fragmented when sanity fails.
Combat: Psychological, ritualistic. Violence is disturbing, not heroic.
Special: Text corruption at low sanity. Reality distortion. Unreliable narration.
""",
            "neo_tokyo": """
NEO-TOKYO 2087 (Cyberpunk):
Style: Blade Runner meets Ghost in the Shell.
Themes: AI consciousness, corporate conspiracy, transhumanism, identity.
Tone: Noir, gritty, philosophical. High-tech low-life.
NPCs: Hackers, corporate agents, AIs, cyborgs, street samurai.
Language: Tech jargon mixed with street slang. Japanese terms occasionally.
Combat: Cybernetic, hacking, social engineering. Fast and brutal.
"""
        }
        
        return scenarios.get(scenario, scenarios["northern_realms"])
    
    @staticmethod
    def generate_master_prompt(
        context: Dict[str, Any],
        scenario: str,
        narrative_type: str = "quest"
    ) -> str:
        """Generate complete AI prompt for narrative generation"""
        
        # Get scenario styling
        scenario_style = NarrativeTemplates.scenario_specific_prompt(scenario)
        
        # Build context-specific prompt
        if narrative_type == "combat":
            specific_prompt = NarrativeTemplates.combat_narrative_prompt(
                combat_state=context.get('combat_state', {}),
                player_action=context.get('player_action', ''),
                player_stats=context.get('player_stats', {}),
                scenario=scenario
            )
        elif narrative_type == "cosmic_horror":
            specific_prompt = NarrativeTemplates.cosmic_horror_prompt(
                quest_state=context.get('quest_state', {}),
                player_action=context.get('player_action', ''),
                sanity_level=context.get('sanity_level', 'stable'),
                corruption_percentage=context.get('corruption_percentage', 0)
            )
        else:  # quest
            specific_prompt = NarrativeTemplates.long_form_quest_prompt(
                quest_state=context.get('quest_state', {}),
                player_action=context.get('player_action', ''),
                scenario=scenario,
                milestone_info=context.get('milestone_info')
            )
        
        # Combine with scenario styling
        master_prompt = f"""{scenario_style}

{specific_prompt}

RESPONSE FORMAT:
Provide your response in this structure:
1. Narrative (2-4 paragraphs)
2. Choices (3-4 distinct options)

Be creative, engaging, and true to the genre!"""
        
        return master_prompt
    
    # Helper methods
    @staticmethod
    def _format_enemies(enemies: list) -> str:
        """Format enemy list for prompt"""
        if not enemies:
            return "No enemies remaining"
        
        lines = []
        for enemy in enemies:
            status = "ALIVE" if enemy.get('is_alive', True) else "DEFEATED"
            lines.append(f"- {enemy.get('name', 'Unknown')}: {enemy.get('health', 0)}/{enemy.get('max_health', 0)} HP [{status}]")
        
        return "\n".join(lines)
    
    @staticmethod
    def _format_environment(environment: list) -> str:
        """Format environment list for prompt"""
        if not environment:
            return "Open battlefield with no special features"
        
        lines = []
        for env in environment:
            lines.append(f"- {env.get('name', 'Feature')}: {env.get('description', 'No description')}")
        
        return "\n".join(lines)


# ============================================================================
# RESPONSE PARSING
# ============================================================================

class NarrativeParser:
    """Parse AI-generated narratives"""
    
    @staticmethod
    def parse_narrative_response(ai_response: str) -> Dict[str, Any]:
        """
        Parse AI response into structured format
        
        Expected format:
        Narrative text...
        
        Choices:
        1. Choice one
        2. Choice two
        3. Choice three
        """
        
        lines = ai_response.strip().split('\n')
        
        narrative_lines = []
        choices = []
        in_choices = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Check if we're entering choices section
            if line.lower().startswith('choice') or line.startswith('1.') or line.startswith('- '):
                in_choices = True
            
            if in_choices:
                # Extract choice text
                # Handle formats: "1. Text", "- Text", "Choice: Text"
                choice_text = line
                for prefix in ['1.', '2.', '3.', '4.', '- ', '* ', 'Choice:', 'Option:']:
                    if choice_text.startswith(prefix):
                        choice_text = choice_text[len(prefix):].strip()
                        break
                
                if choice_text and not choice_text.lower().startswith('choice'):
                    choices.append(choice_text)
            else:
                # Narrative text
                narrative_lines.append(line)
        
        # Default choices if none found
        if not choices:
            choices = [
                "Continue forward",
                "Investigate carefully",
                "Rest and recover"
            ]
        
        return {
            "narrative": "\n\n".join(narrative_lines),
            "choices": choices[:4]  # Maximum 4 choices
        }


# ============================================================================
# FALLBACK NARRATIVES
# ============================================================================

class FallbackNarratives:
    """Fallback narratives when AI is unavailable"""
    
    @staticmethod
    def get_fallback_narrative(
        context: Dict[str, Any],
        scenario: str
    ) -> Dict[str, Any]:
        """Get fallback narrative based on context"""
        
        fallbacks = {
            "northern_realms": {
                "narrative": (
                    "The northern winds howl across the frozen peaks. Your breath mists "
                    "in the cold mountain air as you press onward. Ancient ruins dot the "
                    "landscape, remnants of civilizations long forgotten. The weight of "
                    "destiny sits heavy on your shoulders."
                ),
                "choices": [
                    "Explore the ancient ruins",
                    "Continue along the mountain path",
                    "Seek shelter from the cold",
                    "Examine your surroundings carefully"
                ]
            },
            "whispering_town": {
                "narrative": (
                    "The whispers grow louder. They're always there now, just at the edge "
                    "of hearing. The fog rolls in from the sea, thick and unnatural. "
                    "Ashmouth's streets feel wrong - angles that don't quite make sense, "
                    "shadows that move when they shouldn't. Something is very wrong here."
                ),
                "choices": [
                    "Follow the whispers",
                    "Seek answers in the old library",
                    "Confront someone about the truth",
                    "Try to maintain your sanity"
                ]
            },
            "neo_tokyo": {
                "narrative": (
                    "Neon lights flicker in the perpetual rain. Neo-Tokyo never sleeps, "
                    "a sprawling megacity where corporations rule and humanity is optional. "
                    "Your neural implant buzzes with encrypted data. Whatever you've "
                    "stumbled onto, it goes deep. Very deep."
                ),
                "choices": [
                    "Jack into the network",
                    "Meet your contact in the shadows",
                    "Upgrade your cybernetics",
                    "Dig deeper into the conspiracy"
                ]
            }
        }
        
        return fallbacks.get(scenario, fallbacks["northern_realms"])

