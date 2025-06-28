"""Simple dice-based combat simulator.

Not balanced, intended for early prototype testing.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict

from . import dice
from .character import Character

# ------------------------------------------------------------
# Helper to parse damage strings like "1d6+1"
# ------------------------------------------------------------

def roll_damage_str(dmg: str) -> int:
    match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dmg)
    if not match:
        raise ValueError(f"Invalid damage string: {dmg}")
    num, sides, mod = match.groups()
    total = sum(dice.roll(int(sides)) for _ in range(int(num)))
    if mod:
        total += int(mod)
    return total


@dataclass
class Enemy:
    name: str
    hp: int
    ac: int
    attack_bonus: int
    damage: str
    xp: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Enemy":
        return cls(
            name=data["name"],
            hp=int(data["hp"]),
            ac=int(data["ac"]),
            attack_bonus=int(data["attack_bonus"]),
            damage=data["damage"],
            xp=int(data.get("xp", 0)),
        )

    def attack_roll(self) -> int:
        return dice.d20() + self.attack_bonus

    def roll_damage(self) -> int:
        return roll_damage_str(self.damage)


# ------------------------------------------------------------
# Combat routine
# ------------------------------------------------------------

def simulate_combat(char: Character, enemy: Enemy, verbose: bool = True) -> bool:
    """Returns True if player wins, False if defeated."""
    char_hp = 10 + char.ability_modifier("CON")  # temporary fixed HP
    if verbose:
        print(f"\nEncounter: {enemy.name} (HP {enemy.hp}, AC {enemy.ac})")
        print(f"Your HP: {char_hp}\n")
    turn = 0
    while char_hp > 0 and enemy.hp > 0:
        turn += 1
        if verbose:
            print(f"-- Turn {turn} --")
        # Player attack
        player_roll = char.roll_attack()
        if player_roll >= enemy.ac:
            dmg = char.roll_damage()
            enemy.hp -= dmg
            if verbose:
                print(f"You hit for {dmg} (roll {player_roll}) – enemy HP {enemy.hp}")
        else:
            if verbose:
                print(f"You miss (roll {player_roll})")
        if enemy.hp <= 0:
            break
        # Enemy attack
        enemy_roll = enemy.attack_roll()
        if enemy_roll >= 10 + char.ability_modifier("DEX"):  # player AC simplistic 10+DEX
            dmg_e = enemy.roll_damage()
            char_hp -= dmg_e
            if verbose:
                print(f"{enemy.name} hits you for {dmg_e} (roll {enemy_roll}) – your HP {char_hp}")
        else:
            if verbose:
                print(f"{enemy.name} misses (roll {enemy_roll})")
    if verbose:
        if char_hp > 0:
            print("\nVictory!\n")
        else:
            print("\nDefeat...\n")
    return char_hp > 0 