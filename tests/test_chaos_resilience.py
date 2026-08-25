"""
CityBus Enterprise Platform - Chaos Resilience & Disaster Recovery Tests
File: tests/test_chaos_resilience.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.chaos_resilience.bridge_submersion_rerouter import BridgeClosureRerouter
from services.chaos_resilience.depot_grid_blackout_failover import DepotBlackoutFailoverEngine
from services.chaos_resilience.cell_tower_outage_mesh import CellOutageMeshRelay


class TestChaosResilience(unittest.TestCase):
    def test_bridge_flood_submersion_detour(self):
        eval_flood = BridgeClosureRerouter.evaluate_water_level("BRG_PRAKASAM_BARRAGE", current_water_level_m=13.2) # > 12.5m
        self.assertTrue(eval_flood['is_bridge_closed'])
        self.assertEqual(eval_flood['emergency_action'], 'ACTIVATE_EMERGENCY_DETOUR_PLAN')
        self.assertGreater(eval_flood['additional_detour_km'], 0.0)

    def test_depot_grid_blackout_failover(self):
        failover = DepotBlackoutFailoverEngine.trigger_grid_blackout_protocol(
            depot_name="Main Autonagar Depot",
            grid_voltage_v=0.0, # Zero volts
            active_ev_buses_charging=12
        )
        self.assertTrue(failover['is_grid_blackout_active'])
        self.assertEqual(failover['backup_power_state'], 'DIESEL_GENSET_ONLINE_500KVA')
        self.assertEqual(failover['status'], 'EMERGENCY_ISLAND_MICROGRID_MODE')

    def test_cell_tower_outage_mesh_relay(self):
        hop1 = CellOutageMeshRelay.relay_telemetry_frame("AP16-001", hops=1, has_active_4g_uplink=False)
        self.assertFalse(hop1['is_telemetry_delivered'])
        self.assertIn('BROADCAST_TO_NEIGHBOR_V2V_MESH', hop1['mesh_action'])

        hop_gateway = CellOutageMeshRelay.relay_telemetry_frame("AP16-002", hops=2, has_active_4g_uplink=True)
        self.assertTrue(hop_gateway['is_telemetry_delivered'])
        self.assertEqual(hop_gateway['mesh_action'], 'UPLINK_DIRECT_TO_CLOUD')


if __name__ == '__main__':
    unittest.main()
