/**
 * CityBus - Admin Fleet Management & Operations (js/admin.js)
 * 
 * Handles KPI stats, fleet overview Leaflet map, data tables for buses, routes,
 * and drivers, along with Add Bus, Edit Bus, and Delete Bus modal forms.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Navigation & View Switching
  const sidebarLinks = document.querySelectorAll('.sidebar-link');
  const adminSections = document.querySelectorAll('.admin-section');

  sidebarLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetSectionId = link.dataset.section;

      sidebarLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      adminSections.forEach(sec => {
        if (sec.id === targetSectionId) {
          sec.style.display = 'block';
        } else {
          sec.style.display = 'none';
        }
      });

      if (targetSectionId === 'section-live-map' && fleetMap) {
        setTimeout(() => fleetMap.invalidateSize(), 200);
      }
    });
  });

  // KPI Calculations
  function updateKPIs() {
    const buses = CITYBUS_DATA.buses;
    const total = buses.length;
    const active = buses.filter(b => b.status === 'On Route').length;
    const delayed = buses.filter(b => b.status === 'Delayed').length;
    const offline = buses.filter(b => b.status === 'Offline').length;

    const totalEl = document.getElementById('kpi-total-buses');
    const activeEl = document.getElementById('kpi-active-buses');
    const delayedEl = document.getElementById('kpi-delayed-buses');
    const offlineEl = document.getElementById('kpi-offline-buses');

    if (totalEl) totalEl.textContent = total;
    if (activeEl) activeEl.textContent = active;
    if (delayedEl) delayedEl.textContent = delayed;
    if (offlineEl) offlineEl.textContent = offline;
  }

  // Fleet Overview Map
  const mapElement = document.getElementById('admin-fleet-map');
  let fleetMap = null;
  const adminBusMarkers = {};

  if (mapElement) {
    fleetMap = CityBusMap.init('admin-fleet-map', [16.5062, 80.6480], 12);
    CityBusMap.updateBusMarkers(fleetMap, adminBusMarkers, CITYBUS_DATA.buses);
  }

  // Render Buses Table
  function renderBusesTable() {
    const tbody = document.getElementById('admin-buses-tbody');
    if (!tbody) return;

    tbody.innerHTML = CITYBUS_DATA.buses.map(bus => {
      let badgeClass = 'badge-success';
      if (bus.status === 'Delayed') badgeClass = 'badge-warning';
      if (bus.status === 'Offline') badgeClass = 'badge-danger';

      return `
        <tr id="bus-row-${bus.id}">
          <td style="font-weight: 700;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <div class="logo-icon" style="width: 28px; height: 28px; font-size: 0.8rem;">
                <i class="fa-solid fa-bus"></i>
              </div>
              <span>${bus.number}</span>
              <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 500;">(${bus.id})</span>
            </div>
          </td>
          <td style="font-weight: 600;">${bus.route}</td>
          <td>${bus.driver}</td>
          <td>
            <span class="badge ${badgeClass}">
              <span class="badge-dot"></span>${bus.status}
            </span>
          </td>
          <td>${bus.speed} km/h</td>
          <td><span style="font-size: 0.85rem; color: var(--text-muted);">${bus.lastUpdated}</span></td>
          <td>
            <div style="display: flex; gap: 0.4rem;">
              <a href="bus-details.html?id=${bus.id}" class="btn btn-outline btn-sm" title="Live View">
                <i class="fa-solid fa-eye"></i>
              </a>
              <button class="btn btn-outline btn-sm edit-bus-btn" data-bus-id="${bus.id}" title="Edit Bus">
                <i class="fa-solid fa-pen-to-square"></i>
              </button>
              <button class="btn btn-outline btn-sm delete-bus-btn" data-bus-id="${bus.id}" style="color: var(--danger);" title="Remove">
                <i class="fa-solid fa-trash-can"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    // Attach Edit & Delete Listeners
    document.querySelectorAll('.edit-bus-btn').forEach(btn => {
      btn.addEventListener('click', () => openEditBusModal(btn.dataset.busId));
    });

    document.querySelectorAll('.delete-bus-btn').forEach(btn => {
      btn.addEventListener('click', () => deleteBus(btn.dataset.busId));
    });
  }

  // Render Routes Table
  function renderRoutesTable() {
    const tbody = document.getElementById('admin-routes-tbody');
    if (!tbody) return;

    tbody.innerHTML = CITYBUS_DATA.routes.map(route => `
      <tr>
        <td style="font-weight: 800; color: var(--primary);">Route ${route.number}</td>
        <td>${route.origin}</td>
        <td>${route.destination}</td>
        <td>${route.stopsCount} Stops</td>
        <td><span class="badge badge-primary">${route.activeBusesCount} Operating</span></td>
        <td>${route.fare}</td>
        <td>
          <span class="badge ${route.category === 'Express' ? 'badge-success' : 'badge-warning'}">
            ${route.category}
          </span>
        </td>
      </tr>
    `).join('');
  }

  // Render Drivers Table
  function renderDriversTable() {
    const tbody = document.getElementById('admin-drivers-tbody');
    if (!tbody) return;

    tbody.innerHTML = CITYBUS_DATA.drivers.map(driver => `
      <tr>
        <td style="font-weight: 700;">${driver.name}</td>
        <td>${driver.phone}</td>
        <td><code>${driver.license}</code></td>
        <td><span class="badge badge-dark">Bus ${driver.assignedBus}</span></td>
        <td><i class="fa-solid fa-star" style="color: #EAB308;"></i> ${driver.rating}</td>
        <td>
          <span class="badge ${driver.status === 'Active' ? 'badge-success' : 'badge-warning'}">
            ${driver.status}
          </span>
        </td>
      </tr>
    `).join('');
  }

  // Add Bus Modal Handling
  const addBusBtn = document.getElementById('open-add-bus-modal');
  const addBusModal = document.getElementById('add-bus-modal');
  const addBusForm = document.getElementById('add-bus-form');
  const closeAddBusModalBtn = document.getElementById('close-add-bus-modal');
  const cancelAddBusBtn = document.getElementById('cancel-add-bus');

  if (addBusBtn && addBusModal) {
    addBusBtn.addEventListener('click', () => {
      addBusModal.classList.add('show');
    });

    const closeAddModal = () => addBusModal.classList.remove('show');
    if (closeAddBusModalBtn) closeAddBusModalBtn.addEventListener('click', closeAddModal);
    if (cancelAddBusBtn) cancelAddBusBtn.addEventListener('click', closeAddModal);

    if (addBusForm) {
      addBusForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const num = document.getElementById('new-bus-number').value.trim();
        const routeId = document.getElementById('new-bus-route').value;
        const driverName = document.getElementById('new-bus-driver').value.trim();
        const busType = document.getElementById('new-bus-type').value;
        const status = document.getElementById('new-bus-status').value;

        if (!num || !driverName) {
          showToast('Please fill out all required fields', 'warning');
          return;
        }

        const selectedRoute = CITYBUS_DATA.routes.find(r => r.id === routeId) || CITYBUS_DATA.routes[0];
        const newId = `BUS-${Math.floor(100 + Math.random() * 900)}`;

        const newBus = {
          id: newId,
          number: num,
          routeId: routeId,
          route: selectedRoute.name,
          lat: 16.5062 + (Math.random() - 0.5) * 0.02,
          lng: 80.6480 + (Math.random() - 0.5) * 0.02,
          speed: status === 'Offline' ? 0 : 35,
          status: status,
          driver: driverName,
          busType: busType,
          nextStop: "Benz Circle Junction",
          nextStopId: "STOP-4",
          eta: status === 'Offline' ? null : 8,
          occupancy: "20%",
          lastUpdated: "Just added",
          currentWaypointIdx: 0,
          direction: 1
        };

        CITYBUS_DATA.buses.unshift(newBus);

        updateKPIs();
        renderBusesTable();
        if (fleetMap) CityBusMap.updateBusMarkers(fleetMap, adminBusMarkers, CITYBUS_DATA.buses);

        closeAddModal();
        addBusForm.reset();
        showToast(`Bus ${num} (${newId}) added to fleet!`, 'success');
      });
    }
  }

  // Edit Bus Modal Handling
  function openEditBusModal(busId) {
    const bus = CITYBUS_DATA.buses.find(b => b.id === busId);
    if (!bus) return;

    let editModal = document.getElementById('edit-bus-modal');
    if (!editModal) {
      editModal = document.createElement('div');
      editModal.id = 'edit-bus-modal';
      editModal.className = 'modal-backdrop';
      document.body.appendChild(editModal);
    }

    editModal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-header">
          <h3 class="modal-title">Edit Bus ${bus.number} (${bus.id})</h3>
          <button class="modal-close-btn" id="close-edit-bus"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <form id="edit-bus-form">
          <div class="modal-body">
            <div class="form-group">
              <label class="form-label">Bus Number</label>
              <input type="text" id="edit-bus-number" class="form-control" value="${bus.number}" required>
            </div>
            <div class="form-group">
              <label class="form-label">Driver</label>
              <input type="text" id="edit-bus-driver" class="form-control" value="${bus.driver}" required>
            </div>
            <div class="form-group">
              <label class="form-label">Operating Status</label>
              <select id="edit-bus-status" class="form-control">
                <option value="On Route" ${bus.status === 'On Route' ? 'selected' : ''}>On Route (Active)</option>
                <option value="Delayed" ${bus.status === 'Delayed' ? 'selected' : ''}>Delayed</option>
                <option value="Offline" ${bus.status === 'Offline' ? 'selected' : ''}>Offline (Maintenance/Standby)</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" id="cancel-edit-bus">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </div>
        </form>
      </div>
    `;

    editModal.classList.add('show');

    const closeEdit = () => editModal.classList.remove('show');
    document.getElementById('close-edit-bus').addEventListener('click', closeEdit);
    document.getElementById('cancel-edit-bus').addEventListener('click', closeEdit);

    document.getElementById('edit-bus-form').addEventListener('submit', (e) => {
      e.preventDefault();
      bus.number = document.getElementById('edit-bus-number').value.trim();
      bus.driver = document.getElementById('edit-bus-driver').value.trim();
      bus.status = document.getElementById('edit-bus-status').value;
      if (bus.status === 'Offline') bus.speed = 0;

      updateKPIs();
      renderBusesTable();
      if (fleetMap) CityBusMap.updateBusMarkers(fleetMap, adminBusMarkers, CITYBUS_DATA.buses);

      closeEdit();
      showToast(`Updated details for Bus ${bus.number}`, 'success');
    });
  }

  // Delete Bus
  function deleteBus(busId) {
    if (confirm(`Are you sure you want to decommission bus ${busId} from active fleet?`)) {
      const idx = CITYBUS_DATA.buses.findIndex(b => b.id === busId);
      if (idx !== -1) {
        const deleted = CITYBUS_DATA.buses.splice(idx, 1)[0];
        updateKPIs();
        renderBusesTable();
        if (fleetMap) CityBusMap.updateBusMarkers(fleetMap, adminBusMarkers, CITYBUS_DATA.buses);
        showToast(`Bus ${deleted.number} removed from fleet.`, 'info');
      }
    }
  }

  // Initial Table & Map Render
  updateKPIs();
  renderBusesTable();
  renderRoutesTable();
  renderDriversTable();

  // Listen to simulator coordinate changes to update map & live rows
  window.addEventListener('citybus:data-updated', () => {
    if (fleetMap) {
      CityBusMap.updateBusMarkers(fleetMap, adminBusMarkers, CITYBUS_DATA.buses);
    }
  });
});
