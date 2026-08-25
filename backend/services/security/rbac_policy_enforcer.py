"""
CityBus Enterprise Platform - Role-Based & Attribute-Based Access Control (RBAC/ABAC)
File: backend/services/security/rbac_policy_enforcer.py

Enforces fine-grained authorization policies across 9 platform roles:
- super_admin, admin, dispatcher, fleet_manager, maintenance_manager, finance_manager, conductor, driver, passenger
- Resource permissions matrix (CREATE, READ, UPDATE, DELETE, DISPATCH, RECONCILE, OVERRIDE)
"""

from typing import List, Dict, Set


class RBACPolicyEnforcer:
    ROLE_PERMISSIONS: Dict[str, Set[str]] = {
        'super_admin': {'*'}, # Full wildcard access
        'admin': {
            'users:read', 'users:write', 'buses:read', 'buses:write', 'routes:read', 'routes:write',
            'stops:read', 'stops:write', 'schedules:read', 'schedules:write', 'analytics:read', 'audit:read'
        },
        'dispatcher': {
            'buses:read', 'routes:read', 'stops:read', 'telemetry:read', 'incidents:read', 'incidents:write',
            'dispatch:control', 'alerts:write', 'headway:control'
        },
        'fleet_manager': {
            'buses:read', 'buses:write', 'drivers:read', 'depot:read', 'depot:write', 'telemetry:read', 'fuel:read'
        },
        'maintenance_manager': {
            'buses:read', 'maintenance:read', 'maintenance:write', 'spare_parts:read', 'spare_parts:write', 'workshop:write'
        },
        'finance_manager': {
            'tickets:read', 'settlements:read', 'settlements:write', 'remittances:read', 'remittances:write', 'gst:read', 'reports:read'
        },
        'conductor': {
            'tickets:write', 'tickets:validate', 'cash_bag:remit', 'occupancy:update', 'routes:read', 'smart_card:tap'
        },
        'driver': {
            'driver:roster', 'pre_trip:inspect', 'telemetry:send', 'sos:trigger', 'route:navigate', 'adas:read'
        },
        'passenger': {
            'routes:read', 'stops:read', 'buses:read', 'journey:plan', 'tickets:purchase', 'tickets:read', 'smart_card:manage', 'alerts:read'
        }
    }

    @staticmethod
    def is_authorized(user_role: str, required_permission: str) -> bool:
        """
        Evaluates whether a user role possesses the required permission.
        """
        role_perms = RBACPolicyEnforcer.ROLE_PERMISSIONS.get(user_role.lower(), set())

        # Check wildcard
        if '*' in role_perms:
            return True

        if required_permission in role_perms:
            return True

        # Check domain wildcard (e.g. 'buses:*')
        domain = required_permission.split(':')[0]
        if f"{domain}:*" in role_perms:
            return True

        return False
