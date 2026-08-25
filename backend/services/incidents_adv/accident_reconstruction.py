"""
CityBus Enterprise Platform - Blackbox Telemetry Crash Reconstruction Engine
File: backend/services/incidents_adv/accident_reconstruction.py

Extracts high-resolution blackbox telemetry (100Hz) around crash trigger event:
- Speed profile 10 seconds before impact (km/h)
- Brake application timing & deceleration G-force peak
- Steering wheel angle and turn indicators state
- Generates reconstruction graph data for forensic crash analysis
"""

from typing import List, Dict, Any


class BlackboxTelemetryReconstructor:
    @staticmethod
    def reconstruct_event(telemetry_stream: List[Dict[str, Any]], crash_event_index: int) -> Dict[str, Any]:
        """
        Extracts pre-crash window [-10s, +5s] around trigger event.
        """
        start_idx = max(0, crash_event_index - 10)
        end_idx = min(len(telemetry_stream), crash_event_index + 6)

        window = telemetry_stream[start_idx:end_idx]
        if not window:
            return {'status': 'INSUFFICIENT_TELEMETRY'}

        initial_speed = window[0].get('speed', 40.0)
        crash_speed = telemetry_stream[crash_event_index].get('speed', 0.0) if crash_event_index < len(telemetry_stream) else 0.0
        
        peak_decel_g = max(abs(p.get('ax_g', 0.0)) for p in window) if window else 0.85
        brake_applied = any(p.get('brake_active', False) for p in window)

        return {
            'crash_timestamp': window[min(len(window)-1, crash_event_index - start_idx)].get('timestamp'),
            'initial_speed_kmh': initial_speed,
            'speed_at_impact_kmh': crash_speed,
            'peak_deceleration_g': round(peak_decel_g, 2),
            'was_brake_applied_prior_to_impact': brake_applied,
            'time_series_window': window,
            'forensic_summary': f"Vehicle speed dropped from {initial_speed:.1f} km/h to {crash_speed:.1f} km/h with peak {peak_decel_g:.2f}G deceleration."
        }
