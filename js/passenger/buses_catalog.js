/**
 * CityBus Enterprise Platform - Live Buses Catalog & Directory
 * File: js/passenger/buses_catalog.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let activeFilter = 'All';
  let searchQuery = '';
  let buses = [];

  const mapElement = document.getElementById('buses-catalog-map');
  let map = null;
  let busLayer = null;

  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('buses-catalog-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (map) busLayer = new BusLayerManager(map);
  }

  // Check URL params
  const urlParams = new URLSearchParams(window.location.search);
  const qParam = urlParams.get('q');
  const filterParam = urlParams.get('filter');
  if (qParam) {
    searchQuery = qParam;
    const searchInput = document.getElementById('bus-search-input');
    if (searchInput) searchInput.value = qParam;
  }
  if (filterParam) activeFilter = filterParam;

  async function loadBuses() {
    try {
      if (window.CityBusAPI) {
        const res = await window.CityBusAPI.getBuses();
        buses = res.buses || [];
      }
    } catch {
      buses = (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) ? window.CITYBUS_DATA.buses : [];
    }

    renderBuses();
    if (busLayer) busLayer.updateBuses(buses);
  }

  function renderBuses() {
    const grid = document.getElementById('buses-catalog-grid');
    const countEl = document.getElementById('buses-total-count');
    if (!grid) return;

    let filtered = [...buses];

    if (activeFilter === 'On Route') filtered = filtered.filter(b => b.status === 'On Route');
    else if (activeFilter === 'Delayed') filtered = filtered.filter(b => b.status === 'Delayed');
    else if (activeFilter === 'Offline') filtered = filtered.filter(b => b.status === 'Offline');
    else if (activeFilter === 'Favorites' && window.CityBusStore) {
      filtered = filtered.filter(b => window.CityBusStore.isFavorite('buses', b.id));
    }

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(b => 
        (b.number || b.bus_number || '').toLowerCase().includes(q) ||
        (b.route || '').toLowerCase().includes(q)
      );
    }

    if (countEl) countEl.textContent = `${filtered.length} Buses Found`;

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon"><i class="fa-solid fa-bus-slash"></i></div>
          <div class="empty-title">No matching buses found</div>
          <div class="empty-desc">Try clearing your search query or selecting 'All' status filter.</div>
        </div>
      `;
      return;
    }

    grid.innerHTML = filtered.map(bus => {
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
              <button class="favorite-btn ${isFav ? 'active' : ''}" data-bus-id="${bus.id}" title="Favorite">
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
              Live Details <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>
      `;
    }).join('');

    // Favorite click listeners
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

  // Filter Chips
  document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.onclick = () => {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeFilter = chip.dataset.filter || 'All';
      renderBuses();
    };
  });

  // Search input
  const searchInput = document.getElementById('bus-search-input');
  if (searchInput) {
    searchInput.oninput = (e) => {
      searchQuery = e.target.value.trim();
      renderBuses();
    };
  }

  await loadBuses();

  // Listen for real-time updates
  window.addEventListener('citybus:data-updated', (e) => {
    const updated = e.detail.buses;
    if (updated) {
      buses = updated;
      if (busLayer) busLayer.updateBuses(buses);
      renderBuses();
    }
  });
});
