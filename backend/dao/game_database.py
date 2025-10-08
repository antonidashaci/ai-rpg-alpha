"""
Enhanced Game Database Schema
==============================

Comprehensive database schema for:
- Player characters and progression
- Long-form quest states
- Combat encounters and history
- Sanity tracking for cosmic horror
- Scenario management
- Save/load system
"""

import sqlite3
from typing import Optional, Dict, List, Any
from datetime import datetime
import json


class GameDatabase:
    """Enhanced SQLite database for AI-RPG-Alpha"""
    
    def __init__(self, db_path: str = "game_data.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.initialize_database()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def initialize_database(self):
        """Create all necessary tables"""
        self.connect()
        
        # Players table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                scenario TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                
                -- Core Stats
                health INTEGER DEFAULT 20,
                max_health INTEGER DEFAULT 20,
                gold INTEGER DEFAULT 50,
                
                -- D&D Abilities
                strength INTEGER DEFAULT 10,
                dexterity INTEGER DEFAULT 10,
                constitution INTEGER DEFAULT 10,
                intelligence INTEGER DEFAULT 10,
                wisdom INTEGER DEFAULT 10,
                charisma INTEGER DEFAULT 10,
                
                -- Combat Resources
                stamina INTEGER DEFAULT 100,
                max_stamina INTEGER DEFAULT 100,
                action_points INTEGER DEFAULT 2,
                max_action_points INTEGER DEFAULT 2,
                
                -- Cosmic Horror Specific
                sanity INTEGER DEFAULT 100,
                max_sanity INTEGER DEFAULT 100,
                corruption_level INTEGER DEFAULT 0,
                
                -- Location and State
                current_location TEXT DEFAULT 'starting_village',
                current_quest_id TEXT,
                
                -- Metadata
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_played TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Quest States table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS quest_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                quest_id TEXT NOT NULL,
                scenario TEXT NOT NULL,
                status TEXT NOT NULL,
                
                -- Progression
                current_turn INTEGER DEFAULT 1,
                current_act TEXT DEFAULT 'setup',
                total_turns INTEGER DEFAULT 40,
                
                -- Statistics
                milestones_completed TEXT DEFAULT '[]',
                combat_encounters INTEGER DEFAULT 0,
                major_choices INTEGER DEFAULT 0,
                
                -- State Data (JSON)
                progression_data TEXT,
                choices_made TEXT DEFAULT '[]',
                information_revealed TEXT DEFAULT '[]',
                
                -- Timestamps
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id),
                UNIQUE(player_id, quest_id)
            )
        """)
        
        # Combat Encounters table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS combat_encounters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                quest_id TEXT,
                encounter_id TEXT NOT NULL,
                
                -- Combat Details
                difficulty TEXT NOT NULL,
                outcome TEXT,
                turns_taken INTEGER DEFAULT 0,
                player_health_start INTEGER,
                player_health_end INTEGER,
                
                -- Combat Statistics
                damage_dealt INTEGER DEFAULT 0,
                damage_taken INTEGER DEFAULT 0,
                environmental_actions INTEGER DEFAULT 0,
                successful_negotiations INTEGER DEFAULT 0,
                
                -- State Data (JSON)
                enemies_data TEXT,
                environment_data TEXT,
                combat_log TEXT DEFAULT '[]',
                
                -- Timestamps
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                ended_at TEXT,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        """)
        
        # Sanity Events table (Cosmic Horror)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sanity_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                quest_id TEXT,
                
                -- Event Details
                event_type TEXT NOT NULL,
                sanity_change INTEGER NOT NULL,
                old_sanity INTEGER NOT NULL,
                new_sanity INTEGER NOT NULL,
                old_level TEXT NOT NULL,
                new_level TEXT NOT NULL,
                
                -- Context
                cause TEXT NOT NULL,
                is_voluntary INTEGER DEFAULT 0,
                
                -- Effects
                hallucination_triggered INTEGER DEFAULT 0,
                distortions_added TEXT DEFAULT '[]',
                
                -- Timestamp
                occurred_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        """)
        
        # Forbidden Knowledge table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS player_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                knowledge_id TEXT NOT NULL,
                
                -- Knowledge Details
                title TEXT NOT NULL,
                knowledge_type TEXT NOT NULL,
                sanity_cost INTEGER NOT NULL,
                power_gain INTEGER NOT NULL,
                corruption_level INTEGER NOT NULL,
                
                -- Timestamp
                learned_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id),
                UNIQUE(player_id, knowledge_id)
            )
        """)
        
        # Game Events table (Turn-by-turn history)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS game_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                quest_id TEXT,
                turn_number INTEGER NOT NULL,
                
                -- Event Details
                event_type TEXT NOT NULL,
                player_action TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                
                -- Context (JSON)
                context_data TEXT,
                
                -- Timestamp
                occurred_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        """)
        
        # Inventory table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                item_name TEXT NOT NULL,
                item_type TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                description TEXT,
                
                -- Item Properties (JSON)
                properties TEXT,
                
                -- Timestamp
                acquired_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        """)
        
        # Magic System table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS player_magic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,

                -- Magic Stats
                mage_level INTEGER DEFAULT 1,
                mana INTEGER DEFAULT 10,
                max_mana INTEGER DEFAULT 10,

                -- School Affinities
                destruction_affinity INTEGER DEFAULT 0,
                restoration_affinity INTEGER DEFAULT 0,
                alteration_affinity INTEGER DEFAULT 0,
                conjuration_affinity INTEGER DEFAULT 0,
                illusion_affinity INTEGER DEFAULT 0,
                enchantment_affinity INTEGER DEFAULT 0,

                -- Known Spells (JSON)
                known_spells TEXT DEFAULT '[]',

                -- Concentration
                concentration_spell TEXT,

                -- Equipped Artifacts (JSON)
                equipped_artifacts TEXT DEFAULT '[]',

                -- Timestamps
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (player_id) REFERENCES players (player_id),
                UNIQUE(player_id)
            )
        """)

        # NPC Relationships table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS npc_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                npc_id TEXT NOT NULL,

                -- Relationship Stats
                reputation INTEGER DEFAULT 0,
                current_mood TEXT DEFAULT 'neutral',
                conversations_completed INTEGER DEFAULT 0,

                -- Dialogue Progress
                current_node_id TEXT DEFAULT 'greeting',
                dialogue_history TEXT DEFAULT '[]',

                -- Timestamps
                first_met_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_interaction_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (player_id) REFERENCES players (player_id),
                UNIQUE(player_id, npc_id)
            )
        """)

        # Political Events table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS political_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Event Details
                event_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,

                -- Affected Kingdoms
                primary_kingdom TEXT NOT NULL,
                affected_kingdoms TEXT DEFAULT '[]',

                -- Effects (JSON)
                reputation_changes TEXT DEFAULT '{}',
                status_changes TEXT DEFAULT '{}',
                relation_changes TEXT DEFAULT '{}',

                -- Turn Information
                occurred_turn INTEGER,
                triggered_by_player_id TEXT,

                -- Timestamps
                occurred_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (triggered_by_player_id) REFERENCES players (player_id)
            )
        """)

        # Save Slots table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS save_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                slot_number INTEGER NOT NULL,
                save_name TEXT NOT NULL,

                -- Game State Snapshot (JSON)
                player_state TEXT NOT NULL,
                quest_state TEXT,
                combat_state TEXT,
                magic_state TEXT,
                npc_state TEXT,
                political_state TEXT,
                inventory_state TEXT,

                -- Metadata
                scenario TEXT NOT NULL,
                turn_number INTEGER NOT NULL,
                playtime_minutes INTEGER DEFAULT 0,

                -- Timestamps
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (player_id) REFERENCES players (player_id),
                UNIQUE(player_id, slot_number)
            )
        """)
        
        self.conn.commit()
        self.disconnect()
    
    # ========================================================================
    # PLAYER OPERATIONS
    # ========================================================================
    
    def create_player(
        self,
        player_id: str,
        name: str,
        scenario: str,
        abilities: Optional[Dict[str, int]] = None
    ) -> bool:
        """Create new player"""
        self.connect()
        
        try:
            cursor = self.conn.cursor()
            
            if abilities:
                cursor.execute("""
                    INSERT INTO players (
                        player_id, name, scenario,
                        strength, dexterity, constitution,
                        intelligence, wisdom, charisma
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player_id, name, scenario,
                    abilities.get('strength', 10),
                    abilities.get('dexterity', 10),
                    abilities.get('constitution', 10),
                    abilities.get('intelligence', 10),
                    abilities.get('wisdom', 10),
                    abilities.get('charisma', 10)
                ))
            else:
                cursor.execute("""
                    INSERT INTO players (player_id, name, scenario)
                    VALUES (?, ?, ?)
                """, (player_id, name, scenario))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
        finally:
            self.disconnect()
    
    def get_player(self, player_id: str) -> Optional[Dict]:
        """Get player data"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
        row = cursor.fetchone()
        
        self.disconnect()
        
        if row:
            return dict(row)
        return None
    
    def update_player_stats(self, player_id: str, stats: Dict[str, Any]) -> bool:
        """Update player statistics"""
        self.connect()
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        
        for key, value in stats.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        values.append(player_id)
        
        query = f"UPDATE players SET {', '.join(set_clauses)}, last_played = CURRENT_TIMESTAMP WHERE player_id = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        success = cursor.rowcount > 0
        self.disconnect()
        
        return success
    
    # ========================================================================
    # QUEST STATE OPERATIONS
    # ========================================================================
    
    def create_quest_state(
        self,
        player_id: str,
        quest_id: str,
        scenario: str,
        total_turns: int = 40
    ) -> bool:
        """Create new quest state"""
        self.connect()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO quest_states (
                    player_id, quest_id, scenario, status, total_turns
                ) VALUES (?, ?, ?, 'active', ?)
            """, (player_id, quest_id, scenario, total_turns))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
        finally:
            self.disconnect()
    
    def get_quest_state(self, player_id: str, quest_id: str) -> Optional[Dict]:
        """Get quest state"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM quest_states 
            WHERE player_id = ? AND quest_id = ?
        """, (player_id, quest_id))
        
        row = cursor.fetchone()
        self.disconnect()
        
        if row:
            data = dict(row)
            # Parse JSON fields
            data['milestones_completed'] = json.loads(data['milestones_completed'])
            data['choices_made'] = json.loads(data['choices_made'])
            data['information_revealed'] = json.loads(data['information_revealed'])
            if data['progression_data']:
                data['progression_data'] = json.loads(data['progression_data'])
            return data
        
        return None
    
    def update_quest_state(
        self,
        player_id: str,
        quest_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """Update quest state"""
        self.connect()
        
        # Serialize JSON fields
        if 'milestones_completed' in updates:
            updates['milestones_completed'] = json.dumps(updates['milestones_completed'])
        if 'choices_made' in updates:
            updates['choices_made'] = json.dumps(updates['choices_made'])
        if 'information_revealed' in updates:
            updates['information_revealed'] = json.dumps(updates['information_revealed'])
        if 'progression_data' in updates:
            updates['progression_data'] = json.dumps(updates['progression_data'])
        
        # Build UPDATE query
        set_clauses = []
        values = []
        
        for key, value in updates.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        values.extend([player_id, quest_id])
        
        query = f"""
            UPDATE quest_states 
            SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP 
            WHERE player_id = ? AND quest_id = ?
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        success = cursor.rowcount > 0
        self.disconnect()
        
        return success
    
    # ========================================================================
    # COMBAT OPERATIONS
    # ========================================================================
    
    def create_combat_encounter(
        self,
        player_id: str,
        encounter_id: str,
        difficulty: str,
        player_health: int,
        enemies_data: List[Dict],
        environment_data: List[Dict],
        quest_id: Optional[str] = None
    ) -> int:
        """Create combat encounter record"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO combat_encounters (
                player_id, quest_id, encounter_id, difficulty,
                player_health_start, enemies_data, environment_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id, quest_id, encounter_id, difficulty,
            player_health, json.dumps(enemies_data), json.dumps(environment_data)
        ))
        
        encounter_db_id = cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        
        return encounter_db_id
    
    def update_combat_encounter(
        self,
        encounter_db_id: int,
        outcome: str,
        turns_taken: int,
        player_health_end: int,
        combat_log: List[str],
        stats: Optional[Dict] = None
    ) -> bool:
        """Update combat encounter with results"""
        self.connect()
        
        updates = {
            'outcome': outcome,
            'turns_taken': turns_taken,
            'player_health_end': player_health_end,
            'combat_log': json.dumps(combat_log),
            'ended_at': datetime.now().isoformat()
        }
        
        if stats:
            updates.update(stats)
        
        set_clauses = [f"{k} = ?" for k in updates.keys()]
        values = list(updates.values())
        values.append(encounter_db_id)
        
        query = f"UPDATE combat_encounters SET {', '.join(set_clauses)} WHERE id = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        success = cursor.rowcount > 0
        self.disconnect()
        
        return success
    
    # ========================================================================
    # SANITY OPERATIONS (Cosmic Horror)
    # ========================================================================
    
    def record_sanity_event(
        self,
        player_id: str,
        event_type: str,
        sanity_change: int,
        old_sanity: int,
        new_sanity: int,
        old_level: str,
        new_level: str,
        cause: str,
        is_voluntary: bool = False,
        hallucination_triggered: bool = False,
        distortions_added: Optional[List[str]] = None,
        quest_id: Optional[str] = None
    ) -> int:
        """Record sanity event"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sanity_events (
                player_id, quest_id, event_type, sanity_change,
                old_sanity, new_sanity, old_level, new_level,
                cause, is_voluntary, hallucination_triggered, distortions_added
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id, quest_id, event_type, sanity_change,
            old_sanity, new_sanity, old_level, new_level,
            cause, int(is_voluntary), int(hallucination_triggered),
            json.dumps(distortions_added or [])
        ))
        
        event_id = cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        
        return event_id
    
    def record_forbidden_knowledge(
        self,
        player_id: str,
        knowledge_id: str,
        title: str,
        knowledge_type: str,
        sanity_cost: int,
        power_gain: int,
        corruption_level: int
    ) -> bool:
        """Record learned forbidden knowledge"""
        self.connect()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO player_knowledge (
                    player_id, knowledge_id, title, knowledge_type,
                    sanity_cost, power_gain, corruption_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id, knowledge_id, title, knowledge_type,
                sanity_cost, power_gain, corruption_level
            ))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
        finally:
            self.disconnect()
    
    # ========================================================================
    # GAME EVENT LOGGING
    # ========================================================================
    
    def log_game_event(
        self,
        player_id: str,
        turn_number: int,
        event_type: str,
        player_action: str,
        ai_response: str,
        context_data: Optional[Dict] = None,
        quest_id: Optional[str] = None
    ) -> int:
        """Log game event"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO game_events (
                player_id, quest_id, turn_number, event_type,
                player_action, ai_response, context_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id, quest_id, turn_number, event_type,
            player_action, ai_response,
            json.dumps(context_data) if context_data else None
        ))
        
        event_id = cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        
        return event_id
    
    # ========================================================================
    # SAVE/LOAD OPERATIONS
    # ========================================================================
    
    def create_save(
        self,
        player_id: str,
        slot_number: int,
        save_name: str,
        game_state: Dict[str, Any]
    ) -> bool:
        """Create or update save slot"""
        self.connect()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO save_slots (
                    player_id, slot_number, save_name, scenario, turn_number,
                    player_state, quest_state, combat_state, sanity_state, inventory_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id, slot_number, save_name,
                game_state.get('scenario', ''),
                game_state.get('turn_number', 0),
                json.dumps(game_state.get('player_state', {})),
                json.dumps(game_state.get('quest_state', {})),
                json.dumps(game_state.get('combat_state', {})),
                json.dumps(game_state.get('sanity_state', {})),
                json.dumps(game_state.get('inventory_state', []))
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Save error: {e}")
            return False
        finally:
            self.disconnect()
    
    def load_save(self, player_id: str, slot_number: int) -> Optional[Dict]:
        """Load save from slot"""
        self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM save_slots 
            WHERE player_id = ? AND slot_number = ?
        """, (player_id, slot_number))
        
        row = cursor.fetchone()
        self.disconnect()
        
        if row:
            data = dict(row)
            # Parse JSON fields
            data['player_state'] = json.loads(data['player_state'])
            data['quest_state'] = json.loads(data['quest_state']) if data['quest_state'] else None
            data['combat_state'] = json.loads(data['combat_state']) if data['combat_state'] else None
            data['sanity_state'] = json.loads(data['sanity_state']) if data['sanity_state'] else None
            data['inventory_state'] = json.loads(data['inventory_state']) if data['inventory_state'] else []
            return data
        
        return None

