/**
 * CityBus Enterprise Platform - Chassis Strain Gauge & Fatigue Life Deck
 * File: js/admin/chassis_fatigue_strain_deck.js
 * 
 * Displays structural health monitoring (SHM) from onboard chassis strain gauges:
 * - Microstrain (ue) & mechanical stress (MPa) vs Yield Strength
 * - ASTM E1049 Rainflow cumulative fatigue damage index (D)
 */

class CityBusChassisFatigueDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.sensors = [
      { location: 'Front Axle Crossmember', microstrain: 480.0, stressMpa: 100.8, yieldRatio: '28.4%', fatigueDamage: '0.042', status: 'HEALTHY' },
      { location: 'Mid-Chassis Longitudinal Beam', microstrain: 620.0, stressMpa: 130.2, yieldRatio: '36.7%', fatigueDamage: '0.088', status: 'HEALTHY' },
      { location: 'Rear Suspension Hanger', microstrain: 890.0, stressMpa: 186.9, yieldRatio: '52.6%', fatigueDamage: '0.145', status: 'HEALTHY' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Chassis Structural Strain & Fatigue Life Radar</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">ASTM E1049 Rainflow Cycle Counting & Weld Integrity Monitoring</p>
          </div>
          <span class="badge badge-success">● Structural SHM Nominal</span>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">SENSOR LOCATION</th>
                <th style="padding: 0.75rem;">MICROSTRAIN (με)</th>
                <th style="padding: 0.75rem;">STRESS (MPa)</th>
                <th style="padding: 0.75rem;">% OF YIELD (355 MPa)</th>
                <th style="padding: 0.75rem;">MINER FATIGUE (D)</th>
                <th style="padding: 0.75rem;">INTEGRITY</th>
              </tr>
            </thead>
            <tbody>
              ${this.sensors.map(s => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${s.location}</td>
                  <td style="padding: 0.75rem; font-family: monospace;">${s.microstrain} με</td>
                  <td style="padding: 0.75rem; font-weight: 700;">${s.stressMpa} MPa</td>
                  <td style="padding: 0.75rem;">${s.yieldRatio}</td>
                  <td style="padding: 0.75rem; font-family: monospace; color: var(--cb-status-info);">${s.fatigueDamage}</td>
                  <td style="padding: 0.75rem;">
                    <span class="badge badge-success">${s.status}</span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusChassisFatigueDeck = CityBusChassisFatigueDeck;
