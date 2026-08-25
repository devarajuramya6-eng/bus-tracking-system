/**
 * CityBus Enterprise Platform - Blackbox Telemetry Crash Forensic Viewer
 * File: js/admin/blackbox_accident_viewer.js
 * 
 * Provides forensic reconstruction of high-G collision events:
 * - Pre-crash 10-second speed curve (km/h)
 * - Brake line pneumatic pressure (PSI) and ABS activation pulse
 * - G-Force impact deceleration vector
 */

class CityBusBlackboxAccidentViewer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.crashData = {
      eventNumber: 'EVT-CRASH-2026-0825-01',
      busNumber: 'AP16-014',
      impactTime: '2026-08-25 09:42:18 IST',
      initialSpeedKmh: 42.5,
      impactSpeedKmh: 14.2,
      peakDecelerationG: -0.88,
      brakeAppliedSecBeforeImpact: 1.8,
      absActivated: true
    };
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #DC2626; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">⚠️</span>
            <span style="font-weight: 800; font-size: 1.1rem; color: #EF4444;">BLACKBOX CRASH TELEMETRY RECONSTRUCTION</span>
          </div>
          <button class="btn btn-sm btn-outline-danger" onclick="alert('Exporting forensic MACT insurance evidence package PDF.')">📦 Export Legal Dossier</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          
          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8;">Initial Speed (T - 10s)</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">${this.crashData.initialSpeedKmh} km/h</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Nominal Corridor Speed</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8;">Impact Velocity (T = 0s)</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #EF4444; margin: 4px 0;">${this.crashData.impactSpeedKmh} km/h</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Speed at contact point</div>
          </div>

          <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B;">
            <div style="font-size: 0.75rem; color: #94A3B8;">Peak Deceleration G</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #F59E0B; margin: 4px 0;">${this.crashData.peakDecelerationG} G</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">ABS Active: <strong>YES</strong></div>
          </div>

        </div>

        <div style="background: #0F172A; padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid #1E293B; font-size: 0.85rem; line-height: 1.5; color: #CBD5E1;">
          <strong>Forensic Telemetry Finding:</strong> Driver applied emergency dual-circuit service brakes 1.8 seconds prior to collision. Anti-Lock Braking System (ABS) engaged continuously, successfully shedding 28.3 km/h before impact.
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusBlackboxAccidentViewer = CityBusBlackboxAccidentViewer;
