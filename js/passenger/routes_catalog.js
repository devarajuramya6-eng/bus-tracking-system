/**
 * CityBus Enterprise Platform - Routes Catalog & Timetable Logic
 * File: js/passenger/routes_catalog.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let routes = [];
  let activeCategory = 'All';

  async function loadRoutes() {
    try {
      if (window.CityBusAPI) {
        const res = await window.CityBusAPI.getRoutes();
        routes = res.routes || [];
      }
    } catch {
      routes = (window.CITYBUS_DATA && window.CITYBUS_DATA.routes) ? window.CITYBUS_DATA.routes : [];
    }

    renderRoutes();
  }

  function renderRoutes() {
    const grid = document.getElementById('routes-catalog-grid');
    if (!grid) return;

    let filtered = [...routes];
    if (activeCategory !== 'All') {
      filtered = filtered.filter(r => (r.category || 'Local').toLowerCase() === activeCategory.toLowerCase());
    }

    grid.innerHTML = filtered.map(r => {
      return `
        <div class="card hover-lift" style="border-top: 4px solid ${r.color || '#2563EB'};">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="font-weight: 800; font-size: 1.1rem; color: var(--cb-brand-primary);">Route ${r.number || r.route_number}</span>
              <span class="badge badge-primary">${r.category || 'Local'}</span>
            </div>
            <strong style="color: var(--cb-status-success); font-size: 1.1rem;">₹${r.fare || r.base_fare || 20}</strong>
          </div>

          <h3 style="font-size: 1rem; font-weight: 700; color: var(--cb-text-primary); margin-bottom: 0.5rem;">
            ${r.name}
          </h3>

          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--cb-text-muted); margin-bottom: 1rem;">
            <span><i class="fa-solid fa-route"></i> ${r.distance || `${r.distance_km || 15} km`}</span>
            <span><i class="fa-solid fa-clock"></i> ~${r.duration || `${r.estimated_time || 30} min`}</span>
            <span><i class="fa-solid fa-location-dot"></i> ${r.stops_count || 8} Stops</span>
          </div>

          <div style="display: flex; gap: 0.5rem;">
            <a href="journey-planner.html?from=${encodeURIComponent(r.origin || r.start_point || '')}&to=${encodeURIComponent(r.destination || '')}" class="btn btn-outline btn-sm" style="flex: 1; text-align: center;">
              <i class="fa-solid fa-map"></i> View Stops
            </a>
            <a href="tickets.html?from=${encodeURIComponent(r.origin || r.start_point || '')}&to=${encodeURIComponent(r.destination || '')}&fare=${r.fare || r.base_fare || 20}" class="btn btn-primary btn-sm" style="flex: 1; text-align: center;">
              <i class="fa-solid fa-ticket"></i> Book Pass
            </a>
          </div>
        </div>
      `;
    }).join('');
  }

  // Category filter buttons
  document.querySelectorAll('.route-category-filter').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.route-category-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.dataset.category || 'All';
      renderRoutes();
    };
  });

  await loadRoutes();
});
