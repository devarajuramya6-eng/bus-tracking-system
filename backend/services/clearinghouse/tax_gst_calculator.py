"""
CityBus Enterprise Platform - Indian GST Tax Allocation & Compliance Engine
File: backend/services/clearinghouse/tax_gst_calculator.py

Calculates statutory Goods & Services Tax (GST) according to transit classifications:
- Ordinary Non-AC Urban City Bus: 0% Exempt (SAC Code 996411)
- Electric AC Metro Deluxe: 5% GST with ITC restriction (SAC Code 996412 - CGST 2.5% + SGST 2.5%)
- Private Special Charters / Wedding Hires: 18% GST (CGST 9% + SGST 9%)
- Commercial Depot & Bus Advertising: 18% GST (SAC Code 998361)
"""

from typing import Dict, Any


class GSTTaxCalculator:
    SERVICE_TAX_SLABS = {
        'NON_AC_ORDINARY': {'rate': 0.0, 'sac': '996411', 'desc': 'Exempt Urban Passenger Transport'},
        'AC_ELECTRIC_DELUXE': {'rate': 0.05, 'sac': '996412', 'desc': 'Air Conditioned Stage Carriage Service'},
        'SPECIAL_CHARTER': {'rate': 0.18, 'sac': '996419', 'desc': 'Contract Carriage Passenger Charter'},
        'COMMERCIAL_ADVERTISING': {'rate': 0.18, 'sac': '998361', 'desc': 'Transit Media & Billboard Advertising'}
    }

    @staticmethod
    def calculate_gst(base_amount: float, service_type: str = 'AC_ELECTRIC_DELUXE') -> Dict[str, Any]:
        """
        Calculates CGST, SGST, and total invoice amount.
        """
        slab = GSTTaxCalculator.SERVICE_TAX_SLABS.get(service_type, GSTTaxCalculator.SERVICE_TAX_SLABS['AC_ELECTRIC_DELUXE'])
        rate = slab['rate']

        total_gst = round(base_amount * rate, 2)
        cgst = round(total_gst / 2.0, 2)
        sgst = round(total_gst - cgst, 2)
        total_invoice = round(base_amount + total_gst, 2)

        return {
            'service_type': service_type,
            'sac_code': slab['sac'],
            'description': slab['desc'],
            'base_amount_inr': round(base_amount, 2),
            'gst_rate_pct': int(rate * 100),
            'cgst_inr': cgst,
            'sgst_inr': sgst,
            'total_gst_inr': total_gst,
            'total_invoice_amount_inr': total_invoice
        }
