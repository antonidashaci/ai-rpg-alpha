"""
AI-RPG-Alpha: Game State Data Access Object

This module handles all SQLite database operations for game state management.
It provides CRUD operations for players, quests, and game events.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import contextmanager
import os

from models.dataclasses import Player, Quest, GameEvent, PlayerStats, Reward, ConsequenceThread, RiskLevel, QuestStatus

class GameStateDAO:
    """
    Data Access Object for game state management using SQLite.
    
    Handles all database operations for players, quests, and game events.
    Provides methods for creating, reading, updating, and deleting game data.
    """
    
    def __init__(self, db_path: str = "game_state.db"):
        """
        Initialize the GameStateDAO with database path.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    stats TEXT NOT NULL,  -- JSON serialized PlayerStats
                    inventory TEXT NOT NULL,  -- JSON serialized list
                    active_quests TEXT NOT NULL,  -- JSON serialized list
                    completed_quests TEXT NOT NULL,  -- JSON serialized list
                    current_location TEXT NOT NULL,
                    turn_number INTEGER DEFAULT 0,
                    last_choice TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Quests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quests (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    tags TEXT NOT NULL,  -- JSON serialized list
                    intro TEXT NOT NULL,
                    objectives TEXT NOT NULL,  -- JSON serialized list
                    success TEXT NOT NULL,
                    failure TEXT NOT NULL,
                    reward TEXT NOT NULL,  -- JSON serialized Reward
                    risk TEXT NOT NULL,
                    consequence_thread TEXT,  -- JSON serialized ConsequenceThread
                    status TEXT NOT NULL DEFAULT 'available'
                )
            """)
            
            # Game events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_events (
                    id TEXT PRIMARY KEY,
                    player_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    data TEXT NOT NULL,  -- JSON serialized dict
                    turn_number INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (player_id) REFERENCES players (id)
                )
            """)
            
            conn.commit()
    
    # Player CRUD operations
    def create_player(self, player: Player) -> bool:
        """
        Create a new player in the database.
        
        Args:
            player: Player object to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO players (
                        id, name, stats, inventory, active_quests, completed_quests,
                        current_location, turn_number, last_choice, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player.id,
                    player.name,
                    json.dumps(player.stats.__dict__),
                    json.dumps(player.inventory),
                    json.dumps(player.active_quests),
                    json.dumps(player.completed_quests),
                    player.current_location,
                    player.turn_number,
                    player.last_choice,
                    player.created_at.isoformat(),
                    player.updated_at.isoformat()
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error creating player: {e}")
            return False
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """
        Retrieve a player by ID.
        
        Args:
            player_id: ID of the player to retrieve
            
        Returns:
            Player object if found, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
                row = cursor.fetchone()
                
                if row:
                    stats_data = json.loads(row['stats'])
                    stats = PlayerStats(**stats_data)
                    
                    return Player(
                        id=row['id'],
                        name=row['name'],
                        stats=stats,
                        inventory=json.loads(row['inventory']),
                        active_quests=json.loads(row['active_quests']),
                        completed_quests=json.loads(row['completed_quests']),
                        current_location=row['current_location'],
                        turn_number=row['turn_number'],
                        last_choice=row['last_choice'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at'])
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving player: {e}")
            return None
    
    def update_player(self, player: Player) -> bool:
        """
        Update an existing player in the database.
        
        Args:
            player: Player object with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            player.updated_at = datetime.now()
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE players SET
                        name = ?, stats = ?, inventory = ?, active_quests = ?,
                        completed_quests = ?, current_location = ?, turn_number = ?,
                        last_choice = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    player.name,
                    json.dumps(player.stats.__dict__),
                    json.dumps(player.inventory),
                    json.dumps(player.active_quests),
                    json.dumps(player.completed_quests),
                    player.current_location,
                    player.turn_number,
                    player.last_choice,
                    player.updated_at.isoformat(),
                    player.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating player: {e}")
            return False
    
    # Quest CRUD operations
    def create_quest(self, quest: Quest) -> bool:
        """
        Create a new quest in the database.
        
        Args:
            quest: Quest object to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                consequence_json = None
                if quest.consequence_thread:
                    consequence_json = json.dumps(quest.consequence_thread.__dict__)
                
                cursor.execute("""
                    INSERT INTO quests (
                        id, title, location, tags, intro, objectives, success, failure,
                        reward, risk, consequence_thread, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    quest.id,
                    quest.title,
                    quest.location,
                    json.dumps(quest.tags),
                    quest.intro,
                    json.dumps(quest.objectives),
                    quest.success,
                    quest.failure,
                    json.dumps(quest.reward.__dict__),
                    quest.risk.value,
                    consequence_json,
                    quest.status.value
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error creating quest: {e}")
            return False
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """
        Retrieve a quest by ID.
        
        Args:
            quest_id: ID of the quest to retrieve
            
        Returns:
            Quest object if found, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM quests WHERE id = ?", (quest_id,))
                row = cursor.fetchone()
                
                if row:
                    reward_data = json.loads(row['reward'])
                    reward = Reward(**reward_data)
                    
                    consequence_thread = None
                    if row['consequence_thread']:
                        ct_data = json.loads(row['consequence_thread'])
                        consequence_thread = ConsequenceThread(**ct_data)
                    
                    return Quest(
                        id=row['id'],
                        title=row['title'],
                        location=row['location'],
                        tags=json.loads(row['tags']),
                        intro=row['intro'],
                        objectives=json.loads(row['objectives']),
                        success=row['success'],
                        failure=row['failure'],
                        reward=reward,
                        risk=RiskLevel(row['risk']),
                        consequence_thread=consequence_thread,
                        status=QuestStatus(row['status'])
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving quest: {e}")
            return None
    
    def get_quests_by_location(self, location: str) -> List[Quest]:
        """
        Retrieve all quests for a specific location.
        
        Args:
            location: Location to filter quests by
            
        Returns:
            List of Quest objects
        """
        quests = []
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM quests WHERE location = ?", (location,))
                rows = cursor.fetchall()
                
                for row in rows:
                    quest = self.get_quest(row['id'])
                    if quest:
                        quests.append(quest)
        except sqlite3.Error as e:
            print(f"Error retrieving quests by location: {e}")
        
        return quests
    
    def get_all_quests(self) -> List[Quest]:
        """
        Retrieve all quests from the database.
        
        Returns:
            List of all Quest objects
        """
        quests = []
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM quests")
                rows = cursor.fetchall()
                
                for row in rows:
                    quest = self.get_quest(row['id'])
                    if quest:
                        quests.append(quest)
        except sqlite3.Error as e:
            print(f"Error retrieving all quests: {e}")
        
        return quests
    
    # Game event operations
    def log_event(self, event: GameEvent) -> bool:
        """
        Log a game event to the database.
        
        Args:
            event: GameEvent object to log
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO game_events (
                        id, player_id, event_type, description, data, turn_number, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id,
                    event.player_id,
                    event.event_type,
                    event.description,
                    json.dumps(event.data),
                    event.turn_number,
                    event.timestamp.isoformat()
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error logging event: {e}")
            return False
    
    def get_player_events(self, player_id: str, limit: int = 50) -> List[GameEvent]:
        """
        Retrieve recent events for a player.
        
        Args:
            player_id: ID of the player
            limit: Maximum number of events to retrieve
            
        Returns:
            List of GameEvent objects
        """
        events = []
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM game_events 
                    WHERE player_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (player_id, limit))
                rows = cursor.fetchall()
                
                for row in rows:
                    event = GameEvent(
                        id=row['id'],
                        player_id=row['player_id'],
                        event_type=row['event_type'],
                        description=row['description'],
                        data=json.loads(row['data']),
                        turn_number=row['turn_number'],
                        timestamp=datetime.fromisoformat(row['timestamp'])
                    )
                    events.append(event)
        except sqlite3.Error as e:
            print(f"Error retrieving player events: {e}")
        
        return events

