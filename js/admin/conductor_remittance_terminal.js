/**
 * CityBus Enterprise Platform - Conductor Cash Remittance & Waybill Settlement Terminal
 * File: js/admin/conductor_remittance_terminal.js
 * 
 * Manages daily physical cash remittance from conductors:
 * - Compares ETM Machine Cash Count vs Cash Handed In
 * - Variance detection (Shortage deduction / Excess deposit)
 * - Treasury remittance receipt generation
 */

class CityBusConductorRemittanceTerminal {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.remittances = [
      { id: 'REMIT-01', conductor: 'K. Venkatesh (CND-401)', bus: 'AP16-001', route: '27A', etmCash: 4850.0, etmDigital: 3200.0, depositedCash: 4850.0, variance: 0.0, status: 'Settled' },
      { id: 'REMIT-02', conductor: 'M. Ramesh (CND-402)', bus: 'AP16-004', route: '5K', etmCash: 3920.0, etmDigital: 2150.0, depositedCash: 3900.0, variance: -20.0, status: 'Shortage Flagged' },
      { id: 'REMIT-03', conductor: 'S. Suresh (CND-403)', bus: 'AP16-012', route: '10', etmCash: 5120.0, etmDigital: 4400.0, depositedCash: 5120.0, variance: 0.0, status: 'Settled' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Depot Treasury Cash Remittance Desk</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Daily Conductor Electronic Ticket Machine (ETM) Cash Audit</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Open New Conductor Remittance Intake Form.')">💵 Accept Shift Cash Bag</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">REMIT NO</th>
                <th style="padding: 0.75rem;">CONDUCTOR</th>
                <th style="padding: 0.75rem;">BUS / ROUTE</th>
                <th style="padding: 0.75rem;">ETM CASH</th>
                <th style="padding: 0.75rem;">ETM DIGITAL</th>
                <th style="padding: 0.75rem;">CASH DEPOSITED</th>
                <th style="padding: 0.75rem;">VARIANCE</th>
                <th style="padding: 0.75rem;">STATUS</th>
                <th style="padding: 0.75rem;">RECEIPT</th>
              </tr>
            </thead>
            <tbody>
              ${this.remittances.map(r => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${r.id}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${r.conductor}</td>
                  <td style="padding: 0.75rem;">${r.bus} <span class="badge badge-primary" style="font-size: 0.7rem;">${r.route}</span></td>
                  <td style="padding: 0.75rem; font-weight: 600;">₹${r.etmCash.toLocaleString()}</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">₹${r.etmDigital.toLocaleString()}</td>
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-text-primary);">₹${r.depositedCash.toLocaleString()}</td>
                  <td style="padding: 0.75rem; font-weight: 700; color: ${r.variance < 0 ? 'var(--cb-status-danger)' : (r.variance > 0 ? 'var(--cb-status-warning)' : 'var(--cb-status-success)')};">
                    ${r.variance === 0 ? '₹0.00' : (r.variance > 0 ? `+₹${r.variance}` : `-₹${Math.abs(r.variance)}`)}
                  </td>
                  <td style="padding: 0.75rem;">
                    <span class="badge ${r.status === 'Settled' ? 'badge-success' : 'badge-danger'}">${r.status}</span>
                  </td>
                  <td style="padding: 0.75rem;">
                    <button class="btn btn-sm btn-outline-primary" onclick="alert('Thermal Remittance Receipt Printed for ${r.conductor}')">🖨️ Print</button>
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
window.CityBusConductorRemittanceTerminal = CityBusConductorRemittanceTerminal;
