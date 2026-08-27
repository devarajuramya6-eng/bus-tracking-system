/**
 * CityBus Enterprise Platform - Emergency Broadcast & Passenger Advisory Center
 * File: js/dispatcher/emergencyBroadcastCenter.js
 * 
 * Composes corridor-wide service advisories, weather disruption alerts,
 * push notification blasts, and LED platform sign overrides.
 */

class EmergencyBroadcastCenterController {
    constructor() {
        this.routes = [];
        this.activeBroadcasts = [];
    }

    async init() {
        if (!window.authService.requireAuth(['dispatcher', 'fleet_manager', 'admin', 'super_admin'])) {
            return;
        }

        await this.loadRoutes();
        this.bindEvents();
    }

    async loadRoutes() {
        try {
            this.routes = await window.routeService.getAllRoutes();
            this.renderRouteCheckboxes();
        } catch (e) {
            console.error('Broadcast routes load error:', e);
        }
    }

    renderRouteCheckboxes() {
        const container = document.getElementById('broadcast-routes-list');
        if (!container) return;

        container.innerHTML = `
            <div class="row g-2">
                <div class="col-12 mb-2">
                    <label class="form-check-label font-weight-bold">
                        <input type="checkbox" id="select-all-broadcast-routes"> Broadcast to All Corridors (System-Wide)
                    </label>
                </div>
                ${this.routes.map(r => `
                    <div class="col-md-6">
                        <label class="form-check-label small">
                            <input type="checkbox" class="route-broadcast-check" value="${r.id}">
                            <span class="badge badge-primary mr-1">${r.route_number}</span> ${r.name}
                        </label>
                    </div>
                `).join('')}
            </div>
        `;

        const selectAll = document.getElementById('select-all-broadcast-routes');
        if (selectAll) {
            selectAll.onchange = (e) => {
                document.querySelectorAll('.route-broadcast-check').forEach(cb => cb.checked = e.target.checked);
            };
        }
    }

    bindEvents() {
        const publishBtn = document.getElementById('publish-broadcast-btn');
        if (publishBtn) {
            publishBtn.onclick = () => this.handlePublish();
        }
    }

    async handlePublish() {
        const titleInput = document.getElementById('broadcast-title');
        const descInput = document.getElementById('broadcast-desc');
        const severitySelect = document.getElementById('broadcast-severity');

        const title = titleInput ? titleInput.value.trim() : '';
        const desc = descInput ? descInput.value.trim() : '';
        const severity = severitySelect ? severitySelect.value : 'Medium';

        if (!title || !desc) {
            window.toastManager.warning('Title and description are required for broadcast advisories.');
            return;
        }

        const selectedRouteIds = Array.from(document.querySelectorAll('.route-broadcast-check:checked')).map(cb => Number(cb.value));

        try {
            await window.alertService.createAlert({
                title,
                description: desc,
                severity,
                route_id: selectedRouteIds.length === 1 ? selectedRouteIds[0] : null
            });

            window.toastManager.success('Emergency Advisory Broadcast published across mobile apps, web portal, and LED boards!');
            if (titleInput) titleInput.value = '';
            if (descInput) descInput.value = '';
        } catch (e) {
            window.toastManager.error(`Broadcast failed: ${e.message}`);
        }
    }
}

// Global Export
window.emergencyBroadcastCenter = new EmergencyBroadcastCenterController();
