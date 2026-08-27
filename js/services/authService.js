/**
 * CityBus Enterprise Platform - Authentication & Session Service
 * File: js/services/authService.js
 * 
 * Manages user credentials, role-based route access controls,
 * local storage synchronization, and active login state.
 */

class AuthService {
    constructor() {
        this.currentUser = this.loadStoredUser();
        this.listeners = [];
    }

    loadStoredUser() {
        try {
            const raw = localStorage.getItem('citybus_user');
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    isAuthenticated() {
        return !!this.currentUser && !!localStorage.getItem('citybus_access_token');
    }

    getUser() {
        return this.currentUser;
    }

    getRole() {
        return this.currentUser ? this.currentUser.role : 'guest';
    }

    hasRole(roles) {
        if (!this.currentUser) return false;
        if (Array.isArray(roles)) {
            return roles.includes(this.currentUser.role);
        }
        return this.currentUser.role === roles;
    }

    async login(email, password) {
        const response = await window.apiClient.post('/api/v1/auth/login', { email, password });
        if (response.success && response.access_token) {
            window.apiClient.setToken(response.access_token, response.refresh_token);
            this.currentUser = response.user;
            localStorage.setItem('citybus_user', JSON.stringify(response.user));
            this.notifyListeners();
            return response;
        }
        throw new Error(response.message || 'Login failed');
    }

    async register(name, email, password, phone, role = 'passenger') {
        const response = await window.apiClient.post('/api/v1/auth/register', {
            name, email, password, phone, role
        });
        if (response.success && response.access_token) {
            window.apiClient.setToken(response.access_token, response.refresh_token);
            this.currentUser = response.user;
            localStorage.setItem('citybus_user', JSON.stringify(response.user));
            this.notifyListeners();
            return response;
        }
        throw new Error(response.message || 'Registration failed');
    }

    async logout() {
        try {
            await window.apiClient.post('/api/v1/auth/logout').catch(() => {});
        } finally {
            window.apiClient.clearToken();
            this.currentUser = null;
            this.notifyListeners();
            window.location.href = '/login.html';
        }
    }

    async fetchProfile() {
        if (!this.isAuthenticated()) return null;
        const response = await window.apiClient.get('/api/v1/auth/me');
        if (response.success && response.user) {
            this.currentUser = response.user;
            localStorage.setItem('citybus_user', JSON.stringify(response.user));
            this.notifyListeners();
            return response.user;
        }
        return null;
    }

    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    }

    notifyListeners() {
        this.listeners.forEach(cb => {
            try { cb(this.currentUser); } catch (e) { console.error(e); }
        });
    }

    requireAuth(allowedRoles = []) {
        if (!this.isAuthenticated()) {
            window.location.href = `/login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
            return false;
        }
        if (allowedRoles.length > 0 && !allowedRoles.includes(this.getRole())) {
            alert('Access Denied: You do not have permission to view this portal.');
            window.location.href = '/index.html';
            return false;
        }
        return true;
    }
}

// Global Export
window.authService = new AuthService();
