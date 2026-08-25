/**
 * CityBus Enterprise Platform - NFC Digital Wallet Card & Express Tap
 * File: js/passenger/nfc_digital_wallet_pass.js
 * 
 * Provides interactive Apple Wallet / Google Pay NFC transit card experience:
 * - Dynamic balance display & UPI AutoPay status
 * - 1-Tap simulated NFC validator turnstile pass (<120ms tap)
 */

class CityBusNFCDigitalWallet {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.card = {
      cardholder: 'SITA RAMA RAJU',
      dpanToken: '4900 •••• •••• 8821',
      balanceInr: 340.0,
      autoTopupActive: true,
      passType: 'VIJAYAWADA TRANSIT METRO PASS'
    };
    this.render();
  }

  simulateNFCTap() {
    alert(`📶 NFC TAP SUCCESS!\nValidator: PNBS Platform Turnstile\nFare: ₹25.00 Debited in 118ms\nNew Balance: ₹${(this.card.balanceInr - 25.0).toFixed(2)}`);
    this.card.balanceInr -= 25.0;
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="max-width: 420px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.25rem;">
        
        <!-- Virtual NFC Card -->
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0284C7 100%); border-radius: 16px; padding: 1.5rem; color: #fff; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); position: relative; overflow: hidden;">
          
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div style="font-weight: 800; font-size: 0.9rem; letter-spacing: 1px; color: #38BDF8;">CITYBUS VIRTUAL NCMC</div>
            <span style="font-size: 1.2rem;">📶</span>
          </div>

          <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 2px;">VIRTUAL PURSE BALANCE</div>
          <div style="font-size: 2rem; font-weight: 900; color: #fff; margin-bottom: 1.5rem;">₹${this.card.balanceInr.toFixed(2)}</div>

          <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
              <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Cardholder</div>
              <div style="font-weight: 700; font-size: 0.95rem; letter-spacing: 0.5px;">${this.card.cardholder}</div>
            </div>
            <div style="font-family: monospace; font-size: 0.85rem; color: #38BDF8;">
              ${this.card.dpanToken}
            </div>
          </div>

        </div>

        <!-- Tap Button -->
        <button class="btn btn-primary" style="padding: 0.85rem; font-weight: 800; font-size: 1rem; border-radius: 12px; display: flex; justify-content: center; align-items: center; gap: 0.5rem;" onclick="window.nfcWalletInstance.simulateNFCTap()">
          📶 Hold Near Turnstile to Pay (NFC Tap)
        </button>

        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: var(--cb-text-muted); padding: 0 0.5rem;">
          <span>UPI AutoPay Reload: <strong style="color: var(--cb-status-success);">ENABLED (₹200)</strong></span>
          <span>Apple / Google Wallet Ready</span>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusNFCDigitalWallet = CityBusNFCDigitalWallet;
