/**
 * CityBus Enterprise Platform - Driver Cockpit GLOSA Green Wave HUD
 * File: js/components/glosa_green_wave_hud.js
 * 
 * Displays V2X Traffic Signal Phase and Timing (SPaT) Speed Advisory:
 * - Next intersection signal countdown (Seconds to Green / Red)
 * - Optimal approach speed recommendation to pass on green without stopping
 */

class CityBusGLOSAHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.glosaData = {
      intersectionName: 'Benz Circle Major Junction',
      distanceM: 320,
      currentPhase: 'RED',
      timeToGreenSec: 14,
      targetSpeedKmh: 32.0,
      currentSpeedKmh: 38.0
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #10B981; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">V2X Green Light Optimal Speed Advisory (GLOSA)</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.glosaData.intersectionName} (320m ahead)</span>
          </div>
          <span class="badge badge-success">● C-V2X 5.9 GHz Connected</span>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; align-items: center;">
          
          <div style="background: #0F172A; padding: 1.25rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Signal Countdown</div>
            <div style="font-size: 2.2rem; font-weight: 900; color: #EF4444; margin: 4px 0;">
              🔴 RED (${this.glosaData.timeToGreenSec}s)
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Turns GREEN in 14 seconds</div>
          </div>

          <div style="background: #0F172A; padding: 1.25rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Recommended Speed</div>
            <div style="font-size: 2.2rem; font-weight: 900; color: #10B981; margin: 4px 0;">
              ${this.glosaData.targetSpeedKmh} km/h
            </div>
            <div style="font-size: 0.75rem; color: #10B981;">Glide at 32 km/h to catch Green Wave</div>
          </div>

        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusGLOSAHUD = CityBusGLOSAHUD;
