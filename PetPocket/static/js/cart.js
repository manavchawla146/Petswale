function updateQuantity(productId, delta) {
  const quantitySpan = document.querySelector(`.cart-item[data-product-id="${productId}"] .quantity-number`);
  let quantity = parseInt(quantitySpan.textContent) + delta;
  
  if (quantity < 1) return;
  
  fetch('/update_cart_item', {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({product_id: productId, quantity: quantity})
  }).then(response => response.json())
  .then(data => {
      if (data.success) {
          // Update the quantity display
          quantitySpan.textContent = quantity;
          
          // Update subtotal, tax, shipping, and total
          if (data.cart_total) {
              document.querySelector('.subtotal').textContent = `Rs.${data.cart_total.subtotal.toFixed(2)}`;
              document.querySelector('.tax').textContent = `Rs.${data.cart_total.tax.toFixed(2)}`;
              document.querySelector('.shipping').textContent = `Rs.${data.cart_total.shipping.toFixed(2)}`;
              document.querySelector('.total-value').textContent = `Rs.${data.cart_total.total.toFixed(2)}`;
          } else {
              location.reload();
          }
          
          // Update cart count in navbar with the total from server
          if (data.cart_count !== undefined) {
              updateNavbarCartCountAbsolute(data.cart_count);
          }
      }
  });
}

// Function to set the absolute cart count
function updateNavbarCartCountAbsolute(totalCount) {
    const cartBadge = document.querySelector('.cart-badge');
    const cartIcon = document.querySelector('.cart-icon');
    
    if (!cartIcon) return;
    
    if (cartBadge) {
        // Update existing badge
        cartBadge.textContent = totalCount;
        
        if (totalCount > 0) {
            cartIcon.classList.add('cart-has-items');
        } else {
            cartIcon.classList.remove('cart-has-items');
        }
    } else if (totalCount > 0) {
        // Create new badge
        const badge = document.createElement('span');
        badge.className = 'cart-badge';
        badge.textContent = totalCount;
        cartIcon.appendChild(badge);
        cartIcon.classList.add('cart-has-items');
    }
}

function removeItem(productId) {
  fetch('/remove_from_cart', {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({product_id: productId})
  }).then(response => response.json())
  .then(data => {
      if (data.success) {
          // Remove the item from the display
          const item = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
          if (item) {
              item.remove();
          }
          
          // Update cart totals
          if (data.cart_total) {
              document.querySelector('.subtotal').textContent = `Rs.${data.cart_total.subtotal.toFixed(2)}`;
              document.querySelector('.tax').textContent = `Rs.${data.cart_total.tax.toFixed(2)}`;
              document.querySelector('.shipping').textContent = `Rs.${data.cart_total.shipping.toFixed(2)}`;
              // Update the selector here too
              document.querySelector('.total-value').textContent = `Rs.${data.cart_total.total.toFixed(2)}`;
              
              // Update cart count in navbar
              const cartBadge = document.querySelector('.cart-badge');
              if (cartBadge) {
                  const currentItems = parseInt(cartBadge.textContent) || 0;
                  if (currentItems > 0) {
                      const newCount = currentItems - 1;
                      cartBadge.textContent = newCount;
                      
                      if (newCount === 0) {
                          document.querySelector('.cart-icon').classList.remove('cart-has-items');
                          cartBadge.remove();
                      }
                  }
              }
              
              // Check if cart is now empty
              const cartItems = document.querySelectorAll('.cart-item');
              if (cartItems.length === 0) {
                  // Update UI for empty cart
                  document.querySelector('.checkout-btn').setAttribute('disabled', true);
                  document.querySelector('.checkout-btn a').classList.add('disabled');
                  
                  // Add empty cart message if not already there
                  if (!document.querySelector('.empty-cart-message')) {
                      const emptyMessage = document.createElement('div');
                      emptyMessage.className = 'empty-cart-message';
                      emptyMessage.textContent = 'Your cart is empty';
                      document.querySelector('.cart-items').appendChild(emptyMessage);
                  }
              }
          } else {
              // If no cart total data is returned, simply reload the page
              location.reload();
          }
      }
  });
}

// Update cart header count on load
document.addEventListener('DOMContentLoaded', () => {
  const cartItems = document.querySelectorAll('.cart-item');
  const itemCount = cartItems.length;
  document.querySelector('.cart-header h1').textContent = 
      `Shopping Cart (${itemCount} ${itemCount === 1 ? 'item' : 'items'})`;
});