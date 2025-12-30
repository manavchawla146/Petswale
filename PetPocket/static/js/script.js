document.addEventListener('DOMContentLoaded', function () {
  // --- LOGIN REQUIRED NOTIFICATION LOGIC FOR HOME PAGE ---
  if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
    document.querySelectorAll('.product-card').forEach(card => {
      // Card click (product detail)
      card.addEventListener('click', function(e) {
        if (e.target.closest('.add-to-cart') || e.target.closest('.add-to-wishlist')) return;
        e.preventDefault();
        window.location.href = '/signin?notify=cart';
      });
      // Add to cart
      const cartBtn = card.querySelector('.add-to-cart');
      if (cartBtn) {
        cartBtn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          window.location.href = '/signin?notify=cart';
        });
      }
      // Add to wishlist
      const wishBtn = card.querySelector('.add-to-wishlist');
      if (wishBtn) {
        wishBtn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          window.location.href = '/signin?notify=wishlist';
        });
      }
    });
  }
  // --- END LOGIN REQUIRED LOGIC ---

   const carousel = document.querySelector('.carousel');
  const slides = document.querySelectorAll('.carousel-slide');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  let currentIndex = 0;

  function animateSlideElements(slide) {
      if (!slide) return;
      const h2 = slide.querySelector('h2');
      const p = slide.querySelector('p');
      const button = slide.querySelector('button');
      const img = slide.querySelector('.pet-image');
      const emojiTopLeft = slide.querySelector('.emoji-top-left');
      const emojiBottomRight = slide.querySelector('.emoji-bottom-right');

      gsap.set([h2, p, button, img], { x: 100, opacity: 0, scale: 0.8 });
      gsap.set(emojiTopLeft, { x: -50, y: -50, opacity: 0, scale: 0.5 });
      gsap.set(emojiBottomRight, { x: 50, y: 50, opacity: 0, scale: 0.5 });

      gsap.to(h2, { x: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'power2.out' });
      gsap.to(p, { x: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'power2.out', delay: 0.2 });
      gsap.to(button, { x: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'power2.out', delay: 0.4 });
      gsap.to(img, { x: 0, opacity: 1, scale: 1, duration: 1, ease: 'power3.out', delay: 0.6 });
      gsap.to(emojiTopLeft, { 
          x: 0, 
          y: 0, 
          opacity: 1, 
          scale: 1, 
          duration: 0.9, 
          ease: 'power2.out', 
          delay: 0.3,
          onComplete: () => {
              gsap.to(emojiTopLeft, { 
                  y: -10, 
                  duration: 1.5, 
                  ease: 'sine.inOut', 
                  repeat: -1, 
                  yoyo: true 
              });
          }
      });
      gsap.to(emojiBottomRight, { 
          x: 0, 
          y: 0, 
          opacity: 1, 
          scale: 1, 
          duration: 0.9, 
          ease: 'power2.out', 
          delay: 0.5,
          onComplete: () => {
              gsap.to(emojiBottomRight, { 
                  y: 10, 
                  duration: 1.5, 
                  ease: 'sine.inOut', 
                  repeat: -1, 
                  yoyo: true 
              });
          }
      });
  }

  function updateCarousel() {
      carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
      animateSlideElements(slides[currentIndex]);
  }

  function goToNextSlide() {
      currentIndex = (currentIndex + 1) % slides.length;
      updateCarousel();
  }

  function goToPrevSlide() {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
      updateCarousel();
  }

  // Only add event listeners if the elements exist
  if (nextBtn && prevBtn) {
    nextBtn.addEventListener('click', goToNextSlide);
    prevBtn.addEventListener('click', goToPrevSlide);
  }

  let autoSlide;
  if (slides.length > 0) {
    autoSlide = setInterval(goToNextSlide, 5000);
  }

  const carouselContainer = document.querySelector('.carousel-container');
  if (carouselContainer) {
    carouselContainer.addEventListener('mouseenter', () => {
      if (autoSlide) clearInterval(autoSlide);
    });
    carouselContainer.addEventListener('mouseleave', () => {
      if (slides.length > 0) {
        autoSlide = setInterval(goToNextSlide, 5000);
      }
    });
  }

  animateSlideElements(slides[currentIndex]);

  
    // FAQ functionality
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            faqItems.forEach(i => i.classList.remove('active'));
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Parallax effect on scroll
    const handleParallax = () => {
        const items = document.querySelectorAll('.faq-item');
        items.forEach(item => {
            const rect = item.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            if (rect.top <= windowHeight * 0.8 && rect.bottom >= 0) {
                item.classList.add('parallax');
                item.style.animation = 'parallaxShift 0.8s ease-out forwards';
            }
        });
    };

    window.addEventListener('scroll', handleParallax);
    window.addEventListener('load', handleParallax);

    // Read More functionality
    const storyContainer = document.getElementById('storyContainer');
    const readMoreBtn = document.getElementById('readMoreBtn');
    if (storyContainer && readMoreBtn) {
        readMoreBtn.addEventListener('click', () => {
            storyContainer.classList.toggle('expanded');
            readMoreBtn.textContent = storyContainer.classList.contains('expanded') ? 'Read Less' : 'Read More';
        });
    }

    // Product sliders functionality
    const productLists = document.querySelectorAll('.product-list');
    productLists.forEach(list => {
        const slider = list.querySelector('.product-cards');
        const prevBtn = list.querySelector('.prev');
        const nextBtn = list.querySelector('.next');
        let scrollAmount = 0;
        const cardWidth = 270; // Width of each card + margin

        if (prevBtn && nextBtn && slider) {
            prevBtn.addEventListener('click', () => {
                scrollAmount = Math.max(scrollAmount - cardWidth, 0);
                slider.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });

            nextBtn.addEventListener('click', () => {
                const maxScroll = slider.scrollWidth - slider.clientWidth;
                scrollAmount = Math.min(scrollAmount + cardWidth, maxScroll);
                slider.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });
        }
    });

    // Helper: Attach login-required listeners to product cards
    function attachLoginListenersToCards(container) {
        if (!container) return;
        container.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.closest('.add-to-cart') || e.target.closest('.add-to-wishlist')) return;
                if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                    e.preventDefault();
                    window.location.href = '/signin?notify=cart';
                }
            });
            const cartBtn = card.querySelector('.add-to-cart');
            if (cartBtn) {
                cartBtn.addEventListener('click', function(e) {
                    if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                        e.preventDefault();
                        e.stopPropagation();
                        window.location.href = '/signin?notify=cart';
                        return;
                    }
                });
            }
            const wishBtn = card.querySelector('.add-to-wishlist');
            if (wishBtn) {
                wishBtn.addEventListener('click', function(e) {
                    if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                        e.preventDefault();
                        e.stopPropagation();
                        window.location.href = '/signin?notify=wishlist';
                        return;
                    }
                });
            }
        });
    }

    // ✅ UPDATED: Fetch and render products with discount price
    function renderProducts(container, products) {
        if (!container) return;
        
        if (products.length === 0) {
            container.innerHTML = '<div class="no-products">No products available.</div>';
            return;
        }

        container.innerHTML = '';
        products.forEach(product => {
            // Generate stars HTML
            const rating = Math.round(product.rating || 0);
            let starsHTML = '';
            for (let i = 1; i <= 5; i++) {
                starsHTML += `<span class="star ${i <= rating ? 'filled' : 'empty'}">★</span>`;
            }
            
            // Generate price HTML based on discount
            let priceHTML = '';
            if (product.discount_price && product.discount_price < product.price) {
                priceHTML = `
                    <div class="price-container">
                        <span class="current-price">₹${product.discount_price.toFixed(2)}</span>
                        <span class="original-price">₹${product.price.toFixed(2)}</span>
                    </div>
                `;
            } else {
                priceHTML = `
                    <div class="price-container">
                        <span class="current-price">₹${product.price.toFixed(2)}</span>
                    </div>
                `;
            }
            
            const card = `
                <div class="product-card" data-product-id="${product.id}">
                    <div class="product-content" onclick="window.location.href='/product/${product.id}'">
                        <img src="${product.image_url || 'https://placehold.co/200x200/46f27a/ffffff?text=Product'}" 
                             alt="${product.name}">
                        <h3 class="product-name" title="${product.name}">${product.name}</h3>
                        
                        <!-- ✅ NEW: Updated price and rating structure -->
                        <div class="product-price-rating">
                            ${priceHTML}
                            <div class="product-rating">
                                <span class="stars">${starsHTML}</span>
                                <span class="review-count">(${product.review_count || 0})</span>
                            </div>
                        </div>
                    </div>
                    <div class="product-actions">
                        <button class="add-to-cart">
                            <span class="material-symbols-outlined add-cart-icon">add_shopping_cart</span> 
                            <span class="cart-txt">Add to Cart</span>
                        </button>
                        <button class="add-to-wishlist">
                            <span class="material-symbols-outlined">favorite</span>
                        </button>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', card);
        });

        // Attach login-required listeners (home/search) after rendering
        if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
            attachLoginListenersToCards(container);
        }
        // Remove any existing authentication required message if present
        const authMsg = container.querySelector('.auth-required-msg');
        if (authMsg) authMsg.remove();

        // Attach event listeners to buttons
        container.querySelectorAll('.add-to-cart').forEach(btn => {
            btn.addEventListener('click', async function(e) {
                e.stopPropagation();
                const card = btn.closest('.product-card');
                const productId = parseInt(card.dataset.productId);
                if (btn.classList.contains('go-to-cart')) {
                    window.location.href = '/cart';
                    return;
                }
                if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                    window.location.href = '/signin?notify=cart';
                    return;
                }
                btn.disabled = true;
                fetch('/add_to_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                    },
                    body: JSON.stringify({ product_id: productId, quantity: 1 })
                })
                .then(response => {
                    if (response.status === 401) {
                        window.location.href = '/signin?notify=cart';
                        return;
                    }
                    return response.json();
                })
                .then(data => {
                    btn.disabled = false;
                    if (data && data.success) {
                        btn.classList.add('go-to-cart');
                        btn.style.backgroundColor = '#4caf50';
                        btn.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> <span class="cart-txt">Go to Cart</span>';
                        updateCartCount(data.cart_count);
                    } else if (data && !data.success) {
                        console.error('Error adding to cart:', data.message);
                    }
                })
                .catch(error => {
                    btn.disabled = false;
                    console.error('Error adding to cart:', error);
                });
            });
        });

        container.querySelectorAll('.add-to-wishlist').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const card = btn.closest('.product-card');
                const productId = parseInt(card.dataset.productId);
                if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                    window.location.href = '/signin?notify=wishlist';
                    return;
                }
                fetch('/add_to_wishlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                    },
                    body: JSON.stringify({ product_id: productId })
                })
                .then(response => {
                    if (response.status === 401) {
                        window.location.href = '/signin?notify=wishlist';
                        return;
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.success) {
                        btn.classList.toggle('in-wishlist');
                        const icon = btn.querySelector('.material-symbols-outlined');
                        if (btn.classList.contains('in-wishlist')) {
                            icon.style.fontVariationSettings = "'FILL' 1";
                        } else {
                            icon.style.fontVariationSettings = "'FILL' 0";
                        }
                    } else if (data && !data.success) {
                        console.error('Error updating wishlist:', data.message);
                    }
                })
                .catch(error => console.error('Error updating wishlist:', error));
            });
        });

        // Update wishlist status
        fetch('/check_wishlist_status')
            .then(response => response.json())
            .then(data => {
                const wishlistItems = data.items || [];
                container.querySelectorAll('.product-card').forEach(card => {
                    const productId = parseInt(card.dataset.productId);
                    const btn = card.querySelector('.add-to-wishlist');
                    const icon = btn.querySelector('.material-symbols-outlined');
                    if (wishlistItems.includes(productId)) {
                        btn.classList.add('in-wishlist');
                        icon.style.fontVariationSettings = "'FILL' 1";
                    } else {
                        btn.classList.remove('in-wishlist');
                        icon.style.fontVariationSettings = "'FILL' 0";
                    }
                });
            });

        // Update cart button state for products already in cart
        fetch('/check_cart_status')
            .then(response => response.json())
            .then(data => {
                const cartItems = data.items || [];
                container.querySelectorAll('.product-card').forEach(card => {
                    const productId = parseInt(card.dataset.productId);
                    if (cartItems.includes(productId)) {
                        const btn = card.querySelector('.add-to-cart');
                        btn.classList.add('go-to-cart');
                        btn.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> <span class="cart-txt">Go to Cart</span>';
                        btn.style.backgroundColor = '#4caf50';
                    } else {
                        const btn = card.querySelector('.add-to-cart');
                        btn.classList.remove('go-to-cart');
                        btn.innerHTML = '<span class="material-symbols-outlined add-cart-icon">add_shopping_cart</span> <span class="cart-txt">Add to Cart</span>';
                        btn.style.backgroundColor = '';
                    }
                });
            });
    }

    // Fetch all home product sections from the new endpoint
    const recommendedContainer = document.getElementById('recommended-products');
    const petParentContainer = document.getElementById('pet-parent-loves');
    const bestSellersContainer = document.getElementById('best-sellers');
    if (recommendedContainer || petParentContainer || bestSellersContainer) {
        fetch('/api/home_products')
            .then(response => response.json())
            .then(data => {
                if (recommendedContainer) {
                    recommendedContainer.innerHTML = '';
                    renderProducts(recommendedContainer, data.recommendations || []);
                }
                if (petParentContainer) {
                    petParentContainer.innerHTML = '';
                    renderProducts(petParentContainer, data.pet_parent_loves || []);
                }
                if (bestSellersContainer) {
                    bestSellersContainer.innerHTML = '';
                    renderProducts(bestSellersContainer, data.best_sellers || []);
                }
            })
            .catch(error => {
                if (recommendedContainer) recommendedContainer.innerHTML = '<div class="error-message">Error loading recommended products.</div>';
                if (petParentContainer) petParentContainer.innerHTML = '<div class="error-message">Error loading products.</div>';
                if (bestSellersContainer) bestSellersContainer.innerHTML = '<div class="error-message">Error loading products.</div>';
                console.error('Error fetching home products:', error);
            });
    }

    // Cart functionality
    function handleAddToCart(productId, button) {
        if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
            window.location.href = '/signin?notify=cart';
            return;
        }
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/signin?notify=cart';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                button.classList.add('added');
                button.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Cart';
                setTimeout(() => {
                    button.classList.remove('added');
                    button.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span>';
                }, 3000);
                updateCartCount(data.cart_count);
            } else if (data && !data.success) {
                console.error('Error adding to cart:', data.message);
            }
        })
        .catch(error => console.error('Error adding to cart:', error));
    }

    // Wishlist functionality
    function handleAddToWishlist(productId, button) {
        if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
            window.location.href = '/signin?notify=wishlist';
            return;
        }
        fetch('/add_to_wishlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/signin?notify=wishlist';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                button.classList.toggle('in-wishlist');
                const icon = button.querySelector('.material-symbols-outlined');
                if (button.classList.contains('in-wishlist')) {
                    icon.style.fontVariationSettings = "'FILL' 1";
                } else {
                    icon.style.fontVariationSettings = "'FILL' 0";
                }
            } else if (data && !data.success) {
                console.error('Error updating wishlist:', data.message);
            }
        })
        .catch(error => console.error('Error updating wishlist:', error));
    }

    // Cart count functionality
    function updateCartCount(count) {
        const cartIcon = document.querySelector('.cart-icon');
        let cartBadge = document.querySelector('.cart-badge');
        // If count is undefined/null/NaN, treat as 1 (first product added)
        let safeCount = (typeof count === 'number' && !isNaN(count)) ? count : 1;
        if (cartIcon) {
            if (!cartBadge) {
                cartBadge = document.createElement('span');
                cartBadge.className = 'cart-badge cart-badge-visible';
                cartIcon.appendChild(cartBadge);
            }
            cartBadge.textContent = safeCount;
            if (safeCount > 0) {
                cartBadge.style.display = 'block';
                cartBadge.classList.add('cart-badge-visible');
                cartIcon.classList.add('cart-has-items');
            } else {
                cartBadge.style.display = 'none';
                cartBadge.classList.remove('cart-badge-visible');
                cartIcon.classList.remove('cart-has-items');
            }
        }
    }

    function fetchAndUpdateCartCount() {
        fetch('/check_cart_status')
            .then(response => response.json())
            .then(data => {
                updateCartCount(data.items.length);
            })
            .catch(error => console.error('Error fetching cart status:', error));
    }

    // Initialize cart count
        fetchAndUpdateCartCount();
    window.addEventListener('pageshow', fetchAndUpdateCartCount);

    // Make functions globally available
    window.handleAddToCart = handleAddToCart;
    window.handleAddToWishlist = handleAddToWishlist;

    /* Add this CSS for wishlist animation */
    if (!document.getElementById('wishlist-animate-style')) {
        const style = document.createElement('style');
        style.id = 'wishlist-animate-style';
        style.textContent = `
        .add-to-wishlist.wishlist-animate {
            animation: wishlist-pop 0.5s;
        }
        @keyframes wishlist-pop {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }
        `;
        document.head.appendChild(style);
    }

    // After rendering products, also update cart/wishlist state on browser back/forward
    window.addEventListener('pageshow', function() {
        // For each product slider, re-fetch cart state and update buttons
        document.querySelectorAll('.product-cards').forEach(container => {
            fetch('/check_cart_status')
                .then(response => response.json())
                .then(data => {
                    const cartItems = data.items || [];
                container.querySelectorAll('.product-card').forEach(card => {
                        const productId = parseInt(card.dataset.productId);
                        const btn = card.querySelector('.add-to-cart');
                        if (btn) {
                            if (cartItems.includes(productId)) {
                                btn.classList.add('go-to-cart');
                                btn.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> <span class="cart-txt">Go to Cart</span>';
                                btn.style.backgroundColor = '#4caf50';
                            } else {
                                btn.classList.remove('go-to-cart');
                                btn.innerHTML = '<span class="material-symbols-outlined add-cart-icon">add_shopping_cart</span> <span class="cart-txt">Add to Cart</span>';
                                btn.style.backgroundColor = '';
                            }
                        }
                    });
                });
            // Also re-fetch wishlist state and update heart fill
            fetch('/check_wishlist_status')
                .then(response => response.json())
                .then(data => {
                    const wishlistItems = data.items || [];
                    container.querySelectorAll('.product-card').forEach(card => {
                        const productId = parseInt(card.dataset.productId);
                        const btn = card.querySelector('.add-to-wishlist');
                        const icon = btn.querySelector('.material-symbols-outlined');
                        if (wishlistItems.includes(productId)) {
                            btn.classList.add('in-wishlist');
                            icon.style.fontVariationSettings = "'FILL' 1";
                        } else {
                            btn.classList.remove('in-wishlist');
                            icon.style.fontVariationSettings = "'FILL' 0";
                        }
                    });
                });
        });
    });

    // Carousel functionality for home page
    const homeCarousel = document.querySelector('.carousel');
const homeSlides = document.querySelectorAll('.carousel-slide');
const homePrevButton = document.getElementById('prevBtn');
const homeNextButton = document.getElementById('nextBtn');
let homeCurrentSlide = 0;
const slideCount = homeSlides.length;
const slideInterval = 5000; // 5 seconds as per your original code

// Clone first and last slides for infinite loop effect
if (slideCount > 0) {
    const firstSlideClone = homeSlides[0].cloneNode(true);
    const lastSlideClone = homeSlides[slideCount - 1].cloneNode(true);
    homeCarousel.appendChild(firstSlideClone);
    homeCarousel.insertBefore(lastSlideClone, homeSlides[0]);

    // Set initial position to account for the cloned last slide
    homeCarousel.style.transform = `translateX(-${100}%)`;
}

// Function to move to a specific slide with sliding animation
function homeShowSlide(index) {
    if (slideCount === 0) return;
    
    // Adjust index for infinite looping
    homeCurrentSlide = (index + slideCount) % slideCount;
    homeCarousel.style.transition = 'transform 0.5s ease-in-out';
    homeCarousel.style.transform = `translateX(-${(homeCurrentSlide + 1) * 100}%)`;
}

// Handle transition end for infinite loop
if (homeCarousel) {
    homeCarousel.addEventListener('transitionend', () => {
        if (homeCurrentSlide === slideCount) {
            homeCarousel.style.transition = 'none';
            homeCurrentSlide = 0;
            homeCarousel.style.transform = `translateX(-${100}%)`;
        } else if (homeCurrentSlide === -1) {
            homeCarousel.style.transition = 'none';
            homeCurrentSlide = slideCount - 1;
            homeCarousel.style.transform = `translateX(-${(homeCurrentSlide + 1) * 100}%)`;
        }
    });
}

// Automatic sliding
let homeAutoSlideTimer;
if (slideCount > 0) {
    homeShowSlide(homeCurrentSlide);
    homeAutoSlideTimer = setInterval(() => {
        homeShowSlide(homeCurrentSlide + 1);
    }, slideInterval);
}

// Function to reset the auto-slide timer
function homeResetTimer() {
    if (slideCount === 0) return;
    clearInterval(homeAutoSlideTimer);
    homeAutoSlideTimer = setInterval(() => {
        homeShowSlide(homeCurrentSlide + 1);
    }, slideInterval);
}

// Manual controls
if (homePrevButton && homeNextButton && slideCount > 0) {
    homePrevButton.addEventListener('click', () => {
        homeShowSlide(homeCurrentSlide - 1);
        homeResetTimer();
    });
    homeNextButton.addEventListener('click', () => {
        homeShowSlide(homeCurrentSlide + 1);
        homeResetTimer();
    });

    // Pause auto-slide on hover
    homeCarousel.addEventListener('mouseenter', () => {
        clearInterval(homeAutoSlideTimer);
    });

    homeCarousel.addEventListener('mouseleave', () => {
        homeResetTimer();
    });
}
    // Testimonial/Review Carousel functionality
    
   const reviewCarousel = document.querySelector('.reviews-carousel');
const reviewCards = document.querySelectorAll('.reviews-carousel .reviews-card');
const reviewPrevBtn = document.getElementById('reviews-prev-btn');
const reviewNextBtn = document.getElementById('reviews-next-btn');
let reviewCurrent = 0;
const cardCount = reviewCards.length;
const cardInterval = 5000; // 5 seconds for auto-play

// Clone first and last cards for infinite loop effect
if (cardCount > 0) {
    const firstCardClone = reviewCards[0].cloneNode(true);
    const lastCardClone = reviewCards[cardCount - 1].cloneNode(true);
    reviewCarousel.appendChild(firstCardClone);
    reviewCarousel.insertBefore(lastCardClone, reviewCards[0]);

    // Set initial position to account for the cloned last card
    reviewCarousel.style.transform = `translateX(-${100}%)`;
}

// Function to show a specific review with sliding animation
function showReview(index) {
    if (cardCount === 0) return;
    
    // Adjust index for infinite looping
    reviewCurrent = (index + cardCount) % cardCount;
    reviewCarousel.style.transition = 'transform 0.5s ease-in-out';
    reviewCarousel.style.transform = `translateX(-${(reviewCurrent + 1) * 100}%)`;
}

// Handle transition end for infinite loop
if (reviewCarousel) {
    reviewCarousel.addEventListener('transitionend', () => {
        if (reviewCurrent === cardCount) {
            reviewCarousel.style.transition = 'none';
            reviewCurrent = 0;
            reviewCarousel.style.transform = `translateX(-${100}%)`;
        } else if (reviewCurrent === -1) {
            reviewCarousel.style.transition = 'none';
            reviewCurrent = cardCount - 1;
            reviewCarousel.style.transform = `translateX(-${(reviewCurrent + 1) * 100}%)`;
        }
    });
}

// Automatic sliding
let autoCardTimer;
if (cardCount > 0) {
    showReview(reviewCurrent);
    autoCardTimer = setInterval(() => {
        showReview(reviewCurrent + 1);
    }, cardInterval);
}

// Function to reset the auto-slide timer
function resetCardTimer() {
    if (cardCount === 0) return;
    clearInterval(autoCardTimer);
    autoCardTimer = setInterval(() => {
        showReview(reviewCurrent + 1);
    }, cardInterval);
}

// Manual controls
if (reviewPrevBtn && reviewNextBtn && cardCount > 0) {
    reviewPrevBtn.addEventListener('click', () => {
        showReview(reviewCurrent - 1);
        resetCardTimer();
    });
    reviewNextBtn.addEventListener('click', () => {
        showReview(reviewCurrent + 1);
        resetCardTimer();
    });

    // Pause auto-slide on hover
    reviewCarousel.addEventListener('mouseenter', () => {
        clearInterval(autoCardTimer);
    });

    reviewCarousel.addEventListener('mouseleave', () => {
        resetCardTimer();
    });
}
});