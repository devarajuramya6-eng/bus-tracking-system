/**
 * CityBus Enterprise Platform - Spare Parts Warehouse Inventory Manager
 * File: js/admin/spare_parts_inventory.js
 * 
 * Provides depot spare parts tracking:
 * - Real-time stock on hand vs Minimum Safety Stock
 * - EOQ automated purchase requisition triggers
 * - Barcode search and parts catalog
 */

class CityBusSparePartsInventory {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  async init() {
    this.parts = [
      { partNo: 'BRK-LIN-01', name: 'Heavy Duty Front Brake Lining Set', category: 'Braking', stock: 14, minStock: 20, unitCost: 3450, status: 'Reorder Due', shelfLocation: 'A-04-12' },
      { partNo: 'TIR-295-80', name: 'Radial Transit Bus Tire 295/80R22.5', category: 'Tires & Wheels', stock: 8, minStock: 12, unitCost: 18500, status: 'Reorder Due', shelfLocation: 'T-01-04' },
      { partNo: 'FLT-OIL-HD', name: 'Cummins ISB6.7 Engine Oil Filter', category: 'Engine Service', stock: 45, minStock: 30, unitCost: 680, status: 'Stocked', shelfLocation: 'F-02-08' },
      { partNo: 'EV-CON-120', name: 'CCS2 DC Fast Charging Gun & Cable', category: 'EV Infrastructure', stock: 2, minStock: 3, unitCost: 42000, status: 'Reorder Due', shelfLocation: 'E-01-01' },
      { partNo: 'ALT-24V-150', name: 'Delco Remy 24V 150A Heavy Alternator', category: 'Electrical', stock: 9, minStock: 6, unitCost: 24000, status: 'Stocked', shelfLocation: 'EL-03-05' }
    ];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin: 0;">Central Depot Spare Parts Warehouse</h3>
            <p style="font-size: 0.85rem; color: var(--cb-text-muted); margin: 2px 0 0 0;">Parts Inventory & Automatic Purchase Requisitions</p>
          </div>
          <button class="btn btn-primary" onclick="alert('Generate Batch Purchase Orders.')">📦 Reorder Flagged Items</button>
        </div>

        <div class="card" style="padding: 1.5rem; overflow-x: auto;">
          <table class="table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--cb-border-color); text-align: left; font-size: 0.8rem; color: var(--cb-text-muted);">
                <th style="padding: 0.75rem;">PART NO</th>
                <th style="padding: 0.75rem;">ITEM DESCRIPTION</th>
                <th style="padding: 0.75rem;">CATEGORY</th>
                <th style="padding: 0.75rem;">LOCATION</th>
                <th style="padding: 0.75rem;">STOCK / MIN</th>
                <th style="padding: 0.75rem;">UNIT PRICE</th>
                <th style="padding: 0.75rem;">STATUS</th>
                <th style="padding: 0.75rem;">ACTION</th>
              </tr>
            </thead>
            <tbody>
              ${this.parts.map(p => `
                <tr style="border-bottom: 1px solid var(--cb-border-color); font-size: 0.85rem;">
                  <td style="padding: 0.75rem; font-weight: 700; color: var(--cb-brand-primary);">${p.partNo}</td>
                  <td style="padding: 0.75rem; font-weight: 600;">${p.name}</td>
                  <td style="padding: 0.75rem; color: var(--cb-text-muted);">${p.category}</td>
                  <td style="padding: 0.75rem;"><span class="badge" style="background: var(--cb-bg-subtle);">${p.shelfLocation}</span></td>
                  <td style="padding: 0.75rem; font-weight: 700; color: ${p.stock <= p.minStock ? 'var(--cb-status-danger)' : 'var(--cb-text-primary)'};">
                    ${p.stock} / ${p.minStock} units
                  </td>
                  <td style="padding: 0.75rem; font-weight: 600;">₹${p.unitCost.toLocaleString()}</td>
                  <td style="padding: 0.75rem;">
                    <span class="badge ${p.stock <= p.minStock ? 'badge-danger' : 'badge-success'}">${p.status}</span>
                  </td>
                  <td style="padding: 0.75rem;">
                    <button class="btn btn-sm btn-outline-primary" onclick="alert('Creating purchase requisition for ${p.partNo}')">Reorder</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

      </div>
    `;
  }
}

// Global Export
window.CityBusSparePartsInventory = CityBusSparePartsInventory;
