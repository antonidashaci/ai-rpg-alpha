/**
 * AI-RPG-Alpha: Audio System Component
 * 
 * Handles background music, sound effects, and ambient audio.
 * Part of Phase 4: Advanced UI & User Experience as defined in PRD.
 */

class AudioSystem {
    constructor() {
        this.initialized = false;
        this.audioContext = null;
        this.masterGain = null;
        
        // Audio channels
        this.channels = {
            music: { gain: null, source: null, buffer: null },
            sfx: { gain: null, sources: [] },
            ambient: { gain: null, source: null, buffer: null },
            voice: { gain: null, sources: [] }
        };
        
        // Audio assets
        this.assets = {
            music: new Map(),
            sfx: new Map(),
            ambient: new Map()
        };
        
        // Current state
        this.currentMusic = null;
        this.currentAmbient = null;
        this.musicFading = false;
        this.settings = {
            masterVolume: 0.7,
            musicVolume: 0.5,
            sfxVolume: 0.6,
            ambientVolume: 0.4,
            muteAll: false
        };
        
        this.loadSettings();
        this.init();
    }

    /**
     * Initialize the audio system
     */
    async init() {
        try {
            // Check for Web Audio API support
            if (!window.AudioContext && !window.webkitAudioContext) {
                console.warn('Web Audio API not supported');
                return;
            }
            
            // Initialize audio context on user interaction
            this.setupUserActivation();
            this.loadAudioAssets();
            this.bindSettingsEvents();
            
        } catch (error) {
            console.error('Failed to initialize audio system:', error);
        }
    }

    /**
     * Setup audio context after user interaction
     */
    setupUserActivation() {
        const activateAudio = async () => {
            if (!this.initialized) {
                await this.initializeAudioContext();
                document.removeEventListener('click', activateAudio);
                document.removeEventListener('keydown', activateAudio);
                document.removeEventListener('touchstart', activateAudio);
            }
        };

        document.addEventListener('click', activateAudio);
        document.addEventListener('keydown', activateAudio);
        document.addEventListener('touchstart', activateAudio);
    }

    /**
     * Initialize Web Audio API context
     */
    async initializeAudioContext() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioContext = new AudioContext();
            
            // Create master gain node
            this.masterGain = this.audioContext.createGain();
            this.masterGain.connect(this.audioContext.destination);
            
            // Create channel gain nodes
            Object.keys(this.channels).forEach(channel => {
                this.channels[channel].gain = this.audioContext.createGain();
                this.channels[channel].gain.connect(this.masterGain);
            });
            
            // Apply initial volume settings
            this.updateVolumes();
            
            this.initialized = true;
            console.log('Audio system initialized');
            
            // Emit initialization event
            window.dispatchEvent(new CustomEvent('audioInitialized'));
            
        } catch (error) {
            console.error('Failed to initialize audio context:', error);
        }
    }

    /**
     * Load settings from game settings or localStorage
     */
    loadSettings() {
        // Try to get from game settings first
        if (window.gameSettings) {
            const settings = window.gameSettings.getSettings();
            this.settings = {
                masterVolume: settings.masterVolume,
                musicVolume: settings.musicVolume,
                sfxVolume: settings.sfxVolume,
                ambientVolume: settings.ambientVolume,
                muteAll: settings.muteAll
            };
        } else {
            // Fallback to localStorage
            try {
                const saved = localStorage.getItem('aiRpgAudioSettings');
                if (saved) {
                    this.settings = { ...this.settings, ...JSON.parse(saved) };
                }
            } catch (error) {
                console.warn('Failed to load audio settings:', error);
            }
        }
    }

    /**
     * Listen for settings changes
     */
    bindSettingsEvents() {
        window.addEventListener('settingsChanged', (event) => {
            const settings = event.detail;
            this.settings = {
                masterVolume: settings.masterVolume,
                musicVolume: settings.musicVolume,
                sfxVolume: settings.sfxVolume,
                ambientVolume: settings.ambientVolume,
                muteAll: settings.muteAll
            };
            this.updateVolumes();
        });
    }

    /**
     * Load audio assets (placeholders for now)
     */
    loadAudioAssets() {
        // Create placeholder audio buffers for demo
        this.createPlaceholderSounds();
    }

    /**
     * Create placeholder sounds using Web Audio API
     */
    createPlaceholderSounds() {
        if (!this.audioContext) return;

        // Create simple tones for demo purposes
        const sampleRate = this.audioContext.sampleRate;
        
        // Click sound
        const clickBuffer = this.audioContext.createBuffer(1, sampleRate * 0.1, sampleRate);
        const clickData = clickBuffer.getChannelData(0);
        for (let i = 0; i < clickData.length; i++) {
            clickData[i] = Math.sin(2 * Math.PI * 800 * i / sampleRate) * Math.exp(-i / (sampleRate * 0.05));
        }
        this.assets.sfx.set('click', clickBuffer);
        
        // Success sound
        const successBuffer = this.audioContext.createBuffer(1, sampleRate * 0.3, sampleRate);
        const successData = successBuffer.getChannelData(0);
        for (let i = 0; i < successData.length; i++) {
            const t = i / sampleRate;
            successData[i] = Math.sin(2 * Math.PI * (440 + t * 200) * t) * Math.exp(-t * 3);
        }
        this.assets.sfx.set('success', successBuffer);
        
        // Error sound
        const errorBuffer = this.audioContext.createBuffer(1, sampleRate * 0.2, sampleRate);
        const errorData = errorBuffer.getChannelData(0);
        for (let i = 0; i < errorData.length; i++) {
            const t = i / sampleRate;
            errorData[i] = Math.sin(2 * Math.PI * (220 - t * 100) * t) * Math.exp(-t * 5);
        }
        this.assets.sfx.set('error', errorBuffer);
    }

    /**
     * Play sound effect
     */
    playSFX(soundName, volume = 1.0) {
        if (!this.initialized || this.settings.muteAll) return;

        const buffer = this.assets.sfx.get(soundName);
        if (!buffer) {
            console.warn(`SFX not available: ${soundName}`);
            return;
        }

        // Create and configure source
        const source = this.audioContext.createBufferSource();
        source.buffer = buffer;
        
        // Create gain node for this sound
        const gainNode = this.audioContext.createGain();
        gainNode.gain.value = volume * this.settings.sfxVolume * this.settings.masterVolume;
        
        // Connect audio graph
        source.connect(gainNode);
        gainNode.connect(this.channels.sfx.gain);
        
        // Start playback
        source.start(0);
        
        // Clean up when finished
        source.onended = () => {
            const index = this.channels.sfx.sources.indexOf(source);
            if (index > -1) {
                this.channels.sfx.sources.splice(index, 1);
            }
        };
        
        // Store reference
        this.channels.sfx.sources.push(source);
    }

    /**
     * Update volume levels from settings
     */
    updateVolumes() {
        if (!this.initialized) return;

        const masterVol = this.settings.muteAll ? 0 : this.settings.masterVolume;
        
        // Update master volume
        this.masterGain.gain.setValueAtTime(masterVol, this.audioContext.currentTime);
        
        // Update channel volumes
        if (this.channels.music.gain) {
            this.channels.music.gain.gain.setValueAtTime(
                this.settings.musicVolume, 
                this.audioContext.currentTime
            );
        }
        
        if (this.channels.sfx.gain) {
            this.channels.sfx.gain.gain.setValueAtTime(
                this.settings.sfxVolume, 
                this.audioContext.currentTime
            );
        }
        
        if (this.channels.ambient.gain) {
            this.channels.ambient.gain.gain.setValueAtTime(
                this.settings.ambientVolume, 
                this.audioContext.currentTime
            );
        }
    }

    /**
     * Set music based on game state
     */
    setMusicForGameState(state) {
        // For demo purposes, just log the state change
        console.log(`Music state changed to: ${state}`);
        
        // Play a demo tone for menu state
        if (state === 'menu' && this.initialized && !this.settings.muteAll) {
            this.playTone(220, 0.5, 'sine'); // A3 note
        }
    }

    /**
     * Play a simple tone (demo/placeholder)
     */
    playTone(frequency, duration, type = 'sine') {
        if (!this.initialized || this.settings.muteAll) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.channels.music.gain);
        
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.1, this.audioContext.currentTime + 0.1);
        gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    /**
     * Mute/unmute all audio
     */
    toggleMute() {
        this.settings.muteAll = !this.settings.muteAll;
        this.updateVolumes();
        return this.settings.muteAll;
    }

    /**
     * Get current audio state
     */
    getState() {
        return {
            initialized: this.initialized,
            currentMusic: this.currentMusic?.name || null,
            currentAmbient: this.currentAmbient?.name || null,
            settings: { ...this.settings }
        };
    }

    /**
     * Cleanup audio resources
     */
    cleanup() {
        if (this.currentMusic) {
            this.currentMusic.source.stop();
        }
        
        if (this.currentAmbient) {
            this.currentAmbient.source.stop();
        }
        
        this.channels.sfx.sources.forEach(source => {
            try {
                source.stop();
            } catch (error) {
                // Source may already be stopped
            }
        });
        
        if (this.audioContext) {
            this.audioContext.close();
        }
        
        this.initialized = false;
    }
}

// UI convenience functions
const AudioUI = {
    /**
     * Add audio controls to the UI
     */
    addAudioControls(container) {
        const controlsHTML = `
            <div class="audio-controls">
                <button id="musicToggle" class="audio-btn" title="Toggle Music">🎵</button>
                <button id="sfxToggle" class="audio-btn" title="Toggle Sound Effects">🔊</button>
                <button id="muteToggle" class="audio-btn" title="Mute All">🔇</button>
            </div>
        `;
        
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }
        
        if (container) {
            container.insertAdjacentHTML('beforeend', controlsHTML);
            this.bindAudioControlEvents();
        }
    },

    /**
     * Bind audio control events
     */
    bindAudioControlEvents() {
        const musicToggle = document.getElementById('musicToggle');
        const sfxToggle = document.getElementById('sfxToggle');
        const muteToggle = document.getElementById('muteToggle');

        if (musicToggle) {
            musicToggle.onclick = () => {
                window.audioSystem?.setMusicForGameState('menu');
                window.audioSystem?.playSFX('click');
            };
        }

        if (sfxToggle) {
            sfxToggle.onclick = () => {
                window.audioSystem?.playSFX('success');
            };
        }

        if (muteToggle) {
            muteToggle.onclick = () => {
                const isMuted = window.audioSystem?.toggleMute();
                muteToggle.textContent = isMuted ? '🔇' : '🔊';
                if (window.gameUI) {
                    window.gameUI.showNotification(
                        isMuted ? 'Audio muted' : 'Audio enabled', 
                        'info'
                    );
                }
            };
        }
    }
};

// Initialize audio system when DOM is ready
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        window.audioSystem = new AudioSystem();
        
        // Add basic audio controls if container exists
        const gameHeader = document.querySelector('.game-header');
        if (gameHeader) {
            AudioUI.addAudioControls(gameHeader);
        }
    });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AudioSystem, AudioUI };
} 