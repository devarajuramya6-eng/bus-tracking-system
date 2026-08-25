/**
 * CityBus Enterprise Platform - Web Speech Audio Announcement Engine
 * File: js/core/voice.js
 * 
 * Provides automated text-to-speech voice announcements for:
 * - Upcoming bus stop arrivals
 * - Route transfer announcements
 * - Driver turn-by-turn auditory alerts
 * - Emergency SOS panic broadcast alarms
 */

class CityBusVoiceEngine {
  constructor() {
    this.synth = window.speechSynthesis || null;
    this.enabled = localStorage.getItem('citybus_voice_enabled') !== 'false';
    this.rate = 0.95;
    this.pitch = 1.0;
    this.volume = 1.0;
    this.selectedVoice = null;
    this.initVoices();
  }

  initVoices() {
    if (!this.synth) return;
    const loadVoices = () => {
      const voices = this.synth.getVoices();
      // Try finding Indian English or standard natural voice
      this.selectedVoice = voices.find(v => v.lang === 'en-IN') ||
                           voices.find(v => v.lang.startsWith('en')) ||
                           voices[0];
    };
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = loadVoices;
    }
    loadVoices();
  }

  toggleVoice(state) {
    this.enabled = state !== undefined ? state : !this.enabled;
    localStorage.setItem('citybus_voice_enabled', this.enabled);
    if (!this.enabled && this.synth) {
      this.synth.cancel();
    }
    return this.enabled;
  }

  speak(text, priority = 'normal') {
    if (!this.enabled || !this.synth) return;

    if (priority === 'emergency') {
      this.synth.cancel(); // Interrupt existing speeches
    }

    const utterance = new SpeechSynthesisUtterance(text);
    if (this.selectedVoice) utterance.voice = this.selectedVoice;
    utterance.rate = priority === 'emergency' ? 1.1 : this.rate;
    utterance.pitch = priority === 'emergency' ? 1.2 : this.pitch;
    utterance.volume = this.volume;

    this.synth.speak(utterance);
  }

  announceStopArrival(stopName, routeNumber) {
    this.speak(`Next stop: ${stopName}. Route ${routeNumber}. Please prepare to alight.`);
  }

  announceEmergency(busNumber, reason) {
    this.speak(`Attention all passengers and control. Emergency SOS reported on vehicle ${busNumber}. ${reason}`, 'emergency');
  }

  announceDelay(routeNumber, delayMinutes) {
    this.speak(`Service alert. Route ${routeNumber} is delayed by approximately ${delayMinutes} minutes due to traffic.`);
  }
}

// Global Singleton Export
window.CityBusVoice = new CityBusVoiceEngine();
