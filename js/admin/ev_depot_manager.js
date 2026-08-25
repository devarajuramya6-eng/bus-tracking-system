/**
 * CityBus Enterprise Platform - Electric Bus Depot Charging Station Manager
 * File: js/admin/ev_depot_manager.js
 * 
 * Provides depot charging bay management & power transformer grid monitoring:
 * - Real-time charging bay statuses (Fast DC 120kW bays)
 * - Depot substation power consumption (kW / MW) load gauge
 * - Smart charging priority queue optimizer
 */

class CityBusEVDepotManager {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.depotData = null;
    this.init();
  }

  async init() {
    // Generate initial simulated depot charging status
    this.depotData = {
      depotName: "PNBS Central Transit Depot & Charging Hub",
      transformerMaxKw: 1200,
      currentPowerKw: 840,
      activeBays: [
        { bayId: "BAY-01", busNumber: "AP16-E-101", model: "Olectra K9 Electric", currentSoc: 48, targetSoc: 95, powerKw: 120, timeRemainingMin: 42 },
        { bayId: "BAY-02", busNumber: "AP16-E-102", model: "Switch EiV 12 Low-Floor", currentSoc: 64, targetSoc: 95, powerKw: 120, timeRemainingMin: 28 },
        { bayId: "BAY-03", busNumber: "AP16-E-105", model: "Tata Ultra 9/9m EV", currentSoc: 32, targetSoc: 95, powerKw: 120, timeRemainingMin: 55 },
        { bayId: "BAY-04", busNumber: "AP16-E-108", model: "Olectra K9 Electric", currentSoc: 78, targetSoc: 95, powerKw: 120, timeRemainingMin: 15 },
        { bayId: "BAY-05", busNumber: "AP16-E-112", model: "Switch EiV 12 Low-Floor", currentSoc: 55, targetSoc: 95, powerKw: 120, timeRemainingMin: 36 },
        { bayId: "BAY-06", busNumber: "AP16-E-115", model: "Tata Ultra 9/9m EV", currentSoc: 82, targetSoc: 95, powerKw: 120, timeRemainingMin: 10 },
        { bayId: "BAY-07", busNumber: "AP16-E-119", model: "Olectra K9 Electric", currentSoc: 22, targetSoc: 95, powerKw: 120, timeRemainingMin: 65 }
      ],
      emptyBays: ["BAY-08", "BAY-09", "BAY-10"],
      waitingQueue: [
        { busNumber: "AP16-E-122", soc: 18, priority: "URGENT_MORNING_PULLOUT" },
        { busNumber: "AP16-E-125", soc: 24, priority: "NORMAL" }
      ]
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    const loadPct = Math.round((this.depotData.currentPowerKw / this.depotData.transformerMaxKw) * 100);

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <!-- Top Stats Row -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
          <div class="card" style="padding: 1.25rem;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Substation Power Load</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: ${loadPct > 85 ? 'var(--cb-status-danger)' : 'var(--cb-brand-primary)'}; margin: 4px 0;">
              ${this.depotData.currentPowerKw} / ${this.depotData.transformerMaxKw} kW
            </div>
            <div style="width: 100%; height: 6px; background: var(--cb-bg-subtle); border-radius: 3px; overflow: hidden; margin-top: 6px;">
              <div style="width: ${loadPct}%; height: 100%; background: var(--cb-brand-primary);"></div>
            </div>
          </div>

          <div class="card" style="padding: 1.25rem;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Active Charging Bays</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--cb-status-success); margin: 4px 0;">
              ${this.depotData.activeBays.length} Bays Active
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">${this.depotData.emptyBays.length} Available DC Fast Bays</div>
          </div>

          <div class="card" style="padding: 1.25rem;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Queue Waiting Count</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--cb-status-warning); margin: 4px 0;">
              ${this.depotData.waitingQueue.length} Vehicles
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Smart priority ToU scheduling active</div>
          </div>
        </div>

        <!-- Charging Bays Grid -->
        <div class="card" style="padding: 1.5rem;">
          <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">120 kW Fast DC Charging Bays</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem;">
            ${this.depotData.activeBays.map(bay => `
              <div style="background: var(--cb-bg-subtle); border-radius: var(--cb-radius-md); padding: 1rem; border-left: 4px solid var(--cb-status-success); border-top: 1px solid var(--cb-border-color); border-right: 1px solid var(--cb-border-color); border-bottom: 1px solid var(--cb-border-color);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                  <span style="font-weight: 800; font-size: 0.9rem;">⚡ ${bay.bayId}</span>
                  <span class="badge badge-success">${bay.powerKw} kW Fast</span>
                </div>
                <div style="font-weight: 700; font-size: 0.95rem; color: var(--cb-text-primary);">${bay.busNumber}</div>
                <div style="font-size: 0.75rem; color: var(--cb-text-muted); margin-bottom: 0.75rem;">${bay.model}</div>
                
                <div>
                  <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 4px;">
                    <span>SoC Level</span>
                    <span style="font-weight: bold; color: var(--cb-status-success);">${bay.currentSoc}% ➔ ${bay.targetSoc}%</span>
                  </div>
                  <div style="width: 100%; height: 6px; background: var(--cb-bg-surface); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
                    <div style="width: ${bay.currentSoc}%; height: 100%; background: var(--cb-status-success);"></div>
                  </div>
                </div>
                <div style="font-size: 0.75rem; color: var(--cb-text-muted); text-align: right;">Est. Ready in ${bay.timeRemainingMin} mins</div>
              </div>
            `).join('')}

            ${this.depotData.emptyBays.map(bayId => `
              <div style="background: var(--cb-bg-subtle); border-radius: var(--cb-radius-md); padding: 1rem; border: 1px dashed var(--cb-border-color); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 140px;">
                <div style="font-weight: 700; color: var(--cb-text-muted);">${bayId}</div>
                <div style="font-size: 0.8rem; color: var(--cb-status-success); margin-top: 4px;">● Ready for Docking</div>
              </div>
            `).join('')}
          </div>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusEVDepotManager = CityBusEVDepotManager;
