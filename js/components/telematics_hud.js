/**
 * CityBus Enterprise Platform - High-Precision Vehicle Telematics HUD Gauges
 * File: js/components/telematics_hud.js
 * 
 * Renders interactive SVG/Canvas automotive cockpit dials:
 * - Analog Speedometer (0 - 120 km/h) with redline limit
 * - Engine Tachometer (0 - 3000 RPM)
 * - Traction Battery State of Charge (SoC %) Dial
 * - Coolant Temperature & Oil Pressure HUD
 */

class CityBusTelematicsHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.currentSpeed = 0;
    this.currentRPM = 650;
    this.currentSoC = 88;
    this.currentTemp = 85;
  }

  updateMetrics(metrics) {
    if (metrics.speed !== undefined) this.currentSpeed = metrics.speed;
    if (metrics.rpm !== undefined) this.currentRPM = metrics.rpm;
    if (metrics.soc !== undefined) this.currentSoC = metrics.soc;
    if (metrics.temp !== undefined) this.currentTemp = metrics.temp;
    this.render();
  }

  render() {
    if (!this.container) return;

    const speedAngle = -120 + (Math.min(120, this.currentSpeed) / 120) * 240;
    const rpmAngle = -120 + (Math.min(3000, this.currentRPM) / 3000) * 240;

    this.container.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; background: #0B1120; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff; border: 1px solid #1E293B;">
        
        <!-- Speedometer Dial -->
        <div style="text-align: center; position: relative;">
          <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Velocity HUD</div>
          <svg width="150" height="150" viewBox="0 0 150 150">
            <!-- Background Arc -->
            <path d="M 25 125 A 60 60 0 1 1 125 125" fill="none" stroke="#334155" stroke-width="10" stroke-linecap="round"/>
            <!-- Active Arc -->
            <path d="M 25 125 A 60 60 0 1 1 125 125" fill="none" stroke="#2563EB" stroke-width="10" stroke-linecap="round" stroke-dasharray="280" stroke-dashoffset="${280 - (Math.min(120, this.currentSpeed)/120)*280}"/>
            <!-- Needle -->
            <line x1="75" y1="75" x2="75" y2="25" stroke="#EF4444" stroke-width="3" stroke-linecap="round" transform="rotate(${speedAngle} 75 75)" style="transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);"/>
            <circle cx="75" cy="75" r="7" fill="#EF4444"/>
            <text x="75" y="110" text-anchor="middle" fill="#FFFFFF" font-size="20" font-weight="bold">${Math.round(this.currentSpeed)}</text>
            <text x="75" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">KM/H</text>
          </svg>
        </div>

        <!-- Tachometer RPM Dial -->
        <div style="text-align: center; position: relative;">
          <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Engine Tachometer</div>
          <svg width="150" height="150" viewBox="0 0 150 150">
            <path d="M 25 125 A 60 60 0 1 1 125 125" fill="none" stroke="#334155" stroke-width="10" stroke-linecap="round"/>
            <path d="M 25 125 A 60 60 0 1 1 125 125" fill="none" stroke="#10B981" stroke-width="10" stroke-linecap="round" stroke-dasharray="280" stroke-dashoffset="${280 - (Math.min(3000, this.currentRPM)/3000)*280}"/>
            <line x1="75" y1="75" x2="75" y2="25" stroke="#10B981" stroke-width="3" stroke-linecap="round" transform="rotate(${rpmAngle} 75 75)" style="transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);"/>
            <circle cx="75" cy="75" r="7" fill="#10B981"/>
            <text x="75" y="110" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="bold">${Math.round(this.currentRPM)}</text>
            <text x="75" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">RPM</text>
          </svg>
        </div>

        <!-- Battery SoC & Temp Card -->
        <div style="display: flex; flex-direction: column; justify-content: center; gap: 0.75rem; background: #1E293B; padding: 1rem; border-radius: var(--cb-radius-md);">
          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
              <span style="color: #94A3B8;">Traction Battery SoC</span>
              <span style="color: #10B981; font-weight: bold;">${this.currentSoC}%</span>
            </div>
            <div style="width: 100%; height: 8px; background: #334155; border-radius: 4px; overflow: hidden;">
              <div style="width: ${this.currentSoC}%; height: 100%; background: #10B981; transition: width 0.4s ease;"></div>
            </div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
              <span style="color: #94A3B8;">Engine Coolant Temp</span>
              <span style="color: ${this.currentTemp > 95 ? '#EF4444' : '#F59E0B'}; font-weight: bold;">${this.currentTemp}°C</span>
            </div>
            <div style="width: 100%; height: 8px; background: #334155; border-radius: 4px; overflow: hidden;">
              <div style="width: ${(this.currentTemp/120)*100}%; height: 100%; background: ${this.currentTemp > 95 ? '#EF4444' : '#F59E0B'}; transition: width 0.4s ease;"></div>
            </div>
          </div>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusTelematicsHUD = CityBusTelematicsHUD;
