/**
 * CityBus Enterprise Platform - GTFS-Fares V2 Fare Matrix & Product Registry
 * File: js/admin/gtfs_fares_v2_matrix.js
 * 
 * Manages GTFS-Fares V2 fare structures and multi-modal transfer policies:
 * - Single-leg products (Ordinary Non-AC, Metro Express, AC Electric Deluxe)
 * - Intermodal transfer rules (Free 60-min transfer between feeder & trunk)
 */

class CityBusGTFSFaresV2Matrix {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.products = [
      { id: 'PROD_STAGE_NON_AC', name: 'Ordinary Non-AC Single Journey', amount: 15.0, currency: 'INR', transfersAllowed: 0 },
      { id: 'PROD_METRO_EXPRESS', name: 'Metro Express Corridor Pass', amount: 25.0, currency: 'INR', transfersAllowed: 1 },
      { id: 'PROD_ELECTRIC_AC', name: 'Deluxe Electric AC Express', amount: 35.0, currency: 'INR', transfersAllowed: 1 },
      { id: 'PROD_DAY_UNLIMITED', name: '24-Hour Municipal All-Lines Pass', amount: 80.0, currency: 'INR', transfersAllowed: 99 }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">GTFS-Fares V2 Product Matrix & Transfer Rules</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">MobilityData Interoperable Fare Rules</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Exported GTFS-Fares V2 dataset (fare_products.txt, fare_leg_rules.txt).')">📦 Export GTFS-Fares V2 Zip</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">PRODUCT ID</th>
                <th style="padding: 0.75rem;">PRODUCT NAME</th>
                <th style="padding: 0.75rem;">BASE FARE</th>
                <th style="padding: 0.75rem;">TRANSFERS INCLUDED</th>
                <th style="padding: 0.75rem;">TRANSFER WINDOW</th>
                <th style="padding: 0.75rem;">STATUS</th>
              </tr>
            </thead>
            <tbody>
              ${this.products.map(p => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-family: monospace; font-weight: 700; color: var(--cb-brand-primary);">${p.id}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${p.name}</td>
                  <td style="padding: 0.75rem; font-weight: 800; color: var(--cb-text-primary);">₹${p.amount.toFixed(2)}</td>
                  <td style="padding: 0.75rem;">${p.transfersAllowed === 99 ? 'Unlimited' : p.transfersAllowed}</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">60 mins</td>
                  <td style="padding: 0.75rem;"><span class="badge badge-success">Active Tariff</span></td>
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
window.CityBusGTFSFaresV2Matrix = CityBusGTFSFaresV2Matrix;
