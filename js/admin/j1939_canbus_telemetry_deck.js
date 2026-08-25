/**
 * CityBus Enterprise Platform - SAE J1939 CAN-Bus High-Frequency Telemetry Deck
 * File: js/admin/j1939_canbus_telemetry_deck.js
 * 
 * Displays heavy commercial vehicle CAN-bus powertrain telemetry:
 * - Engine RPM (SPN 190) & Engine Demand Torque (SPN 513)
 * - Hydraulic Retarder Braking Torque (SPN 520) & Oil Temp
 * - Turbocharger Boost Pressure (SPN 102) & Exhaust Gas Temperature (EGT)
 */

class CityBusJ1939Deck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.j1939Data = {
      engineRpm: 1650,
      actualTorquePct: 68,
      boostPressureBar: 1.85,
      egtTempC: 480,
      coolantTempC: 88.5,
      retarderTorquePct: 0.0,
      retarderOilTempC: 78.0
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">SAE J1939 Heavy Powertrain CAN-Bus Radar</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">Bus AP16-002 (Cummins 6BTAA / Allison Transmission)</span>
          </div>
          <span class="badge badge-success">● J1939 Stream 250 kbps</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Engine Speed (SPN 190)</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.j1939Data.engineRpm} RPM</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Load Torque: <strong>${this.j1939Data.actualTorquePct}%</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Turbo Boost (SPN 102)</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.j1939Data.boostPressureBar} bar</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Exhaust EGT: <strong>${this.j1939Data.egtTempC}°C</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Hydraulic Retarder</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">STANDBY</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Oil Temp: <strong>${this.j1939Data.retarderOilTempC}°C</strong></div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusJ1939Deck = CityBusJ1939Deck;
