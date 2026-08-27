"""
CityBus Enterprise Platform - On-Board CCTV & AI Passenger Safety Service
File: backend/services/cctv_passenger_safety_service.py

Monitors on-bus IP security camera streams (4 cameras per vehicle: Driver, Front Door, Saloon, Rear Door):
- Edge AI baggage unattended object detection
- Emergency SOS panic button linkage with live video clip upload to police command
- Passenger safety compliance flags
"""

from typing import Dict, List, Any, Optional


class CCTVPassengerSafetyService:
    """Manages on-board CCTV surveillance streams and AI incident detection triggers."""

    @staticmethod
    def get_bus_camera_streams(bus_id: int) -> Dict[str, Any]:
        """Returns RTSP / HLS video stream feeds for security control room."""
        return {
            "bus_id": bus_id,
            "cameras": [
                {"id": f"CAM-{bus_id}-01", "location": "Driver Cockpit & Forward Road View", "stream_url": f"rtsp://cctv.citybus.transit/live/bus_{bus_id}_cam1", "status": "ONLINE", "fps": 25},
                {"id": f"CAM-{bus_id}-02", "location": "Passenger Saloon Cabin Forward", "stream_url": f"rtsp://cctv.citybus.transit/live/bus_{bus_id}_cam2", "status": "ONLINE", "fps": 25},
                {"id": f"CAM-{bus_id}-03", "location": "Passenger Saloon Cabin Rear", "stream_url": f"rtsp://cctv.citybus.transit/live/bus_{bus_id}_cam3", "status": "ONLINE", "fps": 25},
                {"id": f"CAM-{bus_id}-04", "location": "Rear Exit Step Door", "stream_url": f"rtsp://cctv.citybus.transit/live/bus_{bus_id}_cam4", "status": "ONLINE", "fps": 25}
            ],
            "storage_nvr_status": "RECORDING_LOCAL_AND_CLOUD_SYNC",
            "dvr_storage_days_remaining": 30
        }
