/**
 * CityBus Enterprise Platform - Depot Yard 2D Parking Bay Visualizer
 * File: js/admin/depot_yard_visualizer.js
 * 
 * Provides interactive visual 2D parking layout for transit depots:
 * - EV Dedicated Charging Stack Lanes
 * - Diesel High-Capacity Parking Lanes
 * - Vehicle inspection and automatic pull-out departure sequence
 */

class CityBusDepotYardVisualizer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.yardData = {
      depotName: 'PNBS Central Yard & Overnight Depot',
      lanes: [
        {
          id: 'LANE-EV-01',
          name: 'Fast DC Charging Lane 1',
          type: 'EV',
          slots: [
            { bus: 'AP16-E-101', pullout: '05:30 AM', soc: 98, status: 'Ready' },
            { bus: 'AP16-E-102', pullout: '05:45 AM', soc: 94, status: 'Ready' },
            { bus: 'AP16-E-105', pullout: '06:00 AM', soc: 82, status: 'Charging' }
          ]
        },
        {
          id: 'LANE-EV-02',
          name: 'Fast DC Charging Lane 2',
          type: 'EV',
          slots: [
            { bus: 'AP16-E-108', pullout: '05:35 AM', soc: 100, status: 'Ready' },
            { bus: 'AP16-E-112', pullout: '05:50 AM', soc: 91, status: 'Ready' },
            { bus: 'AP16-E-119', pullout: '06:15 AM', soc: 76, status: 'Charging' }
          ]
        },
        {
          id: 'LANE-DSL-01',
          name: 'Express Diesel Lane A',
          type: 'Diesel',
          slots: [
            { bus: 'AP16-001', pullout: '05:00 AM', fuel: '95%', status: 'Ready' },
            { bus: 'AP16-002', pullout: '05:15 AM', fuel: '90%', status: 'Ready' },
            { bus: 'AP16-003', pullout: '05:30 AM', fuel: '88%', status: 'Ready' }
          ]
        },
        {
          id: 'LANE-DSL-02',
          name: 'Metro Diesel Lane B',
          type: 'Diesel',
          slots: [
            { bus: 'AP16-005', pullout: '05:10 AM', fuel: '92%', status: 'Ready' },
            { bus: 'AP16-006', pullout: '05:25 AM', fuel: '96%', status: 'Ready' },
            { bus: 'AP16-007', pullout: '05:40 AM', fuel: '85%', status: 'Ready' }
          ]
        }
      ]
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Depot Yard Stack Parking & Pull-Out Sequence</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">${this.yardData.depotName}</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Yard shunting sequence optimized.')">⚡ Auto-Sort Pullout Queue</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
          ${this.yardData.lanes.map(lane => `
            <div class="card" style="padding: 1.25rem; border-top: 4px solid ${lane.type === 'EV' ? 'var(--cb-status-success)' : 'var(--cb-brand-primary)'};">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-weight: 800; font-size: 0.95rem;">🅿️ ${lane.id}</span>
                <span class="badge ${lane.type === 'EV' ? 'badge-success' : 'badge-primary'}">${lane.type}</span>
              </div>
              <div style="font-size: 0.8rem; color: var(--cb-text-muted); margin-bottom: 1rem;">${lane.name}</div>

              <!-- Stack Lane (Exit at top) -->
              <div style="display: flex; flex-direction: column; gap: 0.5rem; background: var(--cb-bg-subtle); padding: 0.75rem; border-radius: var(--cb-radius-md); border: 1px dashed var(--cb-border-color);">
                <div style="font-size: 0.7rem; font-weight: 700; color: var(--cb-text-muted); text-align: center; border-bottom: 1px solid var(--cb-border-color); padding-bottom: 4px;">▲ LANE EXIT GATE ▲</div>

                ${lane.slots.map((slot, idx) => `
                  <div style="background: var(--cb-bg-surface); padding: 0.75rem; border-radius: var(--cb-radius-sm); border-left: 3px solid ${slot.status === 'Ready' ? 'var(--cb-status-success)' : 'var(--cb-status-warning)'}; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                      <div style="font-weight: 700; font-size: 0.85rem; color: var(--cb-text-primary);">${slot.bus}</div>
                      <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Pullout: <strong>${slot.pullout}</strong></div>
                    </div>
                    <div style="text-align: right;">
                      <span class="badge ${slot.status === 'Ready' ? 'badge-success' : 'badge-warning'}" style="font-size: 0.7rem;">${slot.status}</span>
                      <div style="font-size: 0.7rem; color: var(--cb-text-muted); margin-top: 2px;">${lane.type === 'EV' ? `${slot.soc}% SoC` : slot.fuel}</div>
                    </div>
                  </div>
                `).join('')}

                <div style="font-size: 0.7rem; font-weight: 700; color: var(--cb-text-muted); text-align: center; border-top: 1px solid var(--cb-border-color); padding-top: 4px;">▼ LANE ENTRY REAR ▼</div>
              </div>

            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusDepotYardVisualizer = CityBusDepotYardVisualizer;
