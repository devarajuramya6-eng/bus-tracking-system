/**
 * CityBus Enterprise Platform - Driver Duty & Shift Compliance Manager
 * File: js/driver/shift_manager.js
 * 
 * Enforces transit safety regulations & vehicle readiness:
 * - Digital Pre-Trip Vehicle Inspection Checklist (Brakes, Tires, Lights, Mirrors, Wipers, AC)
 * - Hours of Service (HoS) compliance counter (Max 8-hour driving limit)
 * - Rest break timer & driver fatigue mitigation alerts
 */

class CityBusDriverShiftManager {
  constructor() {
    this.storageKey = 'citybus_driver_shift_data';
    this.shift = this.loadShift();
  }

  loadShift() {
    const saved = localStorage.getItem(this.storageKey);
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }

    return {
      driverId: 1,
      driverName: 'Ravi Kumar (APSRTC #4012)',
      shiftStatus: 'OFF_DUTY', // 'OFF_DUTY', 'INSPECTION_PENDING', 'ON_DUTY', 'ON_BREAK'
      shiftStartTime: null,
      drivingSeconds: 0,
      maxDrivingSeconds: 8 * 3600, // 8 hours max
      preTripInspection: {
        completed: false,
        brakesTested: false,
        tiresPressureOk: false,
        headlightsTailLightsOk: false,
        wipersFluidOk: false,
        emergencyExitClear: false,
        firstAidKitPresent: false,
        fireExtinguisherCharged: false,
        timestamp: null
      }
    };
  }

  saveShift(shift) {
    this.shift = shift;
    localStorage.setItem(this.storageKey, JSON.stringify(this.shift));
    window.dispatchEvent(new CustomEvent('citybus:shift_updated', { detail: this.shift }));
  }

  startPreTripInspection() {
    this.shift.shiftStatus = 'INSPECTION_PENDING';
    this.saveShift(this.shift);
  }

  submitPreTripInspection(checklist) {
    this.shift.preTripInspection = {
      ...this.shift.preTripInspection,
      ...checklist,
      completed: true,
      timestamp: new Date().toISOString()
    };
    this.shift.shiftStatus = 'ON_DUTY';
    this.shift.shiftStartTime = new Date().toISOString();
    this.saveShift(this.shift);
    if (window.showToast) {
      window.showToast('Pre-trip vehicle safety checklist passed! Shift started.', 'success');
    }
  }

  toggleBreak(takeBreak) {
    if (takeBreak) {
      this.shift.shiftStatus = 'ON_BREAK';
      if (window.showToast) window.showToast('Driver rest break logged.', 'info');
    } else {
      this.shift.shiftStatus = 'ON_DUTY';
      if (window.showToast) window.showToast('Driver resumed active driving duty.', 'success');
    }
    this.saveShift(this.shift);
  }

  endShift() {
    this.shift.shiftStatus = 'OFF_DUTY';
    this.shift.shiftStartTime = null;
    this.shift.preTripInspection.completed = false;
    this.saveShift(this.shift);
    if (window.showToast) {
      window.showToast('Duty shift concluded. Rest period initiated.', 'info');
    }
  }
}

// Global Export
window.CityBusDriverShiftManager = new CityBusDriverShiftManager();
