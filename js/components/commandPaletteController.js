/**
 * CityBus Enterprise Platform - Global Command Palette (Ctrl+K)
 * File: js/components/commandPaletteController.js
 * 
 * Provides keyboard-driven instant navigation, route/stop search,
 * quick actions, and direct portal jumping for power users.
 */

class CommandPaletteController {
    constructor() {
        this.isOpen = false;
        this.commands = [
            { id: 'home', title: 'Home / Live Map', icon: 'fa-map', url: '/passenger-map.html', category: 'Navigation' },
            { id: 'buses', title: 'Bus Directory & Fleet', icon: 'fa-bus', url: '/buses.html', category: 'Navigation' },
            { id: 'routes', title: 'Transit Routes & Corridors', icon: 'fa-route', url: '/routes.html', category: 'Navigation' },
            { id: 'stops', title: 'Stops & Station Shelters', icon: 'fa-map-pin', url: '/stops.html', category: 'Navigation' },
            { id: 'journey', title: 'Journey Planner & Directions', icon: 'fa-directions', url: '/journey-planner.html', category: 'Navigation' },
            { id: 'tickets', title: 'Purchase Digital Ticket', icon: 'fa-ticket-alt', url: '/tickets.html', category: 'Ticketing' },
            { id: 'my-tickets', title: 'My Tickets & QR Wallet', icon: 'fa-wallet', url: '/my-tickets.html', category: 'Ticketing' },
            { id: 'driver', title: 'Driver Cockpit Portal', icon: 'fa-id-card', url: '/driver.html', category: 'Staff' },
            { id: 'conductor', title: 'Conductor QR Scanner', icon: 'fa-qrcode', url: '/conductor.html', category: 'Staff' },
            { id: 'dispatcher', title: 'Dispatcher Command Radar', icon: 'fa-satellite-dish', url: '/dispatcher.html', category: 'Staff' },
            { id: 'admin', title: 'Fleet Admin Dashboard', icon: 'fa-cogs', url: '/admin.html', category: 'Management' },
            { id: 'analytics', title: 'Executive Analytics & OTP', icon: 'fa-chart-line', url: '/analytics.html', category: 'Management' },
            { id: 'maintenance', title: 'Depot Maintenance & Work Orders', icon: 'fa-wrench', url: '/maintenance.html', category: 'Operations' },
            { id: 'fuel', title: 'Fuel & EV Charging Logs', icon: 'fa-gas-pump', url: '/fuel.html', category: 'Operations' },
            { id: 'incidents', title: 'Incident Center & SOS Panic Alarms', icon: 'fa-exclamation-triangle', url: '/incidents.html', category: 'Safety' },
            { id: 'simulation', title: 'Live Fleet GPS Simulator', icon: 'fa-play', url: '/simulation.html', category: 'Developer' },
            { id: 'health', title: 'System Health & Diagnostics', icon: 'fa-heartbeat', url: '/health.html', category: 'Developer' }
        ];
        this.init();
    }

    init() {
        window.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                this.toggle();
            }
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    toggle() {
        if (this.isOpen) this.close();
        else this.open();
    }

    open() {
        this.isOpen = true;
        let palette = document.getElementById('citybus-command-palette');
        if (!palette) {
            palette = document.createElement('div');
            palette.id = 'citybus-command-palette';
            palette.className = 'citybus-command-palette-overlay';
            document.body.appendChild(palette);
        }

        palette.innerHTML = `
            <div class="command-palette-modal">
                <div class="palette-input-wrap">
                    <i class="fas fa-search palette-search-icon"></i>
                    <input type="text" class="palette-input" placeholder="Type a command, route number, or page..." autofocus>
                    <span class="palette-esc-badge">ESC</span>
                </div>
                <div class="palette-results-list"></div>
                <div class="palette-footer">
                    <span><kbd>↑</kbd> <kbd>↓</kbd> to navigate</span>
                    <span><kbd>Enter</kbd> to select</span>
                    <span><kbd>Esc</kbd> to close</span>
                </div>
            </div>
        `;

        const input = palette.querySelector('.palette-input');
        const resultsList = palette.querySelector('.palette-results-list');

        const renderResults = (query = '') => {
            const q = query.toLowerCase().trim();
            const matched = this.commands.filter(c => 
                c.title.toLowerCase().includes(q) || c.category.toLowerCase().includes(q)
            );

            if (matched.length === 0) {
                resultsList.innerHTML = '<div class="palette-empty">No matching commands or routes found</div>';
                return;
            }

            resultsList.innerHTML = matched.map((cmd, idx) => `
                <div class="palette-item ${idx === 0 ? 'selected' : ''}" data-url="${cmd.url}">
                    <i class="fas ${cmd.icon} palette-item-icon"></i>
                    <div class="palette-item-text">
                        <span class="palette-item-title">${cmd.title}</span>
                        <span class="palette-item-cat">${cmd.category}</span>
                    </div>
                </div>
            `).join('');

            resultsList.querySelectorAll('.palette-item').forEach(item => {
                item.onclick = () => {
                    window.location.href = item.dataset.url;
                };
            });
        };

        input.oninput = (e) => renderResults(e.target.value);
        palette.onclick = (e) => {
            if (e.target === palette) this.close();
        };

        renderResults();
        requestAnimationFrame(() => {
            palette.classList.add('visible');
            input.focus();
        });
    }

    close() {
        this.isOpen = false;
        const palette = document.getElementById('citybus-command-palette');
        if (palette) {
            palette.classList.remove('visible');
        }
    }
}

// Global Export
window.commandPalette = new CommandPaletteController();
