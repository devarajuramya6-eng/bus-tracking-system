/**
 * CityBus Enterprise Platform - Real-Time WebSocket & Telemetry Stream Manager
 * File: js/core/ws.js
 * 
 * Manages WebSocket / Socket.IO connection with automatic reconnection,
 * channel subscriptions (bus updates, route channels, emergency alerts, dispatcher feed),
 * and event dispatching to the client application.
 */

class CityBusWebSocketManager {
  constructor() {
    this.socket = null;
    this.serverUrl = window.CITYBUS_WS_URL || 'http://127.0.0.1:5000';
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 2000;
    this.subscribedRooms = new Set();
    this.listeners = new Map();
    this.messageQueue = [];
    this.fallbackSimulatorActive = false;
  }

  /**
   * Initializes the real-time WebSocket connection
   */
  connect() {
    // Check if Socket.IO library is present
    if (typeof io === 'undefined') {
      console.warn('[CityBus WS] Socket.IO library not loaded. Falling back to local event bus.');
      this.initLocalEventBusFallback();
      return;
    }

    const token = window.CityBusAPI ? window.CityBusAPI.getToken() : null;

    try {
      this.socket = io(this.serverUrl, {
        auth: { token: token },
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectDelay,
        timeout: 10000
      });

      this.setupSocketHandlers();
    } catch (err) {
      console.warn('[CityBus WS] Socket connection failed:', err);
      this.initLocalEventBusFallback();
    }
  }

  /**
   * Sets up core socket lifecycle handlers
   */
  setupSocketHandlers() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.fallbackSimulatorActive = false;
      console.log('⚡ [CityBus WS] Connected to real-time telemetry stream. Socket ID:', this.socket.id);
      
      // Update UI network status
      this.emitInternal('network:status', { status: 'online', mode: 'websocket' });

      // Re-subscribe to all active rooms
      this.subscribedRooms.forEach(room => {
        this.socket.emit('subscribe', { room });
      });

      // Flush buffered messages
      while (this.messageQueue.length > 0) {
        const item = this.messageQueue.shift();
        this.socket.emit(item.event, item.data);
      }
    });

    this.socket.on('disconnect', (reason) => {
      this.isConnected = false;
      console.warn('⚠️ [CityBus WS] Disconnected:', reason);
      this.emitInternal('network:status', { status: 'reconnecting', reason });
    });

    this.socket.on('connect_error', (error) => {
      this.reconnectAttempts++;
      console.warn(`⚠️ [CityBus WS] Connection error (${this.reconnectAttempts}/${this.maxReconnectAttempts}):`, error.message);
      
      if (this.reconnectAttempts >= 3 && !this.fallbackSimulatorActive) {
        this.initLocalEventBusFallback();
      }
    });

    // Transit Domain Events
    this.socket.on('gps:update', (data) => this.emitInternal('gps:update', data));
    this.socket.on('eta:update', (data) => this.emitInternal('eta:update', data));
    this.socket.on('trip:status', (data) => this.emitInternal('trip:status', data));
    this.socket.on('ticket:validated', (data) => this.emitInternal('ticket:validated', data));
    this.socket.on('incident:broadcast', (data) => this.emitInternal('incident:broadcast', data));
    this.socket.on('alert:broadcast', (data) => this.emitInternal('alert:broadcast', data));
    this.socket.on('fleet:status', (data) => this.emitInternal('fleet:status', data));
  }

  /**
   * Subscribes to a specific room (e.g. 'bus:BUS-101', 'route:ROUTE-27A', 'dispatcher')
   */
  subscribe(room) {
    this.subscribedRooms.add(room);
    if (this.isConnected && this.socket) {
      this.socket.emit('subscribe', { room });
    }
  }

  /**
   * Unsubscribes from a room
   */
  unsubscribe(room) {
    this.subscribedRooms.delete(room);
    if (this.isConnected && this.socket) {
      this.socket.emit('unsubscribe', { room });
    }
  }

  /**
   * Emits an event to the backend server with offline queue fallback
   */
  emit(event, data = {}) {
    if (this.isConnected && this.socket) {
      this.socket.emit(event, data);
    } else {
      this.messageQueue.push({ event, data, timestamp: Date.now() });
    }
  }

  /**
   * Registers a client listener for real-time events
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);

    return () => this.off(event, callback);
  }

  /**
   * Removes an event listener
   */
  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  /**
   * Dispatches event internally to registered client callbacks
   */
  emitInternal(event, payload) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(cb => {
        try {
          cb(payload);
        } catch (err) {
          console.error(`[CityBus WS] Error in listener for ${event}:`, err);
        }
      });
    }

    // Also dispatch as a native window CustomEvent for global component decoupled reactivity
    window.dispatchEvent(new CustomEvent(`citybus:${event}`, { detail: payload }));
  }

  /**
   * Fallback to in-browser local event bus when server is offline/unreachable
   */
  initLocalEventBusFallback() {
    this.fallbackSimulatorActive = true;
    console.log('🔄 [CityBus WS] Local standalone mode active. Telemetry updates routed via internal engine.');
    this.emitInternal('network:status', { status: 'offline-local', mode: 'standalone' });
  }
}

// Global Singleton Export
window.CityBusWS = new CityBusWebSocketManager();
