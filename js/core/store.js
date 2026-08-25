/**
 * CityBus Enterprise Platform - Reactive Central Data Store
 * File: js/core/store.js
 * 
 * Provides centralized reactive state for live buses, routes, stops,
 * active trips, telemetry buffers, favorites, and service notifications.
 */

class CityBusStore {
  constructor() {
    this.state = {
      buses: [],
      routes: [],
      stops: [],
      drivers: [],
      conductors: [],
      activeTrips: [],
      favorites: { buses: ['BUS-101', 'BUS-102'], routes: ['ROUTE-27A'], stops: ['STOP-4'] },
      alerts: [],
      notifications: [],
      networkStatus: 'online',
      selectedBusId: null,
      selectedRouteId: null,
      userLocation: null
    };

    this.listeners = new Map();
    this.loadFavoritesFromStorage();
    this.initNetworkMonitoring();
  }

  getState() {
    return this.state;
  }

  setState(partialState) {
    const previousState = { ...this.state };
    this.state = { ...this.state, ...partialState };

    Object.keys(partialState).forEach(key => {
      if (this.listeners.has(key)) {
        this.listeners.get(key).forEach(cb => cb(this.state[key], previousState[key]));
      }
    });

    // Global store update event
    window.dispatchEvent(new CustomEvent('citybus:store-updated', {
      detail: { state: this.state, changedKeys: Object.keys(partialState) }
    }));
  }

  subscribe(key, callback) {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key).add(callback);
    return () => this.listeners.get(key).delete(callback);
  }

  /* ------------------------------------------------------------------------
     Favorites Management
     ------------------------------------------------------------------------ */
  loadFavoritesFromStorage() {
    try {
      const data = localStorage.getItem('citybus_favorites_store');
      if (data) {
        this.state.favorites = JSON.parse(data);
      }
    } catch {}
  }

  saveFavoritesToStorage() {
    try {
      localStorage.setItem('citybus_favorites_store', JSON.stringify(this.state.favorites));
    } catch {}
  }

  isFavorite(type, id) {
    const list = this.state.favorites[type] || [];
    return list.includes(id);
  }

  toggleFavorite(type, id) {
    const list = this.state.favorites[type] || [];
    let isAdded = false;
    if (list.includes(id)) {
      this.state.favorites[type] = list.filter(item => item !== id);
      isAdded = false;
    } else {
      this.state.favorites[type] = [...list, id];
      isAdded = true;
    }

    this.saveFavoritesToStorage();
    this.setState({ favorites: { ...this.state.favorites } });

    if (window.showToast) {
      window.showToast(isAdded ? `Added ${id} to favorites` : `Removed ${id} from favorites`, 'info');
    }
    return isAdded;
  }

  /* ------------------------------------------------------------------------
     Network Online/Offline Monitoring
     ------------------------------------------------------------------------ */
  initNetworkMonitoring() {
    window.addEventListener('online', () => {
      this.setState({ networkStatus: 'online' });
      this.removeOfflineBanner();
      if (window.showToast) window.showToast('Network restored. Reconnected to live stream.', 'success');
    });

    window.addEventListener('offline', () => {
      this.setState({ networkStatus: 'offline' });
      this.showOfflineBanner();
      if (window.showToast) window.showToast('You are offline. Showing cached schedules.', 'warning');
    });
  }

  showOfflineBanner() {
    let banner = document.getElementById('global-offline-banner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'global-offline-banner';
      banner.className = 'offline-banner';
      banner.innerHTML = `
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span><strong>OFFLINE MODE:</strong> Live GPS is unavailable. Displaying cached timetable data.</span>
      `;
      document.body.prepend(banner);
    }
  }

  removeOfflineBanner() {
    const banner = document.getElementById('global-offline-banner');
    if (banner) banner.remove();
  }
}

// Global Singleton Export
window.CityBusStore = new CityBusStore();
