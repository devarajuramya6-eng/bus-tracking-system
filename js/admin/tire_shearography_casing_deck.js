/**
 * CityBus Enterprise Platform - Tire Casing Laser Shearography Inspection Deck
 * File: js/admin/tire_shearography_casing_deck.js
 * 
 * Displays 3D laser interferometric shearography results on 295/80R22.5 tire casings:
 * - Subsurface belt separation detection
 * - Retread qualification pass/fail audit
 */

class CityBusTireShearographyDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.casings = [
      { serial: 'MICH-295-8941', retreadCount: 1, anomalies: 0, status: 'APPROVED', result: 'Ready for Cold Buffer & Tread Ring' },
      { serial: 'APOL-295-3210', retreadCount: 2, anomalies: 1, status: 'REJECTED', result: 'Subsurface Crown Belt Separation (12mm)' },
      { serial: 'JK-295-4491', retreadCount: 0, anomalies: 0, status: 'APPROVED', result: 'Virgin Casing Sound - 1st Retread' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Tire Casing Laser Shearography NDT Terminal</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Vacuum Interferogram Subsurface Defect Analysis</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Laser Shearography Scanner Ready for Casing Mount.')">🔬 New Laser Scan</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">TIRE CASING SERIAL</th>
                <th style="padding: 0.75rem;">PAST RETREADS</th>
                <th style="padding: 0.75rem;">DEFECT ANOMALIES</th>
                <th style="padding: 0.75rem;">QUALIFICATION</th>
                <th style="padding: 0.75rem;">DISPOSITION</th>
              </tr>
            </thead>
            <tbody>
              ${this.casings.map(c => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-family: monospace; font-weight: 700; color: var(--cb-brand-primary);">${c.serial}</td>
                  <td style="padding: 0.75rem;">${c.retreadCount} / 3 Max</td>
                  <td style="padding: 0.75rem; font-weight: 700; color: ${c.anomalies > 0 ? 'var(--cb-status-danger)' : 'var(--cb-status-success)'};">${c.anomalies}</td>
                  <td style="padding: 0.75rem;"><span class="badge ${c.status === 'APPROVED' ? 'badge-success' : 'badge-danger'}">${c.status}</span></td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">${c.result}</td>
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
window.CityBusTireShearographyDeck = CityBusTireShearographyDeck;
