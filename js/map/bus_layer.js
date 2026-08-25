/**
 * CityBus Enterprise Platform - Live Bus Marker Layer Manager
 * File: js/map/bus_layer.js
 * 
 * Handles rendering, smooth updating, custom icons, heading arrows,
 * popups, and click callbacks for all active municipal buses.
 */

class BusLayerManager {
  constructor(map) {
    this.map = map;
    this.markers = new Map(); // busId -> L.Marker
    this.layerGroup = L.layerGroup().addTo(map);
    this.onBusClick = null;
    this.initInterpolationListener();
  }

  initInterpolationListener() {
    window.addEventListener('citybus:marker-interpolated', (e) => {
      const { busId, lat, lng, heading } = e.detail;
      const marker = this.markers.get(busId);
      if (marker) {
        marker.setLatLng([lat, lng]);
      }
    });
  }

  /**
   * Generates custom HTML icon for a bus with heading and status
   */
  createBusIcon(bus) {
    let statusClass = 'on-route';
    if (bus.status === 'Delayed') statusClass = 'delayed';
    if (bus.status === 'Offline') statusClass = 'offline';
    if (bus.status === 'Emergency') statusClass = 'emergency';

    const html = `
      <div class="custom-bus-marker" id="marker-${bus.id}" title="Bus ${bus.number} - ${bus.status}">
        <div class="marker-pin ${statusClass}">
          <i class="fa-solid fa-bus"></i>
        </div>
        <div class="marker-label">${bus.number}</div>
      </div>
    `;

    return L.divIcon({
      html: html,
      className: 'bus-marker-wrapper',
      iconSize: [40, 52],
      iconAnchor: [20, 38],
      popupAnchor: [0, -38]
    });
  }

  createPopupContent(bus) {
    let badgeClass = 'badge-success';
    if (bus.status === 'Delayed') badgeClass = 'badge-warning';
    if (bus.status === 'Offline') badgeClass = 'badge-danger';
    if (bus.status === 'Emergency') badgeClass = 'badge-danger';

    return `
      <div class="bus-popup-card">
        <div class="popup-header">
          <span class="popup-bus-num">BUS ${bus.number}</span>
          <span class="badge ${badgeClass}">
            <span class="badge-dot"></span>${bus.status}
          </span>
        </div>
        <div class="popup-route">${bus.route || 'Transit Corridor'}</div>
        <div class="popup-grid">
          <div>
            <span class="popup-label">Speed:</span>
            <span class="popup-val">${bus.speed || 0} km/h</span>
          </div>
          <div>
            <span class="popup-label">ETA:</span>
            <span class="popup-val" style="color: var(--cb-brand-primary);">${bus.eta ? bus.eta + ' mins' : '--'}</span>
          </div>
          <div style="grid-column: span 2;">
            <span class="popup-label">Next Stop:</span>
            <span class="popup-val">${bus.nextStop || 'In Transit'}</span>
          </div>
        </div>
        <a href="bus-details.html?id=${bus.id}" class="btn btn-primary btn-sm" style="width: 100%; display: flex; justify-content: center;">
          <i class="fa-solid fa-circle-info"></i> View Live Telemetry
        </a>
      </div>
    `;
  }

  /**
   * Updates or creates markers for a list of buses
   */
  updateBuses(buses, onSelectCallback = null) {
    if (onSelectCallback) this.onBusClick = onSelectCallback;

    const currentBusIds = new Set(buses.map(b => b.id));

    buses.forEach(bus => {
      // Feed target coordinates to interpolator for smooth animation
      if (window.CityBusInterpolator) {
        window.CityBusInterpolator.updateVehicleTarget(bus.id, bus.lat, bus.lng, bus.heading || 0, bus.speed || 0);
      }

      let marker = this.markers.get(bus.id);

      if (marker) {
        marker.setIcon(this.createBusIcon(bus));
        marker.getPopup()?.setContent(this.createPopupContent(bus));
      } else {
        marker = L.marker([bus.lat, bus.lng], {
          icon: this.createBusIcon(bus),
          riseOnHover: true
        });

        marker.bindPopup(this.createPopupContent(bus));

        marker.on('click', () => {
          if (this.onBusClick) this.onBusClick(bus);
        });

        this.layerGroup.addLayer(marker);
        this.markers.set(bus.id, marker);
      }
    });

    // Remove deleted / decommissioned buses
    this.markers.forEach((marker, busId) => {
      if (!currentBusIds.has(busId)) {
        this.layerGroup.removeLayer(marker);
        this.markers.delete(busId);
      }
    });
  }

  clear() {
    this.layerGroup.clearLayers();
    this.markers.clear();
  }
}

// Global Export
window.BusLayerManager = BusLayerManager;
