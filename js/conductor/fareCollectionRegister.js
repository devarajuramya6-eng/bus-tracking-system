/**
 * CityBus Enterprise Platform - Conductor Fare Collection & Shift POS Register
 * File: js/conductor/fareCollectionRegister.js
 * 
 * Manages physical cash fare transactions, printed receipt slips,
 * concession discount buttons, and end-of-route fare box handovers.
 */

class FareCollectionRegisterController {
    constructor() {
        this.transactions = [];
        this.totalCash = 0.0;
        this.concessionDiscountsTotal = 0.0;
    }

    issueTicket(stageFrom, stageTo, fareAmount, concessionType = 'General') {
        const txnId = `CASH-${Date.now().toString().slice(-6)}`;
        const txn = {
            txn_id: txnId,
            from: stageFrom,
            to: stageTo,
            fare: fareAmount,
            concession: concessionType,
            timestamp: new Date().toLocaleTimeString()
        };

        this.transactions.unshift(txn);
        this.totalCash += fareAmount;

        if (concessionType === 'Student') this.concessionDiscountsTotal += (fareAmount * 0.5);
        else if (concessionType === 'Senior') this.concessionDiscountsTotal += (fareAmount * 0.3);

        this.renderRegisterUI();
        window.toastManager.success(`Ticket #${txnId} issued for ₹${fareAmount.toFixed(2)}`);
        return txn;
    }

    renderRegisterUI() {
        const container = document.getElementById('fare-register-history');
        if (!container) return;

        container.innerHTML = `
            <div class="register-summary-bar d-flex justify-content-between p-2 mb-3 bg-light rounded">
                <div><strong>Shift Total:</strong> ₹${this.totalCash.toFixed(2)}</div>
                <div><strong>Tickets:</strong> ${this.transactions.length}</div>
                <div><strong>Subsidies:</strong> ₹${this.concessionDiscountsTotal.toFixed(2)}</div>
            </div>
            <div class="transaction-receipts-list">
                ${this.transactions.slice(0, 8).map(t => `
                    <div class="txn-item-row d-flex justify-content-between align-items-center p-2 border-bottom">
                        <div>
                            <strong>#${t.txn_id}</strong>
                            <small class="text-muted d-block">${t.from} → ${t.to} (${t.concession})</small>
                        </div>
                        <div class="text-end">
                            <span class="badge badge-success">₹${t.fare.toFixed(2)}</span>
                            <small class="text-muted d-block">${t.timestamp}</small>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Global Export
window.fareCollectionRegister = new FareCollectionRegisterController();
