/**
 * CityBus Enterprise Platform - Central Workshop & Maintenance Bay Manager
 * File: js/admin/workshop_manager.js
 * 
 * Provides interactive workshop bay management:
 * - Real-time pit and lift bay occupancy cards
 * - Job card creation, mechanic assignments, and repair time tracking
 * - Spare parts requisition trigger
 */

class CityBusWorkshopManager {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.bays = [
      { id: 'BAY-PIT-01', type: 'Underbody Inspection Pit', status: 'Occupied', bus: 'AP16-004', job: 'Brake Pad Overhaul', mechanic: 'K. Satyanarayana', elapsedMin: 45, progress: 65 },
      { id: 'BAY-PIT-02', type: 'Underbody Inspection Pit', status: 'Available', bus: null, job: null, mechanic: null, elapsedMin: 0, progress: 0 },
      { id: 'BAY-LFT-01', type: 'Hydraulic 4-Post Lift', status: 'Occupied', bus: 'AP16-012', job: 'Transmission Fluid Flush', mechanic: 'M. Venkatesh', elapsedMin: 80, progress: 85 },
      { id: 'BAY-EV-01', type: 'EV High-Voltage Bay', status: 'Available', bus: null, job: null, mechanic: null, elapsedMin: 0, progress: 0 },
      { id: 'BAY-PNT-01', type: 'Paint & Body Shop', status: 'Occupied', bus: 'AP16-027', job: 'Side Bumper Dent Repair', mechanic: 'S. Raju', elapsedMin: 120, progress: 40 }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Central Depot Workshop Bays</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Autonagar Heavy Maintenance Facility</p>
          </div>
          <button class="btn btn-primary" onclick="alert('New Job Card Created.')">➕ Create Job Card</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.25rem;">
          ${this.bays.map(bay => {
            const isOccupied = bay.status === 'Occupied';
            return `
              <div class="card" style="padding: 1.25rem; border-top: 4px solid ${isOccupied ? 'var(--cb-status-danger)' : 'var(--cb-status-success)'};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                  <span style="font-weight: 800; font-size: 1rem;">🔧 ${bay.id}</span>
                  <span class="badge ${isOccupied ? 'badge-danger' : 'badge-success'}">${bay.status}</span>
                </div>

                <div style="font-size: 0.8rem; color: var(--cb-text-muted); margin-bottom: 1rem;">${bay.type}</div>

                ${isOccupied ? `
                  <div style="background: var(--cb-bg-subtle); padding: 1rem; border-radius: var(--cb-radius-md); margin-bottom: 1rem;">
                    <div style="font-size: 0.8rem; color: var(--cb-text-muted);">Vehicle In Service:</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: var(--cb-text-primary);">${bay.bus}</div>
                    <div style="font-size: 0.85rem; font-weight: 600; color: var(--cb-brand-primary); margin-top: 4px;">${bay.job}</div>
                    <div style="font-size: 0.75rem; color: var(--cb-text-muted); margin-top: 4px;">Tech: <strong>${bay.mechanic}</strong> (${bay.elapsedMin}m logged)</div>

                    <div style="margin-top: 0.75rem;">
                      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 3px;">
                        <span>Task Completion</span>
                        <span>${bay.progress}%</span>
                      </div>
                      <div style="width: 100%; height: 6px; background: var(--cb-bg-surface); border-radius: 3px; overflow: hidden;">
                        <div style="width: ${bay.progress}%; height: 100%; background: var(--cb-brand-primary);"></div>
                      </div>
                    </div>
                  </div>
                  <button class="btn btn-sm btn-outline-success" style="width: 100%;" onclick="alert('Work order signed off.')">Complete & Sign Off Job</button>
                ` : `
                  <div style="min-height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; border: 1px dashed var(--cb-border-color); border-radius: var(--cb-radius-md); margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem; margin-bottom: 4px;">🟢</div>
                    <div style="font-size: 0.85rem; font-weight: 600; color: var(--cb-status-success);">Bay Ready for Intake</div>
                    <div style="font-size: 0.75rem; color: var(--cb-text-muted);">No active repair in progress</div>
                  </div>
                  <button class="btn btn-sm btn-outline-primary" style="width: 100%;" onclick="alert('Select bus to assign to bay.')">Assign Inbound Bus</button>
                `}

              </div>
            `;
          }).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusWorkshopManager = CityBusWorkshopManager;
