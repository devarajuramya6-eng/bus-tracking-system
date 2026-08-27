/**
 * CityBus Enterprise Platform - Passenger Trip Review & Feedback Modal
 * File: js/passenger/feedbackModal.js
 * 
 * Provides interactive star rating, driver compliment/complaint tagging,
 * and review submission dialog.
 */

class FeedbackModalController {
    static openModal(busId, tripId = null) {
        let currentRating = 5;

        window.modalManager.open({
            title: '⭐ Rate Your CityBus Journey',
            content: `
                <form id="passenger-feedback-form">
                    <div class="text-center mb-3">
                        <div class="star-rating-widget" style="font-size: 2rem; cursor: pointer; color: #F59E0B;">
                            <i class="fas fa-star rating-star" data-rating="1"></i>
                            <i class="fas fa-star rating-star" data-rating="2"></i>
                            <i class="fas fa-star rating-star" data-rating="3"></i>
                            <i class="fas fa-star rating-star" data-rating="4"></i>
                            <i class="fas fa-star rating-star" data-rating="5"></i>
                        </div>
                        <small class="text-muted rating-text-feedback font-weight-bold">Excellent (5/5)</small>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Feedback Category</label>
                        <select class="form-control" name="category">
                            <option value="General" selected>General Experience</option>
                            <option value="Driver Behavior">Driver Professionalism & Safety</option>
                            <option value="Punctuality">Punctuality & Schedule Adherence</option>
                            <option value="Cleanliness">Bus Cleanliness & Hygiene</option>
                            <option value="AC Comfort">Air Conditioning / Crowd Comfort</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label font-weight-bold">Tell us more about your trip</label>
                        <textarea class="form-control" name="comment" rows="3" placeholder="Share your experience to help us improve transit service..."></textarea>
                    </div>
                </form>
            `,
            confirmText: 'Submit Review',
            onConfirm: async (modalEl) => {
                const form = modalEl.querySelector('#passenger-feedback-form');
                const cat = form.querySelector('select[name="category"]').value;
                const comment = form.querySelector('textarea[name="comment"]').value.trim();
                const user = window.authService.getUser();

                try {
                    await window.apiClient.post('/api/v1/feedback/submit', {
                        user_id: user ? user.id : 1,
                        bus_id: busId || 1,
                        trip_id: tripId,
                        rating: currentRating,
                        category: cat,
                        comment
                    });

                    window.toastManager.success('Thank you! Your feedback helps us build a better transit network.');
                    return true;
                } catch (e) {
                    window.toastManager.error(`Failed to submit feedback: ${e.message}`);
                    return false;
                }
            }
        });

        // Bind interactive stars
        setTimeout(() => {
            const stars = document.querySelectorAll('.rating-star');
            const ratingText = document.querySelector('.rating-text-feedback');
            const labels = ['', 'Poor (1/5)', 'Fair (2/5)', 'Good (3/5)', 'Very Good (4/5)', 'Excellent (5/5)'];

            stars.forEach(star => {
                star.onclick = () => {
                    const r = Number(star.dataset.rating);
                    currentRating = r;
                    if (ratingText) ratingText.textContent = labels[r];
                    stars.forEach((s, idx) => {
                        if (idx < r) {
                            s.classList.remove('far');
                            s.classList.add('fas');
                        } else {
                            s.classList.remove('fas');
                            s.classList.add('far');
                        }
                    });
                };
            });
        }, 100);
    }
}

// Global Export
window.FeedbackModalController = FeedbackModalController;
