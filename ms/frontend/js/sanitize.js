// XSS Protection - Input sanitization utilities

/**
 * Sanitize HTML to prevent XSS attacks
 * @param {string} str - String to sanitize
 * @returns {string} - Sanitized string
 */
function sanitizeHTML(str) {
    if (typeof str !== 'string') return '';
    
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Sanitize user input for display
 * @param {string} input - User input
 * @returns {string} - Sanitized input
 */
function sanitizeInput(input) {
    if (typeof input !== 'string') return '';
    
    // Remove potentially dangerous characters
    return input
        .replace(/[<>]/g, '') // Remove < and >
        .replace(/javascript:/gi, '') // Remove javascript: protocol
        .replace(/on\w+=/gi, '') // Remove event handlers (onclick=, etc.)
        .trim();
}

/**
 * Escape HTML entities
 * @param {string} str - String to escape
 * @returns {string} - Escaped string
 */
function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    
    return str.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Validate and sanitize medication name
 * @param {string} name - Medication name
 * @returns {string|null} - Sanitized name or null if invalid
 */
function validateMedicationName(name) {
    if (typeof name !== 'string') return null;
    
    const sanitized = sanitizeInput(name).trim();
    
    if (sanitized.length === 0 || sanitized.length > 100) {
        return null;
    }
    
    return sanitized;
}

/**
 * Validate time format (HH:MM)
 * @param {string} time - Time string
 * @returns {boolean} - True if valid
 */
function validateTimeFormat(time) {
    if (typeof time !== 'string') return false;
    
    const pattern = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
    return pattern.test(time);
}

// Make functions globally available
if (typeof window !== 'undefined') {
    window.sanitizeHTML = sanitizeHTML;
    window.sanitizeInput = sanitizeInput;
    window.escapeHTML = escapeHTML;
    window.validateMedicationName = validateMedicationName;
    window.validateTimeFormat = validateTimeFormat;
}

