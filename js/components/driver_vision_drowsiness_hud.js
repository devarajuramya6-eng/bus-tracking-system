/**
 * CityBus Enterprise Platform - Driver Vision AI & Drowsiness PERCLOS HUD
 * File: js/components/driver_vision_drowsiness_hud.js
 * 
 * Displays cockpit real-time edge AI driver attention and PERCLOS telemetry:
 * - PERCLOS percentage (P80 standard: <12% Alert, >12% Fatigued)
 * - Eye blink duration & gaze distraction tracking
 * - Driver seat haptic vibration alert indicators
 */

class CityBusDriverVisionHUD {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.visionData = {
      driverName: 'R. K. Sharma (ID: DRV-104)',
      perclosPct: 4.2,
      maxBlinkDurationSec: 0.28,
      gazeZone: 'FORWARD_ROADWAY',
      mobilePhoneDetected: false,
      alertState: 'ALERT_AND_ATTENTIVE'
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #10B981; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Driver Edge Vision AI & Alertness Monitor</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">${this.visionData.driverName} (PERCLOS P80 Near-IR Telemetry)</span>
          </div>
          <span class="badge badge-success">● DRIVER ATTENTIVE</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">PERCLOS Eye Closure</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #10B981; margin: 4px 0;">${this.visionData.perclosPct}%</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Threshold: <strong>&lt; 12.0% Nominal</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Max Blink Duration</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.visionData.maxBlinkDurationSec}s</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Microsleep: <strong>&gt; 1.50s</strong></div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Gaze Tracking</div>
            <div style="font-size: 1.2rem; font-weight: 900; color: #10B981; margin: 8px 0;">FORWARD ROAD</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Phone Distraction: <strong>NONE</strong></div>
          </div>

        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; background: #0F172A; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem;">
          <span>Seat Cushion Haptic Buzzer: <strong style="color: #10B981;">STANDBY READY</strong></span>
          <button class="btn btn-sm btn-outline-danger" onclick="alert('Test Haptic Seat Vibration Pulse Dispatched.')">📳 Test Seat Haptic</button>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusDriverVisionHUD = CityBusDriverVisionHUD;
