/**
 * CityBus Enterprise Platform - Headway Regularization & Virtual Platooning Deck
 * File: js/admin/headway_platooning_deck.js
 * 
 * Visualizes trunk corridor headway spacing, bus bunching alerts, and virtual platoons:
 * - Anti-bunching hold recommendations (seconds)
 * - V2V Virtual Platoon lock (1.5s time gap between buses)
 */

class CityBusHeadwayPlatooningDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.corridors = [
      { route: '27A (MG Road)', leadBus: 'AP16-001', trailingBus: 'AP16-002', headwayMin: 9.8, targetMin: 10.0, status: 'REGULARIZED_PERFECT', platoon: 'PLATOON_LOCKED (1.5s Gap)' },
      { route: '5K (Eluru Road)', leadBus: 'AP16-003', trailingBus: 'AP16-004', headwayMin: 4.2, targetMin: 8.0, status: 'BUNCHING_RISK', platoon: 'HOLDING_AT_BENZ_CIRCLE (45s)' },
      { route: '100E (Airport Express)', leadBus: 'AP16-008', trailingBus: 'AP16-009', headwayMin: 14.5, targetMin: 15.0, status: 'REGULARIZED_PERFECT', platoon: 'SINGLE_COACH' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Corridor Headway Regularization & Virtual Platooning</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Automated Anti-Bunching Holding Algorithms & V2V CACC Platoons</p>
          </div>
          <span class="badge badge-success">● CACC Platooning Active</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${this.corridors.map(c => `
            <div class="card" style="padding: 1.25rem; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid ${c.status.includes('BUNCHING') ? 'var(--cb-status-warning)' : 'var(--cb-status-success)'};">
              <div>
                <div style="font-weight: 800; font-size: 1.05rem; color: var(--cb-text-primary);">${c.route}</div>
                <div style="font-size: 0.85rem; color: var(--cb-text-muted); margin-top: 2px;">
                  Lead: <strong>${c.leadBus}</strong> ➔ Trailing: <strong>${c.trailingBus}</strong>
                </div>
              </div>

              <div style="text-align: right;">
                <div style="font-size: 1.2rem; font-weight: 900; color: var(--cb-brand-primary);">
                  ${c.headwayMin} min <span style="font-size: 0.75rem; color: var(--cb-text-muted); font-weight: 400;">/ Target ${c.targetMin} min</span>
                </div>
                <div style="margin-top: 4px;">
                  <span class="badge ${c.status.includes('BUNCHING') ? 'badge-warning' : 'badge-success'}">${c.status}</span>
                  <span class="badge badge-primary">${c.platoon}</span>
                </div>
              </div>
            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusHeadwayPlatooningDeck = CityBusHeadwayPlatooningDeck;
