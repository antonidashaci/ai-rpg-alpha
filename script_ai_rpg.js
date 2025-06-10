// ======== AI RPG DEMO GAME STARTER ========
// Enhanced with Phase 4: Advanced UI & User Experience

document.addEventListener("DOMContentLoaded", function () {
  // Get the play area
  const playArea = document.getElementById("play");
  if (!playArea) return;

  // Phase 4: Game state management
  let gameState = {
    currentQuest: 0,
    playerName: '',
    playerStats: {
      health: 100,
      experience: 0,
      level: 1
    },
    gameStarted: false
  };

  // Render "Play Demo" UI with Phase 4 enhancements
  function renderStarter() {
    playArea.innerHTML = `
      <div class="glass animate-fade-in-up" style="text-align:center; max-width:400px; margin:2rem auto;">
        <h2 style="font-size:1.3rem; margin-bottom:1.2rem;">🎮 Start Your Adventure</h2>
        <div class="form-group" style="margin-bottom:1.5rem;">
          <input id="playerName" 
                 placeholder="Enter your hero name..." 
                 style="padding:0.5em 1em; border-radius:1em; border:none; margin-bottom:1em; width:80%; transition: all 0.3s ease;" 
                 maxlength="20"
                 aria-label="Player name input"
                 onkeypress="handleNameKeypress(event)" />
          <div id="nameError" style="color: var(--clr-error); font-size: 0.8rem; display: none;"></div>
        </div>
        <button id="startBtn" 
                class="cta-btn transition-all" 
                style="padding:0.7em 2em; border-radius:1em; background:var(--clr-primary); color:white; font-weight:600; border:none;"
                disabled>
          Start Adventure
        </button>
      </div>
      <div id="gamePanel"></div>
    `;
    
    // Phase 4: Enhanced event bindings
    const nameInput = document.getElementById("playerName");
    const startBtn = document.getElementById("startBtn");
    
    nameInput.addEventListener('input', validatePlayerName);
    nameInput.addEventListener('focus', () => {
      nameInput.style.borderColor = 'var(--clr-primary)';
      nameInput.style.boxShadow = '0 0 0 3px rgba(157, 125, 255, 0.2)';
    });
    nameInput.addEventListener('blur', () => {
      nameInput.style.borderColor = '';
      nameInput.style.boxShadow = '';
    });
    
    startBtn.onclick = startGame;
    
    // Auto-focus name input for better UX
    setTimeout(() => nameInput.focus(), 500);
  }

  // Phase 4: Enhanced player name validation
  function validatePlayerName() {
    const nameInput = document.getElementById("playerName");
    const startBtn = document.getElementById("startBtn");
    const errorDiv = document.getElementById("nameError");
    const name = nameInput.value.trim();
    
    if (name.length === 0) {
      startBtn.disabled = true;
      errorDiv.style.display = 'none';
      return false;
    }
    
    if (name.length < 2) {
      startBtn.disabled = true;
      errorDiv.textContent = 'Name must be at least 2 characters';
      errorDiv.style.display = 'block';
      return false;
    }
    
    if (name.length > 20) {
      startBtn.disabled = true;
      errorDiv.textContent = 'Name must be 20 characters or less';
      errorDiv.style.display = 'block';
      return false;
    }
    
    // Valid name
    startBtn.disabled = false;
    errorDiv.style.display = 'none';
    return true;
  }

  // Phase 4: Handle enter key in name input
  window.handleNameKeypress = function(event) {
    if (event.key === 'Enter') {
      const startBtn = document.getElementById("startBtn");
      if (!startBtn.disabled) {
        startBtn.click();
      }
    }
  };

  // Enhanced quest data with Phase 4 features
  const quests = [
    {
      id: "intro_forest",
      title: "Awakening in the Misty Forest",
      intro: "You wake up in a foggy, ancient woodland. Shadows flicker between twisted trees. What do you do?",
      location: "forest",
      riskLevel: "low",
      choices: [
        { 
          text: "Investigate the strange noise", 
          result: "You creep toward the sound, heart pounding. Through the mist, you discover an old hermit gathering herbs.",
          consequences: { experience: 10, health: -5 },
          nextQuest: 1
        },
        { 
          text: "Climb a tree to get your bearings", 
          result: "You scale a mossy trunk and glimpse a ruined tower in the distance. The view reveals a path through the forest.",
          consequences: { experience: 15 },
          nextQuest: 1
        },
        { 
          text: "Call out for help", 
          result: "Your voice echoes through the forest. Only crows answer from above, but their cawing seems to form a pattern...",
          consequences: { experience: 5, health: -10 },
          nextQuest: 1
        },
      ]
    },
    {
      id: "forest_path",
      title: "The Hermit's Wisdom",
      intro: "The old hermit looks at you with knowing eyes. 'Lost traveler, the forest tests all who enter. Choose your path wisely.'",
      location: "forest",
      riskLevel: "medium",
      choices: [
        { 
          text: "Ask about the ruined tower", 
          result: "The hermit nods gravely. 'Ancient magic dwells there. Many seek its secrets, few return unchanged.'",
          consequences: { experience: 20 },
          nextQuest: null
        },
        { 
          text: "Request guidance out of the forest", 
          result: "With a gentle smile, the hermit points to a hidden trail. 'This path leads to safety, but also to ordinary destiny.'",
          consequences: { experience: 10, health: 20 },
          nextQuest: null
        },
        { 
          text: "Offer to help the hermit", 
          result: "The hermit's eyes brighten. 'A kind heart is rare. Take this healing potion as thanks.'",
          consequences: { experience: 25, health: 30 },
          nextQuest: null
        },
      ]
    }
  ];

  // Phase 4: Enhanced start game with loading states
  function startGame() {
    const nameInput = document.getElementById("playerName");
    const startBtn = document.getElementById("startBtn");
    
    if (!validatePlayerName()) {
      // Shake animation for invalid input
      nameInput.classList.add('animate-shake');
      setTimeout(() => nameInput.classList.remove('animate-shake'), 500);
      
      // Play error sound
      if (window.audioSystem) {
        window.audioSystem.playSFX('error');
      }
      return;
    }

    const playerName = nameInput.value.trim();
    
    // Show loading state
    if (window.gameUI) {
      window.gameUI.addLoadingState(startBtn, 'Starting...');
    }

    // Play success sound
    if (window.audioSystem) {
      window.audioSystem.playSFX('success');
      window.audioSystem.setMusicForGameState('exploration');
    }

    // Update game state
    gameState.playerName = playerName;
    gameState.gameStarted = true;
    gameState.currentQuest = 0;

    // Show loading for better UX
    setTimeout(() => {
      renderQuest(playerName, gameState.currentQuest);
      
      // Show welcome notification
      if (window.gameUI) {
        window.gameUI.showNotification(`Welcome, ${playerName}! Your adventure begins...`, 'success');
      }
    }, 800);
  }

  // Phase 4: Enhanced quest rendering with animations
  function renderQuest(playerName, questIdx) {
    if (questIdx >= quests.length || questIdx < 0) {
      renderGameEnd();
      return;
    }

    const q = quests[questIdx];
    const panel = document.getElementById("gamePanel");
    
    // Update music based on location
    if (window.audioSystem) {
      window.audioSystem.setMusicForGameState('exploration');
    }

    panel.innerHTML = `
      <div class="glass animate-fade-in-up" style="margin-top:2rem; text-align:left;">
        <div class="quest-header" style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <h3 style="color:var(--clr-accent); margin-bottom:0.5rem;">${q.title}</h3>
          <div class="quest-meta" style="display: flex; gap: 1rem; font-size: 0.8rem; color: var(--clr-text); opacity: 0.7;">
            <span>📍 ${q.location}</span>
            <span>⚠️ Risk: ${q.riskLevel}</span>
            <span>💫 ${gameState.playerStats.experience} XP</span>
            <span>❤️ ${gameState.playerStats.health} HP</span>
          </div>
        </div>
        <div class="narrative-text" style="margin-bottom:1.4em; line-height: 1.6;">
          ${q.intro.replace("You", `<strong style="color: var(--clr-primary);">${playerName}</strong>`)}
        </div>
        <div id="choices" class="choices"></div>
      </div>
    `;
    
    // Phase 4: Animated choice rendering
    const choicesDiv = document.getElementById("choices");
    q.choices.forEach((choice, idx) => {
      const btn = document.createElement("button");
      btn.innerHTML = `
        <div style="font-weight: 600; margin-bottom: 0.3rem;">${choice.text}</div>
        ${choice.consequences ? generateConsequencePreview(choice.consequences) : ''}
      `;
      btn.className = "choice-btn transition-all";
      btn.style.cssText = `
        margin: 0.5em 0; 
        padding: 1em 1.5em; 
        border-radius: 1em; 
        background: var(--clr-surface); 
        color: var(--clr-text); 
        border: 1px solid var(--clr-primary); 
        font-weight: 600; 
        cursor: pointer; 
        width: 100%;
        text-align: left;
        opacity: 0;
        transform: translateX(-20px);
      `;
      
      // Add hover sound effect
      btn.addEventListener('mouseenter', () => {
        if (window.audioSystem) {
          window.audioSystem.playSFX('click');
        }
      });
      
      btn.onclick = () => showResult(choice, questIdx);
      choicesDiv.appendChild(btn);
      
      // Staggered animation
      setTimeout(() => {
        btn.style.opacity = '1';
        btn.style.transform = 'translateX(0)';
      }, idx * 100);
    });
  }

  // Phase 4: Generate consequence preview
  function generateConsequencePreview(consequences) {
    const previews = [];
    if (consequences.experience) {
      previews.push(`<span style="color: var(--clr-primary);">+${consequences.experience} XP</span>`);
    }
    if (consequences.health > 0) {
      previews.push(`<span style="color: var(--clr-success);">+${consequences.health} HP</span>`);
    } else if (consequences.health < 0) {
      previews.push(`<span style="color: var(--clr-warning);">${consequences.health} HP</span>`);
    }
    
    return previews.length > 0 ? 
      `<div style="font-size: 0.8rem; opacity: 0.8;">${previews.join(' ')}</div>` : '';
  }

  // Phase 4: Enhanced result showing with consequences
  function showResult(choice, currentQuestIdx) {
    const panel = document.getElementById("gamePanel");
    
    // Apply consequences to game state
    if (choice.consequences) {
      if (choice.consequences.experience) {
        gameState.playerStats.experience += choice.consequences.experience;
        
        // Level up check
        const newLevel = Math.floor(gameState.playerStats.experience / 50) + 1;
        if (newLevel > gameState.playerStats.level) {
          gameState.playerStats.level = newLevel;
          gameState.playerStats.health += 20; // Level up bonus
          
          if (window.gameUI) {
            window.gameUI.showNotification(`Level Up! You are now level ${newLevel}!`, 'success');
          }
          
          if (window.audioSystem) {
            window.audioSystem.playSFX('success');
          }
        }
      }
      
      if (choice.consequences.health) {
        gameState.playerStats.health = Math.max(0, 
          Math.min(100, gameState.playerStats.health + choice.consequences.health)
        );
      }
    }

    // Play appropriate sound
    if (window.audioSystem) {
      if (choice.consequences?.health && choice.consequences.health < 0) {
        window.audioSystem.playSFX('error');
      } else {
        window.audioSystem.playSFX('success');
      }
    }

    panel.innerHTML = `
      <div class="glass animate-fade-in" style="margin-top:2rem; text-align:left;">
        <div class="result-header" style="margin-bottom: 1rem;">
          <div class="player-stats" style="display: flex; gap: 1rem; font-size: 0.9rem; margin-bottom: 1rem;">
            <span>Level ${gameState.playerStats.level}</span>
            <span style="color: var(--clr-primary);">${gameState.playerStats.experience} XP</span>
            <span style="color: ${gameState.playerStats.health > 50 ? 'var(--clr-success)' : 'var(--clr-warning)'};">
              ${gameState.playerStats.health} HP
            </span>
          </div>
        </div>
        <div class="narrative-text animate-fade-in-up" style="margin-bottom:1.4em; font-size:1.1em; line-height: 1.6;">
          ${choice.result}
        </div>
        <div class="action-buttons" style="display: flex; gap: 1rem; flex-wrap: wrap;">
          ${choice.nextQuest !== null ? 
            `<button class="cta-btn transition-all" onclick="continueQuest(${choice.nextQuest})" style="margin-top:1em;">
              Continue Adventure
            </button>` : ''
          }
          <button class="cta-btn transition-all" onclick="location.reload()" style="margin-top:1em; background: var(--clr-accent);">
            Start New Adventure
          </button>
        </div>
      </div>
    `;
  }

  // Phase 4: Continue to next quest
  window.continueQuest = function(nextQuestIdx) {
    if (window.audioSystem) {
      window.audioSystem.playSFX('click');
    }
    
    gameState.currentQuest = nextQuestIdx;
    renderQuest(gameState.playerName, nextQuestIdx);
  };

  // Phase 4: Game end screen
  function renderGameEnd() {
    const panel = document.getElementById("gamePanel");
    
    if (window.audioSystem) {
      window.audioSystem.setMusicForGameState('victory');
    }

    panel.innerHTML = `
      <div class="glass animate-fade-in-up" style="margin-top:2rem; text-align:center;">
        <h3 style="color:var(--clr-accent); margin-bottom:1rem;">🎉 Adventure Complete!</h3>
        <div style="margin-bottom:1.5rem;">
          <p>Congratulations, <strong style="color: var(--clr-primary);">${gameState.playerName}</strong>!</p>
          <p>You've completed your forest adventure.</p>
        </div>
        <div class="final-stats" style="margin-bottom:2rem; padding:1rem; background:rgba(255,255,255,0.05); border-radius:0.5rem;">
          <h4 style="margin-bottom:0.5rem;">Final Stats:</h4>
          <div style="display: flex; justify-content: center; gap: 2rem; font-size: 1.1rem;">
            <span>Level: <strong style="color: var(--clr-primary);">${gameState.playerStats.level}</strong></span>
            <span>XP: <strong style="color: var(--clr-primary);">${gameState.playerStats.experience}</strong></span>
            <span>HP: <strong style="color: var(--clr-success);">${gameState.playerStats.health}</strong></span>
          </div>
        </div>
        <button class="cta-btn transition-all animate-pulse" onclick="location.reload()" style="margin-top:1em;">
          Start New Adventure
        </button>
      </div>
    `;

    if (window.gameUI) {
      window.gameUI.showNotification('Adventure completed! Well done!', 'success', 5000);
    }
  }

  // Phase 4: Enhanced error handling
  window.addEventListener('error', (event) => {
    console.error('Game error:', event.error);
    if (window.gameUI) {
      window.gameUI.showNotification('An error occurred. Please refresh the page.', 'error');
    }
  });

  // Phase 4: Auto-save functionality
  function autoSave() {
    if (gameState.gameStarted) {
      try {
        localStorage.setItem('aiRpgGameState', JSON.stringify(gameState));
      } catch (error) {
        console.warn('Failed to auto-save:', error);
      }
    }
  }

  // Phase 4: Load saved game
  function loadSavedGame() {
    try {
      const saved = localStorage.getItem('aiRpgGameState');
      if (saved) {
        const savedState = JSON.parse(saved);
        if (savedState.gameStarted) {
          gameState = savedState;
          renderQuest(gameState.playerName, gameState.currentQuest);
          
          if (window.gameUI) {
            window.gameUI.showNotification(`Welcome back, ${gameState.playerName}!`, 'info');
          }
          return true;
        }
      }
    } catch (error) {
      console.warn('Failed to load saved game:', error);
    }
    return false;
  }

  // Auto-save every 30 seconds
  setInterval(autoSave, 30000);

  // Initialize the game
  function initializeGame() {
    // Try to load saved game first
    if (!loadSavedGame()) {
      // No saved game, show starter UI
      renderStarter();
    }
    
    // Show initial notification
    setTimeout(() => {
      if (window.gameUI && !gameState.gameStarted) {
        window.gameUI.showNotification('Welcome to AI-RPG Alpha! Try the settings ⚙️', 'info', 4000);
      }
    }, 2000);
  }

  // Start the game
  initializeGame();
});
