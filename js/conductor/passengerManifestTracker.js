/**
 * CityBus Enterprise Platform - Passenger Manifest & Boarding Tally Tracker
 * File: js/conductor/passengerManifestTracker.js
 * 
 * Tracks stop-by-stop passenger boardings, alightings, occupancy percentage,
 * and flags station overcrowding risks to dispatch.
 */

class PassengerManifestTrackerController {
    constructor() {
        this.manifest = [];
        this.currentOccupancy = 15;
        this.busCapacity = 45;
    }

    recordStopActivity(stopName, boardedCount, alightedCount) {
        this.currentOccupancy = Math.max(0, Math.min(this.busCapacity + 10, this.currentOccupancy + boardedCount - alightedCount));

        const entry = {
            stop: stopName,
            boarded: boardedCount,
            alighted: alightedCount,
            occupancy_after: this.currentOccupancy,
            load_factor: Math.round((this.currentOccupancy / this.busCapacity) * 100),
            timestamp: new Date().toLocaleTimeString()
        };

        this.manifest.push(entry);
        this.renderManifest();

        if (entry.load_factor >= 95) {
            window.toastManager.warning(`Bus is at capacity (${this.currentOccupancy}/${this.busCapacity} pax). Next stop may have pass-bys.`);
        }
    }

    renderManifest() {
        const container = document.getElementById('passenger-manifest-table');
        if (!container) return;

        container.innerHTML = `
            <table class="table table-sm table-hover">
                <thead>
                    <tr>
                        <th>Station Stop</th>
                        <th>Boarded</th>
                        <th>Alighted</th>
                        <th>Load %</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    ${this.manifest.map(m => `
                        <tr>
                            <td><strong>${m.stop}</strong></td>
                            <td class="text-success">+${m.boarded}</td>
                            <td class="text-danger">-${m.alighted}</td>
                            <td>
                                <div class="progress" style="height: 14px;">
                                    <div class="progress-bar ${m.load_factor > 85 ? 'bg-danger' : 'bg-primary'}" style="width: ${Math.min(100, m.load_factor)}%">
                                        ${m.load_factor}%
                                    </div>
                                </div>
                            </td>
                            <td><small class="text-muted">${m.timestamp}</small></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
}

// Global Export
window.passengerManifestTracker = new PassengerManifestTrackerController();
