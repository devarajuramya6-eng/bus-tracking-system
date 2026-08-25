/**
 * CityBus Enterprise Platform - Stops Catalog & Amenities Logic
 * File: js/passenger/stops_catalog.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let stops = [];

  const mapElement = document.getElementById('stops-catalog-map');
  let map = null;
  let stopLayer = null;

  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('stops-catalog-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (map) stopLayer = new StopLayerManager(map);
  }

  async function loadStops() {
    try {
      if (window.CityBusAPI) {
        const res = await window.CityBusAPI.getStops();
        stops = res.stops || [];
      }
    } catch {
      stops = (window.CITYBUS_DATA && window.CITYBUS_DATA.stops) ? window.CITYBUS_DATA.stops : [];
    }

    renderStops();
    if (stopLayer) stopLayer.renderStops(stops);
  }

  function renderStops() {
    const grid = document.getElementById('stops-catalog-grid');
    if (!grid) return;

    grid.innerHTML = stops.slice(0, 30).map(s => {
      return `
        <div class="card hover-lift" style="padding: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <strong style="color: var(--cb-text-primary); font-size: 0.95rem;">📍 ${s.name}</strong>
            <span class="badge badge-dark" style="font-size: 0.7rem;">${s.code}</span>
          </div>

          <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
            <span class="badge badge-primary" style="font-size: 0.65rem;"><i class="fa-solid fa-umbrella"></i> Shelter</span>
            <span class="badge badge-success" style="font-size: 0.65rem;"><i class="fa-solid fa-wheelchair"></i> Accessible</span>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--cb-border-subtle); padding-top: 0.5rem;">
            <span style="font-size: 0.75rem; color: var(--cb-text-muted);">Next in: <strong>~4 min</strong></span>
            <a href="journey-planner.html?from=${encodeURIComponent(s.name)}" class="btn btn-outline btn-xs">
              Depart from Here
            </a>
          </div>
        </div>
      `;
    }).join('');
  }

  await loadStops();
});
