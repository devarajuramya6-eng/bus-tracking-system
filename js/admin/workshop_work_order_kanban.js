/**
 * CityBus Enterprise Platform - Maintenance Work Order Kanban Board
 * File: js/admin/workshop_work_order_kanban.js
 * 
 * Manages workshop vehicle repair job card states:
 * - IN_PROGRESS, AWAITING_PARTS, QC_INSPECTION_PENDING, CLOSED
 * - Technician assignment and Standard Repair Time (SRT) tracking
 */

class CityBusWorkOrderKanban {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.workOrders = [
      { id: 'WO-8491', bus: 'AP16-004', job: 'Brake Pad Replacement (Front & Rear)', status: 'IN_PROGRESS', technician: 'M. Suresh', srtHrs: 2.5 },
      { id: 'WO-8492', bus: 'AP16-018', job: 'Alternator Replacement & Belt Tension', status: 'AWAITING_PARTS', technician: 'K. Prasad', srtHrs: 1.5 },
      { id: 'WO-8490', bus: 'AP16-E-102', job: 'Traction Inverter Coolant Flush', status: 'QC_INSPECTION_PENDING', technician: 'V. Naidu', srtHrs: 2.0 }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    const columns = [
      { key: 'IN_PROGRESS', label: '🛠️ IN PROGRESS', color: 'var(--cb-brand-primary)' },
      { key: 'AWAITING_PARTS', label: '📦 AWAITING PARTS', color: 'var(--cb-status-warning)' },
      { key: 'QC_INSPECTION_PENDING', label: '🔍 QC INSPECTION', color: 'var(--cb-status-info)' }
    ];

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Workshop Maintenance Work Order Board</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Job Card Workflow & Technician Labor Tracking</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Creating New Workshop Job Card.')">➕ New Job Card</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
          ${columns.map(col => {
            const items = this.workOrders.filter(w => w.status === col.key);
            return `
              <div class="card" style="padding: 1.25rem; background: var(--cb-bg-secondary);">
                <div style="font-weight: 800; font-size: 0.9rem; margin-bottom: 1rem; color: ${col.color}; display: flex; justify-content: space-between;">
                  <span>${col.label}</span>
                  <span class="badge badge-primary">${items.length}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                  ${items.map(item => `
                    <div style="background: var(--cb-bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--cb-border-color); box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                      <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.85rem; margin-bottom: 4px;">
                        <span style="color: var(--cb-brand-primary);">${item.id}</span>
                        <span>${item.bus}</span>
                      </div>
                      <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;">${item.job}</div>
                      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--cb-text-muted);">
                        <span>Tech: ${item.technician}</span>
                        <span>SRT: ${item.srtHrs}h</span>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusWorkOrderKanban = CityBusWorkOrderKanban;
