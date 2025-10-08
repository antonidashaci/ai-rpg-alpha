#!/usr/bin/env python3
"""
Desktop Application Builder for AI-RPG-Alpha
============================================

This script builds the desktop application into a standalone executable.
Supports Windows, macOS, and Linux builds.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_requirements():
    """Check if PyInstaller and other build requirements are met"""
    required_commands = ['pyinstaller']

    missing = []
    for cmd in required_commands:
        if shutil.which(cmd) is None:
            missing.append(cmd)

    return missing

def install_build_tools():
    """Install required build tools"""
    print("🔧 Installing build tools...")

    try:
        # Install PyInstaller
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 'pyinstaller'
        ])

        print("✅ Build tools installed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install build tools: {e}")
        return False

def build_executable():
    """Build the desktop executable"""
    print("🏗️ Building desktop executable...")

    system = platform.system().lower()

    try:
        # Build command
        if system == 'windows':
            cmd = ['pyinstaller', '--onefile', '--windowed', 'desktop_app.spec']
        else:
            cmd = ['pyinstaller', '--onefile', 'desktop_app.spec']

        print(f"🔨 Running: {' '.join(cmd)}")
        subprocess.check_call(cmd)

        print("✅ Executable built successfully!")

        # Show output location
        if system == 'windows':
            exe_name = "AI-RPG-Alpha.exe"
        else:
            exe_name = "AI-RPG-Alpha"

        dist_path = Path("dist") / exe_name
        if dist_path.exists():
            print(f"📦 Executable created at: {dist_path.absolute()}")
        else:
            print(f"⚠️ Executable not found at expected location: {dist_path}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during build: {e}")
        return False

def create_installer():
    """Create platform-specific installer (optional)"""
    print("📦 Creating installer...")

    system = platform.system().lower()

    try:
        if system == 'windows':
            print("💿 Windows installer creation not implemented yet")
            print("   Use the .exe file directly")
        elif system == 'darwin':  # macOS
            print("🍎 macOS .app bundle creation not implemented yet")
            print("   Use the executable directly")
        else:  # Linux
            print("🐧 Linux AppImage creation not implemented yet")
            print("   Use the executable directly")

        return True

    except Exception as e:
        print(f"❌ Installer creation failed: {e}")
        return False

def cleanup_build_files():
    """Clean up build artifacts"""
    print("🧹 Cleaning up build files...")

    cleanup_dirs = ['build', '__pycache__', '*.spec~']

    for item in cleanup_dirs:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"  Removed directory: {item}")
            else:
                os.remove(item)
                print(f"  Removed file: {item}")

def main():
    """Main build function"""
    print("🚀 AI-RPG-Alpha Desktop Build System")
    print("=" * 50)

    # Check requirements
    missing = check_requirements()
    if missing:
        print(f"❌ Missing build requirements: {', '.join(missing)}")
        print("🔧 Installing build tools...")

        if not install_build_tools():
            print("❌ Could not install build tools.")
            print("Please install manually: pip install pyinstaller")
            return 1

    # Build executable
    if not build_executable():
        print("❌ Build failed!")
        return 1

    # Optional: Create installer
    create_installer()

    # Cleanup
    cleanup_build_files()

    print("\n🎉 Build completed successfully!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Test the executable in the 'dist' folder")
    print("2. Distribute the standalone application")
    print("3. For Steam distribution, package with Steamworks SDK")

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

