/**
 * CityBus Enterprise Platform - Theme & Visual Appearance Controller
 * File: js/core/theme.js
 * 
 * Manages Light, Dark, and System theme preferences with automatic
 * DOM class switching, media query synchronization, and LocalStorage persistence.
 */

class CityBusThemeManager {
  constructor() {
    this.storageKey = 'citybus_theme_preference';
    this.currentTheme = localStorage.getItem(this.storageKey) || 'light';
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

    // Attach click listeners to any .theme-toggle-btn in the DOM
    document.addEventListener('DOMContentLoaded', () => {
      this.attachThemeToggleButtons();
    });
  }

  getEffectiveTheme() {
    if (this.currentTheme === 'system') {
      return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
    }
    return this.currentTheme;
  }

  applyTheme(theme) {
    this.currentTheme = theme;
    localStorage.setItem(this.storageKey, theme);

    const effective = this.getEffectiveTheme();
    const root = document.documentElement;

    if (effective === 'dark') {
      root.setAttribute('data-theme', 'dark');
      document.body?.classList.add('dark-theme');
    } else {
      root.removeAttribute('data-theme');
      document.body?.classList.remove('dark-theme');
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

  updateToggleIcons() {
    const isDark = this.getEffectiveTheme() === 'dark';
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.innerHTML = isDark ? '<i class="fa-solid fa-sun" style="color: #FBBF24;"></i>' : '<i class="fa-solid fa-moon"></i>';
      btn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    });
  }

  attachThemeToggleButtons() {
    this.updateToggleIcons();
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.removeEventListener('click', this._boundToggle);
      this._boundToggle = () => this.toggleTheme();
      btn.addEventListener('click', this._boundToggle);
    });
  }
}

// Global Singleton Export
window.CityBusTheme = new CityBusThemeManager();
