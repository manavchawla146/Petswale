document.addEventListener('DOMContentLoaded', function () {
  const carousel = document.querySelector('.carousel');
  const slides = document.querySelectorAll('.slide');
  const prevButton = document.querySelector('.carousel-control.prev');
  const nextButton = document.querySelector('.carousel-control.next');
  let currentSlide = 0;

  function showSlide(index) {
    slides.forEach(slide => {
      slide.classList.remove('active');
      slide.style.transform = ''; // Reset transform
    });
    slides[index].classList.add('active');
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  }

  /* @tweakable Time in seconds between automatic slides */
  const autoSlideInterval = 5;
  let autoSlideTimer = setInterval(nextSlide, autoSlideInterval * 1000);

  function resetTimer() {
    clearInterval(autoSlideTimer);
    autoSlideTimer = setInterval(nextSlide, autoSlideInterval * 1000);
  }

  prevButton.addEventListener('click', () => {
    prevSlide();
    resetTimer();
  });

  nextButton.addEventListener('click', () => {
    nextSlide();
    resetTimer();
  });

  showSlide(currentSlide);

  // Product slider functionality
  const productSlider = document.querySelector('.product-slider');
  const productCards = document.querySelector('.product-cards');
  const productCardWidth = 270; // Adjusted width to include margin for smoother transition
  const prevProductButton = document.querySelector('.product-slider-control.prev');
  const nextProductButton = document.querySelector('.product-slider-control.next');
  const productModal = document.getElementById('productModal');
  const productDetailsContainer = document.querySelector('.product-details-container');

  /* @tweakable Duration for the product details to appear */
  const modalAnimationDuration = 0.3;

  /* @tweakable the color of the add to cart button when its been clicked */
  const addToCartButtonColor = "#46f27a";

  /* @tweakable the color of the heart/wishlist button when clicked */
  const wishlistButtonColor = "pink";

  function openProductModal(productId) {
    // Fetch product details (replace with your actual data source)
    const productDetails = getProductDetails(productId);

    // Populate modal content
    productDetailsContainer.innerHTML = `
      <div class="product-details-grid">
        <div class="product-image-container">
          <img src="${productDetails.image}" alt="${productDetails.name}" class="product-image">
        </div>
        <div class="product-info">
          <h3>${productDetails.name}</h3>
          <p>${productDetails.description}</p>
          <p class="product-price">Price: ${productDetails.price}</p>
          <p class="product-rating">Rating: ${productDetails.rating}</p>
          <div class="quantity-selector">
            <button class="quantity-button">-</button>
            <input type="number" value="1" min="1">
            <button class="quantity-button">+</button>
          </div>
          <div class="product-actions">
            <button class="add-to-cart">
              <span class="material-symbols-outlined">shopping_cart</span> Add to Cart
            </button>
            <button class="add-to-wishlist">
              <span class="material-symbols-outlined">favorite</span>
            </button>
          </div>
        </div>
      </div>
        `;
    const addToCartButton = productDetailsContainer.querySelector('.add-to-cart');
    const addToWishlistButton = productDetailsContainer.querySelector('.add-to-wishlist');

    addToCartButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent modal from opening when clicking the button
        addToCartButton.innerHTML = '<span class="material-symbols-outlined">done</span> Added to Cart';
        addToCartButton.style.backgroundColor = addToCartButtonColor;
        /* @tweakable the length of time in seconds before the added to cart resets */
        const resetButtonTimeout = 2;
        setTimeout(() => {
          addToCartButton.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> Add to Cart';
          addToCartButton.style.backgroundColor = '#FF6B6B';
        }, resetButtonTimeout * 1000);
      });

      addToWishlistButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent modal from opening when clicking the button
        if (addToWishlistButton.style.color === wishlistButtonColor) {
          addToWishlistButton.style.color = '#555';
        } else {
          addToWishlistButton.style.color = wishlistButtonColor;
        }
      });

    const minusButton = productDetailsContainer.querySelector('.quantity-button:first-of-type');
    const plusButton = productDetailsContainer.querySelector('.quantity-button:last-of-type');
    const input = productDetailsContainer.querySelector('input[type="number"]');

    minusButton.addEventListener('click', () => {
      if (input.value > 1) {
        input.value = parseInt(input.value) - 1;
      }
    });

    plusButton.addEventListener('click', () => {
      input.value = parseInt(input.value) + 1;
    });
    productModal.style.display = "block";

     /* @tweakable Set focus on the modal on open */
     productModal.focus();
  }

  // Dummy function to simulate fetching product details
  function getProductDetails(productId) {
    // Replace this with actual data fetching logic
    switch (productId) {
      case '1':
        return {
          name: "Hill's Science Diet Adult Sensitive Stomach",
          image: "/a/69079b36-bc18-48e0-8f54-b9fdfc21d2f4",
          description: "Formulated for adult dogs with sensitive stomachs.",
          price: "$74.09",
          rating: "★★★★★ (1)"
        };
      case '2':
        return {
          name: "Product Name 2",
          image: "https://placehold.co/200x200/46f27a/ffffff?text=Product",
          description: "Description for Product 2.",
          price: "$29.99",
          rating: "★★★★☆ (4)"
        };
      case '3':
        return {
          name: "Product Name 3",
          image: "https://placehold.co/200x200/46f27a/ffffff?text=Product",
          description: "Description for Product 3.",
          price: "$49.50",
          rating: "★★★☆☆ (3)"
        };
      case '4':
        return {
          name: "Product Name 4",
          image: "https://placehold.co/200x200/46f27a/ffffff?text=Product",
          description: "Description for Product 4.",
          price: "$19.99",
          rating: "★★★★★ (5)"
        };
      case '5':
        return {
          name: "Product Name 5",
          image: "https://placehold.co/200x200/46f27a/ffffff?text=Product",
          description: "Description for Product 5.",
          price: "$35.50",
          rating: "★★★★☆ (4)"
        };
      case '6':
        return {
          name: "Product Name 6",
          image: "https://placehold.co/200x200/46f27a/ffffff?text=Product",
          description: "Description for Product 6.",
          price: "$55.00",
          rating: "★★★★★ (5)"
        };
      default:
        return {
          name: "Product Not Found",
          image: "https://placehold.co/200x200/aaaaaa/ffffff?text=Not+Found",
          description: "Product details could not be loaded.",
          price: "N/A",
          rating: "N/A"
        };
    }
  }

  // Event listeners
  if (productSlider && productCards) {
    productCards.addEventListener('click', (event) => {
      const card = event.target.closest('.product-card');
      if (card) {
        const productId = card.dataset.productId;
        openProductModal(productId);
      }
    });
  }

  const closeButton = document.querySelector('.close-button');
  closeButton.addEventListener('click', function closeProductModal() {
    productModal.style.display = "none";
  });

  // Close the modal if the user clicks outside of it
  window.addEventListener('click', (event) => {
    if (event.target == productModal) {
      closeProductModal();
    }
  });

  if (productSlider && productCards) {
    // Smooth scroll polyfill (for Safari)
    productCards.style.scrollBehavior = 'smooth';

    if (prevProductButton && nextProductButton) {
      prevProductButton.addEventListener('click', () => {
        productCards.scrollLeft -= productCardWidth;
      });

      nextProductButton.addEventListener('click', () => {
        productCards.scrollLeft += productCardWidth;
      });
    } else {
      console.warn('Previous and Next buttons not found for product slider.');
    }

    document.querySelectorAll('.product-card').forEach(card => {
      const addToCartButton = card.querySelector('.add-to-cart');
      const addToWishlistButton = card.querySelector('.add-to-wishlist');

      addToCartButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent modal from opening when clicking the button
        addToCartButton.innerHTML = '<span class="material-symbols-outlined">done</span> Added to Cart';
        addToCartButton.style.backgroundColor = addToCartButtonColor;
        /* @tweakable the length of time in seconds before the added to cart resets */
        const resetButtonTimeout = 2;
        setTimeout(() => {
          addToCartButton.innerHTML = '<span class="material-symbols-outlined">shopping_cart</span> Add to Cart';
          addToCartButton.style.backgroundColor = '#FF6B6B';
        }, resetButtonTimeout * 1000);
      });

      addToWishlistButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent modal from opening when clicking the button
        if (addToWishlistButton.style.color === wishlistButtonColor) {
          addToWishlistButton.style.color = '#555';
        } else {
          addToWishlistButton.style.color = wishlistButtonColor;
        }
      });
    });
  } else {
    console.error('Product slider elements not found.');
  }

  // Remove controls in mobile view
  function checkScreenWidth() {
    if (window.innerWidth <= 768) {
      if (prevProductButton) prevProductButton.style.display = 'none';
      if (nextProductButton) nextProductButton.style.display = 'none';
    } else {
      if (prevProductButton) prevProductButton.style.display = 'block';
      if (nextProductButton) nextProductButton.style.display = 'block';
    }
  }

  // Initial check and listener for screen width changes
  checkScreenWidth();
  window.addEventListener('resize', checkScreenWidth);

  // Quantity selector functionality
  document.querySelectorAll('.quantity-selector').forEach(selector => {
    const minusButton = selector.querySelector('.quantity-button:first-of-type');
    const plusButton = selector.querySelector('.quantity-button:last-of-type');
    const input = selector.querySelector('input[type="number"]');

    minusButton.addEventListener('click', () => {
      if (input.value > 1) {
        input.value = parseInt(input.value) - 1;
      }
    });

    plusButton.addEventListener('click', () => {
      input.value = parseInt(input.value) + 1;
    });
  });

  // Function to navigate to checkout page
  function goToCheckout() {
    window.location.href = 'checkout.html'; // Replace with your checkout page URL
  }

  // Function to navigate to profile page
  /* @tweakable add or remove the profile page */
  function goToProfile() {
    window.location.href = 'profile.html'; 
  }

  /* @tweakable the page to navigate to show wishlist */
  function goToWishlist() {
    window.location.href = 'wishlist.html';
  }
});