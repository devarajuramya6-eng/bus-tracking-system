/**
 * CityBus Enterprise Platform - Cabin HVAC Thermal Comfort (PMV) & Air Quality HUD
 * File: js/components/hvac_thermal_comfort_hud.js
 * 
 * Displays interior passenger thermal comfort indices and air quality:
 * - Fanger's PMV Index (-0.5 to +0.5 Optimal Comfort)
 * - In-cabin CO2 ppm concentration & fresh air roof damper status
 * - AC Inverter power modulation (kW)
 */

class CityBusHVACComfortHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.hvacData = {
      cabinTempC: 23.8,
      ambientTempC: 38.5,
      relativeHumidityPct: 52,
      co2Ppm: 720,
      pmv: 0.12,
      acPowerKw: 7.2,
      damperPct: 40
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">ASHRAE 55 Cabin Climate & Air Quality HUD</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">Electric Bus AP16-E-101 (Dual Inverter AC)</span>
          </div>
          <span class="badge badge-success">🌿 Optimal Comfort</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Cabin Temperature</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.hvacData.cabinTempC}°C</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Outside Ambient: <strong>${this.hvacData.ambientTempC}°C</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Fanger's PMV Index</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">+${this.hvacData.pmv}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Target: <strong>-0.5 to +0.5</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Cabin CO2 Air Quality</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.hvacData.co2Ppm} ppm</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Fresh Air Roof Damper: <strong>${this.hvacData.damperPct}%</strong></div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusHVACComfortHUD = CityBusHVACComfortHUD;
