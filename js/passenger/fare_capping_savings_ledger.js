/**
 * CityBus Enterprise Platform - Fare Capping & Commuter Savings Ledger
 * File: js/passenger/fare_capping_savings_ledger.js
 * 
 * Displays commuter daily/weekly fare capping progress and accumulated savings:
 * - Daily ₹75 Cap & Weekly ₹350 Cap progress bar
 * - Best-value automatic pass conversions
 */

class CityBusFareCappingLedger {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.capping = {
      dailySpent: 75.0,
      dailyCap: 75.0,
      weeklySpent: 260.0,
      weeklyCap: 350.0,
      totalSavedThisMonth: 480.0,
      todayFreeRides: 2
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #10B981; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Smart Fare Capping & Best-Price Savings</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">Automatic Unlimited Rides (London TfL / OMNY Standard)</span>
          </div>
          <span class="badge badge-success">🎉 DAILY CAP REACHED - FREE RIDES</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #10B981;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Today's Spend</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">₹${this.capping.dailySpent.toFixed(2)}</div>
            <div style="font-size: 0.75rem; color: #10B981;">Capped at ₹${this.capping.dailyCap} (Free rides active)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Weekly Spend</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">₹${this.capping.weeklySpent.toFixed(2)}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Cap: <strong>₹${this.capping.weeklyCap}</strong> (₹90 to free travel)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Month Savings</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">₹${this.capping.totalSavedThisMonth.toFixed(2)}</div>
            <div style="font-size: 0.75rem; color: #10B981;">Automatic Best Fare Rate</div>
          </div>

        </div>

        <div style="background: #0F172A; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: center;">
          <span>Today's Bonus Rides: <strong style="color: #10B981;">${this.capping.todayFreeRides} Free Rides Taken</strong></span>
          <span style="color: #38BDF8; font-weight: 700;">Zero Pass Purchase Required</span>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusFareCappingLedger = CityBusFareCappingLedger;
