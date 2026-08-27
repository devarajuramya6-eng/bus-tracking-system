/**
 * CityBus Enterprise Platform - Bus Fleet Management Controller
 * File: js/admin/busFleetManager.js
 * 
 * Provides administrative vehicle registry management, OBD-II device pairing,
 * capacity configuration, fuel type selection, and route assignments.
 */

class BusFleetManagerController {
    constructor() {
        this.buses = [];
        this.routes = [];
        this.drivers = [];
        this.selectedBus = null;
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'fleet_manager'])) {
            return;
        }

        await this.loadDependencies();
        await this.loadBusTable();
        this.bindEvents();
    }

    async loadDependencies() {
        try {
            this.routes = await window.routeService.getAllRoutes();
            const driverRes = await window.driverService.getAllDrivers();
            this.drivers = driverRes.drivers || [];
        } catch (e) {
            console.error('Failed to load fleet dependencies:', e);
        }
    }

    async loadBusTable() {
        const container = document.getElementById('bus-fleet-table-container');
        if (!container) return;

        try {
            this.buses = await window.busService.getAllBuses();

            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th>Bus #</th>
                                <th>Plate #</th>
                                <th>Model & Powertrain</th>
                                <th>Capacity</th>
                                <th>Assigned Route</th>
                                <th>Assigned Driver</th>
                                <th>Status</th>
                                <th class="text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this.buses.map(b => `
                                <tr>
                                    <td><strong>${b.bus_number}</strong></td>
                                    <td><code>${b.registration_plate || 'AP-16-UNREG'}</code></td>
                                    <td>
                                        <span class="badge ${b.fuel_type === 'Electric' ? 'badge-success' : 'badge-secondary'}">
                                            <i class="fas ${b.fuel_type === 'Electric' ? 'fa-bolt' : 'fa-gas-pump'}"></i> ${b.fuel_type || 'Diesel'}
                                        </span>
                                        <small class="text-muted d-block">${b.model || 'Standard City Bus'}</small>
                                    </td>
                                    <td>${b.capacity || 45} seats</td>
                                    <td>${b.route || '<span class="text-muted">Unassigned</span>'}</td>
                                    <td>${b.driver || '<span class="text-muted">None</span>'}</td>
                                    <td>
                                        <span class="badge ${b.status === 'On Route' ? 'badge-success' : (b.status === 'Delayed' ? 'badge-warning' : (b.status === 'Maintenance' ? 'badge-danger' : 'badge-secondary'))}">
                                            ${b.status}
                                        </span>
                                    </td>
                                    <td class="text-end">
                                        <button class="btn btn-xs btn-outline-primary edit-bus-btn" data-id="${b.id}"><i class="fas fa-edit"></i> Edit</button>
                                        <button class="btn btn-xs btn-outline-danger delete-bus-btn" data-id="${b.id}"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;

            this.bindRowActions();
        } catch (e) {
            console.error('Bus table error:', e);
        }
    }

    bindRowActions() {
        document.querySelectorAll('.edit-bus-btn').forEach(btn => {
            btn.onclick = () => {
                const id = Number(btn.dataset.id);
                const bus = this.buses.find(b => b.id === id);
                if (bus) this.openBusModal(bus);
            };
        });

        document.querySelectorAll('.delete-bus-btn').forEach(btn => {
            btn.onclick = async () => {
                const id = Number(btn.dataset.id);
                if (confirm(`Are you sure you want to retire Bus #${id}?`)) {
                    await window.busService.deleteBus(id);
                    window.toastManager.success(`Bus #${id} retired.`);
                    this.loadBusTable();
                }
            };
        });
    }

    openBusModal(bus = null) {
        const isEdit = !!bus;
        const title = isEdit ? `Edit Bus Asset ${bus.bus_number}` : 'Register New Bus Asset';

        const routeOptions = this.routes.map(r => `
            <option value="${r.id}" ${bus && bus.route_id === r.id ? 'selected' : ''}>${r.route_number} - ${r.start_point} ⇄ ${r.destination}</option>
        `).join('');

        const driverOptions = this.drivers.map(d => `
            <option value="${d.id}" ${bus && bus.driver_id === d.id ? 'selected' : ''}>${d.name} (${d.phone})</option>
        `).join('');

        window.modalManager.open({
            title,
            isLarge: true,
            content: `
                <form id="bus-asset-form">
                    <div class="row g-3">
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Bus Number / Fleet ID</label>
                            <input type="text" class="form-control" name="bus_number" value="${bus ? bus.bus_number : ''}" placeholder="e.g. AP16-055" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Registration Number Plate</label>
                            <input type="text" class="form-control" name="registration_plate" value="${bus && bus.registration_plate ? bus.registration_plate : ''}" placeholder="e.g. AP 16 Z 4501">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Vehicle Model / Chassis</label>
                            <input type="text" class="form-control" name="model" value="${bus ? bus.model : 'Metro Express Low Floor'}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Powertrain / Fuel Type</label>
                            <select class="form-control" name="fuel_type">
                                <option value="Diesel" ${bus && bus.fuel_type === 'Diesel' ? 'selected' : ''}>Diesel (BS-VI)</option>
                                <option value="Electric" ${bus && bus.fuel_type === 'Electric' ? 'selected' : ''}>Electric Battery (EV)</option>
                                <option value="CNG" ${bus && bus.fuel_type === 'CNG' ? 'selected' : ''}>CNG Clean Fuel</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Seating Capacity</label>
                            <input type="number" class="form-control" name="capacity" value="${bus ? bus.capacity : 45}" min="15" max="90" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label font-weight-bold">Assigned Corridor Route</label>
                            <select class="form-control" name="route_id">
                                <option value="">-- Unassigned --</option>
                                ${routeOptions}
                            </select>
                        </div>
                    </div>
                </form>
            `,
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#bus-asset-form');
                const busData = {
                    bus_number: form.querySelector('input[name="bus_number"]').value.trim(),
                    registration_plate: form.querySelector('input[name="registration_plate"]').value.trim(),
                    model: form.querySelector('input[name="model"]').value.trim(),
                    fuel_type: form.querySelector('select[name="fuel_type"]').value,
                    capacity: Number(form.querySelector('input[name="capacity"]').value),
                    route_id: form.querySelector('select[name="route_id"]').value ? Number(form.querySelector('select[name="route_id"]').value) : null
                };

                if (!busData.bus_number) {
                    window.toastManager.warning('Bus number is required.');
                    return false;
                }

                try {
                    if (isEdit) {
                        await window.busService.updateBus(bus.id, busData);
                        window.toastManager.success(`Bus ${busData.bus_number} updated.`);
                    } else {
                        await window.busService.createBus(busData);
                        window.toastManager.success(`Bus ${busData.bus_number} registered.`);
                    }
                    this.loadBusTable();
                    return true;
                } catch (e) {
                    window.toastManager.error(`Error saving bus: ${e.message}`);
                    return false;
                }
            }
        });
    }

    bindEvents() {
        const addBtn = document.getElementById('add-new-bus-btn');
        if (addBtn) {
            addBtn.onclick = () => this.openBusModal();
        }
    }
}

// Global Export
window.busFleetManager = new BusFleetManagerController();
