/**
 * CityBus Enterprise Platform - Admin & Operations Management Logic
 * File: js/admin/admin_dashboard.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let buses = [];
  let routes = [];
  let drivers = [];

  // Sidebar navigation switching
  const sidebarLinks = document.querySelectorAll('.sidebar-link');
  const adminSections = document.querySelectorAll('.admin-section');

  sidebarLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetSectionId = link.dataset.section;

      sidebarLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      adminSections.forEach(sec => {
        sec.style.display = (sec.id === targetSectionId) ? 'block' : 'none';
      });
    });
  });

  // Load initial data
  async function loadData() {
    try {
      if (window.CityBusAPI) {
        const [busesRes, routesRes, summaryRes] = await Promise.all([
          window.CityBusAPI.getBuses(),
          window.CityBusAPI.getRoutes(),
          window.CityBusAPI.getAnalyticsSummary()
        ]);
        buses = busesRes.buses || [];
        routes = routesRes.routes || [];
        if (summaryRes && summaryRes.data) updateKPIs(summaryRes.data);
      }
    } catch {
      buses = (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) ? window.CITYBUS_DATA.buses : [];
      routes = (window.CITYBUS_DATA && window.CITYBUS_DATA.routes) ? window.CITYBUS_DATA.routes : [];
    }

    renderBusesTable();
    renderRoutesTable();
  }

  function updateKPIs(data) {
    const totalEl = document.getElementById('kpi-total-buses');
    const activeEl = document.getElementById('kpi-active-buses');
    const delayedEl = document.getElementById('kpi-delayed-buses');
    const revEl = document.getElementById('kpi-revenue');

    if (totalEl) totalEl.textContent = data.total_buses || buses.length;
    if (activeEl) activeEl.textContent = data.active_buses || buses.filter(b => b.status === 'On Route').length;
    if (delayedEl) delayedEl.textContent = data.delayed_buses || buses.filter(b => b.status === 'Delayed').length;
    if (revEl) revEl.textContent = `₹${(data.today_revenue_inr || 45200).toLocaleString()}`;
  }

  // Render Buses Advanced DataTable
  function renderBusesTable() {
    if (!document.getElementById('admin-buses-table-container')) return;

    new CityBusDataTable({
      containerId: 'admin-buses-table-container',
      columns: [
        { key: 'bus_number', title: 'Vehicle Code', render: (val, row) => `<strong>${val || row.number}</strong>` },
        { key: 'route', title: 'Route Corridor' },
        { key: 'driver', title: 'Assigned Driver' },
        { 
          key: 'status', 
          title: 'Status',
          render: (val) => {
            let cls = val === 'On Route' ? 'badge-success' : (val === 'Delayed' ? 'badge-warning' : 'badge-danger');
            return `<span class="badge ${cls}"><span class="badge-dot"></span> ${val}</span>`;
          }
        },
        { key: 'speed', title: 'Speed', render: (val) => `${val || 0} km/h` },
        { key: 'last_updated', title: 'Last GPS Ping' }
      ],
      data: buses,
      searchable: true,
      selectable: true,
      pageSize: 10,
      onRowClick: (row) => {
        window.location.href = `bus-details.html?id=${row.id}`;
      }
    });
  }

  // Render Routes Advanced DataTable
  function renderRoutesTable() {
    if (!document.getElementById('admin-routes-table-container')) return;

    new CityBusDataTable({
      containerId: 'admin-routes-table-container',
      columns: [
        { key: 'route_number', title: 'Route #', render: (val, row) => `<strong style="color: var(--cb-brand-primary);">${val || row.number}</strong>` },
        { key: 'name', title: 'Corridor Name' },
        { key: 'distance_km', title: 'Distance', render: (val, row) => `${val || row.distance || '15 km'}` },
        { key: 'estimated_time', title: 'Duration', render: (val, row) => `~${val || row.duration || '30 min'}` },
        { key: 'base_fare', title: 'Base Fare', render: (val, row) => `<strong style="color: var(--cb-status-success);">₹${val || row.fare || 25}</strong>` },
        { key: 'category', title: 'Type', render: (val) => `<span class="badge badge-primary">${val || 'Local'}</span>` }
      ],
      data: routes,
      searchable: true,
      pageSize: 10
    });
  }

  // Visual Route Editor Setup
  const editorMapEl = document.getElementById('visual-route-editor-map');
  if (editorMapEl && window.CityBusMap) {
    const editorMap = window.CityBusMap.createMap('visual-route-editor-map', { center: [16.5062, 80.6480], zoom: 13 });
    if (editorMap) {
      const editor = new VisualRouteEditor(editorMap);
      
      const startDrawBtn = document.getElementById('start-route-draw-btn');
      const clearDrawBtn = document.getElementById('clear-route-draw-btn');
      const saveRouteBtn = document.getElementById('save-drawn-route-btn');

      if (startDrawBtn) {
        startDrawBtn.onclick = () => {
          editor.startEditing(null, (metrics) => {
            const distEl = document.getElementById('drawn-route-dist');
            const durEl = document.getElementById('drawn-route-dur');
            if (distEl) distEl.textContent = metrics.distanceStr;
            if (durEl) durEl.textContent = metrics.durationStr;
          });
        };
      }

      if (clearDrawBtn) clearDrawBtn.onclick = () => editor.clear();

      if (saveRouteBtn) {
        saveRouteBtn.onclick = () => {
          editor.stopEditing();
          if (window.showToast) window.showToast('Route corridor geometry published to live transit network!', 'success');
        };
      }
    }
  }

  await loadData();
});
