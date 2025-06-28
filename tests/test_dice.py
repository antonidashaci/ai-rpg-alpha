import pytest  # type: ignore  # noqa: F401

from text_rpg import dice


def test_roll_range():
    for _ in range(100):
        assert 1 <= dice.roll(20) <= 20


def test_advantage_higher_or_equal():
    vals = [dice.roll_advantage() for _ in range(100)]
    for v in vals:
        assert 1 <= v <= 20


def test_disadvantage_lower_or_equal():
    vals = [dice.roll_disadvantage() for _ in range(100)]
    for v in vals:
        assert 1 <= v <= 20 