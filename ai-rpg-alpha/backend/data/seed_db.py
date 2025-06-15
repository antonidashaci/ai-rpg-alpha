#!/usr/bin/env python3
"""
AI-RPG-Alpha: Database Seeding Script

This script loads initial data into the SQLite database from JSON files.
It can be run as a CLI tool to populate the database with quests and other game data.

Usage:
    python -m data.seed_db
    python backend/data/seed_db.py
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from dao.game_state import GameStateDAO
from models.dataclasses import Quest, Reward, ConsequenceThread, RiskLevel, QuestStatus

class DatabaseSeeder:
    """
    Handles seeding the database with initial game data.
    
    Loads quest data from JSON files and populates the SQLite database
    with the necessary game content for the AI-RPG engine.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database seeder.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path or "game_state.db"
        self.dao = GameStateDAO(self.db_path)
        self.data_dir = Path(__file__).parent
        
    def seed_all(self, force: bool = False) -> bool:
        """
        Seed all data into the database.
        
        Args:
            force: Whether to overwrite existing data
            
        Returns:
            True if successful, False otherwise
        """
        print("🌱 Starting database seeding process...")
        
        try:
            # Check if database already has data
            if not force and self._has_existing_data():
                print("⚠️  Database already contains data. Use --force to overwrite.")
                return False
            
            # Seed quests
            if self.seed_quests():
                print("✅ Quest data seeded successfully")
            else:
                print("❌ Failed to seed quest data")
                return False
            
            # Add more seeding operations here as needed
            # self.seed_npcs()
            # self.seed_locations()
            # self.seed_items()
            
            print("🎉 Database seeding completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database seeding failed: {e}")
            return False
    
    def seed_quests(self) -> bool:
        """
        Seed quest data from JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        print("📜 Seeding quest data...")
        
        try:
            quests_file = self.data_dir / "quests_seed.json"
            
            if not quests_file.exists():
                print(f"❌ Quest data file not found: {quests_file}")
                return False
            
            # Load quest data from JSON
            with open(quests_file, 'r', encoding='utf-8') as f:
                quest_data = json.load(f)
            
            if not isinstance(quest_data, list):
                print("❌ Quest data must be a list of quest objects")
                return False
            
            # Convert JSON data to Quest objects and insert into database
            successful_inserts = 0
            
            for quest_json in quest_data:
                try:
                    quest = self._json_to_quest(quest_json)
                    
                    if self.dao.create_quest(quest):
                        successful_inserts += 1
                        print(f"  ✓ Added quest: {quest.title}")
                    else:
                        print(f"  ❌ Failed to add quest: {quest.title}")
                        
                except Exception as e:
                    print(f"  ❌ Error processing quest {quest_json.get('id', 'unknown')}: {e}")
            
            print(f"📊 Successfully seeded {successful_inserts}/{len(quest_data)} quests")
            return successful_inserts > 0
            
        except Exception as e:
            print(f"❌ Error seeding quests: {e}")
            return False
    
    def _json_to_quest(self, quest_json: Dict[str, Any]) -> Quest:
        """
        Convert JSON quest data to Quest object.
        
        Args:
            quest_json: Quest data as dictionary
            
        Returns:
            Quest object
        """
        # Create reward object
        reward_data = quest_json.get("reward", {})
        reward = Reward(
            gold=reward_data.get("gold", 0),
            items=reward_data.get("items", []),
            experience=reward_data.get("experience", 0)
        )
        
        # Create consequence thread if present
        consequence_thread = None
        if quest_json.get("consequence_thread"):
            ct_data = quest_json["consequence_thread"]
            consequence_thread = ConsequenceThread(
                trigger_turn=ct_data["trigger_turn"],
                event=ct_data["event"],
                description=ct_data.get("description", ""),
                executed=False
            )
        
        # Create quest object
        quest = Quest(
            id=quest_json["id"],
            title=quest_json["title"],
            location=quest_json["location"],
            tags=quest_json.get("tags", []),
            intro=quest_json.get("intro", ""),
            objectives=quest_json.get("objectives", []),
            success=quest_json.get("success", ""),
            failure=quest_json.get("failure", ""),
            reward=reward,
            risk=RiskLevel(quest_json.get("risk", "calm")),
            consequence_thread=consequence_thread,
            status=QuestStatus.AVAILABLE
        )
        
        return quest
    
    def _has_existing_data(self) -> bool:
        """
        Check if the database already contains data.
        
        Returns:
            True if data exists, False otherwise
        """
        try:
            quests = self.dao.get_all_quests()
            return len(quests) > 0
        except Exception:
            return False
    
    def clear_data(self, confirm: bool = False) -> bool:
        """
        Clear all data from the database.
        
        Args:
            confirm: Whether the user has confirmed the action
            
        Returns:
            True if successful, False otherwise
        """
        if not confirm:
            print("⚠️  This will delete all data from the database!")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Operation cancelled.")
                return False
        
        try:
            print("🗑️  Clearing database data...")
            
            # In a full implementation, you would clear all tables here
            # For now, we'll just recreate the database
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
            
            # Reinitialize the database
            self.dao = GameStateDAO(self.db_path)
            
            print("✅ Database cleared successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to clear database: {e}")
            return False
    
    def show_stats(self) -> None:
        """Show database statistics."""
        print("📊 Database Statistics:")
        print("-" * 30)
        
        try:
            quests = self.dao.get_all_quests()
            print(f"Quests: {len(quests)}")
            
            # Group quests by location
            locations = {}
            risk_levels = {}
            
            for quest in quests:
                locations[quest.location] = locations.get(quest.location, 0) + 1
                risk_levels[quest.risk.value] = risk_levels.get(quest.risk.value, 0) + 1
            
            print("\nQuests by Location:")
            for location, count in locations.items():
                print(f"  {location}: {count}")
            
            print("\nQuests by Risk Level:")
            for risk, count in risk_levels.items():
                print(f"  {risk}: {count}")
                
        except Exception as e:
            print(f"❌ Error retrieving statistics: {e}")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="AI-RPG-Alpha Database Seeding Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m data.seed_db                    # Seed database with default data
  python -m data.seed_db --force            # Force overwrite existing data
  python -m data.seed_db --clear            # Clear all data
  python -m data.seed_db --stats            # Show database statistics
  python -m data.seed_db --db custom.db     # Use custom database file
        """
    )
    
    parser.add_argument(
        '--db', 
        default='game_state.db',
        help='Database file path (default: game_state.db)'
    )
    
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Force overwrite existing data'
    )
    
    parser.add_argument(
        '--clear', 
        action='store_true',
        help='Clear all data from database'
    )
    
    parser.add_argument(
        '--stats', 
        action='store_true',
        help='Show database statistics'
    )
    
    parser.add_argument(
        '--quests-only', 
        action='store_true',
        help='Only seed quest data'
    )
    
    args = parser.parse_args()
    
    # Initialize seeder
    seeder = DatabaseSeeder(args.db)
    
    print(f"🎮 AI-RPG-Alpha Database Seeder")
    print(f"Database: {args.db}")
    print("-" * 40)
    
    # Handle different operations
    if args.clear:
        success = seeder.clear_data()
        sys.exit(0 if success else 1)
    
    elif args.stats:
        seeder.show_stats()
        sys.exit(0)
    
    elif args.quests_only:
        success = seeder.seed_quests()
        sys.exit(0 if success else 1)
    
    else:
        # Default: seed all data
        success = seeder.seed_all(force=args.force)
        
        if success:
            print("\n📊 Final Statistics:")
            seeder.show_stats()
        
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

