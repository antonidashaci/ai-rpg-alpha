"""
Side Quests for The Northern Realms
===================================

Additional quests and story branches that expand the game world:
- Guild quests and faction missions
- Personal storylines for NPCs
- Exploration and discovery quests
- Moral choice dilemmas
- Epic side adventures
"""

from .quest_framework import LongFormQuest, QuestMilestone, ChoiceImpact, QuestAct


def create_guild_quest_mage() -> LongFormQuest:
    """
    Mage Guild Quest - Arcane Academy storyline
    A quest about magical research, forbidden knowledge, and academy politics
    """
    milestones = [
        # ACT I: The Academy's Call
        QuestMilestone(
            turn_number=1,
            title="Summons from the Academy",
            description=(
                "A messenger from the Arcane Academy arrives in Ironhold Village. "
                "High Mage Elara requests your presence for an urgent matter of magical research."
            ),
            choices=[
                "Accept the summons and travel to Frostmere",
                "Politely decline - you have other priorities",
                "Ask for more information before deciding"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The Forbidden Library",
            description=(
                "Deep within Frostmere Citadel, Elara shows you ancient texts "
                "describing a powerful artifact that could change the balance of power."
            ),
            choices=[
                "Help research the artifact's location",
                "Warn about the dangers of forbidden magic",
                "Suggest consulting other kingdoms first"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="Academy Intrigue",
            description=(
                "You discover that not all mages in the Academy support Elara's research. "
                "Some believe the artifact should remain lost forever."
            ),
            choices=[
                "Side with Elara and help her research",
                "Investigate the opposition secretly",
                "Propose a compromise solution"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="The Artifact Awakens",
            description=(
                "Your research has located the artifact in ancient ruins. "
                "As you approach, you feel its immense magical power."
            ),
            choices=[
                "Claim the artifact for the Academy",
                "Destroy it to prevent misuse",
                "Use it to gain personal power"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="mage_guild_research",
        title="The Arcane Academy's Secret",
        description=(
            "High Mage Elara summons you to Frostmere Citadel for a matter of great magical importance. "
            "Ancient texts speak of a powerful artifact that could tip the balance in the dragon war."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "A crisp autumn morning in Ironhold Village is interrupted by the arrival of a "
            "robed messenger bearing the seal of Frostmere Citadel. The young mage hands you "
            "a sealed letter with trembling hands.\n\n"
            "'High Mage Elara requires your immediate presence,' he says. 'She speaks of ancient "
            "magics and forgotten knowledge that could change everything.'\n\n"
            "The letter confirms his words - Elara has discovered references to a powerful "
            "artifact in the Academy's forbidden archives. She believes you, the marked one, "
            "are the key to unlocking its secrets.\n\n"
            "The journey to Frostmere Citadel will take you through treacherous mountain passes, "
            "but the promise of greater magical knowledge beckons."
        ),
        possible_endings=[
            "academy_alliance",
            "artifact_destroyed",
            "mage_betrayal",
            "personal_power"
        ],
        tags=["mage_guild", "forbidden_magic", "research", "politics"],
        difficulty="medium",
        estimated_playtime_minutes=45
    )


def create_blacksmith_quest() -> LongFormQuest:
    """
    Blacksmith Guild Quest - Crafting and trade storyline
    A quest about master craftsmanship, trade routes, and economic warfare
    """
    milestones = [
        # ACT I: The Master's Challenge
        QuestMilestone(
            turn_number=1,
            title="The Master Craftsman's Test",
            description=(
                "Grom the Blacksmith approaches you with a proposition. "
                "He's heard of your adventures and wants to test your mettle with a crafting challenge."
            ),
            choices=[
                "Accept the crafting challenge",
                "Ask what he needs in return",
                "Suggest a different kind of test"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The Dragon-Scale Forge",
            description=(
                "Grom reveals his greatest creation - a forge that can work dragon scales. "
                "But he needs rare materials from dangerous locations."
            ),
            choices=[
                "Help gather the rare materials",
                "Question the ethics of dragon-scale crafting",
                "Offer to find alternative materials"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.MODERATE},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="Trade Route Troubles",
            description=(
                "Bandits have been attacking trade caravans carrying Grom's materials. "
                "The blacksmith guild is losing money and influence."
            ),
            choices=[
                "Lead a defense of the next caravan",
                "Investigate who is behind the attacks",
                "Negotiate with the bandits"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="The Masterpiece Revealed",
            description=(
                "With the materials secured, Grom creates a legendary weapon. "
                "Its creation has drawn the attention of nobles and merchants alike."
            ),
            choices=[
                "Claim the weapon for your quest",
                "Sell it to the highest bidder",
                "Gift it to a worthy ally"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="blacksmith_masterpiece",
        title="The Dragon-Scale Blade",
        description=(
            "Master Blacksmith Grom has a proposition for you - help him create a legendary weapon "
            "from dragon scales, and he'll forge you the ultimate blade for your quest against the dragons."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "The clang of hammer on anvil echoes through Ironhold Village as you pass Grom's forge. "
            "The burly blacksmith looks up from his work, wiping sweat from his brow.\n\n"
            "'You there! The marked one!' he calls out. 'I've heard tales of your adventures. "
            "I have a proposition that could benefit us both.'\n\n"
            "Grom explains that he's discovered a way to work dragon scales into weapons, "
            "but he needs help gathering rare materials and protecting his trade routes. "
            "In return, he'll create the ultimate dragon-slaying blade for you.\n\n"
            "The offer is tempting - a master-crafted weapon could turn the tide in your battles. "
            "But working with dragon materials carries its own risks and moral questions."
        ),
        possible_endings=[
            "legendary_weapon",
            "trade_empire",
            "ethical_standoff",
            "betrayed_alliance"
        ],
        tags=["crafting", "trade", "economy", "weapons"],
        difficulty="easy",
        estimated_playtime_minutes=40
    )


def create_political_quest() -> LongFormQuest:
    """
    Political Intrigue Quest - Noble house conflicts
    A quest about kingdom politics, noble house rivalries, and diplomatic maneuvering
    """
    milestones = [
        # ACT I: The Invitation
        QuestMilestone(
            turn_number=1,
            title="Royal Summons",
            description=(
                "A royal messenger delivers an invitation to Ironhold Castle. "
                "King Alaric wishes to discuss 'matters of state' with you privately."
            ),
            choices=[
                "Accept the invitation immediately",
                "Send a messenger asking for details",
                "Visit the castle unannounced"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MAJOR},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="Noble House Conflicts",
            description=(
                "King Alaric reveals that House Shadowblade has been plotting against the crown. "
                "He needs someone trustworthy to investigate without alerting the traitors."
            ),
            choices=[
                "Infiltrate the Shadowblade household",
                "Confront the house leader directly",
                "Gather intelligence from other nobles"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="The Conspiracy Unfolds",
            description=(
                "Your investigation reveals a web of conspiracy involving multiple noble houses. "
                "The Shadowblades are not acting alone - they've formed an alliance against the king."
            ),
            choices=[
                "Expose the conspiracy publicly",
                "Negotiate with the rebel leaders",
                "Pretend to join them to gather more evidence"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=10,
            title="The King's Judgment",
            description=(
                "With evidence in hand, you return to King Alaric. "
                "The fate of the rebel houses hangs in the balance."
            ),
            choices=[
                "Advocate for mercy and reconciliation",
                "Demand harsh punishment for the traitors",
                "Propose a middle ground solution"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="political_conspiracy",
        title="Shadows in the Court",
        description=(
            "King Alaric summons you to Ironhold Castle with grave news. "
            "Whispers of conspiracy and betrayal threaten the stability of the realm."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "The royal messenger who delivers King Alaric's summons is clearly nervous. "
            "He glances around as if expecting trouble, his hand never far from his sword.\n\n"
            "'His Majesty requests your immediate presence at the castle,' he says quietly. "
            "'There are... sensitive matters that require your unique perspective.'\n\n"
            "As you ride toward Ironhold Castle, you wonder what political intrigue awaits. "
            "The king has always been a fair ruler, but court politics can be as dangerous "
            "as any battlefield.\n\n"
            "The castle guards salute as you approach, but you notice some of the nobles "
            "watching you with suspicion. Something is definitely amiss in the court."
        ),
        possible_endings=[
            "kingdom_united",
            "noble_purge",
            "political_reform",
            "royal_downfall"
        ],
        tags=["politics", "intrigue", "nobles", "conspiracy"],
        difficulty="hard",
        estimated_playtime_minutes=50
    )


def create_exploration_quest() -> LongFormQuest:
    """
    Exploration Quest - Ancient ruins and lost civilizations
    A quest about archaeology, ancient mysteries, and forgotten knowledge
    """
    milestones = [
        # ACT I: The Discovery
        QuestMilestone(
            turn_number=1,
            title="Ancient Map Found",
            description=(
                "While exploring the village library, you discover an ancient map "
                "showing the location of long-lost ruins predating even the dragon wars."
            ),
            choices=[
                "Follow the map immediately",
                "Research the ruins' history first",
                "Share the discovery with the Mage Academy"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=5,
            title="The Guardian's Challenge",
            description=(
                "The ruins are protected by ancient magical wards. "
                "A spectral guardian demands you prove your worth before entering."
            ),
            choices=[
                "Solve the guardian's riddle",
                "Battle the spectral guardian",
                "Find an alternative entrance"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=9,
            title="The Chamber of Secrets",
            description=(
                "Deep within the ruins, you find a chamber containing knowledge "
                "that could change the world's understanding of magic and dragons."
            ),
            choices=[
                "Study the knowledge in secret",
                "Share it with the Mage Academy",
                "Use it to gain personal power"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=12,
            title="The Choice of Ages",
            description=(
                "The ancient chamber reveals a terrible truth about the dragon wars. "
                "Your decision here will echo through history."
            ),
            choices=[
                "Reveal the truth to the world",
                "Keep the secret to prevent chaos",
                "Use the knowledge for your quest"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="ancient_ruins_discovery",
        title="The Lost Library of Eldoria",
        description=(
            "An ancient map leads you to forgotten ruins that predate even the oldest dragon legends. "
            "What knowledge lies buried in these depths, and what price will you pay to uncover it?"
        ),
        scenario="northern_realms",
        total_turns=15,
        milestones=milestones,
        opening_narrative=(
            "The village library in Ironhold is a treasure trove of forgotten knowledge. "
            "As you browse the dusty shelves, a loose stone in the wall catches your eye. "
            "Behind it, you find a perfectly preserved map from an age long past.\n\n"
            "The map shows the location of Eldoria - a legendary city said to have been "
            "destroyed in the first dragon wars. According to legend, Eldoria was home "
            "to the greatest mages and scholars of the ancient world.\n\n"
            "The ruins lie in the Whispering Mountains, a place shunned by locals for "
            "generations. Strange lights and eerie sounds are said to emanate from "
            "the area at night.\n\n"
            "This discovery could change everything you know about the Northern Realms' "
            "history. But ancient places often hold ancient dangers."
        ),
        possible_endings=[
            "knowledge_shared",
            "secret_kept",
            "personal_ascension",
            "catastrophic_revelation"
        ],
        tags=["exploration", "ancient_history", "magic", "discovery"],
        difficulty="medium",
        estimated_playtime_minutes=60
    )


def create_dragon_quest() -> LongFormQuest:
    """
    Dragon-Specific Quest - Direct dragon interaction
    A quest focused on diplomacy and understanding with dragonkind
    """
    milestones = [
        # ACT I: The Dragon's Message
        QuestMilestone(
            turn_number=1,
            title="The Dragon's Envoy",
            description=(
                "A young dragon, barely more than a wyrmling, approaches you under a flag of truce. "
                "She carries a message from the dragon elder - they wish to parley."
            ),
            choices=[
                "Accept the invitation to meet",
                "Attack the dragon immediately",
                "Demand proof of peaceful intentions"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=6,
            title="The Elder Dragon's Lair",
            description=(
                "Deep in the mountains, you meet with the ancient dragon elder. "
                "She speaks of the ancient betrayal and offers a path to peace."
            ),
            choices=[
                "Listen to the dragon's history",
                "Demand immediate surrender",
                "Propose a compromise solution"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=11,
            title="The Ancient Treaty",
            description=(
                "The elder dragon reveals the location of an ancient treaty chamber "
                "where humans and dragons once coexisted peacefully."
            ),
            choices=[
                "Seek out the treaty chamber",
                "Use this information against the dragons",
                "Propose a new era of cooperation"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            reveals_information=True,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=15,
            title="A New Beginning",
            description=(
                "In the ancient treaty chamber, you stand at a crossroads. "
                "Peace between humans and dragons hangs in the balance."
            ),
            choices=[
                "Forge a lasting peace treaty",
                "End the dragon threat forever",
                "Create a new balance of power"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="dragon_diplomacy",
        title="Wings of Peace",
        description=(
            "A young dragon approaches under a flag of truce, bearing an invitation from the dragon elder. "
            "Could peace between humans and dragons finally be possible, or is this another trap?"
        ),
        scenario="northern_realms",
        total_turns=18,
        milestones=milestones,
        opening_narrative=(
            "The young dragon lands gracefully in the village square, her scales shimmering "
            "like emeralds in the sunlight. Villagers scatter in panic, but she makes no "
            "aggressive moves.\n\n"
            "'I come under the ancient sign of parley,' she says, her voice surprisingly "
            "melodious for a dragon. 'The elder wishes to speak with the marked one. "
            "There is much you do not know about our kind.'\n\n"
            "She extends a claw bearing a small, intricately carved stone tablet. "
            "The carvings depict humans and dragons standing together - an ancient symbol "
            "of truce that hasn't been used in centuries.\n\n"
            "This could be a trap, or it could be the opportunity for peace that the "
            "Northern Realms have desperately needed. The choice is yours."
        ),
        possible_endings=[
            "eternal_peace",
            "dragon_extinction",
            "fragile_alliance",
            "new_dragon_age"
        ],
        tags=["dragons", "diplomacy", "peace", "history"],
        difficulty="hard",
        estimated_playtime_minutes=75
    )


# ============================================================================
# QUEST LIBRARY EXPANSION
# ============================================================================

class SideQuestLibrary:
    """Library of additional quests for The Northern Realms"""

    @staticmethod
    def get_all_side_quests() -> List[LongFormQuest]:
        """Get all available side quests"""
        return [
            create_guild_quest_mage(),
            create_blacksmith_quest(),
            create_political_quest(),
            create_exploration_quest(),
            create_dragon_quest()
        ]

    @staticmethod
    def get_quest_by_id(quest_id: str) -> Optional[LongFormQuest]:
        """Get specific quest by ID"""
        quests = SideQuestLibrary.get_all_side_quests()
        for quest in quests:
            if quest.quest_id == quest_id:
                return quest
        return None

    @staticmethod
    def get_quests_by_tag(tag: str) -> List[LongFormQuest]:
        """Get quests by tag"""
        quests = SideQuestLibrary.get_all_side_quests()
        return [quest for quest in quests if tag in quest.tags]

    @staticmethod
    def get_random_quest() -> LongFormQuest:
        """Get a random side quest"""
        quests = SideQuestLibrary.get_all_side_quests()
        return random.choice(quests) if quests else None

