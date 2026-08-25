/**
 * CityBus Enterprise Platform - Progressive Web App (PWA) Manager
 * File: js/core/pwa.js
 * 
 * Handles Service Worker registration, install prompts, offline caching,
 * network recovery, and background sync triggers.
 */

class CityBusPWAManager {
  constructor() {
    this.deferredPrompt = null;
    this.init();
  }

  init() {
    // 1. Register Service Worker if supported
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
          .then(reg => {
            console.log('📱 [CityBus PWA] ServiceWorker registration successful with scope:', reg.scope);
          })
          .catch(err => {
            console.warn('⚠️ [CityBus PWA] ServiceWorker registration failed:', err);
          });
      });
    }

    // 2. Capture install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallBanner();
    });

    // 3. Track successful app install
    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      console.log('🎉 [CityBus PWA] CityBus installed on device.');
      if (window.showToast) window.showToast('CityBus successfully installed on your device!', 'success');
      this.hideInstallBanner();
    });
  }

  showInstallBanner() {
    let banner = document.getElementById('pwa-install-banner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'pwa-install-banner';
      banner.style.cssText = `
        position: fixed;
        bottom: 1.5rem;
        left: 1.5rem;
        background: var(--cb-bg-surface);
        border: 1px solid var(--cb-border-default);
        border-radius: var(--cb-radius-xl);
        padding: 1rem 1.25rem;
        box-shadow: var(--cb-shadow-2xl);
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 1rem;
        max-width: 380px;
        animation: cbSlideInRight 0.3s ease;
      `;

      banner.innerHTML = `
        <div class="logo-icon" style="width: 42px; height: 42px; font-size: 1.2rem; flex-shrink: 0;">
          <i class="fa-solid fa-bus"></i>
        </div>
        <div style="flex: 1;">
          <div style="font-weight: 700; font-size: 0.9rem; color: var(--cb-text-primary);">Install CityBus App</div>
          <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Faster access, offline tickets & real-time alerts.</div>
        </div>
        <button id="pwa-install-btn" class="btn btn-primary btn-sm">Install</button>
        <button id="pwa-dismiss-btn" class="modal-close-btn" style="width: 24px; height: 24px; font-size: 0.8rem;"><i class="fa-solid fa-xmark"></i></button>
      `;

      document.body.appendChild(banner);

      document.getElementById('pwa-install-btn')?.addEventListener('click', () => this.promptInstall());
      document.getElementById('pwa-dismiss-btn')?.addEventListener('click', () => this.hideInstallBanner());
    }
  }

  hideInstallBanner() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) banner.remove();
  }

  async promptInstall() {
    if (!this.deferredPrompt) return;
    this.deferredPrompt.prompt();
    const { outcome } = await this.deferredPrompt.userChoice;
    console.log(`[CityBus PWA] User install choice: ${outcome}`);
    this.deferredPrompt = null;
    this.hideInstallBanner();
  }
}

// Global Singleton Export
window.CityBusPWA = new CityBusPWAManager();
