"""
CityBus Enterprise Platform - Cellular Tower Outage P2P Mesh Relay
File: backend/services/chaos_resilience/cell_tower_outage_mesh.py

Enables ad-hoc multi-hop telemetry forwarding during 4G/5G cellular outages:
- Vehicle-to-Vehicle (V2V) Wi-Fi Direct & Bluetooth LE short-range mesh (Range: 300m)
- Multi-hop store-and-forward telemetry relay until reaching gateway bus with satellite/fibre uplink
"""

from typing import List, Dict, Any


class CellOutageMeshRelay:
    MAX_HOPS = 4

    @staticmethod
    def relay_telemetry_frame(origin_bus_number: str, hops: int,
                              has_active_4g_uplink: bool) -> Dict[str, Any]:
        """
        Determines mesh routing decision.
        """
        if has_active_4g_uplink:
            action = 'UPLINK_DIRECT_TO_CLOUD'
            is_delivered = True
        elif hops < CellOutageMeshRelay.MAX_HOPS:
            action = f"BROADCAST_TO_NEIGHBOR_V2V_MESH (Hop {hops + 1})"
            is_delivered = False
        else:
            action = 'STORE_IN_FLASH_BUFFER_WAIT_FOR_DEPOT_WIFI'
            is_delivered = False

        return {
            'origin_bus': origin_bus_number,
            'current_hop_count': hops,
            'has_direct_cellular_uplink': has_active_4g_uplink,
            'mesh_action': action,
            'is_telemetry_delivered': is_delivered
        }
