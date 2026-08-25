/**
 * CityBus Enterprise Platform - Dispatcher Tactical Command Center Logic
 * File: js/dispatcher/command_center.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let activeFilter = 'All';
  let searchQuery = '';
  let selectedBus = null;
  let allBuses = [];

  const mapElement = document.getElementById('dispatcher-radar-map');
  let map = null;
  let busLayer = null;

  // 1. Initialize Radar Map
  if (mapElement && window.CityBusMap) {
    map = window.CityBusMap.createMap('dispatcher-radar-map', { center: [16.5062, 80.6480], zoom: 12 });
    if (map) {
      busLayer = new BusLayerManager(map);
    }
  }

  // 2. Load Fleet Data
  async function loadFleet() {
    try {
      if (window.CityBusAPI) {
        const res = await window.CityBusAPI.getBuses();
        allBuses = res.buses || [];
      } else if (window.CITYBUS_DATA) {
        allBuses = window.CITYBUS_DATA.buses || [];
      }
    } catch {
      allBuses = (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) ? window.CITYBUS_DATA.buses : [];
    }

    renderFleetList();
    if (busLayer) busLayer.updateBuses(allBuses, selectBus);
  }

  // 3. Render Fleet Vehicle Sidebar
  function renderFleetList() {
    const listContainer = document.getElementById('dispatcher-fleet-list');
    const fleetCountEl = document.getElementById('dispatcher-fleet-count');
    if (!listContainer) return;

    let filtered = [...allBuses];

    if (activeFilter === 'Moving') filtered = filtered.filter(b => b.status === 'On Route' && b.speed > 5);
    else if (activeFilter === 'Delayed') filtered = filtered.filter(b => b.status === 'Delayed');
    else if (activeFilter === 'Offline') filtered = filtered.filter(b => b.status === 'Offline');
    else if (activeFilter === 'Emergency') filtered = filtered.filter(b => b.status === 'Emergency');

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(b => 
        b.number?.toLowerCase().includes(q) || 
        b.bus_number?.toLowerCase().includes(q) || 
        b.route?.toLowerCase().includes(q) ||
        b.driver?.toLowerCase().includes(q)
      );
    }

    if (fleetCountEl) fleetCountEl.textContent = `${filtered.length} Vehicles`;

    if (filtered.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align: center; padding: 2rem 1rem; color: var(--cb-text-muted);">
          <i class="fa-solid fa-bus-slash" style="font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
          <div>No vehicles match active filter</div>
        </div>
      `;
      return;
    }

    listContainer.innerHTML = filtered.map(bus => {
      let badgeClass = 'badge-success';
      if (bus.status === 'Delayed') badgeClass = 'badge-warning';
      if (bus.status === 'Offline') badgeClass = 'badge-danger';
      if (bus.status === 'Emergency') badgeClass = 'badge-danger';

      const isSelected = selectedBus && (selectedBus.id === bus.id);

      return `
        <div class="card hover-lift dispatcher-fleet-item ${isSelected ? 'selected' : ''}" data-bus-id="${bus.id}" style="padding: 0.75rem; margin-bottom: 0.5rem; cursor: pointer; border-left: 4px solid var(--cb-status-${badgeClass === 'badge-success' ? 'success' : (badgeClass === 'badge-warning' ? 'warning' : 'danger')});">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
            <strong style="color: var(--cb-text-primary); font-size: 0.9rem;">${bus.number || bus.bus_number}</strong>
            <span class="badge ${badgeClass}" style="font-size: 0.65rem; padding: 2px 6px;">${bus.status}</span>
          </div>
          <div style="font-size: 0.75rem; color: var(--cb-text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 0.35rem;">
            ${bus.route || 'Transit Corridor'}
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--cb-text-muted);">
            <span><i class="fa-solid fa-gauge"></i> ${bus.speed || 0} km/h</span>
            <span><i class="fa-solid fa-user"></i> ${bus.driver || 'Assigned'}</span>
          </div>
        </div>
      `;
    }).join('');

    listContainer.querySelectorAll('.dispatcher-fleet-item').forEach(item => {
      item.onclick = () => {
        const busId = item.dataset.busId;
        const bus = allBuses.find(b => String(b.id) === String(busId));
        if (bus) selectBus(bus);
      };
    });
  }

  // 4. Select Bus & Open Detailed Control Panel
  function selectBus(bus) {
    selectedBus = bus;
    renderFleetList();

    const controlPanel = document.getElementById('dispatcher-bus-control');
    if (!controlPanel) return;

    if (map && window.CityBusMap) {
      window.CityBusMap.panTo(map, bus.lat || bus.latitude, bus.lng || bus.longitude, 15);
    }

    controlPanel.innerHTML = `
      <div class="card anim-fade-in" style="height: 100%; display: flex; flex-direction: column; gap: 1rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--cb-border-default); padding-bottom: 0.75rem;">
          <div>
            <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--cb-text-primary);">${bus.number || bus.bus_number}</h3>
            <div style="font-size: 0.75rem; color: var(--cb-text-muted);">ID: ${bus.id} • ${bus.model || 'Metro Express'}</div>
          </div>
          <span class="badge ${bus.status === 'On Route' ? 'badge-success' : 'badge-warning'}">${bus.status}</span>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; background: var(--cb-bg-subtle); padding: 0.75rem; border-radius: var(--cb-radius-md); font-size: 0.8rem;">
          <div><span style="color: var(--cb-text-muted);">Speed:</span> <strong>${bus.speed || 0} km/h</strong></div>
          <div><span style="color: var(--cb-text-muted);">Occupancy:</span> <strong>${bus.occupancy || 25} Pax</strong></div>
          <div><span style="color: var(--cb-text-muted);">Driver:</span> <strong>${bus.driver || 'Assigned'}</strong></div>
          <div><span style="color: var(--cb-text-muted);">Next Stop:</span> <strong>${bus.nextStop || 'Approaching'}</strong></div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: auto;">
          <button class="btn btn-primary btn-sm btn-block" id="msg-driver-btn">
            <i class="fa-solid fa-comment-dots"></i> Message Driver
          </button>
          <button class="btn btn-outline btn-sm btn-block" id="reassign-route-btn">
            <i class="fa-solid fa-shuffle"></i> Reassign Route
          </button>
          <button class="btn btn-danger btn-sm btn-block" id="emergency-override-btn">
            <i class="fa-solid fa-triangle-exclamation"></i> Emergency Halt / Override
          </button>
        </div>
      </div>
    `;

    // Attach actions
    document.getElementById('msg-driver-btn').onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.dynamicModal({
          title: `Direct Message to Driver: ${bus.driver || 'Ravi Kumar'}`,
          bodyHtml: `
            <textarea class="form-control" rows="3" placeholder="Enter message for vehicle cockpit display... (e.g. 'Caution: road diversion ahead at Benz Circle')"></textarea>
          `,
          footerHtml: `
            <button class="btn btn-outline" data-dismiss="modal">Cancel</button>
            <button class="btn btn-primary" onclick="window.CityBusModal.close(this.closest('.modal-backdrop')); if(window.showToast) window.showToast('Message transmitted to vehicle cockpit HUD', 'success');">
              <i class="fa-solid fa-paper-plane"></i> Send
            </button>
          `
        });
      }
    };

    document.getElementById('emergency-override-btn').onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.confirm({
          title: `Emergency Vehicle Halt: ${bus.number || bus.bus_number}`,
          message: `Are you sure you want to broadcast an immediate Emergency Pull-Over Directive to Bus ${bus.number}?`,
          confirmText: 'Issue Halt Directive',
          confirmType: 'danger',
          onConfirm: () => {
            if (window.showToast) window.showToast(`Emergency directive broadcasted to Bus ${bus.number}`, 'danger', 6000);
          }
        });
      }
    };
  }

  // Filter Chips
  document.querySelectorAll('.dispatcher-filter-chip').forEach(chip => {
    chip.onclick = () => {
      document.querySelectorAll('.dispatcher-filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeFilter = chip.dataset.filter || 'All';
      renderFleetList();
    };
  });

  // Search input
  const searchInput = document.getElementById('dispatcher-search-input');
  if (searchInput) {
    searchInput.oninput = (e) => {
      searchQuery = e.target.value.trim();
      renderFleetList();
    };
  }

  // Initial load
  await loadFleet();

  // Listen for real-time simulator or WebSocket updates
  window.addEventListener('citybus:data-updated', (e) => {
    const buses = e.detail.buses;
    if (buses) {
      allBuses = buses;
      if (busLayer) busLayer.updateBuses(allBuses, selectBus);
      renderFleetList();
    }
  });
});
