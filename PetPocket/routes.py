from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import PetType, Product, Category, WishlistItem, CartItem, Order
from .models import OrderItem, ProductAnalytics, Address, ProductImage, ProductView, Review
from . import db
from flask import current_app
from . import razorpay_client
from datetime import datetime
from sqlalchemy import func, desc

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    pet_types = PetType.query.all()
    return render_template("home.html", pet_types=pet_types)

@main.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("signin.html")

# Search routes
@main.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    products = Product.query.filter(
        Product.name.ilike(f'%{query}%') |
        Product.description.ilike(f'%{query}%')
    ).all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': float(p.price),
        'stock': p.stock,
        'image_url': p.image_url
    } for p in products])

@main.route('/search')
def search():
    return render_template('search.html')

# Profile routes
@main.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.timestamp.desc()).all()
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', 
                          orders=orders,
                          wishlist_items=wishlist_items,
                          reviews=reviews,
                          addresses=addresses)

# Product routes
@main.route('/products/<int:pet_type_id>')
def products(pet_type_id):
    pet_type = PetType.query.get_or_404(pet_type_id)
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(pet_type_id=pet_type_id).paginate(page=page, per_page=16, error_out=False)
    categories = Category.query.all()
    return render_template('product-listing.html',
                          products=products,
                          pet_type=pet_type,
                          categories=categories)

@main.route('/get_product_details/<int:product_id>')
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'image_url': product.image_url,
        'category': product.category.name if product.category else None,
        'pet_type': product.pet_type.name if product.pet_type else None
    })

# Advanced Recommendation Algorithm
def get_advanced_recommendations(user_id=None, limit=5):
    recommendations = []
    scored_products = {}
    product_ids_added = set()

    weights = {
        'collaborative': 0.4,
        'content': 0.3,
        'popularity': 0.3
    }

    if user_id:
        user_views = ProductView.query.filter_by(user_id=user_id).subquery()
        similar_users = db.session.query(ProductView.user_id).filter(
            ProductView.product_id.in_(db.session.query(user_views.c.product_id)),
            ProductView.user_id != user_id
        ).subquery()

        collaborative_products = db.session.query(
            ProductView.product_id, func.count(ProductView.id).label('view_count')
        ).filter(
            ProductView.user_id.in_(similar_users),
            ProductView.product_id.notin_(db.session.query(user_views.c.product_id))
        ).group_by(ProductView.product_id).order_by(desc('view_count')).limit(limit * 2).all()

        for product_id, score in collaborative_products:
            product = Product.query.get(product_id)
            if product and product.stock > 0 and product.id not in product_ids_added:
                scored_products[product.id] = scored_products.get(product.id, 0) + (score * weights['collaborative'])

        co_purchased_product_ids = db.session.query(
            OrderItem.product_id, func.count(OrderItem.id).label('purchase_count')
        ).join(
            Order, Order.id == OrderItem.order_id
        ).filter(
            Order.id.in_(
                db.session.query(OrderItem.order_id).filter(
                    OrderItem.product_id.in_(db.session.query(user_views.c.product_id))
                )
            ),
            OrderItem.product_id.notin_(db.session.query(user_views.c.product_id))
        ).group_by(OrderItem.product_id).order_by(desc('purchase_count')).limit(limit * 2).all()

        for product_id, score in co_purchased_product_ids:
            product = Product.query.get(product_id)
            if product and product.stock > 0 and product.id not in product_ids_added:
                scored_products[product.id] = scored_products.get(product.id, 0) + (score * weights['collaborative'])

    if user_id:
        user_products = db.session.query(Product).join(
            ProductView, Product.id == ProductView.product_id
        ).filter(ProductView.user_id == user_id).all()
        preferred_categories = set(p.category_id for p in user_products)
        preferred_pet_types = set(p.pet_type_id for p in user_products)

        content_products = Product.query.filter(
            Product.category_id.in_(preferred_categories) | Product.pet_type_id.in_(preferred_pet_types),
            Product.stock > 0
        ).order_by(func.random()).limit(limit * 2).all()

        for product in content_products:
            if product.id not in product_ids_added:
                score = 0
                if product.category_id in preferred_categories:
                    score += 0.6
                if product.pet_type_id in preferred_pet_types:
                    score += 0.4
                scored_products[product.id] = scored_products.get(product.id, 0) + (score * weights['content'])

    popular_products = db.session.query(
        Product.id, func.sum(ProductAnalytics.view_count + ProductAnalytics.purchase_count).label('popularity')
    ).join(
        ProductAnalytics, Product.id == ProductAnalytics.product_id
    ).filter(
        Product.stock > 0
    ).group_by(Product.id).order_by(desc('popularity')).limit(limit * 2).all()

    for product_id, score in popular_products:
        if product_id not in product_ids_added:
            scored_products[product_id] = scored_products.get(product_id, 0) + (score * weights['popularity'])

    for product_id, score in sorted(scored_products.items(), key=lambda x: x[1], reverse=True):
        product = Product.query.get(product_id)
        if product and product.id not in product_ids_added:
            recommendations.append(product)
            product_ids_added.add(product.id)
            if len(recommendations) >= limit:
                break

    if len(recommendations) < limit:
        fallback_products = Product.query.filter(
            Product.stock > 0,
            Product.id.notin_(product_ids_added)
        ).order_by(func.random()).limit(limit - len(recommendations)).all()
        recommendations.extend(fallback_products)

    return recommendations[:limit]

@main.route('/api/home_recommendations')
def home_recommendations():
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        recommendations = get_advanced_recommendations(user_id=user_id, limit=5)
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'image_url': p.image_url,
            'category': p.category.name,
            'pet_type': p.pet_type.name,
            'rating': round(sum(r.rating for r in p.reviews) / len(p.reviews), 1) if p.reviews else 0,
            'review_count': len(p.reviews)
        } for p in recommendations])
    except Exception as e:
        current_app.logger.error(f"Home recommendation error: {str(e)}")
        return jsonify([])

def get_recommended_products(product_id, limit=4):
    current_product = Product.query.get(product_id)
    if not current_product:
        return []

    user_id = current_user.id if current_user.is_authenticated else None
    recommendations = get_advanced_recommendations(user_id=user_id, limit=limit * 2)

    filtered_recommendations = [
        p for p in recommendations
        if p.id != product_id and (
            p.category_id == current_product.category_id or
            p.pet_type_id == current_product.pet_type_id
        )
    ]

    if len(filtered_recommendations) < limit:
        filtered_recommendations.extend([
            p for p in recommendations
            if p.id != product_id and p not in filtered_recommendations
        ])

    return filtered_recommendations[:limit]

@main.route('/api/recommendations/<int:product_id>')
def get_recommendations(product_id):
    try:
        recommendations = get_recommended_products(product_id, limit=4)
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'image_url': p.image_url,
            'category': p.category.name,
            'pet_type': p.pet_type.name
        } for p in recommendations])
    except Exception as e:
        current_app.logger.error(f"Recommendation error: {str(e)}")
        return jsonify([])

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    additional_images = ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.display_order).all()
    
    if product.parent:
        master_product = product.parent
    else:
        master_product = product
    variants = [master_product] + list(master_product.variants)
    variants = sorted(variants, key=lambda x: x.weight or 0)
    
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    total_reviews = len(reviews)
    avg_rating = 0
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    if total_reviews > 0:
        total_rating = sum(review.rating for review in reviews)
        avg_rating = round(total_rating / total_reviews, 1)
        for review in reviews:
            rating_counts[review.rating] = rating_counts.get(review.rating, 0) + 1

    if current_user.is_authenticated:
        ProductAnalytics.increment_view(product_id)
        product_view = ProductView.query.filter_by(
            product_id=product_id,
            user_id=current_user.id
        ).first()
        
        if not product_view:
            product_view = ProductView(
                product_id=product_id,
                user_id=current_user.id
            )
            db.session.add(product_view)
            db.session.commit()
    else:
        ip_address = request.remote_addr
        if ip_address:
            ProductAnalytics.increment_view(product_id)
            product_view = ProductView(
                product_id=product_id,
                ip_address=ip_address
            )
            db.session.add(product_view)
            db.session.commit()
    
    return render_template('product-detail.html', 
                         product=product, 
                         variants=variants,
                         additional_images=additional_images,
                         reviews=reviews,
                         total_reviews=total_reviews,
                         avg_rating=avg_rating,
                         rating_counts=rating_counts)

@main.route('/api/reviews/add', methods=['POST'])
@login_required
def add_review():
    data = request.json
    product_id = data.get('product_id')
    rating = data.get('rating')
    content = data.get('content')
    
    if not all([product_id, rating, content]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing_review:
        existing_review.rating = rating
        existing_review.content = content
        existing_review.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'id': existing_review.id,
            'rating': existing_review.rating,
            'content': existing_review.content,
            'created_at': existing_review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': existing_review.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': current_user.username,
            'message': 'Review updated successfully'
        })
    
    review = Review(
        product_id=product_id,
        user_id=current_user.id,
        rating=rating,
        content=content
    )
    
    db.session.add(review)
    db.session.commit()
    
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    total_reviews = len(reviews)
    avg_rating = round(sum(r.rating for r in reviews) / total_reviews, 1) if total_reviews > 0 else 0
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews:
        rating_counts[r.rating] += 1

    return jsonify({
        'id': review.id,
        'rating': review.rating,
        'content': review.content,
        'created_at': review.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
        'user': current_user.username,
        'average_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_counts': rating_counts,
        'message': 'Review added successfully'
    })

# Wishlist routes
@main.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in wishlist_items]
    return render_template('wishlist.html', products=products)

@main.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    if not current_user.is_authenticated:
        flash('Please login to add items to your wishlist', 'info')
        return jsonify({'success': False, 'redirect': url_for('main.signin')}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    
    try:
        if not WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first():
            wishlist_item = WishlistItem(user_id=current_user.id, product_id=product_id)
            db.session.add(wishlist_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Added to wishlist'})
        return jsonify({'success': True, 'message': 'Already in wishlist'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/check_wishlist_status')
@login_required
def check_wishlist_status():
    if not current_user.is_authenticated:
        return jsonify({'items': []})
    
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    wishlist_product_ids = [item.product_id for item in wishlist_items]
    return jsonify({'items': wishlist_product_ids})

@main.route('/remove_from_wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    data = request.get_json()
    product_id = data.get('product_id')
    
    try:
        wishlist_item = WishlistItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Removed from wishlist'})
        return jsonify({'success': False, 'message': 'Item not found in wishlist'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Cart routes
@main.route('/cart')
def cart():
    cart_items = []
    subtotal = 0
    tax = 0
    shipping = 0
    total = 0

    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        tax = subtotal * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal + tax + shipping

    return render_template('cart.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)

@main.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    
    cart_count = db.session.query(func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    
    return jsonify({
        'success': True, 
        'message': 'Product added to cart',
        'cart_count': int(cart_count)
    })

@main.route('/update_cart_item', methods=['PUT'])
@login_required
def update_cart_item():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first_or_404()
    cart_item.quantity = quantity
    db.session.commit()
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * 0.05
    shipping = 40 if subtotal < 500 else 0
    total = subtotal + tax + shipping
    
    cart_count = CartItem.query.with_entities(func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    
    return jsonify({
        'success': True,
        'cart_total': {
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'total': total
        },
        'cart_count': cart_count
    })

@main.route('/remove_from_cart', methods=['DELETE'])
@login_required
def remove_from_cart():
    product_id = request.json.get('product_id')
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        tax = subtotal * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal + tax + shipping
        
        return jsonify({
            'success': True,
            'cart_total': {
                'subtotal': subtotal,
                'tax': tax,
                'shipping': shipping,
                'total': total
            }
        })
    
    return jsonify({'success': False}), 404

# Checkout routes
@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * 0.10
    shipping = 5.00 if cart_items else 0
    total = subtotal + tax + shipping
    
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    default_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
    
    if request.method == 'POST':
        try:
            address_data = {
                'user_id': current_user.id,
                'address_type': request.form.get('addressType', 'home'),
                'company_name': request.form.get('companyName'),
                'street_address': request.form.get('streetAddress'),
                'apartment': request.form.get('apartment'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'country': request.form.get('country'),
                'pin_code': request.form.get('pinCode'),
                'is_default': request.form.get('setAsDefault') == 'on'
            }
            
            if address_data['is_default']:
                Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
            
            new_address = Address(**address_data)
            db.session.add(new_address)
            db.session.commit()
            
            flash('Address saved successfully!', 'success')
            return redirect(url_for('main.checkout'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving address: {str(e)}', 'danger')
    
    return render_template('checkout.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total,
                         addresses=addresses,
                         default_address=default_address,
                         user=current_user)

@main.route('/get_address/<int:address_id>')
@login_required
def get_address(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
    
    if not address:
        return jsonify({'success': False, 'message': 'Address not found'}), 404
        
    return jsonify({
        'success': True,
        'address': {
            'id': address.id,
            'first_name': current_user.username.split()[0] if current_user.username else '',
            'last_name': current_user.username.split()[1] if current_user.username and ' ' in current_user.username else '',
            'address_type': address.address_type,
            'company_name': address.company_name,
            'street_address': address.street_address,
            'apartment': address.apartment,
            'city': address.city,
            'state': address.state,
            'country': address.country,
            'pin_code': address.pin_code,
            'phone': current_user.phone,
            'email': current_user.email,
            'is_default': address.is_default
        }
    })

@main.route('/check_cart_status')
def check_cart_status():
    if not current_user.is_authenticated:
        return jsonify({'items': []})
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_product_ids = [item.product_id for item in cart_items]
    return jsonify({'items': cart_product_ids})

# Payment routes
@main.route('/create_order', methods=['POST'])
@login_required
def create_order():
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        tax = subtotal * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal + tax + shipping
        
        data = {
            'amount': int(total * 100),
            'currency': 'INR',
            'receipt': f'order_rcptid_{current_user.id}_{datetime.now().timestamp()}',
            'payment_capture': '1'
        }
        
        order = razorpay_client.order.create(data=data)
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'amount': data['amount'],
            'currency': data['currency'],
            'key': current_app.config['RAZORPAY_KEY_ID']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/payment_callback', methods=['POST'])
@login_required
def payment_callback():
    try:
        payment_id = request.form.get('razorpay_payment_id')
        order_id = request.form.get('razorpay_order_id')
        signature = request.form.get('razorpay_signature')
        
        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }
        
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        tax = subtotal * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal + tax + shipping
        
        order = Order(
            user_id=current_user.id,
            total_price=total,
            payment_id=payment_id,
            order_id=order_id,
            payment_status='completed'
        )
        db.session.add(order)
        db.session.commit()
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.product.price
            )
            db.session.add(order_item)
            
            ProductAnalytics.increment_purchase(cart_item.product_id, cart_item.quantity)
            
            product = cart_item.product
            product.stock -= cart_item.quantity
            
            db.session.delete(cart_item)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Payment successful', 'order_id': order.id})
        
    except Exception as e:
        db.session.rollback()
        print(f"Payment verification error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/track/product-view/<int:product_id>')
def track_product_view(product_id):
    if current_user.is_authenticated:
        ProductAnalytics.increment_view(product_id)
    return jsonify({'status': 'success'})

@main.route('/track/cart-add/<int:product_id>')
@login_required
def track_cart_add(product_id):
    ProductAnalytics.increment_cart_add(product_id)
    return jsonify({'status': 'success'})

@main.route('/api/pet_parent_loves')
def pet_parent_loves():
    loved_products = db.session.query(
        Product,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).join(
        Review, Product.id == Review.product_id
    ).group_by(
        Product.id
    ).having(
        func.count(Review.id) >= 3
    ).order_by(
        func.avg(Review.rating).desc()
    ).limit(5).all()
    
    return jsonify([{
        'id': p.Product.id,
        'name': p.Product.name,
        'price': float(p.Product.price),
        'image_url': p.Product.image_url,
        'category': p.Product.category.name if p.Product.category else None,
        'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
        'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
        'review_count': p.review_count
    } for p in loved_products])

@main.route('/api/best_sellers')
def best_sellers():
    best_sellers = db.session.query(
        Product,
        func.coalesce(func.sum(ProductAnalytics.purchase_count), 0).label('total_purchases'),
        func.avg(Review.rating).label('avg_rating'),
        func.coalesce(func.count(Review.id), 0).label('review_count')
    ).outerjoin(
        ProductAnalytics, Product.id == ProductAnalytics.product_id
    ).outerjoin(
        Review, Product.id == ProductAnalytics.product_id
    ).group_by(
        Product.id
    ).having(
        func.sum(ProductAnalytics.purchase_count) > 0
    ).order_by(
        func.sum(ProductAnalytics.purchase_count).desc()
    ).limit(5).all()
    
    return jsonify([{
        'id': p.Product.id,
        'name': p.Product.name,
        'price': float(p.Product.price),
        'image_url': p.Product.image_url,
        'category': p.Product.category.name if p.Product.category else None,
        'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
        'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
        'review_count': p.review_count
    } for p in best_sellers])