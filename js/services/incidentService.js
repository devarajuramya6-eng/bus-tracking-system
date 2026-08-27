/**
 * CityBus Enterprise Platform - Incident & SOS Service
 * File: js/services/incidentService.js
 * 
 * Handles panic alarms, emergency SOS triggers, road accident reporting,
 * dispatch incident triage, and resolution workflows.
 */

class IncidentService {
    async getAllIncidents(status = null, severity = null, page = 1, perPage = 20) {
        let endpoint = `/api/v1/incidents?page=${page}&per_page=${perPage}`;
        if (status) endpoint += `&status=${encodeURIComponent(status)}`;
        if (severity) endpoint += `&severity=${encodeURIComponent(severity)}`;

        const response = await window.apiClient.get(endpoint);
        return response;
    }

    async getIncidentById(incidentId) {
        const response = await window.apiClient.get(`/api/v1/incidents/${incidentId}`);
        if (response && response.success) {
            return response.incident;
        }
        throw new Error(response.message || `Incident ${incidentId} not found`);
    }

    async reportIncident(busId, title, description, incidentType = 'Breakdown', severity = 'Medium', latitude = null, longitude = null) {
        const body = {
            bus_id: busId,
            title,
            description,
            incident_type: incidentType,
            severity,
            latitude,
            longitude
        };
        return window.apiClient.post('/api/v1/incidents', body);
    }

    async triggerPanicSOS(busId, latitude = null, longitude = null, note = 'Emergency SOS Alert') {
        const body = {
            bus_id: busId,
            title: 'EMERGENCY PANIC SOS',
            description: note,
            incident_type: 'Emergency',
            severity: 'Critical',
            latitude,
            longitude
        };
        return window.apiClient.post('/api/v1/incidents', body);
    }

    async updateIncidentStatus(incidentId, status, resolutionNotes = '') {
        return window.apiClient.put(`/api/v1/incidents/${incidentId}`, {
            status,
            resolution_notes: resolutionNotes
        });
    }
}

// Global Export
window.incidentService = new IncidentService();
