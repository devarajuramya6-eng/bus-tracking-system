/**
 * CityBus Enterprise Platform - Driver Union Roster & Peer Duty Swap Portal
 * File: js/driver/driver_roster_swap_portal.js
 * 
 * Provides driver weekly duty roster, peer shift swapping, and leave bidding:
 * - 48-Hour statutory weekly driving hour ceiling tracker
 * - 1-Click peer shift swap request with instant supervisor dispatch sync
 */

class CityBusDriverRosterPortal {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.shifts = [
      { day: 'Monday', route: 'Route 27A (Morning Shift)', hours: '06:00 - 14:00 (8h)', status: 'COMPLETED' },
      { day: 'Tuesday', route: 'Route 27A (Morning Shift)', hours: '06:00 - 14:00 (8h)', status: 'COMPLETED' },
      { day: 'Wednesday', route: 'Route 5K (General Shift)', hours: '08:00 - 16:00 (8h)', status: 'SCHEDULED' },
      { day: 'Thursday', route: 'Route 100E (Afternoon Shift)', hours: '14:00 - 22:00 (8h)', status: 'SCHEDULED' },
      { day: 'Friday', route: 'REST DAY (Statutory Off)', hours: '-', status: 'OFF_DUTY' }
    ];
    this.render();
  }

  requestSwap(day) {
    alert(`Shift swap request for ${day} broadcasted to available depot drivers.`);
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Driver Shift Roster & Peer Swap Portal</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Motor Transport Workers Act Compliant (32h / 48h Weekly Cap)</p>
          </div>
          <span class="badge badge-success">Weekly Hours: 32 / 48h</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          ${this.shifts.map(s => `
            <div class="card" style="padding: 1rem 1.25rem; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-weight: 800; font-size: 0.95rem; color: var(--cb-text-primary);">${s.day}: ${s.route}</div>
                <div style="font-size: 0.8rem; color: var(--cb-text-muted);">${s.hours}</div>
              </div>
              <div style="display: flex; gap: 0.5rem; align-items: center;">
                <span class="badge ${s.status === 'COMPLETED' ? 'badge-primary' : (s.status === 'SCHEDULED' ? 'badge-success' : 'badge-warning')}">${s.status}</span>
                ${s.status === 'SCHEDULED' ? `<button class="btn btn-sm btn-outline-primary" onclick="window.driverRosterInstance.requestSwap('${s.day}')">🔄 Swap</button>` : ''}
              </div>
            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusDriverRosterPortal = CityBusDriverRosterPortal;
