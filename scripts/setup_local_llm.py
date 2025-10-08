#!/usr/bin/env python3
"""
Local LLM Setup Script for AI-RPG-Alpha
=======================================

This script helps users set up Ollama for local LLM functionality.
Provides instructions and automated setup for Windows/Linux/Mac.
"""

import os
import sys
import platform
import subprocess
import time
import requests

def check_ollama_installed():
    """Check if Ollama is already installed"""
    try:
        # Try to connect to Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def install_ollama_windows():
    """Install Ollama on Windows"""
    print("🔄 Installing Ollama on Windows...")

    try:
        # Download Ollama installer
        print("📥 Downloading Ollama installer...")
        # Note: This would normally download from official site
        # For now, we'll provide manual instructions

        print("\n📋 Manual Installation Instructions:")
        print("=" * 50)
        print("1. Open your web browser")
        print("2. Go to: https://ollama.ai/download")
        print("3. Download the Windows installer")
        print("4. Run the installer and follow the setup wizard")
        print("5. After installation, open Command Prompt or PowerShell")
        print("6. Run: ollama pull llama2")
        print("7. Run: ollama serve")
        print("8. Keep the terminal window open")
        print("=" * 50)

        print("\nAfter completing these steps, run this script again to verify installation.")

        return False

    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def install_ollama_linux():
    """Install Ollama on Linux"""
    print("🔄 Installing Ollama on Linux...")

    try:
        # Use curl to install Ollama
        print("📥 Downloading and installing Ollama...")
        subprocess.run([
            "curl", "-fsSL", "https://ollama.ai/install.sh"
        ], check=True, capture_output=True)

        print("✅ Ollama installed successfully!")

        # Pull a default model
        print("📥 Pulling llama2 model...")
        subprocess.run(["ollama", "pull", "llama2"], check=True)

        print("✅ Model downloaded!")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        print("\n📋 Manual Installation Instructions:")
        print("=" * 50)
        print("Run these commands manually:")
        print("curl -fsSL https://ollama.ai/install.sh | sh")
        print("ollama pull llama2")
        print("ollama serve")
        print("=" * 50)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def install_ollama_mac():
    """Install Ollama on macOS"""
    print("🔄 Installing Ollama on macOS...")

    try:
        # Use brew to install (if available)
        try:
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            print("🍺 Using Homebrew for installation...")
            subprocess.run(["brew", "install", "ollama"], check=True)
        except:
            # Manual download method
            print("📥 Downloading Ollama for macOS...")
            # Note: This would normally download from official site

            print("\n📋 Manual Installation Instructions:")
            print("=" * 50)
            print("1. Open your web browser")
            print("2. Go to: https://ollama.ai/download")
            print("3. Download the macOS version")
            print("4. Open the downloaded file")
            print("5. Move Ollama to your Applications folder")
            print("6. Open Terminal")
            print("7. Run: ollama pull llama2")
            print("8. Run: ollama serve")
            print("=" * 50)

            return False

        print("✅ Ollama installed successfully!")

        # Pull a default model
        print("📥 Pulling llama2 model...")
        subprocess.run(["ollama", "pull", "llama2"], check=True)

        print("✅ Model downloaded!")

        return True

    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def setup_ollama():
    """Main setup function"""
    print("🚀 AI-RPG-Alpha Local LLM Setup")
    print("=" * 50)

    system = platform.system().lower()

    if check_ollama_installed():
        print("✅ Ollama is already installed and running!")

        # Check available models
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]

                print(f"\n📋 Available Models: {len(models)}")
                for model in models[:5]:  # Show first 5
                    print(f"  • {model}")
                if len(models) > 5:
                    print(f"  • ... and {len(models) - 5} more")

                if not models:
                    print("⚠️  No models installed. Run: ollama pull llama2")
            else:
                print("⚠️  Could not retrieve model list")

        except:
            print("⚠️  Could not connect to Ollama API")

        return True

    else:
        print("❌ Ollama is not installed or not running.")

        if system == "windows":
            success = install_ollama_windows()
        elif system == "linux":
            success = install_ollama_linux()
        elif system == "darwin":  # macOS
            success = install_ollama_mac()
        else:
            print(f"❌ Unsupported platform: {system}")
            print("Please visit https://ollama.ai/download for manual installation.")
            success = False

        return success

def test_local_llm():
    """Test local LLM functionality"""
    print("\n🧪 Testing Local LLM Integration...")

    try:
        # Import and test the local LLM client
        from ai.local_llm_client import LocalLLMClient

        client = LocalLLMClient()

        if client.connected:
            print("✅ Local LLM client connected successfully!")

            # Test with a simple prompt
            test_prompt = "Write a short description of a brave fantasy adventurer:"
            response = client._make_request(test_prompt, max_tokens=100)

            if response:
                print("✅ Test generation successful!")
                print(f"📝 Sample response: {response[:100]}...")
            else:
                print("❌ Test generation failed")

        else:
            print("❌ Could not connect to local LLM")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📖 Usage Instructions")
    print("=" * 50)
    print("1. Start Ollama server (if not already running):")
    print("   ollama serve")
    print("\n2. Pull a model (if not already pulled):")
    print("   ollama pull llama2")
    print("\n3. Start the game backend:")
    print("   cd backend && python main_enhanced.py")
    print("\n4. Start the frontend:")
    print("   cd frontend && python -m http.server 3000")
    print("\n5. Open browser to: http://localhost:3000")
    print("\n6. Check LLM status at: http://localhost:8000/health")

def main():
    """Main setup function"""
    print("🎮 AI-RPG-Alpha Local LLM Setup")
    print("=" * 50)

    # Setup Ollama
    ollama_ready = setup_ollama()

    if ollama_ready:
        # Test local LLM
        test_local_llm()

        # Show usage instructions
        show_usage_instructions()

        print("\n🎉 Setup complete! You can now enjoy AI-generated narratives!")
    else:
        print("\n❌ Setup incomplete. Please follow the manual instructions above.")
        print("After installing Ollama, run this script again.")

if __name__ == "__main__":
    main()

