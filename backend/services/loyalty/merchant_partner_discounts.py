"""
CityBus Enterprise Platform - Retail Merchant Partner Transit Discount Offers
File: backend/services/loyalty/merchant_partner_discounts.py

Provides redeemable local partner merchant discount vouchers for transit ticket holders:
- 15% off at PNBS Terminal Food Court & Coffee Shops
- 10% discount on groceries at Vijayawada Supermarkets upon showing valid bus pass
"""

from typing import List, Dict, Any


class MerchantDiscountPartnerEngine:
    PARTNERS = [
        {'id': 'MERCH-01', 'name': 'PNBS Central Express Food Court', 'category': 'Dining', 'offer': '15% Off All Meals', 'coupon_code': 'CITYBUSFOOD15', 'min_bill_inr': 150.0},
        {'id': 'MERCH-02', 'name': 'Benz Circle Metro Books & Stationers', 'category': 'Retail', 'offer': '10% Off Stationery & Books', 'coupon_code': 'BUSREAD10', 'min_bill_inr': 200.0},
        {'id': 'MERCH-03', 'name': 'Amaravati Organics Grocery Hub', 'category': 'Groceries', 'offer': '₹50 Off on orders over ₹500', 'coupon_code': 'GREENBUS50', 'min_bill_inr': 500.0}
    ]

    @staticmethod
    def get_available_offers(ticket_number: str) -> List[Dict[str, Any]]:
        return MerchantDiscountPartnerEngine.PARTNERS
