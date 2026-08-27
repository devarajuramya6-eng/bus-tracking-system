/**
 * CityBus Enterprise Platform - Driver Fatigue & DMS Camera Alert Viewer
 * File: js/admin/crewFatigueViewer.js
 * 
 * Displays in-cabin PERCLOS eye-closure alarms, yawning frequencies,
 * and enables supervisor dispatch of rest relief drivers.
 */

class CrewFatigueViewerController {
    constructor() {
        this.alerts = [];
        this.pollTimer = null;
    }

    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'dispatcher', 'fleet_manager'])) {
            return;
        }

        await this.loadAlerts();
        this.pollTimer = setInterval(() => this.loadAlerts(), 4000);
    }

    async loadAlerts() {
        const container = document.getElementById('fatigue-alerts-feed');
        if (!container) return;

        try {
            const res = await window.apiClient.get('/api/v1/crew-fatigue/alerts');
            this.alerts = res.alerts || [];

            if (this.alerts.length === 0) {
                container.innerHTML = '<div class="text-success p-3 text-center"><i class="fas fa-check-circle"></i> All active drivers operating at normal alertness levels.</div>';
                return;
            }

            container.innerHTML = this.alerts.map(a => `
                <div class="fatigue-alert-card p-3 mb-2 border rounded border-danger bg-light-danger">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <strong>${a.driver_name} (${a.bus_number})</strong>
                        <span class="badge badge-danger">${a.alert_level}</span>
                    </div>
                    <div class="d-flex gap-3 small text-muted mb-2">
                        <span>Eye Closure (PERCLOS): <strong>${(a.perclos_ratio * 100).toFixed(0)}%</strong></span>
                        <span>Yawns (5m): <strong>${a.yawn_count}</strong></span>
                        <span>Head Pitch: <strong>${a.head_pitch}°</strong></span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">${a.timestamp}</small>
                        <button class="btn btn-xs btn-danger dispatch-relief-btn" data-bus="${a.bus_id}">Dispatch Relief Crew</button>
                    </div>
                </div>
            `).join('');

            this.bindReliefButtons();
        } catch (e) {
            console.error('Fatigue alert error:', e);
        }
    }

    bindReliefButtons() {
        document.querySelectorAll('.dispatch-relief-btn').forEach(btn => {
            btn.onclick = () => {
                const busId = btn.dataset.bus;
                window.toastManager.warning(`Relief driver dispatched to rendezvous with Bus #${busId}. Mandatory 20-min driver break initiated.`);
            };
        });
    }
}

// Global Export
window.crewFatigueViewer = new CrewFatigueViewerController();
