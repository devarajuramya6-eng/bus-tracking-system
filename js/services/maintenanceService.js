/**
 * CityBus Enterprise Platform - Maintenance & Workshop Service
 * File: js/services/maintenanceService.js
 * 
 * Handles vehicle work order management, scheduled inspections,
 * technician assignments, and depot workshop repairs.
 */

class MaintenanceService {
    async getAllWorkOrders(status = null, busId = null, priority = null, page = 1, perPage = 20) {
        let endpoint = `/api/v1/maintenance?page=${page}&per_page=${perPage}`;
        if (status) endpoint += `&status=${encodeURIComponent(status)}`;
        if (busId) endpoint += `&bus_id=${busId}`;
        if (priority) endpoint += `&priority=${encodeURIComponent(priority)}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getWorkOrderById(orderId) {
        const response = await window.apiClient.get(`/api/v1/maintenance/${orderId}`);
        if (response && response.success) {
            return response.order;
        }
        throw new Error(response.message || `Work order ${orderId} not found`);
    }

    async createWorkOrder(orderData) {
        return window.apiClient.post('/api/v1/maintenance', orderData);
    }

    async updateWorkOrder(orderId, orderData) {
        return window.apiClient.put(`/api/v1/maintenance/${orderId}`, orderData);
    }

    async deleteWorkOrder(orderId) {
        return window.apiClient.delete(`/api/v1/maintenance/${orderId}`);
    }
}

// Global Export
window.maintenanceService = new MaintenanceService();
