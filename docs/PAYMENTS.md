# CityBus Enterprise Platform - Payment Gateway & Ledger Architecture

## 1. Razorpay Payment Flow
1. **Order Creation (`POST /api/v1/payments/order`)**:
   - Creates a unique `order_id` (e.g. `order_rzp_94k20x`).
   - Returns client configuration (`key_id`, `amount`, `currency`).
2. **Checkout Presentation**:
   - Renders instant payment modal supporting UPI, QR, Debit/Credit Card, and NetBanking.
3. **Digital Signature Verification (`POST /api/v1/payments/verify`)**:
   - Computes HMAC-SHA256 signature over `${order_id}|${payment_id}` using `RAZORPAY_KEY_SECRET`.
   - Compares securely via `hmac.compare_digest`.
   - On success, updates `payments.status = "SUCCESS"` and confirms ticket pass validity.

## 2. Refund Workflow
- Initiated via `/api/v1/tickets/{id}/refund` or passenger wallet.
- Records refund ledger transaction with audit logging.
