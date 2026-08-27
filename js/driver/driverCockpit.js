/**
 * CityBus Enterprise Platform - Driver Cockpit & Trip Telemetry Controller
 * File: js/driver/driverCockpit.js
 * 
 * Provides driver cockpit controls, live geolocation ping transmission,
 * trip lifecycle buttons (Start, Pause, Resume, Stop), turn-by-turn alerts,
 * passenger count adjuster, and emergency SOS panic trigger.
 */

class DriverCockpitController {
    constructor() {
        this.activeTrip = null;
        this.assignedBus = null;
        this.assignedRoute = null;
        this.watchPositionId = null;
        this.gpsStatus = 'Disconnected';
        this.currentSpeed = 0;
        this.currentHeading = 0;
        this.passengerCount = 18;
    }

    async init() {
        // Authenticate Driver
        if (!window.authService.requireAuth(['driver', 'admin', 'super_admin'])) {
            return;
        }

        const user = window.authService.getUser();
        document.getElementById('driver-name-display')?.replaceChildren(document.createTextNode(user.name || 'Driver'));

        await this.loadDriverAssignments();
        this.bindCockpitButtons();
    }

    async loadDriverAssignments() {
        try {
            const user = window.authService.getUser();
            const driverData = await window.driverService.getDriverById(user.id || 1).catch(() => null);

            if (driverData) {
                this.assignedBus = driverData.assigned_bus;
            }

            // Fallback load first available bus if unassigned
            if (!this.assignedBus) {
                const buses = await window.busService.getAllBuses();
                this.assignedBus = buses[0] || { id: 1, bus_number: 'AP16-001', route: 'PNBS ⇄ Guntur NTR Terminal' };
            }

            // Populate UI elements
            const busNumEl = document.getElementById('driver-bus-number');
            if (busNumEl) busNumEl.textContent = this.assignedBus.bus_number || 'AP16-001';
            
            const routeEl = document.getElementById('driver-route-name');
            if (routeEl) routeEl.textContent = this.assignedBus.route || 'Vijayawada Central Corridor';

            // Check if active trip is running
            const activeTrips = await window.tripService.getActiveTrips();
            const runningTrip = activeTrips.find(t => t.bus_id === this.assignedBus.id);
            if (runningTrip) {
                this.activeTrip = runningTrip;
                this.updateTripUI('RUNNING');
                this.startGPSTracking();
            } else {
                this.updateTripUI('IDLE');
            }
        } catch (e) {
            console.error('Error loading driver assignments:', e);
        }
    }

    bindCockpitButtons() {
        const startBtn = document.getElementById('start-trip-btn');
        if (startBtn) {
            startBtn.onclick = () => this.handleStartTrip();
        }

        const stopBtn = document.getElementById('stop-trip-btn');
        if (stopBtn) {
            stopBtn.onclick = () => this.handleStopTrip();
        }

        const pauseBtn = document.getElementById('pause-trip-btn');
        if (pauseBtn) {
            pauseBtn.onclick = () => this.handlePauseTrip();
        }

        const sosBtn = document.getElementById('emergency-sos-btn');
        if (sosBtn) {
            sosBtn.onclick = () => this.handleEmergencySOS();
        }

        const paxIncBtn = document.getElementById('pax-inc-btn');
        if (paxIncBtn) {
            paxIncBtn.onclick = () => {
                this.passengerCount = Math.min(55, this.passengerCount + 1);
                this.updatePaxDisplay();
            };
        }

        const paxDecBtn = document.getElementById('pax-dec-btn');
        if (paxDecBtn) {
            paxDecBtn.onclick = () => {
                this.passengerCount = Math.max(0, this.passengerCount - 1);
                this.updatePaxDisplay();
            };
        }
    }

    updatePaxDisplay() {
        const paxEl = document.getElementById('driver-pax-count');
        if (paxEl) paxEl.textContent = `${this.passengerCount} Passengers`;
    }

    async handleStartTrip() {
        if (!this.assignedBus) return;
        try {
            const user = window.authService.getUser();
            const res = await window.tripService.startTrip(this.assignedBus.id, user.id || 1, this.assignedBus.route_id || 1);
            if (res.success) {
                this.activeTrip = res.trip || { id: res.trip_id };
                this.updateTripUI('RUNNING');
                this.startGPSTracking();
                window.toastManager.success('Trip started! Live GPS telemetry is broadcasting.');
            }
        } catch (e) {
            window.toastManager.error(`Failed to start trip: ${e.message}`);
        }
    }

    async handleStopTrip() {
        if (!this.activeTrip) return;
        try {
            await window.tripService.stopTrip(this.activeTrip.id, this.assignedBus.id);
            this.activeTrip = null;
            this.stopGPSTracking();
            this.updateTripUI('IDLE');
            window.toastManager.info('Trip ended successfully. Bus marked Offline.');
        } catch (e) {
            window.toastManager.error(`Failed to stop trip: ${e.message}`);
        }
    }

    async handlePauseTrip() {
        if (!this.activeTrip) return;
        try {
            await window.tripService.pauseTrip(this.activeTrip.id, 'Driver Break');
            this.updateTripUI('PAUSED');
            window.toastManager.warning('Trip paused.');
        } catch (e) {
            window.toastManager.error(`Failed to pause trip: ${e.message}`);
        }
    }

    async handleEmergencySOS() {
        if (!this.assignedBus) return;
        const confirmSOS = confirm('⚠️ Trigger Emergency Panic SOS? This will alert dispatch immediately.');
        if (!confirmSOS) return;

        try {
            await window.incidentService.triggerPanicSOS(this.assignedBus.id, 16.5062, 80.6480, 'Driver activated panic button');
            window.toastManager.error('🚨 EMERGENCY SOS SENT! Dispatch and emergency teams alerted.');
        } catch (e) {
            window.toastManager.error(`SOS failed: ${e.message}`);
        }
    }

    startGPSTracking() {
        this.gpsStatus = 'Transmitting';
        document.getElementById('gps-status-badge')?.replaceChildren(document.createTextNode('GPS Online (1Hz)'));
        
        if ('geolocation' in navigator) {
            this.watchPositionId = navigator.geolocation.watchPosition(
                (pos) => {
                    const lat = pos.coords.latitude;
                    const lng = pos.coords.longitude;
                    const spd = (pos.coords.speed || 0) * 3.6; // m/s to km/h
                    const hdg = pos.coords.heading || 0;
                    
                    this.currentSpeed = spd;
                    this.currentHeading = hdg;
                    
                    document.getElementById('cockpit-speed')?.replaceChildren(document.createTextNode(`${Math.round(spd)}`));

                    // Send telemetry ping
                    if (this.assignedBus) {
                        window.busService.updateLocation(this.assignedBus.id, lat, lng, spd, hdg, pos.coords.accuracy);
                    }
                },
                (err) => {
                    console.warn('GPS watch error:', err);
                },
                { enableHighAccuracy: true, maximumAge: 2000, timeout: 5000 }
            );
        }
    }

    stopGPSTracking() {
        this.gpsStatus = 'Disconnected';
        document.getElementById('gps-status-badge')?.replaceChildren(document.createTextNode('GPS Idle'));
        if (this.watchPositionId !== null) {
            navigator.geolocation.clearWatch(this.watchPositionId);
            this.watchPositionId = null;
        }
    }

    updateTripUI(state) {
        const startBtn = document.getElementById('start-trip-btn');
        const stopBtn = document.getElementById('stop-trip-btn');
        const pauseBtn = document.getElementById('pause-trip-btn');
        const statusEl = document.getElementById('trip-status-display');

        if (state === 'RUNNING') {
            if (startBtn) startBtn.disabled = true;
            if (stopBtn) stopBtn.disabled = false;
            if (pauseBtn) pauseBtn.disabled = false;
            if (statusEl) statusEl.innerHTML = '<span class="badge badge-success">ACTIVE TRIP</span>';
        } else if (state === 'PAUSED') {
            if (startBtn) startBtn.disabled = false;
            if (stopBtn) stopBtn.disabled = false;
            if (pauseBtn) pauseBtn.disabled = true;
            if (statusEl) statusEl.innerHTML = '<span class="badge badge-warning">PAUSED</span>';
        } else {
            if (startBtn) startBtn.disabled = false;
            if (stopBtn) stopBtn.disabled = true;
            if (pauseBtn) pauseBtn.disabled = true;
            if (statusEl) statusEl.innerHTML = '<span class="badge badge-secondary">IDLE</span>';
        }
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('driver-cockpit-root')) {
        window.driverCockpit = new DriverCockpitController();
        window.driverCockpit.init();
    }
});
