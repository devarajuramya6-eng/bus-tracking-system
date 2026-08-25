"""
CityBus Enterprise Platform - Spare Part Supersession & Interchangeability Graph
File: backend/services/maintenance_erp/part_supersession_graph.py

Traces spare parts supersession trees and OEM cross-references:
- Direct part replacement (e.g. Old Oil Filter ➔ Upgraded Spin-on Cartridge)
- Cross-compatibility matching (Tata, Ashok Leyland, WABCO, Bosch, Knorr-Bremse)
"""

from typing import Dict, Any, List, Optional


class PartSupersessionGraph:
    SUPERSESSION_MAP = {
        'FLT-OIL-001': 'FLT-OIL-002',
        'FLT-OIL-002': 'FLT-OIL-003-HD',
        'BRK-PAD-FRONT-A': 'BRK-PAD-FRONT-REV-B'
    }

    CROSS_REFERENCES = {
        'BRK-PAD-FRONT-REV-B': ['WABCO-421355', 'KNORR-K001532'],
        'FLT-OIL-003-HD': ['BOSCH-F002891', 'MANN-WD940']
    }

    @staticmethod
    def get_latest_superseded_part(original_part_number: str) -> Dict[str, Any]:
        """
        Walks the supersession chain to find latest active SKU.
        """
        curr = original_part_number
        chain = [curr]

        while curr in PartSupersessionGraph.SUPERSESSION_MAP:
            curr = PartSupersessionGraph.SUPERSESSION_MAP[curr]
            chain.append(curr)

        cross_refs = PartSupersessionGraph.CROSS_REFERENCES.get(curr, [])

        return {
            'requested_part': original_part_number,
            'latest_active_part': curr,
            'supersession_chain': chain,
            'is_superseded': len(chain) > 1,
            'oem_interchangeable_skus': cross_refs
        }
