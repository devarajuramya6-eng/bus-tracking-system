/**
 * CityBus Enterprise Platform - Live Transit Service Alert & Disruption Ticker
 * File: js/components/siri_alert_ticker.js
 * 
 * Displays live scrolling municipal transit alerts conforming to SIRI-SX / GTFS-RT:
 * - Weather warnings (Heavy monsoons, river flood inundation)
 * - Festival route diversions (Kanaka Durga Temple Bhavani Deeksha)
 * - Emergency roadwork diversions
 */

class CityBusSIRIAlertTicker {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.alerts = options.alerts || [
      { id: 'ALT-01', severity: 'Warning', title: 'Route 27A Diversion', desc: 'Bypassing Prakasham Barrage due to annual canal desilting. Use Kanaka Durga Flyover corridor.' },
      { id: 'ALT-02', severity: 'Info', title: 'Festival Special Services', desc: '20 Extra Electric AC buses operating from Railway Station to Indrakeeladri for Friday rush.' },
      { id: 'ALT-03', severity: 'Normal', title: 'NCMC Smart Card Rebate', desc: '10% cashback on all contactless transit card tap-ins during off-peak hours (11:00 AM - 04:00 PM).' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: var(--cb-radius-md); padding: 0.75rem 1rem; display: flex; align-items: center; gap: 1rem; overflow: hidden;">
        
        <div style="display: flex; align-items: center; gap: 6px; background: #DC2626; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; white-space: nowrap;">
          <span>🚨 LIVE ALERTS</span>
        </div>

        <div style="flex: 1; overflow: hidden; white-space: nowrap;">
          <div style="display: inline-block; animation: cb-marquee 25s linear infinite; font-size: 0.85rem; color: #E2E8F0;">
            ${this.alerts.map(a => `
              <span style="margin-right: 2.5rem;">
                <strong style="color: #F59E0B;">[${a.title}]</strong> ${a.desc}
              </span>
            `).join('')}
          </div>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusSIRIAlertTicker = CityBusSIRIAlertTicker;
