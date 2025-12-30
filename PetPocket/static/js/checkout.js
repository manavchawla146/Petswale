// checkout.js: Handles address form disabling logic for tablet and laptop/desktop

// Global handler for modal navigation buttons
// Placed at the top to catch all clicks, regardless of DOM state
// Also works if buttons are added dynamically

document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'continueShoppingBtn') {
        e.preventDefault();
        window.location.href = '/';
    }
    if (e.target && e.target.id === 'viewOrderBtn') {
        e.preventDefault();
        window.location.href = '/profile/orders';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Attach event listeners for modal action buttons (works even if modal is dynamically shown)
    document.body.addEventListener('click', function(e) {
        if (e.target && e.target.id === 'continueShoppingBtn') {
            window.location.href = '/';
        }
        if (e.target && e.target.id === 'viewOrderBtn') {
            window.location.href = '/profile/orders';
        }
    });

    // Address form logic (unchanged)
    const addressDropdown = document.getElementById('savedAddresses');
    const billingForm = document.getElementById('billingForm');
    if (addressDropdown && billingForm) {
        billingForm.style.display = 'flex';
        const stateSelect = document.getElementById('state');
        const citySelect = document.getElementById('city');
        let statesCitiesData = {};
        function populateStates() {
            if (!statesCitiesData || !stateSelect) return;
            stateSelect.innerHTML = '<option value=\"\">Select a state...</option>';
            Object.keys(statesCitiesData).forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        }
        function populateCities(state) {
            if (!statesCitiesData || !citySelect) return;
            citySelect.innerHTML = '<option value=\"\">Select a city...</option>';
            if (statesCitiesData[state]) {
                statesCitiesData[state].forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        }
        if (stateSelect && citySelect) {
            fetch('/static/assets/Indian-states-cities.json')
                .then(response => response.json())
                .then(data => {
                    statesCitiesData = data;
                    populateStates();
                });
            stateSelect.addEventListener('change', function() {
                populateCities(this.value);
            });
        }
        const formFields = Array.from(billingForm.elements).filter(el => el.tagName !== 'BUTTON' && el.type !== 'submit');
        
        // Store the currently selected state and city
        let currentState = '';
        let currentCity = '';
        
        function handleAddressChange() {
            const stateSelect = document.getElementById('state');
            const citySelect = document.getElementById('city');
            const selectedOption = addressDropdown.options[addressDropdown.selectedIndex];
            const isNewAddress = selectedOption && selectedOption.value === '';
            
            // Save current selections before any potential reset, but only if we're not already in a new address flow
            if (!isNewAddress) {
                if (stateSelect && stateSelect.value) {
                    currentState = stateSelect.value;
                }
                if (citySelect && citySelect.value) {
                    currentCity = citySelect.value;
                }
            }
            
            if (isNewAddress) {
                // For new address, only reset basic fields and preserve state/city
                const basicFields = ['firstName', 'lastName', 'email', 'phone'];
                basicFields.forEach(field => {
                    const el = document.getElementById(field);
                    if (el) {
                        el.value = el.defaultValue || '';
                    }
                });
                
                document.getElementById('country').value = 'India';
                
                // Restore state and city if they were set
                if (stateSelect && currentState) {
                    // Set the state first
                    stateSelect.value = currentState;
                    // Trigger city population if needed
                    if (currentCity) {
                        // If we have cities for this state, populate them
                        if (statesCitiesData[currentState]) {
                            populateCities(currentState);
                            // Restore city selection after a small delay to allow cities to load
                            setTimeout(() => {
                                if (citySelect) {
                                    const cityOption = Array.from(citySelect.options).find(
                                        opt => opt.value === currentCity
                                    );
                                    if (cityOption) {
                                        citySelect.value = currentCity;
                                    } else if (currentCity) {
                                        // If city doesn't exist in the list, add it
                                        const option = document.createElement('option');
                                        option.value = currentCity;
                                        option.textContent = currentCity;
                                        citySelect.appendChild(option);
                                        citySelect.value = currentCity;
                                    }
                                }
                            }, 300);
                        }
                    }
                }
            } else if (selectedOption && selectedOption.value) {
                // Saved address selected - fetch and populate form
                fetch(`/get_address/${selectedOption.value}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Failed to fetch address');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            const address = data.address;
                            // Populate form fields
                            document.getElementById('firstName').value = address.first_name || '';
                            document.getElementById('lastName').value = address.last_name || '';
                            document.getElementById('phone').value = address.phone || '';
                            document.getElementById('email').value = address.email || '';
                            document.getElementById('addressType').value = address.address_type || 'home';
                            document.getElementById('streetAddress').value = address.street_address || '';
                            document.getElementById('apartment').value = address.apartment || '';
                            document.getElementById('country').value = address.country || 'India';
                            
                            // Handle state and city selection
                            const stateSelect = document.getElementById('state');
                            if (stateSelect && address.state) {
                                stateSelect.value = address.state;
                                const event = new Event('change', { bubbles: true });
                                stateSelect.dispatchEvent(event);
                                setTimeout(() => {
                                    const citySelect = document.getElementById('city');
                                    if (citySelect && address.city) {
                                        // Find the city option that matches (case-insensitive)
                                        const cityOptions = Array.from(citySelect.options);
                                        const cityOption = cityOptions.find(option => 
                                            option.value.toLowerCase() === address.city.toLowerCase());
                                        
                                        if (cityOption) {
                                            citySelect.value = cityOption.value;
                                        } else {
                                            // If exact match not found, try to add it
                                            const newOption = document.createElement('option');
                                            newOption.value = address.city;
                                            newOption.textContent = address.city;
                                            citySelect.appendChild(newOption);
                                            citySelect.value = address.city;
                                        }
                                    }
                                }, 300); // Increased delay for better reliability
                            }
                            
                            document.getElementById('pinCode').value = address.pin_code || '';
                            
                            // Keep form visible but make fields read-only
                            // setFormDisabled(true);  // Remove this call
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching address:', error);
                    });
            }
            // Check if form is valid after address change
            setTimeout(checkAddressFormFilled, 500); // Delay to ensure all fields are updated
        }
        
        addressDropdown.addEventListener('change', handleAddressChange);
        // Remove the resize event listener that was causing the form to reset on mobile
        // window.addEventListener('resize', handleAddressChange);
        handleAddressChange();
    }

    // Complete Order button logic (hardened)
    const proceedToPaymentBtn = document.getElementById('proceedToPayment');
    if (proceedToPaymentBtn) {
        proceedToPaymentBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Check if form is valid before proceeding
            if (this.disabled) {
                return;
            }
            
            proceedToPaymentBtn.disabled = true;
            proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Processing...';
            
            const savedAddresses = document.getElementById('savedAddresses');
            const hasSavedAddresses = savedAddresses && savedAddresses.offsetParent !== null && savedAddresses.options.length > 1;
            
            // Determine if we're using a saved address or entering a new one
            const usingSavedAddress = hasSavedAddresses && savedAddresses.value && savedAddresses.value !== '';
            const usingNewAddress = !usingSavedAddress;
            
            // For new address, validate the form
            if (usingNewAddress) {
                const requiredFields = document.querySelectorAll('#billingForm [required]:not(:disabled)');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('invalid-field');
                    } else {
                        field.classList.remove('invalid-field');
                    }
                });
                
                if (!isValid) {
                    alert('Please fill in all required fields');
                    proceedToPaymentBtn.disabled = false;
                    proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
                    return;
                }
            }
            
            // Prepare order data
            let orderData = {
                address_id: usingSavedAddress ? savedAddresses.value : null
            };
            
            // If using new address, collect form data
            if (usingNewAddress) {
                const getVal = id => {
                    const el = document.getElementById(id);
                    return el ? el.value || '' : '';
                };
                
                orderData.new_address = {
                    first_name: getVal('firstName'),
                    last_name: getVal('lastName'),
                    address_type: getVal('addressType'),
                    street_address: getVal('streetAddress'),
                    apartment: getVal('apartment'),
                    city: getVal('city'),
                    state: getVal('state'),
                    country: getVal('country'),
                    pin_code: getVal('pinCode'),
                    phone: getVal('phone'),
                    email: getVal('email')
                };
            }
            
            // In the fetch to /create_order
            fetch('/create_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name=\"csrf-token\"]')?.getAttribute('content') || ''
                },
                body: JSON.stringify(orderData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Failed to create order');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const options = {
                        key: data.key_id,
                        amount: data.amount,
                        currency: data.currency,
                        name: 'PetPocket',
                        description: 'Order Payment',
                        order_id: data.order_id,
                        handler: function(response) {
                            verifyPayment(response.razorpay_payment_id, response.razorpay_order_id, response.razorpay_signature);
                        },
                        prefill: {
                            name: data.customer_name || '',
                            email: data.customer_email || '',
                            contact: data.customer_phone || ''
                        },
                        theme: {
                            color: '#FF6B6B',
                            hide_topbar: true
                        },
                        modal: {
                            ondismiss: function() {
                                proceedToPaymentBtn.disabled = false;
                                proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
                            }
                        }
                    };
                    const razorpayKey = 'rzp_live_RGkEP4XjZZVrxv';
                    const rzp = new Razorpay(options);
                    rzp.open();
                    proceedToPaymentBtn.disabled = false;
                    proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
                } else {
                    throw new Error(data.message || 'Failed to create order');
                }
            })
            .catch(error => {
                console.error('Order creation error:', error);
                let errorMessage = error.message || 'An unexpected error occurred';
                alert('Error processing your order: ' + errorMessage);
                proceedToPaymentBtn.disabled = false;
                proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
            });
        });
    } else {
        console.warn('Proceed to Payment button not found.');
    }

    // Payment verification logic (unchanged)
    function verifyPayment(paymentId, orderId, signature) {
        console.log('Starting payment verification with:', { paymentId, orderId, signature: signature ? 'present' : 'missing' });
        const proceedToPaymentBtn = document.getElementById('proceedToPayment');
        if (proceedToPaymentBtn) {
            proceedToPaymentBtn.disabled = true;
            proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Verifying Payment...';
        }
        const loadingOverlay = document.createElement('div');
        loadingOverlay.style.position = 'fixed';
        loadingOverlay.style.top = '0';
        loadingOverlay.style.left = '0';
        loadingOverlay.style.width = '100%';
        loadingOverlay.style.height = '100%';
        loadingOverlay.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.justifyContent = 'center';
        loadingOverlay.style.alignItems = 'center';
        loadingOverlay.style.zIndex = '9999';
        loadingOverlay.innerHTML = `
            <div style=\"text-align: center; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);\">
                <div class=\"spinner-border text-primary mb-3\" role=\"status\">
                    <span class=\"visually-hidden\">Loading...</span>
                </div>
                <h5>Verifying your payment...</h5>
                <p>Please wait while we process your payment.</p>
            </div>
        `;
        document.body.appendChild(loadingOverlay);
        fetch('/verify_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name=\"csrf-token\"]').getAttribute('content')
            },
            body: JSON.stringify({
                razorpay_payment_id: paymentId,
                razorpay_order_id: orderId,
                razorpay_signature: signature
            })
        })
        .then(response => {
            console.log('Server response status:', response.status);
            if (!response.ok) {
                return response.json().then(err => {
                    console.error('Verification error details:', err);
                    throw new Error(err.error || 'Payment verification failed');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Verification response data:', data);
            if (loadingOverlay && loadingOverlay.parentNode) {
                loadingOverlay.parentNode.removeChild(loadingOverlay);
            }
            if (!data.success) {
                throw new Error(data.error || 'Payment verification failed');
            }
            if (proceedToPaymentBtn) {
                proceedToPaymentBtn.disabled = false;
                proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
            }
            console.log('Checking for showPaymentSuccess:', typeof window.showPaymentSuccess === 'function');
            if (typeof window.showPaymentSuccess === 'function') {
                console.log('Calling showPaymentSuccess with order_id:', data.order_id);
                window.showPaymentSuccess(data.order_id);
            } else {
                console.log('showPaymentSuccess not found, attempting redirect');
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    window.location.href = '/order-confirmation/' + (data.order_id || '');
                }
            }
        })
        .catch(error => {
            if (loadingOverlay && loadingOverlay.parentNode) {
                loadingOverlay.parentNode.removeChild(loadingOverlay);
            }
            let errorElement = document.getElementById('payment-error');
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.id = 'payment-error';
                errorElement.className = 'alert alert-danger';
                const form = document.querySelector('form');
                if (form) form.prepend(errorElement);
            }
            errorElement.innerHTML = `
                <div class=\"d-flex align-items-center\">
                    <i class=\"fas fa-exclamation-circle me-2\"></i>
                    <div>
                        <strong>Payment Error:</strong> ${error.message || 'An error occurred while verifying your payment. Please contact support if the amount was deducted.'}
                        <div class=\"small\">Please try again or contact support if the issue persists.</div>
                    </div>
                    <button type=\"button\" class=\"btn-close ms-auto\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>
                </div>
            `;
            errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => {
                if (errorElement && errorElement.parentNode) {
                    errorElement.style.transition = 'opacity 0.5s';
                    errorElement.style.opacity = '0';
                    setTimeout(() => {
                        if (errorElement && errorElement.parentNode) {
                            errorElement.parentNode.removeChild(errorElement);
                        }
                    }, 500);
                }
            }, 10000);
            if (proceedToPaymentBtn) {
                proceedToPaymentBtn.disabled = false;
                proceedToPaymentBtn.innerHTML = '<i class=\"fas fa-lock\"></i> Complete Order';
            }
        });
    }

    // Helper function to get effective price (considers discount prices)
    function getEffectivePrice(product) {
        // Use discount price if it exists and is less than regular price
        if (product.discount_price && product.discount_price < product.price) {
            return product.discount_price;
        }
        return product.price;
    }

    // Promo code logic (event delegation for apply/remove)
    const promoInput = document.getElementById('promoCode');
    const promoMessage = document.getElementById('promoMessage');
    const promoCodeContainer = document.querySelector('.promo-code');

    function showPromoMessage(msg, type = 'error') {
        if (!promoMessage) return;
        promoMessage.textContent = msg;
        promoMessage.className = 'promo-message ' + (type || 'error');
    }

    // Helper function to update cart summary display
    function updateCartSummary(cartTotal) {
        // Update subtotal
        const subtotalElement = document.querySelector('.summary-calculations .summary-row:first-child span:last-child');
        if (subtotalElement && cartTotal.subtotal !== undefined) {
            subtotalElement.textContent = `₹${cartTotal.subtotal.toFixed(2)}`;
        }
        
        // Update or create discount row
        if (cartTotal.discount && cartTotal.discount > 0) {
            let discountRow = document.querySelector('.discount-row');
            if (!discountRow) {
                discountRow = document.createElement('div');
                discountRow.className = 'summary-row discount-row';
                discountRow.innerHTML = `<span>Discount</span><span class="discount-amount">-₹${cartTotal.discount.toFixed(2)}</span>`;
                
                const summaryCalculations = document.querySelector('.summary-calculations');
                const firstItem = document.querySelector('.summary-calculations .summary-row:first-child');
                if (summaryCalculations && firstItem) {
                    firstItem.insertAdjacentElement('afterend', discountRow);
                }
            } else {
                discountRow.querySelector('.discount-amount').textContent = `-₹${cartTotal.discount.toFixed(2)}`;
            }
        } else {
            // Remove discount row if discount is 0
            const discountRow = document.querySelector('.discount-row');
            if (discountRow && discountRow.parentNode) {
                discountRow.parentNode.removeChild(discountRow);
            }
        }
        
        // Update shipping
        const shippingElement = document.querySelector('.shipping');
        if (shippingElement && cartTotal.shipping !== undefined) {
            if (cartTotal.shipping === 0) {
                shippingElement.innerHTML = '<span class="free-badge">Free</span>';
            } else {
                shippingElement.textContent = `₹${cartTotal.shipping.toFixed(2)}`;
            }
        }
        
        // Update total
        const totalElement = document.querySelector('.total-value');
        if (totalElement && cartTotal.total !== undefined) {
            totalElement.textContent = `₹${cartTotal.total.toFixed(2)}`;
        }
        
        // Update savings if exists
        const savingsElement = document.querySelector('.saved-amount');
        if (savingsElement && cartTotal.savings !== undefined && cartTotal.savings > 0) {
            savingsElement.textContent = `₹${cartTotal.savings.toFixed(2)}`;
        }
    }

    if (promoCodeContainer) {
        promoCodeContainer.addEventListener('click', function(e) {
            // Remove promo
            if (e.target && e.target.classList.contains('remove-promo')) {
                console.log('Remove promo button clicked');
                const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
                e.target.disabled = true;
                showPromoMessage('Removing promo code...', 'info');
                fetch('/remove_promo_code', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    e.target.disabled = false;
                    if (data.success) {
                        let discountRow = document.querySelector('.discount-row');
                        if (discountRow && discountRow.parentNode) discountRow.parentNode.removeChild(discountRow);
                        const subtotalElement = document.querySelector('.summary-item:nth-child(1) span:last-child');
                        const shippingElement = document.querySelector('.summary-item:nth-child(2) span:last-child');
                        const taxElement = document.querySelector('.summary-item:nth-child(3) span:last-child');
                        const totalElement = document.querySelector('.summary-total span:last-child');
                        if (subtotalElement) subtotalElement.textContent = `₹${data.cart_total.subtotal.toFixed(2)}`;
                        if (shippingElement) shippingElement.textContent = `₹${data.cart_total.shipping.toFixed(2)}`;
                        if (taxElement) taxElement.textContent = `₹${data.cart_total.tax.toFixed(2)}`;
                        if (totalElement) totalElement.textContent = `₹${data.cart_total.total.toFixed(2)}`;
                        promoInput.disabled = false;
                        const applyPromoBtn = document.querySelector('.apply-promo');
                        if (applyPromoBtn) applyPromoBtn.style.display = 'inline-block';
                        // Dynamically remove the remove button
                        const removePromoBtn = document.getElementById('removePromoBtn');
                        if (removePromoBtn && removePromoBtn.parentNode) {
                            removePromoBtn.parentNode.removeChild(removePromoBtn);
                        }
                        promoInput.value = '';
                        showPromoMessage('Promo code removed.', 'success');
                    } else {
                        showPromoMessage(data.message || 'Failed to remove promo code', 'error');
                    }
                })
                .catch(error => {
                    e.target.disabled = false;
                    showPromoMessage('Error removing promo code', 'error');
                });
            }
            // Apply promo
            if (e.target && e.target.classList.contains('apply-promo')) {
                console.log('Apply promo button clicked');
                const promoCode = promoInput.value.trim();
                const csrfToken = document.querySelector('meta[name=\"csrf-token\"]').content;
                if (!promoCode) {
                    showPromoMessage('Please enter a promo code.', 'error');
                    return;
                }
                e.target.disabled = true;
                showPromoMessage('Applying promo code...', 'info');
                fetch('/apply_promo_code', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ promo_code: promoCode })
                })
                .then(response => response.json())
                .then(data => {
                    e.target.disabled = false;
                    if (data.success) {
                        const subtotalElement = document.querySelector('.summary-item:nth-child(1) span:last-child');
                        const shippingElement = document.querySelector('.summary-item:nth-child(3) span:last-child');
                        const taxElement = document.querySelector('.summary-item:nth-child(4) span:last-child');
                        const totalElement = document.querySelector('.summary-total span:last-child');
                        if (subtotalElement) subtotalElement.textContent = `₹${data.cart_total.subtotal.toFixed(2)}`;
                        if (shippingElement) shippingElement.textContent = `₹${data.cart_total.shipping.toFixed(2)}`;
                        if (taxElement) taxElement.textContent = `₹${data.cart_total.tax.toFixed(2)}`;
                        if (totalElement) totalElement.textContent = `₹${data.cart_total.total.toFixed(2)}`;
                        let discountRow = document.querySelector('.discount-row');
                        if (!discountRow) {
                            discountRow = document.createElement('div');
                            discountRow.className = 'summary-item discount-row';
                            discountRow.innerHTML = `<span>Discount</span><span class=\"discount-amount\">-₹${data.cart_total.discount.toFixed(2)}</span>`;
                            const summaryCalculations = document.querySelector('.summary-calculations');
                            if (summaryCalculations) {
                                summaryCalculations.insertBefore(discountRow, document.querySelector('.summary-item:nth-child(3)'));
                            }
                        } else if (discountRow.querySelector('.discount-amount')) {
                            discountRow.querySelector('.discount-amount').textContent = `-₹${data.cart_total.discount.toFixed(2)}`;
                        }
                        promoInput.disabled = true;
                        e.target.style.display = 'none';
                        // Dynamically create remove button if not exists
                        let removePromoBtn = document.getElementById('removePromoBtn');
                        if (!removePromoBtn) {
                            removePromoBtn = document.createElement('button');
                            removePromoBtn.id = 'removePromoBtn';
                            removePromoBtn.className = 'remove-promo';
                            removePromoBtn.type = 'button';
                            removePromoBtn.textContent = 'Remove';
                            promoCodeContainer.appendChild(removePromoBtn);
                        }
                        removePromoBtn.style.display = 'inline-block';
                        showPromoMessage('Promo code applied successfully!', 'success');
                    } else {
                        showPromoMessage(data.message || 'Invalid promo code', 'error');
                    }
                })
                .catch(error => {
                    e.target.disabled = false;
                    showPromoMessage('Error applying promo code', 'error');
                });
            }
        });
    }

    // --- Complete Order button enable/disable logic ---
    const proceedBtn = document.getElementById('proceedToPayment');
    const orderTooltip = document.getElementById('orderTooltip');
    
    function checkAddressFormFilled() {
        if (!billingForm || !proceedBtn) {
            if (proceedBtn) {
                proceedBtn.disabled = false;
                proceedBtn.removeAttribute('title');
            }
            if (orderTooltip) orderTooltip.style.display = 'none';
            return;
        }
        
        // Removed the saved address check - always validate form fields
        // const savedAddresses = document.getElementById('savedAddresses');
        // const hasSavedAddresses = savedAddresses && savedAddresses.offsetParent !== null;
        // const usingSavedAddress = hasSavedAddresses && savedAddresses.value && savedAddresses.value !== '';
        // if (usingSavedAddress) { ... }  // Remove this block
        
        // Check if all required fields are filled
        const requiredFields = billingForm.querySelectorAll('[required]:not(:disabled)');
        let isValid = true;
        let missingFields = [];
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('invalid-field');
                missingFields.push(field.labels?.[0]?.textContent.replace('*', '').trim() || field.name);
            } else {
                field.classList.remove('invalid-field');
            }
        });
        
        if (!isValid) {
            if (proceedBtn) {
                proceedBtn.disabled = true;
                const missingFieldsText = missingFields.length > 2 ? 
                    `Missing fields: ${missingFields.slice(0, 2).join(', ')} and ${missingFields.length - 2} more` : 
                    `Missing: ${missingFields.join(', ')}`;
                proceedBtn.setAttribute('title', missingFieldsText);
            }
            if (orderTooltip) {
                orderTooltip.textContent = missingFields.length > 2 ? 
                    `Please fill in ${missingFields.slice(0, 2).join(', ')} and ${missingFields.length - 2} more fields` : 
                    `Please fill in ${missingFields.join(', ')}`;
                orderTooltip.style.display = 'inline-block';
            }
        } else {
            if (proceedBtn) {
                proceedBtn.disabled = false;
                proceedBtn.removeAttribute('title');
            }
            if (orderTooltip) orderTooltip.style.display = 'none';
        }
    }
    
    if (billingForm && proceedBtn) {
        billingForm.addEventListener('input', checkAddressFormFilled);
        billingForm.addEventListener('change', checkAddressFormFilled);
        // Initial check
        setTimeout(checkAddressFormFilled, 500); // Delay to ensure all fields are loaded
    }
});