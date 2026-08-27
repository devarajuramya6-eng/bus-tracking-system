/**
 * CityBus Enterprise Platform - Service Alerts & Advisories Service
 * File: js/services/alertService.js
 * 
 * Manages transit service advisories, route delays, maintenance bulletins,
 * and high-priority emergency notifications.
 */

class AlertService {
    async getActiveAlerts(routeId = null) {
        let endpoint = '/api/v1/alerts?active_only=true';
        if (routeId) endpoint += `&route_id=${routeId}`;

        const response = await window.apiClient.get(endpoint);
        if (response && response.success) {
            return response.alerts || [];
        }
        return [];
    }

    async getAllAlerts(page = 1, perPage = 20) {
        const endpoint = `/api/v1/alerts?page=${page}&per_page=${perPage}`;
        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async createAlert(alertData) {
        return window.apiClient.post('/api/v1/alerts', alertData);
    }

    async updateAlert(alertId, alertData) {
        return window.apiClient.put(`/api/v1/alerts/${alertId}`, alertData);
    }

    async toggleAlertStatus(alertId) {
        return window.apiClient.post(`/api/v1/alerts/${alertId}/toggle`);
    }

    async deleteAlert(alertId) {
        return window.apiClient.delete(`/api/v1/alerts/${alertId}`);
    }
}

// Global Export
window.alertService = new AlertService();
