document.addEventListener('DOMContentLoaded', function() {
    let cartItems = [];
    let wishlistItems = [];
    const productId = document.querySelector('#add-to-cart-btn')?.dataset.productId;

    fetch('/check_cart_status')
        .then(response => response.json())
        .then(data => {
            cartItems = data.items || [];
            updateCartButtons();
            const quantityInput = document.querySelector('.quantity-input');
            if (quantityInput) {
                quantityInput.value = 1;
            }
        })
        .catch(error => console.error('Error fetching cart status:', error));

    fetch('/check_wishlist_status')
        .then(response => response.json())
        .then(data => {
            wishlistItems = data.items || [];
            updateWishlistButtons();
        })
        .catch(error => console.error('Error fetching wishlist status:', error));

    function updateCartButtons() {
        const addToCartBtn = document.getElementById('add-to-cart-btn');
        if (addToCartBtn && cartItems.includes(parseInt(addToCartBtn.dataset.productId))) {
            addToCartBtn.classList.add('added');
            addToCartBtn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Cart';
        }
        document.querySelectorAll('.add-to-cart').forEach(btn => {
            const productId = parseInt(btn.dataset.productId);
            if (cartItems.includes(productId)) {
                btn.classList.add('added');
                btn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Cart';
            }
        });
    }

    function updateWishlistButtons() {
        const wishlistBtn = document.getElementById('add-to-wishlist-btn');
        if (wishlistBtn && wishlistItems.includes(parseInt(wishlistBtn.dataset.productId))) {
            wishlistBtn.classList.add('in-wishlist');
        }
        document.querySelectorAll('.add-to-wishlist').forEach(btn => {
            const productId = parseInt(btn.dataset.productId);
            if (wishlistItems.includes(productId)) {
                btn.classList.add('in-wishlist');
            }
        });
    }

    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).style.display = 'block';
        });
    });

    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.addEventListener('click', () => {
            document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
            
            const mainImage = document.getElementById('main-product-image');
            const imageUrl = thumb.getAttribute('data-image-url');
            if (imageUrl) {
                mainImage.src = imageUrl;
            }
        });
    });

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const rating = document.querySelector('input[name="rating"]:checked')?.value;
            const content = document.getElementById('review-content').value;
            const productId = document.querySelector('input[name="product_id"]').value;
            
            if (!rating || !content) {
                alert('Please provide both rating and review content');
                return;
            }
            
            try {
                const response = await fetch('/api/reviews/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        rating: parseInt(rating),
                        content: content
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert(data.error || 'Failed to submit review');
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Failed to submit review. Please try again.');
            }
        });
    }

    document.querySelectorAll('.rating-select input').forEach(input => {
        input.addEventListener('change', () => {
            const rating = input.value;
            const stars = document.querySelectorAll('.rating-select label');
            
            stars.forEach(star => {
                star.textContent = '☆';
            });
            
            stars.forEach(star => {
                const starValue = star.getAttribute('for').replace('star', '');
                if (starValue <= rating) {
                    star.textContent = '★';
                }
            });
        });
    });

    document.addEventListener('DOMContentLoaded', () => {
        const checkedStar = document.querySelector('.rating-select input:checked');
        if (checkedStar) {
            const rating = checkedStar.value;
            const stars = document.querySelectorAll('.rating-select label');
            
            stars.forEach(star => {
                const starValue = star.getAttribute('for').replace('star', '');
                if (starValue <= rating) {
                    star.textContent = '★';
                }
            });
        }
    });

    document.querySelector('.quantity-btn.decrease')?.addEventListener('click', () => {
        const input = document.querySelector('.quantity-input');
        if (parseInt(input.value) > 1) {
            input.value = parseInt(input.value) - 1;
        }
    });

    document.querySelector('.quantity-btn.increase')?.addEventListener('click', () => {
        const input = document.querySelector('.quantity-input');
        const max = parseInt(input.getAttribute('max') || 1);
        if (parseInt(input.value) < max) {
            input.value = parseInt(input.value) + 1;
        }
    });

    const addToCartBtn = document.getElementById('add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', async () => {
            const productId = addToCartBtn.dataset.productId;
            const quantityInput = document.querySelector('.quantity-input');
            const quantity = parseInt(quantityInput?.value || 1);
            
            if (cartItems.includes(parseInt(productId))) {
                return;
            }
            
            try {
                const response = await fetch('/add_to_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        product_id: productId,
                        quantity: quantity
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (!cartItems.includes(parseInt(productId))) {
                        cartItems.push(parseInt(productId));
                    }
                    
                    addToCartBtn.classList.add('added');
                    addToCartBtn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Cart';
                    
                    if (data.cart_count !== undefined) {
                        updateNavbarCartCountAbsolute(data.cart_count);
                    } else {
                        updateNavbarCartCount(quantity);
                    }
                } else if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message || 'Failed to add to cart');
                }
            } catch (error) {
                console.error('Error adding to cart:', error);
                alert('Failed to add to cart. Please try again.');
            }
        });
    }

    function updateNavbarCartCount(addedQuantity) {
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
            const currentCount = parseInt(cartBadge.textContent) || 0;
            cartBadge.textContent = currentCount + addedQuantity;
        } else {
            const cartIcon = document.querySelector('.cart-icon');
            if (cartIcon) {
                const badge = document.createElement('span');
                badge.className = 'cart-badge';
                badge.textContent = addedQuantity;
                cartIcon.appendChild(badge);
            }
        }
    }

    function updateNavbarCartCountAbsolute(totalCount) {
        const cartBadge = document.querySelector('.cart-badge');
        const cartIcon = document.querySelector('.cart-icon');
        
        if (!cartIcon) return;
        
        if (cartBadge) {
            cartBadge.textContent = totalCount;
            
            if (totalCount > 0) {
                cartIcon.classList.add('cart-has-items');
            } else {
                cartIcon.classList.remove('cart-has-items');
            }
        } else if (totalCount > 0) {
            const badge = document.createElement('span');
            badge.className = 'cart-badge';
            badge.textContent = totalCount;
            cartIcon.appendChild(badge);
            cartIcon.classList.add('cart-has-items');
        }
    }

    const wishlistBtn = document.getElementById('add-to-wishlist-btn');
    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', async () => {
            const productId = wishlistBtn.dataset.productId;
            
            try {
                const response = await fetch('/add_to_wishlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ product_id: productId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (wishlistItems.includes(parseInt(productId))) {
                        wishlistItems = wishlistItems.filter(id => id !== parseInt(productId));
                        wishlistBtn.classList.remove('in-wishlist');
                    } else {
                        wishlistItems.push(parseInt(productId));
                        wishlistBtn.classList.add('in-wishlist');
                    }
                    updateWishlistButtons();
                } else if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message || 'Failed to update wishlist');
                }
            } catch (error) {
                console.error('Error updating wishlist:', error);
                alert('Failed to update wishlist. Please try again.');
            }
        });
    }

    function loadRecommendations(productId) {
        const container = document.getElementById('recommendationsContainer');
        if (!container) return;
    
        container.innerHTML = `<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i></div>`;
    
        fetch(`/api/recommendations/${productId}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(products => {
                container.innerHTML = '';
                if (products.length === 0) {
                    container.innerHTML = `<p class="no-recommendations">No similar products found</p>`;
                    return;
                }
                
                products.forEach(product => {
                    const stars = '★'.repeat(Math.round(product.rating || 0)) + '☆'.repeat(5 - Math.round(product.rating || 0));
                    const card = `
                        <div class="product-card" data-product-id="${product.id}" 
                             onclick="window.location.href='/product/${product.id}'">
                            <div class="product-content">
                                <img src="${product.image_url || 'https://placehold.co/200x200/46f27a/ffffff?text=Product'}" 
                                     alt="${product.name}">
                                <h3>${product.name}</h3>
                                <div class="product-details">
                                    <span class="product-price">$${product.price.toFixed(2)}</span>
                                    <span class="product-rating">${stars} (${product.review_count || 0})</span>
                                </div>
                            </div>
                            <div class="product-actions">
                                <button class="add-to-cart" data-product-id="${product.id}" 
                                        onclick="event.stopPropagation(); addToCart(${product.id}, this)">
                                    <span class="material-symbols-outlined">shopping_cart</span> Add to Cart
                                </button>
                                <button class="add-to-wishlist" data-product-id="${product.id}" 
                                        onclick="event.stopPropagation(); toggleWishlist(${product.id}, this)">
                                    <span class="material-symbols-outlined">favorite</span>
                                </button>
                            </div>
                        </div>
                    `;
                    container.insertAdjacentHTML('beforeend', card);
                });
                updateCartButtons();
                updateWishlistButtons();
            })
            .catch(error => {
                console.error('Recommendation error:', error);
                container.innerHTML = `<p class="recommendation-error">Failed to load recommendations. Please try refreshing the page.</p>`;
            });
    }

    window.addToCart = async function(productId, button) {
        if (cartItems.includes(parseInt(productId))) {
            return;
        }
        
        try {
            const response = await fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    product_id: productId,
                    quantity: 1
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                if (!cartItems.includes(parseInt(productId))) {
                    cartItems.push(parseInt(productId));
                }
                
                button.classList.add('added');
                button.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Cart';
                
                if (data.cart_count !== undefined) {
                    updateNavbarCartCountAbsolute(data.cart_count);
                } else {
                    updateNavbarCartCount(1);
                }
            } else if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                alert(data.message || 'Failed to add to cart');
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('Failed to add to cart. Please try again.');
        }
    };

    window.toggleWishlist = async function(productId, button) {
        try {
            const response = await fetch('/add_to_wishlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: productId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                if (wishlistItems.includes(parseInt(productId))) {
                    wishlistItems = wishlistItems.filter(id => id !== parseInt(productId));
                    button.classList.remove('in-wishlist');
                } else {
                    wishlistItems.push(parseInt(productId));
                    button.classList.add('in-wishlist');
                }
                updateWishlistButtons();
            } else if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                alert(data.message || 'Failed to update wishlist');
            }
        } catch (error) {
            console.error('Error updating wishlist:', error);
            alert('Failed to update wishlist. Please try again.');
        }
    };

    if (productId) {
        loadRecommendations(productId);
        
        const slider = document.querySelector('#recommendationsContainer');
        const prevBtn = document.querySelector('.product-slider-control.prev');
        const nextBtn = document.querySelector('.product-slider-control.next');
        let scrollAmount = 0;

        if (prevBtn && nextBtn && slider) {
            prevBtn.addEventListener('click', () => {
                scrollAmount -= slider.offsetWidth;
                if (scrollAmount < 0) scrollAmount = 0;
                slider.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });

            nextBtn.addEventListener('click', () => {
                scrollAmount += slider.offsetWidth;
                if (scrollAmount >= slider.scrollWidth - slider.offsetWidth) {
                    scrollAmount = slider.scrollWidth - slider.offsetWidth;
                }
                slider.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });
        }
    }

    const weightSelect = document.getElementById('weight-select');
    if (weightSelect) {
        weightSelect.addEventListener('change', function() {
            const selectedProductId = this.value;
            window.location.href = `/product/${selectedProductId}`;
        });
    }
});