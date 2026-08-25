"""
CityBus Enterprise Platform - GTFS-Fares V2 Specification Exporter
File: backend/services/interoperability/gtfs_fares_v2_builder.py

Builds GTFS-Fares V2 data specification compliant files (MobilityData extension):
- fare_products.txt (product_id, amount, currency)
- fare_leg_rules.txt (network_id, from_area_id, to_area_id, fare_product_id)
- fare_transfer_rules.txt (from_leg_group_id, to_leg_group_id, transfer_count, duration_limit_type)
"""

from typing import List, Dict, Any


class GTFSFaresV2Builder:
    @staticmethod
    def generate_fares_v2_dataset(fare_products: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Generates CSV text contents for GTFS-Fares V2 files.
        """
        # 1. fare_products.txt
        fare_products_csv = ["fare_product_id,fare_product_name,amount,currency"]
        for p in fare_products:
            fare_products_csv.append(f"{p['id']},{p['name']},{p['amount']:.2f},INR")

        # 2. fare_leg_rules.txt
        fare_leg_rules_csv = ["leg_group_id,network_id,from_area_id,to_area_id,fare_product_id"]
        for p in fare_products:
            fare_leg_rules_csv.append(f"LG_{p['id']},VIJAYAWADA_NETWORK,ZONE_ALL,ZONE_ALL,{p['id']}")

        # 3. fare_transfer_rules.txt
        fare_transfer_rules_csv = [
            "from_leg_group_id,to_leg_group_id,transfer_count,duration_limit,duration_limit_type,fare_transfer_type,fare_product_id",
            "LG_STAGE_CARRIAGE,LG_STAGE_CARRIAGE,1,3600,1,0,PROD_FREE_TRANSFER"
        ]

        return {
            'fare_products.txt': "\n".join(fare_products_csv),
            'fare_leg_rules.txt': "\n".join(fare_leg_rules_csv),
            'fare_transfer_rules.txt': "\n".join(fare_transfer_rules_csv)
        }
