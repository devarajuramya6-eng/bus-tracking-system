/**
 * CityBus Enterprise Platform - Spatial & Mapping Engine
 * File: js/map/map_engine.js
 * 
 * Provides map abstraction layer over Leaflet.js:
 * - Tile providers (OpenStreetMap, CartoDB Light/Dark)
 * - Layer management (Buses, Routes, Stops, Geofences, Heatmaps)
 * - Smooth viewport panning & bounds fitting
 * - Live browser geolocation with accuracy circles
 */

class CityBusMapEngine {
  constructor() {
    this.DEFAULT_CENTER = [16.5062, 80.6480]; // Vijayawada Central Coordinates
    this.DEFAULT_ZOOM = 13;
    this.TILE_PROVIDERS = {
      osm: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      light: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
      dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    };
    this.activeMaps = new Map();
  }

  /**
   * Initializes a new Leaflet map instance
   */
  createMap(elementId, options = {}) {
    const el = document.getElementById(elementId);
    if (!el) {
      console.warn(`[CityBus Map] Container #${elementId} not found.`);
      return null;
    }

    if (typeof L === 'undefined') {
      console.error('[CityBus Map] Leaflet library is missing.');
      el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--cb-text-muted);font-size:0.9rem;"><i class="fa-solid fa-triangle-exclamation" style="margin-right:0.5rem;color:var(--cb-status-warning)"></i> Map temporarily unavailable.</div>';
      return null;
    }

    // Ensure container has visible dimensions
    if (el.clientHeight === 0) {
      el.style.minHeight = '350px';
    }

    const center = options.center || this.DEFAULT_CENTER;
    const zoom = options.zoom || this.DEFAULT_ZOOM;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark' || document.body?.classList.contains('dark-theme');

    let map = null;
    try {
      // Check if Leaflet map already initialized on element
      if (el._leaflet_id) {
        el._leaflet_id = null;
      }

      map = L.map(elementId, {
        center: center,
        zoom: zoom,
        zoomControl: options.zoomControl !== false,
        scrollWheelZoom: options.scrollWheelZoom !== false,
        attributionControl: true,
        maxZoom: 19,
        minZoom: 10
      });
    } catch (err) {
      console.warn(`[CityBus Map] Failed to create Leaflet map on #${elementId}:`, err);
      return null;
    }

    // Add Primary OpenStreetMap / Carto Tile Layer with Automatic Fallback
    const primaryUrl = isDark ? this.TILE_PROVIDERS.dark : this.TILE_PROVIDERS.osm;
    const tileLayer = L.tileLayer(primaryUrl, {
      maxZoom: 19,
      subdomains: 'abcd',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    tileLayer.on('tileerror', () => {
      if (tileLayer._url !== this.TILE_PROVIDERS.osm) {
        tileLayer.setUrl(this.TILE_PROVIDERS.osm);
      }
    });

    // Invalidate size once ready
    setTimeout(() => {
      try { map.invalidateSize(); } catch {}
    }, 200);

    window.addEventListener('resize', () => {
      try { map.invalidateSize(); } catch {}
    });

    // Track active maps
    this.activeMaps.set(elementId, { map, tileLayer });

    // Handle theme switching automatically
    window.addEventListener('citybus:theme-changed', (e) => {
      const darkActive = e.detail && e.detail.effective === 'dark';
      const newUrl = darkActive ? this.TILE_PROVIDERS.dark : this.TILE_PROVIDERS.osm;
      try {
        tileLayer.setUrl(newUrl);
      } catch {}
    });

    return map;
  }

  /**
   * Compatibility alias for createMap
   */
  init(elementId, center = [16.5062, 80.6480], zoom = 13) {
    return this.createMap(elementId, { center, zoom });
  }

  /**
   * Creates a styled HTML Bus Icon for Leaflet
   */
  createBusIcon(bus = {}) {
    if (typeof L === 'undefined') return null;
    const num = bus.number || bus.bus_number || 'Bus';
    const status = (bus.status || 'on-route').toLowerCase().replace(/\s+/g, '-');
    let statusClass = 'on-route';
    if (status.includes('delay')) statusClass = 'delayed';
    if (status.includes('off') || status.includes('park')) statusClass = 'offline';
    if (status.includes('emerg') || status.includes('sos')) statusClass = 'emergency';

    return L.divIcon({
      className: 'bus-marker-wrapper',
      html: `
        <div class="custom-bus-marker" style="display:flex;flex-direction:column;align-items:center;">
          <div class="marker-pin ${statusClass}">
            <i class="fa-solid fa-bus"></i>
          </div>
          <div class="marker-label">Bus ${num}</div>
        </div>
      `,
      iconSize: [44, 48],
      iconAnchor: [22, 24],
      popupAnchor: [0, -24]
    });
  }

  /**
   * Draws a route polyline on the map
   */
  drawRoute(map, waypoints, color = '#2563EB', weight = 5) {
    if (!map || !waypoints || waypoints.length === 0 || typeof L === 'undefined') return null;
    return L.polyline(waypoints, { color: color, weight: weight, opacity: 0.85, lineJoin: 'round' }).addTo(map);
  }

  /**
   * Fits map bounds to include all provided coordinate points
   */
  fitBounds(map, points, padding = [40, 40]) {
    if (!map || !points || points.length === 0 || typeof L === 'undefined') return;
    const latLngs = points.map(p => Array.isArray(p) ? p : [p.lat || p.latitude, p.lng || p.longitude]);
    const bounds = L.latLngBounds(latLngs);
    map.fitBounds(bounds, { padding: padding, maxZoom: 15, duration: 1.2 });
  }

  /**
   * Smoothly pans map to target coordinate
   */
  panTo(map, lat, lng, zoom = null) {
    if (!map) return;
    if (zoom) {
      map.flyTo([lat, lng], zoom, { duration: 1.2, easeLinearity: 0.25 });
    } else {
      map.panTo([lat, lng], { animate: true, duration: 0.8 });
    }
  }

  /**
   * Locates user's live browser coordinates
   */
  locateUser(map, callback = null) {
    if (!navigator.geolocation) {
      if (window.showToast) window.showToast('Geolocation is not supported by your browser', 'warning');
      return;
    }

    if (window.showToast) window.showToast('Acquiring high-accuracy GPS position...', 'info');

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude, accuracy } = pos.coords;
        if (map && typeof L !== 'undefined') {
          this.panTo(map, latitude, longitude, 14);

          const userIcon = L.divIcon({
            html: '<div class="user-gps-marker"></div>',
            className: 'user-gps-wrapper',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
          });

          L.marker([latitude, longitude], { icon: userIcon })
            .bindPopup(`<strong>📍 Your Current Location</strong><br><small style="color: #64748B;">GPS Accuracy: ±${Math.round(accuracy)}m</small>`)
            .addTo(map);

          if (accuracy < 1000) {
            L.circle([latitude, longitude], {
              radius: accuracy,
              color: '#2563EB',
              fillColor: '#2563EB',
              fillOpacity: 0.1,
              weight: 1
            }).addTo(map);
          }
        }

        if (window.showToast) window.showToast('GPS position acquired', 'success');
        if (callback) callback(latitude, longitude, accuracy);
      },
      (err) => {
        console.warn('Geolocation error:', err);
        let msg = 'Unable to retrieve your location.';
        if (err.code === 1) msg = 'Location permission denied. Please allow GPS access in browser settings.';
        if (window.showToast) window.showToast(msg, 'warning');
      },
      { enableHighAccuracy: true, timeout: 9000, maximumAge: 3000 }
    );
  }
}

// Global Export
window.CityBusMap = new CityBusMapEngine();
