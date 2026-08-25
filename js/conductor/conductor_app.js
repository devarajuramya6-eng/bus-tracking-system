/**
 * CityBus Enterprise Platform - Conductor Terminal & QR Scanner
 * File: js/conductor/conductor_app.js
 */

document.addEventListener('DOMContentLoaded', () => {
  let passengerCount = 32;
  let totalValidated = 48;
  let isScanning = false;

  const countDisplay = document.getElementById('conductor-passenger-count');
  const validatedDisplay = document.getElementById('conductor-validated-count');
  const scanBtn = document.getElementById('start-scanner-btn');
  const manualForm = document.getElementById('manual-ticket-form');
  const scanResultCard = document.getElementById('scan-result-card');

  function updateDisplays() {
    if (countDisplay) countDisplay.textContent = passengerCount;
    if (validatedDisplay) validatedDisplay.textContent = totalValidated;
  }

  // Headcount Increment / Decrement
  const incBtn = document.getElementById('inc-passengers-btn');
  const decBtn = document.getElementById('dec-passengers-btn');
  if (incBtn) incBtn.onclick = () => { passengerCount++; updateDisplays(); };
  if (decBtn) decBtn.onclick = () => { passengerCount = Math.max(0, passengerCount - 1); updateDisplays(); };

  // Manual Ticket ID Validation
  if (manualForm) {
    manualForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('manual-ticket-id');
      const ticketId = input ? input.value.trim() : '';
      if (!ticketId) return;

      validateTicketPayload(ticketId);
      input.value = '';
    });
  }

  // QR Scanner Trigger
  if (scanBtn) {
    scanBtn.onclick = () => {
      isScanning = !isScanning;
      if (isScanning) {
        scanBtn.innerHTML = '<i class="fa-solid fa-camera anim-bounce"></i> Scanner Active (Simulating Lens)...';
        scanBtn.className = 'btn btn-danger btn-block';
        if (window.showToast) window.showToast('Camera active. Scanning for passenger QR ticket...', 'info');

        // Simulate successful optical barcode scan after 2 seconds
        setTimeout(() => {
          if (isScanning) {
            validateTicketPayload('TCK-2608-0042');
            isScanning = false;
            scanBtn.innerHTML = '<i class="fa-solid fa-camera"></i> Start Camera QR Scan';
            scanBtn.className = 'btn btn-primary btn-block';
          }
        }, 2200);
      } else {
        scanBtn.innerHTML = '<i class="fa-solid fa-camera"></i> Start Camera QR Scan';
        scanBtn.className = 'btn btn-primary btn-block';
      }
    };
  }

  async function validateTicketPayload(payload) {
    let result = {
      isValid: true,
      status: 'VALID',
      ticketNumber: payload,
      route: 'Route 27A (PNBS → Guntur)',
      fare: '₹45.00',
      passengers: 1
    };

    // Call Backend / Mock API
    if (window.CityBusAPI) {
      try {
        const res = await window.CityBusAPI.validateTicket(payload);
        if (res) {
          result.isValid = res.success;
          result.status = res.validation_status || (res.success ? 'VALID' : 'INVALID');
          if (res.ticket) {
            result.ticketNumber = res.ticket.ticket_number;
            result.fare = `₹${res.ticket.fare_amount}`;
          }
        }
      } catch (err) {
        result.isValid = false;
        result.status = 'NOT_FOUND';
      }
    }

    renderScanResult(result);
  }

  function renderScanResult(res) {
    if (!scanResultCard) return;

    let alertClass = 'alert-success';
    let iconClass = 'fa-circle-check';
    let title = 'TICKET VALID & CONFIRMED';

    if (res.status === 'ALREADY_USED') {
      alertClass = 'alert-warning';
      iconClass = 'fa-triangle-exclamation';
      title = 'WARNING: TICKET ALREADY USED';
    } else if (res.status === 'EXPIRED') {
      alertClass = 'alert-danger';
      iconClass = 'fa-circle-xmark';
      title = 'INVALID: PASS EXPIRED';
    } else if (!res.isValid) {
      alertClass = 'alert-danger';
      iconClass = 'fa-circle-xmark';
      title = 'INVALID PASS / NOT FOUND';
    }

    if (res.isValid) {
      totalValidated++;
      updateDisplays();
      if (window.CityBusNotifications) {
        window.CityBusNotifications.playChime();
      }
    }

    scanResultCard.style.display = 'block';
    scanResultCard.className = `card anim-scale-in`;
    scanResultCard.innerHTML = `
      <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.8rem; color: var(--cb-status-${res.isValid ? 'success' : 'danger'}); margin-bottom: 0.5rem;">
          <i class="fa-solid ${iconClass}"></i>
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--cb-text-primary); margin-bottom: 0.25rem;">
          ${title}
        </h3>
        <div style="font-size: 0.85rem; color: var(--cb-text-muted); margin-bottom: 1.25rem;">
          Pass: <strong>${res.ticketNumber}</strong> • ${res.route}
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; background: var(--cb-bg-subtle); padding: 0.75rem; border-radius: var(--cb-radius-md); text-align: left; font-size: 0.85rem;">
          <div><span style="color: var(--cb-text-muted);">Fare Paid:</span> <strong>${res.fare}</strong></div>
          <div><span style="color: var(--cb-text-muted);">Passengers:</span> <strong>${res.passengers}</strong></div>
        </div>

        <button class="btn btn-outline btn-sm btn-block" style="margin-top: 1rem;" onclick="document.getElementById('scan-result-card').style.display='none'">
          <i class="fa-solid fa-check"></i> Done (Ready for Next Scan)
        </button>
      </div>
    `;
  }

  updateDisplays();
});
