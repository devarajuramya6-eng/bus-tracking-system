/**
 * CityBus Enterprise Platform - Live Fleet Radar & Telemetry Feed
 * File: js/dispatcher/liveFleetRadar.js
 * 
 * Provides high-frequency bus radar tracking, speed gauge visualizers,
 * delayed corridor filters, and direct driver radio ping buttons.
 */

class LiveFleetRadarController {
    constructor() {
        this.buses = [];
        this.filterStatus = 'ALL';
        this.searchQuery = '';
        this.pollTimer = null;
    }

    async init() {
        if (!window.authService.requireAuth(['dispatcher', 'fleet_manager', 'admin', 'super_admin'])) {
            return;
        }

        await this.loadRadar();
        this.bindEvents();
        this.pollTimer = setInterval(() => this.loadRadar(), 4000);
    }

    async loadRadar() {
        try {
            const buses = await window.busService.getAllBuses();
            this.buses = buses;
            this.renderRadar();
        } catch (e) {
            console.error('Radar poll error:', e);
        }
    }

    getFilteredBuses() {
        let list = [...this.buses];
        if (this.filterStatus !== 'ALL') {
            list = list.filter(b => b.status === this.filterStatus);
        }
        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            list = list.filter(b => 
                (b.bus_number && b.bus_number.toLowerCase().includes(q)) ||
                (b.route && b.route.toLowerCase().includes(q)) ||
                (b.driver && b.driver.toLowerCase().includes(q))
            );
        }
        return list;
    }

    renderRadar() {
        const container = document.getElementById('radar-vehicles-grid');
        if (!container) return;

        const buses = this.getFilteredBuses();

        if (buses.length === 0) {
            container.innerHTML = '<div class="text-muted p-4 text-center">No vehicles match current radar filters.</div>';
            return;
        }

        container.innerHTML = buses.map(bus => `
            <div class="radar-bus-card status-${bus.status.toLowerCase().replace(/\s+/g, '-')}" data-id="${bus.id}">
                <div class="radar-card-header">
                    <div class="bus-id-badge">${bus.bus_number}</div>
                    <span class="badge ${bus.status === 'Delayed' ? 'badge-warning' : (bus.status === 'On Route' ? 'badge-success' : 'badge-secondary')}">${bus.status}</span>
                </div>
                <div class="radar-card-route">${bus.route || 'Transit Corridor'}</div>
                <div class="radar-telemetry-row">
                    <div class="radar-stat"><i class="fas fa-tachometer-alt"></i> <span>${bus.speed || 0} km/h</span></div>
                    <div class="radar-stat"><i class="fas fa-users"></i> <span>${bus.occupancy || 0}/${bus.capacity || 45}</span></div>
                    <div class="radar-stat"><i class="fas fa-user"></i> <span>${bus.driver || 'Assigned'}</span></div>
                </div>
                <div class="radar-card-actions">
                    <button class="btn btn-xs btn-outline-primary ping-driver-btn" data-id="${bus.id}"><i class="fas fa-broadcast-tower"></i> Radio Ping</button>
                    <button class="btn btn-xs btn-outline-secondary track-map-btn" data-id="${bus.id}"><i class="fas fa-crosshairs"></i> Track</button>
                </div>
            </div>
        `).join('');

        this.bindCardActions();
    }

    bindCardActions() {
        document.querySelectorAll('.ping-driver-btn').forEach(btn => {
            btn.onclick = () => {
                const id = btn.dataset.id;
                const bus = this.buses.find(b => String(b.id) === String(id));
                const msg = prompt(`Send radio advisory message to driver of Bus ${bus ? bus.bus_number : id}:`);
                if (msg) {
                    window.toastManager.success(`Advisory sent to Bus ${bus ? bus.bus_number : id}`);
                }
            };
        });

        document.querySelectorAll('.track-map-btn').forEach(btn => {
            btn.onclick = () => {
                const id = btn.dataset.id;
                const bus = this.buses.find(b => String(b.id) === String(id));
                if (bus && window.dispatcherConsole) {
                    window.dispatcherConsole.selectBus(bus);
                }
            };
        });
    }

    bindEvents() {
        const filterBtns = document.querySelectorAll('.radar-filter-btn');
        filterBtns.forEach(btn => {
            btn.onclick = () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.filterStatus = btn.dataset.status;
                this.renderRadar();
            };
        });

        const searchInput = document.getElementById('radar-search-input');
        if (searchInput) {
            searchInput.oninput = (e) => {
                this.searchQuery = e.target.value;
                this.renderRadar();
            };
        }
    }
}

// Global Export
window.liveFleetRadar = new LiveFleetRadarController();
