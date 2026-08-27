/**
 * CityBus Enterprise Platform - Route Stop Sequence & Corridor Builder
 * File: js/admin/routeStopBuilder.js
 * 
 * Provides interactive route geometry creator, stop waypoint sequencer,
 * automatic corridor distance calculation, and base fare tiering.
 */

class RouteStopBuilderController {
    constructor() {
        this.routes = [];
        this.allStops = [];
        this.selectedRoute = null;
        this.activeStopSequence = [];
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'fleet_manager'])) {
            return;
        }

        await this.loadInitialData();
        this.bindEvents();
    }

    async loadInitialData() {
        try {
            this.routes = await window.routeService.getAllRoutes();
            this.allStops = await window.stopService.getAllStops();
            this.renderRouteSelector();
        } catch (e) {
            console.error('Failed to load route builder data:', e);
        }
    }

    renderRouteSelector() {
        const select = document.getElementById('builder-route-select');
        if (!select) return;

        select.innerHTML = `
            <option value="">-- Choose Corridor Route to Edit --</option>
            ${this.routes.map(r => `
                <option value="${r.id}">${r.route_number} - ${r.start_point} ⇄ ${r.destination} (${r.distance_km} km)</option>
            `).join('')}
        `;

        select.onchange = (e) => {
            const routeId = Number(e.target.value);
            if (routeId) this.loadRouteSequence(routeId);
        };
    }

    async loadRouteSequence(routeId) {
        try {
            const route = await window.routeService.getRouteById(routeId);
            this.selectedRoute = route;
            this.activeStopSequence = route.stops || [];
            this.renderSequenceList();
        } catch (e) {
            console.error('Failed to load route stops:', e);
        }
    }

    renderSequenceList() {
        const container = document.getElementById('route-stop-sequence-container');
        if (!container) return;

        if (this.activeStopSequence.length === 0) {
            container.innerHTML = '<div class="text-muted p-4 text-center">No stops assigned to this corridor yet. Add stops from the palette below.</div>';
            return;
        }

        container.innerHTML = `
            <div class="stop-sequence-builder-list">
                ${this.activeStopSequence.map((stop, idx) => `
                    <div class="sequence-stop-card" data-stop-id="${stop.id}" data-index="${idx}">
                        <div class="order-badge">${idx + 1}</div>
                        <div class="stop-card-info">
                            <strong>${stop.name}</strong>
                            <small class="text-muted d-block">Code: ${stop.stop_code || 'STP'} • ${stop.landmark || 'Platform'}</small>
                        </div>
                        <div class="sequence-actions">
                            <button class="btn btn-xs btn-outline-secondary move-up-btn" ${idx === 0 ? 'disabled' : ''}><i class="fas fa-arrow-up"></i></button>
                            <button class="btn btn-xs btn-outline-secondary move-down-btn" ${idx === this.activeStopSequence.length - 1 ? 'disabled' : ''}><i class="fas fa-arrow-down"></i></button>
                            <button class="btn btn-xs btn-outline-danger remove-stop-btn"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                `).join('')}
            </div>
            <div class="mt-3 text-end">
                <button class="btn btn-success" id="save-sequence-btn"><i class="fas fa-save"></i> Save Corridor Sequence</button>
            </div>
        `;

        this.bindSequenceActions();
    }

    bindSequenceActions() {
        const container = document.getElementById('route-stop-sequence-container');
        if (!container) return;

        container.querySelectorAll('.move-up-btn').forEach((btn, idx) => {
            btn.onclick = () => {
                const temp = this.activeStopSequence[idx];
                this.activeStopSequence[idx] = this.activeStopSequence[idx - 1];
                this.activeStopSequence[idx - 1] = temp;
                this.renderSequenceList();
            };
        });

        container.querySelectorAll('.move-down-btn').forEach((btn, idx) => {
            btn.onclick = () => {
                const temp = this.activeStopSequence[idx];
                this.activeStopSequence[idx] = this.activeStopSequence[idx + 1];
                this.activeStopSequence[idx + 1] = temp;
                this.renderSequenceList();
            };
        });

        container.querySelectorAll('.remove-stop-btn').forEach((btn, idx) => {
            btn.onclick = () => {
                this.activeStopSequence.splice(idx, 1);
                this.renderSequenceList();
            };
        });

        const saveBtn = document.getElementById('save-sequence-btn');
        if (saveBtn) {
            saveBtn.onclick = async () => {
                if (!this.selectedRoute) return;
                const stopIds = this.activeStopSequence.map(s => s.id);
                try {
                    await window.apiClient.post(`/api/v1/routes/${this.selectedRoute.id}/stops`, { stop_ids: stopIds });
                    window.toastManager.success('Route stop sequence successfully updated!');
                } catch (e) {
                    window.toastManager.error(`Failed to update sequence: ${e.message}`);
                }
            };
        }
    }

    bindEvents() {
        const addStopSelect = document.getElementById('available-stops-select');
        const appendBtn = document.getElementById('append-stop-to-route-btn');
        if (addStopSelect && this.allStops.length > 0) {
            addStopSelect.innerHTML = this.allStops.map(s => `
                <option value="${s.id}">${s.name} (${s.stop_code})</option>
            `).join('');
        }

        if (appendBtn && addStopSelect) {
            appendBtn.onclick = () => {
                const stopId = Number(addStopSelect.value);
                const stopObj = this.allStops.find(s => s.id === stopId);
                if (stopObj) {
                    this.activeStopSequence.push(stopObj);
                    this.renderSequenceList();
                    window.toastManager.info(`Added ${stopObj.name} to corridor sequence.`);
                }
            };
        }
    }
}

// Global Export
window.routeStopBuilder = new RouteStopBuilderController();
