/**
 * CityBus Enterprise Platform - Air Suspension & ELC Pneumatic Kneeling HUD
 * File: js/components/air_suspension_kneeling_hud.js
 * 
 * Displays electronic leveling control (ELC) and boarding height status in cockpit:
 * - 70mm Pneumatic Kneeling toggle button
 * - Ultrasonic platform curb distance alignment gauge
 */

class CityBusAirSuspensionHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.suspension = {
      busNumber: 'AP16-002',
      currentHeightMm: 340,
      isKneeled: false,
      curbDistanceMm: 45.0,
      airPressureBar: 6.8
    };
    this.render();
  }

  toggleKneel() {
    this.suspension.isKneeled = !this.suspension.isKneeled;
    this.suspension.currentHeightMm = this.suspension.isKneeled ? 270 : 340;
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #38BDF8; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Electronic Leveling Control (ELC) & Kneeling HUD</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.suspension.busNumber} (WABCO ECAS Low-Floor)</span>
          </div>
          <span class="badge ${this.suspension.isKneeled ? 'badge-warning' : 'badge-success'}">
            ${this.suspension.isKneeled ? '● KNEELED (270mm)' : '● RIDE HEIGHT (340mm)'}
          </span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Door Step Height</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.suspension.currentHeightMm} mm</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">ELC Stroke: <strong>-70 mm Drop</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Platform Kerb Gap</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.suspension.curbDistanceMm} mm</div>
            <div style="font-size: 0.75rem; color: #10B981;">Step-Free Accessible</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Air Bellow Pressure</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">${this.suspension.airPressureBar} bar</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Compressor: Standby</div>
          </div>

        </div>

        <button class="btn ${this.suspension.isKneeled ? 'btn-success' : 'btn-primary'}" style="width: 100%; padding: 0.75rem;" onclick="window.airSuspensionHUDInstance.toggleKneel()">
          ${this.suspension.isKneeled ? '⬆️ Restore Standard Ride Height (340mm)' : '⬇️ Kneel Bus for Wheelchair / Elderly Boarding (-70mm)'}
        </button>

      </div>
    `;
  }
}

// Global Export
window.CityBusAirSuspensionHUD = CityBusAirSuspensionHUD;
