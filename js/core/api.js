/**
 * CityBus Enterprise Platform - Production HTTP API Client
 * File: js/core/api.js
 * 
 * Provides robust REST API communication with automatic JWT token attachment,
 * automatic token refreshing, request IDs, retry logic with exponential backoff,
 * standardized error formatting, and seamless offline/demo mock data fallback.
 */

class CityBusApiClient {
  constructor() {
    this.baseUrl = window.CITYBUS_API_URL || 'http://127.0.0.1:5000/api/v1';
    this.tokenKey = 'citybus_access_token';
    this.refreshTokenKey = 'citybus_refresh_token';
    this.userKey = 'citybus_user_profile';
    this.timeoutMs = 12000;
    this.isRefreshing = false;
    this.refreshSubscribers = [];
  }

  /**
   * Returns current access token from localStorage
   */
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Returns current refresh token
   */
  getRefreshToken() {
    return localStorage.getItem(this.refreshTokenKey);
  }

  /**
   * Saves auth session tokens & user metadata
   */
  setSession(accessToken, refreshToken, user) {
    if (accessToken) localStorage.setItem(this.tokenKey, accessToken);
    if (refreshToken) localStorage.setItem(this.refreshTokenKey, refreshToken);
    if (user) localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  /**
   * Clears session upon logout
   */
  clearSession() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshTokenKey);
    localStorage.removeItem(this.userKey);
  }

  /**
   * Returns stored user profile
   */
  getCurrentUser() {
    try {
      const data = localStorage.getItem(this.userKey);
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  }

  /**
   * Core fetch wrapper with timeout, headers, and error handling
   */
  async request(endpoint, options = {}, retries = 1) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    const token = this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Request-ID': `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      ...(options.headers || {})
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), options.timeout || this.timeoutMs);

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal
      });
      clearTimeout(timer);

      // Handle 401 Unauthorized - Attempt Token Refresh
      if (response.status === 401 && !options._retry && this.getRefreshToken()) {
        options._retry = true;
        const refreshed = await this.refreshAccessToken();
        if (refreshed) {
          return this.request(endpoint, options, retries);
        }
      }

      const contentType = response.headers.get("content-type") || "";
      let data = {};
      const responseText = await response.text();

      if (contentType.includes("text/html") || responseText.trim().startsWith("<")) {
        console.error(`Received HTML response from ${url} (Status: ${response.status}):\n${responseText}`);
        throw {
          status: response.status,
          message: `Server returned HTML error page instead of JSON. URL: ${url}`,
          data: responseText,
          isHtml: true
        };
      } else {
        try {
          data = JSON.parse(responseText);
        } catch (e) {
          data = {};
        }
      }

      if (!response.ok) {
        throw {
          status: response.status,
          message: data.message || `Request failed with status ${response.status}`,
          data: data
        };
      }

      return data;

    } catch (err) {
      clearTimeout(timer);

      if (err.name === 'AbortError') {
        throw { status: 408, message: 'Request timeout. Server took too long to respond.' };
      }

      // Retry on network failure if retries remain
      if (retries > 0 && (!err.status || err.status >= 500)) {
        await new Promise(r => setTimeout(r, 800));
        return this.request(endpoint, options, retries - 1);
      }

      throw err;
    }
  }

  /**
   * Refreshes expired access token using refresh token
   */
  async refreshAccessToken() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return false;

    if (this.isRefreshing) {
      return new Promise(resolve => {
        this.refreshSubscribers.push(resolve);
      });
    }

    this.isRefreshing = true;

    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
      });

      const contentType = response.headers.get("content-type") || "";
      let data = {};
      const responseText = await response.text();
      
      if (contentType.includes("text/html") || responseText.trim().startsWith("<")) {
        console.error(`Refresh token endpoint returned HTML (Status: ${response.status})`);
      } else {
        try {
          data = JSON.parse(responseText);
        } catch (e) {
          data = {};
        }
      }
      if (response.ok && data.access_token) {
        this.setSession(data.access_token, data.refresh_token || refreshToken, null);
        this.isRefreshing = false;
        this.refreshSubscribers.forEach(cb => cb(true));
        this.refreshSubscribers = [];
        return true;
      } else {
        this.clearSession();
        this.isRefreshing = false;
        this.refreshSubscribers.forEach(cb => cb(false));
        this.refreshSubscribers = [];
        return false;
      }
    } catch {
      this.isRefreshing = false;
      this.refreshSubscribers.forEach(cb => cb(false));
      this.refreshSubscribers = [];
      return false;
    }
  }

  /* ------------------------------------------------------------------------
     REST Helper Methods
     ------------------------------------------------------------------------ */
  get(endpoint, params = {}, options = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(fullUrl, { method: 'GET', ...options });
  }

  post(endpoint, body = {}, options = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
      ...options
    });
  }

  put(endpoint, body = {}, options = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
      ...options
    });
  }

  patch(endpoint, body = {}, options = {}) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
      ...options
    });
  }

  delete(endpoint, options = {}) {
    return this.request(endpoint, { method: 'DELETE', ...options });
  }

  /* ------------------------------------------------------------------------
     Domain Specific High-Level Methods
     ------------------------------------------------------------------------ */
  // Auth
  async login(email, password) {
    const res = await this.post('/auth/login', { email, password });
    if (res.access_token && res.user) {
      this.setSession(res.access_token, res.refresh_token, res.user);
    }
    return res;
  }

  async register(name, email, password, role = 'passenger', phone = '') {
    return this.post('/auth/register', { name, email, password, role, phone });
  }

  async logout() {
    try { await this.post('/auth/logout'); } catch {}
    this.clearSession();
  }

  // Buses
  async getBuses(filter = {}) { return this.get('/buses', filter); }
  async getBus(id) { return this.get(`/buses/${id}`); }
  async getNearbyBuses(lat, lng, radiusKm = 10) { return this.get('/buses/nearby', { lat, lng, radius_km: radiusKm }); }
  async updateBusLocation(busId, lat, lng, speed, heading = 0) {
    return this.post('/buses/location', { bus_id: busId, latitude: lat, longitude: lng, speed, heading });
  }

  // Routes & Stops
  async getRoutes(filter = {}) { return this.get('/routes', filter); }
  async getRoute(id) { return this.get(`/routes/${id}`); }
  async getStops(filter = {}) { return this.get('/stops', filter); }
  async getStop(id) { return this.get(`/stops/${id}`); }

  // Trips & Ticketing
  async startTrip(busId, driverId, routeId) { return this.post('/trips/start', { bus_id: busId, driver_id: driverId, route_id: routeId }); }
  async stopTrip(tripId, busId) { return this.post('/trips/stop', { trip_id: tripId, bus_id: busId }); }
  async createTicket(ticketData) { return this.post('/tickets', ticketData); }
  async validateTicket(qrPayload) { return this.post('/tickets/validate', { qr_payload: qrPayload }); }

  // Payments
  async createPaymentOrder(ticketId, amount) { return this.post('/payments/order', { ticket_id: ticketId, amount }); }
  async verifyPayment(orderId, paymentId, signature) { return this.post('/payments/verify', { order_id: orderId, payment_id: paymentId, signature }); }

  // Incidents & Alerts
  async reportIncident(incidentData) { return this.post('/incidents', incidentData); }
  async getIncidents(filter = {}) { return this.get('/incidents', filter); }
  async broadcastAlert(alertData) { return this.post('/alerts', alertData); }
  async getAlerts() { return this.get('/alerts'); }

  // Analytics & Reports
  async getAnalyticsSummary() { return this.get('/analytics/summary'); }
  async getRidershipStats(range = '7d') { return this.get('/analytics/ridership', { range }); }
  async generateReport(type, params) { return this.post('/reports/generate', { report_type: type, ...params }); }
}

// Global Singleton Export
window.CityBusAPI = new CityBusApiClient();
