/**
 * CityBus Enterprise Platform - Fuel & Fleet Economy Manager
 * File: js/admin/fuel_manager.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let fuelLogs = [
    { id: 1, bus: 'Bus AP16-001 (27A)', liters: 65, rate: 98.5, total: '₹6,402.50', mileage: '4.3 km/L', station: 'Autonagar Depot Station' },
    { id: 2, bus: 'Bus AP16-002 (12B)', liters: 70, rate: 98.5, total: '₹6,895.00', mileage: '4.1 km/L', station: 'PNBS Central Fuel Depot' },
    { id: 3, bus: 'Bus AP16-004 (5A)', liters: 80, rate: 98.5, total: '₹7,880.00', mileage: '4.5 km/L', station: 'Gannavaram Depot Station' }
  ];

  try {
    if (window.CityBusAPI) {
      const res = await window.CityBusAPI.get('/fuel');
      if (res && res.fuel_logs && res.fuel_logs.length > 0) {
        fuelLogs = res.fuel_logs;
      }
    }
  } catch {}

  const container = document.getElementById('fuel-table-container');
  if (container) {
    new CityBusDataTable({
      containerId: 'fuel-table-container',
      columns: [
        { key: 'bus', title: 'Vehicle', render: (val, row) => val || `Bus #${row.bus_id || 1}` },
        { key: 'liters_filled', title: 'Fuel (L)', render: (val, row) => `${val || row.liters || 60} L` },
        { key: 'cost_per_liter_inr', title: 'Rate (₹/L)', render: (val, row) => `₹${val || row.rate || 98.5}` },
        { key: 'total_cost_inr', title: 'Total Cost', render: (val, row) => val ? `₹${val.toLocaleString()}` : (row.total || '₹5,910') },
        { key: 'calculated_km_per_liter', title: 'Efficiency', render: (val, row) => `<strong style="color: var(--cb-status-success);">${val || row.mileage || '4.2 km/L'}</strong>` },
        { key: 'fuel_station', title: 'Fueling Point', render: (val, row) => val || row.station }
      ],
      data: fuelLogs,
      searchable: true,
      pageSize: 10
    });
  }

  // Draw Fleet Efficiency Bar Chart
  if (window.CityBusChartEngine) {
    window.CityBusChartEngine.renderBarChart('fuel-efficiency-chart', {
      labels: ['Bus 27A', 'Bus 12B', 'Bus 45C', 'Bus 5A', 'Bus 10H', 'Bus 33K'],
      data: [4.3, 4.1, 4.4, 4.5, 3.9, 4.2],
      color: '#10B981',
      yAxisUnit: ' km/L'
    });
  }
});
