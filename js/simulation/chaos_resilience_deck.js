/**
 * CityBus Enterprise Platform - Disaster Recovery & Chaos Resilience Deck
 * File: js/simulation/chaos_resilience_deck.js
 * 
 * Provides disaster simulation controls and failover management:
 * - Monsoon Flood Bridge Submersion (Prakasam Barrage)
 * - 100% Depot Grid Blackout (Diesel Genset Failover)
 * - Cellular Tower Outage (V2V Mesh Relay)
 */

class CityBusChaosResilienceDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.scenarios = [
      { id: 'SCEN_FLOOD', name: 'Krishna River Flood (Prakasam Barrage Submersion)', impact: 'Reroutes 14 Buses via Flyover (+4.8 km)', status: 'STANDBY' },
      { id: 'SCEN_BLACKOUT', name: 'Main Depot 100% Electrical Grid Blackout', impact: 'Switches OCC to 500kVA Genset & Microgrid', status: 'STANDBY' },
      { id: 'SCEN_CELL_OUTAGE', name: 'Citywide 4G/5G Cellular Tower Outage', impact: 'Activates V2V Short-Range Wi-Fi Mesh Relay', status: 'STANDBY' }
    ];
    this.render();
  }

  injectChaos(id) {
    alert(`🚨 CHAOS INJECTED: Protocol ${id} triggered. Emergency response failovers active.`);
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Disaster Chaos Engineering & Emergency Resilience Hub</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Contingency Simulations & Automated Infrastructure Failovers</p>
          </div>
          <span class="badge badge-success">🛡️ Failover Systems Armed</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem;">
          ${this.scenarios.map(s => `
            <div class="card" style="padding: 1.25rem; border-left: 4px solid var(--cb-status-danger);">
              <div style="font-weight: 800; font-size: 0.95rem; color: var(--cb-text-primary); margin-bottom: 0.5rem;">${s.name}</div>
              <div style="font-size: 0.85rem; color: var(--cb-text-muted); margin-bottom: 1rem;">${s.impact}</div>
              <button class="btn btn-sm btn-danger" style="width: 100%;" onclick="window.chaosResilienceInstance.injectChaos('${s.id}')">
                ⚠️ Inject Disaster Scenario
              </button>
            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusChaosResilienceDeck = CityBusChaosResilienceDeck;
