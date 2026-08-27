/**
 * CityBus Enterprise Platform - Dark / Light Theme Mode Switcher
 * File: js/components/themeSwitcher.js
 * 
 * Manages theme persistence, OS color-scheme auto detection, and dynamic CSS token switching.
 */

class ThemeSwitcher {
    constructor() {
        this.storageKey = 'citybus_theme_preference';
        this.currentTheme = this.getStoredTheme() || this.getSystemPreference();
        this.applyTheme(this.currentTheme);
    }

    getStoredTheme() {
        return localStorage.getItem(this.storageKey);
    }

    getSystemPreference() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    applyTheme(theme) {
        this.currentTheme = theme;
        document.body.dataset.theme = theme;
        localStorage.setItem(this.storageKey, theme);

        const icon = document.getElementById('theme-toggle-icon');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    toggle() {
        const next = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(next);
        window.toastManager?.info(`Switched to ${next} theme mode.`);
    }

    bindToggleButtons() {
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.onclick = () => this.toggle();
        });
    }
}

// Global Export
window.themeSwitcher = new ThemeSwitcher();

document.addEventListener('DOMContentLoaded', () => {
    window.themeSwitcher.bindToggleButtons();
});
