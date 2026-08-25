/**
 * CityBus Enterprise Design System - Modal, Drawer & Confirmation Dialog Controller
 * File: js/components/modal.js
 */

class CityBusModalController {
  constructor() {
    this.activeModals = [];
    this.initKeyboardListeners();
  }

  initKeyboardListeners() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.activeModals.length > 0) {
        const topModal = this.activeModals[this.activeModals.length - 1];
        this.close(topModal);
      }
    });
  }

  open(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    this.activeModals.push(modal);

    // Focus first input or close button
    setTimeout(() => {
      const focusable = modal.querySelector('input, select, textarea, button:not(.modal-close-btn)');
      if (focusable) focusable.focus();
    }, 100);

    // Close on backdrop click
    const backdropCloseHandler = (e) => {
      if (e.target === modal) {
        this.close(modal);
        modal.removeEventListener('click', backdropCloseHandler);
      }
    };
    modal.addEventListener('click', backdropCloseHandler);

    // Close on .modal-close-btn
    modal.querySelectorAll('.modal-close-btn, [data-dismiss="modal"]').forEach(btn => {
      btn.onclick = () => this.close(modal);
    });

    window.dispatchEvent(new CustomEvent('citybus:modal-opened', { detail: { modalId } }));
  }

  close(modalOrId) {
    const modal = typeof modalOrId === 'string' ? document.getElementById(modalOrId) : modalOrId;
    if (!modal) return;

    modal.classList.remove('show');
    this.activeModals = this.activeModals.filter(m => m !== modal);

    if (this.activeModals.length === 0) {
      document.body.style.overflow = '';
    }

    window.dispatchEvent(new CustomEvent('citybus:modal-closed', { detail: { modalId: modal.id } }));
  }

  /**
   * Spawns a dynamic modal dialog with custom HTML content
   */
  dynamicModal({ title, bodyHtml, footerHtml = '', size = 'md', onOpen = null }) {
    const modalId = `dyn-modal-${Date.now()}`;
    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal-backdrop';

    let sizeClass = '';
    if (size === 'lg') sizeClass = 'modal-lg';
    if (size === 'xl') sizeClass = 'modal-xl';

    modal.innerHTML = `
      <div class="modal-dialog ${sizeClass}">
        <div class="modal-header">
          <h3 class="modal-title">${title}</h3>
          <button class="modal-close-btn" data-dismiss="modal"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="modal-body">${bodyHtml}</div>
        ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
      </div>
    `;

    document.body.appendChild(modal);
    this.open(modalId);

    if (onOpen) onOpen(modal);

    // Auto cleanup from DOM after closing
    modal.addEventListener('transitionend', () => {
      if (!modal.classList.contains('show')) {
        modal.remove();
      }
    });

    return modal;
  }

  /**
   * Spawns a standardized confirmation dialog
   */
  confirm({ title = 'Confirm Action', message = 'Are you sure you want to proceed?', confirmText = 'Confirm', confirmType = 'primary', onConfirm }) {
    return new Promise((resolve) => {
      let btnClass = 'btn-primary';
      if (confirmType === 'danger') btnClass = 'btn-danger';
      if (confirmType === 'success') btnClass = 'btn-success';

      this.dynamicModal({
        title,
        bodyHtml: `<p style="font-size: 0.95rem; color: var(--cb-text-secondary); line-height: 1.5;">${message}</p>`,
        footerHtml: `
          <button class="btn btn-outline" data-dismiss="modal" id="confirm-cancel-btn">Cancel</button>
          <button class="btn ${btnClass}" id="confirm-accept-btn">${confirmText}</button>
        `,
        onOpen: (modal) => {
          modal.querySelector('#confirm-accept-btn').onclick = () => {
            this.close(modal);
            if (onConfirm) onConfirm();
            resolve(true);
          };
          modal.querySelector('#confirm-cancel-btn').onclick = () => {
            this.close(modal);
            resolve(false);
          };
        }
      });
    });
  }
}

// Global Export
window.CityBusModal = new CityBusModalController();
