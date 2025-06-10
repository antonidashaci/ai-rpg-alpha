"""
AI-RPG-Alpha Quest System Summary

Complete overview of our 55+ interconnected quest system
"""

from backend.engine.quest_collection_extended import ExtendedQuestCollection
from typing import Dict, List, Any


def generate_quest_system_summary():
    """Generate comprehensive summary of the quest system"""
    
    quest_collection = ExtendedQuestCollection()
    
    print("🎯 AI-RPG-Alpha Quest System Overview")
    print("=" * 60)
    
    # Total count
    total_quests = len(quest_collection.quests)
    print(f"📊 Total Quests: {total_quests}")
    
    # Count by category
    print(f"\n📋 Quests by Category:")
    category_counts = {}
    for quest in quest_collection.quests.values():
        category = quest.category.value
        category_counts[category] = category_counts.get(category, 0) + 1
    
    for category, count in sorted(category_counts.items()):
        print(f"  • {category.replace('_', ' ').title()}: {count} quests")
    
    # Quest chains
    print(f"\n🔗 Quest Chains:")
    chains = quest_collection.get_quest_chains_summary()
    for chain_name, chain_quests in chains.items():
        print(f"  • {chain_name.replace('_', ' ').title()}: {len(chain_quests)} quests")
        for quest_info in chain_quests:
            print(f"    - {quest_info['title']}")
    
    # Interconnections
    interconnections = quest_collection.get_interconnection_map()
    interconnected_count = len(interconnections)
    total_connections = sum(len(unlocks) for unlocks in interconnections.values())
    
    print(f"\n🕸️ Quest Interconnections:")
    print(f"  • Quests that unlock others: {interconnected_count}")
    print(f"  • Total unlock connections: {total_connections}")
    
    print(f"\n🎮 Sample Quest Progression Paths:")
    
    # Main Story Path
    print(f"\n📖 Main Story Path:")
    print(f"  1. The Dreamer's Awakening → Crossroads of Destiny")
    print(f"  2. → Whispers in the Dark → Shadow Conspiracy")
    print(f"  3. → The First Sign → Corruption War")
    print(f"  4. → Forging Unlikely Alliances → Final Battle")
    
    # Evil Path
    print(f"\n😈 Evil Character Path:")
    print(f"  1. Crime Syndicate Takeover → Embrace the Darkness")
    print(f"  2. → Royal Treasury Heist → Corruption Spreads")
    print(f"  3. → Shadow Covenant Initiation → Dark Lord Rise")
    
    # Redemption Path
    print(f"\n🕊️ Redemption Arc Path:")
    print(f"  1. Seeking Forgiveness → Trials of Atonement")
    print(f"  2. → Acts of Penance → Redeemed Hero")
    print(f"  3. → Legendary Savior → Atonement Complete")
    
    # Romance Path
    print(f"\n💕 Romance Path:")
    print(f"  1. The Ranger's Secret → Heart of the Forest")
    print(f"  2. → Deepening Bonds → Love Triangle Crisis")
    print(f"  3. → Commitment Choice → Happily Ever After")
    
    print(f"\n🌟 Special Features:")
    print(f"  ✓ Alignment-locked quests (Good/Evil/Neutral exclusive)")
    print(f"  ✓ Karma requirements and consequences")
    print(f"  ✓ Faction reputation dependencies")
    print(f"  ✓ Companion relationship requirements")
    print(f"  ✓ Multi-path story branching")
    print(f"  ✓ Seasonal/time-limited events")
    print(f"  ✓ Epic multi-part chains")
    print(f"  ✓ Cross-system integration")
    
    return quest_collection


def show_quest_details(quest_id: str = None):
    """Show detailed information about specific quests"""
    
    quest_collection = ExtendedQuestCollection()
    
    if quest_id:
        quest = quest_collection.get_quest(quest_id)
        if quest:
            print(f"\n🎯 Quest Details: {quest.quest.title}")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"ID: {quest.quest.id}")
            print(f"Location: {quest.quest.location}")
            print(f"Category: {quest.category.value}")
            if quest.chain:
                print(f"Chain: {quest.chain.value}")
            print(f"Risk Level: {quest.quest.risk.value}")
            print(f"\nIntro: {quest.quest.intro}")
            print(f"\nObjectives:")
            for i, obj in enumerate(quest.quest.objectives, 1):
                print(f"  {i}. {obj}")
            print(f"\nRewards:")
            print(f"  • Gold: {quest.quest.reward.gold}")
            print(f"  • Items: {', '.join(quest.quest.reward.items)}")
            print(f"  • Experience: {quest.quest.reward.experience}")
            
            if quest.requirements:
                req = quest.requirements
                print(f"\nRequirements:")
                if req.min_level > 1:
                    print(f"  • Min Level: {req.min_level}")
                if req.required_alignment:
                    print(f"  • Required Alignment: {', '.join(req.required_alignment)}")
                if req.min_karma != -1000:
                    print(f"  • Min Karma: {req.min_karma}")
                if req.min_corruption > 0:
                    print(f"  • Min Corruption: {req.min_corruption}")
                if req.required_factions:
                    print(f"  • Required Factions: {req.required_factions}")
                if req.required_companions:
                    print(f"  • Required Companions: {', '.join(req.required_companions)}")
            
            if quest.karma_actions:
                print(f"\nKarma Actions:")
                for choice, karma_action in quest.karma_actions.items():
                    print(f"  • {choice}: {karma_action.value}")
            
            if quest.unlocks_quests:
                print(f"\nUnlocks Quests:")
                for unlock in quest.unlocks_quests:
                    print(f"  • {unlock}")
        else:
            print(f"Quest '{quest_id}' not found.")
    else:
        print(f"\n📜 All Available Quests:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        for quest_id, quest in sorted(quest_collection.quests.items()):
            category_icon = {
                "main_story": "📖",
                "faction_political": "⚔️",
                "companion_personal": "👥",
                "alignment_moral": "⚖️",
                "criminal_underground": "🗡️",
                "heroic_legendary": "🏆",
                "mystery_supernatural": "🔮",
                "world_event": "🌍",
                "merchant_trade": "💰",
                "exploration": "🗺️"
            }.get(quest.category.value, "❓")
            
            chain_info = f" [{quest.chain.value}]" if quest.chain else ""
            print(f"  {category_icon} {quest.quest.title} ({quest_id}){chain_info}")


def show_quest_availability_example():
    """Show example of quest availability for different character types"""
    
    quest_collection = ExtendedQuestCollection()
    
    print(f"\n🎭 Quest Availability Examples:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Good character
    print(f"\n😇 Lawful Good Character (Level 10, Karma +150, Corruption 5):")
    good_available = quest_collection.get_available_quests(
        player_level=10,
        alignment="lawful_good", 
        karma=150,
        corruption=5,
        faction_standings={"royal_crown": 50, "order_of_dawn": 40},
        completed_quests=["story_awakening", "story_first_choice"],
        story_flags=["hero_reputation"],
        companions=["thane_warrior", "lyralei_ranger"]
    )
    print(f"  Available Quests: {len(good_available)}")
    for quest in good_available[:5]:  # Show first 5
        print(f"    • {quest.quest.title}")
    
    # Evil character
    print(f"\n😈 Chaotic Evil Character (Level 10, Karma -150, Corruption 70):")
    evil_available = quest_collection.get_available_quests(
        player_level=10,
        alignment="chaotic_evil",
        karma=-150, 
        corruption=70,
        faction_standings={"shadow_covenant": 50, "criminal_underworld": 60},
        completed_quests=["story_awakening", "story_first_choice"],
        story_flags=["notorious_killer"],
        companions=["kael_rogue"]
    )
    print(f"  Available Quests: {len(evil_available)}")
    for quest in evil_available[:5]:  # Show first 5
        print(f"    • {quest.quest.title}")
    
    # Neutral character
    print(f"\n😐 True Neutral Character (Level 10, Karma 0, Corruption 25):")
    neutral_available = quest_collection.get_available_quests(
        player_level=10,
        alignment="true_neutral",
        karma=0,
        corruption=25,
        faction_standings={"merchant_guilds": 30},
        completed_quests=["story_awakening", "story_first_choice"],
        story_flags=[],
        companions=["zara_mage"]
    )
    print(f"  Available Quests: {len(neutral_available)}")
    for quest in neutral_available[:5]:  # Show first 5
        print(f"    • {quest.quest.title}")


if __name__ == "__main__":
    """Run quest system demonstration"""
    
    print("🎮 AI-RPG-Alpha Quest System Demonstration")
    print("=" * 60)
    
    # Generate overview
    generate_quest_system_summary()
    
    # Show availability examples
    show_quest_availability_example()
    
    # Show some quest details
    print(f"\n📋 Sample Quest Details:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    sample_quests = [
        "story_first_choice",
        "shadow_initiation", 
        "orphanage_salvation",
        "heist_royal_treasury",
        "lyralei_romance"
    ]
    
    for quest_id in sample_quests:
        show_quest_details(quest_id)
        print()
    
    print(f"\n🏆 Quest System Summary:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ 55+ Total Quests Created")
    print(f"✅ 10 Quest Categories")
    print(f"✅ 7 Major Quest Chains")
    print(f"✅ Full Alignment Integration")
    print(f"✅ Karma System Integration")
    print(f"✅ Faction Requirements")
    print(f"✅ Companion Dependencies")
    print(f"✅ Story Flag Progression")
    print(f"✅ Cross-Quest Unlocking")
    print(f"✅ Multiple Playstyle Support")
    print(f"")
    print(f"🎯 Players can now experience:")
    print(f"  • Epic main story campaigns")
    print(f"  • Deep companion relationships")
    print(f"  • Faction political intrigue")
    print(f"  • Evil villain playthroughs") 
    print(f"  • Heroic legendary adventures")
    print(f"  • Redemption story arcs")
    print(f"  • Romance storylines")
    print(f"  • Merchant trading careers")
    print(f"  • Exploration expeditions")
    print(f"  • Supernatural mysteries")
    print(f"  • Seasonal events")
    print(f"  • And much more!")