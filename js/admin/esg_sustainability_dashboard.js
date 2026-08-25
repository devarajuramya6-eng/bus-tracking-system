/**
 * CityBus Enterprise Platform - Municipal ESG Sustainability & Carbon Audit Dashboard
 * File: js/admin/esg_sustainability_dashboard.js
 * 
 * Displays quarterly municipal ESG environmental metrics:
 * - Fleet CO2 emissions abatement (Tonnes)
 * - Diesel liters displaced by electric buses
 * - PM2.5 and NOx particulate reduction indices
 */

class CityBusESGDashboard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.esgData = {
      reportingQuarter: 'Q3-2026',
      co2AvoidedTonnes: 418.5,
      dieselDisplacedLiters: 156200,
      pm25ReductionKg: 38.2,
      solarSelfGenPct: 41.2,
      evFleetRatioPct: 40.0
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Municipal ESG Clean Mobility & Carbon Abatement</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Environmental & Clean Air Metrics (${this.esgData.reportingQuarter})</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Downloading ISO 14064 ESG Audit Certificate PDF.')">📄 Download ESG Audit Report</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem;">
          
          <div class="card" style="padding: 1.25rem; border-left: 4px solid var(--cb-status-success);">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Net CO2 Abatement</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: var(--cb-status-success); margin: 4px 0;">
              ${this.esgData.co2AvoidedTonnes} Tonnes
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Avoided by EV fleet operations</div>
          </div>

          <div class="card" style="padding: 1.25rem; border-left: 4px solid var(--cb-brand-primary);">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Diesel Displaced</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: var(--cb-brand-primary); margin: 4px 0;">
              ${this.esgData.dieselDisplacedLiters.toLocaleString()} L
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">High Speed Diesel saved</div>
          </div>

          <div class="card" style="padding: 1.25rem; border-left: 4px solid var(--cb-status-warning);">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">PM2.5 Soot Reduction</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: var(--cb-status-warning); margin: 4px 0;">
              ${this.esgData.pm25ReductionKg} kg
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Urban particulate abatement</div>
          </div>

          <div class="card" style="padding: 1.25rem; border-left: 4px solid #10B981;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Depot Solar Power</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">
              ${this.esgData.solarSelfGenPct}%
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Rooftop solar self-consumption</div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusESGDashboard = CityBusESGDashboard;
