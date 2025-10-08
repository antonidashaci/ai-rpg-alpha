"""
Skyrim-Style Quests for The Northern Realms
==========================================

Inspired by Skyrim quest design philosophy:
- Multiple quest types (guild, faction, exploration, moral dilemmas)
- Varied length and difficulty
- Meaningful choices and consequences
- Connection to main storyline
- Rich world-building and lore

All quest names and elements are original to The Northern Realms setting.
"""

from .quest_framework import LongFormQuest, QuestMilestone, ChoiceImpact, QuestAct
from .side_quests import SideQuestLibrary


def create_fighters_guild_quest() -> LongFormQuest:
    """
    Fighters Guild Quest - Mercenary company storyline
    A quest about joining a mercenary company and rising through the ranks
    """
    milestones = [
        # ACT I: Joining the Company
        QuestMilestone(
            turn_number=1,
            title="The Mercenary's Call",
            description=(
                "Captain Thorne approaches you at the Stormwatch tavern. "
                "The Iron Wolves mercenary company is looking for skilled fighters like you."
            ),
            choices=[
                "Join the Iron Wolves immediately",
                "Ask for more details about the company",
                "Decline politely but stay in contact"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The First Contract",
            description=(
                "Your first mission: escort a merchant caravan through bandit territory. "
                "The Iron Wolves have a reputation to maintain."
            ),
            choices=[
                "Lead the escort mission aggressively",
                "Scout ahead for potential threats",
                "Negotiate safe passage with local bandits"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="Internal Conflicts",
            description=(
                "Not all members of the Iron Wolves are happy with your rapid advancement. "
                "Some veterans see you as a threat to their position."
            ),
            choices=[
                "Confront the dissenters directly",
                "Prove your worth through deeds",
                "Build alliances within the company"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MODERATE, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="The Captain's Test",
            description=(
                "Captain Thorne gives you a final test - lead a mission that could make or break "
                "the company's reputation in the Northern Realms."
            ),
            choices=[
                "Accept the high-stakes mission",
                "Question the wisdom of the assignment",
                "Propose an alternative approach"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            triggers_combat=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="iron_wolves_ascension",
        title="The Iron Wolves",
        description=(
            "Join the legendary Iron Wolves mercenary company and rise through their ranks. "
            "Your combat prowess and leadership skills will be tested as you take on increasingly "
            "dangerous contracts across the Northern Realms."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "The Stormwatch tavern is filled with the rough laughter of mercenaries and the "
            "clink of tankards. Captain Thorne, a scarred veteran with a reputation for getting "
            "results, slides into the seat across from you.\n\n"
            "'I've heard about you, marked one,' he says, his voice like gravel. 'The Iron Wolves "
            "could use someone with your... unique abilities. We're not just sellswords - "
            "we're the best damn fighting force in the Northern Realms.'\n\n"
            "He explains that the Iron Wolves are more than just mercenaries. They're a brotherhood "
            "(and sisterhood) of warriors who take on the jobs others won't touch. Recent losses "
            "have created an opening for new blood.\n\n"
            "The offer is tempting - steady work, good pay, and the chance to hone your combat "
            "skills against real threats. But joining a mercenary company means walking a fine "
            "line between honor and pragmatism."
        ),
        possible_endings=[
            "company_leader",
            "honorable_discharge",
            "company_dissolution",
            "mercenary_legend"
        ],
        tags=["fighters_guild", "mercenary", "combat", "leadership"],
        difficulty="medium",
        estimated_playtime_minutes=50
    )


def create_mages_academy_quest() -> LongFormQuest:
    """
    Mages Academy Quest - Arcane research and magical politics
    A quest about joining the magical academy and dealing with arcane politics
    """
    milestones = [
        # ACT I: The Academy's Interest
        QuestMilestone(
            turn_number=1,
            title="The Archmage's Invitation",
            description=(
                "High Mage Elara sends a formal invitation to Frostmere Citadel. "
                "The Arcane Academy has taken notice of your magical abilities."
            ),
            choices=[
                "Accept the invitation to study",
                "Politely decline the offer",
                "Ask for time to consider"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=5,
            title="The Arcane Trials",
            description=(
                "To join the Academy, you must pass three trials that test your magical knowledge, "
                "control, and creativity. Failure means being turned away."
            ),
            choices=[
                "Focus on theoretical knowledge",
                "Emphasize practical spellcasting",
                "Combine both approaches"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=9,
            title="Academy Politics",
            description=(
                "The Academy is divided between traditionalists who fear your dragon mark "
                "and progressives who see it as a sign of destiny."
            ),
            choices=[
                "Side with the traditional mages",
                "Support the progressive faction",
                "Remain neutral and focus on research"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=12,
            title="The Forbidden Experiment",
            description=(
                "Elara proposes an experiment that could unlock new magical knowledge "
                "but carries tremendous risk to the Academy and the Northern Realms."
            ),
            choices=[
                "Support the dangerous research",
                "Sabotage the experiment",
                "Find a safer alternative approach"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="frostmere_academy",
        title="The Arcane Academy",
        description=(
            "Join the prestigious Frostmere Academy of Magic and navigate the complex politics "
            "of arcane research. Your dragon mark makes you both a curiosity and a potential threat "
            "in the eyes of the established magical community."
        ),
        scenario="northern_realms",
        total_turns=15,
        milestones=milestones,
        opening_narrative=(
            "A raven lands on your windowsill bearing a message sealed with the frost crystal "
            "emblem of the Arcane Academy. High Mage Elara's elegant script invites you to "
            "Frostmere Citadel for 'a matter of great magical significance.'\n\n"
            "The Academy has long been a center of magical learning in the Northern Realms, "
            "training mages from all three kingdoms. Their libraries contain knowledge dating "
            "back to before the dragon wars.\n\n"
            "But the Academy is also a hotbed of political intrigue. Different factions vie for "
            "control of research funding and magical resources. Your unique connection to dragon "
            "magic makes you both valuable and dangerous in their eyes.\n\n"
            "Accepting this invitation means entering a world of arcane politics where knowledge "
            "is power and power is everything."
        ),
        possible_endings=[
            "academy_master",
            "research_banned",
            "magical_revolution",
            "ancient_knowledge"
        ],
        tags=["mages_guild", "magic", "politics", "research"],
        difficulty="hard",
        estimated_playtime_minutes=65
    )


def create_shadow_hand_quest() -> LongFormQuest:
    """
    Shadow Hand Quest - Thieves guild style criminal organization
    A quest about joining a criminal organization and moral compromises
    """
    milestones = [
        # ACT I: The First Job
        QuestMilestone(
            turn_number=1,
            title="The Shadow's Offer",
            description=(
                "A hooded figure approaches you in a dark alley. "
                "The Shadow Hand, a secretive organization, has taken notice of your skills."
            ),
            choices=[
                "Accept their offer of employment",
                "Reject them outright",
                "Pretend to accept and investigate"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MAJOR},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The Initiation Test",
            description=(
                "To prove your worth, you're given a seemingly simple task: "
                "steal a valuable item from a heavily guarded location."
            ),
            choices=[
                "Plan an elaborate heist",
                "Use stealth and misdirection",
                "Create a distraction and grab-and-run"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="Internal Betrayal",
            description=(
                "Someone within the Shadow Hand is selling information to rival organizations. "
                "You must find the traitor before the entire operation is compromised."
            ),
            choices=[
                "Set a trap for the traitor",
                "Investigate discreetly",
                "Confront suspects directly"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="The Big Score",
            description=(
                "The Shadow Hand's leader reveals their greatest plan yet - "
                "a heist that could change the balance of power in the Northern Realms."
            ),
            choices=[
                "Lead the operation",
                "Betray them to the authorities",
                "Find a way to minimize the damage"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            triggers_combat=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="shadow_hand_infiltration",
        title="The Shadow Hand",
        description=(
            "Become involved with the mysterious Shadow Hand, a criminal organization that operates "
            "in the shadows of the Northern Realms. Their skills in stealth and subterfuge could "
            "prove invaluable, but at what moral cost?"
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "The alley behind the Ironhold tavern is darker than it should be, as if the shadows "
            "themselves are watching you. A figure emerges from the gloom, cloaked and hooded.\n\n"
            "'We've been watching you, marked one,' the figure whispers. 'The Shadow Hand has need "
            "of someone with your... particular talents. Discretion. Power. The ability to walk "
            "where others cannot.'\n\n"
            "The Shadow Hand is a legend in the Northern Realms - a criminal organization that "
            "specializes in high-stakes theft, espionage, and sabotage. They're said to have "
            "agents in every major city and connections to every noble house.\n\n"
            "Joining them would mean access to information and resources that could help your quest, "
            "but it would also mean compromising your principles and potentially making enemies "
            "of powerful people."
        ),
        possible_endings=[
            "shadow_master",
            "betrayed_alliance",
            "criminal_empire",
            "redemption_arc"
        ],
        tags=["thieves_guild", "criminal", "stealth", "moral_dilemma"],
        difficulty="hard",
        estimated_playtime_minutes=55
    )


def create_artifact_hunt_quest() -> LongFormQuest:
    """
    Artifact Hunt Quest - Moral dilemma and ancient power
    A quest about hunting for a powerful artifact with dangerous consequences
    """
    milestones = [
        # ACT I: The Vision
        QuestMilestone(
            turn_number=1,
            title="The Dream of Power",
            description=(
                "You experience a vivid dream of an ancient artifact calling to you. "
                "The vision shows it hidden in ruins that predate the dragon wars."
            ),
            choices=[
                "Seek out the ruins immediately",
                "Consult with mages about the vision",
                "Ignore the dream as fantasy"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MINOR},
            reveals_information=True,
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=5,
            title="The Guardian's Riddle",
            description=(
                "The ruins are protected by ancient magical wards. "
                "A spectral guardian poses riddles that test your wisdom and resolve."
            ),
            choices=[
                "Answer the riddles logically",
                "Use magic to force your way through",
                "Search for an alternative entrance"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            triggers_combat=False,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=8,
            title="The Artifact's Temptation",
            description=(
                "The artifact reveals its true nature - it grants immense power but at a terrible cost. "
                "It offers you a choice between personal gain and the greater good."
            ),
            choices=[
                "Claim the artifact's power",
                "Destroy it to prevent misuse",
                "Seal it away for future generations"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=11,
            title="The Price of Power",
            description=(
                "Your choice regarding the artifact has consequences that ripple through "
                "the Northern Realms. The kingdoms react to your newfound power or wisdom."
            ),
            choices=[
                "Use the power to unite the kingdoms",
                "Keep it secret to avoid chaos",
                "Share the knowledge with trusted allies"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="ancient_artifact_hunt",
        title="The Crown of Eternity",
        description=(
            "Visions lead you to seek an ancient artifact of immense power. "
            "The Crown of Eternity was created before the dragon wars and holds secrets "
            "that could change the fate of the Northern Realms forever."
        ),
        scenario="northern_realms",
        total_turns=13,
        milestones=milestones,
        opening_narrative=(
            "Sleep brings no rest tonight. Instead, you dream of a golden crown floating in "
            "darkness, whispering promises of power and knowledge. The vision shows ancient "
            "ruins hidden in the Whispering Mountains.\n\n"
            "The Crown of Eternity - you recognize the name from half-remembered legends. "
            "It was said to be created by the first mages, granting dominion over time itself. "
            "Lost during the dragon wars, it's been sought by kings and mages for centuries.\n\n"
            "The dream feels different from normal visions. There's a compulsion to it, "
            "an urgency that suggests the crown itself is calling to you through your "
            "dragon mark.\n\n"
            "Seeking this artifact could give you the power to end the dragon threat once "
            "and for all, but ancient magic always comes with a price."
        ),
        possible_endings=[
            "eternal_ruler",
            "artifact_destroyed",
            "balanced_power",
            "catastrophic_failure"
        ],
        tags=["artifact_hunt", "ancient_magic", "moral_dilemma", "power"],
        difficulty="epic",
        estimated_playtime_minutes=70
    )


def create_companion_quest() -> LongFormQuest:
    """
    Companion Quest - Personal storyline for a companion character
    A quest about helping a companion resolve their personal demons
    """
    milestones = [
        # ACT I: The Companion's Secret
        QuestMilestone(
            turn_number=1,
            title="A Troubled Ally",
            description=(
                "One of your companions confides in you about a personal matter "
                "that's been haunting them since before they joined your quest."
            ),
            choices=[
                "Offer to help immediately",
                "Give them space to work it out",
                "Investigate discreetly"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The Hidden Past",
            description=(
                "You learn that your companion was involved in events from their past "
                "that still affect them deeply. The truth is more complicated than it seems."
            ),
            choices=[
                "Support their version of events",
                "Seek out the other side of the story",
                "Encourage forgiveness and moving on"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MAJOR},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="Confrontation",
            description=(
                "Your companion must face their past directly. "
                "The confrontation could strengthen or break your relationship."
            ),
            choices=[
                "Stand by their side",
                "Let them face it alone",
                "Try to mediate the conflict"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="Resolution",
            description=(
                "The personal crisis comes to a head. "
                "Your companion's future - and your relationship - hangs in the balance."
            ),
            choices=[
                "Support their chosen path",
                "Try to change their mind",
                "Accept whatever decision they make"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="companion_redemption",
        title="Shadows of the Past",
        description=(
            "A close companion reveals a personal secret that's been haunting them. "
            "Helping them resolve their past could strengthen your bond or create new conflicts "
            "that affect your entire quest."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "Your companion pulls you aside during a quiet moment at camp. Their usual "
            "confident demeanor is replaced by uncertainty and pain.\n\n"
            "'There's something I need to tell you,' they say quietly. 'Something from my past "
            "that I've never told anyone. It... it might affect our quest, and I can't keep "
            "carrying this burden alone.'\n\n"
            "They explain that before joining your quest, they were involved in events that "
            "still haunt them. The details are vague at first, but you can tell this secret "
            "has been eating at them for a long time.\n\n"
            "Helping them resolve this personal crisis could strengthen your relationship "
            "and provide valuable insights, but it might also create complications for "
            "your main quest against the dragons."
        ),
        possible_endings=[
            "unbreakable_bond",
            "parting_ways",
            "redeemed_past",
            "shared_burden"
        ],
        tags=["companion", "personal", "redemption", "relationship"],
        difficulty="medium",
        estimated_playtime_minutes=45
    )


def create_world_event_quest() -> LongFormQuest:
    """
    World Event Quest - Festival and celebration storyline
    A quest about participating in a major world event
    """
    milestones = [
        # ACT I: The Festival Invitation
        QuestMilestone(
            turn_number=1,
            title="The Grand Festival",
            description=(
                "Ironhold is hosting the Grand Festival of Unity, a celebration that brings "
                "together all three kingdoms for games, trade, and diplomacy."
            ),
            choices=[
                "Attend as a participant",
                "Attend as an observer",
                "Skip the festival entirely"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.MINOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=3,
            title="The Games Begin",
            description=(
                "The festival features competitions in combat, magic, and strategy. "
                "Your reputation precedes you - you're expected to participate."
            ),
            choices=[
                "Compete in the combat tournament",
                "Enter the magical contest",
                "Focus on diplomatic negotiations"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=6,
            title="Political Maneuvering",
            description=(
                "The festival becomes a hotbed of political intrigue. "
                "Representatives from all kingdoms are present, and tensions are high."
            ),
            choices=[
                "Act as a mediator between kingdoms",
                "Support your allied kingdom",
                "Expose political machinations"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=9,
            title="The Grand Finale",
            description=(
                "The festival culminates in a grand ceremony. "
                "Your actions throughout the event will determine its outcome."
            ),
            choices=[
                "Give a unifying speech",
                "Challenge the political status quo",
                "Support traditional values"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="grand_festival_unity",
        title="The Grand Festival",
        description=(
            "Attend the legendary Grand Festival of Unity in Ironhold Castle. "
            "This massive celebration brings together all three kingdoms for competitions, "
            "trade, and political maneuvering that could change the Northern Realms forever."
        ),
        scenario="northern_realms",
        total_turns=10,
        milestones=milestones,
        opening_narrative=(
            "Banners fly from every tower in Ironhold as the city prepares for the Grand Festival "
            "of Unity. This ancient tradition, revived after decades of division, brings together "
            "representatives from all three kingdoms.\n\n"
            "King Alaric has declared this festival open to all - nobles, merchants, mages, "
            "and even common folk. There will be tournaments of combat and magic, trade fairs, "
            "diplomatic meetings, and celebrations that last from dawn until the stars fade.\n\n"
            "Your presence is requested - as the marked one, you're seen as a symbol of hope "
            "for unity. But festivals like this are also perfect opportunities for political "
            "intrigue and personal advancement.\n\n"
            "The festival could be a chance to build alliances, gather information, and "
            "advance your quest against the dragons. Or it could become a powder keg of "
            "old grudges and new conflicts."
        ),
        possible_endings=[
            "unified_realms",
            "festival_chaos",
            "political_victory",
            "unexpected_alliance"
        ],
        tags=["festival", "politics", "celebration", "unity"],
        difficulty="easy",
        estimated_playtime_minutes=35
    )


def create_dungeon_exploration_quest() -> LongFormQuest:
    """
    Dungeon Exploration Quest - Classic dungeon crawl with puzzles and combat
    A quest about exploring dangerous ruins and facing ancient threats
    """
    milestones = [
        # ACT I: The Entrance
        QuestMilestone(
            turn_number=1,
            title="The Forbidden Ruins",
            description=(
                "Ancient ruins have been discovered in the wilderness. "
                "Local legends speak of treasures and terrors within."
            ),
            choices=[
                "Enter the ruins immediately",
                "Study the ruins from afar first",
                "Seek guidance from local experts"
            ],
            choice_impacts={0: ChoiceImpact.MODERATE, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MINOR},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The First Guardian",
            description=(
                "The entrance is guarded by a magical construct. "
                "It demands a test of worth before allowing passage."
            ),
            choices=[
                "Solve the guardian's puzzle",
                "Battle the construct",
                "Find a way around the guardian"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            triggers_combat=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="The Central Chamber",
            description=(
                "Deep within the ruins, you find a chamber filled with ancient knowledge "
                "and surrounded by deadly traps."
            ),
            choices=[
                "Study the ancient texts",
                "Focus on disarming the traps",
                "Search for the chamber's guardian"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=10,
            title="The Final Revelation",
            description=(
                "The ruins reveal their greatest secret - knowledge that could "
                "change everything you know about the dragon prophecy."
            ),
            choices=[
                "Embrace the new knowledge",
                "Reject it as dangerous heresy",
                "Share it with trusted allies only"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="forgotten_ruins_exploration",
        title="The Forgotten Ruins",
        description=(
            "Explore ancient ruins that predate even the oldest dragon legends. "
            "What knowledge lies buried in these depths, and what guardians protect "
            "secrets that could change the fate of the Northern Realms?"
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "A weathered map you found in the village library leads you to these forgotten ruins. "
            "The stones are older than any castle in the Northern Realms, covered in runes that "
            "no living scholar can fully decipher.\n\n"
            "Local villagers speak of strange lights and eerie sounds emanating from the ruins "
            "at night. Some say the place is cursed, others claim it holds treasures beyond "
            "imagination.\n\n"
            "The entrance is partially collapsed, but you can see carved reliefs depicting "
            "dragons and humans working together - an image that hasn't been seen since before "
            "the great betrayal.\n\n"
            "Exploring these ruins could provide crucial insights into the dragon prophecy, "
            "but ancient places often hold ancient dangers."
        ),
        possible_endings=[
            "ancient_alliance",
            "catastrophic_awakening",
            "forbidden_knowledge",
            "ruins_collapse"
        ],
        tags=["exploration", "dungeon", "ancient_history", "puzzles"],
        difficulty="medium",
        estimated_playtime_minutes=50
    )


def create_moral_dilemma_quest() -> LongFormQuest:
    """
    Moral Dilemma Quest - Tough choices with no easy answers
    A quest about making difficult moral decisions that affect multiple lives
    """
    milestones = [
        # ACT I: The Village Crisis
        QuestMilestone(
            turn_number=1,
            title="The Plague Village",
            description=(
                "You discover a village suffering from a mysterious plague. "
                "The villagers beg for your help, but the situation is dire."
            ),
            choices=[
                "Investigate the source of the plague",
                "Quarantine the village immediately",
                "Seek help from the Mage Academy"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.MODERATE},
            narrative_weight=3
        ),

        QuestMilestone(
            turn_number=4,
            title="The Hidden Truth",
            description=(
                "Your investigation reveals the plague's source - "
                "a deliberate act by someone with a grudge against the village."
            ),
            choices=[
                "Confront the perpetrator directly",
                "Gather more evidence first",
                "Try to understand their motives"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=4
        ),

        QuestMilestone(
            turn_number=7,
            title="The Impossible Choice",
            description=(
                "The perpetrator offers you a deal - their knowledge in exchange for "
                "allowing some of the plague to spread to a rival village."
            ),
            choices=[
                "Accept the deal for the greater good",
                "Reject it and find another way",
                "Pretend to accept and betray them"
            ],
            choice_impacts={0: ChoiceImpact.CRITICAL, 1: ChoiceImpact.MAJOR, 2: ChoiceImpact.CRITICAL},
            triggers_combat=False,
            narrative_weight=5
        ),

        QuestMilestone(
            turn_number=10,
            title="The Aftermath",
            description=(
                "Your decision has consequences that ripple through multiple villages. "
                "The Northern Realms react to your choice."
            ),
            choices=[
                "Accept responsibility for the outcome",
                "Shift blame to others",
                "Work to mitigate the damage"
            ],
            choice_impacts={0: ChoiceImpact.MAJOR, 1: ChoiceImpact.CRITICAL, 2: ChoiceImpact.MODERATE},
            reveals_information=True,
            narrative_weight=5
        )
    ]

    return LongFormQuest(
        quest_id="plague_village_dilemma",
        title="The Plague's Shadow",
        description=(
            "A village is struck by a mysterious plague that threatens to spread across "
            "the Northern Realms. Your investigation reveals a complex web of motives and "
            "desperation that forces you to make impossible choices."
        ),
        scenario="northern_realms",
        total_turns=12,
        milestones=milestones,
        opening_narrative=(
            "The road to Ironhold Village takes you through farmland that should be bustling "
            "with activity. Instead, you find abandoned fields and silent farmhouses.\n\n"
            "At the village center, you find a scene of quiet desperation. Villagers move "
            "slowly, their faces drawn and pale. A healer approaches you with haunted eyes.\n\n"
            "'Stranger, please help us,' she begs. 'A plague has come upon us - fever, weakness, "
            "and death follow in its wake. We've lost half the village already. The healers "
            "from Stormwatch won't come - they say we're cursed.'\n\n"
            "As you investigate, you realize this plague isn't natural. Someone deliberately "
            "spread it, and their motives run deeper than simple cruelty.\n\n"
            "Stopping the plague means making choices that will affect hundreds of lives "
            "across multiple villages. There are no easy answers here."
        ),
        possible_endings=[
            "plague_contained",
            "moral_compromise",
            "village_sacrifice",
            "greater_evil"
        ],
        tags=["moral_dilemma", "plague", "investigation", "choices"],
        difficulty="hard",
        estimated_playtime_minutes=60
    )


# ============================================================================
# QUEST LIBRARY EXPANSION - SKYRIM STYLE
# ============================================================================

class SkyrimStyleQuestLibrary:
    """Library of Skyrim-inspired quests for The Northern Realms"""

    @staticmethod
    def get_all_skyrim_style_quests() -> List[LongFormQuest]:
        """Get all Skyrim-style quests"""
        return [
            create_fighters_guild_quest(),
            create_mages_academy_quest(),
            create_shadow_hand_quest(),
            create_artifact_hunt_quest(),
            create_companion_quest(),
            create_world_event_quest(),
            create_dungeon_exploration_quest(),
            create_moral_dilemma_quest()
        ]

    @staticmethod
    def get_quests_by_difficulty(difficulty: str) -> List[LongFormQuest]:
        """Get quests by difficulty level"""
        quests = SkyrimStyleQuestLibrary.get_all_skyrim_style_quests()
        difficulty_map = {
            "easy": ["grand_festival_unity"],
            "medium": ["iron_wolves_ascension", "frostmere_academy", "forgotten_ruins_exploration", "companion_redemption"],
            "hard": ["shadow_hand_infiltration", "plague_village_dilemma"],
            "epic": ["ancient_artifact_hunt"]
        }

        target_quests = difficulty_map.get(difficulty, [])
        return [quest for quest in quests if quest.quest_id in target_quests]

    @staticmethod
    def get_quests_by_length() -> Dict[str, List[LongFormQuest]]:
        """Get quests grouped by estimated playtime"""
        quests = SkyrimStyleQuestLibrary.get_all_skyrim_style_quests()

        short_quests = [q for q in quests if q.estimated_playtime_minutes <= 45]
        medium_quests = [q for q in quests if 45 < q.estimated_playtime_minutes <= 60]
        long_quests = [q for q in quests if q.estimated_playtime_minutes > 60]

        return {
            "short": short_quests,
            "medium": medium_quests,
            "long": long_quests
        }

    @staticmethod
    def get_random_quest_by_type(quest_type: str) -> Optional[LongFormQuest]:
        """Get random quest of specific type"""
        type_map = {
            "guild": ["iron_wolves_ascension", "frostmere_academy", "shadow_hand_infiltration"],
            "exploration": ["forgotten_ruins_exploration"],
            "moral": ["plague_village_dilemma", "ancient_artifact_hunt"],
            "event": ["grand_festival_unity"],
            "companion": ["companion_redemption"]
        }

        quest_ids = type_map.get(quest_type, [])
        quests = SkyrimStyleQuestLibrary.get_all_skyrim_style_quests()
        available_quests = [q for q in quests if q.quest_id in quest_ids]

        return random.choice(available_quests) if available_quests else None

    @staticmethod
    def get_quest_connections(main_quest_id: str) -> List[str]:
        """Get quests that connect to a main quest"""
        # Define quest connections based on story logic
        connections = {
            "northern_realms_dragon_prophecy": [
                "mage_guild_research",
                "political_conspiracy",
                "ancient_artifact_hunt",
                "dragon_diplomacy"
            ],
            "mage_guild_research": [
                "frostmere_academy",
                "ancient_ruins_discovery"
            ],
            "blacksmith_masterpiece": [
                "iron_wolves_ascension"
            ]
        }

        return connections.get(main_quest_id, [])

    @staticmethod
    def get_quest_progression_suggestions(current_quest: str, player_level: int) -> List[str]:
        """Suggest next quests based on current progress and level"""
        suggestions = []

        # Level-based suggestions
        if player_level >= 1 and player_level <= 3:
            suggestions.extend(["grand_festival_unity", "iron_wolves_ascension"])
        elif player_level >= 4 and player_level <= 6:
            suggestions.extend(["frostmere_academy", "forgotten_ruins_exploration", "companion_redemption"])
        elif player_level >= 7:
            suggestions.extend(["shadow_hand_infiltration", "plague_village_dilemma", "ancient_artifact_hunt"])

        # Remove current quest from suggestions
        if current_quest in suggestions:
            suggestions.remove(current_quest)

        return suggestions[:3]  # Return top 3 suggestions

