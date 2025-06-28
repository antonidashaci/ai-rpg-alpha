"""Global game state for AI-RPG-Alpha.

This module centralises mutable world variables so that different UI layers
(engine, TUI, future web client) can reference a single source of truth.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GlobalState:
    day: int = 1
    time_of_day: str = "Night"  # "Day" or "Night"
    obelisk_resonance: int = 0   # 0..100

    def toggle_day_night(self) -> None:
        self.time_of_day = "Day" if self.time_of_day == "Night" else "Night"
        if self.time_of_day == "Day":
            self.day += 1

    def add_resonance(self, amount: int) -> None:
        self.obelisk_resonance = max(0, min(100, self.obelisk_resonance + amount)) 