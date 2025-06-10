#!/usr/bin/env python3
"""
AI-RPG-Alpha Game Launcher

Simple launcher that starts the main game.
"""

import os
import sys

def main():
    """Launch the AI-RPG-Alpha game"""
    print("🎮 Starting AI-RPG-Alpha...")
    print("=" * 50)
    
    try:
        # Import and run the main game
        from main_game import AIRPGGame
        
        # Create and run the game
        game = AIRPGGame()
        game.run()
        
    except ImportError as e:
        print(f"Error importing game: {e}")
        print("\nTrying to run main_game.py directly...")
        
        # Try to run main_game.py as a subprocess instead
        import subprocess
        try:
            subprocess.run([sys.executable, "main_game.py"])
        except Exception as e2:
            print(f"Error running game: {e2}")
            print("\nPlease run 'python main_game.py' directly from your Python environment.")
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please check that all game files are present.")

if __name__ == "__main__":
    main() 