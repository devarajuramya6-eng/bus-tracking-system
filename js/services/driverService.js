/**
 * CityBus Enterprise Platform - Driver Service Frontend Client
 * File: js/services/driverService.js
 * 
 * Provides driver roster queries, driver cockpit controls, shift handling,
 * and driver duty management.
 */

class DriverService {
    async getAllDrivers(status = null, search = null, page = 1, perPage = 20) {
        let endpoint = `/api/v1/drivers?page=${page}&per_page=${perPage}`;
        if (status) endpoint += `&status=${encodeURIComponent(status)}`;
        if (search) endpoint += `&search=${encodeURIComponent(search)}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getDriverById(driverId) {
        const response = await window.apiClient.get(`/api/v1/drivers/${driverId}`);
        if (response && response.success) {
            return response.driver;
        }
        throw new Error(response.message || `Driver ${driverId} not found`);
    }

    async createDriver(driverData) {
        return window.apiClient.post('/api/v1/drivers', driverData);
    }

    async updateDriver(driverId, driverData) {
        return window.apiClient.put(`/api/v1/drivers/${driverId}`, driverData);
    }

    async deleteDriver(driverId) {
        return window.apiClient.delete(`/api/v1/drivers/${driverId}`);
    }

    async getDriverTrips(driverId) {
        const response = await window.apiClient.get(`/api/v1/drivers/${driverId}/trips`);
        if (response && response.success) {
            return response.trips || [];
        }
        return [];
    }
}

// Global Export
window.driverService = new DriverService();
