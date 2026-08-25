/**
 * CityBus Enterprise Design System - Toast Notification Component
 * File: js/components/toast.js
 */

class CityBusToastController {
  constructor() {
    this.containerId = 'cb-toast-container';
    this.queue = [];
  }

  getContainer() {
    let container = document.getElementById(this.containerId);
    if (!container) {
      container = document.createElement('div');
      container.id = this.containerId;
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  show(message, type = 'info', durationMs = 4000, action = null) {
    const container = this.getContainer();

    const toast = document.createElement('div');
    toast.className = `toast-msg toast-${type}`;
    
    let iconClass = 'fa-circle-info';
    if (type === 'success') iconClass = 'fa-circle-check';
    if (type === 'warning') iconClass = 'fa-triangle-exclamation';
    if (type === 'danger') iconClass = 'fa-circle-xmark';

    let actionBtnHtml = '';
    if (action && action.label) {
      actionBtnHtml = `<button class="btn btn-xs btn-outline" style="margin-left: auto;" id="toast-act-${Date.now()}">${action.label}</button>`;
    }

    toast.innerHTML = `
      <i class="fa-solid ${iconClass}" style="font-size: 1.15rem; color: var(--cb-status-${type === 'info' ? 'primary' : type}); flex-shrink: 0;"></i>
      <div style="flex: 1; font-size: 0.875rem; line-height: 1.4;">${message}</div>
      ${actionBtnHtml}
      <button class="modal-close-btn" style="width: 24px; height: 24px; font-size: 0.75rem; flex-shrink: 0;" aria-label="Close">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;

    container.appendChild(toast);

    // Close button click
    const closeBtn = toast.querySelector('.modal-close-btn');
    closeBtn.addEventListener('click', () => this.dismiss(toast));

    // Action button callback
    if (action && action.onClick) {
      const actBtn = toast.querySelector(`[id^="toast-act-"]`);
      if (actBtn) {
        actBtn.addEventListener('click', () => {
          action.onClick();
          this.dismiss(toast);
        });
      }
    }

    // Auto dismiss timer
    if (durationMs > 0) {
      setTimeout(() => this.dismiss(toast), durationMs);
    }

    return toast;
  }

  dismiss(toast) {
    if (!toast || !toast.parentNode) return;
    toast.style.transition = 'all 0.25s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(50px)';
    setTimeout(() => {
      if (toast.parentNode) toast.remove();
    }, 250);
  }
}

// Global Export
window.CityBusToast = new CityBusToastController();
window.showToast = (msg, type = 'info', duration = 4000) => window.CityBusToast.show(msg, type, duration);
