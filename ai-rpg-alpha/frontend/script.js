// ======== AI RPG DEMO GAME STARTER ========

document.addEventListener("DOMContentLoaded", function () {
  // Get the play area
  const playArea = document.getElementById("play");
  if (!playArea) return;

  // Render "Play Demo" UI
  function renderStarter() {
    playArea.innerHTML = `
      <div class="glass" style="text-align:center; max-width:400px; margin:2rem auto;">
        <h2 style="font-size:1.3rem; margin-bottom:1.2rem;">🎮 Start Your Adventure</h2>
        <input id="playerName" placeholder="Enter your hero name..." style="padding:0.5em 1em; border-radius:1em; border:none; margin-bottom:1em; width:80%;" />
        <br>
        <button id="startBtn" style="padding:0.7em 2em; border-radius:1em; background:var(--clr-primary); color:white; font-weight:600; border:none;">Start</button>
      </div>
      <div id="gamePanel"></div>
    `;
    document.getElementById("startBtn").onclick = startGame;
  }

  // Dummy quest data (replace with fetch to API for live backend)
  const quests = [
    {
      id: "intro_forest",
      title: "Awakening in the Misty Forest",
      intro: "You wake up in a foggy, ancient woodland. Shadows flicker between twisted trees. What do you do?",
      choices: [
        { text: "Investigate the strange noise", result: "You creep toward the sound, heart pounding..." },
        { text: "Climb a tree to get your bearings", result: "You scale a mossy trunk and glimpse a ruined tower in the distance." },
        { text: "Call out for help", result: "Your voice echoes... but only crows answer from above." },
      ]
    },
    // Add more sample quests as you wish!
  ];

  let currentQuest = 0;

  function startGame() {
    const playerName = document.getElementById("playerName").value.trim();
    if (!playerName) {
      alert("Please enter a name to begin!");
      return;
    }
    renderQuest(playerName, currentQuest);
  }

  function renderQuest(playerName, questIdx) {
    const q = quests[questIdx];
    const panel = document.getElementById("gamePanel");
    panel.innerHTML = `
      <div class="glass" style="margin-top:2rem; text-align:left;">
        <h3 style="color:var(--clr-accent); margin-bottom:1em;">${q.title}</h3>
        <div style="margin-bottom:1.4em;">${q.intro.replace("You", `<strong>${playerName}</strong>`)}</div>
        <div id="choices"></div>
      </div>
    `;
    const choicesDiv = document.getElementById("choices");
    q.choices.forEach((choice, idx) => {
      const btn = document.createElement("button");
      btn.innerText = choice.text;
      btn.className = "choice-btn";
      btn.style.cssText = "margin:0.5em 0.5em 0 0; padding:0.7em 1.5em; border-radius:1em; background:var(--clr-surface); color:var(--clr-text); border:1px solid var(--clr-primary); font-weight:600; cursor:pointer; transition:background 0.2s;";
      btn.onclick = () => showResult(choice.result);
      choicesDiv.appendChild(btn);
    });
  }

  function showResult(resultText) {
    const panel = document.getElementById("gamePanel");
    panel.innerHTML = `
      <div class="glass" style="margin-top:2rem; text-align:left;">
        <div style="margin-bottom:1.4em; font-size:1.2em;">${resultText}</div>
        <button class="cta-btn" style="margin-top:2em;" onclick="location.reload()">Restart Demo</button>
      </div>
    `;
  }

  // Initialize the starter UI
  renderStarter();
});
