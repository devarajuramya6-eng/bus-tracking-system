/**
 * CityBus - Real-Time City Bus Tracking System
 * Core Application Engine & Data Store (js/app.js)
 * 
 * Contains demo datasets, live simulation engine, favorites manager,
 * notification toasts, and mock API abstraction layer.
 */

// ==========================================================================
// 1. Central Demo Dataset (Vijayawada, Andhra Pradesh)
// ==========================================================================

const CITYBUS_DATA = {
  // 15 City Bus Stops
  stops: [
    { id: "STOP-1", name: "Pandit Nehru Bus Station (PNBS)", code: "PNBS", lat: 16.5100, lng: 80.6175, popular: true },
    { id: "STOP-2", name: "Vijayawada Railway Station", code: "VJA-RLY", lat: 16.5186, lng: 80.6200, popular: true },
    { id: "STOP-3", name: "Governorpet Central", code: "GOV-PET", lat: 16.5140, lng: 80.6300, popular: false },
    { id: "STOP-4", name: "Benz Circle Junction", code: "BNZ-CIR", lat: 16.5020, lng: 80.6475, popular: true },
    { id: "STOP-5", name: "DV Manor Center", code: "DVM-CTR", lat: 16.5045, lng: 80.6520, popular: false },
    { id: "STOP-6", name: "Patamata High Road", code: "PAT-MTA", lat: 16.4980, lng: 80.6600, popular: false },
    { id: "STOP-7", name: "Autonagar Bus Terminal", code: "AUTO-NGR", lat: 16.4910, lng: 80.6720, popular: true },
    { id: "STOP-8", name: "Ramavarappadu Ring", code: "RAM-VRU", lat: 16.5260, lng: 80.6710, popular: true },
    { id: "STOP-9", name: "Gunadala Mary Matha Shrine", code: "GND-ALA", lat: 16.5200, lng: 80.6550, popular: false },
    { id: "STOP-10", name: "Gollapudi Center", code: "GOL-PDI", lat: 16.5400, lng: 80.5900, popular: false },
    { id: "STOP-11", name: "Bhavanipuram Swathi Center", code: "BHV-PUR", lat: 16.5250, lng: 80.6000, popular: false },
    { id: "STOP-12", name: "Kanaka Durga Temple Ghat Road", code: "KDK-TMP", lat: 16.5150, lng: 80.6050, popular: true },
    { id: "STOP-13", name: "Mangalagiri AIIMS Bypass", code: "MGL-IMS", lat: 16.4420, lng: 80.5730, popular: true },
    { id: "STOP-14", name: "Guntur NTR Bus Terminal", code: "GNT-TRM", lat: 16.4350, lng: 80.5600, popular: true },
    { id: "STOP-15", name: "Gannavaram International Airport", code: "GAN-AIR", lat: 16.5304, lng: 80.7968, popular: true }
  ],

  // 5 Master Routes with waypoints
  routes: [
    {
      id: "ROUTE-27A",
      number: "27A",
      name: "Vijayawada PNBS → Guntur Bus Terminal",
      origin: "Vijayawada PNBS",
      destination: "Guntur NTR Terminal",
      category: "Express",
      distance: "32.4 km",
      duration: "50 min",
      fare: "₹45",
      stopsCount: 8,
      activeBusesCount: 3,
      color: "#2563EB",
      stops: ["STOP-1", "STOP-3", "STOP-4", "STOP-5", "STOP-6", "STOP-13", "STOP-14"],
      waypoints: [
        [16.5100, 80.6175],
        [16.5140, 80.6300],
        [16.5020, 80.6475],
        [16.5045, 80.6520],
        [16.4980, 80.6600],
        [16.4700, 80.6200],
        [16.4420, 80.5730],
        [16.4350, 80.5600]
      ]
    },
    {
      id: "ROUTE-12B",
      number: "12B",
      name: "Benz Circle → Ramavarappadu Ring",
      origin: "Benz Circle",
      destination: "Ramavarappadu Ring",
      category: "Local",
      distance: "8.6 km",
      duration: "25 min",
      fare: "₹15",
      stopsCount: 6,
      activeBusesCount: 2,
      color: "#16A34A",
      stops: ["STOP-4", "STOP-5", "STOP-9", "STOP-8"],
      waypoints: [
        [16.5020, 80.6475],
        [16.5045, 80.6520],
        [16.5120, 80.6535],
        [16.5200, 80.6550],
        [16.5260, 80.6710]
      ]
    },
    {
      id: "ROUTE-45C",
      number: "45C",
      name: "Autonagar Terminal → Benz Circle",
      origin: "Autonagar",
      destination: "Benz Circle",
      category: "Local",
      distance: "6.2 km",
      duration: "20 min",
      fare: "₹12",
      stopsCount: 5,
      activeBusesCount: 2,
      color: "#F59E0B",
      stops: ["STOP-7", "STOP-6", "STOP-5", "STOP-4"],
      waypoints: [
        [16.4910, 80.6720],
        [16.4945, 80.6660],
        [16.4980, 80.6600],
        [16.5045, 80.6520],
        [16.5020, 80.6475]
      ]
    },
    {
      id: "ROUTE-5A",
      number: "5A",
      name: "PNBS → Gannavaram Airport",
      origin: "Vijayawada PNBS",
      destination: "Gannavaram Airport",
      category: "Express",
      distance: "21.5 km",
      duration: "40 min",
      fare: "₹35",
      stopsCount: 7,
      activeBusesCount: 2,
      color: "#9333EA",
      stops: ["STOP-1", "STOP-2", "STOP-9", "STOP-8", "STOP-15"],
      waypoints: [
        [16.5100, 80.6175],
        [16.5186, 80.6200],
        [16.5200, 80.6550],
        [16.5260, 80.6710],
        [16.5290, 80.7300],
        [16.5304, 80.7968]
      ]
    },
    {
      id: "ROUTE-10H",
      number: "10H",
      name: "Gollapudi → Mangalagiri AIIMS",
      origin: "Gollapudi",
      destination: "Mangalagiri AIIMS",
      category: "Popular",
      distance: "18.2 km",
      duration: "35 min",
      fare: "₹28",
      stopsCount: 6,
      activeBusesCount: 1,
      color: "#0284C7",
      stops: ["STOP-10", "STOP-11", "STOP-12", "STOP-1", "STOP-13"],
      waypoints: [
        [16.5400, 80.5900],
        [16.5250, 80.6000],
        [16.5150, 80.6050],
        [16.5100, 80.6175],
        [16.4800, 80.6000],
        [16.4420, 80.5730]
      ]
    }
  ],

  // 8 Registered Fleet Drivers
  drivers: [
    { id: "DRV-1", name: "Ravi Kumar", phone: "+91 98480 22331", license: "AP-16-2018-884", experience: "8 yrs", rating: 4.9, assignedBus: "BUS-101", status: "Active" },
    { id: "DRV-2", name: "Suresh Reddy", phone: "+91 98481 44552", license: "AP-16-2015-112", experience: "11 yrs", rating: 4.8, assignedBus: "BUS-102", status: "Active" },
    { id: "DRV-3", name: "Venkat Rao", phone: "+91 94401 77883", license: "AP-16-2019-445", experience: "6 yrs", rating: 4.6, assignedBus: "BUS-103", status: "Active" },
    { id: "DRV-4", name: "K. Prasad", phone: "+91 99890 33221", license: "AP-07-2014-991", experience: "12 yrs", rating: 4.9, assignedBus: "BUS-104", status: "Active" },
    { id: "DRV-5", name: "M. Srinivas", phone: "+91 97000 66554", license: "AP-16-2020-332", experience: "5 yrs", rating: 4.7, assignedBus: "BUS-105", status: "Active" },
    { id: "DRV-6", name: "P. Satish", phone: "+91 93930 11223", license: "AP-16-2017-776", experience: "7 yrs", rating: 4.5, assignedBus: "BUS-106", status: "Break" },
    { id: "DRV-7", name: "J. Naidu", phone: "+91 98661 99008", license: "AP-16-2016-554", experience: "9 yrs", rating: 4.8, assignedBus: "BUS-107", status: "Active" },
    { id: "DRV-8", name: "A. Lakshmi Narayana", phone: "+91 94900 88776", license: "AP-07-2013-667", experience: "14 yrs", rating: 4.9, assignedBus: "BUS-108", status: "Active" }
  ],

  // 10 Sample Operating Buses
  buses: [
    {
      id: "BUS-101",
      number: "27A",
      routeId: "ROUTE-27A",
      route: "Vijayawada PNBS → Guntur",
      lat: 16.5062,
      lng: 80.6480,
      speed: 38,
      status: "On Route",
      driver: "Ravi Kumar",
      busType: "City Metro Express (AC)",
      nextStop: "Benz Circle Junction",
      nextStopId: "STOP-4",
      eta: 7,
      occupancy: "65%",
      lastUpdated: "Just now",
      currentWaypointIdx: 2,
      direction: 1 // 1 for forward, -1 for reverse
    },
    {
      id: "BUS-102",
      number: "12B",
      routeId: "ROUTE-12B",
      route: "Benz Circle → Ramavarappadu",
      lat: 16.5075,
      lng: 80.6495,
      speed: 32,
      status: "On Route",
      driver: "Suresh Reddy",
      busType: "Ultra Low Floor (Non-AC)",
      nextStop: "Gunadala Mary Matha",
      nextStopId: "STOP-9",
      eta: 3,
      occupancy: "40%",
      lastUpdated: "Just now",
      currentWaypointIdx: 1,
      direction: 1
    },
    {
      id: "BUS-103",
      number: "45C",
      routeId: "ROUTE-45C",
      route: "Autonagar → Benz Circle",
      lat: 16.5150,
      lng: 80.6400,
      speed: 25,
      status: "Delayed",
      driver: "Venkat Rao",
      busType: "Standard City Bus",
      nextStop: "Patamata High Road",
      nextStopId: "STOP-6",
      eta: 12,
      occupancy: "85%",
      lastUpdated: "1 min ago",
      currentWaypointIdx: 2,
      direction: 1
    },
    {
      id: "BUS-104",
      number: "5A",
      routeId: "ROUTE-5A",
      route: "PNBS → Gannavaram Airport",
      lat: 16.5260,
      lng: 80.6710,
      speed: 48,
      status: "On Route",
      driver: "K. Prasad",
      busType: "Airport Express (Volvo AC)",
      nextStop: "Ramavarappadu Ring",
      nextStopId: "STOP-8",
      eta: 15,
      occupancy: "50%",
      lastUpdated: "Just now",
      currentWaypointIdx: 3,
      direction: 1
    },
    {
      id: "BUS-105",
      number: "22D",
      routeId: "ROUTE-10H",
      route: "Bhavanipuram → Autonagar",
      lat: 16.5180,
      lng: 80.6250,
      speed: 30,
      status: "On Route",
      driver: "M. Srinivas",
      busType: "Standard City Bus",
      nextStop: "Governorpet Central",
      nextStopId: "STOP-3",
      eta: 5,
      occupancy: "70%",
      lastUpdated: "Just now",
      currentWaypointIdx: 2,
      direction: 1
    },
    {
      id: "BUS-106",
      number: "33K",
      routeId: "ROUTE-12B",
      route: "Kanaka Durga Temple → Gunadala",
      lat: 16.5150,
      lng: 80.6050,
      speed: 0,
      status: "Offline",
      driver: "P. Satish",
      busType: "City Mini Bus",
      nextStop: "Temple Gate Terminal",
      nextStopId: "STOP-12",
      eta: null,
      occupancy: "0%",
      lastUpdated: "15 min ago",
      currentWaypointIdx: 0,
      direction: 1
    },
    {
      id: "BUS-107",
      number: "10H",
      routeId: "ROUTE-10H",
      route: "Gollapudi → Mangalagiri AIIMS",
      lat: 16.4800,
      lng: 80.6000,
      speed: 42,
      status: "On Route",
      driver: "J. Naidu",
      busType: "Electric Low Floor",
      nextStop: "Mangalagiri AIIMS",
      nextStopId: "STOP-13",
      eta: 9,
      occupancy: "55%",
      lastUpdated: "Just now",
      currentWaypointIdx: 4,
      direction: 1
    },
    {
      id: "BUS-108",
      number: "18R",
      routeId: "ROUTE-5A",
      route: "Gollapudi → Ramavarappadu",
      lat: 16.5210,
      lng: 80.6400,
      speed: 35,
      status: "On Route",
      driver: "A. Lakshmi Narayana",
      busType: "Standard City Bus",
      nextStop: "Vijayawada Railway Station",
      nextStopId: "STOP-2",
      eta: 8,
      occupancy: "60%",
      lastUpdated: "Just now",
      currentWaypointIdx: 1,
      direction: 1
    },
    {
      id: "BUS-109",
      number: "7M",
      routeId: "ROUTE-45C",
      route: "Benz Circle → Gollapudi",
      lat: 16.5045,
      lng: 80.6520,
      speed: 18,
      status: "Delayed",
      driver: "Venkat Rao",
      busType: "City Ordinary",
      nextStop: "DV Manor Center",
      nextStopId: "STOP-5",
      eta: 14,
      occupancy: "90%",
      lastUpdated: "2 min ago",
      currentWaypointIdx: 3,
      direction: 1
    },
    {
      id: "BUS-110",
      number: "50S",
      routeId: "ROUTE-27A",
      route: "Autonagar → Railway Station",
      lat: 16.4980,
      lng: 80.6600,
      speed: 36,
      status: "On Route",
      driver: "Suresh Reddy",
      busType: "Metro Express",
      nextStop: "Patamata High Road",
      nextStopId: "STOP-6",
      eta: 6,
      occupancy: "45%",
      lastUpdated: "Just now",
      currentWaypointIdx: 4,
      direction: 1
    }
  ]
};

// ==========================================================================
// 2. Real-Time Live Demo Simulator
// ==========================================================================

class LiveDemoSimulator {
  constructor() {
    this.intervalId = null;
    this.intervalMs = 3000; // Update coordinates every 3s
    this.isRunning = false;
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    console.log("⚡ [CityBus Live Demo Simulator] Started real-time GPS broadcast simulation.");
    
    this.intervalId = setInterval(() => {
      this.step();
    }, this.intervalMs);
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.isRunning = false;
  }

  step() {
    CITYBUS_DATA.buses.forEach(bus => {
      if (bus.status === "Offline") return;

      // Small jitter or waypoint interpolation
      const route = CITYBUS_DATA.routes.find(r => r.id === bus.routeId);
      if (route && route.waypoints && route.waypoints.length > 0) {
        // Move towards next waypoint
        const waypoints = route.waypoints;
        let targetIdx = bus.currentWaypointIdx + bus.direction;
        
        if (targetIdx >= waypoints.length) {
          bus.direction = -1;
          targetIdx = waypoints.length - 2;
        } else if (targetIdx < 0) {
          bus.direction = 1;
          targetIdx = 1;
        }

        const currentTarget = waypoints[targetIdx] || waypoints[0];
        const stepRatio = 0.08; // smooth increment
        
        bus.lat += (currentTarget[0] - bus.lat) * stepRatio + (Math.random() - 0.5) * 0.0004;
        bus.lng += (currentTarget[1] - bus.lng) * stepRatio + (Math.random() - 0.5) * 0.0004;

        // Check if reached close to target
        const dist = Math.hypot(bus.lat - currentTarget[0], bus.lng - currentTarget[1]);
        if (dist < 0.003) {
          bus.currentWaypointIdx = targetIdx;
        }
      } else {
        // Simple realistic wandering jitter
        bus.lat += (Math.random() - 0.48) * 0.0006;
        bus.lng += (Math.random() - 0.48) * 0.0006;
      }

      // Slightly fluctuate speed and ETA
      if (bus.status === "On Route") {
        bus.speed = Math.max(15, Math.min(55, Math.round(bus.speed + (Math.random() * 6 - 3))));
        if (Math.random() > 0.7 && bus.eta > 1) {
          bus.eta = Math.max(1, bus.eta - 1);
        }
      } else if (bus.status === "Delayed") {
        bus.speed = Math.max(5, Math.min(28, Math.round(bus.speed + (Math.random() * 4 - 2))));
      }

      bus.lastUpdated = "Just now";
    });

    // Broadcast update event to all active UI & Map listeners
    window.dispatchEvent(new CustomEvent('citybus:data-updated', {
      detail: { buses: CITYBUS_DATA.buses }
    }));
  }
}

// Instantiate and start simulator automatically
const simulator = new LiveDemoSimulator();
simulator.start();


// ==========================================================================
// 3. Mock API Layer (Ready for Flask/Python Backend)
// ==========================================================================

const CityBusAPI = {
  // GET /api/buses
  async getBuses(filter = {}) {
    // TODO: Replace demo data with Flask API: return fetch('/api/buses').then(res => res.json());
    return new Promise(resolve => {
      let result = [...CITYBUS_DATA.buses];
      if (filter.status && filter.status !== 'All') {
        result = result.filter(b => b.status.toLowerCase() === filter.status.toLowerCase());
      }
      if (filter.search) {
        const q = filter.search.toLowerCase();
        result = result.filter(b => 
          b.number.toLowerCase().includes(q) ||
          b.route.toLowerCase().includes(q) ||
          b.nextStop.toLowerCase().includes(q)
        );
      }
      resolve(result);
    });
  },

  // GET /api/buses/:id
  async getBusById(id) {
    // TODO: Replace demo data with Flask API: return fetch(`/api/buses/${id}`).then(res => res.json());
    return new Promise((resolve, reject) => {
      const bus = CITYBUS_DATA.buses.find(b => b.id === id || b.number.toUpperCase() === id.toUpperCase());
      if (bus) resolve(bus);
      else resolve(CITYBUS_DATA.buses[0]); // default fallback
    });
  },

  // GET /api/routes
  async getRoutes(filter = {}) {
    // TODO: Replace demo data with Flask API: return fetch('/api/routes').then(res => res.json());
    return new Promise(resolve => {
      let result = [...CITYBUS_DATA.routes];
      if (filter.category && filter.category !== 'All Routes') {
        result = result.filter(r => r.category.toLowerCase() === filter.category.toLowerCase());
      }
      if (filter.search) {
        const q = filter.search.toLowerCase();
        result = result.filter(r => 
          r.number.toLowerCase().includes(q) ||
          r.name.toLowerCase().includes(q) ||
          r.origin.toLowerCase().includes(q) ||
          r.destination.toLowerCase().includes(q)
        );
      }
      resolve(result);
    });
  },

  // GET /api/stops
  async getStops() {
    // TODO: Replace demo data with Flask API: return fetch('/api/stops').then(res => res.json());
    return new Promise(resolve => resolve(CITYBUS_DATA.stops));
  },

  // GET /api/drivers
  async getDrivers() {
    // TODO: Replace demo data with Flask API: return fetch('/api/drivers').then(res => res.json());
    return new Promise(resolve => resolve(CITYBUS_DATA.drivers));
  },

  // GET /api/buses/nearby
  async getNearbyBuses(userLat, userLng, maxDistKm = 10) {
    // TODO: Replace demo data with Flask API: return fetch(`/api/buses/nearby?lat=${userLat}&lng=${userLng}`).then(res => res.json());
    return new Promise(resolve => {
      const busesWithDist = CITYBUS_DATA.buses
        .filter(b => b.status !== "Offline")
        .map(bus => {
          const dist = calculateDistanceKm(userLat, userLng, bus.lat, bus.lng);
          return { ...bus, distanceKm: dist };
        })
        .filter(b => b.distanceKm <= maxDistKm)
        .sort((a, b) => a.distanceKm - b.distanceKm);
      resolve(busesWithDist);
    });
  },

  // GET /api/stops/nearby
  async getNearbyStops(userLat, userLng, maxDistKm = 10) {
    return new Promise(resolve => {
      const stopsWithDist = CITYBUS_DATA.stops
        .map(stop => {
          const dist = calculateDistanceKm(userLat, userLng, stop.lat, stop.lng);
          return { ...stop, distanceKm: dist };
        })
        .filter(s => s.distanceKm <= maxDistKm)
        .sort((a, b) => a.distanceKm - b.distanceKm);
      resolve(stopsWithDist);
    });
  },

  // POST /api/buses/location
  async updateBusLocation(busId, lat, lng, speed = 35) {
    // TODO: Replace demo data with Flask API: return fetch('/api/buses/location', { method: 'POST', body: JSON.stringify({ busId, lat, lng, speed }) });
    return new Promise(resolve => {
      const bus = CITYBUS_DATA.buses.find(b => b.id === busId);
      if (bus) {
        bus.lat = lat;
        bus.lng = lng;
        bus.speed = speed;
        bus.lastUpdated = "Just now";
      }
      resolve({ success: true, bus });
    });
  },

  // POST /api/trips/start
  async startTrip(driverId, busId) {
    // TODO: Replace demo data with Flask API: return fetch('/api/trips/start', { method: 'POST', body: JSON.stringify({ driverId, busId }) });
    return new Promise(resolve => {
      const bus = CITYBUS_DATA.buses.find(b => b.id === busId);
      if (bus) {
        bus.status = "On Route";
      }
      resolve({ success: true, message: "Trip started successfully" });
    });
  },

  // POST /api/trips/stop
  async stopTrip(driverId, busId) {
    // TODO: Replace demo data with Flask API: return fetch('/api/trips/stop', { method: 'POST', body: JSON.stringify({ driverId, busId }) });
    return new Promise(resolve => {
      const bus = CITYBUS_DATA.buses.find(b => b.id === busId);
      if (bus) {
        bus.status = "Offline";
        bus.speed = 0;
      }
      resolve({ success: true, message: "Trip ended" });
    });
  }
};


// ==========================================================================
// 4. Utility Functions (Haversine Formula, LocalStorage, Toasts)
// ==========================================================================

// Calculate distance between two coordinates in kilometers
function calculateDistanceKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return parseFloat((R * c).toFixed(1));
}

// Format distance string (e.g. "800 m away" or "2.4 km away")
function formatDistance(distKm) {
  if (distKm < 1) {
    return `${Math.round(distKm * 1000)} m away`;
  }
  return `${distKm} km away`;
}

// Favorites Management via LocalStorage
const FavoritesStore = {
  KEY: 'citybus_favorites',
  getFavorites() {
    try {
      const data = localStorage.getItem(this.KEY);
      return data ? JSON.parse(data) : ['BUS-101', 'BUS-102'];
    } catch {
      return ['BUS-101', 'BUS-102'];
    }
  },
  isFavorite(busId) {
    return this.getFavorites().includes(busId);
  },
  toggleFavorite(busId) {
    let favs = this.getFavorites();
    let isAdded = false;
    if (favs.includes(busId)) {
      favs = favs.filter(id => id !== busId);
      isAdded = false;
    } else {
      favs.push(busId);
      isAdded = true;
    }
    localStorage.setItem(this.KEY, JSON.stringify(favs));
    showToast(isAdded ? `Added ${busId} to favorites` : `Removed ${busId} from favorites`, 'info');
    return isAdded;
  }
};

// Toast Notifications
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast-msg toast-${type}`;
  
  let iconClass = 'fa-info-circle';
  if (type === 'success') iconClass = 'fa-check-circle';
  if (type === 'warning') iconClass = 'fa-exclamation-triangle';
  if (type === 'danger') iconClass = 'fa-times-circle';

  toast.innerHTML = `
    <i class="fa-solid ${iconClass}"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}


// ==========================================================================
// 5. Global Navigation & Mobile Menu Setup
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Mobile hamburger menu toggle
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const isOpen = navLinks.classList.contains('open');
      menuBtn.innerHTML = isOpen ? '<i class="fa-solid fa-xmark"></i>' : '<i class="fa-solid fa-bars"></i>';
    });

    // Close menu when clicking outside or on a link
    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !menuBtn.contains(e.target) && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
      }
    });
  }

  // Highlight active link
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
});
// Final Polish
