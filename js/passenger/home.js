/**
 * CityBus Enterprise Platform - Passenger Home & Hero Search Logic
 * File: js/passenger/home.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  const mapElement = document.getElementById('home-live-map');
  let map = null;
  let busLayer = null;

  // 1. Initialize Preview Leaflet Map
  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('home-live-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (map) {
      busLayer = new BusLayerManager(map);
      
      // Load initial buses
      let buses = (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) ? window.CITYBUS_DATA.buses : [];
      try {
        const apiBuses = await window.CityBusAPI.getBuses();
        if (apiBuses && apiBuses.buses) buses = apiBuses.buses;
      } catch {}

      busLayer.updateBuses(buses);
      renderFeaturedBusCards(buses.slice(0, 6));
    }
  }

  // 2. Render Featured Operating Bus Cards
  function renderFeaturedBusCards(buses) {
    const grid = document.getElementById('featured-buses-grid');
    if (!grid) return;

    if (buses.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon"><i class="fa-solid fa-bus-slash"></i></div>
          <div class="empty-title">No active buses right now</div>
          <div class="empty-desc">Check back shortly or explore our transit timetables.</div>
        </div>
      `;
      return;
    }

    grid.innerHTML = buses.map(bus => {
      let badgeClass = 'badge-success';
      if (bus.status === 'Delayed') badgeClass = 'badge-warning';
      if (bus.status === 'Offline') badgeClass = 'badge-danger';

      const isFav = window.CityBusStore ? window.CityBusStore.isFavorite('buses', bus.id) : false;

      return `
        <div class="bus-card hover-lift" id="card-${bus.id}">
          <div class="bus-card-header">
            <div class="bus-number-badge">
              <i class="fa-solid fa-bus" style="color: var(--cb-brand-primary); font-size: 1.1rem;"></i>
              ${bus.number || bus.bus_number}
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span class="badge ${badgeClass}">
                <span class="badge-dot"></span>${bus.status}
              </span>
              <button class="favorite-btn ${isFav ? 'active' : ''}" data-bus-id="${bus.id}" title="Bookmark bus">
                <i class="fa-${isFav ? 'solid' : 'regular'} fa-star"></i>
              </button>
            </div>
          </div>

          <div class="bus-route-text">
            <span>${bus.route || 'Transit Corridor'}</span>
          </div>

          <div class="bus-stats-row">
            <div>
              <span class="stat-label">Speed</span>
              <div style="font-weight: 700; color: var(--cb-text-primary); font-size: 0.9rem;">${bus.speed || 0} km/h</div>
            </div>
            <div>
              <span class="stat-label">Next Stop</span>
              <div style="font-weight: 700; color: var(--cb-text-primary); font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                ${bus.nextStop || 'In Transit'}
              </div>
            </div>
          </div>

          <div class="bus-card-footer">
            <div class="bus-eta-chip">
              <i class="fa-solid fa-clock"></i>
              <span>${bus.eta ? `ETA: ${bus.eta} min` : 'Active'}</span>
            </div>
            <a href="bus-details.html?id=${bus.id}" class="btn btn-primary btn-sm">
              Track Live <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>
      `;
    }).join('');

    // Favorite buttons
    grid.querySelectorAll('.favorite-btn').forEach(btn => {
      btn.onclick = (e) => {
        e.stopPropagation();
        const busId = btn.dataset.busId;
        const added = window.CityBusStore.toggleFavorite('buses', busId);
        btn.classList.toggle('active', added);
        btn.querySelector('i').className = added ? 'fa-solid fa-star' : 'fa-regular fa-star';
      };
    });
  }

  // 3. User Geolocation Trigger
  const locateBtn = document.getElementById('hero-locate-btn');
  if (locateBtn && window.CityBusMap) {
    locateBtn.onclick = () => {
      window.CityBusMap.locateUser(map, (lat, lng) => {
        window.location.href = `buses.html?lat=${lat}&lng=${lng}&filter=Nearby`;
      });
    };
  }

  // 4. Listen for real-time simulator or WebSocket updates
  window.addEventListener('citybus:data-updated', (e) => {
    const buses = e.detail.buses;
    if (busLayer && buses) {
      busLayer.updateBuses(buses);
    }
  });
});
