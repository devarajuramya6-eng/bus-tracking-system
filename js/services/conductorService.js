/**
 * CityBus Enterprise Platform - Conductor Service Frontend Client
 * File: js/services/conductorService.js
 * 
 * Provides conductor roster queries, validation metrics, cash remittance,
 * and fare collection sync.
 */

class ConductorService {
    async getAllConductors(status = null, search = null, page = 1, perPage = 20) {
        let endpoint = `/api/v1/conductors?page=${page}&per_page=${perPage}`;
        if (status) endpoint += `&status=${encodeURIComponent(status)}`;
        if (search) endpoint += `&search=${encodeURIComponent(search)}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getConductorById(conductorId) {
        const response = await window.apiClient.get(`/api/v1/conductors/${conductorId}`);
        if (response && response.success) {
            return response;
        }
        throw new Error(response.message || `Conductor ${conductorId} not found`);
    }

    async createConductor(conductorData) {
        return window.apiClient.post('/api/v1/conductors', conductorData);
    }

    async updateConductor(conductorId, conductorData) {
        return window.apiClient.put(`/api/v1/conductors/${conductorId}`, conductorData);
    }

    async deleteConductor(conductorId) {
        return window.apiClient.delete(`/api/v1/conductors/${conductorId}`);
    }
}

// Global Export
window.conductorService = new ConductorService();
