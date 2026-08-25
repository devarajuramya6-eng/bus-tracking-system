/**
 * CityBus Enterprise Platform - Wheelchair Ramp & WTORS Restraint HUD
 * File: js/components/wheelchair_ramp_actuator_hud.js
 * 
 * Displays powered low-floor ramp deployment state and passenger bay restraint locks:
 * - 1:6 Slope gradient compliance (<12%)
 * - ISO 10542 4-point wheelchair harness lock status
 */

class CityBusWheelchairRampHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.rampData = {
      busNumber: 'AP16-003',
      rampState: 'STOWED_LOCKED',
      slopeGradientPct: 9.5,
      isBayOccupied: true,
      anchorsLocked: true,
      seatbeltBuckled: true
    };
    this.render();
  }

  toggleRamp() {
    this.rampData.rampState = this.rampData.rampState === 'STOWED_LOCKED' ? 'FULLY_DEPLOYED' : 'STOWED_LOCKED';
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #38BDF8; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Wheelchair Boarding Ramp & WTORS Restraint HUD</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.rampData.busNumber} (AIS 052 Accessible Low-Floor)</span>
          </div>
          <span class="badge ${this.rampData.rampState === 'FULLY_DEPLOYED' ? 'badge-warning' : 'badge-success'}">
            ${this.rampData.rampState}
          </span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Ramp Slope Gradient</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.rampData.slopeGradientPct}%</div>
            <div style="font-size: 0.75rem; color: #10B981;">Compliant (&le; 12.0%)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Wheelchair Bay Status</div>
            <div style="font-size: 1.2rem; font-weight: 900; color: #38BDF8; margin: 8px 0;">OCCUPIED (1 PAX)</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Bay 1 Dedicated</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">4-Point Restraint</div>
            <div style="font-size: 1.2rem; font-weight: 900; color: #10B981; margin: 8px 0;">SECURED &amp; LOCKED</div>
            <div style="font-size: 0.75rem; color: #10B981;">ISO 10542 Certified</div>
          </div>

        </div>

        <button class="btn ${this.rampData.rampState === 'STOWED_LOCKED' ? 'btn-primary' : 'btn-success'}" style="width: 100%; padding: 0.75rem;" onclick="window.wheelchairRampHUDInstance.toggleRamp()">
          ${this.rampData.rampState === 'STOWED_LOCKED' ? '♿ Deploy Powered Wheelchair Ramp' : '♿ Retract & Stow Wheelchair Ramp'}
        </button>

      </div>
    `;
  }
}

// Global Export
window.CityBusWheelchairRampHUD = CityBusWheelchairRampHUD;
