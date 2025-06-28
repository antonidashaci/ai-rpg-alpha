"""Dice rolling utilities for the text RPG.

Supports d20 rolls with optional advantage/disadvantage mechanics.
"""
from __future__ import annotations

import random
from typing import List

__all__ = [
    "roll",
    "d20",
    "roll_advantage",
    "roll_disadvantage",
]


def roll(sides: int = 20) -> int:
    """Roll a single die with *sides* number of faces (default 20)."""
    if sides < 2:
        raise ValueError("A die must have at least 2 sides.")
    result = random.randint(1, sides)
    return result


d20 = lambda: roll(20)  # noqa: E731


def roll_advantage(sides: int = 20) -> int:
    """Return the highest of two rolls (advantage rule)."""
    results: List[int] = [roll(sides), roll(sides)]
    return max(results)


def roll_disadvantage(sides: int = 20) -> int:
    """Return the lowest of two rolls (disadvantage rule)."""
    results: List[int] = [roll(sides), roll(sides)]
    return min(results) 