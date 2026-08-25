/**
 * CityBus - Routes Explorer & Timetable (js/routes.js)
 * 
 * Handles route catalog, category filters (All Routes, Popular, Express, Local),
 * text search, and route stop schedule modal.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const routesContainer = document.getElementById('routes-grid');
  const searchInput = document.getElementById('route-search-input');
  const filterChips = document.querySelectorAll('.filter-chip');
  const resultsCount = document.getElementById('routes-count');

  let currentCategory = 'All Routes';
  let searchQuery = '';

  // Filter Chips Click Handlers
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentCategory = chip.dataset.filter || 'All Routes';
      renderRoutes();
    });
  });

  // Search Input Handler
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      renderRoutes();
    });
  }

  /**
   * Render Routes Grid
   */
  async function renderRoutes() {
    if (!routesContainer) return;

    let routes = await CityBusAPI.getRoutes({ category: currentCategory, search: searchQuery });

    if (resultsCount) {
      resultsCount.textContent = `Showing ${routes.length} routes`;
    }

    if (routes.length === 0) {
      routesContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; background: white; border-radius: var(--border-radius); border: 1px solid var(--border-color);">
          <div style="font-size: 2.5rem; color: var(--text-light); margin-bottom: 0.75rem;">
            <i class="fa-solid fa-route"></i>
          </div>
          <h3 style="font-weight: 700; color: var(--dark); margin-bottom: 0.25rem;">No routes found</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Try searching for a different destination or route code</p>
        </div>
      `;
      return;
    }

    routesContainer.innerHTML = routes.map(route => {
      let catBadgeClass = 'badge-primary';
      if (route.category === 'Express') catBadgeClass = 'badge-success';
      if (route.category === 'Popular') catBadgeClass = 'badge-warning';

      return `
        <div class="route-card">
          <div class="route-header">
            <span class="route-badge">${route.number}</span>
            <span class="badge ${catBadgeClass}">${route.category}</span>
          </div>

          <h3 class="route-path">${route.name}</h3>

          <div class="route-meta">
            <div class="route-meta-item">
              <i class="fa-solid fa-location-dot" style="color: var(--primary);"></i>
              <span>${route.stopsCount} Stops</span>
            </div>
            <div class="route-meta-item">
              <i class="fa-solid fa-clock" style="color: var(--warning);"></i>
              <span>~${route.duration}</span>
            </div>
            <div class="route-meta-item">
              <i class="fa-solid fa-road" style="color: var(--text-muted);"></i>
              <span>${route.distance}</span>
            </div>
          </div>

          <div class="bus-card-footer">
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--dark);">
              Fare: <span style="color: var(--success); font-size: 1rem;">${route.fare}</span>
            </div>
            <div style="display: flex; gap: 0.5rem;">
              <button class="btn btn-outline-primary btn-sm view-route-btn" data-route-id="${route.id}">
                <i class="fa-solid fa-list-ol"></i> View Stops
              </button>
              <a href="buses.html?q=${route.number}" class="btn btn-primary btn-sm">
                <i class="fa-solid fa-bus"></i> Live Buses
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Attach View Stops Click Handlers
    document.querySelectorAll('.view-route-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const routeId = btn.dataset.routeId;
        openRouteDetailsModal(routeId);
      });
    });
  }

  /**
   * Opens Route Stop Schedule Modal
   */
  async function openRouteDetailsModal(routeId) {
    const route = CITYBUS_DATA.routes.find(r => r.id === routeId);
    if (!route) return;

    let modal = document.getElementById('route-details-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'route-details-modal';
      modal.className = 'modal-backdrop';
      document.body.appendChild(modal);
    }

    // Resolve stop details
    const stopsList = route.stops.map((stopId, idx) => {
      const stop = CITYBUS_DATA.stops.find(s => s.id === stopId) || { name: stopId, code: 'STP' };
      const isStart = idx === 0;
      const isEnd = idx === route.stops.length - 1;
      
      let badge = `<span class="badge badge-dark">Stop ${idx + 1}</span>`;
      if (isStart) badge = `<span class="badge badge-success">Origin</span>`;
      if (isEnd) badge = `<span class="badge badge-danger">Terminal</span>`;

      return `
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background: var(--bg); border-radius: var(--border-radius-sm); margin-bottom: 0.5rem;">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: #FFFFFF; border: 2px solid var(--primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.75rem; color: var(--primary);">
              ${idx + 1}
            </div>
            <div>
              <div style="font-weight: 700; color: var(--dark); font-size: 0.9rem;">${stop.name}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Stop Code: ${stop.code}</div>
            </div>
          </div>
          ${badge}
        </div>
      `;
    }).join('');

    modal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-header">
          <div>
            <div class="modal-title">Route ${route.number} Schedule</div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">${route.name}</div>
          </div>
          <button class="modal-close-btn" id="close-route-modal"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="modal-body">
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; background: var(--primary-light); padding: 0.75rem; border-radius: var(--border-radius-sm); margin-bottom: 1.25rem; font-size: 0.85rem; text-align: center;">
            <div>
              <div style="color: var(--text-muted); font-size: 0.75rem;">Total Distance</div>
              <div style="font-weight: 800; color: var(--primary);">${route.distance}</div>
            </div>
            <div>
              <div style="color: var(--text-muted); font-size: 0.75rem;">Duration</div>
              <div style="font-weight: 800; color: var(--primary);">${route.duration}</div>
            </div>
            <div>
              <div style="color: var(--text-muted); font-size: 0.75rem;">Base Fare</div>
              <div style="font-weight: 800; color: var(--success);">${route.fare}</div>
            </div>
          </div>

          <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--dark); margin-bottom: 0.75rem;">Stop-by-Stop Itinerary (${route.stops.length} Stops)</h4>
          <div style="max-height: 280px; overflow-y: auto;">
            ${stopsList}
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" id="modal-btn-close">Close</button>
          <a href="buses.html?q=${route.number}" class="btn btn-primary">
            <i class="fa-solid fa-map-location-dot"></i> Track On Live Map
          </a>
        </div>
      </div>
    `;

    modal.classList.add('show');

    const closeModal = () => modal.classList.remove('show');
    document.getElementById('close-route-modal').addEventListener('click', closeModal);
    document.getElementById('modal-btn-close').addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  // Initial render
  await renderRoutes();
});
