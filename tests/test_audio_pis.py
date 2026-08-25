"""
CityBus Enterprise Platform - Audio PIS & Acoustic Synthesis Tests
File: tests/test_audio_pis.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.audio_pis.telugu_phoneme_tts_synthesizer import TeluguAudioTTSSynthesizer
from services.audio_pis.ambient_noise_adaptive_volume import AmbientNoiseAdaptiveVolume
from services.audio_pis.emergency_audio_chime_generator import EmergencyAudioChimeGenerator


class TestAudioPIS(unittest.TestCase):
    def test_telugu_ssml_generation(self):
        ssml = TeluguAudioTTSSynthesizer.generate_next_stop_ssml(
            stop_name_en="Benz Circle",
            stop_name_te="బెంజ్ సర్కిల్",
            interchange_routes="Route 5K & Route 10"
        )
        self.assertIn('బెంజ్ సర్కిల్', ssml['ssml_telugu'])
        self.assertIn('Benz Circle', ssml['ssml_english'])
        self.assertTrue(ssml['interchange_available'])

    def test_ambient_noise_adaptive_volume(self):
        vol = AmbientNoiseAdaptiveVolume.calculate_speaker_volume(cabin_ambient_dba=74.0)
        self.assertGreaterEqual(vol['target_pa_output_dba'], 80.0)
        self.assertEqual(vol['acoustic_mode'], 'HIGH_NOISE_BOOST')

    def test_emergency_audio_chimes(self):
        chime = EmergencyAudioChimeGenerator.get_chime_config('DOOR_CLOSING')
        self.assertEqual(len(chime['frequencies_hz']), 2)
        self.assertEqual(chime['frequencies_hz'][0], 880)


if __name__ == '__main__':
    unittest.main()
