/**
 * CityBus Enterprise Platform - Fleet Asset Lifecycle & Depreciation Deck
 * File: js/admin/asset_tco_depreciation_deck.js
 * 
 * Displays fleet capital asset valuation and straight-line depreciation:
 * - Purchase CapEx, Accumulated Depreciation, Net Book Value (NBV)
 * - Major overhaul milestones (Engine MOH, Transmission Rebuilds)
 */

class CityBusAssetDepreciationDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.assets = [
      { bus: 'AP16-001', type: 'Tata Starbus Urban (Diesel)', capexInr: 3800000, ageYrs: 4.5, nbvInr: 2520000, nextOverhaul: '250,000 km (Transmission Rebuild)' },
      { bus: 'AP16-002', type: 'Tata Starbus Urban (Diesel)', capexInr: 3800000, ageYrs: 4.5, nbvInr: 2520000, nextOverhaul: '250,000 km (Transmission Rebuild)' },
      { bus: 'AP16-E-101', type: 'Olectra Greentech K9 (EV)', capexInr: 14500000, ageYrs: 2.0, nbvInr: 11200000, nextOverhaul: 'Battery Module Balance & Coolant Flush' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Fleet Asset Capital Valuation & Depreciation Ledger</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Schedule II Municipal Accounting & Asset Registry</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Exporting Asset Depreciation Schedule CSV.')">📄 Export Asset Ledger</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">BUS NUMBER</th>
                <th style="padding: 0.75rem;">MODEL & CHASSIS</th>
                <th style="padding: 0.75rem;">CAPEX COST</th>
                <th style="padding: 0.75rem;">AGE</th>
                <th style="padding: 0.75rem;">NET BOOK VALUE (NBV)</th>
                <th style="padding: 0.75rem;">NEXT OVERHAUL</th>
              </tr>
            </thead>
            <tbody>
              ${this.assets.map(a => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${a.bus}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${a.type}</td>
                  <td style="padding: 0.75rem;">₹${(a.capexInr / 100000).toFixed(1)} Lakhs</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">${a.ageYrs} Years</td>
                  <td style="padding: 0.75rem; font-weight: 800; color: var(--cb-status-success);">₹${(a.nbvInr / 100000).toFixed(1)} Lakhs</td>
                  <td style="padding: 0.75rem; font-size: 0.8rem; color: var(--cb-text-muted);">${a.nextOverhaul}</td>
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
window.CityBusAssetDepreciationDeck = CityBusAssetDepreciationDeck;
