/**
 * Enhanced AI-RPG-Alpha Frontend
 * 
 * Supports:
 * - Long-form quest visualization (30-40 turns)
 * - BG3-style combat interface
 * - Cosmic horror sanity meter
 * - Quest progression tracker
 * - Three scenarios
 */

class EnhancedRPGGame {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8000';
        this.playerId = null;
        this.scenario = null;
        this.inCombat = false;
        
        this.gameState = {
            player: null,
            quest: null,
            combat: null,
            sanity: null,
            narrative: '',
            choices: []
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadScenarios();
    }
    
    // ========================================================================
    // EVENT LISTENERS
    // ========================================================================
    
    setupEventListeners() {
        // New game button
        const newGameBtn = document.getElementById('startNewGameBtn');
        if (newGameBtn) {
            newGameBtn.addEventListener('click', () => this.startNewGame());
        }
        
        // Choice buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('choice-btn')) {
                const choiceIndex = parseInt(e.target.dataset.index);
                const choiceText = e.target.dataset.text;
                this.makeChoice(choiceText, choiceIndex);
            }
        });
        
        // Combat action buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('combat-action-btn')) {
                const action = e.target.dataset.action;
                const targetIndex = e.target.dataset.target;
                this.makeCombatAction(action, targetIndex);
            }
        });
        
        // Save/Load buttons
        const saveBtn = document.getElementById('saveGameBtn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveGame());
        }
        
        const loadBtn = document.getElementById('loadGameBtn');
        if (loadBtn) {
            loadBtn.addEventListener('click', () => this.loadGame());
        }
    }
    
    // ========================================================================
    // API CALLS
    // ========================================================================
    
    async loadScenarios() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/scenarios`);
            const data = await response.json();
            this.displayScenarios(data.scenarios);
        } catch (error) {
            console.error('Failed to load scenarios:', error);
        }
    }
    
    async startNewGame() {
        const playerName = document.getElementById('playerNameInput')?.value || 'Adventurer';
        const scenarioSelect = document.getElementById('scenarioSelect');
        this.scenario = scenarioSelect?.value || 'whispering_town';
        
        try {
            this.showLoading(true);
            
            const response = await fetch(`${this.apiBaseUrl}/game/new`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_name: playerName,
                    scenario: this.scenario,
                    abilities: null // Will use defaults
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.playerId = data.player_id;
                this.gameState = {
                    player: data.player_stats,
                    quest: data.quest_state,
                    sanity: data.sanity_state,
                    narrative: data.narrative,
                    choices: data.choices || []
                };
                
                this.updateUI();
                this.displayNarrative(data.narrative);
                this.displayChoices(data.choices || []);
            }
            
        } catch (error) {
            console.error('Failed to start game:', error);
            this.showError('Failed to start game');
        } finally {
            this.showLoading(false);
        }
    }
    
    async makeChoice(choiceText, choiceIndex) {
        if (!this.playerId) return;
        
        try {
            this.showLoading(true);
            
            const response = await fetch(`${this.apiBaseUrl}/game/turn`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    action: choiceText,
                    choice_index: choiceIndex
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.gameState.quest = data.quest_state;
                this.gameState.player = data.player_stats;
                this.gameState.sanity = data.sanity_state;
                
                // Check if combat initiated
                if (data.combat_initiated) {
                    this.inCombat = true;
                    this.gameState.combat = data.combat_state;
                    this.displayCombat(data.combat_narrative, data.combat_choices);
                } else if (data.in_combat) {
                    this.displayCombat(data.narrative, data.choices, data.combat_state);
                } else if (data.combat_ended) {
                    this.inCombat = false;
                    this.gameState.combat = null;
                    this.displayNarrative(data.narrative);
                    this.displayChoices(data.choices);
                } else {
                    this.displayNarrative(data.narrative);
                    this.displayChoices(data.choices);
                }
                
                this.updateUI();
            }
            
        } catch (error) {
            console.error('Failed to process turn:', error);
            this.showError('Failed to process turn');
        } finally {
            this.showLoading(false);
        }
    }
    
    async makeCombatAction(action, targetIndex) {
        if (!this.playerId) return;
        
        try {
            this.showLoading(true);
            
            const response = await fetch(`${this.apiBaseUrl}/game/combat/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    action: action,
                    target_index: targetIndex ? parseInt(targetIndex) : null
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                if (data.combat_ended) {
                    this.inCombat = false;
                    this.gameState.combat = null;
                    this.displayNarrative(data.narrative);
                    this.displayChoices(data.choices);
                } else {
                    this.displayCombat(data.narrative, data.choices, data.combat_state);
                }
                
                this.gameState.player = data.player_stats;
                this.updateUI();
            }
            
        } catch (error) {
            console.error('Failed to process combat action:', error);
            this.showError('Failed to process combat action');
        } finally {
            this.showLoading(false);
        }
    }
    
    // ========================================================================
    // UI UPDATES
    // ========================================================================
    
    updateUI() {
        this.updatePlayerStats();
        this.updateQuestProgress();
        this.updateSanityMeter();
    }
    
    updatePlayerStats() {
        if (!this.gameState.player) return;
        
        const player = this.gameState.player;
        
        // Update basic stats
        this.setElementText('playerName', player.name);
        this.setElementText('playerLevel', player.level);
        this.setElementText('playerHealth', `${player.health}/${player.max_health}`);
        this.setElementText('playerGold', player.gold);
        
        // Update abilities
        this.setElementText('strengthValue', player.strength);
        this.setElementText('dexterityValue', player.dexterity);
        this.setElementText('intelligenceValue', player.intelligence);
        this.setElementText('wisdomValue', player.wisdom);
        this.setElementText('charismaValue', player.charisma);
        
        // Update combat resources
        if (this.inCombat) {
            this.setElementText('staminaText', `${player.stamina}/${player.max_stamina}`);
            this.setProgressBar('staminaBar', player.stamina, player.max_stamina);
            
            this.updateActionPoints(player.action_points, player.max_action_points);
        }
    }
    
    updateQuestProgress() {
        if (!this.gameState.quest) return;
        
        const quest = this.gameState.quest;
        
        // Show quest progress indicator
        const progressContainer = document.getElementById('questProgressContainer');
        if (progressContainer) {
            progressContainer.innerHTML = `
                <div class="quest-progress-bar">
                    <div class="quest-act-indicator">${quest.current_act?.toUpperCase() || 'SETUP'}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${quest.progress_percentage || 0}%"></div>
                    </div>
                    <div class="progress-text">
                        Turn ${quest.turn_number || 1}/${quest.total_turns || 40} 
                        (${(quest.progress_percentage || 0).toFixed(0)}%)
                    </div>
                </div>
                
                ${quest.milestone_reached ? `
                    <div class="milestone-indicator">
                        🎯 <strong>MILESTONE REACHED</strong>
                    </div>
                ` : ''}
                
                <div class="quest-stats">
                    <span>Combat Encounters: ${quest.combat_encounters || 0}</span>
                    <span>Major Choices: ${quest.major_choices || 0}</span>
                </div>
            `;
        }
    }
    
    updateSanityMeter() {
        if (this.scenario !== 'whispering_town' || !this.gameState.sanity) return;
        
        const sanity = this.gameState.sanity;
        const sanitySection = document.getElementById('sanitySection');
        
        if (sanitySection) {
            sanitySection.style.display = 'block';
            
            this.setElementText('sanityText', `${sanity.current_sanity}/${sanity.max_sanity}`);
            this.setProgressBar('sanityBar', sanity.current_sanity, sanity.max_sanity);
            
            // Update corruption indicator
            const corruptionIndicator = document.getElementById('corruptionIndicator');
            if (corruptionIndicator) {
                corruptionIndicator.innerHTML = `
                    <div class="corruption-level">
                        🧠 Corruption: ${sanity.corruption_percentage?.toFixed(0) || 0}%
                    </div>
                    <div class="sanity-level ${sanity.sanity_level}">
                        State: ${sanity.sanity_level?.toUpperCase() || 'STABLE'}
                    </div>
                    ${sanity.knowledge_count > 0 ? `
                        <div class="forbidden-knowledge">
                            📖 Forbidden Knowledge: ${sanity.knowledge_count}
                        </div>
                    ` : ''}
                `;
            }
        }
    }
    
    displayNarrative(narrative) {
        const narrativeContainer = document.getElementById('narrativeText');
        if (narrativeContainer) {
            // Apply cosmic horror text corruption if applicable
            const displayText = this.applyTextEffects(narrative);
            
            narrativeContainer.innerHTML = `
                <div class="narrative-content">
                    ${this.formatNarrative(displayText)}
                </div>
            `;
            
            narrativeContainer.scrollTop = narrativeContainer.scrollHeight;
        }
    }
    
    displayChoices(choices) {
        const choiceContainer = document.getElementById('choicesList');
        if (choiceContainer) {
            choiceContainer.innerHTML = '';
            
            choices.forEach((choice, index) => {
                const button = document.createElement('button');
                button.className = 'choice-btn';
                button.dataset.index = index;
                button.dataset.text = choice;
                button.textContent = choice;
                choiceContainer.appendChild(button);
            });
        }
        
        document.getElementById('choiceContainer').style.display = 'block';
    }
    
    displayCombat(narrative, choices, combatState) {
        // Display combat narrative
        this.displayNarrative(narrative);
        
        // Display combat-specific UI
        const combatContainer = document.getElementById('combatContainer');
        if (combatContainer && combatState) {
            combatContainer.style.display = 'block';
            combatContainer.innerHTML = this.generateCombatUI(combatState);
        }
        
        // Display combat choices
        this.displayCombatChoices(choices);
    }
    
    generateCombatUI(combatState) {
        let html = `
            <div class="combat-ui">
                <div class="combat-header">
                    <h3>⚔️ COMBAT - Turn ${combatState.turn || 1}</h3>
                </div>
                
                <div class="combat-enemies">
                    <h4>Enemies:</h4>
        `;
        
        // Display enemies
        combatState.enemies?.forEach((enemy, index) => {
            const healthPercent = (enemy.health / enemy.max_health) * 100;
            const statusClass = enemy.is_alive ? 'alive' : 'defeated';
            
            html += `
                <div class="enemy-card ${statusClass}">
                    <div class="enemy-name">${enemy.name}</div>
                    <div class="enemy-health-bar">
                        <div class="health-fill" style="width: ${healthPercent}%"></div>
                        <span class="health-text">${enemy.health}/${enemy.max_health}</span>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
                
                <div class="combat-resources">
                    <h4>Your Resources:</h4>
                    <div class="resource-display">
                        <div class="resource-item">
                            <span>⚡ Stamina:</span>
                            <span>${combatState.resources?.stamina || 0}/${combatState.resources?.max_stamina || 100}</span>
                        </div>
                        <div class="resource-item">
                            <span>🎯 Action Points:</span>
                            <span>${combatState.resources?.action_points || 0}/${combatState.resources?.max_action_points || 2}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        return html;
    }
    
    displayCombatChoices(choices) {
        const choiceContainer = document.getElementById('choicesList');
        if (choiceContainer) {
            choiceContainer.innerHTML = '';
            
            choices.forEach((choice, index) => {
                const button = document.createElement('button');
                button.className = 'choice-btn combat-action-btn';
                button.dataset.index = index;
                button.dataset.action = choice;
                button.dataset.target = index;
                button.textContent = choice;
                choiceContainer.appendChild(button);
            });
        }
    }
    
    displayScenarios(scenarios) {
        const scenarioSelect = document.getElementById('scenarioSelect');
        if (scenarioSelect) {
            scenarioSelect.innerHTML = '';
            
            scenarios.forEach(scenario => {
                const option = document.createElement('option');
                option.value = scenario.id;
                option.textContent = `${scenario.name} (${scenario.genre})`;
                scenarioSelect.appendChild(option);
            });
        }
    }
    
    // ========================================================================
    // HELPER METHODS
    // ========================================================================
    
    setElementText(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = text;
        }
    }
    
    setProgressBar(barId, current, max) {
        const bar = document.getElementById(barId);
        if (bar) {
            const percent = (current / max) * 100;
            bar.style.width = `${percent}%`;
        }
    }
    
    updateActionPoints(current, max) {
        const container = document.getElementById('actionPoints');
        if (container) {
            container.innerHTML = '';
            
            for (let i = 0; i < max; i++) {
                const point = document.createElement('span');
                point.className = `action-point ${i < current ? 'active' : ''}`;
                container.appendChild(point);
            }
        }
    }
    
    formatNarrative(text) {
        // Convert markdown-style formatting to HTML
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^(.+)$/, '<p>$1</p>');
    }
    
    applyTextEffects(text) {
        // Apply cosmic horror text corruption if sanity is low
        if (this.scenario === 'whispering_town' && this.gameState.sanity) {
            const sanityPercent = this.gameState.sanity.sanity_percentage || 100;
            
            if (sanityPercent < 40) {
                // Apply corruption effects
                // This would be enhanced with actual corruption algorithms
                return text;
            }
        }
        
        return text;
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }
    
    showError(message) {
        alert(`Error: ${message}`);
    }
    
    // ========================================================================
    // SAVE/LOAD
    // ========================================================================
    
    async saveGame() {
        if (!this.playerId) return;
        
        const slotNumber = prompt('Enter save slot number (1-5):');
        if (!slotNumber) return;
        
        const saveName = prompt('Enter save name:') || `Save ${slotNumber}`;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/game/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    slot_number: parseInt(slotNumber),
                    save_name: saveName
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Game saved successfully!');
            } else {
                alert('Failed to save game');
            }
        } catch (error) {
            console.error('Save failed:', error);
            alert('Failed to save game');
        }
    }
    
    async loadGame() {
        const slotNumber = prompt('Enter save slot number to load (1-5):');
        if (!slotNumber) return;
        
        // Would need player ID - this is simplified
        alert('Load game feature requires player ID. Use continue game instead.');
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new EnhancedRPGGame();
});

