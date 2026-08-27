/**
 * CityBus Enterprise Platform - Fuel & Energy Service
 * File: js/services/fuelService.js
 * 
 * Handles refueling logs, EV charging sessions, energy expenditure,
 * and fleet fuel efficiency analytics.
 */

class FuelService {
    async getAllFuelLogs(busId = null, page = 1, perPage = 20) {
        let endpoint = `/api/v1/fuel?page=${page}&per_page=${perPage}`;
        if (busId) endpoint += `&bus_id=${busId}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getFuelSummary() {
        const response = await window.apiClient.get('/api/v1/fuel/summary');
        if (response && response.success) {
            return response.summary;
        }
        return {};
    }

    async recordFuelLog(logData) {
        return window.apiClient.post('/api/v1/fuel', logData);
    }
}

// Global Export
window.fuelService = new FuelService();
