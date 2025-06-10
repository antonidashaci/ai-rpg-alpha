"""
AI-RPG-Alpha Text-Based Game Runner

Simple CLI interface to experience the quest system and alignment/karma mechanics
"""

import os
import sys
import random
from typing import Dict, List, Any, Optional

# Add the parent directory to sys.path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine.quest_collection_extended import ExtendedQuestCollection, QuestCategory
from backend.engine.alignment_karma import AlignmentKarmaSystem, MoralAlignment, KarmaAction
from backend.models.dataclasses import Player, Quest


class TextGameState:
    """Simple game state for text-based play"""
    
    def __init__(self):
        self.player = Player(
            id="text_player",
            name="",
            level=1,
            location="starting_village",
            active_quests=[],
            completed_quests=[],
            gold=100,
            experience=0
        )
        
        self.alignment_system = AlignmentKarmaSystem()
        self.quest_collection = ExtendedQuestCollection()
        self.current_quest: Optional[str] = None
        self.story_flags: List[str] = []
        self.faction_standings: Dict[str, int] = {
            "royal_crown": 0,
            "peoples_liberation": 0,
            "shadow_covenant": 0,
            "order_of_dawn": 0,
            "criminal_underworld": 0,
            "merchant_guilds": 0,
            "house_ravencrest": 0
        }
        self.companions: List[str] = []
        
    def get_player_alignment(self) -> str:
        """Get player's current alignment as string"""
        morality = self.alignment_system.get_player_morality(self.player.id)
        return morality.current_alignment.value if morality else "true_neutral"
    
    def get_player_karma(self) -> int:
        """Get player's current karma"""
        morality = self.alignment_system.get_player_morality(self.player.id)
        return morality.karma_score if morality else 0
    
    def get_player_corruption(self) -> int:
        """Get player's current corruption level"""
        morality = self.alignment_system.get_player_morality(self.player.id)
        return morality.corruption_level if morality else 0


class TextGameRunner:
    """Main text-based game runner"""
    
    def __init__(self):
        self.game_state = TextGameState()
        self.running = True
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f" {title} ".center(60, "="))
        print("=" * 60)
    
    def print_separator(self):
        """Print a separator line"""
        print("-" * 60)
    
    def wait_for_input(self, prompt: str = "Press Enter to continue..."):
        """Wait for user input"""
        input(f"\n{prompt}")
    
    def show_character_status(self):
        """Display current character status"""
        player = self.game_state.player
        alignment = self.game_state.get_player_alignment()
        karma = self.game_state.get_player_karma()
        corruption = self.game_state.get_player_corruption()
        
        morality = self.game_state.alignment_system.get_player_morality(player.id)
        moral_title = morality.get_moral_title() if morality else "Unknown"
        
        print(f"\n👤 CHARACTER STATUS:")
        print(f"Name: {player.name}")
        print(f"Level: {player.level}")
        print(f"Location: {player.location.replace('_', ' ').title()}")
        print(f"Gold: {player.gold}")
        print(f"Experience: {player.experience}")
        print(f"\n⚖️ MORALITY:")
        print(f"Alignment: {alignment.replace('_', ' ').title()}")
        print(f"Moral Title: {moral_title}")
        print(f"Karma: {karma}")
        print(f"Corruption: {corruption}")
        
        if self.game_state.faction_standings:
            print(f"\n🏛️ FACTION STANDINGS:")
            for faction, standing in self.game_state.faction_standings.items():
                if standing != 0:
                    faction_name = faction.replace('_', ' ').title()
                    status = "Friendly" if standing > 0 else "Hostile"
                    print(f"  {faction_name}: {standing} ({status})")
        
        if self.game_state.companions:
            print(f"\n👥 COMPANIONS:")
            for companion in self.game_state.companions:
                print(f"  • {companion.replace('_', ' ').title()}")
    
    def character_creation(self):
        """Handle character creation"""
        self.clear_screen()
        self.print_header("CHARACTER CREATION")
        
        print("Welcome to AI-RPG-Alpha!")
        print("Let's create your character...\n")
        
        # Get character name
        while True:
            name = input("Enter your character's name: ").strip()
            if name:
                self.game_state.player.name = name
                break
            print("Please enter a valid name.")
        
        # Choose starting moral inclination
        print(f"\nChoose your character's initial moral inclination:")
        print("1. Good-hearted (starts with +karma)")
        print("2. Neutral/Pragmatic (balanced start)")
        print("3. Self-interested (starts with some corruption)")
        print("4. Evil-inclined (starts with -karma and corruption)")
        
        while True:
            try:
                choice = int(input("Enter choice (1-4): "))
                if choice == 1:
                    self.game_state.alignment_system.track_karma_event(
                        self.game_state.player.id, KarmaAction.HELP_POOR
                    )
                    print("You begin with a good heart and noble intentions.")
                    break
                elif choice == 2:
                    print("You begin with a pragmatic, balanced worldview.")
                    break
                elif choice == 3:
                    self.game_state.alignment_system.track_karma_event(
                        self.game_state.player.id, KarmaAction.SELFISH_CHOICE
                    )
                    print("You begin focused on your own interests above others.")
                    break
                elif choice == 4:
                    self.game_state.alignment_system.track_karma_event(
                        self.game_state.player.id, KarmaAction.CAUSE_CHAOS
                    )
                    print("You begin with dark inclinations and questionable morals.")
                    break
                else:
                    print("Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nWelcome, {name}! Your adventure begins...")
        self.wait_for_input()
    
    def show_main_menu(self):
        """Show the main game menu"""
        self.clear_screen()
        self.print_header(f"AI-RPG-ALPHA - {self.game_state.player.name}")
        
        self.show_character_status()
        
        print(f"\n🎮 MAIN MENU:")
        print("1. View Available Quests")
        print("2. Continue Current Quest" + (f" ({self.game_state.current_quest})" if self.game_state.current_quest else " (None)"))
        print("3. Visit Locations")
        print("4. Character Details")
        print("5. Save & Exit")
        
        return input("\nChoose an option (1-5): ").strip()
    
    def show_available_quests(self):
        """Show quests available to the player"""
        self.clear_screen()
        self.print_header("AVAILABLE QUESTS")
        
        available_quests = self.game_state.quest_collection.get_available_quests(
            player_level=self.game_state.player.level,
            alignment=self.game_state.get_player_alignment(),
            karma=self.game_state.get_player_karma(),
            corruption=self.game_state.get_player_corruption(),
            faction_standings=self.game_state.faction_standings,
            completed_quests=self.game_state.player.completed_quests,
            story_flags=self.game_state.story_flags,
            companions=self.game_state.companions
        )
        
        if not available_quests:
            print("No quests are currently available to you.")
            print("Try improving your standing with factions or progressing the main story.")
            self.wait_for_input()
            return
        
        print(f"You have {len(available_quests)} quests available:\n")
        
        for i, enhanced_quest in enumerate(available_quests, 1):
            quest = enhanced_quest.quest
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
            }.get(enhanced_quest.category.value, "❓")
            
            print(f"{i}. {category_icon} {quest.title}")
            print(f"   Location: {quest.location.replace('_', ' ').title()}")
            print(f"   Risk: {quest.risk.value.title()}")
            print(f"   Reward: {quest.reward.gold} gold, {quest.reward.experience} exp")
            print()
        
        print("0. Back to Main Menu")
        
        try:
            choice = int(input("Select a quest (0 to go back): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_quests):
                selected_quest = available_quests[choice - 1]
                self.start_quest(selected_quest)
            else:
                print("Invalid choice.")
                self.wait_for_input()
        except ValueError:
            print("Please enter a valid number.")
            self.wait_for_input()
    
    def start_quest(self, enhanced_quest):
        """Start a specific quest"""
        quest = enhanced_quest.quest
        
        self.clear_screen()
        self.print_header(quest.title)
        
        print(f"📍 Location: {quest.location.replace('_', ' ').title()}")
        print(f"🎯 Category: {enhanced_quest.category.value.replace('_', ' ').title()}")
        print(f"⚠️ Risk Level: {quest.risk.value.title()}")
        
        print(f"\n📜 QUEST DESCRIPTION:")
        print(quest.intro)
        
        print(f"\n🎯 OBJECTIVES:")
        for i, objective in enumerate(quest.objectives, 1):
            print(f"  {i}. {objective}")
        
        print(f"\n💰 REWARDS:")
        print(f"  • Gold: {quest.reward.gold}")
        print(f"  • Items: {', '.join(quest.reward.items) if quest.reward.items else 'None'}")
        print(f"  • Experience: {quest.reward.experience}")
        
        print(f"\n1. Accept Quest")
        print(f"2. Decline Quest")
        
        choice = input("What do you choose? (1-2): ").strip()
        
        if choice == "1":
            self.game_state.current_quest = quest.id
            self.game_state.player.active_quests.append(quest.id)
            print(f"\nYou have accepted '{quest.title}'!")
            self.wait_for_input()
            self.play_quest(enhanced_quest)
        else:
            print("You decline the quest.")
            self.wait_for_input()
    
    def play_quest(self, enhanced_quest):
        """Play through a quest with choices"""
        quest = enhanced_quest.quest
        
        self.clear_screen()
        self.print_header(f"QUEST: {quest.title}")
        
        print("You begin your quest...\n")
        
        # Show quest-specific choices based on karma actions
        choices = []
        karma_actions = enhanced_quest.karma_actions
        
        if karma_actions:
            print("As you progress, you face important decisions:\n")
            
            for i, (choice_desc, karma_action) in enumerate(karma_actions.items(), 1):
                choice_display = choice_desc.replace('_', ' ').title()
                choices.append((choice_desc, karma_action))
                print(f"{i}. {choice_display}")
            
            print(f"{len(choices) + 1}. Take a neutral approach")
            
            try:
                choice_num = int(input(f"\nWhat do you choose? (1-{len(choices) + 1}): "))
                
                if 1 <= choice_num <= len(choices):
                    chosen_action = choices[choice_num - 1]
                    choice_desc, karma_action = chosen_action
                    
                    # Track the karma action
                    self.game_state.alignment_system.track_karma_event(
                        self.game_state.player.id, karma_action
                    )
                    
                    print(f"\nYou chose: {choice_desc.replace('_', ' ')}")
                    print(f"This action reflects: {karma_action.value}")
                    
                    # Apply faction impacts
                    if hasattr(enhanced_quest, 'faction_impacts'):
                        for faction, impact in enhanced_quest.faction_impacts.items():
                            self.game_state.faction_standings[faction] += impact
                            if impact > 0:
                                print(f"Your standing with {faction.replace('_', ' ').title()} increased!")
                            elif impact < 0:
                                print(f"Your standing with {faction.replace('_', ' ').title()} decreased!")
                
                else:
                    print("\nYou take a careful, neutral approach.")
                
            except ValueError:
                print("\nYou hesitate and take a neutral approach.")
        
        # Complete the quest
        success = random.choice([True, True, True, False])  # 75% success rate
        
        print(f"\n" + "="*50)
        
        if success:
            print("🎉 QUEST COMPLETED SUCCESSFULLY!")
            print(quest.success)
            
            # Apply rewards
            self.game_state.player.gold += quest.reward.gold
            self.game_state.player.experience += quest.reward.experience
            
            print(f"\n💰 Rewards Received:")
            print(f"  • Gold: +{quest.reward.gold}")
            print(f"  • Items: {', '.join(quest.reward.items)}")
            print(f"  • Experience: +{quest.reward.experience}")
            
        else:
            print("😞 QUEST FAILED")
            print(quest.failure)
            
            # Partial rewards on failure
            partial_gold = quest.reward.gold // 3
            partial_exp = quest.reward.experience // 2
            
            self.game_state.player.gold += partial_gold
            self.game_state.player.experience += partial_exp
            
            print(f"\n💰 Partial Rewards:")
            print(f"  • Gold: +{partial_gold}")
            print(f"  • Experience: +{partial_exp}")
        
        # Complete the quest
        self.game_state.player.completed_quests.append(quest.id)
        if quest.id in self.game_state.player.active_quests:
            self.game_state.player.active_quests.remove(quest.id)
        self.game_state.current_quest = None
        
        # Level up check
        if self.game_state.player.experience >= self.game_state.player.level * 100:
            self.game_state.player.level += 1
            self.game_state.player.experience = 0
            print(f"\n🎊 LEVEL UP! You are now level {self.game_state.player.level}!")
        
        # Unlock new quests
        if hasattr(enhanced_quest, 'unlocks_quests') and enhanced_quest.unlocks_quests:
            print(f"\n🔓 New quests have become available!")
            for unlocked_id in enhanced_quest.unlocks_quests:
                unlocked_quest = self.game_state.quest_collection.get_quest(unlocked_id)
                if unlocked_quest:
                    print(f"  • {unlocked_quest.quest.title}")
        
        self.wait_for_input()
    
    def visit_locations(self):
        """Show location options"""
        self.clear_screen()
        self.print_header("TRAVEL")
        
        locations = [
            ("starting_village", "Starting Village - A peaceful farming community"),
            ("noble_district", "Noble District - Where the wealthy and powerful reside"),
            ("lower_district", "Lower District - Home to the poor and desperate"),
            ("temple_of_dawn", "Temple of Dawn - Sacred ground of the light"),
            ("underworld_district", "Underworld District - Where criminals gather"),
            ("trade_roads", "Trade Roads - Dangerous paths between cities"),
            ("ancient_ruins", "Ancient Ruins - Mysterious remnants of the past")
        ]
        
        print("Where would you like to travel?")
        print()
        
        for i, (location_id, description) in enumerate(locations, 1):
            current = " (Current)" if location_id == self.game_state.player.location else ""
            print(f"{i}. {description}{current}")
        
        print("0. Back to Main Menu")
        
        try:
            choice = int(input(f"\nChoose destination (0-{len(locations)}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(locations):
                new_location = locations[choice - 1][0]
                self.game_state.player.location = new_location
                print(f"\nYou travel to {locations[choice - 1][1].split(' - ')[0]}.")
                self.wait_for_input()
            else:
                print("Invalid choice.")
                self.wait_for_input()
        except ValueError:
            print("Please enter a valid number.")
            self.wait_for_input()
    
    def show_character_details(self):
        """Show detailed character information"""
        self.clear_screen()
        self.print_header("CHARACTER DETAILS")
        
        self.show_character_status()
        
        # Show completed quests
        if self.game_state.player.completed_quests:
            print(f"\n📜 COMPLETED QUESTS ({len(self.game_state.player.completed_quests)}):")
            for quest_id in self.game_state.player.completed_quests:
                enhanced_quest = self.game_state.quest_collection.get_quest(quest_id)
                if enhanced_quest:
                    print(f"  ✓ {enhanced_quest.quest.title}")
        
        # Show moral history
        morality = self.game_state.alignment_system.get_player_morality(self.game_state.player.id)
        if morality and morality.recent_karma_events:
            print(f"\n⚖️ RECENT MORAL ACTIONS:")
            for event in morality.recent_karma_events[-5:]:  # Show last 5
                print(f"  • {event.action.value}")
        
        self.wait_for_input()
    
    def run(self):
        """Main game loop"""
        self.character_creation()
        
        while self.running:
            try:
                choice = self.show_main_menu()
                
                if choice == "1":
                    self.show_available_quests()
                elif choice == "2":
                    if self.game_state.current_quest:
                        enhanced_quest = self.game_state.quest_collection.get_quest(self.game_state.current_quest)
                        if enhanced_quest:
                            self.play_quest(enhanced_quest)
                    else:
                        print("You have no active quest.")
                        self.wait_for_input()
                elif choice == "3":
                    self.visit_locations()
                elif choice == "4":
                    self.show_character_details()
                elif choice == "5":
                    print("Thanks for playing AI-RPG-Alpha!")
                    self.running = False
                else:
                    print("Invalid choice. Please try again.")
                    self.wait_for_input()
                    
            except KeyboardInterrupt:
                print("\n\nExiting game...")
                self.running = False
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("The game will continue...")
                self.wait_for_input()


if __name__ == "__main__":
    print("🎮 Starting AI-RPG-Alpha Text Game...")
    game = TextGameRunner()
    game.run()