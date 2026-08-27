/**
 * CityBus Enterprise Platform - Driver Incident & Road Breakdown Reporter
 * File: js/driver/driverIncidentReporter.js
 * 
 * Provides on-the-road incident logging modal for flat tires, mechanical breakdowns,
 * road accidents, medical emergencies, and heavy traffic blockages.
 */

class DriverIncidentReporter {
    static openModal(busId) {
        window.modalManager.open({
            title: '⚠️ Report Incident / Road Breakdown',
            content: `
                <form id="driver-incident-form">
                    <div class="form-group mb-3">
                        <label class="form-label font-weight-bold">Incident Category</label>
                        <select class="form-control" name="incident_type" required>
                            <option value="Mechanical Breakdown">Mechanical / Engine Breakdown</option>
                            <option value="Flat Tire">Flat Tire / Suspension</option>
                            <option value="Traffic Congestion">Severe Traffic Gridlock</option>
                            <option value="Road Accident">Road Accident / Collision</option>
                            <option value="Medical Emergency">Passenger Medical Emergency</option>
                            <option value="Security Issue">Passenger Dispute / Security</option>
                        </select>
                    </div>
                    <div class="form-group mb-3">
                        <label class="form-label font-weight-bold">Severity Level</label>
                        <select class="form-control" name="severity">
                            <option value="Low">Low (Informational)</option>
                            <option value="Medium" selected>Medium (Requires Attention)</option>
                            <option value="High">High (Immediate Assistance)</option>
                            <option value="Critical">Critical (Vehicle Stalled)</option>
                        </select>
                    </div>
                    <div class="form-group mb-3">
                        <label class="form-label font-weight-bold">Description & Location Landmark</label>
                        <textarea class="form-control" name="description" rows="3" placeholder="Describe the issue, nearest stop or highway junction..." required></textarea>
                    </div>
                </form>
            `,
            confirmText: 'Submit to Dispatcher',
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#driver-incident-form');
                const type = form.querySelector('select[name="incident_type"]').value;
                const severity = form.querySelector('select[name="severity"]').value;
                const desc = form.querySelector('textarea[name="description"]').value.trim();

                if (!desc) {
                    window.toastManager.warning('Please provide a brief description of the incident.');
                    return false;
                }

                try {
                    await window.incidentService.reportIncident(busId, `${type} Reported by Driver`, desc, type, severity);
                    window.toastManager.success('Incident transmitted to Dispatch Command Center.');
                    return true;
                } catch (e) {
                    window.toastManager.error(`Failed to submit incident: ${e.message}`);
                    return false;
                }
            }
        });
    }
}

// Global Export
window.DriverIncidentReporter = DriverIncidentReporter;
