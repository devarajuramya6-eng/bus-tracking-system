/**
 * CityBus Enterprise Platform - Headway Regulation & Anti-Bunching Optimizer
 * File: js/dispatcher/headwayOptimizer.js
 * 
 * Prevents bus platooning / bunching by recommending dynamic holding times at stops
 * and adaptive corridor dispatch frequencies.
 */

class HeadwayOptimizerController {
    constructor() {
        this.targetHeadwayMinutes = 8.0; // Standard 8 minute interval
    }

    calculateHeadwayRecommendations(busesOnRoute) {
        if (!busesOnRoute || busesOnRoute.length < 2) return [];

        const recommendations = [];
        for (let i = 0; i < busesOnRoute.length - 1; i++) {
            const leadingBus = busesOnRoute[i];
            const trailingBus = busesOnRoute[i + 1];

            // Simulated headway gap
            const actualGapMinutes = Math.abs(leadingBus.id - trailingBus.id) * 3.5 + 4.0;
            const deviation = actualGapMinutes - this.targetHeadwayMinutes;

            let action = "MAINTAIN_PACE";
            let advisoryText = "Pacing optimal. Maintain current speed.";

            if (deviation < -3.0) {
                action = "HOLD_AT_NEXT_STOP";
                advisoryText = `Bus bunching detected! Hold trailing bus #${trailingBus.bus_number} for 90 seconds at next platform.`;
            } else if (deviation > 4.0) {
                action = "ACCELERATE_TRANSIT";
                advisoryText = `Excessive headway gap (+${deviation.toFixed(1)}m). Request bus #${trailingBus.bus_number} to expedite dwell times.`;
            }

            recommendations.push({
                leading_bus: leadingBus.bus_number,
                trailing_bus: trailingBus.bus_number,
                actual_headway_minutes: actualGapMinutes,
                target_headway_minutes: this.targetHeadwayMinutes,
                action,
                advisory: advisoryText
            });
        }

        return recommendations;
    }

    renderHeadwayDashboard(containerId, recommendations) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (recommendations.length === 0) {
            container.innerHTML = '<div class="text-success p-3 text-center"><i class="fas fa-check-circle"></i> Corridor headways are balanced within target intervals.</div>';
            return;
        }

        container.innerHTML = `
            <div class="headway-recommendations-list">
                ${recommendations.map(rec => `
                    <div class="headway-alert-box action-${rec.action.toLowerCase().replace(/_/g, '-')} mb-2 p-3 border rounded">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong>${rec.leading_bus} ⇄ ${rec.trailing_bus}</strong>
                            <span class="badge ${rec.action === 'MAINTAIN_PACE' ? 'badge-success' : 'badge-warning'}">${rec.action}</span>
                        </div>
                        <p class="small mb-1">${rec.advisory}</p>
                        <small class="text-muted">Current Gap: ${rec.actual_headway_minutes.toFixed(1)} min (Target: ${rec.target_headway_minutes} min)</small>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Global Export
window.headwayOptimizer = new HeadwayOptimizerController();
