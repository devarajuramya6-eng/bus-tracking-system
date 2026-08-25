class RevenueDashboard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: 'Inter', sans-serif;
                    padding: 24px;
                    background: var(--bg-color, #f4f7f6);
                }
                .dashboard-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 24px;
                }
                .dashboard-header h1 {
                    margin: 0;
                    font-size: 24px;
                    color: var(--text-dark, #2d3748);
                }
                .metrics-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .metric-card {
                    background: #fff;
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                    display: flex;
                    flex-direction: column;
                }
                .metric-title {
                    font-size: 14px;
                    color: #718096;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                .metric-value {
                    font-size: 32px;
                    font-weight: 700;
                    color: #2b6cb0;
                    margin-bottom: 8px;
                }
                .metric-trend {
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }
                .trend-up { color: #48bb78; }
                .trend-down { color: #f56565; }
                
                .chart-container {
                    background: #fff;
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                    height: 400px;
                    margin-bottom: 30px;
                }
                .chart-container h3 {
                    margin-top: 0;
                    color: #2d3748;
                    margin-bottom: 20px;
                }
            </style>
            
            <div class="dashboard-header">
                <h1>Revenue Analytics Overview</h1>
                <button style="padding: 10px 20px; border-radius: 8px; border: none; background: #2b6cb0; color: white; cursor: pointer;">
                    Download PDF Report
                </button>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-title">Total Daily Revenue</span>
                    <span class="metric-value">$14,592.50</span>
                    <span class="metric-trend trend-up">↑ 12.5% vs Yesterday</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Active Subscriptions</span>
                    <span class="metric-value">3,241</span>
                    <span class="metric-trend trend-up">↑ 5.2% vs Last Week</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Average Transaction</span>
                    <span class="metric-value">$4.50</span>
                    <span class="metric-trend trend-down">↓ 1.1% vs Yesterday</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Refunded Amount</span>
                    <span class="metric-value">$124.00</span>
                    <span class="metric-trend trend-down">↓ 15.0% vs Yesterday</span>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Revenue by Time of Day</h3>
                <div style="display:flex; justify-content:center; align-items:center; height: 300px; background: #f7fafc; border-radius: 8px; color: #a0aec0;">
                    [Interactive Chart Rendering Area]
                </div>
            </div>
        `;
    }
}

customElements.define('revenue-dashboard', RevenueDashboard);
