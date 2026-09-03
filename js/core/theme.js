/**
 * CityBus Enterprise Platform - Theme & Visual Appearance Controller
 * File: js/core/theme.js
 * 
 * Manages Light, Dark, and System theme preferences with automatic
 * DOM class switching, media query synchronization, and LocalStorage persistence.
 */

class CityBusThemeManager {
  constructor() {
    this.storageKey = 'theme';
    this.fallbackStorageKey = 'citybus_theme_preference';
    this.currentTheme = localStorage.getItem(this.storageKey) || localStorage.getItem(this.fallbackStorageKey) || 'light';
    this._boundToggle = () => this.toggleTheme();
    this.init();
  }

  init() {
    this.applyTheme(this.currentTheme);

    // Watch OS system preference changes if user chose 'system'
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (this.currentTheme === 'system') {
          this.applyTheme('system');
        }
      });
    }

    // Attach click listeners to all theme toggle buttons in the DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.attachThemeToggleButtons());
    } else {
      this.attachThemeToggleButtons();
    }
  }

  getEffectiveTheme() {
    if (this.currentTheme === 'system') {
      return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
    }
    return this.currentTheme;
  }

  applyTheme(theme) {
    this.currentTheme = theme;
    try {
      localStorage.setItem(this.storageKey, theme);
      localStorage.setItem(this.fallbackStorageKey, theme);
    } catch {}

    const effective = this.getEffectiveTheme();
    const root = document.documentElement;

    if (effective === 'dark') {
      root.setAttribute('data-theme', 'dark');
      if (document.body) document.body.classList.add('dark-theme');
    } else {
      root.setAttribute('data-theme', 'light');
      if (document.body) document.body.classList.remove('dark-theme');
    }

    this.updateToggleIcons();

    // Dispatch global theme change event
    window.dispatchEvent(new CustomEvent('citybus:theme-changed', { detail: { theme: this.currentTheme, effective } }));
  }

  toggleTheme() {
    const nextTheme = this.getEffectiveTheme() === 'dark' ? 'light' : 'dark';
    this.applyTheme(nextTheme);
    if (window.showToast) {
      window.showToast(`Switched to ${nextTheme === 'dark' ? 'Dark' : 'Light'} Mode`, 'info');
    }
    return nextTheme;
  }

  getToggleButtons() {
    return document.querySelectorAll('.theme-toggle, .theme-toggle-btn, #theme-toggle-btn, [data-action="toggle-theme"]');
  }

  updateToggleIcons() {
    const isDark = this.getEffectiveTheme() === 'dark';
    this.getToggleButtons().forEach(btn => {
      btn.innerHTML = isDark ? '<i class="fa-solid fa-sun" style="color: #FBBF24;"></i>' : '<i class="fa-solid fa-moon"></i>';
      btn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    });
  }

  attachThemeToggleButtons() {
    this.updateToggleIcons();
    this.getToggleButtons().forEach(btn => {
      btn.removeEventListener('click', this._boundToggle);
      btn.addEventListener('click', this._boundToggle);
    });
  }
}

// Global Singleton Export
window.CityBusTheme = new CityBusThemeManager();
