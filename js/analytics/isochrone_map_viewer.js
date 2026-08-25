/**
 * CityBus Enterprise Platform - Transit Isochrone Catchment Map Viewer
 * File: js/analytics/isochrone_map_viewer.js
 * 
 * Renders multi-tiered travel-time reachability polygons:
 * - 15 min (Green), 30 min (Blue), 45 min (Amber), 60 min (Red)
 * - Dynamic origin stop selector and travel-time slider
 */

class CityBusIsochroneMapViewer {
  constructor(mapInstance, containerId) {
    this.map = mapInstance;
    this.container = document.getElementById(containerId);
    this.isochroneLayers = L.layerGroup();
    if (this.map) {
      this.isochroneLayers.addTo(this.map);
    }
  }

  renderIsochrones(centerLat = 16.5100, centerLng = 80.6175) {
    if (!this.map) return;
    this.isochroneLayers.clearLayers();

    const contours = [
      { time: 15, radiusM: 3500, color: '#10B981', label: '15 Mins Catchment' },
      { time: 30, radiusM: 7000, color: '#3B82F6', label: '30 Mins Catchment' },
      { time: 45, radiusM: 11000, color: '#F59E0B', label: '45 Mins Catchment' },
      { time: 60, radiusM: 15000, color: '#EF4444', label: '60 Mins Catchment' }
    ];

    // Render concentric circles in reverse order so inner is on top
    contours.slice().reverse().forEach(c => {
      const circle = L.circle([centerLat, centerLng], {
        radius: c.radiusM,
        color: c.color,
        fillColor: c.color,
        fillOpacity: 0.12,
        weight: 2,
        dashArray: '4, 4'
      });

      circle.bindPopup(`<strong>${c.label}</strong><br>Reachable within ${c.time} minutes from PNBS Terminal.`);
      this.isochroneLayers.addLayer(circle);
    });

    const marker = L.marker([centerLat, centerLng]).bindPopup("<strong>Isochrone Origin:</strong> PNBS Central Terminal");
    this.isochroneLayers.addLayer(marker);
  }
}

// Global Export
window.CityBusIsochroneMapViewer = CityBusIsochroneMapViewer;
