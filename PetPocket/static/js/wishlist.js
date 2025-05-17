document.addEventListener('DOMContentLoaded', function () {
    const wishlistGrid = document.querySelector('.wishlist-grid');
    let cartItems = [];

    // --- Sync cart state on wishlist page ---
    fetch('/check_cart_status')
        .then(response => response.json())
        .then(data => {
            cartItems = data.items || [];
            document.querySelectorAll('.product-card').forEach(card => {
                const productId = parseInt(card.dataset.productId);
                if (cartItems.includes(productId)) {
                    const cartButton = card.querySelector('.add-to-cart');
                    if (cartButton) {
                        cartButton.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> Added to Cart';
                        cartButton.classList.add('added-to-cart');
                        cartButton.disabled = true;
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error checking cart status:', error);
        });

    // Remove from wishlist functionality
    document.querySelectorAll('.remove-from-wishlist').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = this.closest('.product-card').dataset.productId;
            
            fetch('/remove_from_wishlist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('.product-card').remove();
                    if (!document.querySelector('.product-card')) {
                        wishlistGrid.innerHTML = `
                            <div class="empty-wishlist">
                                <p>Your wishlist is empty</p>
                                <a href="/" class="shop-now-btn">Shop Now</a>
                            </div>
                        `;
                    }
                    showNotification('Removed from wishlist!', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to remove from wishlist', 'error');
            });
        });
    });

    // Add to cart functionality for product cards
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (this.classList.contains('added-to-cart') || this.disabled) return;
            const productId = this.closest('.product-card').dataset.productId;
            addToCart(productId, 1, this);
        });
    });

    // Make product cards link to product detail page
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.add-to-cart') && !e.target.closest('.remove-from-wishlist')) {
                const productId = this.dataset.productId;
                window.location.href = `/product/${productId}`;
            }
        });
    });

    // Add to cart helper
    function addToCart(productId, quantity, btn) {
        fetch('/add_to_cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                btn.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> Added to Cart';
                btn.classList.add('added-to-cart');
                btn.disabled = true;
                showNotification('Added to cart!', 'success');
                updateCartCount(true);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                showNotification('Failed to add to cart', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to add to cart', 'error');
        });
    }

    // Notification function
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => { notification.classList.add('show'); }, 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => { notification.remove(); }, 300);
        }, 3000);
    }

    // Update cart count in navbar (optional, if you have a cart badge)
    function updateCartCount(increment = true) {
        const cartIcon = document.querySelector('.cart-icon');
        let cartBadge = document.querySelector('.cart-badge');
    
        if (!cartIcon) return; // If cart icon is missing, do nothing
    
        if (!cartBadge) {
            // Create the cart badge if it doesn't exist
            cartBadge = document.createElement('span');
            cartBadge.className = 'cart-badge';
            cartBadge.textContent = '1';
            cartIcon.appendChild(cartBadge);
            cartIcon.classList.add('cart-has-items');
            return;
        }
    
        // Update existing badge
        let currentCount = parseInt(cartBadge.textContent) || 0;
        if (increment) currentCount += 1;
        else currentCount = Math.max(0, currentCount - 1);
        cartBadge.textContent = currentCount;
    
        if (currentCount > 0) {
            cartBadge.style.display = 'block';
            cartIcon.classList.add('cart-has-items');
        } else {
            cartBadge.style.display = 'none';
            cartIcon.classList.remove('cart-has-items');
        }
    }
});