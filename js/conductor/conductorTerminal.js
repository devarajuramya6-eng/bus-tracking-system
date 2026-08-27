/**
 * CityBus Enterprise Platform - Conductor QR Validation & Remittance Terminal
 * File: js/conductor/conductorTerminal.js
 * 
 * Provides camera QR ticket scanning, manual ticket verification, cash fare sales,
 * occupancy counting, and end-of-shift remittance calculations.
 */

class ConductorTerminalController {
    constructor() {
        this.scannedCount = 0;
        this.cashCollected = 0.0;
        this.occupancy = 12;
        this.assignedBus = { id: 1, bus_number: 'AP16-001', route: 'PNBS ⇄ Guntur NTR Terminal' };
    }

    async init() {
        if (!window.authService.requireAuth(['conductor', 'admin', 'super_admin'])) {
            return;
        }

        const user = window.authService.getUser();
        document.getElementById('conductor-name-display')?.replaceChildren(document.createTextNode(user.name || 'Conductor'));

        this.bindEvents();
    }

    bindEvents() {
        const validateBtn = document.getElementById('validate-ticket-btn');
        if (validateBtn) {
            validateBtn.onclick = () => this.handleManualValidation();
        }

        const issueCashBtn = document.getElementById('issue-cash-ticket-btn');
        if (issueCashBtn) {
            issueCashBtn.onclick = () => this.handleIssueCashTicket();
        }

        const boardPaxBtn = document.getElementById('board-passenger-btn');
        if (boardPaxBtn) {
            boardPaxBtn.onclick = () => {
                this.occupancy = Math.min(55, this.occupancy + 1);
                this.updateCounters();
            };
        }

        const alightPaxBtn = document.getElementById('alight-passenger-btn');
        if (alightPaxBtn) {
            alightPaxBtn.onclick = () => {
                this.occupancy = Math.max(0, this.occupancy - 1);
                this.updateCounters();
            };
        }
    }

    async handleManualValidation() {
        const input = document.getElementById('qr-payload-input');
        if (!input || !input.value.trim()) {
            window.toastManager.warning('Please enter or scan a valid QR ticket code.');
            return;
        }

        const payload = input.value.trim();
        try {
            const res = await window.ticketService.validateQRCode(payload, this.assignedBus.id);
            if (res.success && res.status === 'VALID') {
                this.scannedCount++;
                this.updateCounters();
                this.displayScanResult(true, `VALID TICKET #${res.ticket.ticket_number}`, `Route: ${res.ticket.origin_stop} → ${res.ticket.destination_stop}`);
                window.toastManager.success(`Ticket #${res.ticket.ticket_number} Verified!`);
                input.value = '';
            } else {
                this.displayScanResult(false, 'INVALID OR ALREADY USED TICKET', res.message || 'Ticket verification failed');
                window.toastManager.error(res.message || 'Invalid Ticket');
            }
        } catch (e) {
            this.displayScanResult(false, 'VERIFICATION ERROR', e.message);
            window.toastManager.error(e.message);
        }
    }

    async handleIssueCashTicket() {
        const fareSelect = document.getElementById('cash-fare-select');
        const fare = parseFloat(fareSelect ? fareSelect.value : 20.0);

        this.cashCollected += fare;
        this.scannedCount++;
        this.updateCounters();

        window.toastManager.success(`Cash ticket issued for ₹${fare}. Total cash: ₹${this.cashCollected}`);
    }

    displayScanResult(isValid, title, message) {
        const resultCard = document.getElementById('scan-result-card');
        if (!resultCard) return;

        resultCard.className = `scan-result-card ${isValid ? 'valid' : 'invalid'}`;
        resultCard.innerHTML = `
            <div class="result-icon"><i class="fas ${isValid ? 'fa-check-circle' : 'fa-times-circle'}"></i></div>
            <div class="result-details">
                <h4>${title}</h4>
                <p>${message}</p>
                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        resultCard.style.display = 'flex';
    }

    updateCounters() {
        document.getElementById('scanned-pax-count')?.replaceChildren(document.createTextNode(`${this.scannedCount}`));
        document.getElementById('cash-collected-total')?.replaceChildren(document.createTextNode(`₹${this.cashCollected.toFixed(2)}`));
        document.getElementById('current-bus-occupancy')?.replaceChildren(document.createTextNode(`${this.occupancy}`));
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('conductor-terminal-root')) {
        window.conductorTerminal = new ConductorTerminalController();
        window.conductorTerminal.init();
    }
});
