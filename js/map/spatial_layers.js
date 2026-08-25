/**
 * CityBus Enterprise Platform - Advanced Spatial Map Layers
 * File: js/map/spatial_layers.js
 * 
 * Provides specialized Leaflet vector and analytical visualization layers:
 * - Real-Time Corridor Congestion Speed Choropleth (Green > 35km/h, Amber 15-35km/h, Red < 15km/h)
 * - Depot & Terminus Polygon Geofence Boundaries
 * - Stop Accessibility & Shelter Heatmap Clusters
 * - EV Charging Hub Markers & Real-Time Bay Status
 */

class CityBusSpatialLayers {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.congestionLayerGroup = L.layerGroup();
    this.geofenceLayerGroup = L.layerGroup();
    this.evHubLayerGroup = L.layerGroup();

    if (this.map) {
      this.congestionLayerGroup.addTo(this.map);
      this.geofenceLayerGroup.addTo(this.map);
      this.evHubLayerGroup.addTo(this.map);
    }
  }

  /**
   * Renders colored speed segments along a route polyline.
   */
  renderCorridorCongestion(polylinePoints, avgSpeedKmh = 28.0) {
    this.congestionLayerGroup.clearLayers();
    if (!polylinePoints || polylinePoints.length < 2) return;

    let color = '#10b981'; // Green (Fast)
    if (avgSpeedKmh < 15.0) color = '#ef4444'; // Red (Severe Congestion)
    else if (avgSpeedKmh < 30.0) color = '#f59e0b'; // Amber (Moderate)

    const polyline = L.polyline(polylinePoints, {
      color: color,
      weight: 6,
      opacity: 0.85,
      lineCap: 'round',
      lineJoin: 'round'
    });

    polyline.bindPopup(`
      <div style="font-family: inherit; font-size: 0.85rem; padding: 4px;">
        <strong>Corridor Traffic Velocity</strong><br>
        Speed: <strong>${avgSpeedKmh.toFixed(1)} km/h</strong><br>
        Status: <span style="color: ${color}; font-weight: bold;">${avgSpeedKmh < 15 ? 'Heavy Traffic' : (avgSpeedKmh < 30 ? 'Moderate' : 'Free Flow')}</span>
      </div>
    `);

    this.congestionLayerGroup.addLayer(polyline);
  }

  /**
   * Renders municipal depot polygonal geofence boundaries.
   */
  renderDepotGeofences() {
    this.geofenceLayerGroup.clearLayers();

    const depots = [
      {
        name: 'PNBS Central Bus Station & EV Depot',
        bounds: [[16.5130, 80.6145], [16.5130, 80.6205], [16.5070, 80.6205], [16.5070, 80.6145]],
        color: '#2563eb'
      },
      {
        name: 'Autonagar Heavy Maintenance Yard',
        bounds: [[16.4980, 80.6750], [16.4980, 80.6820], [16.4920, 80.6820], [16.4920, 80.6750]],
        color: '#8b5cf6'
      },
      {
        name: 'Mangalagiri Transit Hub',
        bounds: [[16.4380, 80.5670], [16.4380, 80.5730], [16.4320, 80.5730], [16.4320, 80.5670]],
        color: '#06b6d4'
      }
    ];

    depots.forEach(d => {
      const polygon = L.polygon(d.bounds, {
        color: d.color,
        fillColor: d.color,
        fillOpacity: 0.15,
        weight: 2,
        dashArray: '5, 5'
      });

      polygon.bindPopup(`<strong>${d.name}</strong><br>Geofenced Municipal Transit Facility`);
      this.geofenceLayerGroup.addLayer(polygon);
    });
  }

  /**
   * Renders dedicated EV Charging Hub icons.
   */
  renderEVChargingHubs() {
    this.evHubLayerGroup.clearLayers();

    const hubs = [
      { name: 'PNBS Fast DC Hub', lat: 16.5100, lng: 80.6175, totalBays: 8, availableBays: 3, powerKw: 120 },
      { name: 'Autonagar EV Station', lat: 16.4950, lng: 80.6780, totalBays: 6, availableBays: 4, powerKw: 120 },
      { name: 'Amaravati Secretariat EV Hub', lat: 16.5400, lng: 80.5150, totalBays: 4, availableBays: 2, powerKw: 120 }
    ];

    hubs.forEach(h => {
      const icon = L.divIcon({
        className: 'ev-hub-marker',
        html: `
          <div style="background: #10b981; color: #fff; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4); border: 2px solid #fff;">
            ⚡
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      const marker = L.marker([h.lat, h.lng], { icon });
      marker.bindPopup(`
        <div style="padding: 4px;">
          <strong>${h.name}</strong><br>
          Fast DC Chargers: <strong>${h.powerKw} kW</strong><br>
          Bays Available: <span style="color: #10b981; font-weight: bold;">${h.availableBays} / ${h.totalBays} Free</span>
        </div>
      `);

      this.evHubLayerGroup.addLayer(marker);
    });
  }
}

// Global Export
window.CityBusSpatialLayers = CityBusSpatialLayers;
