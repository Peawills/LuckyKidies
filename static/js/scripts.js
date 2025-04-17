// This script handles the functionality of adding items to the cart, updating quantities, and removing items from the cart.

    document.addEventListener('DOMContentLoaded', function() {
        const addToCartBtn = document.getElementById('add-to-cart-btn');
        const quantitySelect = document.getElementById('quantity');
        
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', async function() {
                const productId = this.dataset.productId;
                const quantity = quantitySelect.value;
                
                try {
                    const response = await fetch(`/cart/add/${productId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: `quantity=${quantity}`
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Show success message
                        alert(data.message);
                        
                        // Update cart count in navbar if it exists
                        const cartCountElement = document.getElementById('cart-count');
                        if (cartCountElement) {
                            cartCountElement.textContent = data.cart_count;
                        }
                    } else {
                        alert(data.message);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred while adding to cart.');
                }
            });
        }
        
        // Get CSRF token
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
    });







document.addEventListener('DOMContentLoaded', function() {
        // Update quantity
        const updateQuantity = async (itemId, quantity) => {
            try {
                const response = await fetch(`/cart/update/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `quantity=${quantity}`
                });
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        };

        // Remove item
        const removeItem = async (itemId) => {
            if (confirm('Are you sure you want to remove this item?')) {
                try {
                    const response = await fetch(`/cart/remove/${itemId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    });
                    const data = await response.json();
                    if (data.success) {
                        location.reload();
                    } else {
                        alert(data.message);
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        };

        // WhatsApp checkout
        const whatsappCheckout = document.getElementById('whatsapp-checkout');
        if (whatsappCheckout) {
            whatsappCheckout.addEventListener('click', function(event) {
                event.preventDefault();

                const cartItems = [];
                document.querySelectorAll('tbody tr').forEach(row => {
                    const productName = row.querySelector('h6')?.textContent || "Unknown Product";
                    const quantity = row.querySelector('.quantity-input')?.value || "1";
                    const category = row.querySelector('.product-category')?.textContent || "Unknown Category";
                    const imageUrl = row.querySelector('.product-image')?.src || "";

                    cartItems.push({
                        productName,
                        quantity,
                        category,
                        imageUrl
                });

                let message = "Hello! I'm interested in these items:\n\n";
                cartItems.forEach(item => {
                    message += `- ${item.productName} (Category: ${item.category}, Quantity: ${item.quantity}, Image: ${item.imageUrl})\n`;
                });
                message += `\n\nPlease confirm availability and price.`;

                const encodedMessage = encodeURIComponent(message);
                const whatsappNumber = "{{ whatsapp_number }}".replace(/\D/g, '');

                if (whatsappNumber) {
                    window.open(`https://wa.me/${whatsappNumber}?text=${encodedMessage}`, '_blank');

                    // Clear the session after sending the WhatsApp message
                    fetch("{% url 'clear-session' %}", {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    }).then(response => {
                        return response.json();
                    }).then(data => {
                        if (data.success) {
                            // Redirect to home or reload
                            location.href = "{% url 'home' %}";
                        } else {
                            alert("Failed to clear session. Please try again.");
                        }
                    }).catch(error => {
                        console.error('Error:', error);
                    });
                } else {
                    alert("WhatsApp number is missing. Please contact support.");
                }
            });
        }

        // Event listeners
        document.querySelectorAll('.update-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.dataset.itemId;
                const action = this.dataset.action;
                const input = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
                let quantity = parseInt(input.value);

                if (action === 'increase') {
                    quantity += 1;
                } else if (action === 'decrease' && quantity > 1) {
                    quantity -= 1;
                }

                input.value = quantity;
                updateQuantity(itemId, quantity);
            });
        });

        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const itemId = this.dataset.itemId;
                const quantity = parseInt(this.value);
                if (quantity > 0) {
                    updateQuantity(itemId, quantity);
                }
            });
        });

        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.dataset.itemId;
                removeItem(itemId);
            });
        });

        // Get CSRF token
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
    });
});