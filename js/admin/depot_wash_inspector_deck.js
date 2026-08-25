/**
 * CityBus Enterprise Platform - Drive-Through Bus Wash & Undercarriage Scanner Deck
 * File: js/admin/depot_wash_inspector_deck.js
 * 
 * Displays automatic depot wash bay metrics and optical undercarriage inspection:
 * - Line-scan camera defect results (Fluid leaks, structural bolt checks)
 * - 85% Wash water recycling & TSS water quality compliance
 */

class CityBusDepotWashDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.washLog = [
      { bus: 'AP16-001', time: '19:42', washType: 'Exterior Brush + Underbody', undercarriageStatus: 'CLEARED_NO_LEAKS', recycleTSS: '28 mg/L' },
      { bus: 'AP16-003', time: '19:50', washType: 'Exterior Brush + Deep Misting', undercarriageStatus: 'CLEARED_NO_LEAKS', recycleTSS: '31 mg/L' },
      { bus: 'AP16-014', time: '20:05', washType: 'Exterior Brush Only', undercarriageStatus: 'DEFECT_OIL_SEEPAGE', recycleTSS: '34 mg/L' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Automated Depot Wash & Undercarriage Scanner</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">86.5% Water Recycling & Optical Chassis Leak Inspection</p>
          </div>
          <span class="badge badge-success">💧 Wash Bay Online</span>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">BUS NUMBER</th>
                <th style="padding: 0.75rem;">RETURN TIME</th>
                <th style="padding: 0.75rem;">WASH CYCLE</th>
                <th style="padding: 0.75rem;">UNDERBODY CHASSIS SCAN</th>
                <th style="padding: 0.75rem;">WATER RECYCLE TSS</th>
              </tr>
            </thead>
            <tbody>
              ${this.washLog.map(w => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${w.bus}</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">${w.time}</td>
                  <td style="padding: 0.75rem;">${w.washType}</td>
                  <td style="padding: 0.75rem;">
                    <span class="badge ${w.undercarriageStatus.includes('DEFECT') ? 'badge-danger' : 'badge-success'}">
                      ${w.undercarriageStatus}
                    </span>
                  </td>
                  <td style="padding: 0.75rem; font-weight: 600;">${w.recycleTSS} (Compliant)</td>
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
window.CityBusDepotWashDeck = CityBusDepotWashDeck;
