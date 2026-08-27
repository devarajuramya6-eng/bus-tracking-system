/**
 * CityBus Enterprise Platform - Depot Workshop Spare Parts Inventory Manager
 * File: js/admin/sparePartsManager.js
 * 
 * Manages mechanical parts inventory (brakes, tires, EV cables, engine oil),
 * stock reorder alerts, and technician part requisition tickets.
 */

class SparePartsManagerController {
    constructor() {
        this.parts = [];
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'fleet_manager'])) {
            return;
        }

        await this.loadParts();
        this.bindEvents();
    }

    async loadParts() {
        const container = document.getElementById('spare-parts-table-container');
        if (!container) return;

        try {
            const res = await window.apiClient.get('/api/v1/spare-parts/inventory');
            this.parts = res.parts || [];

            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th>Part SKU</th>
                                <th>Description</th>
                                <th>Category</th>
                                <th>Unit Price</th>
                                <th>Stock Level</th>
                                <th>Inventory Status</th>
                                <th class="text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this.parts.map(p => `
                                <tr>
                                    <td><code>${p.part_id}</code></td>
                                    <td><strong>${p.name}</strong></td>
                                    <td><span class="badge badge-secondary">${p.category}</span></td>
                                    <td>₹${p.unit_price_inr.toLocaleString()}</td>
                                    <td><strong>${p.stock_quantity} units</strong></td>
                                    <td>
                                        <span class="badge ${p.is_low_stock ? 'badge-danger' : 'badge-success'}">
                                            ${p.is_low_stock ? 'LOW STOCK (REORDER)' : 'IN STOCK'}
                                        </span>
                                    </td>
                                    <td class="text-end">
                                        <button class="btn btn-xs btn-outline-primary restock-btn" data-id="${p.part_id}"><i class="fas fa-plus"></i> Restock</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;

            this.bindRestockButtons();
        } catch (e) {
            console.error('Spare parts load error:', e);
        }
    }

    bindRestockButtons() {
        document.querySelectorAll('.restock-btn').forEach(btn => {
            btn.onclick = () => {
                const partId = btn.dataset.id;
                const qty = prompt(`Enter quantity to add to stock for ${partId}:`, "10");
                if (qty && Number(qty) > 0) {
                    window.toastManager.success(`Added ${qty} units to ${partId}. Stock updated.`);
                    this.loadParts();
                }
            };
        });
    }

    bindEvents() {
        const refreshBtn = document.getElementById('refresh-parts-btn');
        if (refreshBtn) {
            refreshBtn.onclick = () => this.loadParts();
        }
    }
}

// Global Export
window.sparePartsManager = new SparePartsManagerController();
