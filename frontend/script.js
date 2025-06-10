/**
 * AI-RPG-Alpha Frontend JavaScript
 * 
 * Handles all frontend game logic, API communication, and user interactions.
 * Manages game state, UI updates, and audio playback.
 */

class AIRPGGame {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8000';
        this.playerId = null;
        this.gameState = {
            player: null,
            currentNarrative: '',
            availableChoices: [],
            turnNumber: 0,
            gameStarted: false,
            inputMode: 'choices', // 'choices' or 'custom'
            activeQuests: [],
            completedQuests: [],
            selectedScenario: null,
            scenarioData: null,
            combatResources: {
                stamina: 100,
                maxStamina: 100,
                actionPoints: 2,
                maxActionPoints: 3,
                tacticalAdvantage: 0
            },
            sanityState: null // Only for cosmic horror scenario
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
        
        // Check for scenario selection
        this.checkScenarioSelection();
        
        // Show initial UI state
        this.updateUI();
    }
    
    /**
     * Check if a scenario was selected and initialize it
     */
    checkScenarioSelection() {
        const selectedScenario = localStorage.getItem('selectedScenario');
        if (selectedScenario && !this.gameState.selectedScenario) {
            this.gameState.selectedScenario = selectedScenario;
            this.initializeScenario(selectedScenario);
            
            // Show scenario info in UI immediately
            this.updateUI();
            
            // Store in session for this game session
            sessionStorage.setItem('currentScenario', selectedScenario);
            localStorage.removeItem('selectedScenario'); // Clear after use
        } else if (!selectedScenario && !sessionStorage.getItem('currentScenario')) {
            // If no scenario selected and not in a game session, redirect to selection
            if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
                console.log('No scenario selected, redirecting to scenario selection');
                window.location.href = 'scenario-selection.html';
            }
        } else if (sessionStorage.getItem('currentScenario') && !this.gameState.selectedScenario) {
            // Restore scenario from session
            const currentScenario = sessionStorage.getItem('currentScenario');
            this.gameState.selectedScenario = currentScenario;
            this.initializeScenario(currentScenario);
        }
    }
    
    /**
     * Initialize scenario-specific settings
     */
    initializeScenario(scenario) {
        const scenarioConfigs = {
            'northern_realms': {
                name: 'The Northern Realms',
                genre: 'Epic Fantasy',
                startingLocation: 'Ironhold Village',
                specialStats: ['magic_affinity', 'honor'],
                welcomeMessage: 'The ancient kingdoms of the north call to you...'
            },
            'whispering_town': {
                name: 'The Whispering Town',
                genre: 'Cosmic Horror',
                startingLocation: 'Arkham Outskirts',
                specialStats: ['sanity', 'cosmic_knowledge'],
                welcomeMessage: 'Reality grows thin as you approach the forgotten town...',
                sanitySystem: true
            },
            'neo_tokyo': {
                name: 'Neo-Tokyo 2087',
                genre: 'Cyberpunk Dystopia',
                startingLocation: 'Shibuya Undercity',
                specialStats: ['cyber_compatibility', 'corp_standing'],
                welcomeMessage: 'Neon lights flicker through the acid rain...'
            }
        };
        
        this.gameState.scenarioData = scenarioConfigs[scenario];
        
        // Initialize sanity system for cosmic horror
        if (this.gameState.scenarioData.sanitySystem) {
            this.gameState.sanityState = {
                currentSanity: 100,
                realityAnchor: 100,
                cosmicKnowledge: 0
            };
        }
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

        // Check if scenario was selected, if not redirect to scenario selection
        if (!this.gameState.selectedScenario) {
            this.showStatus('Please select a scenario first', 'error');
            setTimeout(() => {
                window.location.href = 'scenario-selection.html';
            }, 1500);
            return;
        }

        this.showLoading(true);

        try {
            // Generate unique player ID
            this.playerId = `player_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            // Initialize game state based on scenario
            const startingLocation = this.gameState.scenarioData ? 
                this.gameState.scenarioData.startingLocation : 'starting_village';
            
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
                current_location: startingLocation,
                turn_number: 0
            };

            // Make first turn request to start the game
            const response = await this.makeTurnRequest('Begin my adventure', playerName);
            
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
                this.showStatus(`${this.gameState.scenarioData.name} adventure begins!`, 'success');
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
    async makeTurnRequest(choice, playerName = null) {
        let requestData = null;
        try {
            requestData = {
                player_id: this.playerId,
                choice: choice,
                scenario: this.gameState.selectedScenario || 'northern_realms'
            };
            
            // Include player name and full player data for first turn
            if (playerName) {
                requestData.player_name = playerName;
                requestData.player_data = this.gameState.player;
            } else if (this.gameState.player) {
                requestData.player_name = this.gameState.player.name;
                requestData.player_data = this.gameState.player;
            }
            
            // Include scenario-specific data
            if (this.gameState.combatResources) {
                requestData.combat_resources = this.gameState.combatResources;
            }
            
            if (this.gameState.sanityState) {
                requestData.sanity_state = this.gameState.sanityState;
            }
            
            console.log('Sending request data:', requestData);
            
            const response = await fetch(`${this.apiBaseUrl}/turn`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('Turn request failed:', error);
            console.error('Request data was:', requestData);
            console.error('Error details:', error.message);
            this.showStatus(`Failed to process your choice: ${error.message}`, 'error');
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
                
                // Handle quest updates
                this.handleQuestUpdates(response);
                
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
        
        // Update scenario info if available
        if (this.gameState.scenarioData) {
            const scenarioInfo = document.getElementById('scenarioInfo');
            document.getElementById('scenarioName').textContent = this.gameState.scenarioData.name;
            document.getElementById('scenarioGenre').textContent = this.gameState.scenarioData.genre;
            scenarioInfo.style.display = 'block';

            // Show sanity for cosmic horror scenario
            if (this.gameState.scenarioData.sanitySystem && this.gameState.sanityState) {
                document.getElementById('sanitySection').style.display = 'block';
                this.updateSanityBar();
            }
        }
        
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
        
        // Update combat resources (BG3-style)
        this.updateCombatResources();
        
        // Update quests and inventory
        this.updateQuests();
        this.updateInventory();
    }

    /**
     * Update combat resources display (BG3-style)
     */
    updateCombatResources() {
        const resources = this.gameState.combatResources;
        
        // Update stamina bar
        const staminaPercentage = (resources.stamina / 100) * 100;
        document.getElementById('staminaBar').style.width = `${staminaPercentage}%`;
        document.getElementById('staminaText').textContent = `${resources.stamina}/100`;
        
        // Update action points
        const actionPointsContainer = document.getElementById('actionPoints');
        const actionPointElements = actionPointsContainer.querySelectorAll('.action-point');
        
        actionPointElements.forEach((element, index) => {
            if (index < resources.actionPoints) {
                element.classList.add('active');
            } else {
                element.classList.remove('active');
            }
        });
    }

    /**
     * Update sanity bar for cosmic horror scenario
     */
    updateSanityBar() {
        if (!this.gameState.sanityState) return;
        
        const sanityPercentage = (this.gameState.sanityState.currentSanity / 100) * 100;
        document.getElementById('sanityBar').style.width = `${sanityPercentage}%`;
        document.getElementById('sanityText').textContent = `${this.gameState.sanityState.currentSanity}/100`;
        
        // Change sanity bar color based on sanity level
        const sanityBar = document.getElementById('sanityBar');
        if (this.gameState.sanityState.currentSanity < 30) {
            sanityBar.style.background = 'linear-gradient(90deg, #d32f2f, #f44336)';
        } else if (this.gameState.sanityState.currentSanity < 60) {
            sanityBar.style.background = 'linear-gradient(90deg, #ff9800, #ffb74d)';
        } else {
            sanityBar.style.background = 'linear-gradient(90deg, #6a1b9a, #9c27b0)';
        }
    }

    /**
     * Handle quest updates from server response
     */
    handleQuestUpdates(response) {
        // Only add quests much later in the game, and more naturally
        if (this.gameState.turnNumber === 7) {
            this.gameState.activeQuests.push({
                title: "A Traveler's Purpose",
                description: "Understand why you're on this journey",
                progress: "Emerging"
            });
        }
        
        if (this.gameState.turnNumber === 12) {
            this.gameState.activeQuests.push({
                title: "Local Connections",
                description: "Learn about the people and places around you",
                progress: "Active"
            });
        }
        
        // Complete quest much later
        if (this.gameState.turnNumber === 18) {
            this.gameState.activeQuests = this.gameState.activeQuests.filter(q => q.title !== "A Traveler's Purpose");
            this.gameState.completedQuests.push("A Traveler's Purpose");
        }
    }

    /**
     * Update quest display
     */
    updateQuests() {
        const questList = document.getElementById('questList');
        const activeQuests = this.gameState.activeQuests;
        
        if (!activeQuests || activeQuests.length === 0) {
            questList.innerHTML = '<div class="quest-empty">No active quests</div>';
            return;
        }
        
        questList.innerHTML = activeQuests.map(quest => 
            `<div class="quest-item">
                <div class="quest-title">${quest.title}</div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">${quest.progress || 'Active'}</div>
            </div>`
        ).join('');
    }

    /**
     * Update inventory display
     */
    updateInventory() {
        const inventoryList = document.getElementById('inventoryList');
        const inventory = this.gameState.player?.inventory || [];
        
        if (inventory.length === 0) {
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
        // Skip music for now - files don't exist yet
        console.log(`Music change requested: ${riskLevel}`);
        return;
        
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

