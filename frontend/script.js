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
            sanityState: null, // Only for cosmic horror scenario
            // D&D System additions
            gameType: 'dnd_adventure',
            aiProvider: 'gemini',
            apiKey: null,
            character: {
                name: 'Ra\'el',
                level: 1,
                health: '20/20',
                xp: 0,
                gold: 50,
                abilities: {},
                inventory: [],
                wearing: [],
                wielding: [],
                armor_class: 10,
                quest: 'None'
            },
            lastRoll: null,
            timeOfDay: 'Morning',
            location: 'Ironhold Village'
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
        // Use event delegation for better performance
        document.addEventListener('click', (e) => {
            // Handle choice button clicks
            if (e.target.closest('.choice-btn')) {
                const button = e.target.closest('.choice-btn');
                const index = Array.from(button.parentNode.children).indexOf(button);
                this.selectChoice(index);
            }
            
            // Handle inventory item clicks
            if (e.target.closest('.inventory-item')) {
                const item = e.target.closest('.inventory-item');
                const itemName = item.querySelector('.item-name').textContent;
                this.useItem(itemName);
            }
        });

        // Start game button
        const startBtn = document.getElementById('startGameBtn');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startGame());
        }

        // Enter key for player name input
        const nameInput = document.getElementById('playerNameInput');
        if (nameInput) {
            nameInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.startGame();
                }
            });
        }

        // Custom choice input
        const customSubmit = document.getElementById('submitCustomChoice');
        if (customSubmit) {
            customSubmit.addEventListener('click', () => this.submitCustomChoice());
        }

        const customInput = document.getElementById('customChoiceInput');
        if (customInput) {
            customInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.submitCustomChoice();
                }
            });
        }

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

        // Menu items
        const menuItems = {
            'menuMain': () => window.location.href = 'scenario-selection.html',
            'menuCharCreate': () => showCharCreateModal(),
            'menuSettings': () => {
                if (typeof GameSettings !== 'undefined') {
                    GameSettings.show();
                }
            },
            'menuSaveLoad': () => showSaveLoadModal(),
            'menuHelp': () => this.showHelp(),
            'menuExit': () => this.exitGame()
        };

        Object.entries(menuItems).forEach(([id, handler]) => {
            const element = document.getElementById(id);
            if (element) {
                element.addEventListener('click', handler);
            }
        });
    }

    /**
     * Check API status and update UI
     */
    async checkAPIStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                signal: AbortSignal.timeout(5000) // 5 second timeout
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('API Status:', data);
            
            // Show API status in UI
            this.showStatus('Connected to game server', 'success');
            
            return data;
            
        } catch (error) {
            console.error('API check failed:', error);
            
            if (error.name === 'AbortError') {
                this.showStatus('Server connection timeout. Check your internet connection.', 'error');
            } else if (error.message.includes('Failed to fetch')) {
                this.showStatus('Cannot connect to game server. Is the backend running?', 'error');
            } else {
                this.showStatus(`Server error: ${error.message}`, 'error');
            }
            
            return null;
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
     * Make a turn request to the backend (D&D Enhanced)
     */
    async makeTurnRequest(choice, playerName = null) {
        try {
            const playerId = playerName || this.gameState.character.name || 'Player';
            
            const requestData = {
                player_id: playerId,
                choice: choice,
                game_state: {
                    turn_number: this.gameState.turnNumber,
                    character: this.gameState.character,
                    scenario: this.gameState.selectedScenario,
                    location: this.gameState.location,
                    time_of_day: this.gameState.timeOfDay
                }
            };

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

            const response = await fetch(`${this.apiBaseUrl}/turn`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('API request failed:', error);
            
            if (error.name === 'AbortError') {
                this.showStatus('Request timeout. The server is taking too long to respond.', 'error');
            } else if (error.message.includes('Failed to fetch')) {
                this.showStatus('Network error. Check your internet connection.', 'error');
            } else {
                this.showStatus(`Request failed: ${error.message}`, 'error');
            }
            
            // Fallback response if API fails
            return {
                narrative: `You chose to ${choice}. The story continues... (Offline mode)`,
                choices: ["Continue exploring", "Rest here", "Check your equipment", "Look around"],
                metadata: {
                    location: this.gameState.location,
                    risk_level: "calm",
                    turn_number: this.gameState.turnNumber + 1
                }
            };
        }
    }
    
    /**
     * Update D&D game state from server response
     */
    updateDnDGameState(response) {
        // Update narrative
        if (response.narrative) {
            this.gameState.currentNarrative = response.narrative;
        }
        
        // Update available choices
        if (response.choices) {
            this.gameState.availableChoices = response.choices;
        }
        
        // Update metadata
        if (response.metadata) {
            if (response.metadata.location) {
                this.gameState.location = response.metadata.location;
            }
            if (response.metadata.risk_level) {
                this.gameState.riskLevel = response.metadata.risk_level;
            }
            if (response.metadata.turn_number) {
                this.gameState.turnNumber = response.metadata.turn_number;
            }
        }
        
        // Update character stats if provided
        if (response.character_updates) {
            Object.assign(this.gameState.character, response.character_updates);
        }
    }

    /**
     * Handle choice selection
     */
    async selectChoice(choiceIndex) {
        if (!this.gameState.gameStarted) {
            await this.startGame();
            return;
        }

        const choices = document.querySelectorAll('.choice-btn');
        if (choiceIndex >= 0 && choiceIndex < choices.length) {
            const choice = choices[choiceIndex].querySelector('.cmd-label').textContent;
            await this.processPlayerChoice(choice);
        }
    }

    /**
     * Submit custom choice
     */
    async submitCustomChoice() {
        const customInput = document.getElementById('customChoiceInput');
        const choice = customInput.value.trim();
        
        if (choice) {
            customInput.value = '';
            await this.processPlayerChoice(choice);
        }
    }

    /**
     * Process player choice and get response
     */
    async processPlayerChoice(choice) {
        try {
            this.showLoading(true);
            this.showStatus('Processing your choice...', 'info');
            
            // Validate choice
            if (!choice || choice.trim().length === 0) {
                throw new Error('Please provide a valid choice');
            }
            
            // Update turn counter
            this.gameState.turnNumber++;
            
            // Make API request to backend
            const response = await this.makeTurnRequest(choice, this.gameState.character.name);
            
            // Update game state with response
            this.updateDnDGameState(response);
            
            // Update UI efficiently
            this.updateUI();
            
            // Update scenario commands for next turn
            if (typeof updateScenarioCommands === 'function') {
                updateScenarioCommands();
            }
            
            // Save game state
            this.saveGameState();
            
            this.showLoading(false);
            
        } catch (error) {
            console.error('Error processing choice:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
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
        // Batch DOM updates for better performance
        requestAnimationFrame(() => {
            this.updateNarrative();
            this.updateChoices();
            this.updatePlayerInfo();
            this.updateTurnCounter();
            this.updateCombatResources();
            this.updateSanityBar();
            this.updateQuests();
            this.updateInventory();
            this.updateAbilities();
            this.updateEquipment();
            this.updateCharacterSummary();
        });
    }

    /**
     * Update player information panel (D&D Enhanced)
     */
    updatePlayerInfo() {
        const character = this.gameState.character;
        if (!character) return;

        // Update basic character info
        document.getElementById('playerName').textContent = character.name;
        document.getElementById('playerLevel').textContent = `Level ${character.level}`;
        
        // Update D&D specific stats
        const healthElement = document.getElementById('playerHealth');
        if (healthElement) {
            healthElement.textContent = `Health: ${character.health}`;
        }
        
        const xpElement = document.getElementById('playerXP');
        if (xpElement) {
            xpElement.textContent = `XP: ${character.xp}`;
        }
        
        const goldElement = document.getElementById('playerGold');
        if (goldElement) {
            goldElement.textContent = `Gold: ${character.gold}`;
        }
        
        const locationElement = document.getElementById('playerLocation');
        if (locationElement) {
            locationElement.textContent = `Location: ${this.gameState.location}`;
        }
        
        const timeElement = document.getElementById('gameTime');
        if (timeElement) {
            timeElement.textContent = `Time: ${this.gameState.timeOfDay}`;
        }
        
        // Update dice roll display
        const rollElement = document.getElementById('lastRoll');
        if (rollElement && this.gameState.lastRoll) {
            rollElement.textContent = `Last Roll: ${this.gameState.lastRoll}`;
            rollElement.style.display = 'block';
        } else if (rollElement) {
            rollElement.style.display = 'none';
        }
        
        // Update abilities
        this.updateAbilities();
        
        // Update equipment
        this.updateEquipment();
        
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
        const staminaBar = document.getElementById('staminaBar');
        const staminaText = document.getElementById('staminaText');
        const actionPoints = document.getElementById('actionPoints');
        
        if (staminaBar && staminaText) {
            const stamina = this.gameState.combatResources.stamina;
            const maxStamina = this.gameState.combatResources.maxStamina;
            const percentage = (stamina / maxStamina) * 100;
            
            staminaBar.style.width = `${percentage}%`;
            staminaText.textContent = `${stamina}/${maxStamina}`;
            
            // Visual feedback for low stamina
            if (percentage < 25) {
                staminaBar.style.backgroundColor = '#ff4444';
            } else if (percentage < 50) {
                staminaBar.style.backgroundColor = '#ffaa00';
            } else {
                staminaBar.style.backgroundColor = '#44ff44';
            }
        }
        
        if (actionPoints) {
            const points = this.gameState.combatResources.actionPoints;
            const maxPoints = this.gameState.combatResources.maxActionPoints;
            
            const pointElements = actionPoints.querySelectorAll('.action-point');
            pointElements.forEach((point, index) => {
                if (index < points) {
                    point.classList.add('active');
                } else {
                    point.classList.remove('active');
                }
            });
        }
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
        if (!questList) return;
        
        const activeQuests = this.gameState.activeQuests || [];
        
        if (activeQuests.length === 0) {
            questList.innerHTML = '<div class="quest-empty">No active quests</div>';
            return;
        }
        
        questList.innerHTML = activeQuests.map(quest => `
            <div class="quest-item">
                <div class="quest-title">${quest.title}</div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${(quest.progress / quest.objectives.length) * 100}%"></div>
                    </div>
                    <span class="progress-text">${quest.progress}/${quest.objectives.length}</span>
                </div>
            </div>
        `).join('');
    }

    /**
     * Update inventory display (D&D Enhanced)
     */
    updateInventory() {
        const inventoryList = document.getElementById('inventoryList');
        if (!inventoryList) return;
        
        const inventory = this.gameState.character.inventory || [];
        
        if (inventory.length === 0) {
            inventoryList.innerHTML = '<div class="inventory-empty">No items</div>';
            return;
        }
        
        inventoryList.innerHTML = inventory.map(item => `
            <div class="inventory-item" onclick="game.useItem('${item.name}')">
                <span class="item-name">${item.name}</span>
                <span class="item-quantity">${item.quantity || 1}</span>
            </div>
        `).join('');
    }
    
    /**
     * Update D&D abilities display
     */
    updateAbilities() {
        const character = this.gameState.character;
        if (!character.abilities) return;
        
        const abilitiesElement = document.getElementById('characterAbilities');
        if (abilitiesElement) {
            let abilitiesHTML = '<h4>🎲 Abilities</h4>';
            for (const [ability, value] of Object.entries(character.abilities)) {
                abilitiesHTML += `<div class="ability-stat">
                    <span class="ability-name">${ability}:</span>
                    <span class="ability-value">${value}</span>
                </div>`;
            }
            abilitiesElement.innerHTML = abilitiesHTML;
        }
    }
    
    /**
     * Update D&D equipment display
     */
    updateEquipment() {
        const character = this.gameState.character;
        
        // Update wearing
        const wearingElement = document.getElementById('characterWearing');
        if (wearingElement && character.wearing) {
            wearingElement.innerHTML = `<h4>👕 Wearing</h4><ul>` +
                character.wearing.map(item => `<li>${item}</li>`).join('') +
                `</ul>`;
        }
        
        // Update wielding
        const wieldingElement = document.getElementById('characterWielding');
        if (wieldingElement && character.wielding) {
            wieldingElement.innerHTML = `<h4>⚔️ Wielding</h4><ul>` +
                character.wielding.map(item => `<li>${item}</li>`).join('') +
                `</ul>`;
        }
        
        // Update armor class
        const acElement = document.getElementById('characterAC');
        if (acElement) {
            acElement.textContent = `AC: ${character.armor_class}`;
        }
        
        // Update quest
        const questElement = document.getElementById('characterQuest');
        if (questElement) {
            questElement.innerHTML = `<h4>📜 Quest</h4><p>${character.quest}</p>`;
        }
    }

    /**
     * Update narrative display
     */
    updateNarrative() {
        const narrativeElement = document.getElementById('narrativeText');
        if (narrativeElement && this.gameState.currentNarrative) {
            narrativeElement.innerHTML = `<div class="narrative-content">${this.gameState.currentNarrative}</div>`;
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
        if (!choicesList) return;
        
        choicesList.innerHTML = '';
        
        if (this.gameState.availableChoices && this.gameState.availableChoices.length > 0) {
            this.gameState.availableChoices.forEach((choice, index) => {
                const button = document.createElement('button');
                button.className = 'choice-btn';
                button.innerHTML = `<span class='cmd-label'>${choice}</span>`;
                button.onclick = () => this.selectChoice(index);
                choicesList.appendChild(button);
            });
        } else {
            // Fallback choices
            const fallbackChoices = ["Continue", "Look around", "Check equipment", "Rest"];
            fallbackChoices.forEach((choice, index) => {
                const button = document.createElement('button');
                button.className = 'choice-btn';
                button.innerHTML = `<span class='cmd-label'>${choice}</span>`;
                button.onclick = () => this.selectChoice(index);
                choicesList.appendChild(button);
            });
        }
    }

    /**
     * Update turn counter
     */
    updateTurnCounter() {
        const turnElement = document.getElementById('turnCounter');
        if (turnElement) {
            turnElement.textContent = `Turn ${this.gameState.turnNumber}`;
        }
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
        const loadingElement = document.getElementById('loadingOverlay');
        if (!loadingElement) {
            // Create loading overlay if it doesn't exist
            const overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Processing your choice...</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.style.display = 'flex';
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }
    }

    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        // Remove existing status messages
        const existingMessages = document.querySelectorAll('.status-message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new status message
        const statusElement = document.createElement('div');
        statusElement.className = `status-message ${type}`;
        statusElement.textContent = message;
        
        document.body.appendChild(statusElement);
        
        // Show with animation
        setTimeout(() => {
            statusElement.classList.add('show');
        }, 100);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            statusElement.classList.remove('show');
            setTimeout(() => {
                if (statusElement.parentNode) {
                    statusElement.remove();
                }
            }, 300);
        }, 3000);
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

    updateCharacterSummary() {
        const char = this.gameState.character;
        if (!char || !char.name) return;
        
        const summaryDiv = document.querySelector('.character-summary');
        if (!summaryDiv) {
            // Create character summary if it doesn't exist
            const playerPanel = document.querySelector('.player-panel');
            if (playerPanel) {
                const summary = document.createElement('div');
                summary.className = 'character-summary';
                summary.innerHTML = `
                    <div class="char-summary-portrait" style="background-image: url('${char.portrait || 'https://api.dicebear.com/7.x/adventurer/svg?seed=default'}')"></div>
                    <div class="char-summary-info">
                        <div class="char-summary-name">${char.name}</div>
                        <div class="char-summary-details">${char.class} • ${char.background}</div>
                    </div>
                `;
                playerPanel.insertBefore(summary, playerPanel.firstChild);
            }
        } else {
            // Update existing summary
            const portrait = summaryDiv.querySelector('.char-summary-portrait');
            const name = summaryDiv.querySelector('.char-summary-name');
            const details = summaryDiv.querySelector('.char-summary-details');
            
            if (portrait) portrait.style.backgroundImage = `url('${char.portrait || 'https://api.dicebear.com/7.x/adventurer/svg?seed=default'}')`;
            if (name) name.textContent = char.name;
            if (details) details.textContent = `${char.class} • ${char.background}`;
        }
    }

    useItem(itemName) {
        const inventory = this.gameState.character.inventory || [];
        const item = inventory.find(i => i.name === itemName);
        
        if (!item) return;
        
        // Handle different item types
        if (item.type === 'consumable') {
            this.consumeItem(item);
        } else if (item.type === 'weapon') {
            this.equipWeapon(item);
        } else if (item.type === 'armor') {
            this.equipArmor(item);
        }
        
        this.updateInventory();
        this.updateEquipment();
        this.showStatus(`Used ${item.name}`, 'success');
    }

    consumeItem(item) {
        // Remove from inventory
        const inventory = this.gameState.character.inventory;
        const index = inventory.findIndex(i => i.name === item.name);
        
        if (index !== -1) {
            if (item.quantity > 1) {
                item.quantity--;
            } else {
                inventory.splice(index, 1);
            }
        }
        
        // Apply effects
        if (item.effects) {
            if (item.effects.health) {
                const currentHealth = parseInt(this.gameState.character.health.split('/')[0]);
                const maxHealth = parseInt(this.gameState.character.health.split('/')[1]);
                const newHealth = Math.min(currentHealth + item.effects.health, maxHealth);
                this.gameState.character.health = `${newHealth}/${maxHealth}`;
            }
            
            if (item.effects.stamina) {
                this.gameState.combatResources.stamina = Math.min(
                    this.gameState.combatResources.stamina + item.effects.stamina,
                    this.gameState.combatResources.maxStamina
                );
            }
        }
    }

    equipWeapon(weapon) {
        // Unequip current weapon
        const currentWeapon = this.gameState.character.wielding[0];
        if (currentWeapon) {
            this.gameState.character.inventory.push({
                name: currentWeapon,
                type: 'weapon',
                quantity: 1
            });
        }
        
        // Equip new weapon
        this.gameState.character.wielding = [weapon.name];
        
        // Remove from inventory
        const inventory = this.gameState.character.inventory;
        const index = inventory.findIndex(i => i.name === weapon.name);
        if (index !== -1) {
            inventory.splice(index, 1);
        }
    }

    equipArmor(armor) {
        // Unequip current armor
        const currentArmor = this.gameState.character.wearing[0];
        if (currentArmor) {
            this.gameState.character.inventory.push({
                name: currentArmor,
                type: 'armor',
                quantity: 1
            });
        }
        
        // Equip new armor
        this.gameState.character.wearing = [armor.name];
        
        // Update armor class
        if (armor.armor_class) {
            this.gameState.character.armor_class = armor.armor_class;
        }
        
        // Remove from inventory
        const inventory = this.gameState.character.inventory;
        const index = inventory.findIndex(i => i.name === armor.name);
        if (index !== -1) {
            inventory.splice(index, 1);
        }
    }

    addQuest(quest) {
        if (!this.gameState.activeQuests) {
            this.gameState.activeQuests = [];
        }
        
        this.gameState.activeQuests.push({
            ...quest,
            progress: 0,
            started: new Date().toISOString()
        });
        
        this.updateQuests();
        this.showStatus(`New quest: ${quest.title}`, 'quest');
    }

    updateQuestProgress(questTitle, objectiveIndex) {
        const quest = this.gameState.activeQuests.find(q => q.title === questTitle);
        if (!quest) return;
        
        if (objectiveIndex >= 0 && objectiveIndex < quest.objectives.length) {
            quest.progress = Math.max(quest.progress, objectiveIndex + 1);
            
            // Check if quest is complete
            if (quest.progress >= quest.objectives.length) {
                this.completeQuest(quest);
            }
        }
        
        this.updateQuests();
    }

    completeQuest(quest) {
        // Remove from active quests
        const index = this.gameState.activeQuests.findIndex(q => q.title === quest.title);
        if (index !== -1) {
            this.gameState.activeQuests.splice(index, 1);
        }
        
        // Add to completed quests
        if (!this.gameState.completedQuests) {
            this.gameState.completedQuests = [];
        }
        this.gameState.completedQuests.push({
            ...quest,
            completed: new Date().toISOString()
        });
        
        // Give rewards
        if (quest.rewards) {
            if (quest.rewards.xp) {
                this.gameState.character.xp += quest.rewards.xp;
                this.checkLevelUp();
            }
            
            if (quest.rewards.gold) {
                this.gameState.character.gold += quest.rewards.gold;
            }
            
            if (quest.rewards.items) {
                quest.rewards.items.forEach(item => {
                    this.addItemToInventory(item);
                });
            }
        }
        
        this.updateQuests();
        this.updatePlayerInfo();
        this.showStatus(`Quest completed: ${quest.title}`, 'success');
    }

    addItemToInventory(item) {
        if (!this.gameState.character.inventory) {
            this.gameState.character.inventory = [];
        }
        
        const existingItem = this.gameState.character.inventory.find(i => i.name === item.name);
        if (existingItem) {
            existingItem.quantity = (existingItem.quantity || 1) + (item.quantity || 1);
        } else {
            this.gameState.character.inventory.push({
                ...item,
                quantity: item.quantity || 1
            });
        }
        
        this.updateInventory();
    }

    checkLevelUp() {
        const xp = this.gameState.character.xp;
        const level = this.gameState.character.level;
        const xpForNextLevel = level * 100; // Simple XP formula
        
        if (xp >= xpForNextLevel) {
            this.gameState.character.level++;
            this.gameState.character.health = `${20 + (this.gameState.character.level - 1) * 5}/20`;
            this.showStatus(`Level up! You are now level ${this.gameState.character.level}`, 'levelup');
            this.updatePlayerInfo();
        }
    }

    showHelp() {
        const helpContent = `
            <div class="help-content">
                <h3>🎮 How to Play</h3>
                <ul>
                    <li><strong>Character Creation:</strong> Choose your class, background, and roll abilities</li>
                    <li><strong>Combat:</strong> Use Attack, Defend, and special abilities</li>
                    <li><strong>Inventory:</strong> Click items to use or equip them</li>
                    <li><strong>Quests:</strong> Complete objectives to earn XP and rewards</li>
                    <li><strong>Save/Load:</strong> Your progress is automatically saved</li>
                </ul>
                
                <h3>🎲 D&D Rules</h3>
                <ul>
                    <li><strong>Abilities:</strong> Strength, Dexterity, Intelligence, Wisdom, Charisma</li>
                    <li><strong>Combat:</strong> Use Action Points and manage Stamina</li>
                    <li><strong>Leveling:</strong> Gain XP to level up and improve abilities</li>
                </ul>
            </div>
        `;
        
        this.showStatus('Help information displayed in console', 'info');
        console.log(helpContent);
    }

    exitGame() {
        if (confirm('Are you sure you want to exit? Your progress will be saved.')) {
            this.saveGameState();
            window.close();
        }
    }
}

// Initialize the game when the page loads
let game;

document.addEventListener('DOMContentLoaded', () => {
    game = new AIRPGGame();

    // Auto-open character creation if no character
    if (!game.gameState.character || !game.gameState.character.name) {
        showCharCreateModal();
    }

    // Menu bar event listeners
    document.getElementById('menuCharCreate').onclick = () => showCharCreateModal();
    document.getElementById('menuMain').onclick = () => window.location.href = 'scenario-selection.html';
    document.getElementById('menuExit').onclick = () => window.location.reload();
    document.getElementById('menuHelp').onclick = () => showHelpModal();
    document.getElementById('menuSettings').onclick = () => showSettingsPanel();
    document.getElementById('menuSaveLoad').onclick = () => showSaveLoadModal();

    // Modal logic
    const modal = document.getElementById('charCreateModal');
    const closeBtn = document.getElementById('closeCharModal');
    closeBtn.onclick = () => modal.style.display = 'none';
    modal.onclick = (e) => { if (e.target === modal) modal.style.display = 'none'; };

    // Portrait logic
    const portraitPreview = document.getElementById('charPortraitPreview');
    const randomPortraitBtn = document.getElementById('randomPortraitBtn');
    function randomPortrait() {
        // Use a set of fantasy/cyberpunk avatars or placeholder
        const portraits = [
            'https://api.dicebear.com/7.x/fantasy/svg?seed=' + Math.random(),
            'https://api.dicebear.com/7.x/adventurer/svg?seed=' + Math.random(),
            'https://api.dicebear.com/7.x/micah/svg?seed=' + Math.random(),
            'https://api.dicebear.com/7.x/bottts/svg?seed=' + Math.random(),
            'https://api.dicebear.com/7.x/pixel-art/svg?seed=' + Math.random()
        ];
        const url = portraits[Math.floor(Math.random() * portraits.length)];
        portraitPreview.style.backgroundImage = `url('${url}')`;
        portraitPreview.dataset.url = url;
    }
    randomPortraitBtn.onclick = randomPortrait;
    randomPortrait();

    // Ability rolls logic
    const abilityNames = ['Strength', 'Dexterity', 'Intelligence', 'Persuasion', 'Luck'];
    const abilityRollsDiv = document.getElementById('abilityRolls');
    let abilityScores = [10, 10, 10, 10, 10];
    function rollAbilities() {
        abilityScores = abilityNames.map(() => Math.floor(Math.random() * 20) + 1);
        renderAbilityRolls();
    }
    function renderAbilityRolls() {
        abilityRollsDiv.innerHTML = '';
        abilityNames.forEach((name, i) => {
            const rollDiv = document.createElement('div');
            rollDiv.className = 'ability-roll';
            rollDiv.innerHTML = `<span class='ability-roll-label'>${name}</span><span class='ability-roll-value'>${abilityScores[i]}</span>`;
            abilityRollsDiv.appendChild(rollDiv);
        });
    }
    document.getElementById('rollAbilitiesBtn').onclick = rollAbilities;
    renderAbilityRolls();

    // Scenario-specific character options
    const scenarioCharacterOptions = {
        'northern_realms': {
            classes: ['Warrior', 'Mage', 'Rogue', 'Cleric', 'Paladin', 'Ranger'],
            backgrounds: ['Hermit', 'Noble', 'Outlander', 'Acolyte', 'Soldier', 'Merchant'],
            portraits: [
                'https://api.dicebear.com/7.x/fantasy/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/adventurer/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/micah/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/fantasy/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/adventurer/svg?seed=' + Math.random()
            ]
        },
        'whispering_town': {
            classes: ['Occultist', 'Detective', 'Doctor', 'Artist', 'Outsider', 'Priest'],
            backgrounds: ['Investigator', 'Scholar', 'Runaway', 'Medium', 'Journalist', 'Librarian'],
            portraits: [
                'https://api.dicebear.com/7.x/micah/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/bottts/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/fantasy/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/adventurer/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/micah/svg?seed=' + Math.random()
            ]
        },
        'neo_tokyo': {
            classes: ['Netrunner', 'Street Samurai', 'Techie', 'Fixer', 'Corporate', 'Hacker'],
            backgrounds: ['Street Kid', 'Ex-Corp', 'Nomad', 'AI Cultist', 'Mercenary', 'Data Broker'],
            portraits: [
                'https://api.dicebear.com/7.x/bottts/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/pixel-art/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/micah/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/bottts/svg?seed=' + Math.random(),
                'https://api.dicebear.com/7.x/pixel-art/svg?seed=' + Math.random()
            ]
        }
    };

    function getCurrentScenarioKey() {
        if (window.game && window.game.gameState && window.game.gameState.selectedScenario) {
            return window.game.gameState.selectedScenario;
        }
        // fallback: try sessionStorage
        return sessionStorage.getItem('currentScenario') || 'northern_realms';
    }

    function updateCharModalOptions() {
        const scenario = getCurrentScenarioKey();
        const opts = scenarioCharacterOptions[scenario] || scenarioCharacterOptions['northern_realms'];
        // Update class options
        const classSelect = document.getElementById('charClassInput');
        classSelect.innerHTML = opts.classes.map(c => `<option value="${c.toLowerCase().replace(/ /g,'_')}">${c}</option>`).join('');
        // Update background options
        const bgSelect = document.getElementById('charBackgroundInput');
        bgSelect.innerHTML = opts.backgrounds.map(b => `<option value="${b.toLowerCase().replace(/ /g,'_')}">${b}</option>`).join('');
    }

    function randomPortraitForScenario() {
        const scenario = getCurrentScenarioKey();
        const opts = scenarioCharacterOptions[scenario] || scenarioCharacterOptions['northern_realms'];
        const portraits = opts.portraits;
        const url = portraits[Math.floor(Math.random() * portraits.length)];
        const portraitPreview = document.getElementById('charPortraitPreview');
        portraitPreview.style.backgroundImage = `url('${url}')`;
        portraitPreview.dataset.url = url;
    }

    // Patch character creation submit for starting equipment
    const oldCharCreateFormSubmit = document.getElementById('charCreateForm').onsubmit;
    document.getElementById('charCreateForm').onsubmit = (e) => {
        e.preventDefault();
        const scenario = getScenarioKeySafe();
        const classVal = document.getElementById('charClassInput').value;
        const equip = (scenarioStartingEquipment[scenario][classVal] || {wearing:[], wielding:[], gold:20});
        // Update game state with new character
        const char = {
            name: document.getElementById('charNameInput').value || 'Ra\'el',
            gender: document.getElementById('charGenderInput').value,
            portrait: document.getElementById('charPortraitPreview').dataset.url,
            background: document.getElementById('charBackgroundInput').value,
            class: classVal,
            abilities: Object.fromEntries(window.abilityNames.map((n,i)=>[n, abilityScores[i] || 10])),
            level: 1,
            health: '20/20',
            xp: 0,
            gold: equip.gold,
            inventory: [],
            wearing: equip.wearing,
            wielding: equip.wielding,
            armor_class: 10,
            quest: 'None'
        };
        if (window.game && window.game.gameState) {
            window.game.gameState.character = char;
            window.game.gameState.gameStarted = true; // Mark game as started
            window.game.updatePlayerInfo();
            updateCharacterSummary();
            
            // Start the game automatically
            window.game.startGame();
        }
        document.getElementById('charCreateModal').style.display = 'none';
    };

    // Patch modal open logic to update ability names
    const oldShowCharCreateModal = window.showCharCreateModal;
    window.showCharCreateModal = function() {
        updateCharModalOptions();
        updateAbilityNamesInModal();
        randomPortraitForScenario();
        document.getElementById('charCreateModal').style.display = 'flex';
    };

    // Patch randomize all logic to update ability names
    const oldRandomCharBtn2 = document.getElementById('randomCharBtn').onclick;
    document.getElementById('randomCharBtn').onclick = () => {
        document.getElementById('charNameInput').value = randomFantasyName();
        document.getElementById('charGenderInput').selectedIndex = Math.floor(Math.random()*3);
        updateCharModalOptions();
        updateAbilityNamesInModal();
        document.getElementById('charBackgroundInput').selectedIndex = Math.floor(Math.random()*document.getElementById('charBackgroundInput').options.length);
        document.getElementById('charClassInput').selectedIndex = Math.floor(Math.random()*document.getElementById('charClassInput').options.length);
        randomPortraitForScenario();
        rollAbilities();
    };

    // Scenario-specific command buttons per turn
    document.addEventListener('DOMContentLoaded', () => {
        function updateScenarioCommands() {
            const scenario = getScenarioKeySafe();
            const commands = scenarioCommands[scenario] || scenarioCommands['northern_realms'];
            const choicesList = document.getElementById('choicesList');
            if (!choicesList) return;
            choicesList.innerHTML = '';
            commands.forEach(cmd => {
                const btn = document.createElement('button');
                btn.className = 'choice-btn';
                btn.innerHTML = `<span class='cmd-icon'>${cmd.icon}</span> <span class='cmd-label'>${cmd.label}</span>`;
                btn.title = cmd.tip;
                choicesList.appendChild(btn);
            });
        }
        // Call on each turn or when scenario changes
        window.updateScenarioCommands = updateScenarioCommands;
        // Optionally, call after game start or scenario select
    });

    // Scenario-specific atmospheric narration/effects
    function updateScenarioAtmosphere() {
        const scenario = getScenarioKeySafe();
        const heroDesc = {
            'northern_realms': 'A land of ancient dragons, mystical ley lines, and epic battles. Magic and steel shape the fate of kingdoms.',
            'whispering_town': 'Foggy streets, gas lamps, and cosmic secrets. Sanity is fragile, and reality is thin.',
            'neo_tokyo': 'Neon lights, acid rain, and digital souls. In the chrome-plated undercity, information is power.'
        };
        const el = document.querySelector('.hero-description');
        if (el) el.textContent = heroDesc[scenario] || heroDesc['northern_realms'];
        // Add scenario-specific background effect (class)
        const bg = document.querySelector('.hero-background');
        if (bg) {
            bg.className = 'hero-background ' + scenario;
        }
    }
    document.addEventListener('DOMContentLoaded', updateScenarioAtmosphere);
});

function randomFantasyName() {
    const first = ['Rael', 'Kael', 'Lira', 'Mira', 'Thar', 'Eryn', 'Jor', 'Sira', 'Vyn', 'Dara'];
    const last = ['Shadow', 'Bright', 'Storm', 'Vale', 'Iron', 'Moon', 'Dusk', 'Frost', 'Ash', 'Dawn'];
    return first[Math.floor(Math.random()*first.length)] + ' ' + last[Math.floor(Math.random()*last.length)];
}

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

// Scenario-specific ability names
const scenarioAbilityNames = {
    'northern_realms': ['Strength', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma'],
    'whispering_town': ['Willpower', 'Observation', 'Knowledge', 'Sanity', 'Persuasion'],
    'neo_tokyo': ['Reflexes', 'Tech', 'Cool', 'Hacking', 'Streetwise']
};

// Scenario-specific starting equipment
const scenarioStartingEquipment = {
    'northern_realms': {
        'warrior': {wearing: ['Chainmail'], wielding: ['Longsword'], gold: 30},
        'mage': {wearing: ['Robes'], wielding: ['Staff'], gold: 20},
        'rogue': {wearing: ['Leather Armor'], wielding: ['Dagger'], gold: 25},
        'cleric': {wearing: ['Priest Vestments'], wielding: ['Mace'], gold: 22},
        'paladin': {wearing: ['Plate Armor'], wielding: ['Warhammer'], gold: 18},
        'ranger': {wearing: ['Leather Armor'], wielding: ['Bow'], gold: 24}
    },
    'whispering_town': {
        'occultist': {wearing: ['Tattered Coat'], wielding: ['Occult Tome'], gold: 10},
        'detective': {wearing: ['Trenchcoat'], wielding: ['Revolver'], gold: 15},
        'doctor': {wearing: ['Lab Coat'], wielding: ['Scalpel'], gold: 18},
        'artist': {wearing: ['Bohemian Clothes'], wielding: ['Paintbrush'], gold: 12},
        'outsider': {wearing: ['Old Jacket'], wielding: ['Strange Relic'], gold: 8},
        'priest': {wearing: ['Clerical Robes'], wielding: ['Holy Symbol'], gold: 14}
    },
    'neo_tokyo': {
        'netrunner': {wearing: ['Synthweave Suit'], wielding: ['Cyberdeck'], gold: 50},
        'street_samurai': {wearing: ['Combat Jacket'], wielding: ['Katana'], gold: 40},
        'techie': {wearing: ['Utility Vest'], wielding: ['Tool Kit'], gold: 35},
        'fixer': {wearing: ['Urban Outfit'], wielding: ['Pistol'], gold: 38},
        'corporate': {wearing: ['Business Suit'], wielding: ['Derringer'], gold: 60},
        'hacker': {wearing: ['Hoodie'], wielding: ['Hacking Rig'], gold: 45}
    }
};

// Scenario-specific command options
const scenarioCommands = {
    'northern_realms': [
        {icon: '⚔️', label: 'Attack', tip: 'Strike with your weapon'},
        {icon: '🛡️', label: 'Defend', tip: 'Brace for incoming attacks'},
        {icon: '🧙', label: 'Cast Spell', tip: 'Use a magical ability'},
        {icon: '🏃', label: 'Flee', tip: 'Attempt to escape'},
        {icon: '🎲', label: 'Skill Check', tip: 'Attempt a special action'},
        {icon: '💬', label: 'Talk', tip: 'Negotiate or persuade'},
        {icon: '🎒', label: 'Inventory', tip: 'Use an item'}
    ],
    'whispering_town': [
        {icon: '🔍', label: 'Investigate', tip: 'Search for clues'},
        {icon: '🧠', label: 'Sanity Check', tip: 'Test your mental fortitude'},
        {icon: '🔫', label: 'Shoot', tip: 'Use your firearm'},
        {icon: '👁️', label: 'Observe', tip: 'Look for hidden details'},
        {icon: '📖', label: 'Read Tome', tip: 'Consult forbidden knowledge'},
        {icon: '🏃', label: 'Run', tip: 'Escape danger'},
        {icon: '💬', label: 'Talk', tip: 'Question or plead'}
    ],
    'neo_tokyo': [
        {icon: '💻', label: 'Hack', tip: 'Access digital systems'},
        {icon: '🤖', label: 'Deploy Drone', tip: 'Use a tech gadget'},
        {icon: '⚔️', label: 'Attack', tip: 'Strike with your weapon'},
        {icon: '🛡️', label: 'Defend', tip: 'Brace for attacks'},
        {icon: '🏃', label: 'Evade', tip: 'Dodge or escape'},
        {icon: '💬', label: 'Negotiate', tip: 'Persuade or bribe'},
        {icon: '🎒', label: 'Inventory', tip: 'Use an item'}
    ]
};

function getScenarioKeySafe() {
    const k = getCurrentScenarioKey ? getCurrentScenarioKey() : (window.game && window.game.gameState && window.game.gameState.selectedScenario) || 'northern_realms';
    return scenarioAbilityNames[k] ? k : 'northern_realms';
}

// Patch ability names in modal and game
function updateAbilityNamesInModal() {
    const scenario = getScenarioKeySafe();
    const names = scenarioAbilityNames[scenario];
    const abilityRollsDiv = document.getElementById('abilityRolls');
    if (!abilityRollsDiv) return;
    // Update abilityNames array for rolling
    window.abilityNames = names;
    // Re-render ability rolls
    if (typeof renderAbilityRolls === 'function') renderAbilityRolls();
}

// Settings panel integration
window.showSettingsPanel = function() {
    if (!window.gameSettings) {
        window.gameSettings = new GameSettings();
    }
    window.gameSettings.openSettingsPanel();
};
// Save/Load modal implementation
function showSaveLoadModal() {
    let modal = document.getElementById('saveLoadModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'saveLoadModal';
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <h2>Save / Load Game</h2>
                <div style="margin-bottom:1rem;">
                    <button id="saveGameBtnModal" class="btn-primary">💾 Save Game</button>
                    <button id="loadGameBtnModal" class="btn-secondary">📂 Load Game</button>
                </div>
                <div id="saveLoadStatus" style="min-height:2em;"></div>
                <button class="modal-cancel" id="closeSaveLoadModal">Close</button>
            </div>
        `;
        document.body.appendChild(modal);
        document.getElementById('closeSaveLoadModal').onclick = () => modal.style.display = 'none';
        document.getElementById('saveGameBtnModal').onclick = () => {
            try {
                localStorage.setItem('aiRpgGameState', JSON.stringify(window.game.gameState));
                document.getElementById('saveLoadStatus').textContent = 'Game saved!';
            } catch (e) {
                document.getElementById('saveLoadStatus').textContent = 'Save failed!';
            }
        };
        document.getElementById('loadGameBtnModal').onclick = () => {
            try {
                const data = localStorage.getItem('aiRpgGameState');
                if (data) {
                    window.game.gameState = JSON.parse(data);
                    window.game.updatePlayerInfo();
                    if (window.game.gameState.character) updateCharacterSummary();
                    document.getElementById('saveLoadStatus').textContent = 'Game loaded!';
                } else {
                    document.getElementById('saveLoadStatus').textContent = 'No saved game found.';
                }
            } catch (e) {
                document.getElementById('saveLoadStatus').textContent = 'Load failed!';
            }
        };
    }
    modal.style.display = 'flex';
}
// Help modal stub
window.showHelpModal = function() {
    alert('Help coming soon!');
};

