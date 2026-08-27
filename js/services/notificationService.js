/**
 * CityBus Enterprise Platform - User Notification Service
 * File: js/services/notificationService.js
 * 
 * Coordinates in-app notifications, unread badges, toast alerts,
 * and user alert preference settings.
 */

class NotificationService {
    constructor() {
        this.unreadCount = 0;
        this.listeners = [];
    }

    async getNotifications(unreadOnly = false, page = 1, perPage = 20) {
        const endpoint = `/api/v1/notifications?unread_only=${unreadOnly}&page=${page}&per_page=${perPage}`;
        const response = await window.apiClient.get(endpoint);
        if (response && response.success) {
            this.unreadCount = response.unread_count || 0;
            this.notifyListeners();
            return response;
        }
        return { notifications: [], total: 0, unread_count: 0 };
    }

    async fetchUnreadCount() {
        const response = await window.apiClient.get('/api/v1/notifications/unread-count');
        if (response && response.success) {
            this.unreadCount = response.unread_count;
            this.notifyListeners();
            return this.unreadCount;
        }
        return 0;
    }

    async markAsRead(notificationId) {
        const response = await window.apiClient.post(`/api/v1/notifications/${notificationId}/read`);
        if (response && response.success) {
            this.unreadCount = Math.max(0, this.unreadCount - 1);
            this.notifyListeners();
        }
        return response;
    }

    async markAllAsRead() {
        const response = await window.apiClient.post('/api/v1/notifications/read-all');
        if (response && response.success) {
            this.unreadCount = 0;
            this.notifyListeners();
        }
        return response;
    }

    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    }

    notifyListeners() {
        this.listeners.forEach(cb => {
            try { cb(this.unreadCount); } catch (e) {}
        });
    }
}

// Global Export
window.notificationService = new NotificationService();
