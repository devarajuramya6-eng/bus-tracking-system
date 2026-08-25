/**
 * CityBus Enterprise Platform - Automated Passenger Counting (APC) Doorway Visualizer
 * File: js/components/apc_doorway_visualizer.js
 * 
 * Renders dual-beam infrared overhead doorway sensors:
 * - Real-time Beam A and Beam B optical break pulses
 * - Passenger Boarding (IN) and Alighting (OUT) counter dials
 * - Air Suspension pneumatic weight sensor verification HUD
 */

class CityBusAPCDoorwayVisualizer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.inCount = 28;
    this.outCount = 6;
    this.weightKg = 14960;
    this.init();
  }

  simulateBoarding() {
    this.inCount += 1;
    this.weightKg += 68;
    this.render();
  }

  simulateAlighting() {
    if (this.inCount > this.outCount) {
      this.outCount += 1;
      this.weightKg -= 68;
      this.render();
    }
  }

  init() {
    this.render();
  }

  render() {
    if (!this.container) return;

    const netPax = this.inCount - this.outCount;

    this.container.innerHTML = `
      <div style="background: #0B1120; border: 2px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.2rem;">🚪</span>
            <span style="font-weight: 800; font-size: 1rem;">APC OVERHEAD DUAL-BEAM SENSOR HUD</span>
          </div>
          <span class="badge badge-success">● Optical Grid Active</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; text-align: center; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Passengers Boarded (IN)</div>
            <div style="font-size: 2rem; font-weight: 900; color: #10B981; margin: 4px 0;">+${this.inCount}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Front Door Beam A➔B</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Passengers Alighted (OUT)</div>
            <div style="font-size: 2rem; font-weight: 900; color: #EF4444; margin: 4px 0;">-${this.outCount}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Rear Door Beam B➔A</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Current Net Onboard</div>
            <div style="font-size: 2rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${netPax} pax</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Air Bellows: <strong>${(this.weightKg/1000).toFixed(1)}t</strong></div>
          </div>

        </div>

        <div style="display: flex; gap: 0.75rem; justify-content: center;">
          <button class="btn btn-sm btn-success" onclick="window.apcVisualizerInstance.simulateBoarding()">➕ Simulate Passenger Entry (IN)</button>
          <button class="btn btn-sm btn-outline-danger" onclick="window.apcVisualizerInstance.simulateAlighting()">➖ Simulate Passenger Exit (OUT)</button>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusAPCDoorwayVisualizer = CityBusAPCDoorwayVisualizer;
