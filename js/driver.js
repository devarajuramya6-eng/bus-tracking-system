/**
 * CityBus - Driver Cockpit & Real-Time GPS Tracking (js/driver.js)
 * 
 * Handles driver session, trip start/stop lifecycle,
 * navigator.geolocation.watchPosition integration with live coordinate broadcasting,
 * and high-fidelity simulated route progression.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Driver State
  const driverState = {
    driverId: 'DRV-1',
    driverName: 'Ravi Kumar',
    busId: 'BUS-101',
    busNumber: '27A',
    routeName: 'Vijayawada PNBS → Guntur',
    routeId: 'ROUTE-27A',
    isTripActive: false,
    watchId: null,
    simInterval: null,
    currentLat: 16.5062,
    currentLng: 80.6480,
    speed: 0,
    odometerKm: 14.2,
    currentStopIdx: 2
  };

  // UI Elements
  const tripBtn = document.getElementById('driver-trip-btn');
  const tripStatusBadge = document.getElementById('driver-status-badge');
  const gpsStatusBadge = document.getElementById('gps-status-badge');
  const coordsLatEl = document.getElementById('coords-lat');
  const coordsLngEl = document.getElementById('coords-lng');
  const speedEl = document.getElementById('driver-speed');
  const odometerEl = document.getElementById('driver-odometer');
  const nextStopEl = document.getElementById('driver-next-stop');
  const routeNameEl = document.getElementById('driver-route-name');
  const busNumberEl = document.getElementById('driver-bus-number');
  const arrivedBtn = document.getElementById('arrived-stop-btn');

  // Mini Cockpit Map
  const mapElement = document.getElementById('driver-mini-map');
  let map = null;
  let busMarker = null;

  if (mapElement) {
    map = CityBusMap.init('driver-mini-map', [driverState.currentLat, driverState.currentLng], 14);
    busMarker = L.marker([driverState.currentLat, driverState.currentLng], {
      icon: CityBusMap.createBusIcon({ number: driverState.busNumber, status: 'Offline' })
    }).addTo(map);

    // Draw assigned route polyline
    const route = CITYBUS_DATA.routes.find(r => r.id === driverState.routeId);
    if (route) {
      CityBusMap.drawRoute(map, route.waypoints, '#2563EB');
    }
  }

  // Update UI Telemetry Values
  function updateTelemetryUI() {
    if (coordsLatEl) coordsLatEl.textContent = driverState.currentLat.toFixed(5);
    if (coordsLngEl) coordsLngEl.textContent = driverState.currentLng.toFixed(5);
    if (speedEl) speedEl.textContent = `${driverState.speed} km/h`;
    if (odometerEl) odometerEl.textContent = `${driverState.odometerKm.toFixed(1)} km`;

    const route = CITYBUS_DATA.routes.find(r => r.id === driverState.routeId);
    if (route && route.stops) {
      const stopId = route.stops[driverState.currentStopIdx] || route.stops[0];
      const stop = CITYBUS_DATA.stops.find(s => s.id === stopId);
      if (nextStopEl && stop) {
        nextStopEl.textContent = stop.name;
      }
    }

    if (map && busMarker) {
      busMarker.setLatLng([driverState.currentLat, driverState.currentLng]);
      busMarker.setIcon(CityBusMap.createBusIcon({
        number: driverState.busNumber,
        status: driverState.isTripActive ? 'On Route' : 'Offline'
      }));
      map.panTo([driverState.currentLat, driverState.currentLng]);
    }
  }

  /**
   * Broadcast location to mock API / Flask backend
   */
  async function broadcastLocation(lat, lng, speed) {
    driverState.currentLat = lat;
    driverState.currentLng = lng;
    driverState.speed = speed;

    // Call Mock API
    await CityBusAPI.updateBusLocation(driverState.busId, lat, lng, speed);

    updateTelemetryUI();
  }

  /**
   * Start Live GPS Watcher
   */
  function startGpsTracking() {
    if (navigator.geolocation) {
      driverState.watchId = navigator.geolocation.watchPosition(
        (position) => {
          const { latitude, longitude, speed } = position.coords;
          const currentSpeedKmH = speed ? Math.round(speed * 3.6) : (Math.floor(Math.random() * 15) + 25);
          broadcastLocation(latitude, longitude, currentSpeedKmH);
          if (gpsStatusBadge) {
            gpsStatusBadge.className = 'badge badge-success';
            gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: LIVE HARDWARE';
          }
        },
        (error) => {
          console.warn('Driver GPS watch error. Falling back to high-accuracy simulation:', error);
          startSimulatedRouteTracking();
        },
        { enableHighAccuracy: true, maximumAge: 2000, timeout: 7000 }
      );
    } else {
      startSimulatedRouteTracking();
    }
  }

  /**
   * Simulated Route Tracker (Fallback if browser GPS not available or desktop)
   */
  function startSimulatedRouteTracking() {
    if (driverState.simInterval) clearInterval(driverState.simInterval);

    if (gpsStatusBadge) {
      gpsStatusBadge.className = 'badge badge-primary';
      gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: SIMULATED (DEMO)';
    }

    const route = CITYBUS_DATA.routes.find(r => r.id === driverState.routeId);
    let stepCount = 0;

    driverState.simInterval = setInterval(() => {
      if (!driverState.isTripActive) return;

      if (route && route.waypoints) {
        const wp = route.waypoints;
        const currentTarget = wp[driverState.currentStopIdx % wp.length];
        
        driverState.currentLat += (currentTarget[0] - driverState.currentLat) * 0.09 + (Math.random() - 0.5) * 0.0003;
        driverState.currentLng += (currentTarget[1] - driverState.currentLng) * 0.09 + (Math.random() - 0.5) * 0.0003;
        
        driverState.speed = Math.floor(Math.random() * 12) + 32;
        driverState.odometerKm += 0.05;
        stepCount++;

        if (stepCount % 5 === 0) {
          driverState.currentStopIdx = (driverState.currentStopIdx + 1) % wp.length;
        }
      }

      broadcastLocation(driverState.currentLat, driverState.currentLng, driverState.speed);
    }, 2500);
  }

  /**
   * Stop Tracking
   */
  function stopGpsTracking() {
    if (driverState.watchId !== null) {
      navigator.geolocation.clearWatch(driverState.watchId);
      driverState.watchId = null;
    }
    if (driverState.simInterval) {
      clearInterval(driverState.simInterval);
      driverState.simInterval = null;
    }
    if (gpsStatusBadge) {
      gpsStatusBadge.className = 'badge badge-dark';
      gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: STANDBY';
    }
  }

  /**
   * Trip Start / Stop Button Handler
   */
  if (tripBtn) {
    tripBtn.addEventListener('click', async () => {
      if (!driverState.isTripActive) {
        // START TRIP
        driverState.isTripActive = true;
        await CityBusAPI.startTrip(driverState.driverId, driverState.busId);

        tripBtn.className = 'driver-btn-trip btn-stop';
        tripBtn.innerHTML = '<i class="fa-solid fa-stop"></i> STOP TRIP';

        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-success';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> ● On Route (Broadcasting)';
        }

        showToast('Trip started! Live location broadcast is active.', 'success');
        startGpsTracking();
      } else {
        // STOP TRIP
        driverState.isTripActive = false;
        driverState.speed = 0;
        await CityBusAPI.stopTrip(driverState.driverId, driverState.busId);

        tripBtn.className = 'driver-btn-trip btn-start';
        tripBtn.innerHTML = '<i class="fa-solid fa-play"></i> START TRIP';

        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-danger';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> ● Offline (Parked)';
        }

        stopGpsTracking();
        updateTelemetryUI();
        showToast('Trip ended. Location broadcasting stopped.', 'info');
      }
    });
  }

  // Arrived at stop manual trigger
  if (arrivedBtn) {
    arrivedBtn.addEventListener('click', () => {
      if (!driverState.isTripActive) {
        showToast('Please start your trip first', 'warning');
        return;
      }

      driverState.currentStopIdx++;
      updateTelemetryUI();
      showToast('Arrival logged at stop! Passenger ETAs refreshed.', 'success');
    });
  }

  // Initial UI Render
  updateTelemetryUI();
});
