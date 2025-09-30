class MinesGame {
  constructor() {
    this.currentGameId = null;
    this.userBalance = 1000;
    this.isGameActive = false;
    this.gridSize = 25;

    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.loadUserStatus();
    this.showLoading(false);
  }

  setupEventListeners() {
    document
      .getElementById("startGameBtn")
      .addEventListener("click", () => this.startGame());
    document
      .getElementById("newGameBtn")
      .addEventListener("click", () => this.showSetup());
    document
      .getElementById("cashOutBtn")
      .addEventListener("click", () => this.cashOut());
    document
      .getElementById("playAgainBtn")
      .addEventListener("click", () => this.closeModal());

    const betInput = document.getElementById("betAmount");
    betInput.addEventListener("input", () => this.validateBet());
    betInput.addEventListener("change", () => this.validateBet());
  }

  async loadUserStatus() {
    try {
      this.showLoading(true);
      const response = await fetch("/status", {
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        this.userBalance = data.balance;
        this.updateBalance();
      } else {
        this.showMessage("Failed to load user status", "error");
      }
    } catch (error) {
      console.error("Error loading status:", error);
      this.showMessage("Connection error", "error");
    } finally {
      this.showLoading(false);
    }
  }

  validateBet() {
    const betInput = document.getElementById("betAmount");
    const betAmount = parseInt(betInput.value);
    const startBtn = document.getElementById("startGameBtn");

    if (betAmount < 1) {
      betInput.value = 1;
    } else if (betAmount > this.userBalance) {
      betInput.value = this.userBalance;
    }

    startBtn.disabled = betAmount < 1 || betAmount > this.userBalance;
  }

  async startGame() {
    const betAmount = parseInt(document.getElementById("betAmount").value);

    if (betAmount < 1 || betAmount > this.userBalance) {
      this.showMessage("Invalid bet amount", "error");
      return;
    }

    try {
      this.showLoading(true);
      const response = await fetch("/start_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ bet_amount: betAmount }),
      });

      if (response.ok) {
        const data = await response.json();
        this.currentGameId = data.game_id;
        this.userBalance = data.balance;
        this.isGameActive = true;

        this.showGameBoard(data);
        this.createGrid();
        this.updateStats(data);
        this.showMessage("Click tiles to reveal. Avoid mines!");
      } else {
        const error = await response.json();
        this.showMessage(error.error || "Failed to start game", "error");
      }
    } catch (error) {
      console.error("Error starting game:", error);
      this.showMessage("Connection error", "error");
    } finally {
      this.showLoading(false);
    }
  }

  showGameBoard(data) {
    document.getElementById("gameSetup").style.display = "none";
    document.getElementById("gameBoardSection").style.display = "flex";
    document.getElementById("currentBet").textContent = `$${data.bet_amount}`;

    // Display server time (seed)
    if (data.server_time) {
      document.getElementById("serverTime").textContent = data.server_time;
    }

    this.updateBalance();
  }

  showSetup() {
    document.getElementById("gameBoardSection").style.display = "none";
    document.getElementById("gameSetup").style.display = "flex";
    this.currentGameId = null;
    this.isGameActive = false;

    // Reset server time display
    document.getElementById("serverTime").textContent = "-";

    this.validateBet();
  }

  createGrid() {
    const gameBoard = document.getElementById("gameBoard");
    gameBoard.innerHTML = '<div class="grid" id="grid"></div>';

    const grid = document.getElementById("grid");

    for (let i = 0; i < this.gridSize; i++) {
      const tile = document.createElement("div");
      tile.className = "tile";
      tile.dataset.position = i;
      tile.addEventListener("click", () => this.revealTile(i));
      grid.appendChild(tile);
    }
  }

  async revealTile(position) {
    if (!this.isGameActive || !this.currentGameId) return;

    const tile = document.querySelector(`[data-position="${position}"]`);
    if (tile.classList.contains("revealed")) return;

    try {
      tile.classList.add("disabled");

      const response = await fetch("/api/reveal-tile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          game_id: this.currentGameId,
          position: position,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        this.handleReveal(data, tile);
      } else {
        const error = await response.json();
        this.showMessage(error.error || "Failed to reveal tile", "error");
        tile.classList.remove("disabled");
      }
    } catch (error) {
      console.error("Error revealing tile:", error);
      this.showMessage("Connection error", "error");
      tile.classList.remove("disabled");
    }
  }

  handleReveal(data, tile) {
    tile.classList.remove("disabled");
    tile.classList.add("revealed", "reveal");

    if (data.success) {
      tile.classList.add("safe");
      tile.innerHTML = '<span class="emoji">✓</span>';

      this.updateStats({
        safe_tiles_found: data.safe_tiles_found,
        current_multiplier: data.current_multiplier,
        potential_payout: data.potential_payout,
      });

      this.showMessage("Safe! Continue or cash out?", "success");
    } else {
      tile.classList.add("mine", "explode");
      tile.innerHTML = '<span class="emoji">💣</span>';

      this.isGameActive = false;
      this.disableAllTiles();

      if (data.mines_revealed) {
        setTimeout(() => this.revealMines(data.mines_revealed), 300);
      }

      setTimeout(() => this.showGameOverModal(false, data), 1000);
    }
  }

  revealMines(positions) {
    positions.forEach((pos) => {
      const tile = document.querySelector(`[data-position="${pos}"]`);
      if (tile && !tile.classList.contains("revealed")) {
        tile.classList.add("revealed", "mine");
        tile.innerHTML = '<span class="emoji">💣</span>';
      }
    });
  }

  disableAllTiles() {
    document.querySelectorAll(".tile:not(.revealed)").forEach((tile) => {
      tile.classList.add("disabled");
    });
  }

  async cashOut() {
    if (!this.isGameActive || !this.currentGameId) return;

    try {
      this.showLoading(true);
      const response = await fetch("/api/cash-out", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ game_id: this.currentGameId }),
      });

      if (response.ok) {
        const data = await response.json();
        this.userBalance = data.new_balance;
        this.isGameActive = false;
        this.disableAllTiles();
        this.showGameOverModal(true, data);
      } else {
        const error = await response.json();
        this.showMessage(error.error || "Failed to cash out", "error");
      }
    } catch (error) {
      console.error("Error cashing out:", error);
      this.showMessage("Connection error", "error");
    } finally {
      this.showLoading(false);
    }
  }

  updateStats(data) {
    if (data.safe_tiles_found !== undefined) {
      document.getElementById("safeTilesCount").textContent =
        data.safe_tiles_found;
    }
    if (data.current_multiplier !== undefined) {
      document.getElementById(
        "currentMultiplier"
      ).textContent = `${data.current_multiplier.toFixed(2)}x`;
    }
    if (data.potential_payout !== undefined) {
      document.getElementById(
        "potentialPayout"
      ).textContent = `$${data.potential_payout}`;
    }
  }

  showGameOverModal(won, data) {
    const modal = document.getElementById("resultModal");
    const title = document.getElementById("resultTitle");
    const message = document.getElementById("resultMessage");
    const details = document.getElementById("resultDetails");

    if (won) {
      title.innerHTML = 'Winner! <span class="emoji">🎉</span>';
      title.style.color = "#00ff88";
      message.textContent = data.message || "You cashed out successfully!";
    } else {
      title.innerHTML = 'Game Over <span class="emoji">💥</span>';
      title.style.color = "#ff4444";
      message.textContent = data.message || "You hit a mine!";
    }

    details.innerHTML = "";

    if (won && data.payout) {
      details.innerHTML = `
                <div class="detail-item">
                    <span>Payout:</span>
                    <span>$${data.payout}</span>
                </div>
                <div class="detail-item">
                    <span>New Balance:</span>
                    <span>$${data.new_balance}</span>
                </div>
            `;

      if (data.flag) {
        details.innerHTML += `
                    <div class="flag-earned">
                        <span class="emoji">🚩</span> FLAG: ${data.flag}
                    </div>
                `;
      }
    }

    modal.classList.add("show");
    this.updateBalance();
  }

  closeModal() {
    document.getElementById("resultModal").classList.remove("show");
    this.showSetup();
  }

  showMessage(text, type = "") {
    const messageEl = document.getElementById("gameMessage");
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;

    setTimeout(() => {
      if (messageEl.textContent === text) {
        messageEl.textContent = "";
        messageEl.className = "message";
      }
    }, 4000);
  }

  showLoading(show) {
    const overlay = document.getElementById("loadingOverlay");
    overlay.classList.toggle("show", show);
  }

  updateBalance() {
    document.getElementById(
      "balance"
    ).textContent = `$${this.userBalance.toLocaleString()}`;

    const betInput = document.getElementById("betAmount");
    betInput.max = this.userBalance;
    this.validateBet();
  }
}

// Initialize game
document.addEventListener("DOMContentLoaded", () => {
  window.game = new MinesGame();
});

// Keyboard shortcuts
document.addEventListener("keydown", (e) => {
  if (!window.game) return;

  switch (e.key) {
    case "Enter":
      if (document.getElementById("gameSetup").style.display !== "none") {
        document.getElementById("startGameBtn").click();
      }
      break;
    case "Escape":
      if (document.getElementById("resultModal").classList.contains("show")) {
        window.game.closeModal();
      }
      break;
    case " ":
      if (window.game.isGameActive) {
        e.preventDefault();
        document.getElementById("cashOutBtn").click();
      }
      break;
  }
});
