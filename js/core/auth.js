/**
 * CityBus Enterprise Platform - Role-Based Access Control & Auth Store
 * File: js/core/auth.js
 * 
 * Manages client authentication state, permissions for 9 roles:
 * PASSENGER, DRIVER, CONDUCTOR, DISPATCHER, FLEET_MANAGER,
 * MAINTENANCE_MANAGER, FINANCE_MANAGER, ADMIN, SUPER_ADMIN.
 */

const USER_ROLES = {
  PASSENGER: 'passenger',
  DRIVER: 'driver',
  CONDUCTOR: 'conductor',
  DISPATCHER: 'dispatcher',
  FLEET_MANAGER: 'fleet_manager',
  MAINTENANCE_MANAGER: 'maintenance_manager',
  FINANCE_MANAGER: 'finance_manager',
  ADMIN: 'admin',
  SUPER_ADMIN: 'super_admin'
};

const ROLE_PERMISSIONS = {
  [USER_ROLES.PASSENGER]: [
    'view_live_map', 'view_routes', 'view_stops', 'plan_journey',
    'buy_tickets', 'view_tickets', 'cancel_ticket', 'manage_favorites', 'view_alerts'
  ],
  [USER_ROLES.DRIVER]: [
    'view_assigned_trip', 'start_trip', 'stop_trip', 'pause_trip',
    'broadcast_gps', 'log_stop_arrival', 'report_incident', 'trigger_emergency'
  ],
  [USER_ROLES.CONDUCTOR]: [
    'view_active_trip', 'scan_qr_ticket', 'validate_ticket', 'manual_ticket_check',
    'update_passenger_count', 'issue_cash_ticket'
  ],
  [USER_ROLES.DISPATCHER]: [
    'view_dispatcher_map', 'view_fleet_radar', 'message_driver', 'reassign_bus_route',
    'manage_incidents', 'broadcast_service_alert', 'emergency_override'
  ],
  [USER_ROLES.FLEET_MANAGER]: [
    'manage_buses', 'assign_drivers', 'manage_gps_devices', 'schedule_maintenance',
    'view_fleet_analytics', 'manage_fuel_logs'
  ],
  [USER_ROLES.MAINTENANCE_MANAGER]: [
    'create_work_orders', 'update_work_orders', 'manage_spare_parts', 'log_downtime',
    'view_vehicle_health'
  ],
  [USER_ROLES.FINANCE_MANAGER]: [
    'view_revenue_reports', 'process_refunds', 'manage_fares', 'view_payment_audit'
  ],
  [USER_ROLES.ADMIN]: [
    'all_operational_features', 'manage_routes', 'manage_stops', 'manage_schedules',
    'manage_fares', 'view_all_analytics', 'export_reports', 'view_audit_logs'
  ],
  [USER_ROLES.SUPER_ADMIN]: [
    'all_features', 'manage_users', 'manage_roles', 'system_config', 'db_backup', 'view_system_health'
  ]
};

// Demo User Profiles for 1-Click Sandbox Logins
const DEMO_USERS = {
  [USER_ROLES.PASSENGER]: {
    id: 'USR-PASS-01',
    name: 'Ananya Sharma',
    email: 'passenger@citybus.transit',
    role: USER_ROLES.PASSENGER,
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&h=120&q=80',
    phone: '+91 98480 11223'
  },
  [USER_ROLES.DRIVER]: {
    id: 'DRV-1',
    name: 'Ravi Kumar',
    email: 'ravi@citybus.transit',
    role: USER_ROLES.DRIVER,
    assignedBus: 'BUS-101',
    assignedRoute: 'ROUTE-27A',
    license: 'AP-16-2018-884'
  },
  [USER_ROLES.CONDUCTOR]: {
    id: 'CND-1',
    name: 'K. Venkatesh',
    email: 'conductor@citybus.transit',
    role: USER_ROLES.CONDUCTOR,
    badgeId: 'CND-VJA-402',
    assignedBus: 'BUS-101'
  },
  [USER_ROLES.DISPATCHER]: {
    id: 'DSP-1',
    name: 'Priya Nambiar',
    email: 'dispatcher@citybus.transit',
    role: USER_ROLES.DISPATCHER,
    controlSector: 'Vijayawada Central & Highway'
  },
  [USER_ROLES.FLEET_MANAGER]: {
    id: 'FLT-1',
    name: 'Mohan Das',
    email: 'fleet@citybus.transit',
    role: USER_ROLES.FLEET_MANAGER,
    depot: 'PNBS Central Depot'
  },
  [USER_ROLES.MAINTENANCE_MANAGER]: {
    id: 'MNT-1',
    name: 'G. Ramakrishna',
    email: 'maintenance@citybus.transit',
    role: USER_ROLES.MAINTENANCE_MANAGER,
    workshop: 'Autonagar Heavy Workshop'
  },
  [USER_ROLES.FINANCE_MANAGER]: {
    id: 'FIN-1',
    name: 'Sunita Reddy',
    email: 'finance@citybus.transit',
    role: USER_ROLES.FINANCE_MANAGER,
    department: 'Revenue & Ticketing Accounts'
  },
  [USER_ROLES.ADMIN]: {
    id: 'ADM-1',
    name: 'Operations Administrator',
    email: 'admin@citybus.transit',
    role: USER_ROLES.ADMIN
  },
  [USER_ROLES.SUPER_ADMIN]: {
    id: 'SADM-1',
    name: 'Transit Director General',
    email: 'superadmin@citybus.transit',
    role: USER_ROLES.SUPER_ADMIN
  }
};

class CityBusAuthManager {
  constructor() {
    this.currentUser = null;
    this.init();
  }

  init() {
    if (window.CityBusAPI) {
      this.currentUser = window.CityBusAPI.getCurrentUser();
    }
    if (!this.currentUser) {
      // Default to Passenger sandbox session
      this.currentUser = DEMO_USERS[USER_ROLES.PASSENGER];
      if (window.CityBusAPI) {
        window.CityBusAPI.setSession('demo_passenger_token', 'demo_refresh_token', this.currentUser);
      }
    }
  }

  getCurrentUser() {
    return this.currentUser;
  }

  getRole() {
    return this.currentUser ? this.currentUser.role : USER_ROLES.PASSENGER;
  }

  isAuthenticated() {
    return !!this.currentUser;
  }

  hasPermission(permission) {
    if (!this.currentUser) return false;
    const role = this.currentUser.role;
    if (role === USER_ROLES.SUPER_ADMIN || role === USER_ROLES.ADMIN) return true;
    const perms = ROLE_PERMISSIONS[role] || [];
    return perms.includes(permission);
  }

  /**
   * Switches active role for demo testing or login
   */
  switchRole(roleKey) {
    const demoProfile = DEMO_USERS[roleKey] || DEMO_USERS[USER_ROLES.PASSENGER];
    this.currentUser = demoProfile;
    if (window.CityBusAPI) {
      window.CityBusAPI.setSession(`demo_jwt_${roleKey}`, `demo_refresh_${roleKey}`, demoProfile);
    }
    console.log(`👤 [CityBus Auth] Switched active role to: ${roleKey} (${demoProfile.name})`);
    
    // Dispatch auth state change
    window.dispatchEvent(new CustomEvent('citybus:auth-changed', { detail: { user: demoProfile } }));
    return demoProfile;
  }

  logout() {
    if (window.CityBusAPI) {
      window.CityBusAPI.clearSession();
    }
    this.currentUser = null;
    window.location.href = 'login.html';
  }
}

// Global Singleton Export
window.CityBusAuth = new CityBusAuthManager();
window.USER_ROLES = USER_ROLES;
window.DEMO_USERS = DEMO_USERS;
