/**
 * CityBus Enterprise Platform - RFID Fuel Nozzle & Automated Dispenser Deck
 * File: js/admin/depot_fueling_rfid_deck.js
 * 
 * Monitors depot automated fuel dispensing with RFID collar authentication:
 * - Anti-pilferage solenoid lock status
 * - High-speed pulse flow meter & BS-VI DEF / AdBlue dosing telemetry
 */

class CityBusDepotFuelingDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.dispensers = [
      { id: 'DISP_01', bus: 'AP16-001', rfid: 'RFID_AP16_001', fuelLiters: 142.5, flowRateLpm: 68.2, defRatio: '5.1%', status: 'DISPENSING_LOCKED_TO_COLLAR' },
      { id: 'DISP_02', bus: 'AP16-003', rfid: 'RFID_AP16_003', fuelLiters: 98.0, flowRateLpm: 65.0, defRatio: '4.9%', status: 'DISPENSING_LOCKED_TO_COLLAR' },
      { id: 'DISP_03', bus: 'IDLE', rfid: 'NONE', fuelLiters: 0.0, flowRateLpm: 0.0, defRatio: '0.0%', status: 'SOLENOID_VALVE_LOCKED' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Automated Fleet Fueling & RFID Nozzle Terminal</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Zero-Pilferage Collar Interlocks & BS-VI AdBlue Dosing Audit</p>
          </div>
          <span class="badge badge-success">⛽ Pumps Online</span>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">DISPENSER BAY</th>
                <th style="padding: 0.75rem;">BUS NUMBER</th>
                <th style="padding: 0.75rem;">RFID COLLAR TAG</th>
                <th style="padding: 0.75rem;">DISPENSED VOLUME</th>
                <th style="padding: 0.75rem;">FLOW RATE</th>
                <th style="padding: 0.75rem;">DEF ADBLUE RATIO</th>
                <th style="padding: 0.75rem;">STATUS</th>
              </tr>
            </thead>
            <tbody>
              ${this.dispensers.map(d => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 800; color: var(--cb-brand-primary);">${d.id}</td>
                  <td style="padding: 0.75rem; font-weight: 700;">${d.bus}</td>
                  <td style="padding: 0.75rem; font-family: monospace; color: var(--cb-text-muted);">${d.rfid}</td>
                  <td style="padding: 0.75rem; font-weight: 700;">${d.fuelLiters > 0 ? `${d.fuelLiters} L` : '-'}</td>
                  <td style="padding: 0.75rem;">${d.flowRateLpm > 0 ? `${d.flowRateLpm} L/min` : '-'}</td>
                  <td style="padding: 0.75rem; font-weight: 600; color: var(--cb-status-success);">${d.defRatio}</td>
                  <td style="padding: 0.75rem;">
                    <span class="badge ${d.status.includes('DISPENSING') ? 'badge-success' : 'badge-primary'}">${d.status}</span>
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
window.CityBusDepotFuelingDeck = CityBusDepotFuelingDeck;
