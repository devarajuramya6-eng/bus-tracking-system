/**
 * CityBus Enterprise Platform - Universal Accessibility Transit Planner
 * File: js/passenger/accessibilityPlanner.js
 * 
 * Filters journeys for low-floor wheelchair accessible ramps, priority seat booking,
 * and audio-visual annunciator platform support.
 */

class AccessibilityPlannerController {
    constructor() {
        this.accessibleRoutes = [];
    }

    async init() {
        await this.loadAccessibleRoutes();
    }

    async loadAccessibleRoutes() {
        const container = document.getElementById('accessible-routes-container');
        if (!container) return;

        try {
            const res = await window.apiClient.get('/api/v1/accessibility/routes');
            this.accessibleRoutes = res.accessible_routes || [];

            container.innerHTML = `
                <div class="row g-3">
                    ${this.accessibleRoutes.map(r => `
                        <div class="col-md-6 col-lg-4">
                            <div class="card h-100 border-0 shadow-sm">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span class="badge badge-primary font-weight-bold">${r.route_number}</span>
                                        <span class="badge ${r.has_wheelchair_ramp ? 'badge-success' : 'badge-secondary'}">
                                            <i class="fas fa-wheelchair"></i> ${r.has_wheelchair_ramp ? '100% Accessible' : 'Standard'}
                                        </span>
                                    </div>
                                    <h5 class="card-title">${r.name}</h5>
                                    <p class="small text-muted mb-2">${r.wheelchair_accessible_buses} of ${r.total_buses} buses equipped with power ramps</p>
                                    <ul class="list-unstyled small text-success mb-3">
                                        ${r.features.map(f => `<li><i class="fas fa-check-circle"></i> ${f}</li>`).join('')}
                                    </ul>
                                    <a href="/journey-planner.html?route=${r.route_id}" class="btn btn-outline-primary btn-sm btn-block">Plan Step-Free Trip</a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (e) {
            console.error('Accessibility routes load error:', e);
        }
    }
}

// Global Export
window.accessibilityPlanner = new AccessibilityPlannerController();
