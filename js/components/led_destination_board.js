/**
 * CityBus Enterprise Platform - High-Fidelity Dot-Matrix LED Destination Board
 * File: js/components/led_destination_board.js
 * 
 * Renders realistic commercial transit LED signboards:
 * - Amber / Green / Full-color dot matrix rendering
 * - Multi-lingual Telugu / English destination text flipping
 * - Route number pill display with scrolling via-stops
 */

class CityBusLEDDestinationBoard {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.routeNumber = options.routeNumber || '27A';
    this.destEn = options.destEn || 'GUNTUR BUS STATION';
    this.destTe = options.destTe || 'గుంటూరు బస్ స్టేషన్';
    this.viaStops = options.viaStops || 'VIA: BENZ CIRCLE • MANGALAGIRI • TADEPALLI';
    this.isTelugu = false;
    this.timer = null;
  }

  startFlipping() {
    this.timer = setInterval(() => {
      this.isTelugu = !this.isTelugu;
      this.updateDisplay();
    }, 4000);
  }

  stopFlipping() {
    if (this.timer) clearInterval(this.timer);
  }

  updateDisplay() {
    const textEl = document.getElementById('led-dest-text');
    if (textEl) {
      textEl.style.opacity = '0';
      setTimeout(() => {
        textEl.innerText = this.isTelugu ? this.destTe : this.destEn;
        textEl.style.opacity = '1';
      }, 300);
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="background: #09090B; border: 4px solid #27272A; border-radius: 12px; padding: 1rem 1.5rem; box-shadow: inset 0 0 30px rgba(0,0,0,0.9), 0 10px 25px rgba(0,0,0,0.5); font-family: monospace; display: flex; align-items: center; gap: 1.5rem;">
        
        <!-- Route Number Box -->
        <div style="background: #18181B; border: 2px solid #F59E0B; border-radius: 8px; padding: 0.5rem 1rem; color: #F59E0B; text-shadow: 0 0 10px #F59E0B, 0 0 20px #F59E0B; font-size: 2.2rem; font-weight: 900; letter-spacing: 2px;">
          ${this.routeNumber}
        </div>

        <!-- Destination & Via Area -->
        <div style="flex: 1; overflow: hidden;">
          <div id="led-dest-text" style="color: #F59E0B; text-shadow: 0 0 8px #F59E0B, 0 0 16px #F59E0B; font-size: 1.6rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; transition: opacity 0.3s ease; white-space: nowrap;">
            ${this.destEn}
          </div>
          <div style="color: #10B981; text-shadow: 0 0 6px #10B981; font-size: 0.85rem; font-weight: 700; letter-spacing: 1px; margin-top: 4px; white-space: nowrap;">
            ${this.viaStops}
          </div>
        </div>

      </div>
    `;

    this.startFlipping();
  }
}

// Global Export
window.CityBusLEDDestinationBoard = CityBusLEDDestinationBoard;
