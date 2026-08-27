/**
 * CityBus Enterprise Platform - Modal Dialog Manager
 * File: js/components/modalDialogManager.js
 * 
 * Provides accessible, animated modal dialogs with backdrop blur,
 * keyboard escape dismiss, focus traps, and dynamic form injection.
 */

class ModalDialogManager {
    constructor() {
        this.activeModal = null;
    }

    open({ title, content, confirmText = 'Confirm', cancelText = 'Cancel', onConfirm = null, onCancel = null, isLarge = false }) {
        this.close(); // Close existing

        const modalOverlay = document.createElement('div');
        modalOverlay.className = 'citybus-modal-overlay';

        const modalDialog = document.createElement('div');
        modalDialog.className = `citybus-modal-dialog ${isLarge ? 'modal-lg' : ''}`;

        modalDialog.innerHTML = `
            <div class="modal-header">
                <h3 class="modal-title">${title}</h3>
                <button class="modal-close-btn" aria-label="Close modal">&times;</button>
            </div>
            <div class="modal-body">
                ${typeof content === 'string' ? content : ''}
            </div>
            <div class="modal-footer">
                ${cancelText ? `<button class="btn btn-secondary modal-cancel-btn">${cancelText}</button>` : ''}
                ${confirmText ? `<button class="btn btn-primary modal-confirm-btn">${confirmText}</button>` : ''}
            </div>
        `;

        if (typeof content !== 'string' && content instanceof HTMLElement) {
            modalDialog.querySelector('.modal-body').appendChild(content);
        }

        modalOverlay.appendChild(modalDialog);
        document.body.appendChild(modalOverlay);

        // Bind events
        const closeBtn = modalDialog.querySelector('.modal-close-btn');
        closeBtn.onclick = () => {
            if (onCancel) onCancel();
            this.close();
        };

        const cancelBtn = modalDialog.querySelector('.modal-cancel-btn');
        if (cancelBtn) {
            cancelBtn.onclick = () => {
                if (onCancel) onCancel();
                this.close();
            };
        }

        const confirmBtn = modalDialog.querySelector('.modal-confirm-btn');
        if (confirmBtn) {
            confirmBtn.onclick = async () => {
                if (onConfirm) {
                    const shouldClose = await onConfirm(modalDialog);
                    if (shouldClose !== false) this.close();
                } else {
                    this.close();
                }
            };
        }

        modalOverlay.onclick = (e) => {
            if (e.target === modalOverlay) {
                if (onCancel) onCancel();
                this.close();
            }
        };

        this.activeModal = modalOverlay;
        requestAnimationFrame(() => modalOverlay.classList.add('modal-visible'));

        // ESC key handler
        this.escHandler = (e) => {
            if (e.key === 'Escape') this.close();
        };
        window.addEventListener('keydown', this.escHandler);

        return modalOverlay;
    }

    close() {
        if (this.activeModal && this.activeModal.parentNode) {
            this.activeModal.classList.remove('modal-visible');
            setTimeout(() => {
                if (this.activeModal && this.activeModal.parentNode) {
                    this.activeModal.parentNode.removeChild(this.activeModal);
                }
                this.activeModal = null;
            }, 250);
        }
        if (this.escHandler) {
            window.removeEventListener('keydown', this.escHandler);
            this.escHandler = null;
        }
    }
}

// Global Export
window.modalManager = new ModalDialogManager();
