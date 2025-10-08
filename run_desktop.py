#!/usr/bin/env python3
"""
Desktop Application Launcher for AI-RPG-Alpha
=============================================

This script launches the desktop application and ensures all dependencies are met.
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'PyQt6',
        'SQLAlchemy',
        'pydantic',
        'requests'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'PyQt6':
                # Special check for PyQt6
                import PyQt6
            else:
                importlib.import_module(package.lower().replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing missing dependencies...")

    try:
        # Install from desktop_requirements.txt if it exists
        if os.path.exists('desktop_requirements.txt'):
            print("📋 Installing from desktop_requirements.txt...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'desktop_requirements.txt'
            ])
        else:
            print("❌ desktop_requirements.txt not found!")
            print("Please run: pip install PyQt6 SQLAlchemy pydantic requests")

        print("✅ Dependencies installed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_database():
    """Initialize game database"""
    try:
        from backend.dao.game_database import GameDatabase

        print("🗄️ Initializing game database...")
        db = GameDatabase()
        print("✅ Database initialized successfully!")

        return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def check_local_llm():
    """Check if local LLM is available"""
    try:
        from backend.ai.local_llm_client import LocalLLMClient

        print("🤖 Checking local LLM status...")
        client = LocalLLMClient()

        if client.connected:
            models = client.get_available_models()
            print(f"✅ Local LLM connected! Available models: {len(models)}")
            for model in models[:3]:  # Show first 3
                print(f"  • {model}")
            return True
        else:
            print("⚠️ Local LLM not available. Game will work with fallback responses.")
            print("💡 To enable AI features, install Ollama and run: ollama pull llama2")
            return False

    except Exception as e:
        print(f"❌ LLM check failed: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚀 AI-RPG-Alpha Desktop Launcher")
    print("=" * 50)

    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("🔧 Installing dependencies...")

        if not install_dependencies():
            print("❌ Could not install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing)}")
            return 1

    # Setup database
    if not setup_database():
        print("❌ Database setup failed!")
        return 1

    # Check local LLM
    llm_available = check_local_llm()

    # Launch application
    print("\n🎮 Starting AI-RPG-Alpha Desktop...")
    print("=" * 50)

    try:
        from desktop_app import main as app_main
        return app_main()

    except ImportError as e:
        print(f"❌ Failed to import desktop application: {e}")
        print("Please ensure all dependencies are installed correctly.")
        return 1
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

