/**
 * CityBus Enterprise Platform - Digital Pass & QR Wallet Logic
 * File: js/passenger/digital_ticket.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const ticketIdParam = urlParams.get('ticket_id') || 'TCK-2608-0042';

  const ticketNumberEl = document.getElementById('ticket-number-display');
  const routeEl = document.getElementById('ticket-route-display');
  const fareEl = document.getElementById('ticket-fare-display');
  const statusEl = document.getElementById('ticket-status-badge');
  const expiryEl = document.getElementById('ticket-expiry-display');
  const qrContainer = document.getElementById('ticket-qr-code');
  const refundBtn = document.getElementById('ticket-refund-btn');

  // Load ticket details
  const ticketData = {
    number: ticketIdParam,
    origin: 'Vijayawada PNBS',
    destination: 'Guntur NTR Bus Terminal',
    route: 'Route 27A (Express)',
    fare: '₹45.00',
    status: 'VALID',
    passengers: 1,
    issuedAt: 'Today, 10:15 AM',
    expiresAt: 'Today, 04:15 PM'
  };

  if (ticketNumberEl) ticketNumberEl.textContent = ticketData.number;
  if (routeEl) routeEl.textContent = `${ticketData.origin} → ${ticketData.destination}`;
  if (fareEl) fareEl.textContent = ticketData.fare;
  if (expiryEl) expiryEl.textContent = ticketData.expiresAt;

  if (statusEl) {
    statusEl.className = 'badge badge-success';
    statusEl.innerHTML = '<span class="badge-dot"></span> VALID PASS';
  }

  // Generate High-Contrast Visual QR representation
  if (qrContainer) {
    qrContainer.innerHTML = `
      <div style="background: #FFFFFF; padding: 1.25rem; border-radius: var(--cb-radius-lg); display: inline-block; box-shadow: var(--cb-shadow-md); border: 2px dashed var(--cb-border-strong);">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(`CITYBUS|${ticketData.number}|PASSENGER|45`)}" alt="Ticket QR Code" style="width: 180px; height: 180px; display: block;" onerror="this.onerror=null; this.src='https://chart.googleapis.com/chart?cht=qr&chs=180x180&chl=${encodeURIComponent(ticketData.number)}'">
      </div>
      <div style="font-size: 0.75rem; color: var(--cb-text-muted); margin-top: 0.5rem;">
        Scan with conductor terminal or show to bus crew
      </div>
    `;
  }

  // Refund Handler
  if (refundBtn) {
    refundBtn.onclick = () => {
      if (window.CityBusModal) {
        window.CityBusModal.confirm({
          title: 'Request Ticket Refund',
          message: `Are you sure you want to cancel Ticket <strong>${ticketData.number}</strong> and initiate a refund of ${ticketData.fare}?`,
          confirmText: 'Confirm Cancellation & Refund',
          confirmType: 'danger',
          onConfirm: () => {
            if (statusEl) {
              statusEl.className = 'badge badge-danger';
              statusEl.innerHTML = '<span class="badge-dot"></span> REFUNDED';
            }
            refundBtn.disabled = true;
            if (window.showToast) window.showToast(`Refund of ${ticketData.fare} processed to original payment method.`, 'success');
          }
        });
      }
    };
  }
});
