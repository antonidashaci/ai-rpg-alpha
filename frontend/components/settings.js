/**
 * AI-RPG-Alpha: Settings Management Component
 * 
 * Handles user preferences, game settings, and customization options.
 * Part of Phase 4: Advanced UI & User Experience as defined in PRD.
 */

class GameSettings {
    constructor() {
        this.settings = this.loadSettings();
        this.settingsPanel = null;
        this.isOpen = false;
        this.init();
    }

    /**
     * Initialize settings system
     */
    init() {
        this.createSettingsButton();
        this.createSettingsPanel();
        this.applySettings();
        this.bindEvents();
    }

    /**
     * Default settings configuration
     */
    getDefaultSettings() {
        return {
            // Display Settings
            theme: 'dark',
            fontSize: 'medium',
            animations: true,
            reducedMotion: false,
            highContrast: false,
            
            // Audio Settings
            masterVolume: 0.7,
            musicVolume: 0.5,
            sfxVolume: 0.6,
            ambientVolume: 0.4,
            muteAll: false,
            
            // Gameplay Settings
            autoSave: true,
            saveInterval: 30, // seconds
            showTips: true,
            confirmActions: false,
            fastText: false,
            skipIntros: false,
            
            // Accessibility Settings
            screenReader: false,
            largeText: false,
            colorBlindSupport: false,
            keyboardNav: false,
            
            // Advanced Settings
            apiTimeout: 30,
            maxRetries: 3,
            debugMode: false,
            telemetry: true
        };
    }

    /**
     * Load settings from localStorage
     */
    loadSettings() {
        try {
            const saved = localStorage.getItem('aiRpgSettings');
            if (saved) {
                const parsed = JSON.parse(saved);
                return { ...this.getDefaultSettings(), ...parsed };
            }
        } catch (error) {
            console.warn('Failed to load settings:', error);
        }
        return this.getDefaultSettings();
    }

    /**
     * Save settings to localStorage
     */
    saveSettings() {
        try {
            localStorage.setItem('aiRpgSettings', JSON.stringify(this.settings));
            this.applySettings();
            this.showNotification('Settings saved successfully', 'success');
        } catch (error) {
            console.error('Failed to save settings:', error);
            this.showNotification('Failed to save settings', 'error');
        }
    }

    /**
     * Create settings toggle button
     */
    createSettingsButton() {
        const button = document.createElement('button');
        button.id = 'settingsToggle';
        button.className = 'settings-toggle';
        button.innerHTML = '⚙️ Settings';
        button.setAttribute('aria-label', 'Open game settings');
        button.onclick = () => this.toggleSettingsPanel();
        
        // Add to page (adjust selector as needed)
        const container = document.querySelector('.game-header') || document.body;
        container.appendChild(button);
    }

    /**
     * Create settings panel HTML
     */
    createSettingsPanel() {
        const panel = document.createElement('div');
        panel.id = 'settingsPanel';
        panel.className = 'settings-panel hidden';
        panel.innerHTML = this.generateSettingsPanelHTML();
        
        document.body.appendChild(panel);
        this.settingsPanel = panel;
        this.bindSettingsEvents();
    }

    /**
     * Generate settings panel HTML
     */
    generateSettingsPanelHTML() {
        return `
            <div class="settings-overlay">
                <div class="settings-content">
                    <div class="settings-header">
                        <h2>Game Settings</h2>
                        <button class="settings-close" aria-label="Close settings">&times;</button>
                    </div>
                    
                    <div class="settings-body">
                        <div class="settings-tabs">
                            <button class="tab-btn active" data-tab="display">Display</button>
                            <button class="tab-btn" data-tab="audio">Audio</button>
                            <button class="tab-btn" data-tab="gameplay">Gameplay</button>
                            <button class="tab-btn" data-tab="accessibility">Accessibility</button>
                            <button class="tab-btn" data-tab="advanced">Advanced</button>
                        </div>
                        
                        <div class="settings-content-area">
                            ${this.generateDisplaySettings()}
                            ${this.generateAudioSettings()}
                            ${this.generateGameplaySettings()}
                            ${this.generateAccessibilitySettings()}
                            ${this.generateAdvancedSettings()}
                        </div>
                    </div>
                    
                    <div class="settings-footer">
                        <button class="btn-secondary" id="resetSettings">Reset to Defaults</button>
                        <button class="btn-primary" id="saveSettings">Save Changes</button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Generate display settings HTML
     */
    generateDisplaySettings() {
        return `
            <div class="tab-content active" data-tab="display">
                <h3>Display Settings</h3>
                
                <div class="setting-group">
                    <label for="theme">Theme</label>
                    <select id="theme" name="theme">
                        <option value="dark" ${this.settings.theme === 'dark' ? 'selected' : ''}>Dark Theme</option>
                        <option value="light" ${this.settings.theme === 'light' ? 'selected' : ''}>Light Theme</option>
                        <option value="auto" ${this.settings.theme === 'auto' ? 'selected' : ''}>Auto (System)</option>
                    </select>
                </div>
                
                <div class="setting-group">
                    <label for="fontSize">Font Size</label>
                    <select id="fontSize" name="fontSize">
                        <option value="small" ${this.settings.fontSize === 'small' ? 'selected' : ''}>Small</option>
                        <option value="medium" ${this.settings.fontSize === 'medium' ? 'selected' : ''}>Medium</option>
                        <option value="large" ${this.settings.fontSize === 'large' ? 'selected' : ''}>Large</option>
                        <option value="xlarge" ${this.settings.fontSize === 'xlarge' ? 'selected' : ''}>Extra Large</option>
                    </select>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="animations" name="animations" ${this.settings.animations ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Enable Animations
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="reducedMotion" name="reducedMotion" ${this.settings.reducedMotion ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Reduce Motion (Accessibility)
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="highContrast" name="highContrast" ${this.settings.highContrast ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        High Contrast Mode
                    </label>
                </div>
            </div>
        `;
    }

    /**
     * Generate audio settings HTML
     */
    generateAudioSettings() {
        return `
            <div class="tab-content" data-tab="audio">
                <h3>Audio Settings</h3>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="muteAll" name="muteAll" ${this.settings.muteAll ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Mute All Audio
                    </label>
                </div>
                
                <div class="volume-group">
                    <div class="setting-group">
                        <label for="masterVolume">Master Volume</label>
                        <div class="volume-control">
                            <input type="range" id="masterVolume" name="masterVolume" min="0" max="1" step="0.1" value="${this.settings.masterVolume}">
                            <span class="volume-value">${Math.round(this.settings.masterVolume * 100)}%</span>
                        </div>
                    </div>
                    
                    <div class="setting-group">
                        <label for="musicVolume">Music Volume</label>
                        <div class="volume-control">
                            <input type="range" id="musicVolume" name="musicVolume" min="0" max="1" step="0.1" value="${this.settings.musicVolume}">
                            <span class="volume-value">${Math.round(this.settings.musicVolume * 100)}%</span>
                        </div>
                    </div>
                    
                    <div class="setting-group">
                        <label for="sfxVolume">Sound Effects</label>
                        <div class="volume-control">
                            <input type="range" id="sfxVolume" name="sfxVolume" min="0" max="1" step="0.1" value="${this.settings.sfxVolume}">
                            <span class="volume-value">${Math.round(this.settings.sfxVolume * 100)}%</span>
                        </div>
                    </div>
                    
                    <div class="setting-group">
                        <label for="ambientVolume">Ambient Sounds</label>
                        <div class="volume-control">
                            <input type="range" id="ambientVolume" name="ambientVolume" min="0" max="1" step="0.1" value="${this.settings.ambientVolume}">
                            <span class="volume-value">${Math.round(this.settings.ambientVolume * 100)}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Generate gameplay settings HTML
     */
    generateGameplaySettings() {
        return `
            <div class="tab-content" data-tab="gameplay">
                <h3>Gameplay Settings</h3>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="autoSave" name="autoSave" ${this.settings.autoSave ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Auto-save Game Progress
                    </label>
                </div>
                
                <div class="setting-group">
                    <label for="saveInterval">Auto-save Interval (seconds)</label>
                    <input type="number" id="saveInterval" name="saveInterval" min="10" max="300" value="${this.settings.saveInterval}">
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="showTips" name="showTips" ${this.settings.showTips ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Show Gameplay Tips
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="confirmActions" name="confirmActions" ${this.settings.confirmActions ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Confirm Important Actions
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="fastText" name="fastText" ${this.settings.fastText ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Fast Text Display
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="skipIntros" name="skipIntros" ${this.settings.skipIntros ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Skip Intro Sequences
                    </label>
                </div>
            </div>
        `;
    }

    /**
     * Generate accessibility settings HTML
     */
    generateAccessibilitySettings() {
        return `
            <div class="tab-content" data-tab="accessibility">
                <h3>Accessibility Settings</h3>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="screenReader" name="screenReader" ${this.settings.screenReader ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Screen Reader Support
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="largeText" name="largeText" ${this.settings.largeText ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Large Text Mode
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="colorBlindSupport" name="colorBlindSupport" ${this.settings.colorBlindSupport ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Color Blind Support
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="keyboardNav" name="keyboardNav" ${this.settings.keyboardNav ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Keyboard Navigation
                    </label>
                </div>
            </div>
        `;
    }

    /**
     * Generate advanced settings HTML
     */
    generateAdvancedSettings() {
        return `
            <div class="tab-content" data-tab="advanced">
                <h3>Advanced Settings</h3>
                
                <div class="setting-group">
                    <label for="apiTimeout">API Timeout (seconds)</label>
                    <input type="number" id="apiTimeout" name="apiTimeout" min="5" max="120" value="${this.settings.apiTimeout}">
                </div>
                
                <div class="setting-group">
                    <label for="maxRetries">Max API Retries</label>
                    <input type="number" id="maxRetries" name="maxRetries" min="1" max="10" value="${this.settings.maxRetries}">
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="debugMode" name="debugMode" ${this.settings.debugMode ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Debug Mode
                    </label>
                </div>
                
                <div class="setting-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="telemetry" name="telemetry" ${this.settings.telemetry ? 'checked' : ''}>
                        <span class="checkmark"></span>
                        Anonymous Usage Analytics
                    </label>
                </div>
            </div>
        `;
    }

    /**
     * Bind events for settings panel
     */
    bindSettingsEvents() {
        // Close button
        this.settingsPanel.querySelector('.settings-close').onclick = () => this.closeSettingsPanel();
        
        // Tab switching
        this.settingsPanel.querySelectorAll('.tab-btn').forEach(btn => {
            btn.onclick = () => this.switchTab(btn.dataset.tab);
        });
        
        // Volume sliders
        this.settingsPanel.querySelectorAll('input[type="range"]').forEach(slider => {
            slider.oninput = () => this.updateVolumeDisplay(slider);
        });
        
        // Settings inputs
        this.settingsPanel.querySelectorAll('input, select').forEach(input => {
            input.onchange = () => this.updateSetting(input.name, this.getInputValue(input));
        });
        
        // Footer buttons
        this.settingsPanel.querySelector('#resetSettings').onclick = () => this.resetSettings();
        this.settingsPanel.querySelector('#saveSettings').onclick = () => this.saveSettings();
        
        // Close on overlay click
        this.settingsPanel.querySelector('.settings-overlay').onclick = (e) => {
            if (e.target.classList.contains('settings-overlay')) {
                this.closeSettingsPanel();
            }
        };
        
        // Keyboard navigation
        this.settingsPanel.onkeydown = (e) => {
            if (e.key === 'Escape') {
                this.closeSettingsPanel();
            }
        };
    }

    /**
     * Bind global events
     */
    bindEvents() {
        // Keyboard shortcut for settings
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === ',') {
                e.preventDefault();
                this.toggleSettingsPanel();
            }
        });
    }

    /**
     * Toggle settings panel visibility
     */
    toggleSettingsPanel() {
        if (this.isOpen) {
            this.closeSettingsPanel();
        } else {
            this.openSettingsPanel();
        }
    }

    /**
     * Open settings panel
     */
    openSettingsPanel() {
        this.settingsPanel.classList.remove('hidden');
        this.isOpen = true;
        document.body.classList.add('settings-open');
        
        // Focus first input for accessibility
        const firstInput = this.settingsPanel.querySelector('input, select, button');
        if (firstInput) firstInput.focus();
    }

    /**
     * Close settings panel
     */
    closeSettingsPanel() {
        this.settingsPanel.classList.add('hidden');
        this.isOpen = false;
        document.body.classList.remove('settings-open');
        
        // Return focus to settings button
        document.querySelector('#settingsToggle')?.focus();
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        // Update tab buttons
        this.settingsPanel.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        
        // Update tab content
        this.settingsPanel.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.dataset.tab === tabName);
        });
    }

    /**
     * Update volume display for sliders
     */
    updateVolumeDisplay(slider) {
        const valueSpan = slider.parentNode.querySelector('.volume-value');
        if (valueSpan) {
            valueSpan.textContent = Math.round(slider.value * 100) + '%';
        }
    }

    /**
     * Get input value based on type
     */
    getInputValue(input) {
        if (input.type === 'checkbox') {
            return input.checked;
        } else if (input.type === 'range' || input.type === 'number') {
            return parseFloat(input.value);
        } else {
            return input.value;
        }
    }

    /**
     * Update individual setting
     */
    updateSetting(name, value) {
        this.settings[name] = value;
        this.applySettings();
    }

    /**
     * Apply current settings to the game
     */
    applySettings() {
        // Apply theme
        document.documentElement.setAttribute('data-theme', this.settings.theme);
        
        // Apply font size
        document.documentElement.setAttribute('data-font-size', this.settings.fontSize);
        
        // Apply accessibility settings
        document.documentElement.classList.toggle('high-contrast', this.settings.highContrast);
        document.documentElement.classList.toggle('large-text', this.settings.largeText);
        document.documentElement.classList.toggle('reduced-motion', this.settings.reducedMotion);
        document.documentElement.classList.toggle('keyboard-nav', this.settings.keyboardNav);
        
        // Apply animations
        if (!this.settings.animations || this.settings.reducedMotion) {
            document.documentElement.classList.add('no-animations');
        } else {
            document.documentElement.classList.remove('no-animations');
        }
        
        // Emit settings change event
        window.dispatchEvent(new CustomEvent('settingsChanged', { 
            detail: this.settings 
        }));
    }

    /**
     * Reset to default settings
     */
    resetSettings() {
        if (confirm('Reset all settings to defaults? This cannot be undone.')) {
            this.settings = this.getDefaultSettings();
            this.updateSettingsUI();
            this.applySettings();
            this.showNotification('Settings reset to defaults', 'info');
        }
    }

    /**
     * Update settings UI with current values
     */
    updateSettingsUI() {
        Object.keys(this.settings).forEach(key => {
            const input = this.settingsPanel.querySelector(`[name="${key}"]`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = this.settings[key];
                } else {
                    input.value = this.settings[key];
                }
                
                // Update volume displays
                if (input.type === 'range') {
                    this.updateVolumeDisplay(input);
                }
            }
        });
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Get current settings
     */
    getSettings() {
        return { ...this.settings };
    }

    /**
     * Get specific setting value
     */
    getSetting(key) {
        return this.settings[key];
    }

    /**
     * Set specific setting value
     */
    setSetting(key, value) {
        this.settings[key] = value;
        this.applySettings();
    }
}

// Initialize settings when DOM is ready
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        window.gameSettings = new GameSettings();
    });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GameSettings;
} 