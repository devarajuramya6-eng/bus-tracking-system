class IncentivePayoutManagerController {
    constructor() { this.payouts = []; }
    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin'])) return;
        this.renderPayoutTable();
    }
    renderPayoutTable() {
        const container = document.getElementById('incentives-table-container');
        if (!container) return;
        container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead><tr><th>Driver</th><th>Trips</th><th>OTP %</th><th>Safety Score</th><th>Monthly Bonus</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>R. Venkatesh</td><td>128</td><td>96.2%</td><td>94.5</td><td><strong>₹5,000</strong></td><td><span class="badge badge-success">APPROVED</span></td></tr>
                        <tr><td>K. Srinivasa Rao</td><td>115</td><td>94.8%</td><td>91.0</td><td><strong>₹4,500</strong></td><td><span class="badge badge-success">APPROVED</span></td></tr>
                        <tr><td>M. Nagaraju</td><td>104</td><td>92.5%</td><td>88.0</td><td><strong>₹3,500</strong></td><td><span class="badge badge-primary">PENDING</span></td></tr>
                    </tbody>
                </table>
            </div>
        `;
    }
}
window.incentivePayoutManager = new IncentivePayoutManagerController();
