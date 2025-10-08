"""
Audio System for The Northern Realms
===================================

Audio system featuring:
- Background music for different scenarios and moods
- Sound effects for actions and events
- Audio settings and volume control
- Cross-platform audio support
"""

import os
import pygame
import time
from typing import Dict, Optional, List
from enum import Enum
import logging


class AudioCategory(Enum):
    """Audio categories"""
    BACKGROUND_MUSIC = "background_music"
    SOUND_EFFECTS = "sound_effects"
    AMBIENT = "ambient"
    UI = "ui"


class MusicTrack(Enum):
    """Available background music tracks"""
    MAIN_THEME = "main_theme"
    COMBAT_THEME = "combat_theme"
    MYSTERY_THEME = "mystery_theme"
    VICTORY_THEME = "victory_theme"
    DEFEAT_THEME = "defeat_theme"
    EXPLORATION_THEME = "exploration_theme"
    TENSION_THEME = "tension_theme"
    PEACEFUL_THEME = "peaceful_theme"


class SoundEffect(Enum):
    """Available sound effects"""
    # Combat sounds
    SWORD_SWING = "sword_swing"
    ARROW_SHOT = "arrow_shot"
    MAGIC_CAST = "magic_cast"
    ENEMY_HIT = "enemy_hit"
    PLAYER_HIT = "player_hit"
    SPELL_IMPACT = "spell_impact"

    # UI sounds
    BUTTON_CLICK = "button_click"
    MENU_OPEN = "menu_open"
    ACHIEVEMENT_UNLOCK = "achievement_unlock"
    LEVEL_UP = "level_up"

    # Environment sounds
    DOOR_OPEN = "door_open"
    TREASURE_CHEST = "treasure_chest"
    FOOTSTEPS = "footsteps"
    AMBIENT_WIND = "ambient_wind"


class AudioSystem:
    """
    Audio system for The Northern Realms

    Manages:
    - Background music playback
    - Sound effects
    - Audio settings and volume control
    - Cross-platform compatibility
    """

    def __init__(self, assets_path: str = "assets/audio"):
        """
        Initialize audio system

        Args:
            assets_path: Path to audio assets directory
        """
        self.assets_path = assets_path
        self.initialized = False
        self.current_track = None
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Audio state
        self.music_enabled = True
        self.sfx_enabled = True

        # Track fade settings
        self.fade_duration = 2000  # milliseconds

        self._initialize_audio()

    def _initialize_audio(self):
        """Initialize pygame mixer for audio"""
        try:
            pygame.mixer.init()

            # Set initial volumes
            pygame.mixer.music.set_volume(self.music_volume)

            self.initialized = True
            logging.info("Audio system initialized successfully")

        except Exception as e:
            logging.error(f"Failed to initialize audio system: {e}")
            self.initialized = False

    def load_audio_assets(self) -> Dict[str, str]:
        """Load and organize audio assets"""
        assets = {}

        if not os.path.exists(self.assets_path):
            logging.warning(f"Audio assets path not found: {self.assets_path}")
            return assets

        # Load music tracks
        music_path = os.path.join(self.assets_path, "music")
        if os.path.exists(music_path):
            for track in MusicTrack:
                track_file = os.path.join(music_path, f"{track.value}.mp3")
                if os.path.exists(track_file):
                    assets[f"music_{track.value}"] = track_file
                else:
                    # Try .ogg format
                    track_file_ogg = os.path.join(music_path, f"{track.value}.ogg")
                    if os.path.exists(track_file_ogg):
                        assets[f"music_{track.value}"] = track_file_ogg

        # Load sound effects
        sfx_path = os.path.join(self.assets_path, "sfx")
        if os.path.exists(sfx_path):
            for effect in SoundEffect:
                effect_file = os.path.join(sfx_path, f"{effect.value}.wav")
                if os.path.exists(effect_file):
                    assets[f"sfx_{effect.value}"] = effect_file
                else:
                    # Try .ogg format
                    effect_file_ogg = os.path.join(sfx_path, f"{effect.value}.ogg")
                    if os.path.exists(effect_file_ogg):
                        assets[f"sfx_{effect.value}"] = effect_file_ogg

        logging.info(f"Loaded {len(assets)} audio assets")
        return assets

    def play_music(self, track: MusicTrack, fade_in: bool = True):
        """Play background music"""
        if not self.initialized or not self.music_enabled:
            return

        track_file = f"assets/audio/music/{track.value}.mp3"

        # Check if file exists
        if not os.path.exists(track_file):
            track_file_ogg = f"assets/audio/music/{track.value}.ogg"
            if not os.path.exists(track_file_ogg):
                logging.warning(f"Music track not found: {track.value}")
                return

            track_file = track_file_ogg

        try:
            if fade_in and self.current_track:
                # Fade out current track
                pygame.mixer.music.fadeout(self.fade_duration)

                # Wait for fade to complete, then start new track
                pygame.time.wait(self.fade_duration + 100)
                pygame.mixer.music.load(track_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            else:
                pygame.mixer.music.load(track_file)
                pygame.mixer.music.play(-1)

            pygame.mixer.music.set_volume(self.music_volume)
            self.current_track = track
            logging.debug(f"Now playing: {track.value}")

        except Exception as e:
            logging.error(f"Error playing music {track.value}: {e}")

    def stop_music(self, fade_out: bool = True):
        """Stop background music"""
        if not self.initialized:
            return

        try:
            if fade_out:
                pygame.mixer.music.fadeout(self.fade_duration)
            else:
                pygame.mixer.music.stop()

            self.current_track = None

        except Exception as e:
            logging.error(f"Error stopping music: {e}")

    def play_sound_effect(self, effect: SoundEffect):
        """Play sound effect"""
        if not self.initialized or not self.sfx_enabled:
            return

        effect_file = f"assets/audio/sfx/{effect.value}.wav"

        # Check if file exists
        if not os.path.exists(effect_file):
            effect_file_ogg = f"assets/audio/sfx/{effect.value}.ogg"
            if not os.path.exists(effect_file_ogg):
                logging.debug(f"Sound effect not found: {effect.value}")
                return

            effect_file = effect_file_ogg

        try:
            sound = pygame.mixer.Sound(effect_file)
            sound.set_volume(self.sfx_volume)
            sound.play()

        except Exception as e:
            logging.error(f"Error playing sound effect {effect.value}: {e}")

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))

        if self.initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_master_volume(self, volume: float):
        """Set master volume for all audio"""
        self.music_volume = max(0.0, min(1.0, volume))
        self.sfx_volume = max(0.0, min(1.0, volume))

        if self.initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def get_audio_settings(self) -> Dict[str, any]:
        """Get current audio settings"""
        return {
            "music_enabled": self.music_enabled,
            "sfx_enabled": self.sfx_enabled,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "initialized": self.initialized,
            "current_track": self.current_track.value if self.current_track else None
        }

    def save_audio_settings(self, settings: Dict[str, any]):
        """Save audio settings to file"""
        try:
            with open("audio_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving audio settings: {e}")

    def load_audio_settings(self) -> Dict[str, any]:
        """Load audio settings from file"""
        default_settings = {
            "music_enabled": True,
            "sfx_enabled": True,
            "music_volume": 0.5,
            "sfx_volume": 0.7
        }

        try:
            if os.path.exists("audio_settings.json"):
                with open("audio_settings.json", "r") as f:
                    settings = json.load(f)
                    # Merge with defaults for missing keys
                    return {**default_settings, **settings}
        except Exception as e:
            logging.error(f"Error loading audio settings: {e}")

        return default_settings


class AudioManager:
    """
    High-level audio manager for game events

    Provides convenient methods for playing audio based on game events:
    - Combat music for battles
    - Ambient sounds for exploration
    - UI sounds for interface actions
    - Achievement sounds for unlocks
    """

    def __init__(self, audio_system: AudioSystem):
        self.audio_system = audio_system
        self.current_context = "menu"

    def set_context(self, context: str):
        """Set current game context for appropriate audio"""
        self.current_context = context

        # Play appropriate music based on context
        if context == "combat":
            self.audio_system.play_music(MusicTrack.COMBAT_THEME)
        elif context == "exploration":
            self.audio_system.play_music(MusicTrack.EXPLORATION_THEME)
        elif context == "mystery":
            self.audio_system.play_music(MusicTrack.MYSTERY_THEME)
        elif context == "peaceful":
            self.audio_system.play_music(MusicTrack.PEACEFUL_THEME)
        elif context == "tension":
            self.audio_system.play_music(MusicTrack.TENSION_THEME)
        elif context == "menu":
            self.audio_system.play_music(MusicTrack.MAIN_THEME)

    def on_game_start(self):
        """Audio for game start"""
        self.set_context("exploration")
        self.audio_system.play_sound_effect(SoundEffect.LEVEL_UP)

    def on_combat_start(self):
        """Audio for combat start"""
        self.set_context("combat")
        self.audio_system.play_sound_effect(SoundEffect.ENEMY_HIT)

    def on_combat_end(self, victory: bool):
        """Audio for combat end"""
        if victory:
            self.audio_system.play_music(MusicTrack.VICTORY_THEME)
            self.audio_system.play_sound_effect(SoundEffect.ACHIEVEMENT_UNLOCK)
        else:
            self.audio_system.play_music(MusicTrack.DEFEAT_THEME)

        # Return to exploration music after a delay
        def return_to_exploration():
            time.sleep(3)
            self.set_context("exploration")

        import threading
        threading.Thread(target=return_to_exploration, daemon=True).start()

    def on_spell_cast(self):
        """Audio for spell casting"""
        self.audio_system.play_sound_effect(SoundEffect.MAGIC_CAST)

    def on_achievement_unlock(self):
        """Audio for achievement unlock"""
        self.audio_system.play_sound_effect(SoundEffect.ACHIEVEMENT_UNLOCK)

    def on_npc_interaction(self):
        """Audio for NPC interaction"""
        self.audio_system.play_sound_effect(SoundEffect.DOOR_OPEN)

    def on_treasure_found(self):
        """Audio for treasure discovery"""
        self.audio_system.play_sound_effect(SoundEffect.TREASURE_CHEST)

    def on_button_click(self):
        """Audio for UI button clicks"""
        self.audio_system.play_sound_effect(SoundEffect.BUTTON_CLICK)

    def on_level_up(self):
        """Audio for level up"""
        self.audio_system.play_sound_effect(SoundEffect.LEVEL_UP)

    def on_save_game(self):
        """Audio for save game"""
        self.audio_system.play_sound_effect(SoundEffect.BUTTON_CLICK)

    def on_quest_complete(self):
        """Audio for quest completion"""
        self.audio_system.play_sound_effect(SoundEffect.ACHIEVEMENT_UNLOCK)

    def on_enemy_defeated(self):
        """Audio for enemy defeat"""
        self.audio_system.play_sound_effect(SoundEffect.ENEMY_HIT)

    def on_player_damage(self):
        """Audio for player taking damage"""
        self.audio_system.play_sound_effect(SoundEffect.PLAYER_HIT)

    def play_ambient_sound(self, sound: SoundEffect):
        """Play ambient sound effect"""
        if sound in [SoundEffect.AMBIENT_WIND, SoundEffect.FOOTSTEPS]:
            self.audio_system.play_sound_effect(sound)

