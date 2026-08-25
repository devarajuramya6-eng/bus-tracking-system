/**
 * CityBus Enterprise Platform - Interactive Bus Seat & Occupancy Visualizer
 * File: js/conductor/occupancy_radar.js
 * 
 * Provides interactive seat allocation for conductors & passengers:
 * - 44-seater 2x2 AC Low-Floor seating grid
 * - Reserved seating categories (Women, Senior Citizens, Differently Abled / Wheelchair Bay)
 * - Clickable seat toggle for boarding / alighting management
 */

class CityBusOccupancyRadar {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.capacity = options.capacity || 44;
    this.seats = this.initSeats();
    this.onSeatChange = options.onSeatChange || null;
    this.render();
  }

  initSeats() {
    const seats = [];
    for (let i = 1; i <= this.capacity; i++) {
      let type = 'REGULAR';
      if (i <= 4) type = 'SENIOR';
      else if (i >= 5 && i <= 10) type = 'WOMEN';
      else if (i === 11 || i === 12) type = 'WHEELCHAIR';

      seats.push({
        number: i,
        type,
        isOccupied: i <= 18 // Initial seeded occupancy
      });
    }
    return seats;
  }

  toggleSeat(seatNumber) {
    const seat = this.seats.find(s => s.number === seatNumber);
    if (seat) {
      seat.isOccupied = !seat.isOccupied;
      this.render();
      if (this.onSeatChange) {
        this.onSeatChange(this.getOccupiedCount(), this.capacity);
      }
    }
  }

  getOccupiedCount() {
    return this.seats.filter(s => s.isOccupied).length;
  }

  render() {
    if (!this.container) return;

    const occupied = this.getOccupiedCount();
    const pct = Math.round((occupied / this.capacity) * 100);

    this.container.innerHTML = `
      <div style="background: var(--cb-bg-subtle); border-radius: var(--cb-radius-lg); padding: 1.25rem; border: 1px solid var(--cb-border-color);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div>
            <span style="font-weight: 700; font-size: 1rem;">Live Deck Seating Map</span>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">44 Seats (2x2 Low-Floor Electric)</div>
          </div>
          <div style="text-align: right;">
            <span class="badge ${pct > 85 ? 'badge-danger' : pct > 50 ? 'badge-warning' : 'badge-success'}">${occupied} / ${this.capacity} (${pct}%)</span>
          </div>
        </div>

        <!-- Legend -->
        <div style="display: flex; gap: 0.75rem; font-size: 0.75rem; margin-bottom: 1.25rem; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 4px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--cb-brand-primary);"></span> Occupied</div>
          <div style="display: flex; align-items: center; gap: 4px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--cb-bg-surface); border: 1px solid var(--cb-border-color);"></span> Available</div>
          <div style="display: flex; align-items: center; gap: 4px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ec4899;"></span> Women</div>
          <div style="display: flex; align-items: center; gap: 4px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #f59e0b;"></span> Senior</div>
          <div style="display: flex; align-items: center; gap: 4px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #06b6d4;"></span> Wheelchair</div>
        </div>

        <!-- Seat Grid -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; max-width: 320px; margin: 0 auto; background: var(--cb-bg-surface); padding: 1rem; border-radius: var(--cb-radius-md); border: 1px solid var(--cb-border-color);">
          ${this.seats.map((s, idx) => {
            const isAisleGap = idx % 2 === 1 && idx % 4 !== 3;
            let bgColor = 'var(--cb-bg-surface)';
            let textColor = 'var(--cb-text-primary)';
            let borderColor = 'var(--cb-border-color)';

            if (s.isOccupied) {
              bgColor = 'var(--cb-brand-primary)';
              textColor = '#fff';
              borderColor = 'var(--cb-brand-primary)';
            } else if (s.type === 'WOMEN') {
              borderColor = '#ec4899';
            } else if (s.type === 'SENIOR') {
              borderColor = '#f59e0b';
            } else if (s.type === 'WHEELCHAIR') {
              borderColor = '#06b6d4';
            }

            return `
              <button onclick="window.CityBusOccupancyInstance.toggleSeat(${s.number})" style="padding: 0.5rem 0.25rem; font-size: 0.75rem; font-weight: 700; border-radius: var(--cb-radius-sm); border: 1.5px solid ${borderColor}; background: ${bgColor}; color: ${textColor}; cursor: pointer; transition: all var(--cb-transition-fast); margin-right: ${isAisleGap ? '12px' : '0'};">
                ${s.number}
              </button>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }
}

// Global Export
window.CityBusOccupancyRadar = CityBusOccupancyRadar;
