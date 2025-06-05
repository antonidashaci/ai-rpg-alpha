/**
 * AI-RPG-Alpha Frontend JavaScript
 * 
 * Handles all frontend game logic, API communication, and user interactions.
 * Manages game state, UI updates, and audio playback.
 */

class AIRPGGame {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.playerId = null;
        this.gameState = {
            player: null,
            currentNarrative: '',
            availableChoices: [],
            turnNumber: 0,
            gameStarted: false,
            inputMode: 'choices' // 'choices' or 'custom'
        };
        this.audioContext = {
            backgroundMusic: null,
            currentTrack: 'calm',
            isPlaying: false,
            volume: 0.3
        };
        
        this.init();
    }

    /**
     * Initialize the game application
     */
    init() {
        this.setupEventListeners();
        this.checkAPIStatus();
        this.setupAudio();
        this.loadGameState();
        
        // Show initial UI state
        this.updateUI();
    }

    /**
     * Set up all event listeners for UI interactions
     */
    setupEventListeners() {
        // Start game button
        document.getElementById('startGameBtn').addEventListener('click', () => {
            this.startGame();
        });

        // Enter key for player name input
        document.getElementById('playerNameInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.startGame();
            }
        });

        // Custom choice input
        document.getElementById('submitCustomChoice').addEventListener('click', () => {
            this.submitCustomChoice();
        });

        document.getElementById('customChoiceInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitCustomChoice();
            }
        });

        // Toggle input mode
        document.getElementById('toggleInputMode').addEventListener('click', () => {
            this.toggleInputMode();
        });

        // Show choices button
        document.getElementById('showChoicesBtn').addEventListener('click', () => {
            this.showChoices();
        });

        // Game control buttons
        document.getElementById('saveGameBtn').addEventListener('click', () => {
            this.saveGame();
        });

        document.getElementById('loadGameBtn').addEventListener('click', () => {
            this.loadGame();
        });

        document.getElementById('newGameBtn').addEventListener('click', () => {
            this.newGame();
        });

        // Music controls
        document.getElementById('toggleMusicBtn').addEventListener('click', () => {
            this.toggleMusic();
        });

        document.getElementById('volumeSlider').addEventListener('input', (e) => {
            this.setVolume(e.target.value / 100);
        });
    }

    /**
     * Check API status and update UI
     */
    async checkAPIStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            document.getElementById('apiStatus').textContent = 
                `API: ${data.status === 'healthy' ? 'Connected' : 'Issues'}`;
            document.getElementById('apiStatus').style.color = 
                data.status === 'healthy' ? 'var(--success)' : 'var(--danger)';
                
        } catch (error) {
            console.error('API check failed:', error);
            document.getElementById('apiStatus').textContent = 'API: Offline';
            document.getElementById('apiStatus').style.color = 'var(--danger)';
        }
    }

    /**
     * Start a new game
     */
    async startGame() {
        const playerName = document.getElementById('playerNameInput').value.trim();
        
        if (!playerName) {
            this.showStatus('Please enter your character name', 'error');
            return;
        }

        if (playerName.length < 2) {
            this.showStatus('Character name must be at least 2 characters', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Generate unique player ID
            this.playerId = `player_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            // Initialize game state
            this.gameState.player = {
                id: this.playerId,
                name: playerName,
                stats: {
                    level: 1,
                    health: 100,
                    mana: 50,
                    strength: 10,
                    intelligence: 10,
                    charisma: 10
                },
                inventory: [],
                current_location: 'starting_village',
                turn_number: 0
            };

            // Make first turn request to start the game
            const response = await this.makeTurnRequest('Begin my adventure');
            
            if (response) {
                this.gameState.gameStarted = true;
                this.gameState.currentNarrative = response.narrative;
                this.gameState.availableChoices = response.choices;
                this.gameState.turnNumber = 1;
                
                // Update music based on metadata
                if (response.metadata && response.metadata.risk_level) {
                    this.changeMusic(response.metadata.risk_level);
                }
                
                this.updateUI();
                this.showGameControls();
                this.showStatus('Adventure begins!', 'success');
            }
            
        } catch (error) {
            console.error('Failed to start game:', error);
            this.showStatus('Failed to start game. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Make a turn request to the backend
     */
    async makeTurnRequest(choice) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/turn`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player_id: this.playerId,
                    choice: choice
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('Turn request failed:', error);
            this.showStatus('Failed to process your choice. Please try again.', 'error');
            return null;
        }
    }

    /**
     * Handle choice selection
     */
    async selectChoice(choiceIndex) {
        if (choiceIndex < 0 || choiceIndex >= this.gameState.availableChoices.length) {
            this.showStatus('Invalid choice selected', 'error');
            return;
        }

        const selectedChoice = this.gameState.availableChoices[choiceIndex];
        await this.processPlayerChoice(selectedChoice);
    }

    /**
     * Submit custom choice
     */
    async submitCustomChoice() {
        const customChoice = document.getElementById('customChoiceInput').value.trim();
        
        if (!customChoice) {
            this.showStatus('Please enter your action', 'error');
            return;
        }

        if (customChoice.length < 3) {
            this.showStatus('Please provide a more detailed action', 'error');
            return;
        }

        document.getElementById('customChoiceInput').value = '';
        await this.processPlayerChoice(customChoice);
    }

    /**
     * Process player choice and get response
     */
    async processPlayerChoice(choice) {
        this.showLoading(true);

        try {
            const response = await this.makeTurnRequest(choice);
            
            if (response) {
                this.gameState.currentNarrative = response.narrative;
                this.gameState.availableChoices = response.choices;
                this.gameState.turnNumber++;
                
                // Update music based on metadata
                if (response.metadata && response.metadata.risk_level) {
                    this.changeMusic(response.metadata.risk_level);
                }
                
                // Update player stats if provided in metadata
                if (response.metadata && response.metadata.player_stats) {
                    this.gameState.player.stats = response.metadata.player_stats;
                }
                
                this.updateUI();
                this.saveGameState();
                
                // Scroll narrative into view
                document.getElementById('narrativeText').scrollTop = 0;
            }
            
        } catch (error) {
            console.error('Failed to process choice:', error);
            this.showStatus('Failed to process your choice. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Toggle between choice and custom input modes
     */
    toggleInputMode() {
        this.gameState.inputMode = this.gameState.inputMode === 'choices' ? 'custom' : 'choices';
        this.updateInputUI();
        
        const modeText = this.gameState.inputMode === 'choices' ? 'Custom Input' : 'Show Choices';
        document.getElementById('inputModeText').textContent = modeText;
    }

    /**
     * Show suggested choices
     */
    showChoices() {
        this.gameState.inputMode = 'choices';
        this.updateInputUI();
    }

    /**
     * Update the entire UI
     */
    updateUI() {
        this.updatePlayerInfo();
        this.updateNarrative();
        this.updateInputUI();
        this.updateTurnCounter();
    }

    /**
     * Update player information panel
     */
    updatePlayerInfo() {
        if (!this.gameState.player) return;

        const player = this.gameState.player;
        
        document.getElementById('playerName').textContent = player.name;
        document.getElementById('playerLevel').textContent = player.stats.level;
        
        // Update health bar
        const healthPercent = (player.stats.health / 100) * 100;
        document.getElementById('healthBar').style.width = `${healthPercent}%`;
        document.getElementById('healthText').textContent = `${player.stats.health}/100`;
        
        // Update mana bar
        const manaPercent = (player.stats.mana / 50) * 100;
        document.getElementById('manaBar').style.width = `${manaPercent}%`;
        document.getElementById('manaText').textContent = `${player.stats.mana}/50`;
        
        // Update attributes
        document.getElementById('strengthValue').textContent = player.stats.strength;
        document.getElementById('intelligenceValue').textContent = player.stats.intelligence;
        document.getElementById('charismaValue').textContent = player.stats.charisma;
        
        // Update location
        document.getElementById('currentLocation').textContent = 
            this.formatLocationName(player.current_location);
        
        // Update inventory
        this.updateInventory();
    }

    /**
     * Update inventory display
     */
    updateInventory() {
        const inventoryList = document.getElementById('inventoryList');
        const inventory = this.gameState.player.inventory;
        
        if (!inventory || inventory.length === 0) {
            inventoryList.innerHTML = '<div class="inventory-empty">No items</div>';
            return;
        }
        
        inventoryList.innerHTML = inventory.map(item => 
            `<div class="inventory-item">${item}</div>`
        ).join('');
    }

    /**
     * Update narrative display
     */
    updateNarrative() {
        const narrativeElement = document.getElementById('narrativeText');
        
        if (this.gameState.currentNarrative) {
            // Format narrative text with proper paragraphs
            const formattedNarrative = this.gameState.currentNarrative
                .split('\n')
                .filter(line => line.trim())
                .map(line => `<p>${line.trim()}</p>`)
                .join('');
                
            narrativeElement.innerHTML = formattedNarrative;
        }
    }

    /**
     * Update input UI based on current mode
     */
    updateInputUI() {
        const choiceContainer = document.getElementById('choiceContainer');
        const customInputContainer = document.getElementById('customInputContainer');
        const playerSetup = document.getElementById('playerSetup');
        
        if (!this.gameState.gameStarted) {
            playerSetup.style.display = 'block';
            choiceContainer.style.display = 'none';
            customInputContainer.style.display = 'none';
            return;
        }
        
        playerSetup.style.display = 'none';
        
        if (this.gameState.inputMode === 'choices') {
            choiceContainer.style.display = 'block';
            customInputContainer.style.display = 'none';
            this.updateChoices();
        } else {
            choiceContainer.style.display = 'none';
            customInputContainer.style.display = 'block';
        }
    }

    /**
     * Update choices display
     */
    updateChoices() {
        const choicesList = document.getElementById('choicesList');
        
        if (!this.gameState.availableChoices || this.gameState.availableChoices.length === 0) {
            choicesList.innerHTML = '<div class="no-choices">No choices available</div>';
            return;
        }
        
        choicesList.innerHTML = this.gameState.availableChoices.map((choice, index) => 
            `<button class="choice-btn" onclick="game.selectChoice(${index})">
                ${choice}
            </button>`
        ).join('');
    }

    /**
     * Update turn counter
     */
    updateTurnCounter() {
        document.getElementById('turnCounter').textContent = this.gameState.turnNumber;
    }

    /**
     * Show game controls
     */
    showGameControls() {
        const controls = ['toggleInputMode', 'saveGameBtn', 'loadGameBtn', 'newGameBtn'];
        controls.forEach(id => {
            document.getElementById(id).style.display = 'inline-block';
        });
    }

    /**
     * Setup audio system
     */
    setupAudio() {
        this.audioContext.backgroundMusic = document.getElementById('backgroundMusic');
        this.audioContext.backgroundMusic.volume = this.audioContext.volume;
        
        // Set initial volume slider
        document.getElementById('volumeSlider').value = this.audioContext.volume * 100;
    }

    /**
     * Change background music based on risk level
     */
    changeMusic(riskLevel) {
        if (!this.audioContext.backgroundMusic) return;
        
        const musicMap = {
            'calm': 'assets/music/calm.mp3',
            'mystery': 'assets/music/mystery.mp3',
            'combat': 'assets/music/combat.mp3'
        };
        
        const newTrack = musicMap[riskLevel] || musicMap['calm'];
        
        if (this.audioContext.currentTrack !== riskLevel) {
            this.audioContext.currentTrack = riskLevel;
            this.audioContext.backgroundMusic.src = newTrack;
            
            if (this.audioContext.isPlaying) {
                this.audioContext.backgroundMusic.play().catch(e => {
                    console.log('Audio autoplay prevented:', e);
                });
            }
        }
    }

    /**
     * Toggle music playback
     */
    toggleMusic() {
        if (!this.audioContext.backgroundMusic) return;
        
        if (this.audioContext.isPlaying) {
            this.audioContext.backgroundMusic.pause();
            this.audioContext.isPlaying = false;
            document.getElementById('toggleMusicBtn').innerHTML = '<span class="music-icon">🔇</span>';
        } else {
            this.audioContext.backgroundMusic.play().catch(e => {
                console.log('Audio play failed:', e);
                this.showStatus('Audio playback not available', 'info');
            });
            this.audioContext.isPlaying = true;
            document.getElementById('toggleMusicBtn').innerHTML = '<span class="music-icon">🎵</span>';
        }
    }

    /**
     * Set audio volume
     */
    setVolume(volume) {
        this.audioContext.volume = Math.max(0, Math.min(1, volume));
        if (this.audioContext.backgroundMusic) {
            this.audioContext.backgroundMusic.volume = this.audioContext.volume;
        }
    }

    /**
     * Save game state to localStorage
     */
    saveGame() {
        try {
            const saveData = {
                playerId: this.playerId,
                gameState: this.gameState,
                timestamp: new Date().toISOString()
            };
            
            localStorage.setItem('aiRpgSave', JSON.stringify(saveData));
            this.showStatus('Game saved successfully!', 'success');
            
        } catch (error) {
            console.error('Failed to save game:', error);
            this.showStatus('Failed to save game', 'error');
        }
    }

    /**
     * Load game state from localStorage
     */
    loadGame() {
        try {
            const saveData = localStorage.getItem('aiRpgSave');
            
            if (!saveData) {
                this.showStatus('No saved game found', 'info');
                return;
            }
            
            const parsed = JSON.parse(saveData);
            this.playerId = parsed.playerId;
            this.gameState = parsed.gameState;
            
            this.updateUI();
            this.showGameControls();
            this.showStatus('Game loaded successfully!', 'success');
            
        } catch (error) {
            console.error('Failed to load game:', error);
            this.showStatus('Failed to load game', 'error');
        }
    }

    /**
     * Save game state automatically
     */
    saveGameState() {
        try {
            const saveData = {
                playerId: this.playerId,
                gameState: this.gameState,
                timestamp: new Date().toISOString()
            };
            
            localStorage.setItem('aiRpgAutoSave', JSON.stringify(saveData));
            
        } catch (error) {
            console.error('Auto-save failed:', error);
        }
    }

    /**
     * Load game state automatically
     */
    loadGameState() {
        try {
            const saveData = localStorage.getItem('aiRpgAutoSave');
            
            if (saveData) {
                const parsed = JSON.parse(saveData);
                
                // Only auto-load if the save is recent (within 24 hours)
                const saveTime = new Date(parsed.timestamp);
                const now = new Date();
                const hoursDiff = (now - saveTime) / (1000 * 60 * 60);
                
                if (hoursDiff < 24 && parsed.gameState.gameStarted) {
                    this.playerId = parsed.playerId;
                    this.gameState = parsed.gameState;
                    this.updateUI();
                    this.showGameControls();
                    this.showStatus('Previous session restored', 'info');
                }
            }
            
        } catch (error) {
            console.error('Auto-load failed:', error);
        }
    }

    /**
     * Start a new game (reset everything)
     */
    newGame() {
        if (confirm('Are you sure you want to start a new game? Current progress will be lost.')) {
            this.playerId = null;
            this.gameState = {
                player: null,
                currentNarrative: '',
                availableChoices: [],
                turnNumber: 0,
                gameStarted: false,
                inputMode: 'choices'
            };
            
            // Clear inputs
            document.getElementById('playerNameInput').value = '';
            document.getElementById('customChoiceInput').value = '';
            
            // Hide game controls
            const controls = ['toggleInputMode', 'saveGameBtn', 'loadGameBtn', 'newGameBtn'];
            controls.forEach(id => {
                document.getElementById(id).style.display = 'none';
            });
            
            // Reset UI
            this.updateUI();
            
            // Clear auto-save
            localStorage.removeItem('aiRpgAutoSave');
            
            this.showStatus('New game started', 'info');
        }
    }

    /**
     * Show loading overlay
     */
    showLoading(show) {
        document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
    }

    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        const statusContainer = document.getElementById('statusContainer');
        
        const statusElement = document.createElement('div');
        statusElement.className = `status-message ${type}`;
        statusElement.textContent = message;
        
        statusContainer.appendChild(statusElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (statusElement.parentNode) {
                statusElement.parentNode.removeChild(statusElement);
            }
        }, 5000);
        
        // Remove on click
        statusElement.addEventListener('click', () => {
            if (statusElement.parentNode) {
                statusElement.parentNode.removeChild(statusElement);
            }
        });
    }

    /**
     * Format location name for display
     */
    formatLocationName(location) {
        return location
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
}

// Initialize the game when the page loads
let game;

document.addEventListener('DOMContentLoaded', () => {
    game = new AIRPGGame();
});

// Handle page visibility changes to pause/resume music
document.addEventListener('visibilitychange', () => {
    if (game && game.audioContext.backgroundMusic) {
        if (document.hidden && game.audioContext.isPlaying) {
            game.audioContext.backgroundMusic.pause();
        } else if (!document.hidden && game.audioContext.isPlaying) {
            game.audioContext.backgroundMusic.play().catch(e => {
                console.log('Audio resume failed:', e);
            });
        }
    }
});

// Handle beforeunload to save game state
window.addEventListener('beforeunload', () => {
    if (game && game.gameState.gameStarted) {
        game.saveGameState();
    }
});

