/**
 * CityBus Enterprise Platform - Advanced Leaflet Map Manager
 * File: js/map/leafletMapManager.js
 * 
 * Manages map initialization, dark/light Carto tile layer switching,
 * smooth pan-to vehicle transitions, marker clustering, and polyline layers.
 */

class LeafletMapManager {
    constructor(containerId = 'map', options = {}) {
        this.containerId = containerId;
        this.defaultCenter = options.center || [16.5062, 80.6480]; // Vijayawada Benz Circle
        this.defaultZoom = options.zoom || 13;
        this.map = null;
        this.tileLayers = {};
        this.currentTheme = localStorage.getItem('citybus_theme') || 'light';
        this.busMarkers = new Map();
        this.stopMarkers = new Map();
        this.routeLayers = new Map();
        this.userLocationMarker = null;
    }

    init() {
        const container = document.getElementById(this.containerId);
        if (!container || this.map) return this.map;

        if (typeof L === 'undefined') {
            console.error('Leaflet.js is not loaded.');
            return null;
        }

        this.map = L.map(this.containerId, {
            center: this.defaultCenter,
            zoom: this.defaultZoom,
            zoomControl: false,
            attributionControl: false
        });

        // Add custom top-right zoom control
        L.control.zoom({ position: 'topright' }).addTo(this.map);

        // Tile layer definitions (OpenStreetMap Carto)
        this.tileLayers.light = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            maxZoom: 19,
            subdomains: 'abcd'
        });

        this.tileLayers.dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            maxZoom: 19,
            subdomains: 'abcd'
        });

        // Add active tile layer based on current theme
        const activeTile = this.currentTheme === 'dark' ? this.tileLayers.dark : this.tileLayers.light;
        activeTile.addTo(this.map);

        // Listen for theme change events
        window.addEventListener('themeChanged', (e) => {
            this.setTheme(e.detail.theme);
        });

        return this.map;
    }

    setTheme(theme) {
        if (!this.map) return;
        this.currentTheme = theme;
        if (theme === 'dark') {
            if (this.map.hasLayer(this.tileLayers.light)) this.map.removeLayer(this.tileLayers.light);
            this.tileLayers.dark.addTo(this.map);
        } else {
            if (this.map.hasLayer(this.tileLayers.dark)) this.map.removeLayer(this.tileLayers.dark);
            this.tileLayers.light.addTo(this.map);
        }
    }

    panTo(lat, lng, zoom = null) {
        if (!this.map) return;
        if (zoom) {
            this.map.setView([lat, lng], zoom, { animate: true, duration: 0.8 });
        } else {
            this.map.panTo([lat, lng], { animate: true, duration: 0.8 });
        }
    }

    setUserLocation(lat, lng) {
        if (!this.map) return;
        if (this.userLocationMarker) {
            this.userLocationMarker.setLatLng([lat, lng]);
        } else {
            const userIcon = L.divIcon({
                className: 'user-pulse-marker',
                html: `<div class="user-pulse-dot"><div class="user-pulse-ring"></div></div>`,
                iconSize: [24, 24],
                iconAnchor: [12, 12]
            });
            this.userLocationMarker = L.marker([lat, lng], { icon: userIcon, zIndexOffset: 1000 }).addTo(this.map);
            this.userLocationMarker.bindPopup("<b>Your Current Location</b>");
        }
    }

    renderBuses(buses, onBusClick = null) {
        if (!this.map) return;
        const currentBusIds = new Set(buses.map(b => b.id));

        // Remove stale markers
        for (const [id, marker] of this.busMarkers.entries()) {
            if (!currentBusIds.has(id)) {
                this.map.removeLayer(marker);
                this.busMarkers.delete(id);
            }
        }

        // Add or update markers
        buses.forEach(bus => {
            if (!bus.latitude || !bus.longitude) return;
            const pos = [bus.latitude, bus.longitude];
            const isDelayed = bus.status === 'Delayed';
            const statusClass = isDelayed ? 'delayed' : 'on-route';

            const busIcon = L.divIcon({
                className: `citybus-marker-container ${statusClass}`,
                html: `
                    <div class="citybus-marker ${statusClass}">
                        <div class="marker-badge">${bus.route_rel ? bus.route_rel.route_number : (bus.bus_number || 'BUS')}</div>
                        <div class="marker-pin"><i class="fas fa-bus"></i></div>
                    </div>
                `,
                iconSize: [44, 44],
                iconAnchor: [22, 22]
            });

            if (this.busMarkers.has(bus.id)) {
                const marker = this.busMarkers.get(bus.id);
                marker.setLatLng(pos);
                marker.setIcon(busIcon);
            } else {
                const marker = L.marker(pos, { icon: busIcon }).addTo(this.map);
                marker.bindPopup(`
                    <div class="bus-popup-card">
                        <h4>${bus.bus_number} <span class="badge ${statusClass}">${bus.status}</span></h4>
                        <p><strong>Route:</strong> ${bus.route || 'Unassigned'}</p>
                        <p><strong>Speed:</strong> ${bus.speed || 0} km/h</p>
                        <p><strong>Driver:</strong> ${bus.driver || 'Assigned'}</p>
                        <a href="/bus-details.html?id=${bus.id}" class="popup-btn">View Live Telemetry</a>
                    </div>
                `);
                if (onBusClick) {
                    marker.on('click', () => onBusClick(bus));
                }
                this.busMarkers.set(bus.id, marker);
            }
        });
    }

    renderRoutePolyline(routeId, waypoints, colorHex = '#2563EB') {
        if (!this.map || !waypoints || waypoints.length === 0) return;
        this.clearRoutePolyline(routeId);

        const polyline = L.polyline(waypoints, {
            color: colorHex,
            weight: 5,
            opacity: 0.85,
            smoothFactor: 1.0,
            lineJoin: 'round'
        }).addTo(this.map);

        this.routeLayers.set(routeId, polyline);
        this.map.fitBounds(polyline.getBounds(), { padding: [40, 40] });
    }

    clearRoutePolyline(routeId) {
        if (this.routeLayers.has(routeId)) {
            this.map.removeLayer(this.routeLayers.get(routeId));
            this.routeLayers.delete(routeId);
        }
    }

    renderStops(stops, onStopClick = null) {
        if (!this.map) return;
        this.clearStops();

        stops.forEach(stop => {
            if (!stop.latitude || !stop.longitude) return;
            const stopIcon = L.divIcon({
                className: 'transit-stop-marker',
                html: `<div class="stop-dot ${stop.is_popular ? 'popular' : ''}"></div>`,
                iconSize: [16, 16],
                iconAnchor: [8, 8]
            });

            const marker = L.marker([stop.latitude, stop.longitude], { icon: stopIcon }).addTo(this.map);
            marker.bindPopup(`
                <div class="stop-popup-card">
                    <h4>${stop.name}</h4>
                    <p class="code">Code: ${stop.stop_code || 'STP'}</p>
                    <p>${stop.landmark || 'Transit Platform'}</p>
                    ${stop.is_wheelchair_accessible ? '<span class="amenity-tag"><i class="fas fa-wheelchair"></i> Accessible</span>' : ''}
                </div>
            `);
            if (onStopClick) {
                marker.on('click', () => onStopClick(stop));
            }
            this.stopMarkers.set(stop.id, marker);
        });
    }

    clearStops() {
        if (!this.map) return;
        for (const marker of this.stopMarkers.values()) {
            this.map.removeLayer(marker);
        }
        this.stopMarkers.clear();
    }
}

// Global Export
window.LeafletMapManager = LeafletMapManager;
