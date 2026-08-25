/**
 * CityBus Enterprise Platform - Electric Bus Heat Pump & Battery Glycol Chiller HUD
 * File: js/components/thermal_heat_pump_hud.js
 * 
 * Displays thermal management inverter and battery chiller loop metrics:
 * - 4-Way valve mode (Cooling, Heating, Motor Waste Heat Scavenging)
 * - Battery pack glycol loop temperature & flow rate (L/min)
 * - Compressor VFD electrical power draw (kW)
 */

class CityBusThermalHeatPumpHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.thermalData = {
      busNumber: 'AP16-E-102',
      ambientTempC: 38.5,
      cabinTempC: 23.0,
      batteryTempC: 27.8,
      glycolFlowLpm: 24.0,
      mode: 'ACTIVE_GLYCOL_CHILLER + REVERSE_CYCLE',
      compressorKw: 4.8,
      cop: 3.4
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #38BDF8; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Eco Heat Pump & Battery Glycol Chiller Radar</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.thermalData.busNumber} (R1234yf Eco-Refrigerant Loop)</span>
          </div>
          <span class="badge badge-success">● THERMAL LOOP OPTIMAL (COP 3.4)</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Battery Pack Temp</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.thermalData.batteryTempC}°C</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Optimal Target: 22-32°C</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Cabin Climate</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.thermalData.cabinTempC}°C</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Ambient: <strong>${this.thermalData.ambientTempC}°C</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Compressor Power</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">${this.thermalData.compressorKw} kW</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Glycol Flow: <strong>${this.thermalData.glycolFlowLpm} L/min</strong></div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusThermalHeatPumpHUD = CityBusThermalHeatPumpHUD;
