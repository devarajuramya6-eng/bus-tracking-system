/**
 * CityBus Enterprise Platform - Passenger Interactive Dashboard Controller
 * File: js/passenger/passengerDashboard.js
 * 
 * Orchestrates live bus tracking, nearby stops radar, quick ticket wallet view,
 * journey planner integration, and dynamic ETA refresh loops.
 */

class PassengerDashboardController {
    constructor() {
        this.mapManager = null;
        this.currentBuses = [];
        this.selectedBus = null;
        this.refreshInterval = null;
        this.userLocation = [16.5062, 80.6480]; // Benz Circle default
    }

    async init() {
        // Initialize Map
        if (document.getElementById('map')) {
            this.mapManager = new window.LeafletMapManager('map', { center: this.userLocation, zoom: 14 });
            this.mapManager.init();
        }

        // Detect user location if available
        this.detectLocation();

        // Load initial data
        await this.loadNearbyBuses();
        await this.loadActiveAlerts();
        await this.loadRecentTickets();

        // Start auto-refresh loop (every 5 seconds)
        this.startLiveTelemetryStream();
        this.bindEvents();
    }

    detectLocation() {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    this.userLocation = [pos.coords.latitude, pos.coords.longitude];
                    if (this.mapManager) {
                        this.mapManager.setUserLocation(pos.coords.latitude, pos.coords.longitude);
                    }
                },
                (err) => console.log('Location access denied or unavailable:', err),
                { enableHighAccuracy: true, timeout: 5000 }
            );
        }
    }

    async loadNearbyBuses() {
        try {
            const buses = await window.busService.getAllBuses('On Route');
            this.currentBuses = buses;
            if (this.mapManager) {
                this.mapManager.renderBuses(buses, (bus) => this.selectBus(bus));
            }
            this.renderBusList(buses);
        } catch (e) {
            console.error('Failed to load buses:', e);
        }
    }

    async loadActiveAlerts() {
        try {
            const alerts = await window.alertService.getActiveAlerts();
            const banner = document.getElementById('passenger-alerts-banner');
            if (banner && alerts.length > 0) {
                banner.innerHTML = alerts.map(a => `
                    <div class="alert-item alert-${a.severity ? a.severity.toLowerCase() : 'warning'}">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span><strong>${a.title}:</strong> ${a.description}</span>
                    </div>
                `).join('');
                banner.style.display = 'block';
            }
        } catch (e) {
            console.error('Failed to load alerts:', e);
        }
    }

    async loadRecentTickets() {
        const ticketList = document.getElementById('recent-tickets-container');
        if (!ticketList) return;

        try {
            const tickets = await window.ticketService.getMyTickets();
            if (tickets.length === 0) {
                ticketList.innerHTML = '<div class="text-muted p-3">No active tickets found. Book one now!</div>';
                return;
            }
            ticketList.innerHTML = tickets.slice(0, 3).map(t => `
                <div class="ticket-card-mini">
                    <div class="ticket-route">${t.origin_stop} → ${t.destination_stop}</div>
                    <div class="ticket-meta">Ticket #${t.ticket_number} • ₹${t.fare_amount}</div>
                    <span class="badge badge-success">${t.status}</span>
                </div>
            `).join('');
        } catch (e) {
            console.error('Failed to load tickets:', e);
        }
    }

    renderNearbyBuses() {
        const container = document.getElementById('nearby-buses-feed');
        if (!container) return;

        if (this.nearbyBuses.length === 0) {
            container.innerHTML = '<div class="text-muted p-3 text-center"><i class="fas fa-bus-alt fa-2x mb-2 d-block"></i>No active buses currently in transit in your immediate radius. Check full schedule board.</div>';
            return;
        }

        container.innerHTML = this.nearbyBuses.map(b => {
            const distanceStr = b.distance_km ? `${b.distance_km.toFixed(1)} km away` : 'Approaching stop';
            const etaMin = b.eta_minutes ? `${b.eta_minutes} mins` : 'Live';
            const occupancyPct = b.occupancy ? Math.round((b.occupancy / 50) * 100) : 35;
            
            return `
                <div class="nearby-bus-card p-3 mb-2 border rounded hover-shadow cursor-pointer" data-id="${b.id}">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <div>
                            <span class="badge badge-primary font-weight-bold">${b.route || 'City Line'}</span>
                            <strong class="ml-2">${b.bus_number}</strong>
                        </div>
                        <span class="badge ${b.speed > 0 ? 'badge-success' : 'badge-secondary'}">
                            <i class="fas fa-satellite-dish"></i> ${b.speed > 0 ? `${b.speed} km/h` : 'Stopped'}
                        </span>
                    </div>
                    <div class="d-flex justify-content-between text-muted small mt-2">
                        <span><i class="fas fa-map-marker-alt text-danger"></i> ${distanceStr}</span>
                        <span><i class="fas fa-users text-primary"></i> ${occupancyPct}% Full</span>
                        <span class="font-weight-bold text-success"><i class="fas fa-clock"></i> ETA ${etaMin}</span>
                    </div>
                </div>
            `;
        }).join('');

        this.bindBusCardClicks();
    }

    renderBusList(buses) {
        const listContainer = document.getElementById('live-buses-list');
        if (!listContainer) return;

        if (buses.length === 0) {
            listContainer.innerHTML = '<div class="text-muted p-4 text-center">No active buses on route right now.</div>';
            return;
        }

        listContainer.innerHTML = buses.map(bus => `
            <div class="bus-card-item ${this.selectedBus && this.selectedBus.id === bus.id ? 'active' : ''}" data-bus-id="${bus.id}">
                <div class="bus-card-header">
                    <span class="route-badge">${bus.route_rel ? bus.route_rel.route_number : (bus.bus_number || 'BUS')}</span>
                    <span class="status-indicator ${bus.status === 'Delayed' ? 'delayed' : 'on-time'}">${bus.status}</span>
                </div>
                <div class="bus-destination">${bus.route || 'Vijayawada Corridor'}</div>
                <div class="bus-footer-meta">
                    <span><i class="fas fa-tachometer-alt"></i> ${bus.speed || 0} km/h</span>
                    <span><i class="fas fa-users"></i> ${bus.occupancy || 0} pax</span>
                    <span><i class="fas fa-clock"></i> ${bus.last_updated || 'Live'}</span>
                </div>
            </div>
        `).join('');

        listContainer.querySelectorAll('.bus-card-item').forEach(card => {
            card.onclick = () => {
                const busId = Number(card.dataset.busId);
                const bus = this.currentBuses.find(b => b.id === busId);
                if (bus) this.selectBus(bus);
            };
        });
    }

    selectBus(bus) {
        this.selectedBus = bus;
        if (this.mapManager && bus.latitude && bus.longitude) {
            this.mapManager.panTo(bus.latitude, bus.longitude, 16);
        }
        this.renderBusList(this.currentBuses);
        this.showBusBottomDrawer(bus);
    }

    showBusBottomDrawer(bus) {
        let drawer = document.getElementById('bus-detail-drawer');
        if (!drawer) {
            drawer = document.createElement('div');
            drawer.id = 'bus-detail-drawer';
            drawer.className = 'bus-detail-drawer';
            document.body.appendChild(drawer);
        }

        drawer.innerHTML = `
            <div class="drawer-header">
                <h3>Bus ${bus.bus_number} (${bus.route || 'Transit Route'})</h3>
                <button class="drawer-close" onclick="document.getElementById('bus-detail-drawer').classList.remove('open')">&times;</button>
            </div>
            <div class="drawer-body">
                <div class="drawer-stats-grid">
                    <div class="stat-box"><span class="lbl">Speed</span><span class="val">${bus.speed || 0} km/h</span></div>
                    <div class="stat-box"><span class="lbl">Driver</span><span class="val">${bus.driver || 'Assigned'}</span></div>
                    <div class="stat-box"><span class="lbl">Status</span><span class="val">${bus.status}</span></div>
                    <div class="stat-box"><span class="lbl">Capacity</span><span class="val">${bus.occupancy || 0}/${bus.capacity || 45}</span></div>
                </div>
                <div class="drawer-actions">
                    <a href="/bus-details.html?id=${bus.id}" class="btn btn-primary btn-block">Open Live Telemetry & Stop Times</a>
                </div>
            </div>
        `;
        drawer.classList.add('open');
    }

    startLiveTelemetryStream() {
        this.refreshInterval = setInterval(() => {
            this.loadNearbyBuses();
        }, 5000);
    }

    bindEvents() {
        const searchInput = document.getElementById('bus-route-search');
        if (searchInput) {
            searchInput.oninput = (e) => {
                const q = e.target.value.toLowerCase();
                const filtered = this.currentBuses.filter(b => 
                    (b.bus_number && b.bus_number.toLowerCase().includes(q)) ||
                    (b.route && b.route.toLowerCase().includes(q))
                );
                this.renderBusList(filtered);
            };
        }
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('passenger-dashboard-root') || document.getElementById('map')) {
        window.passengerDashboard = new PassengerDashboardController();
        window.passengerDashboard.init();
    }
});
