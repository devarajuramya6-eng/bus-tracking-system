/**
 * CityBus Enterprise Platform - Commuter Green Points & Carbon Offset Wallet
 * File: js/passenger/green_rewards_wallet.js
 * 
 * Displays commuter eco footprint and rewards:
 * - kg CO2 emissions avoided vs driving personal motorbike / car
 * - Trees planted equivalent indicator
 * - Redeemable eco-points for free electric bus rides
 */

class CityBusGreenRewardsWallet {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.ecoData = {
      userName: 'Ananya Sharma',
      greenPoints: 480,
      co2SavedKg: 44.2,
      treesEquivalent: 2.1,
      totalCleanKm: 380,
      ecoRank: '🌿 Eco Master Commuter'
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: linear-gradient(135deg, #064E3B 0%, #022C22 100%); border-radius: var(--cb-radius-lg); padding: 2rem; color: #fff; border: 1px solid #059669; box-shadow: 0 10px 25px rgba(6, 78, 59, 0.4);">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <div>
            <span class="badge badge-success" style="background: #10B981; color: #000; font-weight: 800;">${this.ecoData.ecoRank}</span>
            <h3 style="font-size: 1.4rem; font-weight: 800; margin: 6px 0 0 0;">Green Mobility Carbon Wallet</h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 0.8rem; color: #A7F3D0;">Available Eco Points</div>
            <div style="font-size: 2rem; font-weight: 900; color: #34D399;">${this.ecoData.greenPoints} PTS</div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
          
          <div style="background: rgba(255,255,255,0.08); padding: 1.25rem; border-radius: var(--cb-radius-md); backdrop-filter: blur(10px);">
            <div style="font-size: 0.8rem; color: #A7F3D0;">Total CO2 Avoided</div>
            <div style="font-size: 1.6rem; font-weight: 800; margin: 4px 0;">${this.ecoData.co2SavedKg} kg</div>
            <div style="font-size: 0.75rem; color: #D1FAE5;">vs Petrol Motorbike</div>
          </div>

          <div style="background: rgba(255,255,255,0.08); padding: 1.25rem; border-radius: var(--cb-radius-md); backdrop-filter: blur(10px);">
            <div style="font-size: 0.8rem; color: #A7F3D0;">Forest Trees Equivalent</div>
            <div style="font-size: 1.6rem; font-weight: 800; margin: 4px 0;">🌳 ${this.ecoData.treesEquivalent} Trees</div>
            <div style="font-size: 0.75rem; color: #D1FAE5;">Annual CO2 absorption</div>
          </div>

          <div style="background: rgba(255,255,255,0.08); padding: 1.25rem; border-radius: var(--cb-radius-md); backdrop-filter: blur(10px);">
            <div style="font-size: 0.8rem; color: #A7F3D0;">Clean EV Kilometers</div>
            <div style="font-size: 1.6rem; font-weight: 800; margin: 4px 0;">⚡ ${this.ecoData.totalCleanKm} km</div>
            <div style="font-size: 0.75rem; color: #D1FAE5;">Electric bus trips</div>
          </div>

        </div>

        <div style="display: flex; gap: 0.75rem;">
          <button class="btn btn-success" style="background: #10B981; color: #000; font-weight: 800;" onclick="alert('Redeemed 200 Green Points for a Free Electric AC Transit Pass!')">
            🎁 Redeem Free Bus Pass (200 PTS)
          </button>
          <button class="btn btn-outline-light" onclick="alert('Viewing Vijayawada Green Commuter Leaderboard.')">
            🏆 View City Eco Leaderboard
          </button>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusGreenRewardsWallet = CityBusGreenRewardsWallet;
