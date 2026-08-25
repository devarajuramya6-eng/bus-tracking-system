/**
 * CityBus Enterprise Platform - Digital Out-of-Home (DOOH) Transit Ad Monetization Deck
 * File: js/admin/transit_ad_revenue_deck.js
 * 
 * Manages geofenced in-cabin advertising campaigns and commercial revenue:
 * - Proof-of-Play (PoP) verified passenger impressions
 * - Commercial revenue tracking (CPM ₹150 - ₹180)
 */

class CityBusTransitAdDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.campaigns = [
      { id: 'CAMP-01', sponsor: 'Trendset Mall Vijayawada', trigger: 'Benz Circle (600m Geofence)', cpm: '₹180', impressions: 42800, revenueInr: 7704 },
      { id: 'CAMP-02', sponsor: 'Mangalagiri AIIMS Screening', trigger: 'AIIMS Corridor (1000m)', cpm: '₹150', impressions: 31200, revenueInr: 4680 },
      { id: 'CAMP-03', sponsor: 'Hotel Novotel Airport', trigger: 'Gannavaram Airport (800m)', cpm: '₹200', impressions: 18400, revenueInr: 3680 }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    const totalRev = this.campaigns.reduce((acc, c) => acc + c.revenueInr, 0);

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">In-Bus Programmatic DOOH Advertising & Revenue Console</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">GPS Geofenced Commercial Campaigns & Cryptographic PoP Impression Audits</p>
          </div>
          <div style="font-size: 1.1rem; font-weight: 800; color: var(--cb-status-success);">
            Monthly Ad Revenue: ₹${totalRev.toLocaleString()}
          </div>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">CAMPAIGN</th>
                <th style="padding: 0.75rem;">SPONSOR</th>
                <th style="padding: 0.75rem;">GEOFENCE TRIGGER</th>
                <th style="padding: 0.75rem;">CPM RATE</th>
                <th style="padding: 0.75rem;">VERIFIED IMPRESSIONS</th>
                <th style="padding: 0.75rem;">REVENUE EARNED</th>
              </tr>
            </thead>
            <tbody>
              ${this.campaigns.map(c => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-family: monospace; font-weight: 700; color: var(--cb-brand-primary);">${c.id}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${c.sponsor}</td>
                  <td style="padding: 0.75rem; font-size: 0.8rem; color: var(--cb-text-muted);">${c.trigger}</td>
                  <td style="padding: 0.75rem; font-weight: 700;">${c.cpm}</td>
                  <td style="padding: 0.75rem; font-weight: 800; color: var(--cb-status-info);">${c.impressions.toLocaleString()}</td>
                  <td style="padding: 0.75rem; font-weight: 800; color: var(--cb-status-success);">₹${c.revenueInr.toLocaleString()}</td>
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
window.CityBusTransitAdDeck = CityBusTransitAdDeck;
