/**
 * CityBus Enterprise Platform - Digital Ticketing & QR Service
 * File: js/services/ticketService.js
 * 
 * Handles electronic ticket purchases, dynamic QR validation barcodes,
 * ticket wallet storage, fare calculation, and conductor scan verification.
 */

class TicketService {
    async purchaseTicket(routeId, originStop, destStop, passengerCount = 1, paymentMethod = 'UPI') {
        const body = {
            route_id: routeId,
            origin_stop: originStop,
            destination_stop: destStop,
            passenger_count: passengerCount,
            payment_method: paymentMethod
        };
        const response = await window.apiClient.post('/api/v1/tickets/purchase', body);
        return response;
    }

    async getMyTickets() {
        const response = await window.apiClient.get('/api/v1/tickets/my-tickets');
        if (response && response.success) {
            return response.tickets || [];
        }
        return [];
    }

    async getTicketById(ticketId) {
        const response = await window.apiClient.get(`/api/v1/tickets/${ticketId}`);
        if (response && response.success) {
            return response.ticket;
        }
        throw new Error(response.message || `Ticket ${ticketId} not found`);
    }

    async validateQRCode(qrPayload, busId = null) {
        const body = {
            qr_payload: qrPayload,
            bus_id: busId
        };
        const response = await window.apiClient.post('/api/v1/tickets/validate', body);
        return response;
    }

    async cancelTicket(ticketId) {
        return window.apiClient.post(`/api/v1/tickets/${ticketId}/cancel`);
    }
}

// Global Export
window.ticketService = new TicketService();
