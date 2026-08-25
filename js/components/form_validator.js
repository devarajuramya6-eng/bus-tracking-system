/**
 * CityBus Enterprise Platform - Client Form Validation Engine
 * File: js/components/form_validator.js
 * 
 * Provides automated, reactive input validation with real-time UI error messages:
 * - Email, phone, vehicle registration plate (AP16-XX-XXXX), speed limits, coordinate bounds
 * - Schema-based constraint verification
 */

class CityBusFormValidator {
  static rules = {
    required: (val) => (val !== undefined && val !== null && String(val).trim().length > 0) || 'This field is required',
    email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Enter a valid email address',
    phone: (val) => /^[6-9]\d{9}$/.test(val) || 'Enter a valid 10-digit Indian phone number',
    busPlate: (val) => /^AP\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{1,4}$/i.test(val) || 'Enter valid Andhra Pradesh registration (e.g. AP16-Z-1042)',
    positiveNumber: (val) => (!isNaN(val) && Number(val) > 0) || 'Must be a positive number',
    latitude: (val) => (!isNaN(val) && Number(val) >= -90 && Number(val) <= 90) || 'Latitude must be between -90 and 90',
    longitude: (val) => (!isNaN(val) && Number(val) >= -180 && Number(val) <= 180) || 'Longitude must be between -180 and 180',
    minLength: (min) => (val) => (String(val).length >= min) || `Must be at least ${min} characters`,
    password: (val) => (String(val).length >= 6) || 'Password must be at least 6 characters'
  };

  /**
   * Binds live validation to a HTML form element.
   */
  static attach(formElement, schema, onSubmitCallback) {
    if (!formElement) return;

    const getFieldValue = (fieldName) => {
      const input = formElement.querySelector(`[name="${fieldName}"]`);
      if (!input) return null;
      if (input.type === 'checkbox') return input.checked;
      return input.value;
    };

    const validateField = (fieldName, showUI = true) => {
      const input = formElement.querySelector(`[name="${fieldName}"]`);
      if (!input) return true;
      const val = getFieldValue(fieldName);
      const fieldRules = schema[fieldName] || [];

      let errorMsg = null;
      for (const rule of fieldRules) {
        const result = rule(val);
        if (result !== true) {
          errorMsg = result;
          break;
        }
      }

      let errorContainer = input.parentElement.querySelector('.form-error-msg');
      if (errorMsg && showUI) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        if (!errorContainer) {
          errorContainer = document.createElement('div');
          errorContainer.className = 'form-error-msg';
          errorContainer.style.cssText = 'color: var(--cb-status-danger); font-size: 0.75rem; margin-top: 4px;';
          input.parentElement.appendChild(errorContainer);
        }
        errorContainer.textContent = errorMsg;
        return false;
      } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        if (errorContainer) errorContainer.remove();
        return true;
      }
    };

    // Attach blur and input event listeners
    Object.keys(schema).forEach(fieldName => {
      const input = formElement.querySelector(`[name="${fieldName}"]`);
      if (input) {
        input.addEventListener('blur', () => validateField(fieldName, true));
        input.addEventListener('input', () => {
          if (input.classList.contains('is-invalid')) {
            validateField(fieldName, true);
          }
        });
      }
    });

    // Form submit handler
    formElement.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;
      const formData = {};

      Object.keys(schema).forEach(fieldName => {
        const fieldValid = validateField(fieldName, true);
        if (!fieldValid) isValid = false;
        formData[fieldName] = getFieldValue(fieldName);
      });

      if (isValid && onSubmitCallback) {
        onSubmitCallback(formData);
      }
    });
  }
}

// Global Export
window.CityBusFormValidator = CityBusFormValidator;
