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
     * Make a turn request to the backend (D&D Enhanced)
     */
    async makeTurnRequest(choice, playerName = null) {
        let requestData = null;
        try {
            requestData = {
                player_name: playerName || this.gameState.character.name,
                choice: choice,
                scenario: this.gameState.selectedScenario || 'northern_realms',
                ai_provider: this.gameState.aiProvider,
                api_key: this.gameState.apiKey
            };
            
            // Include D&D character data
            if (this.gameState.character) {
                requestData.character_data = this.gameState.character;
            }
            
            // Include scenario-specific data
            if (this.gameState.combatResources) {
                requestData.combat_resources = this.gameState.combatResources;
            }
            
            if (this.gameState.sanityState) {
                requestData.sanity_state = this.gameState.sanityState;
            }
            
            console.log('Sending D&D request data:', requestData);
            
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
            
            // Update D&D game state from response
            if (data.game_type === 'dnd_adventure') {
                this.updateDnDGameState(data);
            }
            
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
     * Update D&D game state from server response
     */
    updateDnDGameState(response) {
        if (response.metadata) {
            const meta = response.metadata;
            this.gameState.turnNumber = meta.turn || this.gameState.turnNumber;
            this.gameState.timeOfDay = meta.time_of_day || this.gameState.timeOfDay;
            this.gameState.location = meta.location || this.gameState.location;
            this.gameState.lastRoll = meta.last_roll;
            
            // Update character stats
            if (meta.health) this.gameState.character.health = meta.health;
            if (meta.xp !== undefined) this.gameState.character.xp = meta.xp;
            if (meta.level !== undefined) this.gameState.character.level = meta.level;
            if (meta.gold !== undefined) this.gameState.character.gold = meta.gold;
        }
        
        if (response.character) {
            const char = response.character;
            if (char.abilities) this.gameState.character.abilities = char.abilities;
            if (char.inventory) this.gameState.character.inventory = char.inventory;
            if (char.wearing) this.gameState.character.wearing = char.wearing;
            if (char.wielding) this.gameState.character.wielding = char.wielding;
            if (char.armor_class !== undefined) this.gameState.character.armor_class = char.armor_class;
            if (char.quest) this.gameState.character.quest = char.quest;
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
     * Update inventory display (D&D Enhanced)
     */
    updateInventory() {
        const inventoryList = document.getElementById('inventoryList');
        const inventory = this.gameState.character?.inventory || [];
        
        if (inventory.length === 0) {
            inventoryList.innerHTML = '<div class="inventory-empty">No items</div>';
            return;
        }
        
        inventoryList.innerHTML = inventory.map(item => 
            `<div class="inventory-item">${item}</div>`
        ).join('');
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

    // Randomize all
    document.getElementById('randomCharBtn').onclick = () => {
        document.getElementById('charNameInput').value = randomFantasyName();
        document.getElementById('charGenderInput').selectedIndex = Math.floor(Math.random()*3);
        document.getElementById('charBackgroundInput').selectedIndex = Math.floor(Math.random()*5);
        document.getElementById('charClassInput').selectedIndex = Math.floor(Math.random()*5);
        randomPortrait();
        rollAbilities();
    };
    function randomFantasyName() {
        const first = ['Rael', 'Kael', 'Lira', 'Mira', 'Thar', 'Eryn', 'Jor', 'Sira', 'Vyn', 'Dara'];
        const last = ['Shadow', 'Bright', 'Storm', 'Vale', 'Iron', 'Moon', 'Dusk', 'Frost', 'Ash', 'Dawn'];
        return first[Math.floor(Math.random()*first.length)] + ' ' + last[Math.floor(Math.random()*last.length)];
    }

    // Handle character creation submit
    document.getElementById('charCreateForm').onsubmit = (e) => {
        e.preventDefault();
        // Update game state with new character
        const char = {
            name: document.getElementById('charNameInput').value || 'Ra\'el',
            gender: document.getElementById('charGenderInput').value,
            portrait: portraitPreview.dataset.url,
            background: document.getElementById('charBackgroundInput').value,
            class: document.getElementById('charClassInput').value,
            abilities: {
                Strength: abilityScores[0],
                Dexterity: abilityScores[1],
                Intelligence: abilityScores[2],
                Persuasion: abilityScores[3],
                Luck: abilityScores[4]
            },
            level: 1,
            health: '20/20',
            xp: 0,
            gold: 50,
            inventory: [],
            wearing: [],
            wielding: [],
            armor_class: 10,
            quest: 'None'
        };
        if (window.game && window.game.gameState) {
            window.game.gameState.character = char;
            window.game.updatePlayerInfo();
            updateCharacterSummary();
        }
        modal.style.display = 'none';
    };

    // Character summary always visible
    function updateCharacterSummary() {
        const panel = document.querySelector('.player-panel');
        let summary = document.getElementById('characterSummary');
        if (!summary) {
            summary = document.createElement('div');
            summary.id = 'characterSummary';
            summary.className = 'character-summary';
            panel.prepend(summary);
        }
        const char = game.gameState.character;
        if (char) {
            summary.innerHTML = `
                <div class="char-summary-portrait" style="background-image:url('${char.portrait}')"></div>
                <div class="char-summary-info">
                    <div class="char-summary-name">${char.name}</div>
                    <div class="char-summary-meta">${char.class} | ${char.background}</div>
                </div>
            `;
        }
    }
    // Also call on load if character exists
    if (game.gameState.character && game.gameState.character.name) {
        updateCharacterSummary();
    }

    // Settings panel integration
    window.showSettingsPanel = function() {
        if (!window.gameSettings) {
            window.gameSettings = new GameSettings();
        }
        window.gameSettings.openSettingsPanel();
    };
    // Save/Load modal stub
    window.showSaveLoadModal = function() {
        alert('Save/Load coming soon!');
    };
    // Help modal stub
    window.showHelpModal = function() {
        alert('Help coming soon!');
    };
});

function showCharCreateModal() {
    document.getElementById('charCreateModal').style.display = 'flex';
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

