/**
 * CityBus Enterprise Platform - Ticket Booking & Checkout Flow
 * File: js/passenger/ticketing.js
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('ticket-booking-form');
  const countInput = document.getElementById('ticket-passengers');
  const concessionSelect = document.getElementById('ticket-concession');
  const fareDisplay = document.getElementById('summary-total-fare');

  // Pre-fill from query params
  const urlParams = new URLSearchParams(window.location.search);
  const fromParam = urlParams.get('from');
  const toParam = urlParams.get('to');
  const fareParam = urlParams.get('fare');

  if (fromParam) document.getElementById('ticket-origin').value = fromParam;
  if (toParam) document.getElementById('ticket-destination').value = toParam;

  function updateFareSummary() {
    const baseFare = fareParam ? parseFloat(fareParam) : 30.0;
    const count = parseInt(countInput ? countInput.value : 1) || 1;
    const concession = concessionSelect ? concessionSelect.value : 'general';

    let discount = 0.0;
    if (concession === 'student') discount = 0.5;
    if (concession === 'senior') discount = 0.3;

    const unitFare = Math.max(10, Math.round(baseFare * (1.0 - discount)));
    const total = unitFare * count;

    if (fareDisplay) {
      fareDisplay.textContent = `₹${total}`;
    }
    return total;
  }

  if (countInput) countInput.addEventListener('input', updateFareSummary);
  if (concessionSelect) concessionSelect.addEventListener('change', updateFareSummary);
  updateFareSummary();

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const origin = document.getElementById('ticket-origin').value.trim();
      const destination = document.getElementById('ticket-destination').value.trim();
      const count = parseInt(countInput.value) || 1;
      const totalAmount = updateFareSummary();

      if (!origin || !destination) {
        if (window.showToast) window.showToast('Please select valid origin and destination stops', 'warning');
        return;
      }

      // 1. Open Razorpay Test Payment Modal
      if (window.CityBusModal) {
        window.CityBusModal.dynamicModal({
          title: 'Complete Payment (Razorpay Sandbox)',
          bodyHtml: `
            <div style="text-align: center; padding: 1rem 0;">
              <div style="font-size: 2.5rem; color: var(--cb-brand-primary); margin-bottom: 0.5rem;">
                <i class="fa-solid fa-credit-card"></i>
              </div>
              <div style="font-size: 1.5rem; font-weight: 800; color: var(--cb-text-primary); margin-bottom: 0.25rem;">
                ₹${totalAmount}.00
              </div>
              <div style="font-size: 0.85rem; color: var(--cb-text-muted); margin-bottom: 1.5rem;">
                CityBus Smart Mobility • ${origin} → ${destination} (${count} Passenger)
              </div>

              <div style="display: flex; flex-direction: column; gap: 0.75rem; text-align: left;">
                <label style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; border: 1px solid var(--cb-border-default); border-radius: var(--cb-radius-md); cursor: pointer;">
                  <input type="radio" name="pay_mode" value="upi" checked>
                  <i class="fa-solid fa-mobile-screen" style="color: var(--cb-brand-primary); font-size: 1.1rem;"></i>
                  <div>
                    <div style="font-weight: 700; font-size: 0.9rem;">Instant UPI / QR</div>
                    <div style="font-size: 0.75rem; color: var(--cb-text-muted);">GPay, PhonePe, Paytm, BHIM</div>
                  </div>
                </label>

                <label style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; border: 1px solid var(--cb-border-default); border-radius: var(--cb-radius-md); cursor: pointer;">
                  <input type="radio" name="pay_mode" value="card">
                  <i class="fa-solid fa-credit-card" style="color: var(--cb-status-success); font-size: 1.1rem;"></i>
                  <div>
                    <div style="font-weight: 700; font-size: 0.9rem;">Debit / Credit Card</div>
                    <div style="font-size: 0.75rem; color: var(--cb-text-muted);">Visa, MasterCard, RuPay</div>
                  </div>
                </label>
              </div>
            </div>
          `,
          footerHtml: `
            <button class="btn btn-outline" data-dismiss="modal">Cancel</button>
            <button class="btn btn-success" id="pay-confirm-btn">
              <i class="fa-solid fa-lock"></i> Pay ₹${totalAmount}
            </button>
          `,
          onOpen: (modal) => {
            modal.querySelector('#pay-confirm-btn').onclick = async () => {
              const payBtn = modal.querySelector('#pay-confirm-btn');
              payBtn.disabled = true;
              payBtn.innerHTML = '<i class="fa-solid fa-circle-notch anim-spin"></i> Processing...';

              // Call Backend / Mock API to create ticket and record payment
              try {
                let ticket = null;
                if (window.CityBusAPI) {
                  const res = await window.CityBusAPI.createTicket({
                    origin,
                    destination,
                    fare_amount: totalAmount,
                    passenger_count: count,
                    route_id: 1
                  });
                  ticket = res.ticket;
                }

                if (window.CityBusModal) window.CityBusModal.close(modal);
                if (window.showToast) window.showToast('Payment successful! Ticket issued.', 'success');

                setTimeout(() => {
                  window.location.href = `my-tickets.html?ticket_id=${ticket ? ticket.ticket_number : 'TCK-DEMO'}`;
                }, 600);

              } catch (err) {
                payBtn.disabled = false;
                payBtn.innerHTML = '<i class="fa-solid fa-lock"></i> Pay';
                if (window.showToast) window.showToast('Payment processing failed. Please retry.', 'danger');
              }
            };
          }
        });
      }
    });
  }
});
