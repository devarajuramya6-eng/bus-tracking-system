/**
 * CityBus - Live Buses Catalog & Real-Time Directory (js/buses.js)
 * 
 * Handles bus card rendering, live filter chips (All, Nearby, On Route, Delayed, Favorites),
 * search filtering, interactive map sync, and favorite toggling.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const mapElement = document.getElementById('live-buses-map');
  let map = null;
  const busMarkers = {};
  const userMarkerRef = { current: null };

  let currentFilter = 'All';
  let searchQuery = '';
  let userCoords = null;

  // Initialize Map
  if (mapElement) {
    map = CityBusMap.init('live-buses-map', [16.5062, 80.6480], 13);
  }

  // Filter Chips Click Handlers
  const filterChips = document.querySelectorAll('.filter-chip');
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.dataset.filter || 'All';

      if (currentFilter === 'Nearby' && !userCoords) {
        CityBusMap.locateUser(map, userMarkerRef, (lat, lng) => {
          userCoords = { lat, lng };
          renderBusCardsAndMap();
        });
      } else {
        renderBusCardsAndMap();
      }
    });
  });

  // Search Input Handler
  const searchInput = document.getElementById('bus-search-input');
  if (searchInput) {
    // Check if query was passed in URL (e.g. buses.html?q=27A)
    const urlParams = new URLSearchParams(window.location.search);
    const q = urlParams.get('q');
    if (q) {
      searchInput.value = q;
      searchQuery = q;
    }

    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      renderBusCardsAndMap();
    });
  }

  // Locate Me Button
  const locateBtn = document.getElementById('locate-me-btn');
  if (locateBtn) {
    locateBtn.addEventListener('click', () => {
      CityBusMap.locateUser(map, userMarkerRef, (lat, lng) => {
        userCoords = { lat, lng };
        renderBusCardsAndMap();
      });
    });
  }

  /**
   * Main Render Function: Filters buses, builds HTML cards, and updates Map markers
   */
  async function renderBusCardsAndMap() {
    const cardsContainer = document.getElementById('buses-grid');
    const resultsCountEl = document.getElementById('results-count');

    let buses = await CityBusAPI.getBuses();

    // 1. Apply Status/Type Filter
    if (currentFilter === 'On Route') {
      buses = buses.filter(b => b.status === 'On Route');
    } else if (currentFilter === 'Delayed') {
      buses = buses.filter(b => b.status === 'Delayed');
    } else if (currentFilter === 'Favorites') {
      const favs = FavoritesStore.getFavorites();
      buses = buses.filter(b => favs.includes(b.id));
    } else if (currentFilter === 'Nearby') {
      if (userCoords) {
        buses = await CityBusAPI.getNearbyBuses(userCoords.lat, userCoords.lng, 8);
      }
    }

    // 2. Apply Text Search Query
    if (searchQuery) {
      buses = buses.filter(b =>
        b.number.toLowerCase().includes(searchQuery) ||
        b.route.toLowerCase().includes(searchQuery) ||
        b.nextStop.toLowerCase().includes(searchQuery) ||
        b.driver.toLowerCase().includes(searchQuery)
      );
    }

    // Update Results Count
    if (resultsCountEl) {
      resultsCountEl.textContent = `Showing ${buses.length} buses`;
    }

    // Update Map
    if (map) {
      CityBusMap.updateBusMarkers(map, busMarkers, buses, (clickedBus) => {
        // Scroll card into view if exists
        const card = document.getElementById(`card-${clickedBus.id}`);
        if (card) {
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          card.style.borderColor = 'var(--primary)';
          setTimeout(() => card.style.borderColor = '', 1500);
        }
      });
    }

    // Build Cards HTML
    if (!cardsContainer) return;

    if (buses.length === 0) {
      cardsContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; background: white; border-radius: var(--border-radius); border: 1px solid var(--border-color);">
          <div style="font-size: 2.5rem; color: var(--text-light); margin-bottom: 0.75rem;">
            <i class="fa-solid fa-bus-slash"></i>
          </div>
          <h3 style="font-weight: 700; color: var(--dark); margin-bottom: 0.25rem;">No buses found</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Try adjusting your search or active filter</p>
        </div>
      `;
      return;
    }

    cardsContainer.innerHTML = buses.map(bus => {
      const isFav = FavoritesStore.isFavorite(bus.id);
      
      let badgeClass = 'badge-success';
      if (bus.status === 'Delayed') badgeClass = 'badge-warning';
      if (bus.status === 'Offline') badgeClass = 'badge-danger';

      let distanceBadge = '';
      if (userCoords) {
        const dist = calculateDistanceKm(userCoords.lat, userCoords.lng, bus.lat, bus.lng);
        distanceBadge = `<span style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);"><i class="fa-solid fa-location-arrow"></i> ${formatDistance(dist)}</span>`;
      }

      return `
        <div class="bus-card" id="card-${bus.id}">
          <div class="bus-card-header">
            <div class="bus-number-badge">
              <i class="fa-solid fa-bus" style="color: var(--primary); font-size: 1.1rem;"></i>
              ${bus.number}
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span class="badge ${badgeClass}">
                <span class="badge-dot"></span>${bus.status}
              </span>
              <button class="favorite-btn ${isFav ? 'active' : ''}" data-bus-id="${bus.id}" title="Save to favorites">
                <i class="fa-${isFav ? 'solid' : 'regular'} fa-star"></i>
              </button>
            </div>
          </div>

          <div class="bus-route-text">
            <span>${bus.route}</span>
          </div>

          <div class="bus-stats-row">
            <div class="stat-item">
              <span class="stat-label">Current Speed</span>
              <span class="stat-value">${bus.speed} km/h</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Next Stop</span>
              <span class="stat-value" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${bus.nextStop}">
                ${bus.nextStop}
              </span>
            </div>
          </div>

          <div class="bus-card-footer">
            <div class="bus-eta-chip">
              <i class="fa-solid fa-clock"></i>
              <span>${bus.eta ? `ETA: ${bus.eta} min` : 'Offline'}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              ${distanceBadge}
              <a href="bus-details.html?id=${bus.id}" class="btn btn-primary btn-sm">
                Track Bus <i class="fa-solid fa-arrow-right"></i>
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Attach Favorite Click Listeners
    document.querySelectorAll('.favorite-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const busId = btn.dataset.busId;
        const isAdded = FavoritesStore.toggleFavorite(busId);
        btn.classList.toggle('active', isAdded);
        const icon = btn.querySelector('i');
        if (icon) {
          icon.className = isAdded ? 'fa-solid fa-star' : 'fa-regular fa-star';
        }
        if (currentFilter === 'Favorites') {
          renderBusCardsAndMap();
        }
      });
    });
  }

  // Initial Render
  await renderBusCardsAndMap();

  // Listen to Live Simulator Broadcasts for auto-updating live coordinates & cards
  window.addEventListener('citybus:data-updated', () => {
    renderBusCardsAndMap();
  });
});
