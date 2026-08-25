"""
CityBus Enterprise Platform - Ambient Noise Adaptive PA Speaker Volume
File: backend/services/audio_pis/ambient_noise_adaptive_volume.py

Dynamically modulates in-cabin loudspeaker volume based on ambient decibel levels (dBA):
- Quiet Cabin (55 dBA) ➔ 68 dBA PA output (Level 4/10)
- Highway Speed / High Traffic (75 dBA) ➔ 84 dBA PA output (Level 8/10)
- Maintains comfortable Signal-to-Noise Ratio (+9 dB above cabin noise)
"""

from typing import Dict, Any


class AmbientNoiseAdaptiveVolume:
    MIN_SPEAKER_GAIN_DB = 60.0
    MAX_SPEAKER_GAIN_DB = 88.0
    TARGET_SNR_OFFSET_DB = 9.0

    @staticmethod
    def calculate_speaker_volume(cabin_ambient_dba: float) -> Dict[str, Any]:
        """
        Computes dynamic volume level (0 to 100%) and gain in decibels.
        """
        target_gain_dba = min(
            AmbientNoiseAdaptiveVolume.MAX_SPEAKER_GAIN_DB,
            max(AmbientNoiseAdaptiveVolume.MIN_SPEAKER_GAIN_DB, cabin_ambient_dba + AmbientNoiseAdaptiveVolume.TARGET_SNR_OFFSET_DB)
        )

        vol_pct = ((target_gain_dba - AmbientNoiseAdaptiveVolume.MIN_SPEAKER_GAIN_DB) / 
                   (AmbientNoiseAdaptiveVolume.MAX_SPEAKER_GAIN_DB - AmbientNoiseAdaptiveVolume.MIN_SPEAKER_GAIN_DB)) * 100.0

        return {
            'ambient_noise_dba': round(cabin_ambient_dba, 1),
            'target_pa_output_dba': round(target_gain_dba, 1),
            'master_volume_percentage': int(round(vol_pct)),
            'acoustic_mode': 'HIGH_NOISE_BOOST' if cabin_ambient_dba >= 72.0 else 'NORMAL_ACOUSTICS'
        }
