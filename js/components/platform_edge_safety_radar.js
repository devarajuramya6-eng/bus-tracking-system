/**
 * CityBus Enterprise Platform - 360-Degree Blind-Spot & Platform Edge Safety Radar
 * File: js/components/platform_edge_safety_radar.js
 * 
 * Displays cockpit 360 perimeter pedestrian warning zones & door traction interlock:
 * - Front Blind Spot, Left Kerb, Right A-Pillar, Rear Reverse Sonar
 * - Doorway Anti-Pinch & Traction Inhibit interlock state
 */

class CityBusPlatformSafetyRadar {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.zones = {
      front: { status: 'CLEAR', distM: 4.5 },
      leftKerb: { status: 'PEDESTRIAN_DETECTED', distM: 1.4, color: '#EF4444' },
      rightAPillar: { status: 'CLEAR', distM: 6.2 },
      rear: { status: 'CLEAR', distM: 8.0 }
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #EF4444; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">360° Blind-Spot & Platform Edge Safety Radar</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">77 GHz mmWave Radar & Ultrasonic Proximity Grid</span>
          </div>
          <span class="badge badge-danger" style="animation: pulse 1s infinite;">⚠️ PEDESTRIAN NEAR KERB</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Front Cross-Traffic</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #10B981; margin: 4px 0;">CLEAR (4.5m)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #EF4444;">
            <div style="font-size: 0.75rem; color: #FCA5A5; text-transform: uppercase;">Left Kerb Turn Blind Spot</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #EF4444; margin: 4px 0;">PEDESTRIAN (1.4m)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Right A-Pillar</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #10B981; margin: 4px 0;">CLEAR (6.2m)</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Rear Reverse Sonar</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #10B981; margin: 4px 0;">CLEAR (8.0m)</div>
          </div>

        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; background: #0F172A; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem;">
          <span>Door Interlock: <strong style="color: #10B981;">DOORS LOCKED</strong></span>
          <span>Traction Motor: <strong style="color: #10B981;">DRIVE ENABLED</strong></span>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusPlatformSafetyRadar = CityBusPlatformSafetyRadar;
