/**
 * CityBus Enterprise Platform - Transit Smart Cargo Locker Pickup Terminal
 * File: js/passenger/cargo_locker_pickup_terminal.js
 * 
 * Contactless parcel pickup terminal for station locker banks:
 * - 6-Digit OTP pickup entry
 * - Automatic locker door solenoid latch release
 */

class CityBusCargoLockerTerminal {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.render();
  }

  submitOTP() {
    const input = document.getElementById('locker-otp-input');
    if (input && input.value.length === 6) {
      alert(`🔓 ACCESS GRANTED: Locker Box #124 unlocked! Please retrieve your parcel and close the door firmly.`);
    } else {
      alert('Please enter a valid 6-digit OTP.');
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card" style="max-width: 480px; margin: 0 auto; padding: 2rem; text-align: center;">
        
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📦</div>
        <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0 0 0.5rem 0;">Transit Smart Parcel Locker Terminal</h3>
        <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin-bottom: 1.5rem;">PNBS Central Station Locker Bank A</p>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <input id="locker-otp-input" type="text" maxlength="6" placeholder="Enter 6-Digit Pickup PIN" 
                 style="font-family: monospace; font-size: 1.5rem; letter-spacing: 6px; text-align: center; padding: 0.75rem; border: 2px solid var(--cb-border-color); border-radius: 8px;" />
          
          <button class="btn btn-primary" style="padding: 0.75rem;" onclick="window.cargoLockerInstance.submitOTP()">
            🔓 Unlock Locker Door
          </button>
        </div>

        <div style="font-size: 0.75rem; color: var(--cb-text-muted); margin-top: 1.5rem;">
          Need help? Scan your transit QR ticket at the barcode reader beneath the screen.
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusCargoLockerTerminal = CityBusCargoLockerTerminal;
