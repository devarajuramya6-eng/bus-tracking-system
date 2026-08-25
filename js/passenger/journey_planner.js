/**
 * CityBus Enterprise Platform - Intermodal Journey Planner Logic
 * File: js/passenger/journey_planner.js
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('journey-planner-form');
  const resultsContainer = document.getElementById('journey-results-container');
  const mapElement = document.getElementById('journey-map');
  let map = null;
  let routeLayer = null;

  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('journey-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (map) routeLayer = new RouteLayerManager(map);
  }

  // Pre-fill from query params if available
  const urlParams = new URLSearchParams(window.location.search);
  const fromParam = urlParams.get('from');
  const toParam = urlParams.get('to');

  if (fromParam) document.getElementById('planner-from').value = fromParam;
  if (toParam) document.getElementById('planner-to').value = toParam;

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      calculateJourney();
    });
  }

  if (fromParam && toParam) {
    calculateJourney();
  }

  function calculateJourney() {
    const fromVal = document.getElementById('planner-from').value.trim();
    const toVal = document.getElementById('planner-to').value.trim();

    if (!fromVal || !toVal) {
      if (window.showToast) window.showToast('Please enter both Origin and Destination stops', 'warning');
      return;
    }

    if (!resultsContainer) return;

    // Simulate multi-modal journey calculation
    resultsContainer.innerHTML = `
      <div class="card anim-fade-up" style="margin-bottom: 1.5rem; border-left: 4px solid var(--cb-brand-primary);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
          <div>
            <span class="badge badge-success">Recommended Route</span>
            <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--cb-text-primary); margin-top: 0.35rem;">
              Fastest Connection: Express Bus 27A
            </h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 1.4rem; font-weight: 800; color: var(--cb-brand-primary);">35 min</div>
            <div style="font-size: 0.8rem; color: var(--cb-text-muted);">Fare: ₹30 • 1 Transfer</div>
          </div>
        </div>

        <!-- Step-by-step itinerary -->
        <div class="route-timeline">
          <div class="timeline-item passed">
            <div class="timeline-node"></div>
            <div class="timeline-content">
              <div>
                <div class="timeline-name"><i class="fa-solid fa-person-walking" style="color: var(--cb-text-muted);"></i> Walk 250m to ${fromVal}</div>
                <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Approx. 3 mins walking</div>
              </div>
              <span class="badge badge-dark">Start</span>
            </div>
          </div>

          <div class="timeline-item active">
            <div class="timeline-node"></div>
            <div class="timeline-content">
              <div>
                <div class="timeline-name"><i class="fa-solid fa-bus" style="color: var(--cb-brand-primary);"></i> Board Bus 27A (towards ${toVal})</div>
                <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Departing every 10 mins • AC Low Floor</div>
              </div>
              <span class="badge badge-primary">24 min ride</span>
            </div>
          </div>

          <div class="timeline-item">
            <div class="timeline-node"></div>
            <div class="timeline-content">
              <div>
                <div class="timeline-name"><i class="fa-solid fa-location-dot" style="color: var(--cb-status-success);"></i> Arrive at ${toVal}</div>
                <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Final destination terminal</div>
              </div>
              <span class="badge badge-success">Destination</span>
            </div>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem; border-top: 1px solid var(--cb-border-subtle); padding-top: 1rem;">
          <a href="tickets.html?from=${encodeURIComponent(fromVal)}&to=${encodeURIComponent(toVal)}&fare=30" class="btn btn-primary">
            <i class="fa-solid fa-ticket"></i> Book Ticket (₹30)
          </a>
          <a href="buses.html?q=27A" class="btn btn-outline">
            <i class="fa-solid fa-map-location-dot"></i> Track on Live Map
          </a>
        </div>
      </div>
    `;

    // Highlight route on Leaflet map if present
    if (map && routeLayer && window.CITYBUS_DATA && window.CITYBUS_DATA.routes) {
      const sampleRoute = window.CITYBUS_DATA.routes[0];
      routeLayer.focusRoute(sampleRoute);
    }
  }
});
