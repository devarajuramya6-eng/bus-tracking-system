/**
 * CityBus Enterprise Platform - Maintenance & Work Orders Manager
 * File: js/admin/maintenance_manager.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  let workOrders = [
    { id: 1, work_order_number: 'WO-2608-001', bus: 'Bus AP16-001 (27A)', service_type: 'Brake Inspection', status: 'Completed', cost: '₹3,200', downtime: '3.5 hrs', date: 'Yesterday' },
    { id: 2, work_order_number: 'WO-2608-002', bus: 'Bus AP16-004 (5A)', service_type: 'Coolant Radiator Flush', status: 'In Progress', cost: '₹5,400', downtime: '4.0 hrs', date: 'Today' },
    { id: 3, work_order_number: 'WO-2608-003', bus: 'Bus AP16-009 (45C)', service_type: 'Tire Renewal', status: 'Due', cost: '₹12,800', downtime: '2.0 hrs', date: 'Tomorrow' }
  ];

  try {
    if (window.CityBusAPI) {
      const res = await window.CityBusAPI.get('/maintenance');
      if (res && res.work_orders && res.work_orders.length > 0) {
        workOrders = res.work_orders;
      }
    }
  } catch {}

  const container = document.getElementById('maintenance-table-container');
  if (container) {
    new CityBusDataTable({
      containerId: 'maintenance-table-container',
      columns: [
        { key: 'work_order_number', title: 'Work Order #', render: (val, row) => `<strong>${val || row.id}</strong>` },
        { key: 'bus', title: 'Vehicle', render: (val, row) => val || `Bus #${row.bus_id || 1}` },
        { key: 'service_type', title: 'Service Type' },
        { 
          key: 'status', 
          title: 'Status',
          render: (val) => {
            let cls = val === 'Completed' ? 'badge-success' : (val === 'In Progress' ? 'badge-warning' : 'badge-danger');
            return `<span class="badge ${cls}">${val}</span>`;
          }
        },
        { key: 'cost_inr', title: 'Cost', render: (val, row) => val ? `₹${val}` : (row.cost || '₹4,500') },
        { key: 'downtime_hours', title: 'Downtime', render: (val, row) => val ? `${val} hrs` : (row.downtime || '3 hrs') }
      ],
      data: workOrders,
      searchable: true,
      pageSize: 10
    });
  }

  // Create Work Order Modal Handler
  const createBtn = document.getElementById('open-create-wo-btn');
  if (createBtn) {
    createBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.dynamicModal({
          title: 'Create Preventive Maintenance Work Order',
          bodyHtml: `
            <form id="create-wo-form">
              <div class="form-group">
                <label class="form-label">Select Bus Asset</label>
                <select class="form-control" id="wo-bus-id">
                  <option value="1">Bus AP16-001 (Route 27A)</option>
                  <option value="2">Bus AP16-002 (Route 12B)</option>
                  <option value="3">Bus AP16-003 (Route 45C)</option>
                  <option value="4">Bus AP16-004 (Route 5A)</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Service Type</label>
                <select class="form-control" id="wo-type">
                  <option value="Scheduled Periodic">Scheduled Periodic (15,000 km)</option>
                  <option value="Brake System">Brake Disc & Pad Renewal</option>
                  <option value="Engine & Transmission">Engine & Transmission Check</option>
                  <option value="HVAC / AC Overhaul">HVAC / AC Express Overhaul</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Estimated Cost (INR)</label>
                <input type="number" class="form-control" id="wo-cost" value="4500">
              </div>
              <div class="form-group">
                <label class="form-label">Technician Notes</label>
                <textarea class="form-control" id="wo-desc" rows="2" placeholder="Inspection checklist notes..."></textarea>
              </div>
            </form>
          `,
          footerHtml: `
            <button class="btn btn-outline" data-dismiss="modal">Cancel</button>
            <button class="btn btn-primary" id="save-wo-btn">Create Work Order</button>
          `,
          onOpen: (modal) => {
            modal.querySelector('#save-wo-btn').onclick = async () => {
              const busId = modal.querySelector('#wo-bus-id').value;
              const type = modal.querySelector('#wo-type').value;
              const cost = modal.querySelector('#wo-cost').value;
              const desc = modal.querySelector('#wo-desc').value;

              try {
                if (window.CityBusAPI) {
                  await window.CityBusAPI.post('/maintenance', {
                    bus_id: parseInt(busId),
                    service_type: type,
                    cost_inr: parseFloat(cost),
                    description: desc || 'Routine periodic maintenance'
                  });
                }
              } catch {}

              window.CityBusModal.close(modal);
              if (window.showToast) window.showToast('Work order created and assigned to workshop bay', 'success');
            };
          }
        });
      }
    };
  }
});
