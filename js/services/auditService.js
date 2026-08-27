/**
 * CityBus Enterprise Platform - Audit Log Service
 * File: js/services/auditService.js
 * 
 * Provides client operations for compliance log inspection,
 * security auditing, and user activity traces.
 */

class AuditService {
    async getAuditLogs(entity = null, action = null, userId = null, search = null, page = 1, perPage = 50) {
        let endpoint = `/api/v1/audit?page=${page}&per_page=${perPage}`;
        if (entity) endpoint += `&entity=${encodeURIComponent(entity)}`;
        if (action) endpoint += `&action=${encodeURIComponent(action)}`;
        if (userId) endpoint += `&user_id=${userId}`;
        if (search) endpoint += `&search=${encodeURIComponent(search)}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getUserActivity(userId, limit = 25) {
        const response = await window.apiClient.get(`/api/v1/audit/user/${userId}?limit=${limit}`);
        if (response && response.success) {
            return response.logs || [];
        }
        return [];
    }
}

// Global Export
window.auditService = new AuditService();
