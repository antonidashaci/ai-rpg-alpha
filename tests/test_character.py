from text_rpg.character import Character


def test_ability_modifier():
    char = Character(name="Test", race="Human", char_class="Wizard", attributes={"STR": 8, "DEX": 12, "CON": 10, "INT": 16, "WIS": 14, "CHA": 10})
    assert char.ability_modifier("STR") == -1
    assert char.ability_modifier("DEX") == 1
    assert char.ability_modifier("INT") == 3


def test_alignment_adjustment():
    char = Character(name="Test", race="Elf", char_class="Ranger")
    char.adjust_alignment(lc_delta=3, ge_delta=-4)
    assert char.alignment_lc == 3
    assert char.alignment_ge == -4
    assert char.alignment == "Lawful Evil" 