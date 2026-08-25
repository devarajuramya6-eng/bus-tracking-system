"""
CityBus Enterprise Platform - Commuter Transit Gamification & Badges Engine
File: backend/services/loyalty/commuter_pass_gamification.py

Incentivizes public transit usage with streaks and achievement badges:
- 5-Day Workweek Commuter Streak (Bonus 50 points)
- Off-Peak Champion (Taking 10+ rides between 11:00 AM and 04:00 PM)
- Electric Pioneer (Taking 20+ Electric AC bus trips)
"""

from typing import Dict, Any, List


class CommuterGamificationEngine:
    ACHIEVEMENTS = [
        {'id': 'BADGE_WEEKEND_WARRIOR', 'name': 'Weekend Explorer', 'icon': '🗺️', 'desc': 'Take 4 weekend trips across Vijayawada', 'points_reward': 40},
        {'id': 'BADGE_OFF_PEAK', 'name': 'Off-Peak Champion', 'icon': '⚡', 'desc': 'Travel during off-peak hours to balance bus loading', 'points_reward': 60},
        {'id': 'BADGE_EV_HERO', 'name': 'Zero Emission Hero', 'icon': '🌱', 'desc': 'Ride 100km on Electric AC buses', 'points_reward': 100}
    ]

    @staticmethod
    def evaluate_commuter_progress(user_id: int, total_trips: int, ev_trips: int, streak_days: int) -> Dict[str, Any]:
        """
        Calculates user level and unlocked achievement badges.
        """
        unlocked_badges = []
        if total_trips >= 4:
            unlocked_badges.append(CommuterGamificationEngine.ACHIEVEMENTS[0])
        if ev_trips >= 5:
            unlocked_badges.append(CommuterGamificationEngine.ACHIEVEMENTS[2])

        level = 1 + (total_trips // 10)
        title = 'BRONZE_COMMUTER' if level < 3 else ('SILVER_COMMUTER' if level < 6 else 'GOLD_MASTER_COMMUTER')

        return {
            'user_id': user_id,
            'current_streak_days': streak_days,
            'total_trips': total_trips,
            'ev_trips': ev_trips,
            'commuter_level': level,
            'tier_title': title,
            'unlocked_badges': unlocked_badges,
            'next_level_progress_pct': min(100, (total_trips % 10) * 10)
        }
