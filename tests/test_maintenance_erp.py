"""
CityBus Enterprise Platform - Maintenance ERP & Workshop Job Cards Tests
File: tests/test_maintenance_erp.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.maintenance_erp.work_order_state_machine import WorkOrderStateMachine
from services.maintenance_erp.mechanic_labor_productivity import MechanicLaborProductivity
from services.maintenance_erp.part_supersession_graph import PartSupersessionGraph


class TestMaintenanceERP(unittest.TestCase):
    def test_work_order_state_transitions(self):
        t1 = WorkOrderStateMachine.transition_state('DRAFT', 'APPROVED')
        self.assertTrue(t1['success'])
        self.assertEqual(t1['new_state'], 'APPROVED')

        t_bad = WorkOrderStateMachine.transition_state('DRAFT', 'CLOSED')
        self.assertFalse(t_bad['success'])

        t_qc = WorkOrderStateMachine.transition_state('QC_INSPECTION_PENDING', 'CLOSED', supervisor_id=105)
        self.assertTrue(t_qc['success'])
        self.assertTrue(t_qc['is_vehicle_roadworthy'])

    def test_mechanic_labor_efficiency(self):
        eff = MechanicLaborProductivity.calculate_technician_efficiency(
            technician_id=12,
            job_type='BRAKE_PAD_REPLACEMENT_ALL',
            actual_hours=2.0 # SRT is 2.5h (125% efficient)
        )
        self.assertEqual(eff['productivity_rating'], 'EXCEEDS_BENCHMARK')
        self.assertEqual(eff['labor_efficiency_percentage'], 125.0)

    def test_part_supersession_chain(self):
        part = PartSupersessionGraph.get_latest_superseded_part('FLT-OIL-001')
        self.assertEqual(part['latest_active_part'], 'FLT-OIL-003-HD')
        self.assertTrue(part['is_superseded'])
        self.assertIn('BOSCH-F002891', part['oem_interchangeable_skus'])


if __name__ == '__main__':
    unittest.main()
