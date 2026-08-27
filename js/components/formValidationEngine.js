/**
 * CityBus Enterprise Platform - Client Form Validation Engine
 * File: js/components/formValidationEngine.js
 * 
 * Provides declarative form validation rules (email, phone, numeric bounds,
 * password strength, license plates) with inline UI feedback.
 */

class FormValidationEngine {
    static RULES = {
        required: (val) => val !== null && val !== undefined && String(val).trim().length > 0,
        email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(val).trim()),
        phone: (val) => /^[+]?[\d\s-]{10,15}$/.test(String(val).trim()),
        plate: (val) => /^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{1,4}$/i.test(String(val).trim()),
        minLength: (val, len) => String(val).trim().length >= Number(len),
        minVal: (val, min) => Number(val) >= Number(min),
        maxVal: (val, max) => Number(val) <= Number(max)
    };

    static validateForm(formElement) {
        if (!formElement) return { isValid: true, errors: {} };
        const inputs = formElement.querySelectorAll('input, select, textarea');
        const errors = {};
        let isValid = true;

        inputs.forEach(input => {
            const name = input.name || input.id;
            const value = input.value;
            const errorContainer = formElement.querySelector(`.error-feedback[data-for="${name}"]`) || input.nextElementSibling;

            // Clear previous state
            input.classList.remove('is-invalid', 'is-valid');
            if (errorContainer && errorContainer.classList.contains('error-feedback')) {
                errorContainer.textContent = '';
                errorContainer.style.display = 'none';
            }

            // Check required
            if (input.hasAttribute('required') && !FormValidationEngine.RULES.required(value)) {
                errors[name] = 'This field is required.';
                isValid = false;
            } else if (input.type === 'email' && value && !FormValidationEngine.RULES.email(value)) {
                errors[name] = 'Please enter a valid email address.';
                isValid = false;
            } else if (input.dataset.rule === 'phone' && value && !FormValidationEngine.RULES.phone(value)) {
                errors[name] = 'Please enter a valid phone number (10-15 digits).';
                isValid = false;
            } else if (input.dataset.minLength && value && !FormValidationEngine.RULES.minLength(value, input.dataset.minLength)) {
                errors[name] = `Must be at least ${input.dataset.minLength} characters.`;
                isValid = false;
            }

            if (errors[name]) {
                input.classList.add('is-invalid');
                if (errorContainer && errorContainer.classList.contains('error-feedback')) {
                    errorContainer.textContent = errors[name];
                    errorContainer.style.display = 'block';
                }
            } else if (value) {
                input.classList.add('is-valid');
            }
        });

        return { isValid, errors };
    }
}

// Global Export
window.FormValidationEngine = FormValidationEngine;
