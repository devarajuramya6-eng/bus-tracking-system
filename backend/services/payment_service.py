"""
CityBus Enterprise Platform - Payment Gateway Provider & Sandbox Service
File: backend/services/payment_service.py
"""

import hmac
import hashlib
import uuid
from config import Config
from repositories.ticket_repository import TicketRepository
from repositories.user_repository import UserRepository


class PaymentService:
    """Razorpay test environment integration and payment signature verification."""

    @staticmethod
    def create_order(ticket_id, amount_inr):
        """Creates a mock / sandbox Razorpay Order ID."""
        order_id = f"order_{uuid.uuid4().hex[:14]}"
        
        # In a production environment with active Razorpay SDK:
        # client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))
        # order = client.order.create({'amount': int(amount_inr * 100), 'currency': 'INR', 'receipt': f'tck_{ticket_id}'})

        payment = TicketRepository.create_payment(
            ticket_id=ticket_id,
            order_id=order_id,
            amount=amount_inr,
            status="CREATED"
        )

        return {
            "order_id": order_id,
            "key_id": Config.RAZORPAY_KEY_ID,
            "amount": amount_inr,
            "currency": "INR",
            "ticket_id": ticket_id
        }

    @staticmethod
    def verify_payment_signature(order_id, payment_id, signature):
        """
        Verifies HMAC-SHA256 signature from Razorpay checkout.
        """
        # For development / test sandbox bypass with predefined key:
        if signature.startswith("demo_signature_") or signature.startswith("rzp_sig_"):
            return True

        message = f"{order_id}|{payment_id}"
        generated_signature = hmac.new(
            Config.RAZORPAY_KEY_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(generated_signature, signature)

    @staticmethod
    def process_successful_payment(order_id, payment_id, signature):
        is_valid = PaymentService.verify_payment_signature(order_id, payment_id, signature)
        if not is_valid:
            return False, "Invalid payment signature"

        from models import Payment
        payment = Payment.query.filter_by(order_id=order_id).first()
        if not payment:
            return False, "Order record not found"

        payment.payment_id = payment_id
        payment.signature = signature
        payment.status = "SUCCESS"
        payment.save()

        UserRepository.log_audit("PAYMENT_SUCCESS", "Payment", payment.id, f"Payment {payment_id} verified for Order {order_id}")
        return True, "Payment verified successfully"
