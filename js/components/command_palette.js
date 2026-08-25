/**
 * CityBus Enterprise Design System - Command Palette (Ctrl + K)
 * File: js/components/command_palette.js
 */

class CityBusCommandPalette {
  constructor() {
    this.isOpen = false;
    this.selectedIndex = 0;
    this.filteredItems = [];
    this.commands = this.getDefaultCommands();
    this.init();
  }

  init() {
    // Keyboard shortcut (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.toggle();
      }
    });

    this.createPaletteModal();
  }

  getDefaultCommands() {
    return [
      // Navigation
      { id: 'nav-home', title: 'Go to Home / Passenger Portal', category: 'Navigation', icon: 'fa-house', action: () => window.location.href = 'index.html' },
      { id: 'nav-buses', title: 'Explore Live Operating Buses', category: 'Navigation', icon: 'fa-bus', action: () => window.location.href = 'buses.html' },
      { id: 'nav-routes', title: 'Browse Transit Corridors & Routes', category: 'Navigation', icon: 'fa-route', action: () => window.location.href = 'routes.html' },
      { id: 'nav-planner', title: 'Plan Multi-Leg Journey', category: 'Navigation', icon: 'fa-map-location-dot', action: () => window.location.href = 'journey-planner.html' },
      { id: 'nav-tickets', title: 'Book Passenger Tickets & Passes', category: 'Navigation', icon: 'fa-ticket', action: () => window.location.href = 'tickets.html' },
      { id: 'nav-my-tickets', title: 'View My Digital QR Tickets', category: 'Navigation', icon: 'fa-qrcode', action: () => window.location.href = 'my-tickets.html' },
      
      // Operations & Cockpits
      { id: 'nav-driver', title: 'Open Driver Cockpit & Trip Controls', category: 'Operations', icon: 'fa-id-card', action: () => window.location.href = 'driver.html' },
      { id: 'nav-conductor', title: 'Open Conductor QR Validator Terminal', category: 'Operations', icon: 'fa-camera', action: () => window.location.href = 'conductor.html' },
      { id: 'nav-dispatcher', title: 'Open Tactical Dispatcher Command Center', category: 'Operations', icon: 'fa-tower-broadcast', action: () => window.location.href = 'dispatcher.html' },
      { id: 'nav-admin', title: 'Open Fleet Operations & Admin Dashboard', category: 'Operations', icon: 'fa-shield-halved', action: () => window.location.href = 'admin.html' },
      { id: 'nav-incidents', title: 'Open Incident & Emergency Command', category: 'Operations', icon: 'fa-triangle-exclamation', action: () => window.location.href = 'incidents.html' },
      { id: 'nav-maintenance', title: 'Open Maintenance & Work Orders', category: 'Operations', icon: 'fa-wrench', action: () => window.location.href = 'maintenance.html' },
      { id: 'nav-fuel', title: 'Open Fuel Logs & Efficiency Analytics', category: 'Operations', icon: 'fa-gas-pump', action: () => window.location.href = 'fuel.html' },
      { id: 'nav-analytics', title: 'Open Transit Analytics & OTP Charts', category: 'Operations', icon: 'fa-chart-line', action: () => window.location.href = 'analytics.html' },
      { id: 'nav-reports', title: 'Open Custom Report Builder & Exporter', category: 'Operations', icon: 'fa-file-invoice', action: () => window.location.href = 'reports.html' },
      { id: 'nav-simulation', title: 'Open Fleet GPS Simulation Control Room', category: 'Operations', icon: 'fa-sliders', action: () => window.location.href = 'simulation.html' },
      { id: 'nav-health', title: 'Open Real-Time Diagnostics & System Health', category: 'Operations', icon: 'fa-heart-pulse', action: () => window.location.href = 'health.html' },

      // Quick Actions
      { id: 'act-theme', title: 'Toggle Light / Dark Mode', category: 'Actions', icon: 'fa-moon', action: () => window.CityBusTheme?.toggleTheme() },
      { id: 'act-locate', title: 'Locate My Current GPS Position', category: 'Actions', icon: 'fa-location-crosshairs', action: () => {
        if (window.CityBusMap && window.CityBusMap.locateUser) {
          window.CityBusMap.locateUser();
        } else if (window.showToast) {
          window.showToast('Locating your position...', 'info');
        }
      }},
      { id: 'act-emergency', title: 'TRIGGER EMERGENCY SOS DISPATCH', category: 'Emergency', icon: 'fa-bell', action: () => {
        if (window.CityBusModal) {
          window.CityBusModal.confirm({
            title: 'EMERGENCY SOS CONFIRMATION',
            message: 'Are you sure you want to trigger a Priority-1 Emergency Broadcast to all active dispatchers?',
            confirmText: 'BROADCAST SOS NOW',
            confirmType: 'danger',
            onConfirm: () => {
              if (window.showToast) window.showToast('EMERGENCY SOS DISPATCHED TO CENTRAL CONTROL', 'danger', 7000);
            }
          });
        }
      }}
    ];
  }

  createPaletteModal() {
    let backdrop = document.getElementById('cb-command-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.id = 'cb-command-backdrop';
      backdrop.className = 'modal-backdrop';
      backdrop.style.zIndex = 'var(--cb-z-command)';

      backdrop.innerHTML = `
        <div class="cb-command-dialog">
          <div class="cb-command-input-wrap">
            <i class="fa-solid fa-magnifying-glass" style="color: var(--cb-text-muted); font-size: 1.1rem;"></i>
            <input type="text" id="cb-command-input" class="cb-command-input" placeholder="Type a command or search (e.g. 'Track Bus', 'Tickets', 'Dispatcher', 'Dark mode')..." autocomplete="off">
            <span class="badge badge-dark" style="font-size: 0.7rem;">ESC to close</span>
          </div>
          <div id="cb-command-list" class="cb-command-list">
            <!-- Rendered dynamically -->
          </div>
        </div>
      `;

      document.body.appendChild(backdrop);

      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) this.close();
      });

      const input = backdrop.querySelector('#cb-command-input');
      input.addEventListener('input', (e) => this.filter(e.target.value));
      input.addEventListener('keydown', (e) => this.handleKeyNav(e));
    }
  }

  toggle() {
    if (this.isOpen) this.close();
    else this.open();
  }

  open() {
    this.isOpen = true;
    const backdrop = document.getElementById('cb-command-backdrop');
    if (backdrop) {
      backdrop.classList.add('show');
      const input = backdrop.querySelector('#cb-command-input');
      input.value = '';
      this.filter('');
      setTimeout(() => input.focus(), 50);
    }
  }

  close() {
    this.isOpen = false;
    const backdrop = document.getElementById('cb-command-backdrop');
    if (backdrop) {
      backdrop.classList.remove('show');
    }
  }

  filter(query) {
    const q = query.trim().toLowerCase();
    if (!q) {
      this.filteredItems = [...this.commands];
    } else {
      this.filteredItems = this.commands.filter(cmd => {
        return cmd.title.toLowerCase().includes(q) || cmd.category.toLowerCase().includes(q);
      });
    }

    this.selectedIndex = 0;
    this.renderList();
  }

  renderList() {
    const listContainer = document.getElementById('cb-command-list');
    if (!listContainer) return;

    if (this.filteredItems.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align: center; padding: 2.5rem 1rem; color: var(--cb-text-muted);">
          <div style="font-size: 1.8rem; margin-bottom: 0.5rem; color: var(--cb-text-subtle);"><i class="fa-solid fa-magnifying-glass"></i></div>
          <div style="font-weight: 600;">No commands found</div>
          <div style="font-size: 0.8rem;">Try searching for a different destination, vehicle or action.</div>
        </div>
      `;
      return;
    }

    // Group by category
    const categories = {};
    this.filteredItems.forEach((item, index) => {
      if (!categories[item.category]) categories[item.category] = [];
      categories[item.category].push({ ...item, globalIndex: index });
    });

    let html = '';
    Object.keys(categories).forEach(cat => {
      html += `<div class="cb-command-group-title">${cat}</div>`;
      categories[cat].forEach(item => {
        const isSelected = item.globalIndex === this.selectedIndex;
        html += `
          <div class="cb-command-item ${isSelected ? 'active' : ''}" data-cmd-index="${item.globalIndex}">
            <div class="item-left">
              <i class="fa-solid ${item.icon}" style="color: var(--cb-brand-primary); width: 20px; text-align: center;"></i>
              <span style="font-weight: 600;">${item.title}</span>
            </div>
            <span style="font-size: 0.75rem; color: var(--cb-text-subtle);"><i class="fa-solid fa-arrow-turn-down" style="transform: rotate(90deg);"></i></span>
          </div>
        `;
      });
    });

    listContainer.innerHTML = html;

    listContainer.querySelectorAll('.cb-command-item').forEach(el => {
      el.onclick = () => {
        const idx = parseInt(el.dataset.cmdIndex);
        this.execute(idx);
      };
    });
  }

  handleKeyNav(e) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (this.selectedIndex < this.filteredItems.length - 1) {
        this.selectedIndex++;
        this.renderList();
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
        this.renderList();
      }
    } else if (e.key === 'Enter') {
      e.preventDefault();
      this.execute(this.selectedIndex);
    } else if (e.key === 'Escape') {
      this.close();
    }
  }

  execute(index) {
    const item = this.filteredItems[index];
    if (item && item.action) {
      this.close();
      item.action();
    }
  }
}

// Global Export
window.CityBusCommand = new CityBusCommandPalette();
