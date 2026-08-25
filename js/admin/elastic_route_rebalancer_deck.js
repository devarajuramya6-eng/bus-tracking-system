/**
 * CityBus Enterprise Platform - Elastic Corridor Rebalancer & Short-Turn Control Deck
 * File: js/admin/elastic_route_rebalancer_deck.js
 * 
 * Manages live network fleet capacity rebalancing and short-turn loops:
 * - Dynamic shift of standby buses from low to high-demand corridors
 * - Turnaround loop optimizations doubling central frequency
 */

class CityBusElasticRebalancerDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.recommendations = [
      { from: 'Route 12 (Rural Suburb)', to: 'Route 27A (MG Road)', buses: 2, reason: 'Route 27A is at 95% crush load (Relieve crowding)', status: 'PROPOSED' },
      { from: 'Route 18 (Industrial Off-Peak)', to: 'Route 5K (Eluru Road)', buses: 1, reason: 'Route 5K at 88% capacity during evening rush', status: 'PROPOSED' }
    ];
    this.render();
  }

  executeRebalance(index) {
    this.recommendations[index].status = 'EXECUTING_DISPATCH';
    this.render();
    alert(`Fleet dispatch transfer executed for ${this.recommendations[index].to}`);
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Elastic Network Rebalancing & Fleet Optimization</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Dynamic Load-Factor Balancing & Short-Turn Loop Injections</p>
          </div>
          <span class="badge badge-success">● AI Rebalancer Active</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${this.recommendations.map((r, i) => `
            <div class="card" style="padding: 1.25rem; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid var(--cb-brand-primary);">
              <div>
                <div style="font-weight: 800; font-size: 1.05rem; color: var(--cb-text-primary);">
                  Transfer ${r.buses} Buses: <span style="color: var(--cb-text-muted);">${r.from}</span> ➔ <span style="color: var(--cb-brand-primary);">${r.to}</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--cb-text-muted); margin-top: 4px;">${r.reason}</div>
              </div>

              <div>
                <button class="btn btn-sm ${r.status === 'PROPOSED' ? 'btn-primary' : 'btn-success'}" onclick="window.elasticRebalancerDeckInstance.executeRebalance(${i})">
                  ${r.status === 'PROPOSED' ? '🚀 Authorize Transfer' : '✓ Transfer Active'}
                </button>
              </div>
            </div>
          `).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusElasticRebalancerDeck = CityBusElasticRebalancerDeck;
