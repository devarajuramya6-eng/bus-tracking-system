/**
 * CityBus Enterprise Platform - Visual Map Route Editor
 * File: js/map/route_editor.js
 * 
 * Interactive map editor for transit authorities:
 * - Click map to add waypoints
 * - Drag stops to reorder transit sequence
 * - Calculate total corridor distance and estimated running time
 * - Export route geometry as GeoJSON or JSON waypoint array
 */

class VisualRouteEditor {
  constructor(map, containerId = null) {
    this.map = map;
    this.container = containerId ? document.getElementById(containerId) : null;
    this.isEditing = false;
    this.waypoints = []; // [[lat, lng], ...]
    this.stops = [];     // [{ id, name, lat, lng, stopOrder }]
    this.polyline = null;
    this.markers = [];
    this.onUpdateCallback = null;
  }

  startEditing(existingRoute = null, onUpdate = null) {
    this.isEditing = true;
    this.onUpdateCallback = onUpdate;
    this.clear();

    if (existingRoute && existingRoute.waypoints) {
      this.waypoints = [...existingRoute.waypoints];
      this.stops = existingRoute.stops ? [...existingRoute.stops] : [];
      this.redraw();
    }

    this.map.on('click', this.handleMapClick, this);
    if (window.showToast) window.showToast('Route Editor Active: Click on map to add waypoints & stops', 'info');
  }

  stopEditing() {
    this.isEditing = false;
    this.map.off('click', this.handleMapClick, this);
  }

  handleMapClick(e) {
    if (!this.isEditing) return;
    const { lat, lng } = e.latlng;
    this.addWaypoint(lat, lng);
  }

  addWaypoint(lat, lng, isStop = false, stopName = '') {
    const pt = [parseFloat(lat.toFixed(5)), parseFloat(lng.toFixed(5))];
    this.waypoints.push(pt);

    if (isStop) {
      const stopOrder = this.stops.length + 1;
      this.stops.push({
        id: `STOP-NEW-${Date.now()}`,
        name: stopName || `Stop ${stopOrder}`,
        lat: pt[0],
        lng: pt[1],
        stopOrder
      });
    }

    this.redraw();
  }

  removeLastWaypoint() {
    if (this.waypoints.length > 0) {
      this.waypoints.pop();
      this.redraw();
    }
  }

  clear() {
    if (this.polyline) this.map.removeLayer(this.polyline);
    this.markers.forEach(m => this.map.removeLayer(m));
    this.markers = [];
    this.waypoints = [];
    this.stops = [];
  }

  redraw() {
    // Remove existing polyline & markers
    if (this.polyline) this.map.removeLayer(this.polyline);
    this.markers.forEach(m => this.map.removeLayer(m));
    this.markers = [];

    if (this.waypoints.length === 0) return;

    // Draw editable polyline
    this.polyline = L.polyline(this.waypoints, {
      color: '#2563EB',
      weight: 5,
      opacity: 0.9,
      dashArray: '8, 8'
    }).addTo(this.map);

    // Draw Draggable Waypoint Markers
    this.waypoints.forEach((pt, idx) => {
      const isFirst = idx === 0;
      const isLast = idx === this.waypoints.length - 1;
      
      let markerColor = '#2563EB';
      if (isFirst) markerColor = '#10B981';
      if (isLast) markerColor = '#EF4444';

      const icon = L.divIcon({
        html: `<div style="width: 22px; height: 22px; border-radius: 50%; background: ${markerColor}; border: 3px solid #FFFFFF; box-shadow: 0 2px 6px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 10px; font-weight: bold;">${idx + 1}</div>`,
        className: 'editor-waypoint-pin',
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      });

      const marker = L.marker(pt, { icon, draggable: true }).addTo(this.map);
      
      marker.on('dragend', (e) => {
        const newPos = e.target.getLatLng();
        this.waypoints[idx] = [parseFloat(newPos.lat.toFixed(5)), parseFloat(newPos.lng.toFixed(5))];
        this.redraw();
      });

      this.markers.push(marker);
    });

    const metrics = this.calculateMetrics();
    if (this.onUpdateCallback) {
      this.onUpdateCallback({
        waypoints: this.waypoints,
        stops: this.stops,
        ...metrics
      });
    }
  }

  calculateMetrics() {
    let totalDistKm = 0;
    for (let i = 1; i < this.waypoints.length; i++) {
      const p1 = this.waypoints[i - 1];
      const p2 = this.waypoints[i];
      totalDistKm += this.distanceKm(p1[0], p1[1], p2[0], p2[1]);
    }

    const estimatedMins = Math.max(5, Math.round((totalDistKm / 30) * 60)); // assume 30km/h avg urban speed

    return {
      distanceKm: parseFloat(totalDistKm.toFixed(2)),
      distanceStr: `${totalDistKm.toFixed(1)} km`,
      durationMins: estimatedMins,
      durationStr: `${estimatedMins} min`,
      waypointCount: this.waypoints.length
    };
  }

  distanceKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }
}

// Global Export
window.VisualRouteEditor = VisualRouteEditor;
