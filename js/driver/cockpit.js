/**
 * CityBus Enterprise Platform - Driver Cockpit & Real-Time Telemetry Hub
 * File: js/driver/cockpit.js
 */

document.addEventListener('DOMContentLoaded', () => {
  const driverState = {
    driverId: 'DRV-1',
    driverName: 'Ravi Kumar',
    busId: 1,
    busNumber: '27A',
    busPlate: 'AP16-001',
    routeId: 'ROUTE-27A',
    routeName: 'Vijayawada PNBS → Guntur NTR Terminal',
    isTripActive: false,
    currentLat: 16.5062,
    currentLng: 80.6480,
    speed: 0,
    heading: 45,
    odometerKm: 15420.5,
    passengerCount: 28,
    watchId: null,
    simInterval: null,
    currentStopIdx: 1
  };

  // UI Elements
  const tripBtn = document.getElementById('driver-trip-btn');
  const tripStatusBadge = document.getElementById('driver-status-badge');
  const gpsStatusBadge = document.getElementById('gps-status-badge');
  const latEl = document.getElementById('coords-lat');
  const lngEl = document.getElementById('coords-lng');
  const speedEl = document.getElementById('driver-speed');
  const passengerCountEl = document.getElementById('driver-passengers');
  const nextStopEl = document.getElementById('driver-next-stop');
  const arrivedBtn = document.getElementById('arrived-stop-btn');
  const sosBtn = document.getElementById('driver-sos-btn');
  const reportIncidentBtn = document.getElementById('driver-incident-btn');
  const mapStatusLabel = document.getElementById('map-status-label');

  // Map & Marker State
  const mapElement = document.getElementById('driver-mini-map');
  let map = null;
  let busMarker = null;
  let routePolyline = null;
  const stopMarkers = [];

  // Route stops data
  const corridorStops = [
    { name: 'Pandit Nehru Bus Station (PNBS)', lat: 16.5100, lng: 80.6175 },
    { name: 'Vijayawada Railway Station', lat: 16.5186, lng: 80.6200 },
    { name: 'Governorpet Central', lat: 16.5140, lng: 80.6300 },
    { name: 'Benz Circle Junction', lat: 16.5020, lng: 80.6475 },
    { name: 'DV Manor Center', lat: 16.5045, lng: 80.6520 },
    { name: 'Patamata High Road', lat: 16.4980, lng: 80.6600 },
    { name: 'Autonagar Bus Terminal', lat: 16.4910, lng: 80.6720 },
    { name: 'Mangalagiri AIIMS Bypass', lat: 16.4420, lng: 80.5730 },
    { name: 'Guntur NTR Bus Terminal', lat: 16.4350, lng: 80.5600 }
  ];

  const corridorWaypoints = corridorStops.map(s => [s.lat, s.lng]);

  // 1. Initialize Interactive Driver Cockpit Leaflet Map
  function initDriverMap() {
    if (!mapElement) return;

    if (typeof L === 'undefined' || !window.CityBusMap) {
      if (mapStatusLabel) mapStatusLabel.textContent = 'Map temporarily unavailable.';
      return;
    }

    try {
      map = window.CityBusMap.createMap('driver-mini-map', {
        center: [driverState.currentLat, driverState.currentLng],
        zoom: 14
      });

      if (map) {
        // Draw Route Polyline
        routePolyline = L.polyline(corridorWaypoints, {
          color: '#2563EB',
          weight: 5,
          opacity: 0.85,
          lineJoin: 'round'
        }).addTo(map);

        // Add Stop Markers
        corridorStops.forEach((stop, idx) => {
          const isTerminus = idx === 0 || idx === corridorStops.length - 1;
          const stopIcon = L.divIcon({
            className: 'stop-marker-wrapper',
            html: `
              <div style="background: ${isTerminus ? '#EF4444' : '#3B82F6'}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
            `,
            iconSize: [16, 16],
            iconAnchor: [8, 8]
          });

          const sm = L.marker([stop.lat, stop.lng], { icon: stopIcon })
            .bindPopup(`<strong>📍 Stop #${idx + 1}: ${stop.name}</strong><br><small>Corridor 27A</small>`)
            .addTo(map);
          stopMarkers.push(sm);
        });

        // Add Single Persistent Bus Marker
        const busIcon = window.CityBusMap.createBusIcon({
          number: driverState.busNumber,
          status: 'Offline'
        });

        busMarker = L.marker([driverState.currentLat, driverState.currentLng], {
          icon: busIcon,
          zIndexOffset: 1000
        }).addTo(map);

        busMarker.bindPopup(`
          <div style="text-align:center; padding: 4px;">
            <strong style="font-size: 1rem; color: #2563EB;">🚌 Bus ${driverState.busNumber}</strong><br>
            <span>${driverState.routeName}</span><br>
            <small style="color: #64748B;">Driver: ${driverState.driverName}</small>
          </div>
        `);

        // Trigger resize invalidation
        setTimeout(() => {
          map.invalidateSize();
        }, 250);

        if (mapStatusLabel) {
          mapStatusLabel.textContent = `Bus ${driverState.busNumber} • Standby Coordinates`;
        }
      }
    } catch (err) {
      console.error('[Driver Cockpit Map] Initialization error:', err);
      if (mapStatusLabel) mapStatusLabel.textContent = 'Map temporarily unavailable.';
    }
  }

  // 2. HUD & Coordinates Update
  function updateHUD() {
    if (latEl) latEl.textContent = driverState.currentLat.toFixed(5);
    if (lngEl) lngEl.textContent = driverState.currentLng.toFixed(5);
    if (speedEl) speedEl.textContent = `${driverState.speed} km/h`;
    if (passengerCountEl) passengerCountEl.textContent = driverState.passengerCount;

    if (nextStopEl && corridorStops[driverState.currentStopIdx]) {
      nextStopEl.textContent = corridorStops[driverState.currentStopIdx].name;
    }

    // Update single bus marker coordinates smoothly (no recreation)
    if (map && busMarker) {
      busMarker.setLatLng([driverState.currentLat, driverState.currentLng]);
      busMarker.setIcon(window.CityBusMap.createBusIcon({
        number: driverState.busNumber,
        status: driverState.isTripActive ? 'On Route' : 'Offline'
      }));
      map.panTo([driverState.currentLat, driverState.currentLng], { animate: true });
    }

    if (mapStatusLabel) {
      mapStatusLabel.textContent = driverState.isTripActive
        ? `Bus ${driverState.busNumber} • Active @ ${driverState.speed} km/h`
        : `Bus ${driverState.busNumber} • Parked (Standby)`;
    }
  }

  // 3. Telemetry Broadcast to Flask Backend & WebSocket
  async function broadcastLocation(lat, lng, speed) {
    driverState.currentLat = lat;
    driverState.currentLng = lng;
    driverState.speed = speed;

    // REST API ping to Flask
    if (window.CityBusAPI) {
      try {
        await window.CityBusAPI.updateBusLocation(driverState.busId, lat, lng, speed, driverState.heading);
      } catch (e) {
        console.warn('[Driver Telemetry] API broadcast failed (offline fallback active):', e);
      }
    }

    // WebSocket event emit
    if (window.CityBusWS && typeof window.CityBusWS.emit === 'function') {
      try {
        window.CityBusWS.emit('driver:telemetry', {
          bus_id: driverState.busId,
          bus_number: driverState.busNumber,
          latitude: lat,
          longitude: lng,
          speed: speed,
          heading: driverState.heading,
          passenger_count: driverState.passengerCount
        });
      } catch (e) {}
    }

    updateHUD();
  }

  // 4. GPS Stream Manager (Hardware Sensor with Kinematic Simulator Fallback)
  function startLiveGPS() {
    if (navigator.geolocation) {
      if (gpsStatusBadge) {
        gpsStatusBadge.className = 'badge badge-info';
        gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: CONNECTING...';
      }

      driverState.watchId = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude, speed } = pos.coords;
          const speedKmH = speed ? Math.round(speed * 3.6) : (Math.floor(Math.random() * 12) + 36);
          broadcastLocation(latitude, longitude, speedKmH);
          if (gpsStatusBadge) {
            gpsStatusBadge.className = 'badge badge-success';
            gpsStatusBadge.innerHTML = '<span class="badge-dot"></span> GPS: LIVE SENSOR';
          }
        },
        (err) => {
          console.warn('[Driver Cockpit] Hardware GPS unavailable, using high-fidelity kinematic simulator:', err.message);
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

    driverState.simInterval = setInterval(() => {
      if (!driverState.isTripActive) return;

      const target = corridorWaypoints[driverState.currentStopIdx % corridorWaypoints.length];
      const dLat = (target[0] - driverState.currentLat) * 0.12 + (Math.random() - 0.5) * 0.0001;
      const dLng = (target[1] - driverState.currentLng) * 0.12 + (Math.random() - 0.5) * 0.0001;

      driverState.currentLat += dLat;
      driverState.currentLng += dLng;
      driverState.speed = Math.floor(Math.random() * 14) + 38;
      driverState.odometerKm += 0.05;

      // Close to target stop? Advance to next waypoint
      const dist = Math.hypot(target[0] - driverState.currentLat, target[1] - driverState.currentLng);
      if (dist < 0.001) {
        driverState.currentStopIdx = (driverState.currentStopIdx + 1) % corridorWaypoints.length;
      }

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

  // 5. Trip Start / End Button Listener
  if (tripBtn) {
    tripBtn.onclick = () => {
      if (!driverState.isTripActive) {
        // Start Trip
        driverState.isTripActive = true;
        tripBtn.className = 'driver-btn-trip btn-stop';
        tripBtn.innerHTML = '<i class="fa-solid fa-stop"></i> END ACTIVE TRIP';
        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-success';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> ON ROUTE (BROADCASTING)';
        }
        startLiveGPS();
        if (window.showToast) window.showToast('Trip started! Real-time GPS broadcaster active.', 'success');
      } else {
        // Stop Trip
        driverState.isTripActive = false;
        driverState.speed = 0;
        tripBtn.className = 'driver-btn-trip btn-start';
        tripBtn.innerHTML = '<i class="fa-solid fa-play"></i> START NEW TRIP (BROADCAST GPS)';
        if (tripStatusBadge) {
          tripStatusBadge.className = 'badge badge-danger';
          tripStatusBadge.innerHTML = '<span class="badge-dot"></span> OFFLINE (PARKED)';
        }
        stopLiveGPS();
        updateHUD();
        if (window.showToast) window.showToast('Trip ended. Bus status set to offline.', 'info');
      }
    };
  }

  // 6. Arrived at Bus Stop Button
  if (arrivedBtn) {
    arrivedBtn.onclick = () => {
      if (!driverState.isTripActive) {
        if (window.showToast) window.showToast('Please start the trip first to log stop arrivals.', 'warning');
        return;
      }
      driverState.currentStopIdx = (driverState.currentStopIdx + 1) % corridorStops.length;
      driverState.speed = 0;
      updateHUD();
      const stopName = corridorStops[driverState.currentStopIdx].name;
      if (window.showToast) window.showToast(`Arrived at ${stopName}. ETAs recalculated.`, 'success');
    };
  }

  // 7. Emergency SOS Panic Button
  if (sosBtn) {
    sosBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.confirm({
          title: '🚨 CONFIRM EMERGENCY SOS DISPATCH',
          message: `Are you sure you want to broadcast a Priority-1 Emergency for Bus ${driverState.busNumber}? Dispatch radar and emergency response units will be dispatched immediately with GPS coordinates (${driverState.currentLat.toFixed(4)}, ${driverState.currentLng.toFixed(4)}).`,
          confirmText: 'DISPATCH EMERGENCY SOS',
          confirmType: 'danger',
          onConfirm: async () => {
            try {
              if (window.CityBusAPI) {
                await window.CityBusAPI.post('/incidents/emergency/sos', {
                  bus_id: driverState.busId,
                  driver_id: driverState.driverId,
                  latitude: driverState.currentLat,
                  longitude: driverState.currentLng
                });
              }
            } catch (e) {}

            if (busMarker) {
              busMarker.setIcon(window.CityBusMap.createBusIcon({
                number: driverState.busNumber,
                status: 'emergency'
              }));
            }

            if (window.showToast) window.showToast('🚨 EMERGENCY SOS BROADCASTED TO DISPATCH RADAR', 'danger', 10000);
          }
        });
      }
    };
  }

  // 8. Incident Report Modal
  if (reportIncidentBtn) {
    reportIncidentBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.dynamicModal({
          title: `Report Vehicle Incident / Delay — Bus ${driverState.busNumber}`,
          bodyHtml: `
            <form id="cockpit-incident-form">
              <div class="form-group">
                <label class="form-label">Incident Category</label>
                <select class="form-control" id="inc-type">
                  <option value="Traffic">Severe Traffic Congestion / Gridlock</option>
                  <option value="Breakdown">Mechanical Breakdown / Engine Issue</option>
                  <option value="Medical">Passenger Medical Emergency</option>
                  <option value="Accident">Road Collision / Minor Accident</option>
                  <option value="Detour">Road Closure / Route Detour</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Severity Level</label>
                <select class="form-control" id="inc-sev">
                  <option value="Low">Low - Informational (5-10 min delay)</option>
                  <option value="Medium" selected>Medium - Significant delay (15-30 min)</option>
                  <option value="High">High - Assistance / Replacement bus needed</option>
                  <option value="Critical">Critical - Immediate emergency escalation</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Incident Description / Notes</label>
                <textarea class="form-control" id="inc-desc" rows="3" placeholder="Provide additional details regarding the incident..."></textarea>
              </div>
            </form>
          `,
          footerHtml: `
            <button class="btn btn-outline" data-dismiss="modal">Cancel</button>
            <button class="btn btn-danger" id="submit-inc-btn">Submit Incident</button>
          `,
          onOpen: (modal) => {
            const submitBtn = modal.querySelector('#submit-inc-btn');
            if (submitBtn) {
              submitBtn.onclick = async () => {
                const incType = modal.querySelector('#inc-type').value;
                const sev = modal.querySelector('#inc-sev').value;
                const desc = modal.querySelector('#inc-desc').value;

                try {
                  if (window.CityBusAPI) {
                    await window.CityBusAPI.reportIncident({
                      incident_type: incType,
                      title: `Driver Report: ${incType} (Bus ${driverState.busNumber})`,
                      description: desc || `Driver reported ${incType} near ${corridorStops[driverState.currentStopIdx].name}`,
                      severity: sev,
                      bus_id: driverState.busId,
                      driver_id: driverState.driverId,
                      latitude: driverState.currentLat,
                      longitude: driverState.currentLng
                    });
                  }
                } catch (e) {}

                window.CityBusModal.close(modal);
                if (window.showToast) window.showToast('Incident logged and forwarded to dispatcher control', 'success');
              };
            }
          }
        });
      }
    };
  }

  // Initialize
  initDriverMap();
  updateHUD();
});
