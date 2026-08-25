"""
CityBus Enterprise Platform - Incident Delay Cascade Ripple Propagator
File: backend/services/digital_twin/incident_cascade_propagator.py

Predicts upstream ripple effects and timetable delay cascades:
- Calculates downstream bus bunching risk and headway irregularity
- Models delay propagation speed across multi-line interchange corridors
- Recommends proactive short-turning / headway regulation holds
"""

from typing import List, Dict, Any


class IncidentCascadePropagator:
    @staticmethod
    def propagate_delay(primary_incident_delay_min: float, upstream_buses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates compounded delay on following buses.
        """
        propagated_buses = []
        decay_factor = 0.82 # 18% damping per headway gap

        current_delay = primary_incident_delay_min

        for b in upstream_buses:
            current_delay *= decay_factor
            propagated_buses.append({
                'bus_number': b.get('bus_number'),
                'route_number': b.get('route_number'),
                'scheduled_headway_min': b.get('headway_min', 10.0),
                'predicted_delay_min': round(current_delay, 1),
                'bunching_risk': 'HIGH' if current_delay > 6.0 else ('MEDIUM' if current_delay > 3.0 else 'LOW')
            })

        return {
            'initial_incident_delay_min': round(primary_incident_delay_min, 1),
            'affected_upstream_vehicles': len(upstream_buses),
            'cascade_schedule': propagated_buses,
            'intervention_recommended': primary_incident_delay_min >= 10.0
        }
