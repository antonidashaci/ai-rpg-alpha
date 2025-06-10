"""
AI-RPG-Alpha: Quest Progression System Demonstration

This demonstrates how our new Bethesda-style quest progression system
fixes the major flaw where level 1 characters could access high-level 
content. Shows proper level gating and natural story progression.
"""

from typing import Dict, List, Any
from backend.engine.quest_progression_system import QuestProgressionSystem, ProgessionTier

class QuestProgressionDemo:
    """
    Demonstrates the quest progression system and how it prevents
    inappropriate quest access while providing immersive storytelling.
    """
    
    def __init__(self):
        self.progression_system = QuestProgressionSystem()
        
    def demonstrate_level_progression(self):
        """Show how quests unlock appropriately by level"""
        
        print("=== QUEST PROGRESSION DEMONSTRATION ===")
        print("Showing how quests unlock naturally as player progresses\n")
        
        # Simulate player progression from level 1 to 20
        for level in [1, 3, 5, 7, 10, 13, 16, 20]:
            print(f"📊 LEVEL {level} ANALYSIS")
            print("=" * 50)
            
            # Get current location description
            location = self._get_location_for_level(level)
            location_desc = self.progression_system.get_current_location_description(location)
            print(f"🏘️  Current Location: {location}")
            print(f"📝 {location_desc[:200]}...\n")
            
            # Get available quests
            completed_quests = self._get_completed_quests_for_level(level)
            player_stats = self._get_player_stats_for_level(level)
            
            available = self.progression_system.get_available_quests_for_level(
                level, completed_quests, player_stats
            )
            
            # Get progression info
            recommendations = self.progression_system.get_progression_recommendations(
                level, completed_quests
            )
            
            print(f"🎯 Progression Tier: {recommendations['current_tier'].upper()}")
            print(f"💡 Advice: {recommendations['progression_advice']}")
            print(f"📋 Available Quests ({len(available)}):")
            
            for quest in available[:5]:  # Show top 5
                difficulty = self.progression_system.get_quest_difficulty_explanation(
                    quest.id, level
                )
                print(f"   • {quest.title} ({quest.tier.value}) - {difficulty}")
            
            print("\n" + "─" * 80 + "\n")
    
    def demonstrate_crime_lord_progression(self):
        """Show the specific crime lord quest progression to prove the fix"""
        
        print("=== CRIME LORD QUEST PROGRESSION FIX ===")
        print("Demonstrating that 'become crime lord' is now properly level-gated\n")
        
        print("🚫 BEFORE (The Problem):")
        print("Level 1 character could access 'Shadow Throne' (crime syndicate takeover)")
        print("This was completely inappropriate - a novice becoming a crime lord!\n")
        
        print("✅ AFTER (The Fix):")
        print("'Shadow Throne' quest now requires extensive progression:\n")
        
        crime_lord_quest = "crime_lord"
        
        # Check requirements at different levels
        for level in [1, 5, 10, 15, 16, 20]:
            can_start, message = self.progression_system.validate_quest_progression(
                crime_lord_quest, level, []
            )
            
            status = "✅ AVAILABLE" if can_start else "🚫 BLOCKED"
            print(f"Level {level:2d}: {status} - {message}")
        
        # Show proper progression path
        print(f"\n🗺️  PROPER PROGRESSION PATH TO CRIME LORD:")
        print("Level 1-3 (Novice): Start with basic village tasks")
        print("  ├─ Village Messenger (letter delivery)")
        print("  ├─ Gathering Herbs")
        print("  └─ Finding Whiskers (lost cat)")
        print()
        print("Level 4-6 (Apprentice): Local problems and minor crimes")
        print("  ├─ Bandits on the Trade Road")
        print("  ├─ The Corrupt Guard")
        print("  └─ Contraband Runner (first criminal activity)")
        print()
        print("Level 7-10 (Journeyman): Faction introduction")
        print("  ├─ A Whisper in the Dark (thieves guild contact)")
        print("  └─ Build reputation through smaller heists")
        print()
        print("Level 11-15 (Expert): Faction advancement")
        print("  ├─ Guild Lieutenant (leadership role)")
        print("  ├─ The Trade War (major faction conflict)")
        print("  └─ Prove worthiness for ultimate power")
        print()
        print("Level 16-20 (Master): Ultimate quest unlocked")
        print("  └─ Shadow Throne (become crime lord)")
        print("      Requires: 80+ thieves faction, 60+ corruption, -100 karma")
        
    def demonstrate_location_storytelling(self):
        """Show how location descriptions enhance immersion"""
        
        print("\n=== IMMERSIVE LOCATION STORYTELLING ===")
        print("Every turn now includes detailed location descriptions\n")
        
        locations = [
            ("Village of Millbrook", "day"),
            ("Thieves' Quarter", "night"),
            ("Temple District", "dawn"),
            ("Abandoned Mines", "day"),
            ("Darkwood Forest", "dusk")
        ]
        
        for location, time in locations:
            print(f"📍 {location.upper()} ({time})")
            print("─" * 60)
            desc = self.progression_system.get_current_location_description(location, time)
            print(desc)
            print("\n" + "═" * 80 + "\n")
    
    def demonstrate_quest_difficulty_validation(self):
        """Show how quest difficulty is properly explained"""
        
        print("=== QUEST DIFFICULTY VALIDATION ===")
        print("Players now get clear explanations of quest difficulty\n")
        
        test_quests = [
            ("letter_delivery", "Tutorial quest"),
            ("bandits_road", "First real challenge"),
            ("thieves_guild_contact", "Faction introduction"),
            ("crime_lord", "Ultimate challenge")
        ]
        
        player_level = 5
        print(f"Player Level: {player_level}")
        print("─" * 50)
        
        for quest_id, description in test_quests:
            difficulty = self.progression_system.get_quest_difficulty_explanation(
                quest_id, player_level
            )
            
            quest_data = self.progression_system.progression_tree.get(quest_id)
            if quest_data:
                level_range = f"(Levels {quest_data.min_level}-{quest_data.max_level})"
                print(f"📋 {quest_data.title} {level_range}")
                print(f"   {description}")
                print(f"   ⚖️  Difficulty: {difficulty}")
                print()
    
    def _get_location_for_level(self, level: int) -> str:
        """Get appropriate location for player level"""
        if level <= 3:
            return "Village of Millbrook"
        elif level <= 6:
            return "Crossroads Inn"
        elif level <= 10:
            return "Riverside Town"
        elif level <= 15:
            return "Thieves' Quarter"
        else:
            return "Temple District"
    
    def _get_completed_quests_for_level(self, level: int) -> List[str]:
        """Simulate completed quests for a given level"""
        completed = []
        
        # Level 1-3 quests
        if level >= 2:
            completed.extend(["letter_delivery", "herb_gathering"])
        if level >= 3:
            completed.extend(["lost_cat"])
        if level >= 4:
            completed.extend(["apple_thief", "first_rat"])
        
        # Level 4-6 quests
        if level >= 5:
            completed.extend(["bandits_road"])
        if level >= 6:
            completed.extend(["merchant_escort"])
        if level >= 7:
            completed.extend(["missing_miners", "corrupt_guard", "small_time_smuggling"])
        
        # Level 7-10 quests
        if level >= 8:
            completed.extend(["wolf_pack_leader"])
        if level >= 9:
            completed.extend(["thieves_guild_contact", "temple_acolyte"])
        if level >= 10:
            completed.extend(["ancient_tomb"])
        
        # Level 11-15 quests
        if level >= 12:
            completed.extend(["guild_lieutenant", "temple_priest"])
        if level >= 14:
            completed.extend(["regional_threat"])
        if level >= 15:
            completed.extend(["trade_war"])
        
        return completed
    
    def _get_player_stats_for_level(self, level: int) -> Dict[str, Any]:
        """Simulate player stats for a given level"""
        
        # Base stats that scale with level
        karma = 0
        corruption = 0
        faction_thieves = 0
        faction_temple = 0
        
        # Simulate moral choices based on level progression
        if level >= 5:  # Started making moral choices
            karma = -20  # Chose some darker paths
            corruption = 15
        
        if level >= 8:  # Joined thieves guild
            faction_thieves = 40
            karma = -50
            corruption = 30
        
        if level >= 12:  # Advanced in thieves guild
            faction_thieves = 70
            karma = -80
            corruption = 50
        
        if level >= 16:  # Ready for ultimate evil quests
            faction_thieves = 85
            karma = -120
            corruption = 65
        
        return {
            "level": level,
            "karma": karma,
            "corruption": corruption,
            "faction_thieves": faction_thieves,
            "faction_temple": faction_temple,
            "stealth_kills": max(0, level - 7),
            "successful_heists": max(0, level - 10),
            "temple_donations": 0,
            "guild_reputation": faction_thieves
        }

def run_demo():
    """Run the complete demonstration"""
    
    demo = QuestProgressionDemo()
    
    print("🎮 AI-RPG-ALPHA: QUEST PROGRESSION SYSTEM DEMO")
    print("=" * 80)
    print("Demonstrating how we fixed the major progression flaw")
    print("where level 1 characters could access end-game content.")
    print("=" * 80 + "\n")
    
    # Show level progression
    demo.demonstrate_level_progression()
    
    # Show specific crime lord fix
    demo.demonstrate_crime_lord_progression()
    
    # Show location storytelling
    demo.demonstrate_location_storytelling()
    
    # Show difficulty validation
    demo.demonstrate_quest_difficulty_validation()
    
    print("🎯 SUMMARY OF FIXES:")
    print("─" * 40)
    print("✅ Level-appropriate quest gating")
    print("✅ Natural story progression")
    print("✅ Immersive location descriptions every turn")
    print("✅ Proper difficulty explanations")
    print("✅ No more level 1 crime lords!")
    print("✅ Follows Skyrim/Fallout progression design")
    print("\n🚀 The quest system now provides proper RPG progression!")

if __name__ == "__main__":
    run_demo() 