#!/usr/bin/env python3
"""
Simple script to run the AI-RPG-Alpha FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    print("Starting AI-RPG-Alpha Backend Server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 