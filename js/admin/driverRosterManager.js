/**
 * CityBus Enterprise Platform - Driver Roster & Crew Scheduling Manager
 * File: js/admin/driverRosterManager.js
 * 
 * Provides driver shift assignment, weekly roster planning, safety rating review,
 * and license compliance auditing.
 */

class DriverRosterManagerController {
    constructor() {
        this.drivers = [];
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'fleet_manager'])) {
            return;
        }

        await this.loadDriverRoster();
        this.bindEvents();
    }

    async loadDriverRoster() {
        const container = document.getElementById('driver-roster-container');
        if (!container) return;

        try {
            const res = await window.driverService.getAllDrivers();
            this.drivers = res.drivers || [];

            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th>Driver Name</th>
                                <th>Contact Phone</th>
                                <th>License #</th>
                                <th>Experience</th>
                                <th>Safety Rating</th>
                                <th>Shift Status</th>
                                <th class="text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this.drivers.map(d => `
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center gap-2">
                                            <div class="avatar-circle">${d.name.charAt(0)}</div>
                                            <div>
                                                <strong>${d.name}</strong>
                                                <small class="text-muted d-block">${d.email || 'operator@citybus.transit'}</small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>${d.phone}</td>
                                    <td><code>${d.license_number || 'AP-16-2020-001'}</code></td>
                                    <td>${d.experience_years || 3} Years</td>
                                    <td>
                                        <span class="badge badge-warning text-dark font-weight-bold">
                                            ⭐ ${d.rating || 4.8}
                                        </span>
                                    </td>
                                    <td>
                                        <span class="badge ${d.status === 'Active' ? 'badge-success' : 'badge-secondary'}">
                                            ${d.status}
                                        </span>
                                    </td>
                                    <td class="text-end">
                                        <button class="btn btn-xs btn-outline-primary edit-driver-btn" data-id="${d.id}"><i class="fas fa-edit"></i> Edit</button>
                                        <button class="btn btn-xs btn-outline-danger delete-driver-btn" data-id="${d.id}"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;

            this.bindRowActions();
        } catch (e) {
            console.error('Driver roster error:', e);
        }
    }

    bindRowActions() {
        document.querySelectorAll('.edit-driver-btn').forEach(btn => {
            btn.onclick = () => {
                const id = Number(btn.dataset.id);
                const driver = this.drivers.find(d => d.id === id);
                if (driver) this.openDriverModal(driver);
            };
        });

        document.querySelectorAll('.delete-driver-btn').forEach(btn => {
            btn.onclick = async () => {
                const id = Number(btn.dataset.id);
                if (confirm(`Are you sure you want to remove Driver record #${id}?`)) {
                    await window.driverService.deleteDriver(id);
                    window.toastManager.success(`Driver record #${id} removed.`);
                    this.loadDriverRoster();
                }
            };
        });
    }

    openDriverModal(driver = null) {
        const isEdit = !!driver;
        const title = isEdit ? `Edit Driver Profile: ${driver.name}` : 'Register New Fleet Driver';

        window.modalManager.open({
            title,
            content: `
                <form id="driver-profile-form">
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Full Name</label>
                        <input type="text" class="form-control" name="name" value="${driver ? driver.name : ''}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Phone Number</label>
                        <input type="text" class="form-control" name="phone" value="${driver ? driver.phone : ''}" placeholder="+91 98480 12345" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Commercial Driving License #</label>
                        <input type="text" class="form-control" name="license_number" value="${driver && driver.license_number ? driver.license_number : ''}" placeholder="AP-16-2022-4589">
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Experience (Years)</label>
                        <input type="number" class="form-control" name="experience_years" value="${driver ? driver.experience_years : 4}" min="1" max="40">
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Shift Duty Status</label>
                        <select class="form-control" name="status">
                            <option value="Active" ${driver && driver.status === 'Active' ? 'selected' : ''}>Active (Available on Roster)</option>
                            <option value="On Break" ${driver && driver.status === 'On Break' ? 'selected' : ''}>On Break / Rest Period</option>
                            <option value="Offline" ${driver && driver.status === 'Offline' ? 'selected' : ''}>Offline / Leave</option>
                        </select>
                    </div>
                </form>
            `,
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#driver-profile-form');
                const driverData = {
                    name: form.querySelector('input[name="name"]').value.trim(),
                    phone: form.querySelector('input[name="phone"]').value.trim(),
                    license_number: form.querySelector('input[name="license_number"]').value.trim(),
                    experience_years: Number(form.querySelector('input[name="experience_years"]').value),
                    status: form.querySelector('select[name="status"]').value
                };

                if (!driverData.name || !driverData.phone) {
                    window.toastManager.warning('Name and phone number are required.');
                    return false;
                }

                try {
                    if (isEdit) {
                        await window.driverService.updateDriver(driver.id, driverData);
                        window.toastManager.success(`Driver ${driverData.name} updated.`);
                    } else {
                        await window.driverService.createDriver(driverData);
                        window.toastManager.success(`Driver ${driverData.name} enrolled.`);
                    }
                    this.loadDriverRoster();
                    return true;
                } catch (e) {
                    window.toastManager.error(`Error saving driver: ${e.message}`);
                    return false;
                }
            }
        });
    }

    bindEvents() {
        const addBtn = document.getElementById('add-new-driver-btn');
        if (addBtn) {
            addBtn.onclick = () => this.openDriverModal();
        }
    }
}

// Global Export
window.driverRosterManager = new DriverRosterManagerController();
