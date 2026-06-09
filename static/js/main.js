// Saffron Store - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips (if using Bootstrap)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle quantity input
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            if (this.value > 10) this.value = 10;
        });
    });

    // Handle cart add via AJAX (optional)
    handleCartAddition();
    
    // Handle form validation
    handleFormValidation();
});

/**
 * Handle cart addition with optional AJAX
 */
function handleCartAddition() {
    const addToCartForms = document.querySelectorAll('[id^="add-to-cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Allow default form submission for now
            // Can be converted to AJAX later
        });
    });
}

/**
 * Validate checkout form
 */
function handleFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Add to cart via AJAX (optional enhancement)
 */
function addToCartAjax(variantId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/add/${variantId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Update cart count
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = data;
        }
        showNotification('Added to cart!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to cart', 'danger');
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Update quantity in cart
 */
function updateQuantity(variantId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(variantId);
        return;
    }
    
    const form = document.querySelector(`form[action*="/cart/update/${variantId}/"]`);
    if (form) {
        form.submit();
    }
}

/**
 * Remove from cart
 */
function removeFromCart(variantId) {
    if (confirm('Are you sure you want to remove this item?')) {
        const form = document.querySelector(`form[action*="/cart/remove/${variantId}/"]`);
        if (form) {
            form.submit();
        }
    }
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

/**
 * Calculate cart total
 */
function calculateCartTotal() {
    const rows = document.querySelectorAll('table tbody tr');
    let total = 0;
    
    rows.forEach(row => {
        const priceCell = row.querySelector('td:nth-child(5)');
        if (priceCell) {
            const price = parseFloat(priceCell.textContent.replace('₹', ''));
            total += price;
        }
    });
    
    return total;
}

// Export functions for use in HTML
window.addToCartAjax = addToCartAjax;
window.updateQuantity = updateQuantity;
window.removeFromCart = removeFromCart;
window.formatCurrency = formatCurrency;
