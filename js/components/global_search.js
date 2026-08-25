/**
 * CityBus Enterprise Design System - Global OmniSearch Engine
 * File: js/components/global_search.js
 * 
 * Provides unified searching across buses, routes, stops, drivers,
 * conductors, tickets, users, and maintenance incidents.
 */

class CityBusGlobalSearch {
  constructor() {
    this.recentSearchesKey = 'citybus_recent_searches';
    this.maxRecent = 5;
  }

  getRecentSearches() {
    try {
      const data = localStorage.getItem(this.recentSearchesKey);
      return data ? JSON.parse(data) : ['Bus 27A', 'Benz Circle', 'Guntur Express'];
    } catch {
      return ['Bus 27A', 'Benz Circle'];
    }
  }

  addRecentSearch(query) {
    if (!query || query.trim().length === 0) return;
    let list = this.getRecentSearches().filter(q => q.toLowerCase() !== query.toLowerCase());
    list.unshift(query.trim());
    if (list.length > this.maxRecent) list = list.slice(0, this.maxRecent);
    localStorage.setItem(this.recentSearchesKey, JSON.stringify(list));
  }

  /**
   * Searches all entity domains in the CityBus data store
   */
  search(query, dataset) {
    const q = (query || '').trim().toLowerCase();
    if (!q) return { total: 0, results: [] };

    const results = [];
    const buses = dataset.buses || (window.CITYBUS_DATA ? window.CITYBUS_DATA.buses : []);
    const routes = dataset.routes || (window.CITYBUS_DATA ? window.CITYBUS_DATA.routes : []);
    const stops = dataset.stops || (window.CITYBUS_DATA ? window.CITYBUS_DATA.stops : []);
    const drivers = dataset.drivers || (window.CITYBUS_DATA ? window.CITYBUS_DATA.drivers : []);

    // Search Buses
    buses.forEach(b => {
      if (b.number.toLowerCase().includes(q) || b.route.toLowerCase().includes(q) || b.id.toLowerCase().includes(q)) {
        results.push({
          type: 'bus',
          title: `Bus ${b.number} (${b.id})`,
          subtitle: `${b.route} • ${b.status}`,
          icon: 'fa-bus',
          url: `bus-details.html?id=${b.id}`
        });
      }
    });

    // Search Routes
    routes.forEach(r => {
      if (r.number.toLowerCase().includes(q) || r.name.toLowerCase().includes(q) || r.origin.toLowerCase().includes(q) || r.destination.toLowerCase().includes(q)) {
        results.push({
          type: 'route',
          title: `Route ${r.number}: ${r.name}`,
          subtitle: `${r.distance} • ~${r.duration} • Fare: ${r.fare}`,
          icon: 'fa-route',
          url: `routes.html?q=${r.number}`
        });
      }
    });

    // Search Stops
    stops.forEach(s => {
      if (s.name.toLowerCase().includes(q) || s.code.toLowerCase().includes(q)) {
        results.push({
          type: 'stop',
          title: `📍 ${s.name}`,
          subtitle: `Stop Code: ${s.code}`,
          icon: 'fa-location-dot',
          url: `stops.html?q=${s.code}`
        });
      }
    });

    // Search Drivers
    drivers.forEach(d => {
      if (d.name.toLowerCase().includes(q) || d.phone.toLowerCase().includes(q) || (d.license && d.license.toLowerCase().includes(q))) {
        results.push({
          type: 'driver',
          title: `Driver: ${d.name}`,
          subtitle: `Assigned: Bus ${d.assignedBus} • Rating: ${d.rating || 4.8}★`,
          icon: 'fa-user-tie',
          url: `admin.html#drivers`
        });
      }
    });

    return {
      query: q,
      total: results.length,
      results: results
    };
  }
}

// Global Export
window.CityBusSearch = new CityBusGlobalSearch();
