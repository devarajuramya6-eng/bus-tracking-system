/**
 * CityBus Enterprise Platform - Regenerative Braking & Supercapacitor HUD
 * File: js/components/regen_energy_hud.js
 * 
 * Displays real-time electric braking and kinetic energy recovery:
 * - Electric motor regen torque (Nm) vs Pneumatic friction disc share
 * - 48V Supercapacitor buffer voltage & state of charge
 * - Shift kWh recovered energy gauge
 */

class CityBusRegenEnergyHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.regenData = {
      busNumber: 'AP16-E-104',
      speedKmh: 34.0,
      regenTorqueNm: 1850.0,
      frictionTorqueNm: 0.0,
      regenSharePct: 100.0,
      supercapVolts: 44.2,
      supercapSocPct: 84,
      shiftEnergyRecoveredKwh: 24.8
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #10B981; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Kinetic Energy Recovery (KERS) & Regen HUD</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.regenData.busNumber} (Electric Traction Inverter #1)</span>
          </div>
          <span class="badge badge-success" style="animation: pulse 1.5s infinite;">⚡ 100% REGEN BRAKING</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Regen Torque</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.regenData.regenTorqueNm} Nm</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Friction Disc: <strong>0 Nm (Zero Wear)</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Supercap Buffer</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.regenData.supercapVolts} V</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Buffer Charge: <strong>${this.regenData.supercapSocPct}%</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Shift Energy Saved</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">+${this.regenData.shiftEnergyRecoveredKwh} kWh</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Savings: <strong>₹${(this.regenData.shiftEnergyRecoveredKwh * 6.2).toFixed(0)}</strong></div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusRegenEnergyHUD = CityBusRegenEnergyHUD;
