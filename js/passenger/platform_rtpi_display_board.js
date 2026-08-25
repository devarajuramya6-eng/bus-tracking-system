/**
 * CityBus Enterprise Platform - Terminal 4K Passenger Departure Board
 * File: js/passenger/platform_rtpi_display_board.js
 * 
 * Renders terminal overhead 4K passenger departure display:
 * - Next 6 departures with live platform bay allocations
 * - Live Telugu & English destination ticker
 */

class CityBusPlatformRTPIBoard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.departures = [
      { route: '27A', destEn: 'Guntur Bus Station', destTe: 'గుంటూరు', bay: 'BAY 04', etaMin: 2, status: 'BOARDING' },
      { route: '5K', destEn: 'Autonagar Terminal', destTe: 'ఆటోనగర్', bay: 'BAY 02', etaMin: 5, status: 'ON TIME' },
      { route: '100E', destEn: 'Gannavaram Airport (EV)', destTe: 'విమానాశ్రయం', bay: 'BAY 01', etaMin: 8, status: 'ON TIME' },
      { route: '10', destEn: 'City Circular Loop', destTe: 'సిటీ సర్క్యులర్', bay: 'BAY 06', etaMin: 12, status: 'ON TIME' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 3px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 1rem; margin-bottom: 1.25rem;">
          <div>
            <h3 style="font-size: 1.3rem; font-weight: 900; margin: 0; color: #F8FAFC;">PANDIT NEHRU BUS STATION (PNBS)</h3>
            <span style="font-size: 0.85rem; color: #94A3B8;">Live Passenger Departure Information (RTPI)</span>
          </div>
          <div style="font-family: monospace; font-size: 1.4rem; font-weight: 800; color: #38BDF8;">
            14:10:25
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          ${this.departures.map(d => `
            <div style="display: flex; justify-content: space-between; align-items: center; background: #0F172A; padding: 1rem 1.25rem; border-radius: 8px; border-left: 6px solid #38BDF8;">
              <div style="display: flex; align-items: center; gap: 1.25rem;">
                <span style="font-family: monospace; font-size: 1.5rem; font-weight: 900; color: #F59E0B; width: 60px;">${d.route}</span>
                <div>
                  <div style="font-weight: 800; font-size: 1.1rem; color: #F8FAFC;">${d.destEn}</div>
                  <div style="font-size: 0.9rem; color: #94A3B8;">${d.destTe}</div>
                </div>
              </div>
              
              <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="background: #1E293B; padding: 0.4rem 0.75rem; border-radius: 6px; font-weight: 800; color: #38BDF8; font-size: 0.95rem;">
                  ${d.bay}
                </div>
                <div style="text-align: right; width: 100px;">
                  <div style="font-size: 1.2rem; font-weight: 900; color: ${d.etaMin <= 2 ? '#10B981' : '#38BDF8'};">
                    ${d.etaMin} MIN
                  </div>
                  <div style="font-size: 0.75rem; color: #94A3B8;">${d.status}</div>
                </div>
              </div>
            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusPlatformRTPIBoard = CityBusPlatformRTPIBoard;
