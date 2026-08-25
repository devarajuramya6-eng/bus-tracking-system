/**
 * CityBus - Map Management & Leaflet Helpers (js/map.js)
 * 
 * Handles OpenStreetMap rendering, custom styled markers, route polylines,
 * interactive popups, user geolocation, and smooth coordinate animations.
 */

const CityBusMap = {
  // Default coordinates: Vijayawada, Andhra Pradesh
  DEFAULT_CENTER: [16.5062, 80.6480],
  DEFAULT_ZOOM: 13,

  /**
   * Initializes a Leaflet map with standard Carto/OSM tiles
   */
  init(elementId, center = this.DEFAULT_CENTER, zoom = this.DEFAULT_ZOOM) {
    const mapElement = document.getElementById(elementId);
    if (!mapElement) {
      console.warn(`Map container #${elementId} not found.`);
      return null;
    }

    if (typeof L === 'undefined') {
      console.error('Leaflet library is not loaded. Please include leaflet.js');
      return null;
    }

    const map = L.map(elementId, {
      center: center,
      zoom: zoom,
      zoomControl: true,
      scrollWheelZoom: true
    });

    // High quality OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    return map;
  },

  /**
   * Creates custom HTML marker icon for buses
   */
  createBusIcon(bus) {
    let statusClass = 'on-route';
    if (bus.status === 'Delayed') statusClass = 'delayed';
    if (bus.status === 'Offline') statusClass = 'offline';

    const html = `
      <div class="custom-bus-marker" title="Bus ${bus.number} - ${bus.status}">
        <div class="marker-pin ${statusClass}">
          <i class="fa-solid fa-bus"></i>
        </div>
        <div class="marker-label">${bus.number}</div>
      </div>
    `;

    return L.divIcon({
      html: html,
      className: 'bus-marker-wrapper',
      iconSize: [36, 48],
      iconAnchor: [18, 36],
      popupAnchor: [0, -36]
    });
  },

  /**
   * Creates custom icon for bus stops
   */
  createStopIcon(stop) {
    const html = `
      <div class="stop-marker-pin" title="${stop.name}">
        <i class="fa-solid fa-location-dot"></i>
      </div>
    `;

    return L.divIcon({
      html: html,
      className: 'stop-marker-wrapper',
      iconSize: [22, 22],
      iconAnchor: [11, 11],
      popupAnchor: [0, -12]
    });
  },

  /**
   * Creates user GPS location marker icon
   */
  createUserGpsIcon() {
    const html = `<div class="user-gps-marker"></div>`;
    return L.divIcon({
      html: html,
      className: 'user-gps-wrapper',
      iconSize: [18, 18],
      iconAnchor: [9, 9]
    });
  },

  /**
   * Generates interactive HTML popup content for a bus
   */
  createBusPopupHTML(bus) {
    let badgeClass = 'badge-success';
    if (bus.status === 'Delayed') badgeClass = 'badge-warning';
    if (bus.status === 'Offline') badgeClass = 'badge-danger';

    return `
      <div class="bus-popup-card">
        <div class="popup-header">
          <span class="popup-bus-num">BUS ${bus.number}</span>
          <span class="badge ${badgeClass}">
            <span class="badge-dot"></span>${bus.status}
          </span>
        </div>
        <div class="popup-route">${bus.route}</div>
        <div class="popup-grid">
          <div>
            <span class="popup-label">Speed:</span>
            <span class="popup-val">${bus.speed} km/h</span>
          </div>
          <div>
            <span class="popup-label">ETA:</span>
            <span class="popup-val" style="color: var(--primary);">${bus.eta ? bus.eta + ' mins' : '--'}</span>
          </div>
          <div style="grid-column: span 2;">
            <span class="popup-label">Next Stop:</span>
            <span class="popup-val">${bus.nextStop}</span>
          </div>
        </div>
        <a href="bus-details.html?id=${bus.id}" class="btn btn-primary btn-sm" style="width: 100%; display: flex;">
          <i class="fa-solid fa-circle-info"></i> View Bus Details
        </a>
      </div>
    `;
  },

  /**
   * Renders and updates a collection of buses on the map without rebuilding the whole layer
   */
  updateBusMarkers(map, markerStore, buses, onMarkerClick = null) {
    if (!map) return;

    buses.forEach(bus => {
      if (markerStore[bus.id]) {
        // Smoothly animate/move existing marker
        markerStore[bus.id].setLatLng([bus.lat, bus.lng]);
        markerStore[bus.id].setIcon(this.createBusIcon(bus));
        markerStore[bus.id].getPopup().setContent(this.createBusPopupHTML(bus));
      } else {
        // Create new marker
        const marker = L.marker([bus.lat, bus.lng], {
          icon: this.createBusIcon(bus),
          riseOnHover: true
        });

        marker.bindPopup(this.createBusPopupHTML(bus));

        if (onMarkerClick) {
          marker.on('click', () => onMarkerClick(bus));
        }

        marker.addTo(map);
        markerStore[bus.id] = marker;
      }
    });

    // Remove markers for buses that no longer exist
    Object.keys(markerStore).forEach(busId => {
      if (!buses.some(b => b.id === busId)) {
        map.removeLayer(markerStore[busId]);
        delete markerStore[busId];
      }
    });
  },

  /**
   * Renders stop markers on the map
   */
  renderStops(map, stops) {
    if (!map) return [];
    const stopMarkers = [];

    stops.forEach(stop => {
      const marker = L.marker([stop.lat, stop.lng], {
        icon: this.createStopIcon(stop)
      });

      marker.bindPopup(`
        <div style="padding: 0.5rem; font-family: inherit;">
          <div style="font-weight: 700; color: var(--dark); font-size: 0.95rem;">📍 ${stop.name}</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Stop Code: <strong>${stop.code}</strong></div>
        </div>
      `);

      marker.addTo(map);
      stopMarkers.push(marker);
    });

    return stopMarkers;
  },

  /**
   * Draws a route path polyline on the map
   */
  drawRoute(map, waypoints, color = '#2563EB') {
    if (!map || !waypoints || waypoints.length === 0) return null;

    const polyline = L.polyline(waypoints, {
      color: color,
      weight: 5,
      opacity: 0.85,
      smoothFactor: 1
    }).addTo(map);

    return polyline;
  },

  /**
   * Requests user's live browser location
   */
  locateUser(map, userMarkerRef, onSuccess = null) {
    if (!navigator.geolocation) {
      showToast('Geolocation is not supported by your browser', 'warning');
      return;
    }

    showToast('Locating your position...', 'info');

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        
        if (map) {
          map.flyTo([latitude, longitude], 14, { duration: 1.5 });

          if (userMarkerRef && userMarkerRef.current) {
            userMarkerRef.current.setLatLng([latitude, longitude]);
          } else if (map) {
            const userMarker = L.marker([latitude, longitude], {
              icon: this.createUserGpsIcon()
            }).bindPopup('<strong>📍 You are here</strong>');
            userMarker.addTo(map);
            if (userMarkerRef) userMarkerRef.current = userMarker;
          }
        }

        showToast('Location updated successfully', 'success');
        if (onSuccess) onSuccess(latitude, longitude);
      },
      (error) => {
        console.warn('Geolocation error:', error);
        let msg = 'Unable to retrieve your location.';
        if (error.code === error.PERMISSION_DENIED) {
          msg = 'Location permission denied. Please enable GPS in your browser settings.';
        }
        showToast(msg, 'warning');
      },
      { enableHighAccuracy: true, timeout: 8000 }
    );
  }
};
