/**
 * CityBus Enterprise Platform - Simulation Control Panel Logic
 * File: js/admin/simulation_panel.js
 */

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('sim-toggle-btn');
  const speedSlider = document.getElementById('sim-speed-slider');
  const stepBtn = document.getElementById('sim-step-manual-btn');
  const injectDelayBtn = document.getElementById('sim-inject-delay-btn');
  const injectSOSBtn = document.getElementById('sim-inject-sos-btn');
  const simStatusBadge = document.getElementById('sim-status-badge');

  if (toggleBtn) {
    toggleBtn.onclick = () => {
      if (window.LiveSimulator) {
        if (window.LiveSimulator.isRunning) {
          window.LiveSimulator.stop();
          toggleBtn.className = 'btn btn-success';
          toggleBtn.innerHTML = '<i class="fa-solid fa-play"></i> Resume Simulator';
          if (simStatusBadge) {
            simStatusBadge.className = 'badge badge-warning';
            simStatusBadge.textContent = 'PAUSED';
          }
        } else {
          window.LiveSimulator.start();
          toggleBtn.className = 'btn btn-warning';
          toggleBtn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause Simulator';
          if (simStatusBadge) {
            simStatusBadge.className = 'badge badge-success';
            simStatusBadge.textContent = 'RUNNING';
          }
        }
      }
    };
  }

  if (stepBtn) {
    stepBtn.onclick = async () => {
      if (window.CityBusAPI) {
        try {
          const res = await window.CityBusAPI.post('/simulation/step', {});
          if (res && res.buses) {
            window.dispatchEvent(new CustomEvent('citybus:data-updated', { detail: { buses: res.buses } }));
          }
        } catch {}
      }
      if (window.showToast) window.showToast('Manually advanced simulation kinematic tick', 'info');
    };
  }

  if (injectDelayBtn) {
    injectDelayBtn.onclick = () => {
      if (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) {
        const bus = window.CITYBUS_DATA.buses[0];
        bus.status = 'Delayed';
        bus.speed = 14;
        window.dispatchEvent(new CustomEvent('citybus:data-updated', { detail: { buses: window.CITYBUS_DATA.buses } }));
        if (window.showToast) window.showToast(`Injected simulated traffic delay on Bus ${bus.number}`, 'warning');
      }
    };
  }

  if (injectSOSBtn) {
    injectSOSBtn.onclick = () => {
      if (window.CITYBUS_DATA && window.CITYBUS_DATA.buses) {
        const bus = window.CITYBUS_DATA.buses[0];
        bus.status = 'Emergency';
        bus.speed = 0;
        window.dispatchEvent(new CustomEvent('citybus:data-updated', { detail: { buses: window.CITYBUS_DATA.buses } }));
        if (window.showToast) window.showToast(`🚨 Priority-1 SOS event injected on Bus ${bus.number}`, 'danger', 8000);
      }
    };
  }
});
