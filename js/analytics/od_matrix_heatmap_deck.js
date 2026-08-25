/**
 * CityBus Enterprise Platform - Origin-Destination (OD) Passenger Flow Heatmap Deck
 * File: js/analytics/od_matrix_heatmap_deck.js
 * 
 * Visualizes commuter travel desire lines and transfer volume matrix:
 * - Interactive N x N Origin-Destination flow matrix
 * - Passenger transfer hub synchronization insights
 */

class CityBusODMatrixHeatmapDeck {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.stops = ['PNBS Terminal', 'Benz Circle', 'Autonagar', 'Gannavaram', 'Guntur'];
    this.matrix = [
      [0, 1240, 890, 420, 680],
      [450, 0, 1100, 310, 520],
      [780, 950, 0, 180, 240],
      [310, 280, 150, 0, 90],
      [590, 480, 210, 80, 0]
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Origin-Destination (OD) Commuter Flow Heatmap</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Inverted from 45,000 Daily APC Boarding / Alighting Records</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Exporting OD Trip Matrix CSV.')">📊 Export OD Matrix</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="text-align: left; padding: 0.75rem;">ORIGIN \\ DEST</th>
                ${this.stops.map(s => `<th style="padding: 0.75rem;">${s}</th>`).join('')}
              </tr>
            </thead>
            <tbody>
              ${this.matrix.map((row, i) => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="text-align: left; padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${this.stops[i]}</td>
                  ${row.map((val, j) => {
                    const bg = i === j ? '#F1F5F9' : (val > 800 ? 'rgba(56, 189, 248, 0.25)' : (val > 400 ? 'rgba(56, 189, 248, 0.12)' : 'transparent'));
                    return `<td style="padding: 0.75rem; background: ${bg}; font-weight: ${val > 500 ? '800' : '500'};">${i === j ? '-' : val}</td>`;
                  }).join('')}
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusODMatrixHeatmapDeck = CityBusODMatrixHeatmapDeck;
