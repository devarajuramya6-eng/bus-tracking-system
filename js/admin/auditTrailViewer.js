/**
 * CityBus Enterprise Platform - Security Audit Trail & Compliance Viewer
 * File: js/admin/auditTrailViewer.js
 * 
 * Provides security audit log exploration, filter by action/entity type,
 * IP address tracking, and payload inspection.
 */

class AuditTrailViewerController {
    constructor() {
        this.logs = [];
        this.currentPage = 1;
        this.filterAction = '';
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin'])) {
            return;
        }

        await this.loadAuditLogs();
        this.bindEvents();
    }

    async loadAuditLogs() {
        const container = document.getElementById('audit-trail-container');
        if (!container) return;

        try {
            const res = await window.auditService.getAuditLogs(this.currentPage, 20);
            this.logs = res.logs || [];

            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-hover table-sm align-middle">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Action</th>
                                <th>Entity</th>
                                <th>Entity ID</th>
                                <th>Operator / User</th>
                                <th>IP Address</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this.logs.map(l => `
                                <tr>
                                    <td><small class="text-muted">${l.timestamp}</small></td>
                                    <td><code>${l.action}</code></td>
                                    <td><span class="badge badge-secondary">${l.entity}</span></td>
                                    <td>${l.entity_id || '-'}</td>
                                    <td>${l.user_id ? `User #${l.user_id}` : 'System'}</td>
                                    <td><small>${l.ip_address || '127.0.0.1'}</small></td>
                                    <td><small class="text-muted">${l.extra_info || '-'}</small></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } catch (e) {
            console.error('Audit trail error:', e);
        }
    }

    bindEvents() {
        const refreshBtn = document.getElementById('refresh-audit-btn');
        if (refreshBtn) {
            refreshBtn.onclick = () => this.loadAuditLogs();
        }
    }
}

// Global Export
window.auditTrailViewer = new AuditTrailViewerController();
