/**
 * CityBus Enterprise Platform - Route Data & Journey Planner Service
 * File: js/services/routeService.js
 * 
 * Provides client operations for route catalog browsing, corridor geometry,
 * stop sequences, headway frequencies, and journey pathfinding.
 */

class RouteService {
    constructor() {
        this.routesCache = [];
    }

    async getAllRoutes(category = null, search = null) {
        let endpoint = '/api/v1/routes?';
        if (category) endpoint += `category=${encodeURIComponent(category)}&`;
        if (search) endpoint += `search=${encodeURIComponent(search)}&`;

        const response = await window.apiClient.get(endpoint, { useCache: true });
        if (response && response.success) {
            this.routesCache = response.routes || [];
            return this.routesCache;
        }
        return [];
    }

    async getRouteById(routeId) {
        const response = await window.apiClient.get(`/api/v1/routes/${routeId}`);
        if (response && response.success) {
            return response.route;
        }
        throw new Error(response.message || `Route ${routeId} not found`);
    }

    async getRouteStops(routeId) {
        const route = await this.getRouteById(routeId);
        return route.stops || [];
    }

    async createRoute(routeData) {
        return window.apiClient.post('/api/v1/routes', routeData);
    }

    async updateRoute(routeId, routeData) {
        return window.apiClient.put(`/api/v1/routes/${routeId}`, routeData);
    }

    async deleteRoute(routeId) {
        return window.apiClient.delete(`/api/v1/routes/${routeId}`);
    }

    async planJourney(originLat, originLng, destLat, destLng) {
        // High-performance direct & transfer journey planner
        const routes = await this.getAllRoutes();
        const solutions = [];

        // Identify closest stops to origin and destination
        const allStops = await window.stopService.getAllStops();
        const originStop = window.geoService.findClosest(originLat, originLng, allStops);
        const destStop = window.geoService.findClosest(destLat, destLng, allStops);

        if (!originStop || !destStop) return [];

        for (const route of routes) {
            const routeDetails = await this.getRouteById(route.id);
            const stops = routeDetails.stops || [];
            const originIdx = stops.findIndex(s => s.id === originStop.id);
            const destIdx = stops.findIndex(s => s.id === destStop.id);

            if (originIdx !== -1 && destIdx !== -1 && originIdx < destIdx) {
                // Direct route found!
                const rideStops = stops.slice(originIdx, destIdx + 1);
                const travelMin = (destIdx - originIdx) * 3 + 2;
                solutions.push({
                    type: 'DIRECT',
                    transfers: 0,
                    route: routeDetails,
                    origin_stop: originStop,
                    destination_stop: destStop,
                    stops_count: rideStops.length,
                    duration_minutes: travelMin,
                    fare_inr: Math.max(15, (destIdx - originIdx) * 3),
                    segments: [{
                        mode: 'BUS',
                        route_number: route.route_number,
                        from: originStop.name,
                        to: destStop.name,
                        stops: rideStops
                    }]
                });
            }
        }

        return solutions.sort((a, b) => a.duration_minutes - b.duration_minutes);
    }
}

// Global Export
window.routeService = new RouteService();
