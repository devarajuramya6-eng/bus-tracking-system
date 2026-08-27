/**
 * CityBus Enterprise Platform - Toast Notification Manager
 * File: js/components/toastManager.js
 * 
 * Renders non-blocking floating notifications with smooth animations,
 * severity icons, progress bars, and auto-dismissal.
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        let el = document.getElementById('citybus-toast-container');
        if (!el) {
            el = document.createElement('div');
            el.id = 'citybus-toast-container';
            el.className = 'citybus-toast-container';
            document.body.appendChild(el);
        }
        this.container = el;
    }

    show(message, type = 'info', durationMs = 4000) {
        if (!this.container) this.init();

        const toast = document.createElement('div');
        toast.className = `citybus-toast toast-${type}`;

        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        const iconClass = icons[type] || icons.info;

        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${iconClass} toast-icon"></i>
                <div class="toast-message">${message}</div>
                <button class="toast-close" aria-label="Close">&times;</button>
            </div>
            <div class="toast-progress-bar" style="animation-duration: ${durationMs}ms;"></div>
        `;

        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.onclick = () => this.dismiss(toast);

        this.container.appendChild(toast);

        // Trigger entrance animation
        requestAnimationFrame(() => {
            toast.classList.add('toast-visible');
        });

        // Auto dismiss timer
        const timer = setTimeout(() => {
            this.dismiss(toast);
        }, durationMs);

        toast.dataset.timer = timer;
        return toast;
    }

    dismiss(toast) {
        if (!toast || !toast.parentNode) return;
        clearTimeout(Number(toast.dataset.timer));
        toast.classList.remove('toast-visible');
        toast.classList.add('toast-hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    success(msg, duration = 4000) { return this.show(msg, 'success', duration); }
    error(msg, duration = 5000) { return this.show(msg, 'error', duration); }
    warning(msg, duration = 4500) { return this.show(msg, 'warning', duration); }
    info(msg, duration = 4000) { return this.show(msg, 'info', duration); }
}

// Global Export
window.toastManager = new ToastManager();
