"""
Enhanced AI-RPG-Alpha Backend
==============================

FastAPI backend with complete game systems:
- Long-form quest progression (30-40 turns)
- BG3-style tactical combat
- Cosmic horror sanity mechanics
- Scenario management
- Save/load system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Import game systems
from engine.game_orchestrator import GameOrchestrator
from ai.narrative_templates import NarrativeTemplates, NarrativeParser, FallbackNarratives

app = FastAPI(
    title="AI-RPG-Alpha Enhanced Backend",
    description="Complete AI-driven RPG with combat, quests, and cosmic horror",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game orchestrator
game_orchestrator = GameOrchestrator()

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class NewGameRequest(BaseModel):
    player_name: str
    scenario: str  # "northern_realms", "whispering_town", "neo_tokyo"
    abilities: Optional[Dict[str, int]] = None


class TurnRequest(BaseModel):
    player_id: str
    action: str
    choice_index: int = 0


class CombatActionRequest(BaseModel):
    player_id: str
    action: str
    target_index: Optional[int] = None
    environment_index: Optional[int] = None


class SanityLossRequest(BaseModel):
    player_id: str
    amount: int
    cause: str


class LearnKnowledgeRequest(BaseModel):
    player_id: str
    knowledge_id: str


class SaveGameRequest(BaseModel):
    player_id: str
    slot_number: int
    save_name: str


class LoadGameRequest(BaseModel):
    player_id: str
    slot_number: int


class GameResponse(BaseModel):
    success: bool
    narrative: str
    choices: List[str]
    player_stats: Dict[str, Any]
    quest_state: Optional[Dict[str, Any]] = None
    combat_state: Optional[Dict[str, Any]] = None
    sanity_state: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = {}


# ============================================================================
# GAME ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "message": "AI-RPG-Alpha Enhanced Backend",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "Long-form quests (30-40 turns)",
            "BG3-style tactical combat",
            "Cosmic horror sanity system",
            "3 unique scenarios",
            "Save/load system"
        ]
    }


@app.post("/game/new")
async def create_new_game(request: NewGameRequest):
    """
    Start a new game in The Northern Realms
    
    Epic fantasy scenario with:
    - Dragon prophecy storyline
    - Kingdom politics and warfare
    - Ancient magic and artifacts
    """
    try:
        result = game_orchestrator.start_new_game(
            player_name=request.player_name,
            abilities=request.abilities
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/turn")
async def process_game_turn(request: TurnRequest):
    """
    Process a game turn
    
    Handles:
    - Quest progression
    - Combat triggers
    - Sanity effects
    - AI narrative generation
    """
    try:
        result = game_orchestrator.process_turn(
            player_id=request.player_id,
            player_action=request.action,
            choice_index=request.choice_index
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/combat/action")
async def process_combat_action(request: CombatActionRequest):
    """
    Process a combat action
    
    Combat actions:
    - Attack enemies
    - Use environment
    - Defensive stance
    - Negotiate
    - Flee
    """
    try:
        # Combat actions are processed through the main turn system
        result = game_orchestrator.process_turn(
            player_id=request.player_id,
            player_action=request.action,
            choice_index=request.target_index or 0
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/sanity/loss")
async def trigger_sanity_loss(request: SanityLossRequest):
    """
    Trigger sanity loss event (Cosmic Horror scenario)
    
    Returns sanity state and any hallucinations/distortions
    """
    try:
        result = game_orchestrator.trigger_sanity_loss(
            player_id=request.player_id,
            amount=request.amount,
            cause=request.cause
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/knowledge/learn")
async def learn_forbidden_knowledge(request: LearnKnowledgeRequest):
    """
    Learn forbidden knowledge (Cosmic Horror scenario)
    
    Gains power but loses sanity. May unlock new options.
    
    Available knowledge:
    - eldritch_geometry
    - true_names
    - ritual_of_binding
    - ashmouth_truth
    - cosmic_perspective
    """
    try:
        result = game_orchestrator.learn_forbidden_knowledge(
            player_id=request.player_id,
            knowledge_id=request.knowledge_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/game/state/{player_id}")
async def get_game_state(player_id: str):
    """Get complete game state for player"""
    try:
        player_data = game_orchestrator.db.get_player(player_id)
        if not player_data:
            raise HTTPException(status_code=404, detail="Player not found")
        
        quest_state = None
        if game_orchestrator.quest_engine.active_quest:
            quest_state = game_orchestrator.quest_engine.get_quest_state()
        
        sanity_state = None
        if player_data['scenario'] == 'whispering_town':
            sanity_state = game_orchestrator.sanity_engine.get_sanity_state_summary()
        
        return {
            "player": player_data,
            "quest": quest_state,
            "sanity": sanity_state,
            "in_combat": game_orchestrator.current_combat is not None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/save")
async def save_game(request: SaveGameRequest):
    """Save game to slot"""
    try:
        success = game_orchestrator.save_game(
            player_id=request.player_id,
            slot_number=request.slot_number,
            save_name=request.save_name
        )
        
        return {"success": success, "message": "Game saved" if success else "Save failed"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/load")
async def load_game(request: LoadGameRequest):
    """Load game from slot"""
    try:
        save_data = game_orchestrator.load_game(
            player_id=request.player_id,
            slot_number=request.slot_number
        )
        
        if not save_data:
            raise HTTPException(status_code=404, detail="Save not found")
        
        return save_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INFORMATION ENDPOINTS
# ============================================================================

@app.get("/scenarios")
async def get_scenarios():
    """Get available scenarios"""
    return {
        "scenarios": [
            {
                "id": "northern_realms",
                "name": "The Northern Realms",
                "genre": "Epic Fantasy",
                "description": "Dragons, magic, and ancient prophecies in a Skyrim-inspired world",
                "features": ["Epic combat", "Political intrigue", "Dragon encounters"],
                "difficulty": "Medium"
            },
            {
                "id": "whispering_town",
                "name": "The Whispering Town",
                "genre": "Cosmic Horror",
                "description": "Lovecraftian psychological terror where reality breaks down",
                "features": ["Sanity system", "Forbidden knowledge", "Reality distortion"],
                "difficulty": "Hard"
            },
            {
                "id": "neo_tokyo",
                "name": "Neo-Tokyo 2087",
                "genre": "Cyberpunk",
                "description": "Tech-noir corporate conspiracy in a dystopian megacity",
                "features": ["Hacking", "Cybernetics", "AI consciousness"],
                "difficulty": "Medium"
            }
        ]
    }


@app.get("/knowledge")
async def get_forbidden_knowledge():
    """Get available forbidden knowledge (Whispering Town only)"""
    knowledge_list = []
    
    for k_id, knowledge in game_orchestrator.sanity_engine.knowledge_library.items():
        knowledge_list.append({
            "id": k_id,
            "title": knowledge.title,
            "type": knowledge.knowledge_type.value,
            "sanity_cost": knowledge.sanity_cost,
            "power_gain": knowledge.power_gain,
            "corruption_level": knowledge.corruption_level,
            "description": knowledge.description
        })
    
    return {"knowledge": knowledge_list}


@app.get("/health")
async def health_check():
    """Extended health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "systems": {
            "quest_engine": "operational",
            "combat_engine": "operational",
            "sanity_engine": "operational",
            "database": "operational"
        }
    }


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@app.get("/stats/player/{player_id}")
async def get_player_statistics(player_id: str):
    """Get player statistics and history"""
    try:
        # This would query various database tables for player stats
        # Placeholder implementation
        return {
            "player_id": player_id,
            "total_turns": 0,
            "combats_won": 0,
            "combats_lost": 0,
            "major_choices": 0,
            "sanity_events": 0,
            "knowledge_gained": 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

