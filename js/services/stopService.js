/**
 * CityBus Enterprise Platform - Stop & Station Data Service
 * File: js/services/stopService.js
 * 
 * Manages transit stop catalogs, nearest stop proximity lookup,
 * stop arrival prediction boards, and station amenities.
 */

class StopService {
    constructor() {
        this.cachedStops = [];
    }

    async getAllStops(search = null, wheelchairOnly = false) {
        let endpoint = '/api/v1/stops?';
        if (search) endpoint += `search=${encodeURIComponent(search)}&`;
        if (wheelchairOnly) endpoint += `wheelchair_only=true&`;

        const response = await window.apiClient.get(endpoint, { useCache: true });
        if (response && response.success) {
            this.cachedStops = response.stops || [];
            return this.cachedStops;
        }
        return [];
    }

    async getStopById(stopId) {
        const response = await window.apiClient.get(`/api/v1/stops/${stopId}`);
        if (response && response.success) {
            return response.stop;
        }
        throw new Error(response.message || `Stop ${stopId} not found`);
    }

    async getNearbyStops(lat, lng, radiusKm = 5.0, limit = 20) {
        const endpoint = `/api/v1/stops/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}&limit=${limit}`;
        const response = await window.apiClient.get(endpoint);
        if (response && response.success) {
            return response.stops || [];
        }
        return [];
    }

    async getStopArrivals(stopId) {
        const response = await window.apiClient.get(`/api/v1/eta/stop/${stopId}`);
        if (response && response.success) {
            return response.arrivals || [];
        }
        return [];
    }

    async createStop(stopData) {
        return window.apiClient.post('/api/v1/stops', stopData);
    }

    async updateStop(stopId, stopData) {
        return window.apiClient.put(`/api/v1/stops/${stopId}`, stopData);
    }

    async deleteStop(stopId) {
        return window.apiClient.delete(`/api/v1/stops/${stopId}`);
    }
}

// Global Export
window.stopService = new StopService();
