document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-button');
    const productCards = document.querySelectorAll('.product-card');
    const sortSelect = document.getElementById('sort');

    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            productCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                if (filter === 'all' || cardCategory === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Sort functionality
    sortSelect.addEventListener('change', function() {
        const sortValue = this.value;
        const productGrid = document.querySelector('.product-grid');
        const cardsArray = Array.from(productCards);

        cardsArray.sort((a, b) => {
            const aPrice = parseFloat(a.querySelector('.product-price').textContent.replace('$', ''));
            const bPrice = parseFloat(b.querySelector('.product-price').textContent.replace('$', ''));
            const aName = a.querySelector('h3').textContent.toLowerCase();
            const bName = b.querySelector('h3').textContent.toLowerCase();

            switch (sortValue) {
                case 'price-low-to-high':
                    return aPrice - bPrice;
                case 'price-high-to-low':
                    return bPrice - aPrice;
                case 'name-a-to-z':
                    return aName.localeCompare(bName);
                case 'name-z-to-a':
                    return bName.localeCompare(aName);
                default:
                    return 0;
            }
        });

        // Clear and re-append sorted cards
        productGrid.innerHTML = '';
        cardsArray.forEach(card => productGrid.appendChild(card));
    });

    // Add to cart functionality
    window.addToCart = function(productId) {
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const button = document.querySelector(`.product-card[data-product-id="${productId}"] .add-to-cart`);
                button.classList.add('added-to-cart');
                button.textContent = 'Added to Cart';
                alert(data.message);
            } else {
                alert('Error adding to cart');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding to cart');
        });
    };

    // Wishlist functionality
    window.toggleWishlist = function(productId, button) {
        fetch('/check_wishlist_status')
            .then(response => response.json())
            .then(data => {
                const isInWishlist = data.items.includes(productId);
                const endpoint = isInWishlist ? '/remove_from_wishlist' : '/add_to_wishlist';
                
                return fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ product_id: productId })
                });
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.classList.toggle('active');
                    alert(data.message);
                } else if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error toggling wishlist');
            });
    };

    // Check initial wishlist status
    fetch('/check_wishlist_status')
        .then(response => response.json())
        .then(data => {
            productCards.forEach(card => {
                const productId = parseInt(card.getAttribute('data-product-id'));
                if (data.items.includes(productId)) {
                    card.querySelector('.add-to-wishlist').classList.add('active');
                }
            });
        });

    // Check initial cart status
    fetch('/check_cart_status')
        .then(response => response.json())
        .then(data => {
            productCards.forEach(card => {
                const productId = parseInt(card.getAttribute('data-product-id'));
                if (data.items.includes(productId)) {
                    const button = card.querySelector('.add-to-cart');
                    button.classList.add('added-to-cart');
                    button.textContent = 'Added to Cart';
                }
            });
        });
});