"""
AI-RPG-Alpha: FastAPI Backend Entry Point

This is the main FastAPI application that serves as the backend for the AI-driven text-RPG engine.
It provides the /turn endpoint for game interactions and handles CORS for frontend communication.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import game engine components (will be implemented in later phases)
# from engine.context import build_game_context
# from engine.quest_picker import select_quest
# from engine.combat import resolve_combat
# from engine.consequence import schedule_consequence
# from ai.openai_client import OpenAIClient
# from dao.game_state import GameStateDAO
# from dao.memory import MemoryDAO

app = FastAPI(
    title="AI-RPG-Alpha Backend",
    description="Backend API for AI-driven text-RPG engine",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class TurnRequest(BaseModel):
    player_id: str
    choice: str

class TurnResponse(BaseModel):
    narrative: str
    choices: List[str]
    metadata: dict = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI-RPG-Alpha Backend v0.1.0", "status": "running"}

@app.post("/turn", response_model=TurnResponse)
async def process_turn(request: TurnRequest):
    """
    Main game turn processing endpoint.
    
    This endpoint receives a player's choice and returns the next narrative
    segment along with available choices for the next turn.
    
    Args:
        request: TurnRequest containing player_id and choice
        
    Returns:
        TurnResponse with narrative text and available choices
    """
    try:
        # TODO: Implement full game logic in later phases
        # For now, return a placeholder response
        
        # Validate OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured"
            )
        
        # Placeholder response for v0.1 scaffold
        sample_narrative = f"""
        Welcome to the AI-RPG-Alpha engine, {request.player_id}!
        
        You find yourself standing at the edge of a mysterious forest. The ancient trees 
        whisper secrets in the wind, and you can sense that adventure awaits within their 
        shadowy depths. Your choice was: "{request.choice}"
        
        The path ahead splits into three directions, each promising different challenges 
        and rewards. What will you choose?
        """
        
        sample_choices = [
            "Take the left path toward the glowing mushrooms",
            "Follow the right path where you hear distant music",
            "Walk straight into the heart of the forest",
            "Turn back and seek another adventure"
        ]
        
        # Metadata for frontend (music selection, risk level, etc.)
        metadata = {
            "risk_level": "calm",  # calm, mystery, combat
            "location": "forest_entrance",
            "turn_number": 1
        }
        
        return TurnResponse(
            narrative=sample_narrative.strip(),
            choices=sample_choices,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Game processing error: {str(e)}")

@app.get("/health")
async def health_check():
    """Extended health check with system status"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "components": {
            "database": "not_implemented",  # Will be updated in later phases
            "vector_store": "not_implemented",
            "ai_client": "not_implemented"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

