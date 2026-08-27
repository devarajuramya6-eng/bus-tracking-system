/**
 * CityBus Enterprise Platform - Multimodal Journey Planner Controller
 * File: js/passenger/multimodalPlanner.js
 * 
 * Provides door-to-door itinerary search combining walking, CityBus express routes,
 * feeder microtransit, and shared mobility with carbon/calorie displays.
 */

class MultimodalPlannerController {
    constructor() {
        this.originCoords = [16.5062, 80.6480];
        this.destCoords = [16.5186, 80.6200];
        this.itineraries = [];
    }

    async init() {
        this.bindEvents();
    }

    bindEvents() {
        const planBtn = document.getElementById('search-multimodal-btn');
        if (planBtn) {
            planBtn.onclick = () => this.handleSearch();
        }

        const swapBtn = document.getElementById('swap-locations-btn');
        if (swapBtn) {
            swapBtn.onclick = () => {
                const origInput = document.getElementById('planner-origin-input');
                const destInput = document.getElementById('planner-dest-input');
                if (origInput && destInput) {
                    const temp = origInput.value;
                    origInput.value = destInput.value;
                    destInput.value = temp;
                }
            };
        }
    }

    async handleSearch() {
        const container = document.getElementById('itineraries-results-container');
        if (!container) return;

        container.innerHTML = '<div class="text-center p-4"><div class="spinner-border text-primary"></div><p class="mt-2 text-muted">Calculating optimal multimodal itineraries...</p></div>';

        try {
            const res = await window.apiClient.get(`/api/v1/multimodal/plan?origin_lat=${this.originCoords[0]}&origin_lng=${this.originCoords[1]}&dest_lat=${this.destCoords[0]}&dest_lng=${this.destCoords[1]}`);
            this.itineraries = (res && res.itineraries) ? res.itineraries : [];
            this.renderItineraries(this.itineraries);
        } catch (e) {
            container.innerHTML = `<div class="alert alert-danger">Error planning trip: ${e.message}</div>`;
        }
    }

    renderItineraries(itineraries) {
        const container = document.getElementById('itineraries-results-container');
        if (!container) return;

        if (itineraries.length === 0) {
            container.innerHTML = '<div class="text-muted p-4 text-center">No transit options found for this journey. Try adjusting start/end points.</div>';
            return;
        }

        container.innerHTML = itineraries.map(itin => `
            <div class="itinerary-card">
                <div class="itinerary-header">
                    <div class="itin-title-wrap">
                        <h4>${itin.title}</h4>
                        <span class="badge badge-success">${itin.tag || 'FASTEST'}</span>
                    </div>
                    <div class="itin-fare">₹${itin.total_fare_inr.toFixed(2)}</div>
                </div>
                <div class="itin-stats-row">
                    <span><i class="fas fa-clock"></i> ${itin.total_duration_minutes} min</span>
                    <span><i class="fas fa-walking"></i> ${itin.walking_distance_km} km walk</span>
                    <span><i class="fas fa-leaf text-success"></i> ${itin.co2_saved_kg} kg CO2 saved</span>
                    <span><i class="fas fa-fire text-warning"></i> ${itin.calories_burned_kcal} kcal</span>
                </div>
                <div class="itinerary-legs-timeline">
                    ${itin.legs.map((leg, idx) => `
                        <div class="timeline-leg ${leg.mode.toLowerCase()}">
                            <div class="leg-icon-dot"><i class="fas ${leg.mode === 'WALK' ? 'fa-walking' : 'fa-bus'}"></i></div>
                            <div class="leg-body">
                                <strong>${leg.instruction}</strong>
                                <span class="text-muted d-block">${leg.duration_minutes} min • ${leg.distance_km} km</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="itin-footer mt-3">
                    <a href="/tickets.html" class="btn btn-primary btn-sm btn-block">Book Digital Ticket for This Trip</a>
                </div>
            </div>
        `).join('');
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('multimodal-planner-root')) {
        window.multimodalPlanner = new MultimodalPlannerController();
        window.multimodalPlanner.init();
    }
});
