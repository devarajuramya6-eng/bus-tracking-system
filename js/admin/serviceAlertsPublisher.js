/**
 * CityBus Enterprise Platform - Service Disruption Alerts Publisher
 * File: js/admin/serviceAlertsPublisher.js
 * 
 * Creates, updates, and expires system-wide passenger travel advisories,
 * road work alerts, and weather detour warnings.
 */

class ServiceAlertsPublisherController {
    constructor() {
        this.alerts = [];
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'dispatcher'])) {
            return;
        }

        await this.loadAlerts();
        this.bindEvents();
    }

    async loadAlerts() {
        const container = document.getElementById('admin-alerts-list');
        if (!container) return;

        try {
            this.alerts = await window.alertService.getActiveAlerts();

            if (this.alerts.length === 0) {
                container.innerHTML = '<div class="text-success p-3 text-center"><i class="fas fa-check-circle"></i> No active disruption advisories. Service running normally.</div>';
                return;
            }

            container.innerHTML = this.alerts.map(a => `
                <div class="alert-publish-card p-3 mb-2 border rounded d-flex justify-content-between align-items-center">
                    <div>
                        <div class="d-flex align-items-center gap-2 mb-1">
                            <strong>${a.title}</strong>
                            <span class="badge ${a.severity === 'High' ? 'badge-danger' : 'badge-warning'}">${a.severity}</span>
                        </div>
                        <p class="small text-muted mb-0">${a.description}</p>
                    </div>
                    <button class="btn btn-sm btn-outline-danger expire-alert-btn" data-id="${a.id}">Expire / Clear</button>
                </div>
            `).join('');

            this.bindExpireButtons();
        } catch (e) {
            console.error('Alerts load error:', e);
        }
    }

    bindExpireButtons() {
        document.querySelectorAll('.expire-alert-btn').forEach(btn => {
            btn.onclick = async () => {
                const id = btn.dataset.id;
                await window.alertService.deactivateAlert(id);
                window.toastManager.info(`Advisory #${id} cleared.`);
                this.loadAlerts();
            };
        });
    }

    bindEvents() {
        const newAlertBtn = document.getElementById('create-new-alert-btn');
        if (newAlertBtn) {
            newAlertBtn.onclick = () => this.openCreateModal();
        }
    }

    openCreateModal() {
        window.modalManager.open({
            title: '📢 Publish Service Advisory',
            content: `
                <form id="publish-advisory-form">
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Advisory Headline</label>
                        <input type="text" class="form-control" name="title" placeholder="e.g. Route 27A Heavy Rain Detour" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Severity Level</label>
                        <select class="form-control" name="severity">
                            <option value="Low">Low (General Notice)</option>
                            <option value="Medium" selected>Medium (Moderate Delay)</option>
                            <option value="High">High (Route Suspension / Major Detour)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Detailed Passenger Advice</label>
                        <textarea class="form-control" name="description" rows="3" placeholder="Explain the cause and alternate boarding platforms..." required></textarea>
                    </div>
                </form>
            `,
            confirmText: 'Publish Live',
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#publish-advisory-form');
                const title = form.querySelector('input[name="title"]').value.trim();
                const severity = form.querySelector('select[name="severity"]').value;
                const description = form.querySelector('textarea[name="description"]').value.trim();

                if (!title || !description) {
                    window.toastManager.warning('Headline and description are required.');
                    return false;
                }

                try {
                    await window.alertService.createAlert({ title, severity, description });
                    window.toastManager.success('Advisory published across all passenger mobile & web feeds.');
                    this.loadAlerts();
                    return true;
                } catch (e) {
                    window.toastManager.error(`Publish error: ${e.message}`);
                    return false;
                }
            }
        });
    }
}

// Global Export
window.serviceAlertsPublisher = new ServiceAlertsPublisherController();
