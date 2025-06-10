"""
Alignment & Karma System Examples and Integration

This file demonstrates how players can be evil, indifferent, or good,
and how the world reacts to their moral choices.
"""

from backend.engine.alignment_karma import (
    AlignmentKarmaSystem, KarmaAction, MoralAlignment, ReputationLevel
)


def example_evil_playthrough():
    """Example of how an evil character progression works"""
    
    karma_system = AlignmentKarmaSystem()
    player_id = "evil_player_123"
    
    print("=== EVIL CHARACTER PLAYTHROUGH ===")
    
    # Starting as neutral, player makes increasingly evil choices
    print("\n1. Starting as True Neutral...")
    morality = karma_system.get_morality_summary(player_id)
    print(f"Alignment: {morality['alignment']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    
    # First evil act - stealing from the poor
    print("\n2. Stealing gold from beggars...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.STEAL_FROM_POOR,
        "Stole 50 gold from homeless beggars",
        location="slums",
        witnesses=["beggar_1", "beggar_2"],
        context={"present_companions": ["thane_warrior"]}
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"Alignment: {morality['alignment']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    print(f"Common Folk Rep: {morality['reputation_levels']['common_folk']}")
    
    # Murder an innocent
    print("\n3. Murdering an innocent witness...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.MURDER_INNOCENT,
        "Killed a witness to silence them",
        location="dark_alley",
        witnesses=["street_urchin"],
        context={"present_companions": ["kael_rogue"]}
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"Alignment: {morality['alignment']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    print(f"Infamy: {morality['infamy_level']}")
    print(f"Stats: {morality['stats']}")
    
    # Torture for information
    print("\n4. Torturing a prisoner...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.TORTURE,
        "Tortured a captured spy for information",
        location="abandoned_warehouse",
        context={"involved_factions": ["shadow_covenant"]}
    )
    
    # Betray ally
    print("\n5. Betraying a trusted ally...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.BETRAY_ALLY,
        "Sold out ally to enemies for profit",
        location="tavern",
        witnesses=["bartender", "patron_1", "patron_2"]
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"\nFINAL EVIL CHARACTER STATE:")
    print(f"Alignment: {morality['alignment']}")
    print(f"Moral Title: {morality['moral_title']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    print(f"Evil Options Available: {morality['available_evil_options']}")
    print(f"Dark Options Available: {morality['available_dark_options']}")
    print(f"Story Flags: {morality['story_flags']}")
    
    # Show available evil choices
    base_choices = [
        {"id": "ask_nicely", "text": "Ask politely for information"},
        {"id": "offer_payment", "text": "Offer to pay for the information"}
    ]
    
    evil_choices = karma_system.get_available_choices_for_alignment(player_id, base_choices)
    print(f"\nAvailable choices for evil character:")
    for choice in evil_choices:
        print(f"- {choice['text']}")
    
    # Show NPC reactions
    print(f"\nNPC Reaction Modifiers:")
    print(f"Guards: {karma_system.get_npc_reaction_modifier(player_id, 'guard'):.2f}")
    print(f"Commoners: {karma_system.get_npc_reaction_modifier(player_id, 'commoner'):.2f}")
    print(f"Criminals: {karma_system.get_npc_reaction_modifier(player_id, 'criminal'):.2f}")
    print(f"Priests: {karma_system.get_npc_reaction_modifier(player_id, 'priest'):.2f}")


def example_indifferent_playthrough():
    """Example of how an indifferent/neutral character works"""
    
    karma_system = AlignmentKarmaSystem()
    player_id = "neutral_player_456"
    
    print("\n\n=== INDIFFERENT CHARACTER PLAYTHROUGH ===")
    
    # Player consistently makes selfish, pragmatic choices
    print("\n1. Starting as True Neutral...")
    
    # Ignoring suffering
    print("\n2. Ignoring people in need...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.IGNORE_SUFFERING,
        "Walked past crying child without helping",
        location="street"
    )
    
    # Selfish choice
    karma_system.record_karma_action(
        player_id,
        KarmaAction.SELFISH_CHOICE,
        "Kept all the treasure for yourself",
        location="dungeon"
    )
    
    # Avoiding involvement
    karma_system.record_karma_action(
        player_id,
        KarmaAction.AVOID_INVOLVEMENT,
        "Refused to take sides in local conflict",
        location="village"
    )
    
    # Pragmatic decision
    karma_system.record_karma_action(
        player_id,
        KarmaAction.PRAGMATIC_DECISION,
        "Made deal with both sides for maximum profit",
        location="merchant_district"
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"\nFINAL INDIFFERENT CHARACTER STATE:")
    print(f"Alignment: {morality['alignment']}")
    print(f"Moral Title: {morality['moral_title']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Recent Karma: {morality['recent_karma']}")
    
    # Show reputation effects
    print(f"\nReputation with different groups:")
    for group, level in morality['reputation_levels'].items():
        print(f"- {group.replace('_', ' ').title()}: {level}")


def example_good_character_falls():
    """Example of good character falling to evil"""
    
    karma_system = AlignmentKarmaSystem()
    player_id = "fallen_hero_789"
    
    print("\n\n=== FALLEN HERO PLAYTHROUGH ===")
    
    # Start with good actions
    print("\n1. Starting as a hero...")
    karma_system.record_karma_action(
        player_id,
        KarmaAction.SAVE_INNOCENT,
        "Saved villagers from bandits",
        location="village"
    )
    
    karma_system.record_karma_action(
        player_id,
        KarmaAction.HELP_POOR,
        "Gave food to hungry families",
        location="slums"
    )
    
    karma_system.record_karma_action(
        player_id,
        KarmaAction.PROTECT_WEAK,
        "Defended orphanage from raiders",
        location="orphanage"
    )
    
    print("After good deeds:")
    morality = karma_system.get_morality_summary(player_id)
    print(f"Alignment: {morality['alignment']}")
    print(f"Karma: {morality['total_karma']}")
    
    # Tragic event leads to corruption
    print("\n2. Tragedy strikes - loved one dies...")
    print("Hero begins making darker choices...")
    
    # Revenge killing
    karma_system.record_karma_action(
        player_id,
        KarmaAction.MURDER_INNOCENT,
        "Killed someone you suspected of betrayal",
        location="tavern",
        witnesses=["tavern_keeper"]
    )
    
    # Torture for revenge
    karma_system.record_karma_action(
        player_id,
        KarmaAction.TORTURE,
        "Tortured suspects for information about your loved one's death",
        location="basement"
    )
    
    # More evil acts
    karma_system.record_karma_action(
        player_id,
        KarmaAction.BETRAY_ALLY,
        "Betrayed former ally who tried to stop your revenge",
        location="bridge"
    )
    
    print("\nAfter fall to darkness:")
    morality = karma_system.get_morality_summary(player_id)
    print(f"Alignment: {morality['alignment']}")
    print(f"Moral Title: {morality['moral_title']}")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    print(f"Redemption Points: {morality['redemption_points']}")
    
    # Show alignment history
    print(f"\nAlignment Changes:")
    for i, action in enumerate(morality['recent_actions']):
        print(f"{i+1}. {action['description']} (Karma: {action['karma']})")


def example_quest_restrictions():
    """Example of how alignment restricts quest access"""
    
    karma_system = AlignmentKarmaSystem()
    evil_player = "evil_player_123"
    good_player = "good_player_456"
    
    # Create evil player
    karma_system.record_karma_action(
        evil_player, KarmaAction.MURDER_INNOCENT, "Killed for fun", "street"
    )
    karma_system.record_karma_action(
        evil_player, KarmaAction.TORTURE, "Tortured prisoner", "dungeon"
    )
    
    # Create good player  
    karma_system.record_karma_action(
        good_player, KarmaAction.SAVE_INNOCENT, "Rescued villagers", "village"
    )
    karma_system.record_karma_action(
        good_player, KarmaAction.HELP_POOR, "Fed the hungry", "slums"
    )
    
    print("\n\n=== QUEST ACCESS EXAMPLES ===")
    
    # Define different quest types
    quests = {
        "holy_pilgrimage": {
            "required_alignment": ["good"],
            "min_karma": 20,
            "max_corruption": 25
        },
        "dark_ritual": {
            "required_alignment": ["evil"],
            "min_corruption": 50,
            "max_karma": -30
        },
        "assassin_guild": {
            "required_alignment": ["chaotic_evil", "neutral_evil"],
            "reputation_requirements": {"criminal_underworld": 30}
        },
        "temple_service": {
            "required_alignment": ["lawful_good", "neutral_good"],
            "reputation_requirements": {"religious_orders": 40}
        },
        "neutral_merchant": {
            # No alignment restrictions - anyone can do trade
        }
    }
    
    for quest_name, requirements in quests.items():
        print(f"\n{quest_name.replace('_', ' ').title()} Quest Access:")
        
        evil_can_start = karma_system.can_start_quest(evil_player, quest_name, requirements)
        good_can_start = karma_system.can_start_quest(good_player, quest_name, requirements)
        
        print(f"  Evil Player: {'✓ Available' if evil_can_start else '✗ Locked'}")
        print(f"  Good Player: {'✓ Available' if good_can_start else '✗ Locked'}")


def example_npc_reactions():
    """Example of how NPCs react differently to different alignments"""
    
    karma_system = AlignmentKarmaSystem()
    
    # Create characters with different reputations
    players = {
        "hero": "good_player_123",
        "villain": "evil_player_456", 
        "neutral": "neutral_player_789"
    }
    
    # Setup hero
    karma_system.record_karma_action(
        players["hero"], KarmaAction.SAVE_INNOCENT, "Saved many lives", "city"
    )
    karma_system.record_karma_action(
        players["hero"], KarmaAction.HELP_POOR, "Helped the needy", "slums"
    )
    
    # Setup villain with high infamy
    karma_system.record_karma_action(
        players["villain"], KarmaAction.MURDER_INNOCENT, "Public execution", "square",
        witnesses=["crowd_1", "crowd_2", "guard_1"]
    )
    karma_system.record_karma_action(
        players["villain"], KarmaAction.MASSACRE, "Destroyed village", "village",
        witnesses=["survivor_1", "survivor_2"]
    )
    
    # Setup neutral character
    karma_system.record_karma_action(
        players["neutral"], KarmaAction.PRAGMATIC_DECISION, "Made logical choice", "tavern"
    )
    
    print("\n\n=== NPC REACTION EXAMPLES ===")
    
    npc_types = ["guard", "commoner", "criminal", "priest", "merchant"]
    
    print(f"\n{'NPC Type':<12} {'Hero':<8} {'Villain':<8} {'Neutral':<8}")
    print("-" * 40)
    
    for npc_type in npc_types:
        hero_mod = karma_system.get_npc_reaction_modifier(players["hero"], npc_type)
        villain_mod = karma_system.get_npc_reaction_modifier(players["villain"], npc_type)
        neutral_mod = karma_system.get_npc_reaction_modifier(players["neutral"], npc_type)
        
        print(f"{npc_type.title():<12} {hero_mod:>+.2f}    {villain_mod:>+.2f}    {neutral_mod:>+.2f}")


def example_redemption_arc():
    """Example of evil character seeking redemption"""
    
    karma_system = AlignmentKarmaSystem()
    player_id = "redemption_seeker"
    
    print("\n\n=== REDEMPTION ARC EXAMPLE ===")
    
    # Start with evil acts
    print("1. Character commits evil acts...")
    karma_system.record_karma_action(
        player_id, KarmaAction.MURDER_INNOCENT, "Killed innocent", "alley"
    )
    karma_system.record_karma_action(
        player_id, KarmaAction.BETRAY_ALLY, "Betrayed friend", "tavern"
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"Evil State - Karma: {morality['total_karma']}, Corruption: {morality['corruption_level']}")
    print(f"Alignment: {morality['alignment']}")
    
    # Begin redemption
    print("\n2. Character seeks redemption...")
    karma_system.record_karma_action(
        player_id, KarmaAction.SAVE_INNOCENT, "Saved child from fire", "burning_house"
    )
    karma_system.record_karma_action(
        player_id, KarmaAction.SELF_SACRIFICE, "Sacrificed wealth to save others", "village"
    )
    karma_system.record_karma_action(
        player_id, KarmaAction.PROTECT_WEAK, "Protected refugees", "border"
    )
    karma_system.record_karma_action(
        player_id, KarmaAction.HEAL_WOUNDED, "Tended to the injured", "battlefield"
    )
    
    morality = karma_system.get_morality_summary(player_id)
    print(f"\nRedemption Progress:")
    print(f"Karma: {morality['total_karma']}")
    print(f"Corruption: {morality['corruption_level']}")
    print(f"Redemption Points: {morality['redemption_points']}")
    print(f"Alignment: {morality['alignment']}")
    print(f"Moral Title: {morality['moral_title']}")
    
    print(f"\nCan still access evil options: {morality['available_evil_options']}")
    print(f"Can access dark options: {morality['available_dark_options']}")


if __name__ == "__main__":
    """Run all examples to demonstrate the alignment system"""
    
    print("ALIGNMENT & KARMA SYSTEM DEMONSTRATION")
    print("=" * 50)
    
    # Run all examples
    example_evil_playthrough()
    example_indifferent_playthrough() 
    example_good_character_falls()
    example_quest_restrictions()
    example_npc_reactions()
    example_redemption_arc()
    
    print("\n\n=== SUMMARY ===")
    print("The Alignment & Karma System provides:")
    print("✓ Full spectrum of moral choices (Good → Neutral → Evil)")
    print("✓ Dynamic alignment shifts based on player actions")
    print("✓ Corruption system that unlocks darker options")
    print("✓ Reputation tracking with different groups")
    print("✓ Quest restrictions based on moral standing")
    print("✓ NPC reactions that change based on player reputation")
    print("✓ Redemption arcs for players who want to change")
    print("✓ Consequences for every moral choice")
    print("✓ Support for truly evil, indifferent, or heroic characters")