/**
 * CityBus Enterprise Platform - Driver Telematics Safety Scorecard & Coaching Hub
 * File: js/driver/driver_scorecard_hub.js
 * 
 * Provides Driver daily safety metrics and defensive driving coaching:
 * - 100-Point Safety Score (Harsh braking, cornering, tailgating)
 * - Monthly Safety Incentive Bonus Tracker (₹500 for 90+ score)
 * - Eco-Driving regenerative coasting efficiency
 */

class CityBusDriverScorecardHub {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.scorecard = {
      driverName: 'Ravi Kumar (DRV-102)',
      safetyScore: 94.5,
      tier: '👑 MASTER CAPTAIN',
      distanceKm: 420.0,
      harshBrakes: 1,
      rapidAccels: 0,
      harshTurns: 0,
      coastingPct: 22.4,
      earnedIncentiveInr: 500.0
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Driver Safety Scorecard & Eco-Coach</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">${this.scorecard.driverName}</p>
          </div>
          <span class="badge badge-success" style="font-size: 0.85rem;">${this.scorecard.tier}</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem;">
          
          <div class="card" style="padding: 1.25rem; text-align: center;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Overall Safety Score</div>
            <div style="font-size: 2.5rem; font-weight: 900; color: var(--cb-status-success); margin: 4px 0;">
              ${this.scorecard.safetyScore}
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Top 5% across Vijayawada depot</div>
          </div>

          <div class="card" style="padding: 1.25rem;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Telematics Infractions</div>
            <div style="display: flex; flex-direction: column; gap: 4px; margin-top: 6px; font-size: 0.85rem;">
              <div style="display: flex; justify-content: space-between;">
                <span>Harsh Braking:</span>
                <strong style="color: var(--cb-status-warning);">${this.scorecard.harshBrakes}</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span>Harsh Cornering:</span>
                <strong style="color: var(--cb-status-success);">${this.scorecard.harshTurns}</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span>Overspeed Violations:</span>
                <strong style="color: var(--cb-status-success);">0</strong>
              </div>
            </div>
          </div>

          <div class="card" style="padding: 1.25rem;">
            <div style="font-size: 0.8rem; color: var(--cb-text-muted); text-transform: uppercase;">Safety Bonus Reward</div>
            <div style="font-size: 2rem; font-weight: 900; color: var(--cb-brand-primary); margin: 4px 0;">
              ₹${this.scorecard.earnedIncentiveInr}
            </div>
            <div style="font-size: 0.75rem; color: var(--cb-status-success);">Eligible for monthly bonus payout</div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusDriverScorecardHub = CityBusDriverScorecardHub;
