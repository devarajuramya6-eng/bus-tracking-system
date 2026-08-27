/**
 * CityBus Enterprise Platform - Public Timetable & Departure Schedule Manager
 * File: js/admin/timetableManager.js
 * 
 * Configures fixed departure schedules, stop dwell buffers, weekend vs weekday variations,
 * and exports GTFS frequencies.txt data.
 */

class TimetableManagerController {
    constructor() {
        this.routes = [];
        this.selectedRouteId = 1;
        this.serviceDay = 'WEEKDAY';
        this.timetableData = null;
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'dispatcher'])) {
            return;
        }

        await this.loadRoutes();
        this.bindEvents();
    }

    async loadRoutes() {
        try {
            this.routes = await window.routeService.getAllRoutes();
            this.renderRouteSelector();
            if (this.routes.length > 0) {
                this.loadTimetable(this.routes[0].id);
            }
        } catch (e) {
            console.error('Timetable routes error:', e);
        }
    }

    renderRouteSelector() {
        const select = document.getElementById('timetable-route-select');
        if (!select) return;

        select.innerHTML = this.routes.map(r => `
            <option value="${r.id}">${r.route_number} - ${r.start_point} ⇄ ${r.destination}</option>
        `).join('');

        select.onchange = (e) => {
            this.selectedRouteId = Number(e.target.value);
            this.loadTimetable(this.selectedRouteId);
        };
    }

    async loadTimetable(routeId) {
        const container = document.getElementById('timetable-grid-container');
        if (!container) return;

        try {
            const res = await window.apiClient.get(`/api/v1/timetable/route/${routeId}?day=${this.serviceDay}`);
            this.timetableData = res;

            const departures = res.departures || [];
            const stops = res.stops || [];

            container.innerHTML = `
                <div class="timetable-card p-3 bg-white border rounded shadow-sm">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h4>${res.route_number} Scheduled Timetable</h4>
                            <p class="text-muted mb-0">${res.corridor_name} • ${res.total_daily_trips} Daily Runs</p>
                        </div>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-primary day-filter-btn ${this.serviceDay === 'WEEKDAY' ? 'active' : ''}" data-day="WEEKDAY">Weekday</button>
                            <button class="btn btn-sm btn-outline-primary day-filter-btn ${this.serviceDay === 'WEEKEND' ? 'active' : ''}" data-day="WEEKEND">Weekend</button>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-sm table-striped timetable-table">
                            <thead>
                                <tr>
                                    <th>Trip #</th>
                                    <th>Origin Dep.</th>
                                    ${stops.map(s => `<th>${s.name}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${departures.map(d => `
                                    <tr>
                                        <td><code>${d.trip_code}</code></td>
                                        <td><strong>${d.origin_departure}</strong></td>
                                        ${(d.stop_times || []).map(st => `<td>${st.scheduled_time}</td>`).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            this.bindDayButtons();
        } catch (e) {
            console.error('Timetable load error:', e);
        }
    }

    bindDayButtons() {
        document.querySelectorAll('.day-filter-btn').forEach(btn => {
            btn.onclick = () => {
                this.serviceDay = btn.dataset.day;
                this.loadTimetable(this.selectedRouteId);
            };
        });
    }

    bindEvents() {
        const printBtn = document.getElementById('print-timetable-btn');
        if (printBtn) {
            printBtn.onclick = () => window.print();
        }
    }
}

// Global Export
window.timetableManager = new TimetableManagerController();
