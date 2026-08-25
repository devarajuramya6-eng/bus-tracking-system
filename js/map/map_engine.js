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
      light: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
      dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      osm: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
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
      return null;
    }

    const center = options.center || this.DEFAULT_CENTER;
    const zoom = options.zoom || this.DEFAULT_ZOOM;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    const map = L.map(elementId, {
      center: center,
      zoom: zoom,
      zoomControl: options.zoomControl !== false,
      scrollWheelZoom: options.scrollWheelZoom !== false,
      attributionControl: true,
      maxZoom: 19,
      minZoom: 10
    });

    // Add Tile Layer
    const tileUrl = isDark ? this.TILE_PROVIDERS.dark : this.TILE_PROVIDERS.light;
    const tileLayer = L.tileLayer(tileUrl, {
      maxZoom: 19,
      subdomains: 'abcd',
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
    }).addTo(map);

    // Track active maps
    this.activeMaps.set(elementId, { map, tileLayer });

    // Handle theme switching automatically
    window.addEventListener('citybus:theme-changed', (e) => {
      const darkActive = e.detail.effective === 'dark';
      tileLayer.setUrl(darkActive ? this.TILE_PROVIDERS.dark : this.TILE_PROVIDERS.light);
    });

    return map;
  }

  /**
   * Fits map bounds to include all provided coordinate points
   */
  fitBounds(map, points, padding = [40, 40]) {
    if (!map || !points || points.length === 0) return;
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
        if (map) {
          this.panTo(map, latitude, longitude, 14);

          // Add user pulse marker
          const userIcon = L.divIcon({
            html: '<div class="user-gps-marker"></div>',
            className: 'user-gps-wrapper',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
          });

          const marker = L.marker([latitude, longitude], { icon: userIcon })
            .bindPopup(`<strong>📍 Your Current Location</strong><br><small style="color: #64748B;">GPS Accuracy: ±${Math.round(accuracy)}m</small>`)
            .addTo(map);

          // Optional accuracy circle
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
