"""Textual-based user interface prototype for AI-RPG-Alpha.

Run with:
    $ python -m text_rpg.tui_app

This TUI uses the existing markdown scene files and the lightweight engine
parsers, but handles rendering and input via the Textual framework for a richer
terminal experience (scrolling panes, color themes, keybindings).
"""
from __future__ import annotations

from typing import List

# type: ignore
from textual.app import App, ComposeResult  # type: ignore
from textual.containers import Container  # type: ignore
from textual.widgets import Footer, Header, Static  # type: ignore
from textual.widget import Widget  # type: ignore
from textual.reactive import reactive  # type: ignore

from .character import Character
from .engine import parse_scene_markdown, Scene, Choice, SCENE_DIR

# ------------------------------------------------------------
# Widgets
# ------------------------------------------------------------


class NarrativeView(Static):
    """Displays the narrative text of the current scene."""

    text: reactive[str] = reactive("")

    def render(self):  # type: ignore[override]
        from rich.markdown import Markdown

        return Markdown(self.text)


class ChoiceList(Static):
    """Displays selectable choices."""

    choices: reactive[List[Choice]] = reactive([])
    selected_index: reactive[int] = reactive(0)

    def render(self):  # type: ignore[override]
        from rich.table import Table

        table = Table.grid(padding=1)
        for idx, ch in enumerate(self.choices):
            prefix = "➤" if idx == self.selected_index else " "
            table.add_row(f"{prefix} [{idx+1}] {ch.text}")
        return table


# ------------------------------------------------------------
# Main App
# ------------------------------------------------------------


class RPGApp(App):
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("up", "cursor_up", "Up"),
        ("down", "cursor_down", "Down"),
        ("enter", "confirm", "Select"),
        ("i", "toggle_inventory", "Inventory"),
    ]

    def __init__(self):
        super().__init__()
        self.char = Character(name="Arden", race="Human", char_class="Swordsman")
        self.current_scene_id = "scene_01_prologue"
        self.scene: Scene | None = None

    # -----------------------------
    # Compose UI
    # -----------------------------
    def compose(self) -> ComposeResult:  # type: ignore[override]
        yield Header(show_clock=True)
        with Container():
            self.narrative = NarrativeView()
            self.choice_list = ChoiceList()
            self.inventory_view = Static("", classes="inventory", id="inv")
            self.inventory_view.display = False
            yield self.narrative
            yield self.choice_list
            yield self.inventory_view
        yield Footer()

    # -----------------------------
    # Helpers
    # -----------------------------
    def load_scene(self):
        path = SCENE_DIR / f"{self.current_scene_id}.md"
        self.scene = parse_scene_markdown(path)
        self.narrative.text = f"# {self.scene.scene_id.replace('_', ' ').title()}\n\n" + self.scene.opening
        self.choice_list.choices = self.scene.choices
        self.choice_list.selected_index = 0

    # -----------------------------
    # App lifecycle
    # -----------------------------
    async def on_mount(self):  # type: ignore[override]
        self.load_scene()

    # -----------------------------
    # Keybindings
    # -----------------------------
    def action_cursor_up(self):
        if self.choice_list.selected_index > 0:
            self.choice_list.selected_index -= 1

    def action_cursor_down(self):
        if self.choice_list.selected_index < len(self.choice_list.choices) - 1:
            self.choice_list.selected_index += 1

    def action_confirm(self):
        choice = self.choice_list.choices[self.choice_list.selected_index]

        success = True
        outcome_text = ""
        if choice.ability and choice.dc:
            roll_total = self.char.roll_ability_check(choice.ability)
            dc_req = choice.dc  # TODO: include difficulty scaling
            success = roll_total >= dc_req
            outcome_text = (
                f"\n\n> You roll **{roll_total}** vs DC {dc_req}: "
                + ("**Success**" if success else "**Failure**")
            )

        next_node = None
        if success and choice.success_node:
            next_node = choice.success_node
        elif not success and choice.fail_node:
            next_node = choice.fail_node

        if next_node:
            self.current_scene_id = next_node
            self.load_scene()
            if outcome_text:
                # Prepend outcome to new scene narrative for context
                self.narrative.text = outcome_text + "\n\n" + self.narrative.text
        else:
            # No next node – end path
            self.narrative.text += outcome_text + "\n\n**End of prototype path.**"
            self.choice_list.choices = []

    # -----------------------------
    # Inventory toggle
    # -----------------------------
    def action_toggle_inventory(self):
        inv = "\n".join(f"- {itm}" for itm in self.char.inventory) or "(empty)"
        self.inventory_view.update(f"[bold yellow]Inventory[/]\n{inv}")
        self.inventory_view.display = not self.inventory_view.display


def run():  # pragma: no cover
    RPGApp().run()


if __name__ == "__main__":
    run() 