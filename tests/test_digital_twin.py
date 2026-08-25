"""
CityBus Enterprise Platform - Digital Twin & Network Dynamics Tests
File: tests/test_digital_twin.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.digital_twin.corridor_physics_twin import CorridorPhysicsTwin
from services.digital_twin.macro_transit_flow_model import MacroscopicFlowModel
from services.digital_twin.incident_cascade_propagator import IncidentCascadePropagator


class TestDigitalTwin(unittest.TestCase):
    def test_corridor_physics_simulation_step(self):
        twin = CorridorPhysicsTwin.simulate_vehicle_step(
            mass_kg=14000.0,
            current_speed_kmh=40.0,
            road_grade_pct=2.0,
            is_wet_road=False
        )
        self.assertEqual(twin['status'], 'TWIN_STATE_SYNCHRONIZED')
        self.assertGreater(twin['total_tractive_force_n'], 2000.0)
        self.assertGreater(twin['instantaneous_power_demand_kw'], 20.0)

    def test_macroscopic_flow_model_congested(self):
        flow = MacroscopicFlowModel.evaluate_corridor_flow(current_density_veh_km=60.0) # > 45 k_crit
        self.assertTrue(flow['is_in_hyper_congestion'])
        self.assertLess(flow['space_mean_speed_kmh'], 30.0)

    def test_incident_cascade_propagation(self):
        upstream = [
            {'bus_number': 'AP16-002', 'route_number': '27A', 'headway_min': 10.0},
            {'bus_number': 'AP16-003', 'route_number': '27A', 'headway_min': 10.0}
        ]
        cascade = IncidentCascadePropagator.propagate_delay(primary_incident_delay_min=15.0, upstream_buses=upstream)
        self.assertEqual(len(cascade['cascade_schedule']), 2)
        self.assertTrue(cascade['intervention_recommended'])
        self.assertEqual(cascade['cascade_schedule'][0]['bunching_risk'], 'HIGH')


if __name__ == '__main__':
    unittest.main()
