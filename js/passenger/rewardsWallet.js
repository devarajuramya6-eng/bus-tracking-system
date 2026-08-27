/**
 * CityBus Enterprise Platform - Green Commute Rewards & Cashback Wallet
 * File: js/passenger/rewardsWallet.js
 * 
 * Manages passenger green eco-points earned per public transit kilometer,
 * daily streak bonuses, and discount voucher redemption.
 */

class RewardsWalletController {
    constructor() {
        this.rewardPoints = 480;
        this.co2SavedTotalKg = 34.2;
    }

    async init() {
        if (!window.authService.requireAuth(['passenger', 'admin', 'super_admin'])) {
            return;
        }

        this.renderRewardsDashboard();
        this.bindEvents();
    }

    renderRewardsDashboard() {
        const container = document.getElementById('rewards-wallet-container');
        if (!container) return;

        container.innerHTML = `
            <div class="rewards-summary-card p-4 bg-white border rounded shadow-sm mb-4">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <span class="text-muted small text-uppercase font-weight-bold">Available Green Points</span>
                        <h2 class="display-4 font-weight-bold text-success mb-1">🌿 ${this.rewardPoints}</h2>
                        <p class="text-muted small">Earn 10 points for every 5 km travelled on public transit</p>
                    </div>
                    <div class="col-md-6 border-start">
                        <div class="mb-2"><strong>CO2 Avoided:</strong> <span class="text-success font-weight-bold">${this.co2SavedTotalKg} kg</span></div>
                        <div class="mb-2"><strong>Commuter Tier:</strong> <span class="badge badge-primary">Silver Commuter (Level 2)</span></div>
                        <div><strong>Daily Commute Streak:</strong> 🔥 6 Days Active</div>
                    </div>
                </div>
            </div>

            <h4 class="mb-3">Redeem Green Points for Transit Vouchers</h4>
            <div class="row g-3">
                <div class="col-md-4">
                    <div class="card h-100 border-0 shadow-sm p-3">
                        <h5>₹20 Transit Pass Voucher</h5>
                        <p class="text-muted small">Valid on any CityBus Local & Express line</p>
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <span class="font-weight-bold text-success">200 Points</span>
                            <button class="btn btn-sm btn-outline-success redeem-voucher-btn" data-cost="200" data-name="₹20 Pass Voucher">Redeem</button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 border-0 shadow-sm p-3">
                        <h5>50% Off Day Pass</h5>
                        <p class="text-muted small">Valid for unlimited rides across tri-city network</p>
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <span class="font-weight-bold text-success">350 Points</span>
                            <button class="btn btn-sm btn-outline-success redeem-voucher-btn" data-cost="350" data-name="50% Off Day Pass">Redeem</button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 border-0 shadow-sm p-3">
                        <h5>Free Metro Feeder Ride</h5>
                        <p class="text-muted small">Single journey token on any metro feeder line</p>
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <span class="font-weight-bold text-success">150 Points</span>
                            <button class="btn btn-sm btn-outline-success redeem-voucher-btn" data-cost="150" data-name="Free Metro Feeder Ride">Redeem</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.bindRedeemButtons();
    }

    bindRedeemButtons() {
        document.querySelectorAll('.redeem-voucher-btn').forEach(btn => {
            btn.onclick = () => {
                const cost = Number(btn.dataset.cost);
                const name = btn.dataset.name;

                if (this.rewardPoints >= cost) {
                    this.rewardPoints -= cost;
                    window.toastManager.success(`Successfully redeemed ${name}! Promo code: CB-REWARD-${Date.now().toString().slice(-4)}`);
                    this.renderRewardsDashboard();
                } else {
                    window.toastManager.warning('Insufficient green points for this voucher.');
                }
            };
        });
    }

    bindEvents() {
        // Additional rewards events
    }
}

// Global Export
window.rewardsWallet = new RewardsWalletController();
