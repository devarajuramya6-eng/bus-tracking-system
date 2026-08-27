/**
 * CityBus Enterprise Platform - Bus Data & Telemetry Service
 * File: js/services/busService.js
 * 
 * Provides client methods to fetch all fleet vehicles, query nearby buses,
 * retrieve single vehicle telemetry/ETA, and push live driver GPS pings.
 */

class BusService {
    constructor() {
        this.activeBuses = [];
        this.subscribers = [];
    }

    async getAllBuses(status = null, routeId = null) {
        let endpoint = '/api/v1/buses?';
        if (status) endpoint += `status=${encodeURIComponent(status)}&`;
        if (routeId) endpoint += `route_id=${encodeURIComponent(routeId)}&`;
        
        const response = await window.apiClient.get(endpoint, { useCache: true });
        if (response && response.success) {
            this.activeBuses = response.buses || [];
            return this.activeBuses;
        }
        return [];
    }

    async getBusById(busId) {
        const response = await window.apiClient.get(`/api/v1/buses/${busId}`);
        if (response && response.success) {
            return response.bus;
        }
        throw new Error(response.message || `Bus ${busId} not found`);
    }

    async getNearbyBuses(lat, lng, radiusKm = 15.0) {
        const endpoint = `/api/v1/buses/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`;
        const response = await window.apiClient.get(endpoint);
        if (response && response.success) {
            return response.buses || [];
        }
        return [];
    }

    async updateLocation(busId, latitude, longitude, speed = 0.0, heading = null, accuracy = 5.0) {
        const body = {
            bus_id: busId,
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude),
            speed: parseFloat(speed),
            heading: heading !== null ? parseFloat(heading) : null,
            accuracy: parseFloat(accuracy)
        };
        const response = await window.apiClient.post('/api/v1/buses/location', body);
        return response;
    }

    async createBus(busData) {
        return window.apiClient.post('/api/v1/buses', busData);
    }

    async updateBus(busId, busData) {
        return window.apiClient.put(`/api/v1/buses/${busId}`, busData);
    }

    async deleteBus(busId) {
        return window.apiClient.delete(`/api/v1/buses/${busId}`);
    }

    async getBusTrail(busId, limit = 50) {
        const response = await window.apiClient.get(`/api/v1/telemetry/trail/${busId}?limit=${limit}`);
        if (response && response.success) {
            return response.trail || [];
        }
        return [];
    }
}

// Global Export
window.busService = new BusService();
