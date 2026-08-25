"""
CityBus Enterprise Platform - Route Rebalancing & Elastic Fleet Tests
File: tests/test_route_rebalancing.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.route_rebalancing.elastic_corridor_rebalancing import ElasticCorridorRebalancer
from services.route_rebalancing.crowdsourced_feeder_synthesizer import CrowdsourcedFeederSynthesizer
from services.route_rebalancing.deadhead_turnaround_minimizer import ShortTurnLoopOptimizer


class TestRouteRebalancing(unittest.TestCase):
    def test_elastic_corridor_fleet_rebalancing(self):
        telemetry = [
            {'route_number': '27A', 'load_factor': 0.95}, # Overcrowded
            {'route_number': '12', 'load_factor': 0.20}   # Underutilized
        ]
        res = ElasticCorridorRebalancer.calculate_fleet_rebalance(telemetry)
        self.assertEqual(res['overcrowded_corridors_count'], 1)
        self.assertEqual(res['underutilized_corridors_count'], 1)
        self.assertEqual(len(res['recommended_reallocations']), 1)
        self.assertEqual(res['recommended_reallocations'][0]['from_route'], '12')
        self.assertEqual(res['recommended_reallocations'][0]['to_route'], '27A')

    def test_crowdsourced_feeder_synthesis_viable(self):
        reqs = [{'pax_id': i} for i in range(20)] # 20 requests >= 15 threshold
        synth = CrowdsourcedFeederSynthesizer.synthesize_feeder_line(
            demand_requests=reqs,
            origin_area="Tadigadapa",
            destination_hub="PNBS"
        )
        self.assertTrue(synth['is_economically_viable'])
        self.assertEqual(synth['status'], 'PROPOSE_ON_DEMAND_MICRO_SHUTTLE')

    def test_short_turn_loop_optimization(self):
        stops = ['Stop1', 'Stop2', 'Stop3', 'Benz Circle', 'Stop5', 'Stop6']
        pax_profile = [50, 50, 45, 12, 8, 4] # Large drop at Benz Circle
        opt = ShortTurnLoopOptimizer.evaluate_short_turn_opportunity(
            full_route_stops=stops,
            stop_passenger_on_board=pax_profile,
            peak_max_passengers=50
        )
        self.assertTrue(opt['is_short_turn_recommended'])
        self.assertEqual(opt['optimal_turnaround_stop'], 'Benz Circle')


if __name__ == '__main__':
    unittest.main()
