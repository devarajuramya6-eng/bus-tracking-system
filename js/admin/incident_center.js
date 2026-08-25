/**
 * CityBus Enterprise Platform - Incident Center & Kanban Workflow
 * File: js/admin/incident_center.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let incidents = [
    { id: 1, number: 'INC-260825-01', title: 'Heavy Traffic near Benz Circle', type: 'Traffic_Delay', severity: 'Low', status: 'New', bus: 'Bus 27A', time: '10 mins ago' },
    { id: 2, number: 'INC-260825-02', title: 'Coolant Temperature Warning', type: 'Breakdown', severity: 'Medium', status: 'Acknowledged', bus: 'Bus 12B', time: '25 mins ago' },
    { id: 3, number: 'INC-260825-03', title: 'Route Diversion on MG Road', type: 'Traffic', severity: 'Medium', status: 'In Progress', bus: 'Bus 45C', time: '40 mins ago' },
    { id: 4, number: 'INC-260825-04', title: 'Passenger Fare Dispute', type: 'Security', severity: 'Low', status: 'Resolved', bus: 'Bus 5A', time: '2 hours ago' }
  ];

  try {
    if (window.CityBusAPI) {
      const res = await window.CityBusAPI.getIncidents();
      if (res && res.incidents && res.incidents.length > 0) {
        incidents = res.incidents;
      }
    }
  } catch {}

  const columns = ['New', 'Acknowledged', 'In Progress', 'Resolved'];

  function renderKanban() {
    columns.forEach(col => {
      const colId = `kanban-col-${col.toLowerCase().replace(' ', '-')}`;
      const colContainer = document.getElementById(colId);
      if (!colContainer) return;

      const colIncidents = incidents.filter(i => (i.status || 'New').toLowerCase() === col.toLowerCase());
      const countEl = document.getElementById(`count-${col.toLowerCase().replace(' ', '-')}`);
      if (countEl) countEl.textContent = colIncidents.length;

      colContainer.innerHTML = colIncidents.map(inc => {
        let badgeClass = 'badge-info';
        if (inc.severity === 'Medium') badgeClass = 'badge-warning';
        if (inc.severity === 'High' || inc.severity === 'Critical') badgeClass = 'badge-danger';

        return `
          <div class="card hover-lift kanban-card" draggable="true" data-inc-id="${inc.id}" style="padding: 0.85rem; margin-bottom: 0.75rem; cursor: grab; border-left: 4px solid var(--cb-status-${badgeClass === 'badge-info' ? 'info' : (badgeClass === 'badge-warning' ? 'warning' : 'danger')});">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: var(--cb-text-muted);">${inc.incident_number || inc.number}</span>
              <span class="badge ${badgeClass}" style="font-size: 0.65rem;">${inc.severity}</span>
            </div>
            <h4 style="font-size: 0.9rem; font-weight: 700; color: var(--cb-text-primary); margin-bottom: 0.35rem;">
              ${inc.title}
            </h4>
            <div style="font-size: 0.75rem; color: var(--cb-text-secondary); margin-bottom: 0.5rem;">
              ${inc.description || 'Assigned to active transit sector'}
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--cb-text-muted);">
              <span><i class="fa-solid fa-bus"></i> ${inc.bus || `Bus #${inc.bus_id || 1}`}</span>
              <span><i class="fa-solid fa-clock"></i> ${inc.time || 'Active'}</span>
            </div>
          </div>
        `;
      }).join('');
    });

    attachDragAndDrop();
  }

  function attachDragAndDrop() {
    document.querySelectorAll('.kanban-card').forEach(card => {
      card.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', card.dataset.incId);
        card.style.opacity = '0.4';
      });
      card.addEventListener('dragend', () => {
        card.style.opacity = '1';
      });
    });

    document.querySelectorAll('.kanban-column-body').forEach(col => {
      col.addEventListener('dragover', (e) => {
        e.preventDefault();
        col.style.backgroundColor = 'var(--cb-brand-primary-light)';
      });
      col.addEventListener('dragleave', () => {
        col.style.backgroundColor = '';
      });
      col.addEventListener('drop', async (e) => {
        e.preventDefault();
        col.style.backgroundColor = '';
        const incId = e.dataTransfer.getData('text/plain');
        const targetStatus = col.dataset.status;

        const inc = incidents.find(i => String(i.id) === String(incId));
        if (inc && targetStatus) {
          inc.status = targetStatus;
          renderKanban();

          if (window.showToast) window.showToast(`Incident #${inc.incident_number || inc.number} moved to ${targetStatus}`, 'info');

          if (window.CityBusAPI) {
            try {
              await window.CityBusAPI.patch(`/incidents/${inc.id}/status`, { status: targetStatus });
            } catch {}
          }
        }
      });
    });
  }

  renderKanban();
});
