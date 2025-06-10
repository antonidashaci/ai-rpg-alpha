"""
Test script to verify imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test basic model imports
    from models.dataclasses import Player, Quest
    print("✓ Models imported successfully")
    
    # Test alignment karma system
    from engine.alignment_karma import AlignmentKarmaSystem, KarmaAction
    print("✓ Alignment/Karma system imported successfully")
    
    # Test quest collection
    from engine.quest_collection_extended import ExtendedQuestCollection
    print("✓ Quest collection imported successfully")
    
    # Test creating instances
    player = Player(
        id="test_player",
        name="Test Character",
        level=1,
        location="starting_village",
        active_quests=[],
        completed_quests=[],
        gold=100,
        experience=0
    )
    print("✓ Player created successfully")
    
    alignment_system = AlignmentKarmaSystem()
    print("✓ Alignment system created successfully")
    
    quest_collection = ExtendedQuestCollection()
    print("✓ Quest collection created successfully")
    
    print(f"✓ Quest collection has {len(quest_collection.quests)} quests")
    
    # Test getting available quests
    available = quest_collection.get_available_quests(
        player_level=1,
        alignment="true_neutral",
        karma=0,
        corruption=0,
        faction_standings={},
        completed_quests=[],
        story_flags=[],
        companions=[]
    )
    
    print(f"✓ Found {len(available)} available quests for level 1 character")
    
    if available:
        print("Sample quests:")
        for i, quest in enumerate(available[:3]):
            print(f"  {i+1}. {quest.quest.title}")
    
    print("\n🎉 All imports working correctly! Ready to run the game.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 