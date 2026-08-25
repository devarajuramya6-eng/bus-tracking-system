/**
 * CityBus Enterprise Platform - SAM HSM & Contactless Cryptography Terminal
 * File: js/admin/sam_hsm_cryptography_deck.js
 * 
 * Displays SAM hardware security module status and contactless cryptographic verification:
 * - AES-128 / 3DES CMAC Mutual Authentication
 * - ISO 8583 Banking settlement batches
 */

class CityBusSAMCryptoDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.samStatus = {
      hsmSlot: 'SLOT_01_NCMC_SAM_EV3',
      keyVersion: 'v4.2.1',
      activeCryptogramsToday: 14280,
      failedTaps: 3,
      settlementBatchStatus: 'SEALED_READY_FOR_ACH'
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #38BDF8; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">SAM Hardware Security Module (HSM) Cryptography</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.samStatus.hsmSlot} (AES-128 / NCMC 3DES)</span>
          </div>
          <span class="badge badge-success">● HSM ONLINE</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Verified Tap Cryptograms</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.samStatus.activeCryptogramsToday.toLocaleString()}</div>
            <div style="font-size: 0.75rem; color: #10B981;">100% CMAC Integrity Cleared</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Fraudulent / Replay Taps</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #EF4444; margin: 4px 0;">${this.samStatus.failedTaps}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Blocked by Nonce Verification</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">ISO 8583 Batch Settlement</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">₹3,42,800</div>
            <div style="font-size: 0.75rem; color: #10B981;">SBI Transit Clearing Queue</div>
          </div>

        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; background: #0F172A; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem;">
          <span>Terminal Key Rollover: <strong>In 180 Days</strong></span>
          <button class="btn btn-sm btn-outline-primary" onclick="alert('Exporting ISO 8583 Settlement Batch to SBI Clearing.')">🏦 Transmit ISO 8583 Batch</button>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusSAMCryptoDeck = CityBusSAMCryptoDeck;
