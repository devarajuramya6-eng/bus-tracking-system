/**
 * CityBus Enterprise Platform - Route Geometry & Polyline Layer
 * File: js/map/route_layer.js
 * 
 * Draws high-contrast vector polyline trajectories for transit routes,
 * highlighting corridors, stops, and waypoints with customizable colors.
 */

class RouteLayerManager {
  constructor(map) {
    this.map = map;
    this.layerGroup = L.layerGroup().addTo(map);
    this.activePolylines = new Map(); // routeId -> L.Polyline
  }

  /**
   * Draws or updates a route path on the map
   */
  drawRoute(route, color = '#2563EB', weight = 5) {
    if (!route || !route.waypoints || route.waypoints.length === 0) return null;

    let polyline = this.activePolylines.get(route.id);

    if (polyline) {
      polyline.setLatLngs(route.waypoints);
      polyline.setStyle({ color: color || route.color || '#2563EB', weight });
    } else {
      polyline = L.polyline(route.waypoints, {
        color: color || route.color || '#2563EB',
        weight: weight,
        opacity: 0.88,
        smoothFactor: 1.0,
        lineCap: 'round',
        lineJoin: 'round'
      });

      polyline.bindPopup(`
        <div style="font-family: var(--cb-font-sans); padding: 0.25rem;">
          <strong style="color: var(--cb-brand-primary);">Route ${route.number || ''}</strong><br>
          <span style="font-size: 0.85rem; color: var(--cb-text-secondary);">${route.name || ''}</span><br>
          <small style="color: var(--cb-text-muted);">${route.distance || ''} • ~${route.duration || ''}</small>
        </div>
      `);

      this.layerGroup.addLayer(polyline);
      this.activePolylines.set(route.id, polyline);
    }

    return polyline;
  }

  /**
   * Highlights a single active route and fits bounds to it
   */
  focusRoute(route) {
    this.clear();
    const polyline = this.drawRoute(route, route.color || '#2563EB', 6);
    if (polyline && route.waypoints && route.waypoints.length > 0) {
      this.map.fitBounds(polyline.getBounds(), { padding: [50, 50], duration: 1.0 });
    }
  }

  clear() {
    this.layerGroup.clearLayers();
    this.activePolylines.clear();
  }
}

// Global Export
window.RouteLayerManager = RouteLayerManager;
