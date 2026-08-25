/**
 * CityBus Enterprise Platform - Driver Cockpit & Real-Time Telemetry Hub
 * File: js/driver/cockpit.js
 */

document.addEventListener('DOMContentLoaded', () => {
  const driverState = {
    driverId: 'DRV-1',
    driverName: 'Ravi Kumar',
    busId: 'BUS-101',
    busNumber: 'AP16-001 (27A)',
    routeId: 'ROUTE-27A',
    routeName: 'Vijayawada PNBS → Guntur',
    isTripActive: false,
    currentLat: 16.5062,
    currentLng: 80.6480,
    speed: 0,
    heading: 45,
    odometerKm: 15420.5,
    passengerCount: 28,
    watchId: null,
    simInterval: null,
    currentStopIdx: 2
  };

  // UI Elements
  const tripBtn = document.getElementById('driver-trip-btn');
  const tripStatusBadge = document.getElementById('driver-status-badge');
  const gpsStatusBadge = document.getElementById('gps-status-badge');
  const latEl = document.getElementById('coords-lat');
  const lngEl = document.getElementById('coords-lng');
  const speedEl = document.getElementById('driver-speed');
  const odoEl = document.getElementById('driver-odometer');
  const passengerCountEl = document.getElementById('driver-passengers');
  const arrivedBtn = document.getElementById('arrived-stop-btn');
  const departBtn = document.getElementById('depart-stop-btn');
  const sosBtn = document.getElementById('driver-sos-btn');
  const reportIncidentBtn = document.getElementById('driver-incident-btn');

  // Mini Map
  const mapElement = document.getElementById('driver-mini-map');
  let map = null;
  let busMarker = null;

  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('driver-mini-map', { center: [driverState.currentLat, driverState.currentLng], zoom: 14 });
    if (map) {
      busMarker = L.marker([driverState.currentLat, driverState.currentLng], {
        icon: L.divIcon({
          html: `<div class="marker-pin on-route"><i class="fa-solid fa-bus"></i></div>`,
          className: 'bus-marker-wrapper',
          iconSize: [36, 36]
        })
      }).addTo(map);

      // Draw assigned route polyline
      if (window.CITYBUS_DATA && window.CITYBUS_DATA.routes) {
        const route = window.CITYBUS_DATA.routes.find(r => r.id === driverState.routeId);
        if (route && route.waypoints) {
          L.polyline(route.waypoints, { color: '#2563EB', weight: 5 }).addTo(map);
        }
      }
    }
  }

  function updateHUD() {
    if (latEl) latEl.textContent = driverState.currentLat.toFixed(5);
    if (lngEl) lngEl.textContent = driverState.currentLng.toFixed(5);
    if (speedEl) speedEl.textContent = `${driverState.speed} km/h`;
    if (odoEl) odoEl.textContent = `${driverState.odometerKm.toFixed(1)} km`;
    if (passengerCountEl) passengerCountEl.textContent = driverState.passengerCount;

    if (map && busMarker) {
      busMarker.setLatLng([driverState.currentLat, driverState.currentLng]);
      map.panTo([driverState.currentLat, driverState.currentLng]);
    }
  }

  async function broadcastLocation(lat, lng, speed) {
    driverState.currentLat = lat;
    driverState.currentLng = lng;
    driverState.speed = speed;

    if (window.CityBusAPI) {
      try {
        await window.CityBusAPI.updateBusLocation(1, lat, lng, speed, driverState.heading);
      } catch {}
    }

    if (window.CityBusWS) {
      window.CityBusWS.emit('driver:telemetry', {
        bus_id: 1,
        latitude: lat,
        longitude: lng,
        speed: speed,
        heading: driverState.heading
      });
    }

    updateHUD();
  }

  function startLiveGPS() {
    if (navigator.geolocation) {
      driverState.watchId = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude, speed } = pos.coords;
          const speedKmH = speed ? Math.round(speed * 3.6) : (Math.floor(Math.random() * 15) + 32);
          broadcastLocation(latitude, longitude, speedKmH);
          if (gpsStatusBadge) {
            gpsStatusBadge.className = 'badge badge-success';
            gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: LIVE SENSOR';
          }
        },
        (err) => {
          console.warn('[Driver] Hardware GPS failed, using kinematic simulator:', err);
          startKinematicSimulation();
        },
        { enableHighAccuracy: true, timeout: 6000, maximumAge: 2000 }
      );
    } else {
      startKinematicSimulation();
    }
  }

  function startKinematicSimulation() {
    if (driverState.simInterval) clearInterval(driverState.simInterval);
    if (gpsStatusBadge) {
      gpsStatusBadge.className = 'badge badge-primary';
      gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: SIMULATED (DEMO)';
    }

    const route = window.CITYBUS_DATA ? window.CITYBUS_DATA.routes.find(r => r.id === driverState.routeId) : null;
    const waypoints = route && route.waypoints ? route.waypoints : [[16.5062, 80.6480], [16.5140, 80.6300], [16.5200, 80.6550]];

    driverState.simInterval = setInterval(() => {
      if (!driverState.isTripActive) return;

      const target = waypoints[driverState.currentStopIdx % waypoints.length];
      driverState.currentLat += (target[0] - driverState.currentLat) * 0.08 + (Math.random() - 0.5) * 0.0002;
      driverState.currentLng += (target[1] - driverState.currentLng) * 0.08 + (Math.random() - 0.5) * 0.0002;
      driverState.speed = Math.floor(Math.random() * 14) + 34;
      driverState.odometerKm += 0.04;

      broadcastLocation(driverState.currentLat, driverState.currentLng, driverState.speed);
    }, 2800);
  }

  function stopLiveGPS() {
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

  // Trip Start/Stop Handler
  if (tripBtn) {
    tripBtn.onclick = async () => {
      if (!driverState.isTripActive) {
        // START
        driverState.isTripActive = true;
        tripBtn.className = 'driver-btn-trip btn-stop';
        tripBtn.innerHTML = '<i class="fa-solid fa-stop"></i> END ACTIVE TRIP';
        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-success';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> ON ROUTE (BROADCASTING)';
        }
        startLiveGPS();
        if (window.showToast) window.showToast('Trip started! Live location broadcast active.', 'success');
      } else {
        // STOP
        driverState.isTripActive = false;
        driverState.speed = 0;
        tripBtn.className = 'driver-btn-trip btn-start';
        tripBtn.innerHTML = '<i class="fa-solid fa-play"></i> START NEW TRIP';
        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-danger';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> OFFLINE (PARKED)';
        }
        stopLiveGPS();
        updateHUD();
        if (window.showToast) window.showToast('Trip completed. Vehicle set to offline.', 'info');
      }
    };
  }

  // Arrived / Depart Buttons
  if (arrivedBtn) {
    arrivedBtn.onclick = () => {
      if (!driverState.isTripActive) return;
      driverState.currentStopIdx++;
      driverState.speed = 0;
      updateHUD();
      if (window.showToast) window.showToast('Arrival logged at bus stop. Passenger ETAs refreshed.', 'success');
    };
  }

  // SOS Emergency Panic Button
  if (sosBtn) {
    sosBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.confirm({
          title: '🚨 CONFIRM EMERGENCY SOS DISPATCH',
          message: 'Are you sure you want to declare a Priority-1 Emergency? Dispatchers and emergency medical/police units will be alerted with your current GPS coordinates.',
          confirmText: 'DISPATCH EMERGENCY SOS',
          confirmType: 'danger',
          onConfirm: async () => {
            try {
              if (window.CityBusAPI) {
                await window.CityBusAPI.post('/incidents/emergency/sos', {
                  bus_id: 1,
                  driver_id: 1,
                  latitude: driverState.currentLat,
                  longitude: driverState.currentLng
                });
              }
            } catch {}
            if (window.showToast) window.showToast('EMERGENCY SOS BROADCASTED TO DISPATCH COMMAND', 'danger', 10000);
          }
        });
      }
    };
  }

  // Incident Report Modal
  if (reportIncidentBtn) {
    reportIncidentBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.dynamicModal({
          title: 'Report Vehicle Incident / Delay',
          bodyHtml: `
            <form id="cockpit-incident-form">
              <div class="form-group">
                <label class="form-label">Incident Category</label>
                <select class="form-control" id="inc-type">
                  <option value="Breakdown">Mechanical Breakdown</option>
                  <option value="Traffic">Severe Traffic Congestion</option>
                  <option value="Medical">Medical Emergency on Board</option>
                  <option value="Accident">Road Accident / Collision</option>
                  <option value="GPS_Failure">GPS Sensor Outage</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Severity</label>
                <select class="form-control" id="inc-sev">
                  <option value="Low">Low - Informational</option>
                  <option value="Medium" selected>Medium - Delay expected</option>
                  <option value="High">High - Assistance required</option>
                  <option value="Critical">Critical - Urgent</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Description</label>
                <textarea class="form-control" id="inc-desc" rows="3" placeholder="Describe the issue..."></textarea>
              </div>
            </form>
          `,
          footerHtml: `
            <button class="btn btn-outline" data-dismiss="modal">Cancel</button>
            <button class="btn btn-danger" id="submit-inc-btn">Submit Report</button>
          `,
          onOpen: (modal) => {
            modal.querySelector('#submit-inc-btn').onclick = async () => {
              const incType = modal.querySelector('#inc-type').value;
              const sev = modal.querySelector('#inc-sev').value;
              const desc = modal.querySelector('#inc-desc').value;

              try {
                if (window.CityBusAPI) {
                  await window.CityBusAPI.reportIncident({
                    incident_type: incType,
                    title: `Driver Report: ${incType}`,
                    description: desc || `Driver logged ${incType}`,
                    severity: sev,
                    bus_id: 1,
                    driver_id: 1,
                    latitude: driverState.currentLat,
                    longitude: driverState.currentLng
                  });
                }
              } catch {}

              window.CityBusModal.close(modal);
              if (window.showToast) window.showToast('Incident logged and forwarded to dispatcher control', 'success');
            };
          }
        });
      }
    };
  }

  updateHUD();
});
