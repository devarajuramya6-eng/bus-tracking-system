/**
 * CityBus Enterprise Platform - Favorite Routes & Bus Tracker Bookmarks
 * File: js/passenger/favoriteRoutesManager.js
 * 
 * Manages user bookmarks for frequent corridors, daily commute shortcuts,
 * and quick-launch ETA widgets.
 */

class FavoriteRoutesManager {
    constructor() {
        this.storageKey = 'citybus_favorites';
        this.favorites = this.loadFavorites();
    }

    loadFavorites() {
        try {
            const raw = localStorage.getItem(this.storageKey);
            return raw ? JSON.parse(raw) : { routes: [], stops: [], buses: [] };
        } catch (e) {
            return { routes: [], stops: [], buses: [] };
        }
    }

    save() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.favorites));
        window.dispatchEvent(new CustomEvent('favoritesUpdated', { detail: this.favorites }));
    }

    isRouteFavorite(routeId) {
        return this.favorites.routes.some(r => r.id === routeId);
    }

    toggleRouteFavorite(route) {
        if (this.isRouteFavorite(route.id)) {
            this.favorites.routes = this.favorites.routes.filter(r => r.id !== route.id);
            window.toastManager?.info(`Route ${route.route_number} removed from favorites.`);
        } else {
            this.favorites.routes.push({
                id: route.id,
                route_number: route.route_number,
                name: route.name,
                start_point: route.start_point,
                destination: route.destination,
                color_hex: route.color_hex || '#2563EB'
            });
            window.toastManager?.success(`Route ${route.route_number} added to favorites!`);
        }
        this.save();
    }

    isStopFavorite(stopId) {
        return this.favorites.stops.some(s => s.id === stopId);
    }

    toggleStopFavorite(stop) {
        if (this.isStopFavorite(stop.id)) {
            this.favorites.stops = this.favorites.stops.filter(s => s.id !== stop.id);
            window.toastManager?.info(`Stop ${stop.name} removed from favorites.`);
        } else {
            this.favorites.stops.push({
                id: stop.id,
                name: stop.name,
                stop_code: stop.stop_code,
                latitude: stop.latitude,
                longitude: stop.longitude
            });
            window.toastManager?.success(`Stop ${stop.name} added to favorites!`);
        }
        this.save();
    }

    renderFavoritesWidget(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (this.favorites.routes.length === 0 && this.favorites.stops.length === 0) {
            container.innerHTML = '<div class="text-muted p-3 text-center">No bookmarked routes or stops yet. Click the star icon to bookmark!</div>';
            return;
        }

        container.innerHTML = `
            <div class="favorites-list">
                ${this.favorites.routes.map(r => `
                    <a href="/routes.html?id=${r.id}" class="favorite-pill-item">
                        <span class="badge" style="background:${r.color_hex || '#2563EB'}; color:#fff;">${r.route_number}</span>
                        <span class="route-title">${r.start_point} ⇄ ${r.destination}</span>
                    </a>
                `).join('')}
                ${this.favorites.stops.map(s => `
                    <a href="/stops.html?id=${s.id}" class="favorite-pill-item stop-pill">
                        <i class="fas fa-map-marker-alt text-danger"></i>
                        <span class="stop-title">${s.name} (${s.stop_code})</span>
                    </a>
                `).join('')}
            </div>
        `;
    }
}

// Global Export
window.favoriteRoutesManager = new FavoriteRoutesManager();
