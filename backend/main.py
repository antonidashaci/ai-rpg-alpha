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

# Import AI client
from ai.gemini_client import GeminiClient

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

# Initialize AI client
ai_client = GeminiClient()

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
        # Handle initial game start
        if request.choice.lower() in ["start", "begin", "begin adventure"]:
            context = {
                'location': 'starting_village',
                'turn_number': 1,
                'risk_level': 'calm'
            }
            
            # Generate initial story with Gemini
            story_response = ai_client.generate_story_response(
                player_name=request.player_id,
                choice="starting the adventure",
                context=context
            )
            
            return TurnResponse(
                narrative=story_response['narrative'],
                choices=story_response['choices'],
                metadata=story_response['metadata']
            )
        
        # Handle regular game turns
        # For now, we'll use basic context - in later phases this will come from database
        context = {
            'location': 'adventure_realm',
            'turn_number': 2,
            'risk_level': 'mystery'
        }
        
        # Generate story response with Gemini AI
        story_response = ai_client.generate_story_response(
            player_name=request.player_id,
            choice=request.choice,
            context=context
        )
        
        return TurnResponse(
            narrative=story_response['narrative'],
            choices=story_response['choices'],
            metadata=story_response['metadata']
        )
        
    except Exception as e:
        print(f"Error processing turn: {e}")
        raise HTTPException(status_code=500, detail=f"Game processing error: {str(e)}")

@app.get("/health")
async def health_check():
    """Extended health check with system status"""
    try:
        # Test AI client
        test_response = ai_client._get_fallback_response("Test", "health check")
        ai_status = "connected" if test_response else "error"
    except:
        ai_status = "error"
        
    return {
        "status": "healthy",
        "version": "0.1.0",
        "gemini_configured": bool(ai_client.api_key),
        "components": {
            "database": "not_implemented",  # Will be updated in later phases
            "vector_store": "not_implemented",
            "ai_client": ai_status
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

