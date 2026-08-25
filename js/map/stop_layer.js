/**
 * CityBus Enterprise Platform - Bus Stop Layer Manager
 * File: js/map/stop_layer.js
 * 
 * Renders city bus stops with custom pins, shelter/accessibility badges,
 * and upcoming departures popup cards.
 */

class StopLayerManager {
  constructor(map) {
    this.map = map;
    this.layerGroup = L.layerGroup().addTo(map);
    this.markers = new Map();
    this.onStopClick = null;
  }

  createStopIcon(stop) {
    const isPopular = stop.popular;
    const html = `
      <div class="stop-marker-pin ${isPopular ? 'popular' : ''}" title="${stop.name}">
        <i class="fa-solid fa-location-dot"></i>
      </div>
    `;

    return L.divIcon({
      html: html,
      className: 'stop-marker-wrapper',
      iconSize: [26, 26],
      iconAnchor: [13, 13],
      popupAnchor: [0, -14]
    });
  }

  createStopPopup(stop) {
    return `
      <div style="padding: 0.35rem; font-family: var(--cb-font-sans); min-width: 220px;">
        <div style="font-weight: 700; color: var(--cb-text-primary); font-size: 0.95rem; line-height: 1.3;">
          📍 ${stop.name}
        </div>
        <div style="font-size: 0.75rem; color: var(--cb-text-muted); margin-top: 0.25rem;">
          Code: <strong>${stop.code || 'STP'}</strong> • Shelter: Yes • Wheelchair: Accessible
        </div>
        <div style="margin-top: 0.65rem; border-top: 1px solid var(--cb-border-subtle); padding-top: 0.5rem;">
          <div style="font-size: 0.75rem; font-weight: 700; color: var(--cb-text-primary); margin-bottom: 0.25rem;">Next Arrivals:</div>
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--cb-text-secondary); margin-bottom: 0.2rem;">
            <span>Bus 27A (to Guntur)</span>
            <span class="badge badge-success" style="font-size: 0.65rem; padding: 2px 5px;">~4 min</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--cb-text-secondary);">
            <span>Bus 12B (to Ramavarappadu)</span>
            <span class="badge badge-success" style="font-size: 0.65rem; padding: 2px 5px;">~8 min</span>
          </div>
        </div>
        <a href="journey-planner.html?from=${encodeURIComponent(stop.name)}" class="btn btn-primary btn-xs btn-block" style="margin-top: 0.65rem;">
          <i class="fa-solid fa-map-location-dot"></i> Plan Trip from Here
        </a>
      </div>
    `;
  }

  renderStops(stops, onStopClick = null) {
    this.clear();
    if (onStopClick) this.onStopClick = onStopClick;

    stops.forEach(stop => {
      const lat = stop.lat || stop.latitude;
      const lng = stop.lng || stop.longitude;
      if (!lat || !lng) return;

      const marker = L.marker([lat, lng], {
        icon: this.createStopIcon(stop)
      });

      marker.bindPopup(this.createStopPopup(stop));

      marker.on('click', () => {
        if (this.onStopClick) this.onStopClick(stop);
      });

      this.layerGroup.addLayer(marker);
      this.markers.set(stop.id, marker);
    });
  }

  clear() {
    this.layerGroup.clearLayers();
    this.markers.clear();
  }
}

// Global Export
window.StopLayerManager = StopLayerManager;
