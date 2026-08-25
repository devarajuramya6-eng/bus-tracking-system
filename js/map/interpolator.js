/**
 * CityBus Enterprise Platform - Vehicle GPS & Heading Interpolator
 * File: js/map/interpolator.js
 * 
 * Smooths out incoming telemetry pings so bus markers glide along roadways
 * without sudden jumps, animating latitude, longitude, speed, and heading.
 */

class VehicleInterpolator {
  constructor() {
    this.vehicles = new Map(); // busId -> { currentLat, currentLng, targetLat, targetLng, currentHeading, targetHeading, animStartTime, animDuration }
    this.animationFrameId = null;
    this.isLoopRunning = false;
  }

  /**
   * Updates or registers target coordinate for a vehicle
   */
  updateVehicleTarget(busId, targetLat, targetLng, heading = 0, speed = 35, durationMs = 2800) {
    let v = this.vehicles.get(busId);
    const now = performance.now();

    if (!v) {
      v = {
        busId,
        currentLat: targetLat,
        currentLng: targetLng,
        targetLat: targetLat,
        targetLng: targetLng,
        currentHeading: heading,
        targetHeading: heading,
        speed: speed,
        animStartTime: now,
        animDuration: durationMs
      };
      this.vehicles.set(busId, v);
    } else {
      // Set current position to current interpolated frame before setting new target
      v.currentLat = this.calculateCurrent(v.currentLat, v.targetLat, v.animStartTime, v.animDuration, now);
      v.currentLng = this.calculateCurrent(v.currentLng, v.targetLng, v.animStartTime, v.animDuration, now);
      
      v.targetLat = targetLat;
      v.targetLng = targetLng;
      v.targetHeading = heading || this.calculateHeading(v.currentLat, v.currentLng, targetLat, targetLng);
      v.speed = speed;
      v.animStartTime = now;
      v.animDuration = durationMs;
    }

    if (!this.isLoopRunning) {
      this.startInterpolationLoop();
    }
  }

  /**
   * Computes heading angle (degrees 0-360) between two coordinates
   */
  calculateHeading(lat1, lon1, lat2, lon2) {
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const y = Math.sin(dLon) * Math.cos(lat2 * Math.PI / 180);
    const x = Math.cos(lat1 * Math.PI / 180) * Math.sin(lat2 * Math.PI / 180) -
              Math.sin(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.cos(dLon);
    const brng = Math.atan2(y, x) * 180 / Math.PI;
    return (brng + 360) % 360;
  }

  calculateCurrent(start, end, startTime, duration, now) {
    const elapsed = now - startTime;
    if (elapsed >= duration) return end;
    const progress = Math.min(1, Math.max(0, elapsed / duration));
    // Smooth cubic easing
    const eased = progress < 0.5 ? 4 * progress * progress * progress : 1 - Math.pow(-2 * progress + 2, 3) / 2;
    return start + (end - start) * eased;
  }

  /**
   * Main requestAnimationFrame tick loop
   */
  startInterpolationLoop() {
    this.isLoopRunning = true;

    const tick = (now) => {
      let activeAnimations = false;

      this.vehicles.forEach((v, busId) => {
        const lat = this.calculateCurrent(v.currentLat, v.targetLat, v.animStartTime, v.animDuration, now);
        const lng = this.calculateCurrent(v.currentLng, v.targetLng, v.animStartTime, v.animDuration, now);
        
        // Notify marker layer
        window.dispatchEvent(new CustomEvent('citybus:marker-interpolated', {
          detail: {
            busId,
            lat,
            lng,
            heading: v.targetHeading,
            speed: v.speed
          }
        }));

        if (now - v.animStartTime < v.animDuration) {
          activeAnimations = true;
        }
      });

      if (this.isLoopRunning) {
        this.animationFrameId = requestAnimationFrame(tick);
      }
    };

    this.animationFrameId = requestAnimationFrame(tick);
  }

  stop() {
    this.isLoopRunning = false;
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }
}

// Global Export
window.CityBusInterpolator = new VehicleInterpolator();
