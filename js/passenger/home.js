/**
 * CityBus Enterprise Platform - Passenger Home & Hero Search Logic
 * File: js/passenger/home.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  const mapElement = document.getElementById('home-live-map');
  const searchInput = document.getElementById('hero-search-input');
  const searchBtn = document.getElementById('hero-search-btn');
  const clearSearchBtn = document.getElementById('clear-search-btn');
  const statusBar = document.getElementById('search-status-bar');
  const statusText = document.getElementById('search-status-text');
  const resetBtn = document.getElementById('search-status-reset-btn');
  const fleetHeading = document.getElementById('fleet-heading');
  const fleetSubheading = document.getElementById('fleet-subheading');

  let map = null;
  let busLayer = null;
  let allBuses = [];
  let currentFilterQuery = '';

  // 1. Initialize Preview Leaflet Map
  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('home-live-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (map) {
      busLayer = new BusLayerManager(map);
      setTimeout(() => { if (map.invalidateSize) map.invalidateSize(); }, 300);
    }
  }

  // Helper to normalize bus objects
  function normalizeBus(bus) {
    const num = bus.bus_number || bus.number || `BUS-${bus.id}`;
    let routeTitle = bus.route || 'Transit Corridor';
    if (!bus.route && bus.route_rel) {
      routeTitle = `${bus.route_rel.start_point} → ${bus.route_rel.destination}`;
    }
    const lat = bus.latitude || (bus.coords ? bus.coords[0] : 16.5062);
    const lng = bus.longitude || (bus.coords ? bus.coords[1] : 80.6480);
    const speed = typeof bus.speed === 'number' ? bus.speed : 0;
    const status = bus.status || 'Active';
    const eta = bus.eta || (bus.telemetry_eta ? bus.telemetry_eta.eta_minutes : Math.floor(Math.random() * 12) + 3);

    return {
      id: bus.id || num,
      number: num,
      bus_number: num,
      route: routeTitle,
      route_id: bus.route_id || '',
      status: status,
      latitude: lat,
      longitude: lng,
      speed: speed,
      eta: eta,
      nextStop: bus.nextStop || bus.next_stop || 'In Transit',
      driver: bus.driver || 'Captain'
    };
  }

  // Load initial fleet from Backend API or local seed dataset
  async function loadInitialFleet() {
    let rawBuses = (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) ? window.CITYBUS_DATA.buses : [];
    if (window.CityBusAPI) {
      try {
        const apiRes = await window.CityBusAPI.getBuses();
        if (apiRes && apiRes.buses && apiRes.buses.length > 0) {
          rawBuses = apiRes.buses;
        }
      } catch (err) {
        console.warn('[CityBus Home] API fetch error, using local dataset fallback:', err);
      }
    }
    allBuses = rawBuses.map(normalizeBus);

    if (busLayer && allBuses.length > 0) {
      busLayer.updateBuses(allBuses);
    }
    renderFeaturedBusCards(allBuses.slice(0, 8));
  }

  // 2. Perform Real Search across Buses, Routes, and Locations
  async function performSearch(query) {
    const q = (query || '').trim();
    currentFilterQuery = q;

    if (!q) {
      // Empty search: reset view
      if (statusBar) statusBar.style.display = 'none';
      if (clearSearchBtn) clearSearchBtn.style.display = 'none';
      if (fleetHeading) fleetHeading.textContent = 'Active Municipal Fleet';
      if (fleetSubheading) fleetSubheading.textContent = 'Real-time tracking of active city express corridors and feeder networks.';
      renderFeaturedBusCards(allBuses.slice(0, 8));
      if (busLayer) busLayer.updateBuses(allBuses);
      return;
    }

    let matchingBuses = [];

    // First attempt to query backend API
    if (window.CityBusAPI) {
      try {
        const apiRes = await window.CityBusAPI.getBuses({ q: q, search: q });
        if (apiRes && apiRes.buses && Array.isArray(apiRes.buses)) {
          matchingBuses = apiRes.buses.map(normalizeBus);
        }
      } catch (err) {
        console.warn('[CityBus Search] Backend search failed, falling back to client match:', err);
      }
    }

    // Client-side matching if API returned empty or failed
    if (matchingBuses.length === 0 && allBuses.length > 0) {
      const qLower = q.toLowerCase();
      matchingBuses = allBuses.filter(bus => {
        const numMatch = (bus.number || '').toLowerCase().includes(qLower);
        const routeMatch = (bus.route || '').toLowerCase().includes(qLower);
        const idMatch = String(bus.id || '').toLowerCase().includes(qLower);
        const nextStopMatch = (bus.nextStop || '').toLowerCase().includes(qLower);
        return numMatch || routeMatch || idMatch || nextStopMatch;
      });
    }

    // Also check static CITYBUS_DATA routes/buses if still empty
    if (matchingBuses.length === 0 && window.CITYBUS_DATA && window.CITYBUS_DATA.buses) {
      const qLower = q.toLowerCase();
      const localMatches = window.CITYBUS_DATA.buses.filter(b => {
        return (b.number && b.number.toLowerCase().includes(qLower)) ||
               (b.route && b.route.toLowerCase().includes(qLower)) ||
               (b.id && b.id.toLowerCase().includes(qLower));
      });
      if (localMatches.length > 0) {
        matchingBuses = localMatches.map(normalizeBus);
      }
    }

    // Update Status Bar
    if (statusBar && statusText) {
      statusBar.style.display = 'flex';
      statusText.innerHTML = `Showing results for "<strong>${escapeHtml(q)}</strong>" (${matchingBuses.length} ${matchingBuses.length === 1 ? 'bus' : 'buses'} found)`;
    }
    if (clearSearchBtn) clearSearchBtn.style.display = 'inline-flex';
    if (fleetHeading) fleetHeading.textContent = `Search Results for "${q}"`;
    if (fleetSubheading) fleetSubheading.textContent = `Matching active municipal transit units in the corridor.`;

    // Render results
    renderFeaturedBusCards(matchingBuses, q);

    // Update preview map
    if (busLayer) {
      busLayer.updateBuses(matchingBuses.length > 0 ? matchingBuses : allBuses);
      if (map && matchingBuses.length > 0) {
        const first = matchingBuses[0];
        if (first.latitude && first.longitude) {
          map.panTo([first.latitude, first.longitude], { animate: true });
        }
      }
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>'"]/g, tag => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[tag] || tag));
  }

  // 3. Render Bus Cards in Grid
  function renderFeaturedBusCards(buses, activeQuery = '') {
    const grid = document.getElementById('featured-buses-grid');
    if (!grid) return;

    if (!buses || buses.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1; padding: 3rem 1.5rem; text-align: center;">
          <div class="empty-icon" style="font-size: 3rem; color: var(--cb-text-muted); margin-bottom: 1rem;">
            <i class="fa-solid fa-magnifying-glass"></i>
          </div>
          <div class="empty-title" style="font-size: 1.25rem; font-weight: 700; color: var(--cb-text-primary); margin-bottom: 0.5rem;">
            No buses found for '${escapeHtml(activeQuery || 'your query')}'.
          </div>
          <div class="empty-desc" style="color: var(--cb-text-secondary); margin-bottom: 1.5rem; max-width: 460px; margin-left: auto; margin-right: auto;">
            Try searching by bus number (e.g. <strong>27A</strong>, <strong>12</strong>), route (<strong>Guntur</strong>), or popular stop (<strong>Benz Circle</strong>).
          </div>
          <button class="btn btn-outline btn-sm" id="reset-empty-search-btn">
            <i class="fa-solid fa-rotate-left"></i> View All Active Buses
          </button>
        </div>
      `;

      const resetEmptyBtn = document.getElementById('reset-empty-search-btn');
      if (resetEmptyBtn) {
        resetEmptyBtn.onclick = () => {
          if (searchInput) searchInput.value = '';
          performSearch('');
        };
      }
      return;
    }

    grid.innerHTML = buses.map(bus => {
      let badgeClass = 'badge-success';
      if (bus.status === 'Delayed') badgeClass = 'badge-warning';
      if (bus.status === 'Offline') badgeClass = 'badge-danger';

      const isFav = window.CityBusStore ? window.CityBusStore.isFavorite('buses', bus.id) : false;

      return `
        <div class="bus-card hover-lift" id="card-${bus.id}" data-bus-id="${bus.id}" data-lat="${bus.latitude}" data-lng="${bus.longitude}">
          <div class="bus-card-header">
            <div class="bus-number-badge">
              <i class="fa-solid fa-bus" style="color: var(--cb-brand-primary); font-size: 1.1rem;"></i>
              Bus ${bus.number || bus.bus_number}
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

          <div class="bus-route-text" style="margin: 0.75rem 0;">
            <span style="font-weight: 600; color: var(--cb-text-primary);"><i class="fa-solid fa-route" style="color: var(--cb-text-muted); margin-right: 0.35rem;"></i>${bus.route}</span>
          </div>

          <div class="bus-stats-row" style="margin-bottom: 0.75rem;">
            <div>
              <span class="stat-label">Speed</span>
              <div style="font-weight: 700; color: var(--cb-text-primary); font-size: 0.9rem;">${bus.speed || 0} km/h</div>
            </div>
            <div>
              <span class="stat-label">Next Stop</span>
              <div style="font-weight: 700; color: var(--cb-text-primary); font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px;">
                ${bus.nextStop || 'In Transit'}
              </div>
            </div>
          </div>

          <div class="bus-card-footer" style="display: flex; justify-content: space-between; align-items: center; padding-top: 0.75rem; border-top: 1px solid var(--cb-border-subtle);">
            <div class="bus-eta-chip" style="font-size: 0.8rem; color: var(--cb-text-secondary);">
              <i class="fa-solid fa-clock" style="color: var(--cb-brand-primary); margin-right: 0.25rem;"></i>
              <span>${bus.eta ? `ETA: ${bus.eta} min` : 'Available'}</span>
            </div>
            <a href="bus-details.html?id=${bus.id}" class="btn btn-primary btn-sm">
              Track Live <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>
      `;
    }).join('');

    // Selecting a bus card centers preview map on it
    grid.querySelectorAll('.bus-card').forEach(card => {
      card.onclick = (e) => {
        if (e.target.closest('a') || e.target.closest('.favorite-btn')) return;
        const lat = parseFloat(card.dataset.lat);
        const lng = parseFloat(card.dataset.lng);
        if (map && !isNaN(lat) && !isNaN(lng)) {
          map.panTo([lat, lng], { animate: true });
          card.style.borderColor = 'var(--cb-brand-primary)';
          setTimeout(() => { card.style.borderColor = ''; }, 1500);
        }
      };
    });

    // Favorite buttons listener
    grid.querySelectorAll('.favorite-btn').forEach(btn => {
      btn.onclick = (e) => {
        e.stopPropagation();
        const busId = btn.dataset.busId;
        if (window.CityBusStore) {
          const added = window.CityBusStore.toggleFavorite('buses', busId);
          btn.classList.toggle('active', added);
          btn.querySelector('i').className = added ? 'fa-solid fa-star' : 'fa-regular fa-star';
        }
      };
    });
  }

  // 4. Attach Search Listeners
  if (searchBtn && searchInput) {
    searchBtn.onclick = () => performSearch(searchInput.value);
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        performSearch(searchInput.value);
      }
    });
  }

  if (clearSearchBtn) {
    clearSearchBtn.onclick = () => {
      if (searchInput) searchInput.value = '';
      performSearch('');
    };
  }

  if (resetBtn) {
    resetBtn.onclick = () => {
      if (searchInput) searchInput.value = '';
      performSearch('');
    };
  }

  // Geolocation trigger
  const locateBtn = document.getElementById('hero-locate-btn');
  if (locateBtn && window.CityBusMap) {
    locateBtn.onclick = () => {
      window.CityBusMap.locateUser(map, (lat, lng) => {
        window.location.href = `buses.html?lat=${lat}&lng=${lng}&filter=Nearby`;
      });
    };
  }

  // Listen for real-time simulator or WebSocket updates
  window.addEventListener('citybus:data-updated', (e) => {
    const buses = e.detail && e.detail.buses ? e.detail.buses : [];
    if (buses.length > 0) {
      allBuses = buses.map(normalizeBus);
      if (busLayer && !currentFilterQuery) {
        busLayer.updateBuses(allBuses);
      }
    }
  });

  // Initial load
  await loadInitialFleet();
});
