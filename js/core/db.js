/**
 * CityBus Enterprise Platform - IndexedDB Offline Storage & Synchronization Engine
 * File: js/core/db.js
 * 
 * Provides production-grade transactional client-side storage:
 * - Persistent caching for routes, stops, buses, and user tickets
 * - Offline mutation queue (stores tickets created, validations, incident reports offline)
 * - Automatic background synchronization when network reconnects
 */

class CityBusIndexedDB {
  constructor() {
    this.dbName = 'CityBusEnterpriseDB';
    this.dbVersion = 2;
    this.db = null;
    this.isReady = false;
    this.initPromise = this.init();
  }

  async init() {
    return new Promise((resolve, reject) => {
      if (!window.indexedDB) {
        console.warn('[CityBus DB] IndexedDB not supported by browser environment.');
        resolve(null);
        return;
      }

      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // 1. Buses cache store
        if (!db.objectStoreNames.contains('buses')) {
          const busStore = db.createObjectStore('buses', { keyPath: 'id' });
          busStore.createIndex('status', 'status', { unique: false });
          busStore.createIndex('route_id', 'route_id', { unique: false });
        }

        // 2. Routes cache store
        if (!db.objectStoreNames.contains('routes')) {
          const routeStore = db.createObjectStore('routes', { keyPath: 'id' });
          routeStore.createIndex('route_number', 'route_number', { unique: true });
          routeStore.createIndex('category', 'category', { unique: false });
        }

        // 3. Stops cache store
        if (!db.objectStoreNames.contains('stops')) {
          const stopStore = db.createObjectStore('stops', { keyPath: 'id' });
          stopStore.createIndex('code', 'code', { unique: true });
          stopStore.createIndex('name', 'name', { unique: false });
        }

        // 4. Offline Tickets store
        if (!db.objectStoreNames.contains('tickets')) {
          const ticketStore = db.createObjectStore('tickets', { keyPath: 'ticket_number' });
          ticketStore.createIndex('status', 'status', { unique: false });
          ticketStore.createIndex('user_id', 'user_id', { unique: false });
        }

        // 5. Offline Outbox / Mutations Queue
        if (!db.objectStoreNames.contains('offline_queue')) {
          const queueStore = db.createObjectStore('offline_queue', { keyPath: 'id', autoIncrement: true });
          queueStore.createIndex('created_at', 'created_at', { unique: false });
          queueStore.createIndex('endpoint', 'endpoint', { unique: false });
        }

        // 6. User Profile & Settings store
        if (!db.objectStoreNames.contains('user_settings')) {
          db.createObjectStore('user_settings', { keyPath: 'key' });
        }
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        this.isReady = true;
        console.log('[CityBus DB] IndexedDB storage initialized successfully.');
        this.setupOnlineSyncListener();
        resolve(this.db);
      };

      request.onerror = (event) => {
        console.error('[CityBus DB] Failed to open IndexedDB:', event.target.error);
        reject(event.target.error);
      };
    });
  }

  async getStore(storeName, mode = 'readonly') {
    await this.initPromise;
    if (!this.db) return null;
    const tx = this.db.transaction(storeName, mode);
    return tx.objectStore(storeName);
  }

  // --- Entity CRUD operations ---

  async put(storeName, item) {
    try {
      const store = await this.getStore(storeName, 'readwrite');
      if (!store) return null;
      return new Promise((resolve, reject) => {
        const req = store.put(item);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      console.warn(`[CityBus DB] Put failed for ${storeName}:`, e);
      return null;
    }
  }

  async putBulk(storeName, items) {
    try {
      await this.initPromise;
      if (!this.db || !items || items.length === 0) return;
      const tx = this.db.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      items.forEach(item => store.put(item));
      return new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
      });
    } catch (e) {
      console.warn(`[CityBus DB] Bulk put failed for ${storeName}:`, e);
    }
  }

  async get(storeName, key) {
    try {
      const store = await this.getStore(storeName, 'readonly');
      if (!store) return null;
      return new Promise((resolve, reject) => {
        const req = store.get(key);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      console.warn(`[CityBus DB] Get failed for ${storeName}:`, e);
      return null;
    }
  }

  async getAll(storeName) {
    try {
      const store = await this.getStore(storeName, 'readonly');
      if (!store) return [];
      return new Promise((resolve, reject) => {
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      console.warn(`[CityBus DB] GetAll failed for ${storeName}:`, e);
      return [];
    }
  }

  async delete(storeName, key) {
    try {
      const store = await this.getStore(storeName, 'readwrite');
      if (!store) return false;
      return new Promise((resolve, reject) => {
        const req = store.delete(key);
        req.onsuccess = () => resolve(true);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      return false;
    }
  }

  async clear(storeName) {
    try {
      const store = await this.getStore(storeName, 'readwrite');
      if (!store) return false;
      return new Promise((resolve, reject) => {
        const req = store.clear();
        req.onsuccess = () => resolve(true);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      return false;
    }
  }

  // --- Offline Outbox Queue & Sync Management ---

  async enqueueMutation(endpoint, method, payload) {
    const mutation = {
      endpoint,
      method: method.toUpperCase(),
      payload,
      created_at: new Date().toISOString(),
      retries: 0
    };
    const id = await this.put('offline_queue', mutation);
    console.log(`[CityBus Sync] Mutation enqueued offline (ID: ${id}) for ${endpoint}`);
    if (window.showToast) {
      window.showToast('Action saved offline. Will sync when connection is restored.', 'info');
    }
    return id;
  }

  async processSyncQueue() {
    if (!navigator.onLine) return;
    const mutations = await this.getAll('offline_queue');
    if (mutations.length === 0) return;

    console.log(`[CityBus Sync] Processing ${mutations.length} pending offline mutations...`);
    if (window.showToast) {
      window.showToast(`Syncing ${mutations.length} offline actions with transit servers...`, 'info');
    }

    for (const item of mutations) {
      try {
        let res;
        if (item.method === 'POST') {
          res = await window.CityBusAPI.post(item.endpoint, item.payload);
        } else if (item.method === 'PATCH') {
          res = await window.CityBusAPI.patch(item.endpoint, item.payload);
        } else if (item.method === 'DELETE') {
          res = await window.CityBusAPI.delete(item.endpoint);
        }

        if (res && (res.success || res.status === 200 || res.status === 201)) {
          await this.delete('offline_queue', item.id);
          console.log(`[CityBus Sync] Mutation ${item.id} (${item.endpoint}) synced successfully.`);
        }
      } catch (err) {
        console.warn(`[CityBus Sync] Failed to sync mutation ${item.id}:`, err);
        item.retries = (item.retries || 0) + 1;
        if (item.retries > 5) {
          // Discard after 5 failed retries
          await this.delete('offline_queue', item.id);
        } else {
          await this.put('offline_queue', item);
        }
      }
    }

    if (window.showToast) {
      window.showToast('Offline sync completed!', 'success');
    }
  }

  setupOnlineSyncListener() {
    window.addEventListener('online', () => {
      console.log('[CityBus Sync] Network connection restored. Triggering auto-sync...');
      this.processSyncQueue();
    });
  }
}

// Global Singleton Export
window.CityBusDB = new CityBusIndexedDB();
