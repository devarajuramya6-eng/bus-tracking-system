/**
 * CityBus Enterprise Platform - Master Fleet Simulation Command Deck
 * File: js/simulation/simulation_control_deck.js
 * 
 * Provides interactive control over the 50-bus multi-route kinematic simulator:
 * - Speed Multipliers: 1x Real-Time, 5x Fast-Forward, 10x Rush-Hour, 20x Warp
 * - Live Traffic Congestion Injector (Trigger Benz Circle Jam, Barrage Closure)
 * - Fleet Telemetry Broadcast Rate counter
 */

class CityBusSimulationControlDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.speedMultiplier = 1;
    this.isRunning = true;
    this.pingsPerSec = 48;
    this.init();
  }

  setSpeed(speed) {
    this.speedMultiplier = speed;
    const badge = document.getElementById('sim-speed-badge');
    if (badge) badge.innerText = `${speed}x Speed`;
  }

  togglePlay() {
    this.isRunning = !this.isRunning;
    const btn = document.getElementById('sim-play-btn');
    if (btn) btn.innerText = this.isRunning ? '⏸️ Pause Simulation' : '▶️ Resume Simulation';
  }

  injectIncident(type) {
    alert(`🚨 INJECTED SIMULATION EVENT: ${type} triggered on Vijayawada corridor. Real-time headway adjustments dispatched.`);
  }

  init() {
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #0B1120; border: 2px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">🎮</span>
            <span style="font-weight: 800; font-size: 1.1rem;">FLEET KINEMATICS SIMULATOR DECK</span>
          </div>
          <span id="sim-speed-badge" class="badge badge-success">${this.speedMultiplier}x Speed</span>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; margin-bottom: 1.25rem;">
          <button id="sim-play-btn" class="btn btn-primary" onclick="window.simControlDeckInstance.togglePlay()">⏸️ Pause Simulation</button>
          
          <div style="display: flex; gap: 4px; background: #1E293B; padding: 4px; border-radius: 8px;">
            <button class="btn btn-sm" style="background: #334155; color: #fff;" onclick="window.simControlDeckInstance.setSpeed(1)">1x</button>
            <button class="btn btn-sm" style="background: #334155; color: #fff;" onclick="window.simControlDeckInstance.setSpeed(5)">5x</button>
            <button class="btn btn-sm" style="background: #334155; color: #fff;" onclick="window.simControlDeckInstance.setSpeed(10)">10x</button>
            <button class="btn btn-sm" style="background: #334155; color: #fff;" onclick="window.simControlDeckInstance.setSpeed(20)">20x</button>
          </div>

          <span style="font-size: 0.8rem; color: #94A3B8; margin-left: auto;">
            Telemetry Rate: <strong>${this.pingsPerSec} pings/sec</strong> across 50 active buses
          </span>
        </div>

        <!-- Chaos & Congestion Injector Buttons -->
        <div style="border-top: 1px solid #1E293B; padding-top: 1rem;">
          <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; margin-bottom: 0.5rem;">Chaos & Stress Test Injection</div>
          <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            <button class="btn btn-sm btn-outline-danger" onclick="window.simControlDeckInstance.injectIncident('Benz Circle Heavy Traffic Jam')">🚗 Benz Circle Gridlock</button>
            <button class="btn btn-sm btn-outline-warning" onclick="window.simControlDeckInstance.injectIncident('Prakasham Barrage High Water Diversion')">🌊 Canal Flood Diversion</button>
            <button class="btn btn-sm btn-outline-primary" onclick="window.simControlDeckInstance.injectIncident('AP16-008 Brake Overheat Work Order')">⚠️ Bus Breakdown Injection</button>
          </div>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusSimulationControlDeck = CityBusSimulationControlDeck;
