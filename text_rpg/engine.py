"""Lightweight engine to drive the text-RPG scenes.

For early prototype purposes this module:
1. Loads a markdown scene under ``story/scenes/*.md``
2. Extracts the opening blurb and branching choices via regex.
3. Performs ability checks using :pymod:`text_rpg.character`.
4. Advances to next node (if present) or prints placeholder outcome.

It is intentionally minimal and will evolve once Twine JSON compiler is complete.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.prompt import Prompt

from .character import Character

CONSOLE = Console()
SCENE_DIR = Path(__file__).resolve().parent.parent / "story" / "scenes"

# ------------------------------------------------------------
# Data structures
# ------------------------------------------------------------


@dataclass
class Choice:
    index: int
    text: str
    ability: Optional[str] = None  # e.g. "WIS"
    dc: Optional[int] = None
    success_node: Optional[str] = None
    fail_node: Optional[str] = None


@dataclass
class Scene:
    scene_id: str
    opening: str
    choices: List[Choice]


# ------------------------------------------------------------
# Markdown parser (simple, opinionated)
# ------------------------------------------------------------

_OPENING_RGX = re.compile(r"^>\s*(.*)")
_CHOICE_RGX = re.compile(
    r"^\s*\d+\.\s*\*(.*?)\*\s*→\s*(?:Ability check\s*–\s*(\w+) .*?\(DC\s*(\d+)\))?.*?`([^`]+)`(?:.*?`([^`]+)`)?",
    re.IGNORECASE,
)


def parse_scene_markdown(path: Path) -> Scene:
    """Parse a markdown scene file and return a :class:`Scene`."""
    lines = path.read_text(encoding="utf-8").splitlines()

    opening_lines: List[str] = []
    choices: List[Choice] = []
    in_opening = False

    for line in lines:
        if line.startswith("**Opening Blurb"):
            in_opening = True
            continue
        if in_opening:
            if not line.startswith(">"):
                # End of opening block
                if opening_lines:
                    in_opening = False
                continue
            m = _OPENING_RGX.match(line)
            if m:
                opening_lines.append(m.group(1))
        # choices
        m2 = _CHOICE_RGX.match(line)
        if m2:
            text, ability, dc, succ, fail = m2.groups()
            choices.append(
                Choice(
                    index=len(choices) + 1,
                    text=text.strip(),
                    ability=ability,
                    dc=int(dc) if dc else None,
                    success_node=succ,
                    fail_node=fail,
                )
            )

    if not opening_lines:
        raise ValueError(f"Opening paragraph not found in {path}")
    if not choices:
        raise ValueError(f"No branching choices found in {path}")

    return Scene(path.stem, "\n".join(opening_lines), choices)


# ------------------------------------------------------------
# Game Engine (CLI)
# ------------------------------------------------------------


class GameEngine:
    def __init__(self, protagonist: Character):
        self.char = protagonist
        self.current_scene_id = "scene_01_prologue"
        self.time_of_day = "Night"  # Start at night per prologue
        self.day_count = 1

    # ------------------------
    # Utility
    # ------------------------
    def toggle_day_night(self):
        self.time_of_day = "Day" if self.time_of_day == "Night" else "Night"

    def difficulty_offset(self) -> int:
        """Return extra DC based on level tiers (Tier1=0, Tier2=+2, Tier3=+4)."""
        if self.char.level <= 3:
            return 0
        if self.char.level <= 6:
            return 2
        if self.char.level <= 10:
            return 4
        return 6

    # ------------------------
    # Main loop
    # ------------------------
    def run(self):
        while True:
            scene_path = SCENE_DIR / f"{self.current_scene_id}.md"
            if not scene_path.exists():
                CONSOLE.print(f"[bold red]Scene not found:[/] {self.current_scene_id}")
                sys.exit(1)
            scene = parse_scene_markdown(scene_path)
            self.render_scene(scene)

            # gather choice
            choice_num = Prompt.ask("\nChoose", choices=[str(c.index) for c in scene.choices], default="1")
            choice = scene.choices[int(choice_num) - 1]
            success = None
            if choice.ability and choice.dc:
                roll_total = self.char.roll_ability_check(choice.ability)
                dc_req = choice.dc + self.difficulty_offset()
                success = roll_total >= dc_req
                outcome = "SUCCESS" if success else "FAILURE"
                CONSOLE.print(f"[cyan]\nYou roll {roll_total} vs DC {dc_req}: {outcome}[/]\n")
            else:
                success = True  # no check implies auto success for now

            # advance node (placeholder)
            next_node = choice.success_node if success else choice.fail_node
            if next_node:
                self.current_scene_id = next_node
            else:
                CONSOLE.print("[bold yellow]End of prototype path. Thanks for playing![/]")
                break

            # simple day/night toggle each node
            self.toggle_day_night()

    # ------------------------
    # Rendering helpers
    # ------------------------
    def render_scene(self, scene: Scene) -> None:
        CONSOLE.rule(f"[bold magenta]{scene.scene_id.replace('_', ' ').title()} — {self.time_of_day}, Day {self.day_count}")
        CONSOLE.print(scene.opening)

        for choice in scene.choices:
            CONSOLE.print(f"[green]{choice.index}[/]. {choice.text}")


# ------------------------------------------------------------
# CLI entry
# ------------------------------------------------------------

def demo():
    char = Character(name="Arden", race="Human", char_class="Swordsman")
    engine = GameEngine(char)
    engine.run()


if __name__ == "__main__":
    demo() 