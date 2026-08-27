/**
 * CityBus Enterprise Platform - Passenger Stop Arrival Real-Time Board
 * File: js/passenger/stopArrivalBoard.js
 * 
 * Renders next bus arrival departure displays (RTPI), live ETAs, crowding levels,
 * and stop platform amenities.
 */

class StopArrivalBoardController {
    constructor() {
        this.currentStop = null;
        this.arrivals = [];
        this.pollInterval = null;
    }

    async init() {
        const urlParams = new URLSearchParams(window.location.search);
        const stopId = urlParams.get('id') || 1;
        await this.loadStopData(Number(stopId));
    }

    async loadStopData(stopId) {
        try {
            const stop = await window.stopService.getStopById(stopId);
            this.currentStop = stop;
            this.renderStopHeader(stop);

            await this.refreshArrivals(stopId);
            if (this.pollInterval) clearInterval(this.pollInterval);
            this.pollInterval = setInterval(() => this.refreshArrivals(stopId), 5000);
        } catch (e) {
            console.error('Stop arrival board error:', e);
        }
    }

    renderStopHeader(stop) {
        const titleEl = document.getElementById('stop-board-title');
        if (titleEl) titleEl.textContent = `${stop.name} (${stop.stop_code})`;

        const landmarkEl = document.getElementById('stop-board-landmark');
        if (landmarkEl) landmarkEl.textContent = stop.landmark || 'Vijayawada Municipal Platform';
    }

    async refreshArrivals(stopId) {
        try {
            const arrivals = await window.stopService.getStopArrivals(stopId);
            this.arrivals = arrivals;
            this.renderArrivalsTable(arrivals);
        } catch (e) {
            console.error('Arrivals refresh error:', e);
        }
    }

    renderArrivalsTable(arrivals) {
        const container = document.getElementById('stop-arrivals-table-container');
        if (!container) return;

        if (arrivals.length === 0) {
            container.innerHTML = '<div class="text-muted p-4 text-center">No upcoming buses scheduled for this stop in the next 30 minutes.</div>';
            return;
        }

        container.innerHTML = `
            <table class="table table-hover stop-rtpi-table">
                <thead>
                    <tr>
                        <th>Route</th>
                        <th>Destination</th>
                        <th>Crowding</th>
                        <th class="text-end">Live ETA</th>
                    </tr>
                </thead>
                <tbody>
                    ${arrivals.map(arr => `
                        <tr>
                            <td><span class="route-badge">${arr.route_number}</span></td>
                            <td>${arr.destination || 'City Center'}</td>
                            <td>
                                <div class="crowding-indicator">
                                    <i class="fas fa-user ${arr.crowding > 10 ? 'active' : ''}"></i>
                                    <i class="fas fa-user ${arr.crowding > 25 ? 'active' : ''}"></i>
                                    <i class="fas fa-user ${arr.crowding > 40 ? 'active' : ''}"></i>
                                    <span class="pax-count">${arr.crowding || 12} pax</span>
                                </div>
                            </td>
                            <td class="text-end">
                                <span class="eta-countdown-badge ${arr.eta_minutes <= 3 ? 'urgent' : ''}">
                                    ${arr.eta_minutes <= 1 ? 'Approaching' : `${arr.eta_minutes} min`}
                                </span>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('stop-arrival-board-root')) {
        window.stopArrivalBoard = new StopArrivalBoardController();
        window.stopArrivalBoard.init();
    }
});
