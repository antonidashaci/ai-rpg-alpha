# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for AI-RPG-Alpha Desktop Application
==========================================================

This creates a standalone executable for the desktop RPG application.
"""

import os
import sys

# Application metadata
APP_NAME = "AI-RPG-Alpha"
APP_VERSION = "2.0.0"
MAIN_SCRIPT = "desktop_app.py"

# Determine platform-specific settings
if sys.platform.startswith('win'):
    ICON_FILE = None  # Windows doesn't need .ico for now
    CONSOLE = True  # Keep console for debugging
elif sys.platform.startswith('darwin'):  # macOS
    ICON_FILE = None
    CONSOLE = False
else:  # Linux
    ICON_FILE = None
    CONSOLE = False

# Hidden imports for PyQt6 and other dependencies
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'backend.dao.game_database',
    'backend.engine.game_orchestrator',
    'backend.engine.magic_system',
    'backend.engine.npc_dialogue',
    'backend.engine.political_system',
    'backend.ai.local_llm_client',
    'sqlite3',
    'requests',
    'chromadb',
    'sentence_transformers'
]

# Data files to include
datas = [
    # Include any asset files, databases, etc.
    # ('assets/', 'assets/'),
    # ('data/', 'data/'),
]

# Excluded modules (to reduce size)
excludes = [
    'tkinter',
    'test',
    'unittest',
    'pydoc',
    'pdb',
    'profile',
    'cProfile'
]

block_cipher = None

a = Analysis(
    [MAIN_SCRIPT],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=CONSOLE,
    icon=ICON_FILE,
    version='version_info.txt' if os.path.exists('version_info.txt') else None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME
)

