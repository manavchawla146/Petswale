// Login-required notification logic for home/search/product pages
// Requires: template to inject window.isAuthenticated (true/false)
// Usage: import this script on pages where login notification is needed

function showLoginRequiredNotification(type) {
    // Remove any existing notification
    const existing = document.querySelector('.login-required-notification');
    if (existing) existing.remove();
    // Create notification
    const notification = document.createElement('div');
    notification.className = 'login-required-notification';
    notification.innerHTML = `
        <span class="notif-icon" style="margin-right:10px;vertical-align:middle;">🔒</span>
        <span class="notif-text">Sign in to ${type === 'cart' ? 'add to cart' : type === 'wishlist' ? 'add to wishlist' : 'continue'}</span>
        <button class="notif-close" aria-label="Close">&times;</button>
    `;
    // Inline styles for lime green + mobile
    notification.style.position = 'fixed';
    notification.style.top = '16px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.background = 'linear-gradient(90deg, #a8ff78 0%, #78ffd6 100%)'; // lime green
    notification.style.color = 'white';
    notification.style.fontWeight = 'bold';
    notification.style.fontSize = '1.1rem';
    notification.style.borderRadius = '18px';
    notification.style.boxShadow = '0 4px 24px rgba(0,0,0,0.12)';
    notification.style.padding = '12px 32px 12px 16px';
    notification.style.zIndex = '9999';
    notification.style.display = 'flex';
    notification.style.alignItems = 'center';
    notification.style.maxWidth = '95vw';
    notification.style.minWidth = '200px';
    notification.style.justifyContent = 'center';
    notification.style.gap = '10px';
    notification.style.transition = 'opacity 0.3s';
    // Mobile
    if (window.innerWidth <= 767) {
        notification.style.width = 'calc(100vw - 32px)';
        notification.style.left = '16px';
        notification.style.right = '16px';
        notification.style.transform = 'none';
        notification.style.top = '10px';
        notification.style.fontSize = '1rem';
        notification.style.padding = '10px 10px 10px 14px';
        notification.style.borderRadius = '14px';
    }
    // Close button
    const closeBtn = notification.querySelector('.notif-close');
    closeBtn.style.background = 'transparent';
    closeBtn.style.border = 'none';
    closeBtn.style.color = 'white';
    closeBtn.style.fontSize = '1.7rem';
    closeBtn.style.marginLeft = '12px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.borderRadius = '50%';
    closeBtn.style.width = '32px';
    closeBtn.style.height = '32px';
    closeBtn.style.display = 'flex';
    closeBtn.style.alignItems = 'center';
    closeBtn.style.justifyContent = 'center';
    closeBtn.onmouseenter = () => closeBtn.style.background = 'rgba(255,255,255,0.12)';
    closeBtn.onmouseleave = () => closeBtn.style.background = 'transparent';
    let closed = false;
    closeBtn.onclick = () => {
        if (!closed) {
            closed = true;
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) notification.remove();
            }, 400);
        }
    };
    // Auto-hide after 5s
    setTimeout(() => {
        if (!closed) {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) notification.remove();
            }, 400);
        }
    }, 5000);
    document.body.appendChild(notification);
}

// Usage example for home page (call this after DOMContentLoaded):
// if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
//   document.querySelectorAll('.product-card').forEach(card => {
//     card.addEventListener('click', function(e) {
//       if (e.target.closest('.add-to-cart') || e.target.closest('.add-to-wishlist')) return;
//       e.preventDefault();
//       showLoginRequiredNotification('cart');
//       setTimeout(() => { window.location.href = '/signin?notify=cart'; }, 1200);
//     });
//     const cartBtn = card.querySelector('.add-to-cart');
//     if (cartBtn) {
//       cartBtn.addEventListener('click', function(e) {
//         e.preventDefault(); e.stopPropagation();
//         showLoginRequiredNotification('cart');
//         setTimeout(() => { window.location.href = '/signin?notify=cart'; }, 1200);
//       });
//     }
//     const wishBtn = card.querySelector('.add-to-wishlist');
//     if (wishBtn) {
//       wishBtn.addEventListener('click', function(e) {
//         e.preventDefault(); e.stopPropagation();
//         showLoginRequiredNotification('wishlist');
//         setTimeout(() => { window.location.href = '/signin?notify=wishlist'; }, 1200);
//       });
//     }
//   });
// }
