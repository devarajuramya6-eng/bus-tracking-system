/**
 * CityBus Enterprise Platform - Interactive Gantt Schedule Visualizer
 * File: js/components/gantt_scheduler.js
 * 
 * Renders visual vehicle block and crew duty timelines across 24-hour spans:
 * - Block execution bars with departure and arrival spans
 * - Layover buffer and deadheading segments
 * - Interactive hover tooltips with trip details
 */

class CityBusGanttScheduler {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.startHour = options.startHour || 5; // 05:00
    this.endHour = options.endHour || 24; // 24:00
    this.blocks = options.blocks || [];
  }

  setBlocks(blocks) {
    this.blocks = blocks;
    this.render();
  }

  render() {
    if (!this.container) return;

    const totalHours = this.endHour - this.startHour;
    const totalMinutes = totalHours * 60;

    this.container.innerHTML = `
      <div style="background: var(--cb-bg-surface); border-radius: var(--cb-radius-lg); padding: 1.5rem; border: 1px solid var(--cb-border-color); overflow-x: auto;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--cb-text-primary); margin: 0;">Daily Vehicle Block Schedule Matrix</h3>
          <span class="badge badge-primary">${this.blocks.length} Active Blocks</span>
        </div>

        <!-- Time Header Scale -->
        <div style="display: grid; grid-template-columns: 120px 1fr; border-bottom: 2px solid var(--cb-border-color); padding-bottom: 0.5rem; margin-bottom: 0.75rem;">
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--cb-text-muted);">BLOCK / BUS</div>
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--cb-text-muted);">
            ${Array.from({ length: totalHours + 1 }).map((_, i) => `
              <span>${String(this.startHour + i).padStart(2, '0')}:00</span>
            `).join('')}
          </div>
        </div>

        <!-- Block Rows -->
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          ${this.blocks.map(b => {
            return `
              <div style="display: grid; grid-template-columns: 120px 1fr; align-items: center;">
                <div style="font-size: 0.85rem; font-weight: 700; color: var(--cb-text-primary);">${b.block_id || 'BLK-01'}</div>
                <div style="position: relative; height: 32px; background: var(--cb-bg-subtle); border-radius: var(--cb-radius-sm); border: 1px solid var(--cb-border-color);">
                  ${(b.trips || []).map(t => {
                    const startMin = (t.departure_min || 360) - (this.startHour * 60);
                    const durMin = (t.arrival_min || 420) - (t.departure_min || 360);
                    const leftPct = Math.max(0, Math.min(100, (startMin / totalMinutes) * 100));
                    const widthPct = Math.max(2, Math.min(100, (durMin / totalMinutes) * 100));

                    return `
                      <div title="${t.route_number}: ${t.start_stop} ➔ ${t.end_stop}" style="position: absolute; left: ${leftPct}%; width: ${widthPct}%; height: 24px; top: 3px; background: var(--cb-brand-primary); color: #fff; border-radius: 4px; font-size: 0.7rem; font-weight: 600; display: flex; align-items: center; justify-content: center; overflow: hidden; white-space: nowrap; padding: 0 4px; cursor: pointer;">
                        ${t.route_number || 'TRIP'}
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusGanttScheduler = CityBusGanttScheduler;
