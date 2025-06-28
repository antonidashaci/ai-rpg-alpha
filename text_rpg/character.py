"""Character model for the text RPG.

Implements D&D-like attributes and simple skill/ability check helpers.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from . import dice

ABILITIES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")


@dataclass
class Character:
    name: str
    race: str
    char_class: str
    level: int = 1
    attributes: Dict[str, int] = field(default_factory=lambda: {a: 10 for a in ABILITIES})
    skills: Dict[str, bool] = field(default_factory=dict)  # skill name -> proficiency bool
    inventory: List[str] = field(default_factory=list)

    # Alignment represented as two axes: law_chaos (-5..+5), good_evil (-5..+5)
    alignment_lc: int = 0  # -5 chaos, +5 law
    alignment_ge: int = 0  # -5 evil, +5 good

    def ability_modifier(self, ability: str) -> int:
        """Return the D&D-style ability modifier for the given ability code."""
        ability = ability.upper()
        if ability not in ABILITIES:
            raise KeyError(f"Unknown ability '{ability}'. Must be one of {ABILITIES}.")
        score = self.attributes.get(ability, 10)
        return (score - 10) // 2

    # ---------------------------------------------------------------------
    # Checks & rolls
    # ---------------------------------------------------------------------
    def roll_ability_check(
        self,
        ability: str,
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> int:
        """Perform an ability check and return the total (d20 + modifier)."""
        if advantage and disadvantage:
            # They cancel out per 5e rules
            advantage = disadvantage = False

        if advantage:
            base = dice.roll_advantage()
        elif disadvantage:
            base = dice.roll_disadvantage()
        else:
            base = dice.d20()
        return base + self.ability_modifier(ability)

    # ------------------------------------------------------------------
    # Alignment helpers
    # ------------------------------------------------------------------
    @property
    def alignment(self) -> str:
        """Return textual representation like 'Lawful Good', 'Chaotic Neutral'."""
        lc = "Lawful" if self.alignment_lc > 1 else "Chaotic" if self.alignment_lc < -1 else "Neutral"
        ge = (
            "Good" if self.alignment_ge > 1 else "Evil" if self.alignment_ge < -1 else "Neutral"
        )
        return f"{lc} {ge}"

    def adjust_alignment(self, lc_delta: int = 0, ge_delta: int = 0) -> None:
        """Shift alignment values keeping them within -5..+5 range."""
        self.alignment_lc = max(-5, min(5, self.alignment_lc + lc_delta))
        self.alignment_ge = max(-5, min(5, self.alignment_ge + ge_delta))

    # ------------------------------------------------------------------
    # Inventory helpers
    # ------------------------------------------------------------------
    def add_item(self, item_name: str) -> None:
        """Add an item to the character's inventory if not already present."""
        if item_name not in self.inventory:
            self.inventory.append(item_name)

    def has_item(self, item_name: str) -> bool:
        return item_name in self.inventory 