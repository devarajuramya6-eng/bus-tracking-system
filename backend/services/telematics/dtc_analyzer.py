"""
CityBus Enterprise Platform - Diagnostic Trouble Code (DTC) Analyzer
File: backend/services/telematics/dtc_analyzer.py

Parses and diagnoses SAE J2012 / ISO 15031 OBD diagnostic fault codes:
- Powertrain (P), Chassis (C), Body (B), Network Communication (U)
- Severity classification and automated preventive maintenance work order generation
"""

from typing import Dict, Any, List, Optional
from models import db, MaintenanceWorkOrder


class DTCAnalyzer:
    DTC_DATABASE = {
        'P0117': {'system': 'Cooling', 'desc': 'Engine Coolant Temperature Sensor 1 Circuit Low', 'severity': 'Medium', 'action': 'Inspect coolant sensor wiring harness'},
        'P0217': {'system': 'Cooling', 'desc': 'Engine Overtemperature Condition', 'severity': 'Critical', 'action': 'Immediate vehicle halt. Inspect radiator and water pump'},
        'P0300': {'system': 'Ignition/Fuel', 'desc': 'Random/Multiple Cylinder Misfire Detected', 'severity': 'High', 'action': 'Check fuel injectors and compression'},
        'P0500': {'system': 'Speed Sensor', 'desc': 'Vehicle Speed Sensor "A" Malfunction', 'severity': 'Medium', 'action': 'Inspect transmission speed sensor'},
        'C0035': {'system': 'Brakes/ABS', 'desc': 'Left Front Wheel Speed Sensor Malfunction', 'severity': 'Critical', 'action': 'Inspect ABS sensor and tone ring'},
        'U0100': {'system': 'CAN Network', 'desc': 'Lost Communication With ECM/PCM', 'severity': 'Critical', 'action': 'Check CAN bus termination resistor and wiring'},
        'P20EE': {'system': 'Emissions', 'desc': 'SCR NOx Catalyst Efficiency Below Threshold', 'severity': 'Medium', 'action': 'Check DEF dosing unit and catalyst'}
    }

    @staticmethod
    def analyze_fault_code(dtc_code: str, bus_id: int) -> Dict[str, Any]:
        """
        Analyzes a DTC fault code and creates automated workshop logs.
        """
        code = dtc_code.upper().strip()
        info = DTCAnalyzer.DTC_DATABASE.get(code, {
            'system': 'General Subsystem',
            'desc': f'Unclassified Diagnostic Code {code}',
            'severity': 'Low',
            'action': 'Run general diagnostic scan'
        })

        return {
            'dtc_code': code,
            'bus_id': bus_id,
            'subsystem': info['system'],
            'description': info['desc'],
            'severity': info['severity'],
            'recommended_action': info['action'],
            'requires_immediate_halt': info['severity'] == 'Critical'
        }
