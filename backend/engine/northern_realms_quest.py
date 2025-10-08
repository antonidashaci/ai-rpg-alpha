"""
The Northern Realms - Complete Quest
=====================================

Epic 40-turn fantasy quest with:
- Dragon prophecy storyline
- Kingdom politics and alliances
- Ancient magic and artifacts
- Dragon encounters
- Political intrigue
"""

from .quest_framework import (
    LongFormQuest, QuestMilestone, ChoiceImpact, QuestAct
)


def create_northern_realms_quest() -> LongFormQuest:
    """
    The Dragon's Prophecy - Complete 40-turn epic fantasy quest
    
    A hero marked by fate must unite fractured kingdoms against
    an awakening dragon threat while navigating political intrigue
    and uncovering ancient prophecies.
    """
    
    milestones = [
        # ACT I: SETUP (Turns 1-15) - The Prophecy Awakens
        QuestMilestone(
            turn_number=1,
            title="The Mark of Destiny",
            description=(
                "You wake to find a glowing dragon mark burning on your hand. "
                "The village elder speaks of ancient prophecies—a chosen one "
                "who will unite the kingdoms against the coming storm."
            ),
            choices=[
                "Seek counsel from the Kingdom Mages",
                "Travel to Ironhold Castle to meet the King",
                "Investigate the ancient dragon ruins alone"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=5,
            title="The Fractured Kingdoms",
            description=(
                "You learn the kingdoms are divided: Ironhold, Stormwatch, and Frostmere "
                "refuse to unite despite dragon sightings. Each blames the others for past betrayals."
            ),
            choices=[
                "Attempt to broker peace between the kingdoms",
                "Side with one kingdom to gain their trust",
                "Focus on gathering allies regardless of politics"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),
        
        QuestMilestone(
            turn_number=9,
            title="First Dragon Sighting",
            description=(
                "A dragon attacks a northern village. You arrive to find devastation. "
                "Survivors speak of a massive red wyrm—Crimsonwing, thought extinct for centuries."
            ),
            choices=[
                "Track the dragon to its lair",
                "Help rebuild and defend the village",
                "Seek ancient dragon-slaying weapons"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.MAJOR},
            triggers_combat=True,
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=15,
            title="The Ancient Prophecy Revealed",
            description=(
                "In the depths of the Ironhold library, you discover the full prophecy: "
                "'When the mark awakens, the chosen must unite three kingdoms under one banner, "
                "or all shall burn.' [ACT I FINALE]"
            ),
            choices=[
                "Share the prophecy with all kingdoms",
                "Keep it secret to avoid panic",
                "Use the prophecy to your advantage"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        ),
        
        # ACT II: PURSUIT (Turns 16-30) - The Dragon War
        QuestMilestone(
            turn_number=18,
            title="The Dragon Council",
            description=(
                "You discover dragons are not mindless beasts—they're ancient, intelligent, "
                "and they remember the humans who betrayed them 500 years ago."
            ),
            choices=[
                "Seek peace with the dragons",
                "Prepare for total war",
                "Find the truth about the ancient betrayal"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=22,
            title="Political Betrayal",
            description=(
                "One of the kingdoms plots against you. Assassins strike in the night. "
                "Trust is shattered. The alliance teeters on collapse."
            ),
            choices=[
                "Expose the traitors publicly",
                "Deal with them quietly",
                "Use this to consolidate power"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=4
        ),
        
        QuestMilestone(
            turn_number=25,
            title="The Dragonlord Awakens",
            description=(
                "The ancient Dragonlord, Blackfang, rises from his mountain tomb. "
                "He is the father of all dragons, and he seeks revenge for crimes long forgotten."
            ),
            choices=[
                "Challenge Blackfang to single combat",
                "Rally the kingdoms for a united assault",
                "Seek the legendary Dragonbane sword"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=28,
            title="The Battle of Stormwatch",
            description=(
                "Dragons descend upon Stormwatch Keep. Thousands of lives hang in the balance. "
                "This is your moment to prove the prophecy true."
            ),
            choices=[
                "Lead the defense personally",
                "Command from the rear with strategic overview",
                "Attempt a desperate strike at Blackfang himself"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=5
        ),
        
        # ACT III: CLIMAX (Turns 31-40) - The Final Choice
        QuestMilestone(
            turn_number=31,
            title="The Truth of the Mark",
            description=(
                "Your dragon mark is not a blessing—it's a bond. You carry dragon blood. "
                "You are both human and dragon, the key to peace... or ultimate destruction. [CLIMAX BEGINS]"
            ),
            choices=[
                "Embrace your dragon nature",
                "Reject the dragon within",
                "Seek balance between both natures"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=35,
            title="The Final Confrontation",
            description=(
                "You stand before Blackfang in his lair. The kingdoms await your return. "
                "The fate of an entire age rests on what happens next."
            ),
            choices=[
                "Convince Blackfang that peace is possible",
                "Slay Blackfang and end the dragon threat forever",
                "Offer yourself as a bridge between species"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=5
        ),
        
        QuestMilestone(
            turn_number=40,
            title="The Age of Unity",
            description=(
                "The dust settles. Dragons and humans stand at a crossroads. "
                "Your choices have led to this moment. The future is in your hands."
            ),
            choices=[
                "Forge a lasting peace—the Age of Unity begins",
                "Rule as Dragonlord—unite all under your dominion",
                "Sacrifice yourself to seal the dragons away forever"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            reveals_information=True,
            narrative_weight=5
        )
    ]
    
    quest = LongFormQuest(
        quest_id="northern_realms_dragon_prophecy",
        title="The Dragon's Prophecy",
        description=(
            "Ancient prophecies speak of a chosen one marked by dragons who will unite "
            "the fractured kingdoms against an ancient threat. Dragons thought extinct "
            "for centuries are awakening, and only you can prevent the coming war—or "
            "embrace it."
        ),
        scenario="northern_realms",
        total_turns=40,
        milestones=milestones,
        opening_narrative=(
            "The northern winds howl across the peaks of Ironhold as you wake to searing pain. "
            "Your right hand burns with an otherworldly fire—a glowing mark in the shape of "
            "a dragon's claw has appeared overnight.\n\n"
            
            "The village elder, Aldric, examines the mark with wide eyes. 'The prophecy,' he whispers. "
            "'After five hundred years, the mark has chosen. You are the one who will either save "
            "the Northern Realms... or watch them burn.'\n\n"
            
            "Tales speak of dragons awakening in the far mountains. The three great kingdoms—"
            "Ironhold, Stormwatch, and Frostmere—refuse to unite despite the threat. Ancient "
            "grudges run deep. But you... you carry the mark of destiny.\n\n"
            
            "Your journey begins in Ironhold Village, but it will take you across the entire realm. "
            "Dragons stir in their ancient lairs. Kings plot in their castles. And you stand at "
            "the center of it all, marked by fate itself.\n\n"
            
            "The prophecy is clear: Unite the kingdoms, or all shall fall to dragonfire."
        ),
        possible_endings=[
            "age_of_unity",           # Lasting peace between dragons and humans
            "dragonlord_emperor",     # Player becomes supreme ruler
            "hero_sacrifice",         # Player sacrifices self to seal dragons
            "dragon_ascension",       # Player becomes dragon, rules from above
            "kingdoms_victorious",    # Humans win, dragons extinct
            "dragon_supremacy"        # Dragons win, humans subjugated
        ],
        tags=["epic_fantasy", "dragons", "prophecy", "politics", "long_form"],
        difficulty="medium",
        estimated_playtime_minutes=150
    )
    
    return quest

