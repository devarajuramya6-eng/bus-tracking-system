/**
 * CityBus Enterprise Platform - Driver Turn-by-Turn Navigation HUD
 * File: js/driver/driverTurnByTurn.js
 * 
 * Renders next maneuver instructions, compass direction, distance countdown,
 * upcoming stop alerts, and audio speech synthesis chimes.
 */

class DriverTurnByTurnHUD {
    constructor(containerId = 'driver-turn-hud') {
        this.container = document.getElementById(containerId);
        this.currentStep = 1;
        this.maneuvers = [];
        this.nextStopName = 'Approaching Stop';
        this.distanceToNextManeuver = 350; // meters
    }

    setManeuvers(maneuverList) {
        this.maneuvers = maneuverList || [];
        this.currentStep = 1;
        this.render();
    }

    updateProximity(distanceMeters, speedKmh) {
        this.distanceToNextManeuver = distanceMeters;
        const distEl = this.container?.querySelector('.maneuver-dist');
        if (distEl) distEl.textContent = `${Math.round(distanceMeters)}m`;

        // Voice announcement when within 100 meters
        if (distanceMeters <= 100 && !this.announcedCurrent) {
            this.speakCurrentInstruction();
            this.announcedCurrent = true;
        } else if (distanceMeters > 150) {
            this.announcedCurrent = false;
        }
    }

    speakCurrentInstruction() {
        const curr = this.maneuvers[this.currentStep - 1];
        if (curr && 'speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(curr.instruction);
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }
    }

    nextManeuver() {
        if (this.currentStep < this.maneuvers.length) {
            this.currentStep++;
            this.render();
            this.speakCurrentInstruction();
        }
    }

    render() {
        if (!this.container) return;
        const curr = this.maneuvers[this.currentStep - 1] || {
            instruction: 'Follow corridor path',
            type: 'STRAIGHT',
            bearing: 0
        };

        const iconMap = {
            'DEPART': 'fa-play',
            'TURN_RIGHT': 'fa-arrow-right',
            'TURN_LEFT': 'fa-arrow-left',
            'STRAIGHT': 'fa-arrow-up',
            'ARRIVE': 'fa-flag-checkered'
        };

        const iconClass = iconMap[curr.type] || 'fa-arrow-up';

        this.container.innerHTML = `
            <div class="turn-by-turn-card">
                <div class="maneuver-icon-wrap"><i class="fas ${iconClass}"></i></div>
                <div class="maneuver-details">
                    <div class="maneuver-dist">${Math.round(this.distanceToNextManeuver)}m</div>
                    <div class="maneuver-text">${curr.instruction}</div>
                    <div class="maneuver-step-meta">Step ${this.currentStep} of ${this.maneuvers.length || 1} • Bearing: ${curr.bearing}°</div>
                </div>
                <button class="btn btn-sm btn-outline-primary next-step-btn" title="Next Maneuver"><i class="fas fa-step-forward"></i></button>
            </div>
        `;

        const nextBtn = this.container.querySelector('.next-step-btn');
        if (nextBtn) {
            nextBtn.onclick = () => this.nextManeuver();
        }
    }
}

// Global Export
window.driverTurnByTurn = new DriverTurnByTurnHUD();
