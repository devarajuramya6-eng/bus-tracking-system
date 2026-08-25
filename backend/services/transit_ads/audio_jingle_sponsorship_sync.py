"""
CityBus Enterprise Platform - Sponsored Audio Station Announcement Jingle Sync
File: backend/services/transit_ads/audio_jingle_sponsorship_sync.py

Appends non-intrusive 3-second sponsored commercial tags after station announcements:
- Official Announcement: "Next Stop: Benz Circle"
- Sponsored Tail: "...presented by Trendset Mall, Vijayawada's Premier Shopping Hub"
- Respects passenger peace: Max 1 sponsored tag every 4 stops
"""

from typing import Dict, Any


class AudioJingleSponsorshipSync:
    SPONSORSHIPS = {
        'Benz Circle': {'sponsor': 'Trendset Mall', 'tag_en': 'Presented by Trendset Mall.', 'tag_te': 'ట్రెండ్‌సెట్ మాల్ సమర్పణ.'},
        'Gannavaram Airport': {'sponsor': 'Hotel Novotel', 'tag_en': 'Stay refreshed at Novotel Vijayawada.', 'tag_te': 'హోటల్ నోవోటెల్ లో ఆహ్లాదకరమైన బస.'}
    }

    @staticmethod
    def get_sponsored_audio_tail(stop_name: str, stops_since_last_sponsor: int) -> Dict[str, Any]:
        """
        Determines whether to append sponsored sponsor audio tag.
        """
        is_frequency_allowed = stops_since_last_sponsor >= 3
        sponsor_data = AudioJingleSponsorshipSync.SPONSORSHIPS.get(stop_name)

        if sponsor_data and is_frequency_allowed:
            return {
                'stop_name': stop_name,
                'sponsor_name': sponsor_data['sponsor'],
                'tag_english': sponsor_data['tag_en'],
                'tag_telugu': sponsor_data['tag_te'],
                'audio_duration_seconds': 3.0,
                'is_sponsored': True
            }

        return {
            'stop_name': stop_name,
            'is_sponsored': False,
            'reason': 'INTERVAL_THROTTLED' if sponsor_data else 'NO_ACTIVE_SPONSOR_FOR_STOP'
        }
