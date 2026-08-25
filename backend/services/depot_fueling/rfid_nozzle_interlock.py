"""
CityBus Enterprise Platform - RFID Fuel Nozzle Collar Interlock Authorizer
File: backend/services/depot_fueling/rfid_nozzle_interlock.py

Controls automatic RFID fuel dispensing nozzles (PetroPoint / Orpak standard):
- Nozzle antenna authenticates RFID transponder tag installed on bus fuel tank collar
- Solenoid valve unlocks ONLY while nozzle is seated inside authorized vehicle tank neck
- Instantly closes solenoid valve if nozzle is withdrawn (Anti-Fuel-Pilferage Protection)
"""

from typing import Dict, Any


class RFIDFuelNozzleInterlock:
    AUTHORIZED_FLEET_TAGS = {
        'RFID_AP16_001': {'bus_number': 'AP16-001', 'fuel_type': 'HSD_DIESEL', 'tank_capacity_l': 250.0},
        'RFID_AP16_002': {'bus_number': 'AP16-002', 'fuel_type': 'HSD_DIESEL', 'tank_capacity_l': 250.0},
        'RFID_AP16_003': {'bus_number': 'AP16-003', 'fuel_type': 'HSD_DIESEL', 'tank_capacity_l': 250.0}
    }

    @staticmethod
    def verify_nozzle_insertion(scanned_rfid_tag: str, is_nozzle_seated: bool) -> Dict[str, Any]:
        """
        Authorizes fuel dispensing solenoid valve.
        """
        fleet_data = RFIDFuelNozzleInterlock.AUTHORIZED_FLEET_TAGS.get(scanned_rfid_tag)
        is_tag_authorized = fleet_data is not None
        is_safe_to_dispense = is_tag_authorized and is_nozzle_seated

        if is_safe_to_dispense:
            valve_state = 'SOLENOID_VALVE_OPEN_DISPENSE'
            status = 'AUTHORIZED_VEHICLE_FUELING_ACTIVE'
        elif not is_tag_authorized:
            valve_state = 'SOLENOID_LOCKED_UNAUTHORIZED_TAG'
            status = 'UNAUTHORIZED_RFID_TAG_REJECTED'
        else:
            valve_state = 'SOLENOID_CLOSED_NOZZLE_WITHDRAWN'
            status = 'SAFETY_CUTOFF_NOZZLE_NOT_SEATED'

        return {
            'scanned_rfid_tag': scanned_rfid_tag,
            'bus_number': fleet_data['bus_number'] if fleet_data else 'UNKNOWN',
            'fuel_type': fleet_data['fuel_type'] if fleet_data else 'NONE',
            'is_nozzle_properly_seated': is_nozzle_seated,
            'solenoid_valve_state': valve_state,
            'dispense_authorized': is_safe_to_dispense,
            'status': status
        }
