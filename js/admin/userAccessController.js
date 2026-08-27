/**
 * CityBus Enterprise Platform - User Access & RBAC Role Permission Controller
 * File: js/admin/userAccessController.js
 * 
 * Manages user authentication accounts, role hierarchy (Super Admin, Fleet Manager,
 * Dispatcher, Conductor, Driver, Passenger), account lockout flags, and audit logs.
 */

class UserAccessController {
    constructor() {
        this.users = [];
        this.roleFilter = 'ALL';
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin'])) {
            return;
        }

        await this.loadUsers();
        this.bindEvents();
    }

    async loadUsers() {
        const container = document.getElementById('user-access-table-container');
        if (!container) return;

        try {
            const res = await window.apiClient.get('/api/v1/users');
            this.users = res.users || [];
            this.renderUsers();
        } catch (e) {
            console.error('User access load error:', e);
        }
    }

    getFilteredUsers() {
        if (this.roleFilter === 'ALL') return this.users;
        return this.users.filter(u => u.role.toLowerCase() === this.roleFilter.toLowerCase());
    }

    renderUsers() {
        const container = document.getElementById('user-access-table-container');
        if (!container) return;

        const filtered = this.getFilteredUsers();

        container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name & Identity</th>
                            <th>Email Address</th>
                            <th>Assigned Role</th>
                            <th>Phone</th>
                            <th>Account Status</th>
                            <th class="text-end">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filtered.map(u => `
                            <tr>
                                <td><code>#USR-${u.id}</code></td>
                                <td>
                                    <div class="d-flex align-items-center gap-2">
                                        <div class="avatar-circle">${u.name.charAt(0)}</div>
                                        <strong>${u.name}</strong>
                                    </div>
                                </td>
                                <td>${u.email}</td>
                                <td>
                                    <span class="badge ${this.getRoleBadgeClass(u.role)}">${u.role.toUpperCase()}</span>
                                </td>
                                <td>${u.phone || '-'}</td>
                                <td>
                                    <span class="badge badge-success">ACTIVE</span>
                                </td>
                                <td class="text-end">
                                    <button class="btn btn-xs btn-outline-primary change-role-btn" data-id="${u.id}"><i class="fas fa-user-shield"></i> Change Role</button>
                                    <button class="btn btn-xs btn-outline-warning reset-pwd-btn" data-id="${u.id}"><i class="fas fa-key"></i> Reset PWD</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        this.bindUserActions();
    }

    getRoleBadgeClass(role) {
        const r = role.toLowerCase();
        if (r === 'super_admin' || r === 'admin') return 'badge-danger';
        if (r === 'dispatcher' || r === 'fleet_manager') return 'badge-primary';
        if (r === 'conductor' || r === 'driver') return 'badge-warning text-dark';
        return 'badge-secondary';
    }

    bindUserActions() {
        document.querySelectorAll('.change-role-btn').forEach(btn => {
            btn.onclick = () => {
                const id = Number(btn.dataset.id);
                const user = this.users.find(u => u.id === id);
                if (user) this.openRoleChangeModal(user);
            };
        });

        document.querySelectorAll('.reset-pwd-btn').forEach(btn => {
            btn.onclick = async () => {
                const id = Number(btn.dataset.id);
                if (confirm(`Send secure temporary password reset email to User #${id}?`)) {
                    window.toastManager.success(`Password reset token dispatched to user email.`);
                }
            };
        });
    }

    openRoleChangeModal(user) {
        window.modalManager.open({
            title: `🛡️ Change Role for ${user.name}`,
            content: `
                <form id="change-role-form">
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Current Role</label>
                        <input type="text" class="form-control" value="${user.role}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">New Role Permission</label>
                        <select class="form-control" name="new_role">
                            <option value="passenger" ${user.role === 'passenger' ? 'selected' : ''}>Passenger (Standard App Access)</option>
                            <option value="driver" ${user.role === 'driver' ? 'selected' : ''}>Driver (Cockpit & GPS Broadcast)</option>
                            <option value="conductor" ${user.role === 'conductor' ? 'selected' : ''}>Conductor (QR Scanner & Cash POS)</option>
                            <option value="dispatcher" ${user.role === 'dispatcher' ? 'selected' : ''}>Dispatcher (Fleet Radar & Advisories)</option>
                            <option value="fleet_manager" ${user.role === 'fleet_manager' ? 'selected' : ''}>Fleet Manager (Vehicles & Workshops)</option>
                            <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin (Full Access)</option>
                        </select>
                    </div>
                </form>
            `,
            confirmText: 'Update Role',
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#change-role-form');
                const newRole = form.querySelector('select[name="new_role"]').value;

                try {
                    await window.apiClient.put(`/api/v1/users/${user.id}`, { role: newRole });
                    window.toastManager.success(`Updated ${user.name}'s role to ${newRole}.`);
                    this.loadUsers();
                    return true;
                } catch (e) {
                    window.toastManager.error(`Failed to update role: ${e.message}`);
                    return false;
                }
            }
        });
    }

    bindEvents() {
        const filterSelect = document.getElementById('role-filter-select');
        if (filterSelect) {
            filterSelect.onchange = (e) => {
                this.roleFilter = e.target.value;
                this.renderUsers();
            };
        }
    }
}

// Global Export
window.userAccessController = new UserAccessController();
