/**
 * CityBus Enterprise Platform - Bus Details & Live Telemetry Inspector
 * File: js/passenger/bus_details.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const busId = urlParams.get('id') || '1';

  let bus = null;
  const mapElement = document.getElementById('bus-detail-map');
  let map = null;
  let busMarker = null;

  // Find bus from API or Mock dataset
  try {
    if (window.CityBusAPI) {
      const res = await window.CityBusAPI.getSingleBus(parseInt(busId) || 1);
      if (res && res.bus) bus = res.bus;
    }
  } catch {
    if (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) {
      bus = window.CITYBUS_DATA.buses.find(b => String(b.id) === String(busId)) || window.CITYBUS_DATA.buses[0];
    }
  }

  if (!bus) {
    if (window.showToast) window.showToast('Bus not found', 'danger');
    return;
  }

  // Populate Header & HUD elements
  const numEl = document.getElementById('detail-bus-num');
  const routeEl = document.getElementById('detail-bus-route');
  const statusBadge = document.getElementById('detail-bus-status');
  const speedEl = document.getElementById('detail-speed');
  const nextStopEl = document.getElementById('detail-next-stop');
  const etaEl = document.getElementById('detail-eta');
  const driverEl = document.getElementById('detail-driver');
  const lastUpdatedEl = document.getElementById('detail-last-updated');

  if (numEl) numEl.textContent = bus.number || bus.bus_number;
  if (routeEl) routeEl.textContent = bus.route || 'Vijayawada Express Corridor';
  if (speedEl) speedEl.textContent = `${bus.speed || 0} km/h`;
  if (nextStopEl) nextStopEl.textContent = bus.nextStop || 'Approaching Stop';
  if (etaEl) etaEl.textContent = bus.eta ? `${bus.eta} min` : '4 min';
  if (driverEl) driverEl.textContent = bus.driver || 'Ravi Kumar';
  if (lastUpdatedEl) lastUpdatedEl.textContent = bus.last_updated || 'Just now';

  if (statusBadge) {
    let badgeClass = bus.status === 'On Route' ? 'badge-success' : (bus.status === 'Delayed' ? 'badge-warning' : 'badge-danger');
    statusBadge.className = `badge ${badgeClass}`;
    statusBadge.innerHTML = `<span class="badge-dot"></span> ${bus.status}`;
  }

  // Setup Leaflet Map
  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('bus-detail-map', {
      center: [bus.lat || bus.latitude || 16.5062, bus.lng || bus.longitude || 80.6480],
      zoom: 14
    });

    if (map) {
      // Draw Bus Marker
      busMarker = L.marker([bus.lat || bus.latitude || 16.5062, bus.lng || bus.longitude || 80.6480], {
        icon: L.divIcon({
          html: `<div class="marker-pin on-route"><i class="fa-solid fa-bus"></i></div>`,
          className: 'bus-marker-wrapper',
          iconSize: [40, 52],
          iconAnchor: [20, 38]
        })
      }).addTo(map);

      // Draw Route Polyline if present
      if (window.CITYBUS_DATA && window.CITYBUS_DATA.routes) {
        const routeObj = window.CITYBUS_DATA.routes[0];
        if (routeObj && routeObj.waypoints) {
          L.polyline(routeObj.waypoints, { color: '#2563EB', weight: 5, opacity: 0.8 }).addTo(map);
        }
      }
    }
  }

  // Render Stop Progression Timeline
  const timelineEl = document.getElementById('bus-stops-timeline');
  if (timelineEl && window.CITYBUS_DATA && window.CITYBUS_DATA.stops) {
    const sampleStops = window.CITYBUS_DATA.stops.slice(0, 6);
    timelineEl.innerHTML = sampleStops.map((stop, idx) => {
      const isPassed = idx < 2;
      const isCurrent = idx === 2;
      let nodeClass = isPassed ? 'passed' : (isCurrent ? 'active' : '');

      return `
        <div class="timeline-item ${nodeClass}">
          <div class="timeline-node"></div>
          <div class="timeline-content">
            <div>
              <div class="timeline-name">📍 ${stop.name}</div>
              <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Stop Code: ${stop.code}</div>
            </div>
            ${isCurrent ? '<span class="badge badge-primary">Next Stop</span>' : (isPassed ? '<span class="badge badge-success">Passed</span>' : '<span style="font-size: 0.75rem; color: var(--cb-text-muted);">~12 min</span>')}
          </div>
        </div>
      `;
    }).join('');
  }

  // Real-Time telemetry updates
  window.addEventListener('citybus:data-updated', (e) => {
    const buses = e.detail.buses;
    if (buses) {
      const updated = buses.find(b => String(b.id) === String(busId));
      if (updated) {
        if (speedEl) speedEl.textContent = `${updated.speed || 0} km/h`;
        if (map && busMarker) {
          busMarker.setLatLng([updated.lat || updated.latitude, updated.lng || updated.longitude]);
        }
      }
    }
  });
});
