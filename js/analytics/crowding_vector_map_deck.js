/**
 * CityBus Enterprise Platform - Live Real-Time Vector Crowding Map Deck
 * File: js/analytics/crowding_vector_map_deck.js
 * 
 * Renders real-time passenger occupancy density layers on Leaflet maps:
 * - Low Occupancy (< 50% Green)
 * - Medium Occupancy (50-85% Amber)
 * - High Crush Occupancy (> 85% Red)
 */

class CityBusCrowdingVectorMapDeck {
  constructor(mapInstance, containerId) {
    this.map = mapInstance;
    this.container = document.getElementById(containerId);
    this.crowdLayer = L.layerGroup();
    if (this.map) {
      this.crowdLayer.addTo(this.map);
    }
  }

  renderCrowdingHeat(busTelemetry = []) {
    if (!this.map) return;
    this.crowdLayer.clearLayers();

    busTelemetry.forEach(bus => {
      const occ = bus.occupancy || 25;
      const color = occ > 40 ? '#EF4444' : (occ > 25 ? '#F59E0B' : '#10B981');

      const circle = L.circleMarker([bus.latitude || 16.5062, bus.longitude || 80.6480], {
        radius: 12,
        fillColor: color,
        color: '#FFFFFF',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
      });

      circle.bindPopup(`
        <strong>${bus.bus_number || 'Bus'}</strong><br>
        Route: ${bus.route_number || '27A'}<br>
        Occupancy: <strong>${occ} / 45 seats</strong><br>
        Status: <span style="color:${color}; font-weight:bold;">${occ > 40 ? 'CRUSH LOAD' : (occ > 25 ? 'FEW SEATS' : 'SEATS AVAILABLE')}</span>
      `);

      this.crowdLayer.addLayer(circle);
    });
  }
}

// Global Export
window.CityBusCrowdingVectorMapDeck = CityBusCrowdingVectorMapDeck;
