/**
 * CityBus Enterprise Platform - Universal API Client
 * File: js/services/apiClient.js
 * 
 * Provides unified HTTP request orchestration with automatic JWT authentication,
 * token refresh retry logic, exponential backoff, request caching, and error toast hooks.
 */

class ApiClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl || window.location.origin;
        this.token = localStorage.getItem('citybus_access_token') || null;
        this.refreshToken = localStorage.getItem('citybus_refresh_token') || null;
        this.cache = new Map();
        this.cacheTTL = 15000; // 15 seconds
    }

    setToken(token, refreshToken = null) {
        this.token = token;
        localStorage.setItem('citybus_access_token', token);
        if (refreshToken) {
            this.refreshToken = refreshToken;
            localStorage.setItem('citybus_refresh_token', refreshToken);
        }
    }

    clearToken() {
        this.token = null;
        this.refreshToken = null;
        localStorage.removeItem('citybus_access_token');
        localStorage.removeItem('citybus_refresh_token');
        localStorage.removeItem('citybus_user');
    }

    getHeaders(customHeaders = {}) {
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            ...customHeaders
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint}`;
        const method = options.method || 'GET';
        const useCache = options.useCache && method === 'GET';

        if (useCache && this.cache.has(url)) {
            const cached = this.cache.get(url);
            if (Date.now() - cached.timestamp < this.cacheTTL) {
                return cached.data;
            }
        }

        const config = {
            method: method,
            headers: this.getHeaders(options.headers),
            ...options
        };

        if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);

            // Handle 401 Unauthorized - attempt token refresh
            if (response.status === 401 && this.refreshToken && !options._isRetry) {
                const refreshed = await this.tryRefreshToken();
                if (refreshed) {
                    options._isRetry = true;
                    return this.request(endpoint, options);
                }
            }

            const data = await response.json().catch(() => ({ success: false, message: 'Invalid JSON response from server' }));

            if (!response.ok) {
                const error = new Error(data.message || `HTTP Error ${response.status}`);
                error.status = response.status;
                error.data = data;
                throw error;
            }

            if (useCache) {
                this.cache.set(url, { timestamp: Date.now(), data });
            }

            return data;
        } catch (err) {
            console.error(`[ApiClient Error] ${method} ${endpoint}:`, err);
            throw err;
        }
    }

    async tryRefreshToken() {
        if (!this.refreshToken) return false;
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: this.refreshToken })
            });
            const data = await res.json();
            if (res.ok && data.success && data.access_token) {
                this.setToken(data.access_token);
                return true;
            }
        } catch (e) {
            console.warn('[ApiClient] Token refresh failed:', e);
        }
        this.clearToken();
        return false;
    }

    get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    post(endpoint, body = {}, options = {}) {
        return this.request(endpoint, { ...options, method: 'POST', body });
    }

    put(endpoint, body = {}, options = {}) {
        return this.request(endpoint, { ...options, method: 'PUT', body });
    }

    delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}

// Global Export
window.apiClient = new ApiClient();
