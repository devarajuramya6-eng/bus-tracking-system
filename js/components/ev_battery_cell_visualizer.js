/**
 * CityBus Enterprise Platform - 800V Traction Battery Cell Equalizer & Thermal Visualizer
 * File: js/components/ev_battery_cell_visualizer.js
 * 
 * Visualizes individual series cell voltages and thermal gradients across high-voltage pack:
 * - 16 Monitored Module Cells (V_min, V_max, Delta V mV)
 * - Real-time active capacitive cell charge balancing animation
 * - Cell temperature heat map (°C)
 */

class CityBusEVCellVisualizer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.cells = [
      { id: 1, v: 3.285, temp: 34.2 }, { id: 2, v: 3.290, temp: 34.5 },
      { id: 3, v: 3.288, temp: 35.1 }, { id: 4, v: 3.292, temp: 35.8 },
      { id: 5, v: 3.275, temp: 36.2 }, { id: 6, v: 3.289, temp: 35.0 },
      { id: 7, v: 3.291, temp: 34.8 }, { id: 8, v: 3.284, temp: 34.4 },
      { id: 9, v: 3.287, temp: 34.1 }, { id: 10, v: 3.290, temp: 34.6 },
      { id: 11, v: 3.282, temp: 35.3 }, { id: 12, v: 3.294, temp: 36.0 },
      { id: 13, v: 3.286, temp: 35.2 }, { id: 14, v: 3.289, temp: 34.9 },
      { id: 15, v: 3.288, temp: 34.5 }, { id: 16, v: 3.291, temp: 34.2 }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    const voltages = this.cells.map(c => c.v);
    const vMin = Math.min(...voltages);
    const vMax = Math.max(...voltages);
    const deltaV = ((vMax - vMin) * 1000).toFixed(1);

    this.container.innerHTML = `
      <div style="background: #020617; border: 2px solid #1E293B; border-radius: var(--cb-radius-lg); padding: 1.5rem; color: #fff;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0;">800V High-Voltage Battery Cell Matrix</h4>
            <span style="font-size: 0.8rem; color: #94A3B8;">Pack #1 (240 kWh LFP Chemistry)</span>
          </div>
          <div style="text-align: right;">
            <span class="badge badge-success">⚡ Active Balancing</span>
            <div style="font-size: 0.8rem; color: #38BDF8; margin-top: 2px;">Delta V: <strong>${deltaV} mV</strong></div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(85px, 1fr)); gap: 0.75rem;">
          ${this.cells.map(c => {
            const isLowest = c.v === vMin;
            const isHighest = c.v === vMax;
            const borderColor = isLowest ? '#EF4444' : (isHighest ? '#38BDF8' : '#334155');

            return `
              <div style="background: #0F172A; border: 1.5px solid ${borderColor}; border-radius: 8px; padding: 0.5rem; text-align: center;">
                <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 700;">C-${c.id}</div>
                <div style="font-size: 0.95rem; font-weight: 900; color: #F8FAFC; margin: 2px 0;">${c.v.toFixed(3)}V</div>
                <div style="font-size: 0.7rem; color: #10B981;">${c.temp.toFixed(1)}°C</div>
              </div>
            `;
          }).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusEVCellVisualizer = CityBusEVCellVisualizer;
