"""
CityBus Enterprise Platform - Passenger Feedback API
File: backend/routes/feedback.py

Handles passenger star ratings, reviews, driver feedback, and comfort evaluations.
"""

from flask import Blueprint, request, jsonify
from services.passenger_feedback_service import PassengerFeedbackService

feedback_bp = Blueprint('feedback_v1', __name__, url_prefix='/api/v1/feedback')


@feedback_bp.route('/submit', methods=['POST'])
def submit_review():
    """Submits a passenger ride review."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        bus_id = data.get('bus_id', 1)
        rating = int(data.get('rating', 5))
        comment = data.get('comment', '').strip()
        category = data.get('category', 'General')
        trip_id = data.get('trip_id')

        res = PassengerFeedbackService.submit_feedback(user_id, bus_id, rating, comment, category, trip_id)
        return jsonify({"success": True, "message": "Feedback submitted successfully", "review": res}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@feedback_bp.route('/bus/<int:bus_id>', methods=['GET'])
def get_bus_reviews(bus_id):
    """Retrieves review summary and average rating for a bus."""
    try:
        summary = PassengerFeedbackService.get_bus_feedback_summary(bus_id)
        return jsonify({"success": True, **summary}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
