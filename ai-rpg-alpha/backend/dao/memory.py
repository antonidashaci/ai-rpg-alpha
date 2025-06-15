"""
AI-RPG-Alpha: Memory Data Access Object

This module handles ChromaDB vector database operations for AI memory management.
It provides semantic similarity search capabilities for maintaining narrative context.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Optional, Dict, Any
import uuid
import os
from datetime import datetime

from models.dataclasses import Memory

class MemoryDAO:
    """
    Data Access Object for AI memory management using ChromaDB.
    
    Handles vector embeddings and semantic similarity search for maintaining
    narrative context and continuity across game sessions.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "game_memories"):
        """
        Initialize the MemoryDAO with ChromaDB client and embedding model.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "AI-RPG game memories for narrative context"}
        )
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding vector for the given text.
        
        Args:
            text: Text to create embedding for
            
        Returns:
            List of float values representing the embedding
        """
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []
    
    def store_memory(self, memory: Memory) -> bool:
        """
        Store a memory in the vector database.
        
        Args:
            memory: Memory object to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create embedding if not provided
            if not memory.embedding:
                memory.embedding = self.create_embedding(memory.content)
            
            # Prepare metadata
            metadata = {
                "player_id": memory.player_id,
                "turn_number": memory.turn_number,
                "importance": memory.importance,
                "created_at": memory.created_at.isoformat(),
                **memory.metadata  # Include any additional metadata
            }
            
            # Store in ChromaDB
            self.collection.add(
                ids=[memory.id],
                embeddings=[memory.embedding],
                documents=[memory.content],
                metadatas=[metadata]
            )
            
            return True
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve_memories(
        self, 
        query_text: str, 
        player_id: str, 
        n_results: int = 5,
        importance_threshold: float = 0.0
    ) -> List[Memory]:
        """
        Retrieve memories similar to the query text for a specific player.
        
        Args:
            query_text: Text to search for similar memories
            player_id: ID of the player to filter memories for
            n_results: Maximum number of results to return
            importance_threshold: Minimum importance score to include
            
        Returns:
            List of Memory objects ordered by similarity
        """
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query_text)
            
            if not query_embedding:
                return []
            
            # Search for similar memories
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where={
                    "$and": [
                        {"player_id": {"$eq": player_id}},
                        {"importance": {"$gte": importance_threshold}}
                    ]
                },
                include=["documents", "metadatas", "distances", "embeddings"]
            )
            
            memories = []
            if results['ids'] and results['ids'][0]:
                for i, memory_id in enumerate(results['ids'][0]):
                    metadata = results['metadatas'][0][i]
                    
                    memory = Memory(
                        id=memory_id,
                        player_id=metadata['player_id'],
                        content=results['documents'][0][i],
                        embedding=results['embeddings'][0][i] if results['embeddings'] else None,
                        metadata={k: v for k, v in metadata.items() 
                                if k not in ['player_id', 'turn_number', 'importance', 'created_at']},
                        turn_number=metadata.get('turn_number', 0),
                        importance=metadata.get('importance', 1.0),
                        created_at=datetime.fromisoformat(metadata.get('created_at', datetime.now().isoformat()))
                    )
                    memories.append(memory)
            
            return memories
            
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def get_recent_memories(
        self, 
        player_id: str, 
        n_results: int = 10,
        turns_back: int = 5
    ) -> List[Memory]:
        """
        Retrieve recent memories for a player within a certain turn range.
        
        Args:
            player_id: ID of the player
            n_results: Maximum number of results to return
            turns_back: How many turns back to look
            
        Returns:
            List of recent Memory objects
        """
        try:
            # Get all memories for the player
            results = self.collection.get(
                where={"player_id": {"$eq": player_id}},
                include=["documents", "metadatas", "embeddings"]
            )
            
            memories = []
            if results['ids']:
                for i, memory_id in enumerate(results['ids']):
                    metadata = results['metadatas'][i]
                    
                    memory = Memory(
                        id=memory_id,
                        player_id=metadata['player_id'],
                        content=results['documents'][i],
                        embedding=results['embeddings'][i] if results['embeddings'] else None,
                        metadata={k: v for k, v in metadata.items() 
                                if k not in ['player_id', 'turn_number', 'importance', 'created_at']},
                        turn_number=metadata.get('turn_number', 0),
                        importance=metadata.get('importance', 1.0),
                        created_at=datetime.fromisoformat(metadata.get('created_at', datetime.now().isoformat()))
                    )
                    memories.append(memory)
            
            # Sort by turn number (most recent first) and limit results
            memories.sort(key=lambda m: m.turn_number, reverse=True)
            return memories[:n_results]
            
        except Exception as e:
            print(f"Error retrieving recent memories: {e}")
            return []
    
    def update_memory_importance(self, memory_id: str, new_importance: float) -> bool:
        """
        Update the importance score of a memory.
        
        Args:
            memory_id: ID of the memory to update
            new_importance: New importance score (0.0 to 1.0)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the existing memory
            results = self.collection.get(
                ids=[memory_id],
                include=["documents", "metadatas", "embeddings"]
            )
            
            if not results['ids'] or not results['ids'][0]:
                return False
            
            # Update metadata
            metadata = results['metadatas'][0]
            metadata['importance'] = new_importance
            
            # Update in ChromaDB (delete and re-add with new metadata)
            self.collection.delete(ids=[memory_id])
            self.collection.add(
                ids=[memory_id],
                embeddings=[results['embeddings'][0]],
                documents=[results['documents'][0]],
                metadatas=[metadata]
            )
            
            return True
            
        except Exception as e:
            print(f"Error updating memory importance: {e}")
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory from the vector database.
        
        Args:
            memory_id: ID of the memory to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[memory_id])
            return True
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False
    
    def get_memory_count(self, player_id: str) -> int:
        """
        Get the total number of memories for a player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            int: Number of memories
        """
        try:
            results = self.collection.get(
                where={"player_id": {"$eq": player_id}},
                include=[]  # Only need count, not data
            )
            return len(results['ids']) if results['ids'] else 0
        except Exception as e:
            print(f"Error getting memory count: {e}")
            return 0
    
    def cleanup_old_memories(self, player_id: str, max_memories: int = 100) -> bool:
        """
        Clean up old memories to maintain performance, keeping only the most important ones.
        
        Args:
            player_id: ID of the player
            max_memories: Maximum number of memories to keep
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get all memories for the player
            results = self.collection.get(
                where={"player_id": {"$eq": player_id}},
                include=["metadatas"]
            )
            
            if not results['ids'] or len(results['ids']) <= max_memories:
                return True  # No cleanup needed
            
            # Sort by importance and turn number, keep the most important/recent
            memory_data = []
            for i, memory_id in enumerate(results['ids']):
                metadata = results['metadatas'][i]
                memory_data.append({
                    'id': memory_id,
                    'importance': metadata.get('importance', 1.0),
                    'turn_number': metadata.get('turn_number', 0)
                })
            
            # Sort by importance (desc) then by turn number (desc)
            memory_data.sort(key=lambda x: (x['importance'], x['turn_number']), reverse=True)
            
            # Delete the least important memories
            memories_to_delete = memory_data[max_memories:]
            ids_to_delete = [m['id'] for m in memories_to_delete]
            
            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
            
            return True
            
        except Exception as e:
            print(f"Error cleaning up memories: {e}")
            return False

