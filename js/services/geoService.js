/**
 * CityBus Enterprise Platform - Geospatial Math & Proximity Service
 * File: js/services/geoService.js
 * 
 * Provides Haversine distance calculations, coordinate bearing/heading interpolation,
 * bounding box checks, and nearest-entity pathfinding.
 */

class GeoService {
    static EARTH_RADIUS_KM = 6371.0;
    static EARTH_RADIUS_METERS = 6371000.0;

    static toRadians(degrees) {
        return degrees * (Math.PI / 180.0);
    }

    static toDegrees(radians) {
        return radians * (180.0 / Math.PI);
    }

    static distanceKm(lat1, lng1, lat2, lng2) {
        const dLat = this.toRadians(lat2 - lat1);
        const dLng = this.toRadians(lng2 - lng1);
        const a = Math.sin(dLat / 2.0) ** 2 +
                  Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
                  Math.sin(dLng / 2.0) ** 2;
        const c = 2.0 * Math.atan2(Math.sqrt(a), Math.sqrt(1.0 - a));
        return this.EARTH_RADIUS_KM * c;
    }

    static distanceMeters(lat1, lng1, lat2, lng2) {
        return this.distanceKm(lat1, lng1, lat2, lng2) * 1000.0;
    }

    static calculateBearing(lat1, lng1, lat2, lng2) {
        const φ1 = this.toRadians(lat1);
        const φ2 = this.toRadians(lat2);
        const Δλ = this.toRadians(lng2 - lng1);

        const y = Math.sin(Δλ) * Math.cos(φ2);
        const x = Math.cos(φ1) * Math.sin(φ2) -
                  Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
        const θ = Math.atan2(y, x);
        return (this.toDegrees(θ) + 360.0) % 360.0;
    }

    static interpolate(lat1, lng1, lat2, lng2, fraction) {
        const lat = lat1 + (lat2 - lat1) * fraction;
        const lng = lng1 + (lng2 - lng1) * fraction;
        return [lat, lng];
    }

    static findClosest(lat, lng, items = [], latKey = 'latitude', lngKey = 'longitude') {
        if (!items || items.length === 0) return null;
        let closest = null;
        let minDistance = Infinity;

        for (const item of items) {
            const itemLat = item[latKey];
            const itemLng = item[lngKey];
            if (itemLat !== undefined && itemLng !== undefined) {
                const dist = this.distanceKm(lat, lng, itemLat, itemLng);
                if (dist < minDistance) {
                    minDistance = dist;
                    closest = item;
                }
            }
        }
        return closest;
    }

    static isInsideBounds(lat, lng, minLat = 15.5, maxLat = 17.5, minLng = 79.5, maxLng = 81.5) {
        return lat >= minLat && lat <= maxLat && lng >= minLng && lng <= maxLng;
    }
}

// Global Export
window.geoService = GeoService;
