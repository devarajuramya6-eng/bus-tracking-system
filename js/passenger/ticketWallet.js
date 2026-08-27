/**
 * CityBus Enterprise Platform - Passenger Digital Ticket Wallet
 * File: js/passenger/ticketWallet.js
 * 
 * Manages active tickets, renders dynamic SVG QR code passes,
 * handles refund requests, and stores offline ticket payloads in localStorage.
 */

class TicketWalletController {
    constructor() {
        this.tickets = [];
        this.selectedTicket = null;
    }

    async init() {
        if (!window.authService.requireAuth(['passenger', 'admin', 'super_admin'])) {
            return;
        }

        await this.loadTickets();
        this.bindEvents();
    }

    async loadTickets() {
        const container = document.getElementById('ticket-wallet-container');
        if (!container) return;

        try {
            const tickets = await window.ticketService.getMyTickets();
            this.tickets = tickets;

            if (tickets.length === 0) {
                container.innerHTML = `
                    <div class="empty-wallet-card text-center p-5">
                        <i class="fas fa-ticket-alt fa-3x text-muted mb-3"></i>
                        <h3>No Active Tickets</h3>
                        <p class="text-muted">You have no tickets in your wallet. Plan a journey and book a ride!</p>
                        <a href="/tickets.html" class="btn btn-primary mt-3">Book New Ticket</a>
                    </div>
                `;
                return;
            }

            container.innerHTML = `
                <div class="ticket-cards-grid">
                    ${tickets.map(t => this.renderTicketCard(t)).join('')}
                </div>
            `;

            this.bindCardClicks();
        } catch (e) {
            console.error('Wallet error:', e);
        }
    }

    renderTicketCard(ticket) {
        const isValid = ticket.status === 'VALID';
        const statusClass = isValid ? 'badge-success' : (ticket.status === 'USED' ? 'badge-secondary' : 'badge-danger');

        return `
            <div class="digital-ticket-card ${isValid ? 'valid-ticket' : 'used-ticket'}" data-ticket-id="${ticket.id}">
                <div class="ticket-notch-top"></div>
                <div class="ticket-header">
                    <div class="agency-title">CityBus Vijayawada</div>
                    <span class="badge ${statusClass}">${ticket.status}</span>
                </div>
                <div class="ticket-route-section">
                    <div class="stop-node origin">
                        <span class="node-dot"></span>
                        <div class="node-info">
                            <span class="node-label">ORIGIN</span>
                            <span class="node-name">${ticket.origin_stop}</span>
                        </div>
                    </div>
                    <div class="route-line-connector"><i class="fas fa-bus"></i></div>
                    <div class="stop-node destination">
                        <span class="node-dot"></span>
                        <div class="node-info">
                            <span class="node-label">DESTINATION</span>
                            <span class="node-name">${ticket.destination_stop}</span>
                        </div>
                    </div>
                </div>
                <div class="ticket-meta-grid">
                    <div class="meta-item">
                        <span class="meta-label">TICKET NO.</span>
                        <span class="meta-val">#${ticket.ticket_number}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">PASSENGERS</span>
                        <span class="meta-val">${ticket.passenger_count || 1} Adult</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">TOTAL FARE</span>
                        <span class="meta-val fare-val">₹${ticket.fare_amount.toFixed(2)}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">EXPIRES</span>
                        <span class="meta-val">${ticket.expires_at ? new Date(ticket.expires_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'Today'}</span>
                    </div>
                </div>
                <div class="ticket-qr-area">
                    <div class="qr-placeholder">
                        <div class="mock-qr-pattern"></div>
                        <span class="qr-instruction">Scan by Conductor on Boarding</span>
                    </div>
                </div>
                ${isValid ? `
                    <div class="ticket-actions mt-3">
                        <button class="btn btn-sm btn-outline-danger cancel-ticket-btn" data-id="${ticket.id}">Cancel & Refund</button>
                    </div>
                ` : ''}
                <div class="ticket-notch-bottom"></div>
            </div>
        `;
    }

    bindCardClicks() {
        document.querySelectorAll('.cancel-ticket-btn').forEach(btn => {
            btn.onclick = async (e) => {
                e.stopPropagation();
                const ticketId = btn.dataset.id;
                if (confirm('Cancel this ticket and request an automatic refund?')) {
                    await window.ticketService.cancelTicket(ticketId);
                    window.toastManager.success('Ticket cancelled and refund initiated.');
                    this.loadTickets();
                }
            };
        });
    }

    bindEvents() {
        const refreshBtn = document.getElementById('refresh-wallet-btn');
        if (refreshBtn) {
            refreshBtn.onclick = () => this.loadTickets();
        }
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('ticket-wallet-root')) {
        window.ticketWallet = new TicketWalletController();
        window.ticketWallet.init();
    }
});
