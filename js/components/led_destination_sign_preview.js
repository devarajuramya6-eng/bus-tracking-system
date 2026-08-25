/**
 * CityBus Enterprise Platform - 128x16 Bus Destination LED Sign Simulator
 * File: js/components/led_destination_sign_preview.js
 * 
 * Simulates physical 128x16 amber LED matrix destination sign hardware:
 * - Alternating English and Telugu destination text
 * - Front, Side, and Rear sign preview
 */

class CityBusLEDSignPreview {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.signTextEn = '27A  PNBS ➔ GUNTUR EXP';
    this.signTextTe = '27A  గుంటూరు ఎక్స్‌ప్రెస్';
    this.isTelugu = false;
    this.render();

    setInterval(() => {
      this.isTelugu = !this.isTelugu;
      this.updateSign();
    }, 3500);
  }

  updateSign() {
    const el = document.getElementById('led-sign-text-display');
    if (el) {
      el.textContent = this.isTelugu ? this.signTextTe : this.signTextEn;
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #334155; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">Electronic LED Destination Sign (128x16 Matrix)</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">Front Header Sign Board (Bilingual Flip Mode)</span>
          </div>
          <span class="badge badge-warning">● RS-485 SYNC OK</span>
        </div>

        <!-- 128x16 Simulated LED Display Window -->
        <div style="background: #000; border: 4px solid #1E293B; border-radius: 8px; padding: 1.25rem; text-align: center; box-shadow: inset 0 0 20px rgba(0,0,0,0.9);">
          <div id="led-sign-text-display" style="font-family: monospace; font-size: 1.6rem; font-weight: 900; color: #F59E0B; letter-spacing: 4px; text-shadow: 0 0 8px #F59E0B;">
            ${this.signTextEn}
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; font-size: 0.8rem; color: #94A3B8;">
          <span>Dot Pitch: 10mm | 2048 High-Luminance Amber LEDs</span>
          <span>Bilingual Alternating Interval: <strong>3.5s</strong></span>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusLEDSignPreview = CityBusLEDSignPreview;
