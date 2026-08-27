/**
 * CityBus Enterprise Platform - Trip Lifecycle Service
 * File: js/services/tripService.js
 * 
 * Coordinates operational trip start/pause/resume/stop actions,
 * active trip monitoring, and passenger ride tracking.
 */

class TripService {
    async startTrip(busId, driverId, routeId, conductorId = null) {
        const body = {
            bus_id: busId,
            driver_id: driverId,
            route_id: routeId,
            conductor_id: conductorId
        };
        const response = await window.apiClient.post('/api/v1/trips/start', body);
        return response;
    }

    async stopTrip(tripId, busId = null) {
        const body = { trip_id: tripId, bus_id: busId };
        const response = await window.apiClient.post('/api/v1/trips/stop', body);
        return response;
    }

    async pauseTrip(tripId, reason = 'Traffic Delay') {
        return window.apiClient.post(`/api/v1/trips/${tripId}/pause`, { reason });
    }

    async resumeTrip(tripId) {
        return window.apiClient.post(`/api/v1/trips/${tripId}/resume`);
    }

    async getActiveTrips() {
        const response = await window.apiClient.get('/api/v1/trips?status=Active');
        if (response && response.success) {
            return response.trips || [];
        }
        return [];
    }

    async getTripById(tripId) {
        const response = await window.apiClient.get(`/api/v1/trips/${tripId}`);
        if (response && response.success) {
            return response.trip;
        }
        throw new Error(response.message || `Trip ${tripId} not found`);
    }

    async getTripTrail(tripId) {
        const response = await window.apiClient.get(`/api/v1/telemetry/trip/${tripId}`);
        if (response && response.success) {
            return response.trail || [];
        }
        return [];
    }
}

// Global Export
window.tripService = new TripService();
