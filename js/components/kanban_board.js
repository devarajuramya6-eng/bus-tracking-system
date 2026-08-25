/**
 * CityBus Enterprise Platform - Interactive Drag-and-Drop Kanban Board Engine
 * File: js/components/kanban_board.js
 * 
 * Powers visual operations workflows:
 * - Incident lifecycle (`New` -> `Acknowledged` -> `In Progress` -> `Resolved`)
 * - Maintenance work order bays (`Scheduled` -> `In Workshop` -> `Quality Check` -> `Released`)
 */

class CityBusKanban {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.columns = options.columns || [
      { id: 'New', title: 'New Unassigned', badgeClass: 'badge-danger' },
      { id: 'Acknowledged', title: 'Acknowledged', badgeClass: 'badge-warning' },
      { id: 'In Progress', title: 'In Progress', badgeClass: 'badge-primary' },
      { id: 'Resolved', title: 'Resolved', badgeClass: 'badge-success' }
    ];
    this.items = options.items || [];
    this.onStatusChange = options.onStatusChange || null;
    this.renderCard = options.renderCard || this.defaultCardRenderer;
    this.render();
  }

  setItems(items) {
    this.items = items;
    this.render();
  }

  defaultCardRenderer(item) {
    return `
      <div class="card" style="padding: 1rem; margin-bottom: 0.75rem; border-left: 4px solid var(--cb-brand-primary); cursor: grab;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <span style="font-weight: 700; font-size: 0.85rem;">#${item.id || item.incident_number}</span>
          <span class="badge ${item.severity === 'Critical' ? 'badge-danger' : 'badge-warning'}">${item.severity || 'Normal'}</span>
        </div>
        <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 0.25rem;">${item.title || item.type}</div>
        <div style="font-size: 0.75rem; color: var(--cb-text-muted);">${item.description || ''}</div>
      </div>
    `;
  }

  render() {
    if (!this.container) return;
    this.container.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; align-items: start;">
        ${this.columns.map(col => {
          const colItems = this.items.filter(item => (item.status || 'New') === col.id);
          return `
            <div class="kanban-column" data-col-id="${col.id}" style="background: var(--cb-bg-subtle); border-radius: var(--cb-radius-lg); padding: 1rem; min-height: 400px; border: 1px solid var(--cb-border-color);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--cb-border-color);">
                <span style="font-weight: 700; font-size: 0.95rem;">${col.title}</span>
                <span class="badge ${col.badgeClass || 'badge-neutral'}">${colItems.length}</span>
              </div>
              <div class="kanban-dropzone" data-col-id="${col.id}" style="min-height: 320px; display: flex; flex-direction: column;">
                ${colItems.map(item => `
                  <div class="kanban-card" draggable="true" data-item-id="${item.id}">
                    ${this.renderCard(item)}
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

    this.attachDragEvents();
  }

  attachDragEvents() {
    const cards = this.container.querySelectorAll('.kanban-card');
    const dropzones = this.container.querySelectorAll('.kanban-dropzone');

    cards.forEach(card => {
      card.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', card.getAttribute('data-item-id'));
        card.style.opacity = '0.5';
      });

      card.addEventListener('dragend', () => {
        card.style.opacity = '1';
      });
    });

    dropzones.forEach(zone => {
      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.background = 'rgba(37, 99, 235, 0.08)';
        zone.style.borderRadius = 'var(--cb-radius-md)';
      });

      zone.addEventListener('dragleave', () => {
        zone.style.background = 'transparent';
      });

      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.background = 'transparent';
        const itemId = e.dataTransfer.getData('text/plain');
        const targetStatus = zone.getAttribute('data-col-id');

        const item = this.items.find(i => String(i.id) === String(itemId));
        if (item && item.status !== targetStatus) {
          const oldStatus = item.status;
          item.status = targetStatus;
          this.render();
          if (this.onStatusChange) {
            this.onStatusChange(item, targetStatus, oldStatus);
          }
        }
      });
    });
  }
}

// Global Export
window.CityBusKanban = CityBusKanban;
