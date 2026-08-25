# CityBus Enterprise Platform - Security & Threat Model

## 1. Authentication & Session Security
- **JWT Token Architecture**: Dual-token strategy with short-lived access tokens (8h) and long-lived refresh tokens (30d). Tokens are signed with HMAC-SHA256 and validate strict standard claims (`sub`, `iat`, `exp`, `role`).
- **Password Security**: Passwords are salted and hashed with SHA-256 / bcrypt preventing rainbow table attacks.
- **Role-Based Authorization Matrix**: RBAC decorators enforce fine-grained endpoint protection across all 9 roles.

## 2. API Protection & Cryptography
- **Cryptographic QR Signing**: Digital transit passes are signed with HMAC-SHA256, protecting against forgery and tampering.
- **Payment Verification**: Razorpay sandbox webhooks and client callbacks compute HMAC-SHA256 signatures over `${order_id}|${payment_id}` using constant-time string comparison (`hmac.compare_digest`) to prevent timing attacks.
- **Rate Limiting & CORS**: All API routes restrict cross-origin access and throttle abusive request floods.
- **Audit Logging**: All security actions (`USER_LOGIN`, `TICKET_ISSUED`, `TICKET_SCANNED`, `EMERGENCY_SOS`) are logged to immutable `audit_logs` records.
