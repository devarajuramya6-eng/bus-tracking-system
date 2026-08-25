/**
 * CityBus Enterprise Platform - Demand Responsive Transit (DRT) Microtransit Dispatcher
 * File: js/admin/drts_microtransit_dispatcher.js
 * 
 * Manages on-demand first-mile feeder van pooling:
 * - Live commuter pickup request queue
 * - Dynamic route optimization & vehicle dispatch
 * - Guaranteed transfer window sync with trunk routes
 */

class CityBusDRTSDispatcher {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.feederRequests = [
      { id: 'DRT-REQ-101', user: 'V. Ramanathan', pickup: 'Gayatri Nagar Cross (Virtual Stop 1)', time: '07:15 AM', status: 'Assigned Van 1', connectingTrunk: 'Route 27A (PNBS)' },
      { id: 'DRT-REQ-102', user: 'S. Divya', pickup: 'Labbipet Park Gate (Virtual Stop 2)', time: '07:18 AM', status: 'Assigned Van 1', connectingTrunk: 'Route 27A (PNBS)' },
      { id: 'DRT-REQ-103', user: 'K. Naresh', pickup: 'Moghalrajpuram Hill Road (Virtual Stop 3)', time: '07:22 AM', status: 'Queued (Awaiting Van 2)', connectingTrunk: 'Route 5K (Autonagar)' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">On-Demand Feeder Microtransit Dispatch Radar</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">First-Mile & Last-Mile Neighborhood Pooling Vans</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Feeder Van 2 Dispatched for Moghalrajpuram pickup tour.')">🚐 Dispatch Feeder Van</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">REQ ID</th>
                <th style="padding: 0.75rem;">PASSENGER</th>
                <th style="padding: 0.75rem;">VIRTUAL PICKUP POINT</th>
                <th style="padding: 0.75rem;">REQUEST TIME</th>
                <th style="padding: 0.75rem;">CONNECTING TRUNK ROUTE</th>
                <th style="padding: 0.75rem;">STATUS</th>
                <th style="padding: 0.75rem;">ACTION</th>
              </tr>
            </thead>
            <tbody>
              ${this.feederRequests.map(r => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${r.id}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${r.user}</td>
                  <td style="padding: 0.75rem;">📍 ${r.pickup}</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">${r.time}</td>
                  <td style="padding: 0.75rem; font-weight: 600; color: var(--cb-text-primary);">${r.connectingTrunk}</td>
                  <td style="padding: 0.75rem;"><span class="badge ${r.status.includes('Assigned') ? 'badge-success' : 'badge-warning'}">${r.status}</span></td>
                  <td style="padding: 0.75rem;">
                    <button class="btn btn-sm btn-outline-primary" onclick="alert('Notified driver of pickup for ${r.user}')">Notify</button>
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
window.CityBusDRTSDispatcher = CityBusDRTSDispatcher;
