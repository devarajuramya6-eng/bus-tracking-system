/**
 * CityBus Enterprise Platform - Passenger Lost & Found Search Portal
 * File: js/passenger/lostFoundPortal.js
 * 
 * Provides catalog search for items lost on transit vehicles, filter by category,
 * and claim submission forms.
 */

class LostFoundPortalController {
    constructor() {
        this.items = [];
        this.currentCategory = 'all';
    }

    async init() {
        await this.loadItems();
        this.bindEvents();
    }

    async loadItems() {
        const container = document.getElementById('lost-found-items-container');
        if (!container) return;

        try {
            const res = await window.apiClient.get(`/api/v1/lost-found/items?category=${this.currentCategory}`);
            this.items = res.items || [];
            this.renderItems(this.items);
        } catch (e) {
            console.error('Lost & found error:', e);
        }
    }

    renderItems(items) {
        const container = document.getElementById('lost-found-items-container');
        if (!container) return;

        if (items.length === 0) {
            container.innerHTML = '<div class="text-muted p-4 text-center">No unclaimed property matching your query in the depot safe.</div>';
            return;
        }

        container.innerHTML = `
            <div class="row g-3">
                ${items.map(item => `
                    <div class="col-md-6 col-lg-4">
                        <div class="card h-100 shadow-sm border-0">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <span class="badge badge-primary">${item.category}</span>
                                    <small class="text-muted">${item.found_date}</small>
                                </div>
                                <h5 class="card-title">${item.description}</h5>
                                <p class="card-text small text-muted">Found on Bus #${item.bus_id} • Held at Central Depot Safe</p>
                                <button class="btn btn-outline-primary btn-sm btn-block claim-property-btn" data-id="${item.item_id}">
                                    <i class="fas fa-hand-holding"></i> File Ownership Claim
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        this.bindClaimButtons();
    }

    bindClaimButtons() {
        document.querySelectorAll('.claim-property-btn').forEach(btn => {
            btn.onclick = () => {
                const itemId = Number(btn.dataset.id);
                this.openClaimModal(itemId);
            };
        });
    }

    openClaimModal(itemId) {
        window.modalManager.open({
            title: '🏷️ Claim Lost Property',
            content: `
                <form id="claim-property-form">
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Proof of Ownership / Distinct Identifiers</label>
                        <textarea class="form-control" name="notes" rows="3" placeholder="Describe specific contents, colors, lock screens, serial numbers or unique marks..." required></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Contact Phone Number</label>
                        <input type="text" class="form-control" name="phone" placeholder="+91 98480 12345" required>
                    </div>
                </form>
            `,
            confirmText: 'Submit Claim',
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#claim-property-form');
                const notes = form.querySelector('textarea[name="notes"]').value.trim();
                const user = window.authService.getUser();

                if (!notes) {
                    window.toastManager.warning('Please provide identifying details for your item.');
                    return false;
                }

                try {
                    await window.apiClient.post(`/api/v1/lost-found/claim/${itemId}`, {
                        user_id: user ? user.id : 1,
                        notes
                    });
                    window.toastManager.success('Claim submitted! Depot supervisor will verify and reach out.');
                    this.loadItems();
                    return true;
                } catch (e) {
                    window.toastManager.error(`Claim error: ${e.message}`);
                    return false;
                }
            }
        });
    }

    bindEvents() {
        const catSelect = document.getElementById('lost-found-cat-filter');
        if (catSelect) {
            catSelect.onchange = (e) => {
                this.currentCategory = e.target.value;
                this.loadItems();
            };
        }
    }
}

// Global Export
window.lostFoundPortal = new LostFoundPortalController();
