class AdCampaignManagerController {
    constructor() { this.campaigns = []; }
    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin'])) return;
        this.renderAdTable();
    }
    renderAdTable() {
        const container = document.getElementById('ad-campaigns-table-container');
        if (!container) return;
        container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead><tr><th>Campaign ID</th><th>Advertiser</th><th>Format</th><th>Daily Budget</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td><code>AD-ANDHRA-BANK</code></td><td>Union Bank of India</td><td>In-Cabin Video</td><td>₹1,500/day</td><td><span class="badge badge-success">ACTIVE</span></td></tr>
                        <tr><td><code>AD-KLU-UNIV</code></td><td>KL University</td><td>Bus Side Wrap</td><td>₹2,800/day</td><td><span class="badge badge-success">ACTIVE</span></td></tr>
                        <tr><td><code>AD-AP-TOURISM</code></td><td>AP Tourism</td><td>In-Cabin Video</td><td>₹1,200/day</td><td><span class="badge badge-success">ACTIVE</span></td></tr>
                    </tbody>
                </table>
            </div>
        `;
    }
}
window.adCampaignManager = new AdCampaignManagerController();
