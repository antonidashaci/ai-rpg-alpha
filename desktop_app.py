#!/usr/bin/env python3
"""
AI-RPG-Alpha Desktop Application
================================

Standalone desktop RPG application with:
- PyQt6 native GUI
- Complete game engine integration
- Local LLM support
- Save/load functionality
- Steam-ready architecture

This replaces the web-based interface with a native desktop experience.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# PyQt6 imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem,
    QProgressBar, QFrame, QSplitter, QTabWidget, QStatusBar,
    QMessageBox, QInputDialog, QFileDialog, QDialog, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QCheckBox, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon, QAction

# Game engine imports
from backend.dao.game_database import GameDatabase
from backend.engine.game_orchestrator import GameOrchestrator
from backend.engine.magic_system import MagicEngine, MageStats
from backend.engine.npc_dialogue import DialogueEngine
from backend.engine.political_system import PoliticalEngine
from backend.ai.local_llm_client import LocalLLMManager


class GameThread(QThread):
    """Background thread for game operations"""
    game_update = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, orchestrator, action, *args, **kwargs):
        super().__init__()
        self.orchestrator = orchestrator
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            if self.action == "start_game":
                result = self.orchestrator.start_new_game(*self.args, **self.kwargs)
            elif self.action == "process_turn":
                result = self.orchestrator.process_turn(*self.args, **self.kwargs)
            elif self.action == "cast_spell":
                result = self.orchestrator.magic_engine.cast_spell(*self.args, **self.kwargs)
            elif self.action == "npc_dialogue":
                result = self.orchestrator.dialogue_engine.process_conversation(*self.args, **self.kwargs)
            elif self.action == "form_alliance":
                result = self.orchestrator.political_engine.form_alliance(*self.args, **self.kwargs)
            else:
                result = {"error": "Unknown action"}

            self.game_update.emit(result)

        except Exception as e:
            self.error_signal.emit(str(e))


class AIRPGDesktopApp(QMainWindow):
    """
    Main desktop application for AI-RPG-Alpha

    Features:
    - Native PyQt6 GUI
    - Tabbed interface for different game sections
    - Real-time game state updates
    - Save/load functionality
    - Local LLM integration
    """

    def __init__(self):
        super().__init__()

        # Initialize game systems
        self.db_path = "game_data.db"
        self.db = GameDatabase(self.db_path)
        self.game_orchestrator = GameOrchestrator(self.db_path)
        self.llm_manager = LocalLLMManager()

        # Game state
        self.current_player_id = None
        self.game_state = {}
        self.in_combat = False
        self.current_quest = None

        # Setup UI
        self.setup_window()
        self.setup_menu()
        self.setup_central_widget()
        self.setup_status_bar()

        # Setup game thread for background operations
        self.game_thread = None

        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_game)
        self.auto_save_timer.start(300000)  # Auto-save every 5 minutes

        # Check LLM status
        self.check_llm_status()

    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle("AI-RPG-Alpha - Epic Fantasy RPG")
        self.setMinimumSize(1200, 800)

        # Set window icon (placeholder)
        # self.setWindowIcon(QIcon("assets/icon.png"))

        # Center window
        self.center_window()

    def center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_game_action = QAction("&New Game", self)
        new_game_action.triggered.connect(self.new_game)
        file_menu.addAction(new_game_action)

        load_game_action = QAction("&Load Game", self)
        load_game_action.triggered.connect(self.load_game_dialog)
        file_menu.addAction(load_game_action)

        save_game_action = QAction("&Save Game", self)
        save_game_action.triggered.connect(self.save_game_dialog)
        file_menu.addAction(save_game_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Game menu
        game_menu = menubar.addMenu("&Game")

        character_action = QAction("&Character Sheet", self)
        character_action.triggered.connect(self.show_character_sheet)
        game_menu.addAction(character_action)

        magic_action = QAction("&Magic", self)
        magic_action.triggered.connect(self.show_magic_interface)
        game_menu.addAction(magic_action)

        quests_action = QAction("&Quests", self)
        quests_action.triggered.connect(self.show_quests)
        game_menu.addAction(quests_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        llm_status_action = QAction("&LLM Status", self)
        llm_status_action.triggered.connect(self.show_llm_status)
        tools_menu.addAction(llm_status_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_central_widget(self):
        """Setup main central widget with tabs"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Main game tab
        self.game_tab = self.create_game_tab()
        self.tab_widget.addTab(self.game_tab, "🎮 Game")

        # Character tab
        self.character_tab = self.create_character_tab()
        self.tab_widget.addTab(self.character_tab, "👤 Character")

        # Magic tab
        self.magic_tab = self.create_magic_tab()
        self.tab_widget.addTab(self.magic_tab, "🪄 Magic")

        # NPCs tab
        self.npcs_tab = self.create_npcs_tab()
        self.tab_widget.addTab(self.npcs_tab, "👥 NPCs")

        # Kingdoms tab
        self.kingdoms_tab = self.create_kingdoms_tab()
        self.tab_widget.addTab(self.kingdoms_tab, "🏰 Kingdoms")

        layout.addWidget(self.tab_widget)

    def create_game_tab(self):
        """Create main game interface tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Top section - Player info and quest progress
        top_section = QHBoxLayout()

        # Player info panel
        player_panel = self.create_player_panel()
        top_section.addWidget(player_panel, 1)

        # Quest progress panel
        quest_panel = self.create_quest_panel()
        top_section.addWidget(quest_panel, 2)

        layout.addLayout(top_section, 1)

        # Middle section - Narrative display
        narrative_section = QFrame()
        narrative_section.setFrameStyle(QFrame.Shape.Box)
        narrative_section.setLineWidth(2)
        narrative_layout = QVBoxLayout(narrative_section)

        narrative_label = QLabel("Narrative")
        narrative_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        narrative_layout.addWidget(narrative_label)

        self.narrative_display = QTextEdit()
        self.narrative_display.setReadOnly(True)
        self.narrative_display.setMinimumHeight(200)
        narrative_layout.addWidget(self.narrative_display)

        layout.addWidget(narrative_section, 3)

        # Bottom section - Choices and actions
        bottom_section = QHBoxLayout()

        # Choices panel
        choices_panel = QFrame()
        choices_panel.setFrameStyle(QFrame.Shape.Box)
        choices_layout = QVBoxLayout(choices_panel)

        choices_label = QLabel("Choose your action:")
        choices_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        choices_layout.addWidget(choices_label)

        self.choices_list = QListWidget()
        self.choices_list.itemDoubleClicked.connect(self.on_choice_selected)
        choices_layout.addWidget(self.choices_list)

        bottom_section.addWidget(choices_panel, 2)

        # Action buttons
        actions_panel = QFrame()
        actions_layout = QVBoxLayout(actions_panel)

        self.cast_spell_btn = QPushButton("🪄 Cast Spell")
        self.cast_spell_btn.clicked.connect(self.show_spell_dialog)
        actions_layout.addWidget(self.cast_spell_btn)

        self.talk_npc_btn = QPushButton("👥 Talk to NPC")
        self.talk_npc_btn.clicked.connect(self.show_npc_dialog)
        actions_layout.addWidget(self.talk_npc_btn)

        self.view_kingdoms_btn = QPushButton("🏰 View Kingdoms")
        self.view_kingdoms_btn.clicked.connect(self.show_kingdoms_dialog)
        actions_layout.addWidget(self.view_kingdoms_btn)

        actions_layout.addStretch()
        bottom_section.addWidget(actions_panel, 1)

        layout.addLayout(bottom_section, 1)

        return tab

    def create_player_panel(self):
        """Create player information panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        layout = QVBoxLayout(panel)

        title = QLabel("Player Status")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Player name
        self.player_name_label = QLabel("Name: Not set")
        layout.addWidget(self.player_name_label)

        # Health
        health_layout = QHBoxLayout()
        health_layout.addWidget(QLabel("Health:"))
        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 20)
        self.health_bar.setValue(20)
        health_layout.addWidget(self.health_bar)
        layout.addLayout(health_layout)

        # Mana
        mana_layout = QHBoxLayout()
        mana_layout.addWidget(QLabel("Mana:"))
        self.mana_bar = QProgressBar()
        self.mana_bar.setRange(0, 10)
        self.mana_bar.setValue(10)
        mana_layout.addWidget(self.mana_bar)
        layout.addLayout(mana_layout)

        # Level and XP
        self.level_label = QLabel("Level: 1")
        layout.addWidget(self.level_label)

        layout.addStretch()
        return panel

    def create_quest_panel(self):
        """Create quest progress panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        layout = QVBoxLayout(panel)

        title = QLabel("Quest Progress")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Current quest
        self.current_quest_label = QLabel("Current Quest: The Dragon's Prophecy")
        layout.addWidget(self.current_quest_label)

        # Quest progress bar
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("Progress:"))
        self.quest_progress_bar = QProgressBar()
        self.quest_progress_bar.setRange(0, 40)
        self.quest_progress_bar.setValue(1)
        progress_layout.addWidget(self.quest_progress_bar)
        layout.addLayout(progress_layout)

        # Current act
        self.current_act_label = QLabel("Act: Setup")
        layout.addWidget(self.current_act_label)

        # Turn counter
        self.turn_label = QLabel("Turn: 1/40")
        layout.addWidget(self.turn_label)

        layout.addStretch()
        return panel

    def create_character_tab(self):
        """Create character sheet tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Character stats
        stats_group = QGroupBox("Character Statistics")
        stats_layout = QFormLayout()

        self.char_name_edit = QLineEdit()
        stats_layout.addRow("Name:", self.char_name_edit)

        self.char_level_spin = QSpinBox()
        self.char_level_spin.setRange(1, 20)
        stats_layout.addRow("Level:", self.char_level_spin)

        self.char_health_spin = QSpinBox()
        self.char_health_spin.setRange(1, 100)
        stats_layout.addRow("Health:", self.char_health_spin)

        self.char_mana_spin = QSpinBox()
        self.char_mana_spin.setRange(1, 50)
        stats_layout.addRow("Mana:", self.char_mana_spin)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Abilities
        abilities_group = QGroupBox("Abilities")
        abilities_layout = QFormLayout()

        self.str_spin = QSpinBox()
        self.str_spin.setRange(8, 20)
        abilities_layout.addRow("Strength:", self.str_spin)

        self.dex_spin = QSpinBox()
        self.dex_spin.setRange(8, 20)
        abilities_layout.addRow("Dexterity:", self.dex_spin)

        self.int_spin = QSpinBox()
        self.int_spin.setRange(8, 20)
        abilities_layout.addRow("Intelligence:", self.int_spin)

        self.wis_spin = QSpinBox()
        self.wis_spin.setRange(8, 20)
        abilities_layout.addRow("Wisdom:", self.wis_spin)

        self.cha_spin = QSpinBox()
        self.cha_spin.setRange(8, 20)
        abilities_layout.addRow("Charisma:", self.cha_spin)

        abilities_group.setLayout(abilities_layout)
        layout.addWidget(abilities_group)

        layout.addStretch()
        return tab

    def create_magic_tab(self):
        """Create magic interface tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Magic schools
        schools_group = QGroupBox("Magic Schools")
        schools_layout = QVBoxLayout()

        self.magic_schools_list = QListWidget()
        schools_layout.addWidget(self.magic_schools_list)

        schools_group.setLayout(schools_layout)
        layout.addWidget(schools_group)

        # Known spells
        spells_group = QGroupBox("Known Spells")
        spells_layout = QVBoxLayout()

        self.known_spells_list = QListWidget()
        self.known_spells_list.itemDoubleClicked.connect(self.cast_spell_from_list)
        spells_layout.addWidget(self.known_spells_list)

        spells_group.setLayout(spells_layout)
        layout.addWidget(spells_group)

        # Spell casting
        cast_group = QGroupBox("Cast Spell")
        cast_layout = QHBoxLayout()

        self.spell_combo = QComboBox()
        cast_layout.addWidget(self.spell_combo)

        cast_btn = QPushButton("Cast")
        cast_btn.clicked.connect(self.cast_selected_spell)
        cast_layout.addWidget(cast_btn)

        cast_group.setLayout(cast_layout)
        layout.addWidget(cast_group)

        layout.addStretch()
        return tab

    def create_npcs_tab(self):
        """Create NPCs interface tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # NPCs list
        npcs_group = QGroupBox("Available NPCs")
        npcs_layout = QVBoxLayout()

        self.npcs_list = QListWidget()
        self.npcs_list.itemDoubleClicked.connect(self.start_npc_conversation)
        npcs_layout.addWidget(self.npcs_list)

        npcs_group.setLayout(npcs_layout)
        layout.addWidget(npcs_group)

        # Conversation area
        convo_group = QGroupBox("Conversation")
        convo_layout = QVBoxLayout()

        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        convo_layout.addWidget(self.conversation_display)

        # Conversation choices
        self.convo_choices_list = QListWidget()
        self.convo_choices_list.itemDoubleClicked.connect(self.continue_conversation)
        convo_layout.addWidget(self.convo_choices_list)

        convo_group.setLayout(convo_layout)
        layout.addWidget(convo_group)

        layout.addStretch()
        return tab

    def create_kingdoms_tab(self):
        """Create kingdoms interface tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Kingdoms list
        kingdoms_group = QGroupBox("Kingdoms")
        kingdoms_layout = QVBoxLayout()

        self.kingdoms_list = QListWidget()
        self.kingdoms_list.itemDoubleClicked.connect(self.show_kingdom_details)
        kingdoms_layout.addWidget(self.kingdoms_list)

        kingdoms_group.setLayout(kingdoms_layout)
        layout.addWidget(kingdoms_group)

        # Kingdom details
        details_group = QGroupBox("Kingdom Details")
        details_layout = QVBoxLayout()

        self.kingdom_details_display = QTextEdit()
        self.kingdom_details_display.setReadOnly(True)
        details_layout.addWidget(self.kingdom_details_display)

        # Diplomatic actions
        actions_layout = QHBoxLayout()

        self.ally_btn = QPushButton("Form Alliance")
        self.ally_btn.clicked.connect(self.form_alliance)
        actions_layout.addWidget(self.ally_btn)

        self.trade_btn = QPushButton("Negotiate Trade")
        self.trade_btn.clicked.connect(self.negotiate_trade)
        actions_layout.addWidget(self.trade_btn)

        details_layout.addLayout(actions_layout)

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        layout.addStretch()
        return tab

    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = self.statusBar()

        # LLM status
        self.llm_status_label = QLabel("LLM: Checking...")
        self.status_bar.addWidget(self.llm_status_label)

        self.status_bar.addPermanentWidget(QLabel("AI-RPG-Alpha v2.0"))

    # ============================================================================
    # GAME LOGIC METHODS
    # ============================================================================

    def new_game(self):
        """Start a new game"""
        dialog = NewGameDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, abilities = dialog.get_character_data()

            self.game_thread = GameThread(
                self.game_orchestrator,
                "start_game",
                name,
                abilities
            )
            self.game_thread.game_update.connect(self.on_game_update)
            self.game_thread.error_signal.connect(self.on_game_error)
            self.game_thread.start()

    def load_game_dialog(self):
        """Show load game dialog"""
        slot_number, ok = QInputDialog.getInt(
            self, "Load Game", "Enter save slot number (1-5):", 1, 1, 5
        )

        if ok:
            self.load_game(slot_number)

    def load_game(self, slot_number: int):
        """Load game from slot"""
        save_data = self.game_orchestrator.load_game(None, slot_number)  # player_id None for now

        if save_data:
            self.game_state = save_data
            self.current_player_id = save_data.get('player_state', {}).get('player_id')
            self.update_ui()
            QMessageBox.information(self, "Success", f"Game loaded from slot {slot_number}")
        else:
            QMessageBox.warning(self, "Error", f"No save found in slot {slot_number}")

    def save_game_dialog(self):
        """Show save game dialog"""
        slot_number, ok = QInputDialog.getInt(
            self, "Save Game", "Enter save slot number (1-5):", 1, 1, 5
        )

        if ok:
            self.save_game(slot_number)

    def save_game(self, slot_number: int):
        """Save current game"""
        if not self.current_player_id:
            QMessageBox.warning(self, "Error", "No active game to save")
            return

        success = self.game_orchestrator.save_game(
            self.current_player_id,
            slot_number,
            f"Save {slot_number}"
        )

        if success:
            QMessageBox.information(self, "Success", f"Game saved to slot {slot_number}")
        else:
            QMessageBox.warning(self, "Error", "Failed to save game")

    def auto_save_game(self):
        """Auto-save game periodically"""
        if self.current_player_id:
            self.save_game(0)  # Auto-save to slot 0

    def on_choice_selected(self, item: QListWidgetItem):
        """Handle choice selection"""
        choice_text = item.text()

        if self.current_player_id:
            self.game_thread = GameThread(
                self.game_orchestrator,
                "process_turn",
                self.current_player_id,
                choice_text,
                0  # choice_index
            )
            self.game_thread.game_update.connect(self.on_game_update)
            self.game_thread.error_signal.connect(self.on_game_error)
            self.game_thread.start()

    def on_game_update(self, result: Dict[str, Any]):
        """Handle game update from background thread"""
        if result.get("success"):
            self.game_state.update(result)
            self.update_ui()

            # Update narrative display
            if "narrative" in result:
                self.narrative_display.setPlainText(result["narrative"])

            # Update choices
            if "choices" in result:
                self.choices_list.clear()
                for choice in result["choices"]:
                    self.choices_list.addItem(choice)

            # Handle quest completion
            if result.get("quest_completed"):
                QMessageBox.information(
                    self, "Quest Complete!",
                    f"Congratulations! You've completed: {result.get('ending', 'Unknown ending')}"
                )

        self.game_thread = None

    def on_game_error(self, error: str):
        """Handle game error"""
        QMessageBox.warning(self, "Game Error", f"An error occurred: {error}")
        self.game_thread = None

    def update_ui(self):
        """Update all UI elements with current game state"""
        if not self.game_state:
            return

        # Update player info
        player_data = self.game_state.get("player_stats", {})
        if player_data:
            self.player_name_label.setText(f"Name: {player_data.get('name', 'Unknown')}")
            self.health_bar.setValue(player_data.get('health', 20))
            self.mana_bar.setValue(player_data.get('mana', 10))
            self.level_label.setText(f"Level: {player_data.get('level', 1)}")

        # Update quest info
        quest_data = self.game_state.get("quest_state", {})
        if quest_data:
            self.quest_progress_bar.setValue(quest_data.get('turn_number', 1))
            self.turn_label.setText(f"Turn: {quest_data.get('turn_number', 1)}/40")
            self.current_act_label.setText(f"Act: {quest_data.get('current_act', 'Setup').title()}")

        # Update character tab
        if player_data:
            self.char_name_edit.setText(player_data.get('name', ''))
            self.char_level_spin.setValue(player_data.get('level', 1))
            self.char_health_spin.setValue(player_data.get('health', 20))
            self.char_mana_spin.setValue(player_data.get('mana', 10))

            # Abilities
            self.str_spin.setValue(player_data.get('strength', 10))
            self.dex_spin.setValue(player_data.get('dexterity', 10))
            self.int_spin.setValue(player_data.get('intelligence', 10))
            self.wis_spin.setValue(player_data.get('wisdom', 10))
            self.cha_spin.setValue(player_data.get('charisma', 10))

    def check_llm_status(self):
        """Check and display LLM status"""
        if self.llm_manager.is_available():
            status = "✅ Local LLM Ready"
            model = self.llm_manager.current_model
            self.llm_status_label.setText(f"LLM: {model}")
        else:
            self.llm_status_label.setText("LLM: ❌ Not Available")

    # ============================================================================
    # DIALOG METHODS
    # ============================================================================

    def show_character_sheet(self):
        """Show character sheet dialog"""
        dialog = CharacterSheetDialog(self.game_state, self)
        dialog.exec()

    def show_magic_interface(self):
        """Show magic interface"""
        self.tab_widget.setCurrentWidget(self.magic_tab)

    def show_quests(self):
        """Show quests dialog"""
        dialog = QuestsDialog(self.game_state, self)
        dialog.exec()

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_llm_status(self):
        """Show LLM status dialog"""
        dialog = LLMStatusDialog(self.llm_manager, self)
        dialog.exec()

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About AI-RPG-Alpha",
            "AI-RPG-Alpha v2.0\n\n"
            "An epic fantasy RPG with AI-powered storytelling.\n\n"
            "Features:\n"
            "- 40-turn quest progression\n"
            "- 6 magic schools\n"
            "- Dynamic NPC interactions\n"
            "- Kingdom politics\n"
            "- Local AI integration"
        )

    # Placeholder methods for dialog implementations
    def show_spell_dialog(self): pass
    def show_npc_dialog(self): pass
    def show_kingdoms_dialog(self): pass
    def cast_spell_from_list(self, item): pass
    def cast_selected_spell(self): pass
    def start_npc_conversation(self, item): pass
    def continue_conversation(self, item): pass
    def show_kingdom_details(self, item): pass
    def form_alliance(self): pass
    def negotiate_trade(self): pass


# ============================================================================
# DIALOG CLASSES
# ============================================================================

class NewGameDialog(QDialog):
    """New game creation dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Character")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Character name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Character Name:"))
        self.name_edit = QLineEdit("Adventurer")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Abilities
        abilities_group = QGroupBox("Ability Scores")
        abilities_layout = QFormLayout()

        self.abilities = {}
        for ability in ["Strength", "Dexterity", "Intelligence", "Wisdom", "Charisma"]:
            spin = QSpinBox()
            spin.setRange(8, 18)
            spin.setValue(10)
            self.abilities[ability.lower()] = spin
            abilities_layout.addRow(f"{ability}:", spin)

        abilities_group.setLayout(abilities_layout)
        layout.addWidget(abilities_group)

        # Buttons
        buttons_layout = QHBoxLayout()

        ok_btn = QPushButton("Start Game")
        ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

    def get_character_data(self):
        """Get character creation data"""
        name = self.name_edit.text()

        abilities = {}
        for ability, spin in self.abilities.items():
            abilities[ability] = spin.value()

        return name, abilities


class CharacterSheetDialog(QDialog):
    """Character sheet dialog"""

    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Character Sheet")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Character sheet implementation coming soon..."))
        layout.addStretch()


class QuestsDialog(QDialog):
    """Quests dialog"""

    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Active Quests")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Quest interface implementation coming soon..."))
        layout.addStretch()


class SettingsDialog(QDialog):
    """Settings dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings interface implementation coming soon..."))
        layout.addStretch()


class LLMStatusDialog(QDialog):
    """LLM status dialog"""

    def __init__(self, llm_manager, parent=None):
        super().__init__(parent)
        self.llm_manager = llm_manager
        self.setWindowTitle("Local LLM Status")
        self.setModal(True)

        layout = QVBoxLayout(self)

        status = llm_manager.get_status()
        layout.addWidget(QLabel(f"Available: {status['available']}"))
        layout.addWidget(QLabel(f"Model: {status.get('model', 'None')}"))

        if status.get('available_models'):
            models_label = QLabel("Available Models:")
            layout.addWidget(models_label)

            for model in status['available_models'][:5]:
                layout.addWidget(QLabel(f"  • {model}"))

        layout.addStretch()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("AI-RPG-Alpha")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("AI-RPG-Alpha Team")

    # Create and show main window
    window = AIRPGDesktopApp()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

