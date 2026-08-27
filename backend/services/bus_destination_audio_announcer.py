from typing import Dict, List, Any

class BusDestinationAudioAnnouncer:
    """Generates trilingual exterior speaker announcements for waiting platform passengers."""

    @staticmethod
    def get_exterior_announcement(route_number: str, destination_name: str) -> Dict[str, Any]:
        clean_route = route_number.upper()
        return {
            "route_number": clean_route,
            "destination": destination_name,
            "audio_transcripts": {
                "english": f"Route {clean_route} to {destination_name}. Boarding now.",
                "telugu": f"రూట్ {clean_route} {destination_name} వైపు వెళ్ళును.",
                "hindi": f"मार्ग {clean_route} {destination_name} के लिए।"
            },
            "exterior_speaker_chime": "CHIME_HIGH_PITCH_BEEP",
            "volume_decibels": 75
        }
