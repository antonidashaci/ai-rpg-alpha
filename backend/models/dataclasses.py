"""
AI-RPG-Alpha: Data Models

This module defines the core data structures used throughout the AI-RPG engine.
These dataclasses represent the main entities: Player, Quest, Memory, and related objects.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class RiskLevel(Enum):
    """Risk levels for quests and encounters"""
    CALM = "calm"
    MYSTERY = "mystery"
    COMBAT = "combat"

class QuestStatus(Enum):
    """Status of a quest"""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Reward:
    """Represents quest rewards"""
    gold: int = 0
    items: List[str] = field(default_factory=list)
    experience: int = 0

@dataclass
class ConsequenceThread:
    """Represents delayed consequences that trigger after certain conditions"""
    trigger_turn: int
    event: str
    description: str = ""
    executed: bool = False

@dataclass
class Quest:
    """
    Represents a quest in the game world.
    
    Quests are the primary content units that drive the narrative forward.
    They contain objectives, rewards, and consequences.
    """
    id: str
    title: str
    location: str
    tags: List[str] = field(default_factory=list)
    intro: str = ""
    objectives: List[str] = field(default_factory=list)
    success: str = ""
    failure: str = ""
    reward: Reward = field(default_factory=Reward)
    risk: RiskLevel = RiskLevel.CALM
    consequence_thread: Optional[ConsequenceThread] = None
    status: QuestStatus = QuestStatus.AVAILABLE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quest to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "tags": self.tags,
            "intro": self.intro,
            "objectives": self.objectives,
            "success": self.success,
            "failure": self.failure,
            "reward": {
                "gold": self.reward.gold,
                "items": self.reward.items,
                "experience": self.reward.experience
            },
            "risk": self.risk.value,
            "consequence_thread": {
                "trigger_turn": self.consequence_thread.trigger_turn,
                "event": self.consequence_thread.event,
                "description": self.consequence_thread.description,
                "executed": self.consequence_thread.executed
            } if self.consequence_thread else None,
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quest':
        """Create Quest from dictionary"""
        reward = Reward(
            gold=data.get("reward", {}).get("gold", 0),
            items=data.get("reward", {}).get("items", []),
            experience=data.get("reward", {}).get("experience", 0)
        )
        
        consequence_thread = None
        if data.get("consequence_thread"):
            ct_data = data["consequence_thread"]
            consequence_thread = ConsequenceThread(
                trigger_turn=ct_data["trigger_turn"],
                event=ct_data["event"],
                description=ct_data.get("description", ""),
                executed=ct_data.get("executed", False)
            )
        
        return cls(
            id=data["id"],
            title=data["title"],
            location=data["location"],
            tags=data.get("tags", []),
            intro=data.get("intro", ""),
            objectives=data.get("objectives", []),
            success=data.get("success", ""),
            failure=data.get("failure", ""),
            reward=reward,
            risk=RiskLevel(data.get("risk", "calm")),
            consequence_thread=consequence_thread,
            status=QuestStatus(data.get("status", "available"))
        )

@dataclass
class PlayerStats:
    """Player statistics and attributes"""
    health: int = 100
    mana: int = 50
    strength: int = 10
    intelligence: int = 10
    charisma: int = 10
    level: int = 1
    experience: int = 0
    gold: int = 100

@dataclass
class Player:
    """
    Represents a player character in the game.
    
    Contains all player state including stats, inventory, quest progress,
    and current game position.
    """
    id: str
    name: str
    stats: PlayerStats = field(default_factory=PlayerStats)
    inventory: List[str] = field(default_factory=list)
    active_quests: List[str] = field(default_factory=list)  # Quest IDs
    completed_quests: List[str] = field(default_factory=list)  # Quest IDs
    current_location: str = "starting_village"
    turn_number: int = 0
    last_choice: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "stats": {
                "health": self.stats.health,
                "mana": self.stats.mana,
                "strength": self.stats.strength,
                "intelligence": self.stats.intelligence,
                "charisma": self.stats.charisma,
                "level": self.stats.level,
                "experience": self.stats.experience,
                "gold": self.stats.gold
            },
            "inventory": self.inventory,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "current_location": self.current_location,
            "turn_number": self.turn_number,
            "last_choice": self.last_choice,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create Player from dictionary"""
        stats = PlayerStats(
            health=data.get("stats", {}).get("health", 100),
            mana=data.get("stats", {}).get("mana", 50),
            strength=data.get("stats", {}).get("strength", 10),
            intelligence=data.get("stats", {}).get("intelligence", 10),
            charisma=data.get("stats", {}).get("charisma", 10),
            level=data.get("stats", {}).get("level", 1),
            experience=data.get("stats", {}).get("experience", 0),
            gold=data.get("stats", {}).get("gold", 100)
        )
        
        return cls(
            id=data["id"],
            name=data["name"],
            stats=stats,
            inventory=data.get("inventory", []),
            active_quests=data.get("active_quests", []),
            completed_quests=data.get("completed_quests", []),
            current_location=data.get("current_location", "starting_village"),
            turn_number=data.get("turn_number", 0),
            last_choice=data.get("last_choice", ""),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        )

@dataclass
class Memory:
    """
    Represents a memory entry for the vector database.
    
    Memories are used to maintain context and continuity in the AI-generated narrative.
    They are stored as embeddings for semantic similarity search.
    """
    id: str
    player_id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    turn_number: int = 0
    importance: float = 1.0  # 0.0 to 1.0, higher = more important
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "turn_number": self.turn_number,
            "importance": self.importance,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        """Create Memory from dictionary"""
        return cls(
            id=data["id"],
            player_id=data["player_id"],
            content=data["content"],
            embedding=data.get("embedding"),
            metadata=data.get("metadata", {}),
            turn_number=data.get("turn_number", 0),
            importance=data.get("importance", 1.0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        )

@dataclass
class GameEvent:
    """
    Represents a game event for logging and consequence tracking.
    """
    id: str
    player_id: str
    event_type: str  # "quest_start", "quest_complete", "combat", "choice", etc.
    description: str
    data: Dict[str, Any] = field(default_factory=dict)
    turn_number: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "event_type": self.event_type,
            "description": self.description,
            "data": self.data,
            "turn_number": self.turn_number,
            "timestamp": self.timestamp.isoformat()
        }

