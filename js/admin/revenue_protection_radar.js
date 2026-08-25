/**
 * CityBus Enterprise Platform - Revenue Protection & Fare Evasion Radar
 * File: js/admin/revenue_protection_radar.js
 * 
 * Displays real-time fare evasion hotspots and flying-squad inspection deployments:
 * - Compares physical APC door entries vs NFC/QR ticket validations
 * - Flags unvalidated boarding corridors and revenue leakage rates
 */

class CityBusRevenueProtectionRadar {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.evasionHotspots = [
      { route: 'Route 5K (Kaleswara Rao ➔ Autonagar)', stop: 'Ramavarappadu Ring', apcEntries: 42, ticketValidations: 31, leakageRate: '26.2%', status: 'HIGH_RISK_SURGE' },
      { route: 'Route 27A (PNBS ➔ Guntur)', stop: 'Benz Circle Corridor', apcEntries: 65, ticketValidations: 62, leakageRate: '4.6%', status: 'NOMINAL' },
      { route: 'Route 10 (City Loop)', stop: 'Railway Station East Gate', apcEntries: 38, ticketValidations: 29, leakageRate: '23.7%', status: 'HIGH_RISK_SURGE' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Revenue Protection & Fare Evasion Radar</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">APC Door Sensors vs Contactless Ticket Validations Discrepancy</p>
          </div>
          <button class="btn btn-danger" onclick="alert('Flying Squad Inspector Unit 3 dispatched to Ramavarappadu Ring!')">🚨 Dispatch Flying Squad</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">ROUTE</th>
                <th style="padding: 0.75rem;">STATION / CORRIDOR</th>
                <th style="padding: 0.75rem;">APC ENTRIES</th>
                <th style="padding: 0.75rem;">PAID TICKETS</th>
                <th style="padding: 0.75rem;">LEAKAGE RATE</th>
                <th style="padding: 0.75rem;">STATUS</th>
                <th style="padding: 0.75rem;">ACTION</th>
              </tr>
            </thead>
            <tbody>
              ${this.evasionHotspots.map(h => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${h.route}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${h.stop}</td>
                  <td style="padding: 0.75rem;">${h.apcEntries} boarded</td>
                  <td style="padding: 0.75rem; font-weight: 700;">${h.ticketValidations} validated</td>
                  <td style="padding: 0.75rem; font-weight: 800; color: ${h.status.includes('HIGH') ? 'var(--cb-status-danger)' : 'var(--cb-status-success)'};">${h.leakageRate}</td>
                  <td style="padding: 0.75rem;"><span class="badge ${h.status.includes('HIGH') ? 'badge-danger' : 'badge-success'}">${h.status}</span></td>
                  <td style="padding: 0.75rem;">
                    <button class="btn btn-sm btn-outline-danger" onclick="alert('Inspection checkpoint activated for ${h.stop}')">Intercept</button>
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
window.CityBusRevenueProtectionRadar = CityBusRevenueProtectionRadar;
