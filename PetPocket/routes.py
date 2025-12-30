from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from .models import PetType, Product, Category, WishlistItem, CartItem, Order, User
from .models import OrderItem, ProductAnalytics, Address, ProductImage, ProductView, Review, ProductAttribute, PromoCode
from . import db
from flask import current_app
from . import razorpay_client
from datetime import datetime
from sqlalchemy import func, desc
from flask_wtf.csrf import validate_csrf, CSRFError  # Added for explicit CSRF validation
from werkzeug.exceptions import BadRequest, NotFound, HTTPException # Added NotFound for explicit handling

main = Blueprint('main', __name__)

# General handler for all HTTP exceptions to ensure JSON response for AJAX requests
@main.app_errorhandler(HTTPException)
def handle_http_exception(e):
    if request.is_json:
        # For AJAX requests, return JSON error
        return jsonify({'success': False, 'message': e.description or str(e)}), e.code
    # For regular browser requests, render an HTML error page
    return render_template('error.html', error=e.description, code=e.code), e.code

# Specific handler for CSRF errors (can be kept if you want custom messaging for CSRF)
@main.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.is_json:
        return jsonify({'success': False, 'message': 'CSRF token missing or incorrect.'}), 400
    return render_template('csrf_error.html', reason=e.description), 400

@main.route("/", methods=["GET", "POST"])
def home():
    pet_types = PetType.query.all()
    products = Product.query.limit(8).all()
    return render_template("home.html", pet_types=pet_types, products=products)

@main.route("/signin", methods=["GET", "POST"])
def signin():
    notify = request.args.get('notify')
    if notify == 'cart':
        flash('Sign in to add to cart', 'info')
    elif notify == 'wishlist':
        flash('Sign in to add to wishlist', 'info')
    return render_template("signin.html")

@main.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    # Join with Category and PetType to allow searching by those names
    products = Product.query \
        .join(Category, isouter=True) \
        .join(PetType, isouter=True) \
        .filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%')) |
            (Category.name.ilike(f'%{query}%')) |
            (PetType.name.ilike(f'%{query}%'))
        ).all()
    
    # Format results with all necessary fields
    results = []
    for p in products:
        # Calculate average rating and review count
        avg_rating = 0
        review_count = len(p.reviews) if p.reviews else 0
        if review_count > 0:
            avg_rating = round(sum(r.rating for r in p.reviews) / review_count, 1)
        
        results.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'discount_price': float(p.discount_price) if p.discount_price else None,  # ✅ ADD THIS
            'stock': p.stock,
            'image_url': p.image_url if p.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
            'category': p.category.name if p.category else None,
            'pet_type': p.pet_type.name if p.pet_type else None,
            'rating': avg_rating,  # ✅ ADD THIS
            'review_count': review_count  # ✅ ADD THIS
        })
    
    return jsonify(results)

@main.route('/search')
def search():
    return render_template('search.html')

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

@main.route('/products/<int:pet_type_id>')
def products(pet_type_id):
    pet_type = PetType.query.get_or_404(pet_type_id)
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    
    # Build the query with optional category filtering
    query = Product.query.filter_by(pet_type_id=pet_type_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.paginate(page=page, per_page=15, error_out=False)
    categories = Category.query.all()
    
    return render_template('product-listing.html',
                          products=products,
                          pet_type=pet_type,
                          categories=categories,
                          selected_category_id=category_id)

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

def get_advanced_recommendations(user_id=None, limit=10):  # Changed limit from 5 to 10
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
            ProductView.product_id.in_(db.session.query(user_views.c.product_id).subquery().select()),
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
        # Get products that are not in best sellers or pet parent loves
        best_seller_ids = db.session.query(Product.id).join(
            ProductAnalytics, Product.id == ProductAnalytics.product_id
        ).group_by(Product.id).having(
            func.sum(ProductAnalytics.purchase_count) > 0
        ).order_by(func.sum(ProductAnalytics.purchase_count).desc()).limit(10).subquery()

        loved_product_ids = db.session.query(Product.id).join(
            Review, Product.id == Review.product_id
        ).group_by(Product.id).having(
            func.count(Review.id) >= 3
        ).order_by(func.avg(Review.rating).desc()).limit(10).subquery()

        recommendations = Product.query.filter(
            ~Product.id.in_(best_seller_ids),
            ~Product.id.in_(loved_product_ids)
        ).order_by(func.random()).limit(10).all()

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

def get_recommended_products(product_id, limit=10):  # Changed default limit from 4 to 10
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
        recommendations = get_recommended_products(product_id, limit=10)
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
    attributes = ProductAttribute.query.filter_by(product_id=product_id).order_by(ProductAttribute.display_order).all()
    recommended_products = Product.query.filter(
        Product.id != product_id,
        (Product.category_id == product.category_id) | (Product.pet_type_id == product.pet_type_id)
    ).limit(10).all()
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    total_reviews = len(reviews)
    avg_rating = 0
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    if total_reviews > 0:
        total_rating = sum(review.rating for review in reviews)
        avg_rating = round(total_rating / total_reviews, 1)
        for review in reviews:
            rating_counts[review.rating] = rating_counts.get(review.rating, 0) + 1
    if product.parent:
        master_product = product.parent
        selected_variant = product
    else:
        master_product = product
        selected_variant = product
    variants = [master_product] + list(master_product.variants)
    variants = sorted(variants, key=lambda x: x.weight or 0)
    return render_template('product-detail.html', 
                         product=product, 
                         variants=variants,
                         selected_variant=selected_variant,
                         additional_images=additional_images,
                         attributes=attributes,
                         reviews=reviews,
                         total_reviews=total_reviews,
                         avg_rating=avg_rating,
                         rating_counts=rating_counts,
                         recommended_products=recommended_products)

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
            'created_at': existing_review.updated_at.strftime('%B %d, %Y'),
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
        'created_at': review.created_at.strftime('%B %d, %Y'),
        'user': current_user.username,
        'average_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_counts': rating_counts,
        'message': 'Review added successfully'
    })

@main.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in wishlist_items]
    return render_template('wishlist.html', products=products)

@main.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    try:
        # Debug log
        print("Received add_to_wishlist request")
        print("Request headers:", dict(request.headers))
        print("Request data:", request.get_json())

        if not request.is_json:
            print("Request is not JSON")
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        data = request.get_json()
        if not data:
            print("No JSON data received")
            return jsonify({'success': False, 'message': 'No data received'}), 400

        product_id = data.get('product_id')
        if not product_id:
            print("No product_id in request")
            return jsonify({'success': False, 'message': 'Product ID is required'}), 400
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            print(f"Invalid product_id: {product_id}")
            return jsonify({'success': False, 'message': 'Invalid product ID'}), 400

        # Debug log
        print(f"Processing wishlist update - Product ID: {product_id}")

        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            print(f"Product not found - ID: {product_id}")
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        # Check if product is already in wishlist
        wishlist_item = WishlistItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if wishlist_item:
            # Remove from wishlist
            db.session.delete(wishlist_item)
            message = 'Product removed from wishlist'
            print(f"Removed product from wishlist - ID: {product_id}")
        else:
            # Add to wishlist
            wishlist_item = WishlistItem(
                user_id=current_user.id,
                product_id=product_id
            )
            db.session.add(wishlist_item)
            message = 'Product added to wishlist'
            print(f"Added product to wishlist - ID: {product_id}")

        db.session.commit()
        return jsonify({'success': True, 'message': message})

    except Exception as e:
        print(f"Error in add_to_wishlist: {str(e)}")
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
    print(f"Remove from wishlist request: product_id={data.get('product_id')}")  # Debug log
    try:
        product_id = data.get('product_id')
        if not product_id:
            print("Remove from wishlist error: Missing product_id")
            return jsonify({'success': False, 'message': 'Missing product_id'}), 400
        wishlist_item = WishlistItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            print(f"Removed product {product_id} from wishlist for user {current_user.id}")
            return jsonify({'success': True, 'message': 'Removed from wishlist'})
        print(f"Product {product_id} not found in wishlist for user {current_user.id}")
        return jsonify({'success': False, 'message': 'Item not found in wishlist'})
    except Exception as e:
        db.session.rollback()
        print(f"Remove from wishlist error: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/api/wishlist_products')
@login_required
def get_wishlist_products():
    try:
        wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
        products_data = []
        for item in wishlist_items:
            product = item.product
            # Fetch reviews for the product to calculate rating
            reviews = Review.query.filter_by(product_id=product.id).all()
            avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0
            review_count = len(reviews)
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'discount_price': float(product.discount_price) if product.discount_price else None,  # ✅ ADD THIS LINE
                'image_url': product.image_url,
                'avg_rating': avg_rating,
                'review_count': review_count
            })
        return jsonify({'success': True, 'products': products_data})
    except Exception as e:
        current_app.logger.error(f"Error fetching wishlist products: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _unit_price(product):
    """
    Return discounted unit price if valid, otherwise normal price.
    """
    try:
        if product.discount_price is not None and product.discount_price < product.price:
            return float(product.discount_price)
    except Exception:
        pass
    return float(product.price or 0.0)

def _compute_cart_totals(user_id):
    """
    Compute totals using discounted prices where available.
    - savings = original_total - discounted_subtotal
    - shipping = 100 if discounted_subtotal < 500 and > 0 else 0
    - No tax calculation
    """
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    # Calculate subtotal using discounted prices if available
    subtotal = 0.0
    original_subtotal = 0.0
    
    for item in cart_items:
        price = _unit_price(item.product)
        subtotal += price * item.quantity
        original_subtotal += item.product.price * item.quantity
    
    # Get discount from session
    discount = 0.0
    if 'discount' in session:
        try:
            discount = float(session['discount'])
        except (ValueError, TypeError):
            pass
    
    # Calculate savings (product discounts + promo code discounts)
    product_discounts = original_subtotal - subtotal
    total_savings = product_discounts + discount
    
    # Apply discount to get final subtotal
    discounted_subtotal = max(0, subtotal - discount)
    
    # Calculate shipping (no tax)
    shipping = 100.0 if 0 < discounted_subtotal < 500 else 0.0
    
    # Calculate final total (without tax)
    total = discounted_subtotal + shipping
    
    return {
        'subtotal': float(subtotal),
        'discount': float(discount),
        'discounted_subtotal': float(discounted_subtotal),
        'shipping': float(shipping),
        'total': float(total),
        'savings': float(total_savings),
        'product_discounts': float(product_discounts)
    }

def _cart_count_rows(user_id):
    """
    Number of unique items (rows) in the cart. Keep same behavior as your code.
    """
    return CartItem.query.filter_by(user_id=user_id).count()

@main.route('/cart')
def cart():
    cart_items = []
    # Defaults (when not authenticated)
    subtotal = 0.0
    shipping = 0.0
    total = 0.0
    savings = 0.0

    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        totals = _compute_cart_totals(current_user.id)
        subtotal = totals['subtotal']
        shipping = totals['shipping']
        total = totals['total']
        savings = totals['savings']

    return render_template(
        'cart.html',
        cart_items=cart_items,
        cart_count=_cart_count_rows(current_user.id) if current_user.is_authenticated else 0,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
        savings=savings
    )


@main.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        if not request.is_json:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        data = request.get_json() or {}
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        try:
            product_id = int(product_id)
            quantity = max(1, int(quantity))
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Invalid product ID or quantity'}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()

        cart_count = _cart_count_rows(current_user.id)

        # Get updated cart totals
        totals = _compute_cart_totals(current_user.id)

        return jsonify({
            'success': True,
            'message': 'Product added to cart successfully!',
            'cart_count': cart_count,
            'cart_total': totals  # optional - your front-end may ignore it on non-cart pages
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@main.route('/update_cart_item', methods=['PUT'])
@login_required
def update_cart_item():
    try:
        data = request.get_json() or {}
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if product_id is None or quantity is None:
            return jsonify({'success': False, 'message': 'product_id and quantity are required'}), 400

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first_or_404()

        cart_item.quantity = max(1, int(quantity))
        db.session.commit()

        totals = _compute_cart_totals(current_user.id)
        cart_count = _cart_count_rows(current_user.id)

        return jsonify({
            'success': True,
            'cart_total': totals,  # includes subtotal, tax, shipping, total, savings
            'cart_count': cart_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@main.route('/remove_from_cart', methods=['DELETE'])
@login_required
def remove_from_cart():
    try:
        data = request.get_json() or {}
        product_id = data.get('product_id')

        if product_id is None:
            return jsonify({'success': False, 'message': 'product_id is required'}), 400

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

        totals = _compute_cart_totals(current_user.id)
        cart_count = _cart_count_rows(current_user.id)

        return jsonify({
            'success': True,
            'cart_total': totals,
            'cart_count': cart_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/apply_promo_code', methods=['POST'])
@login_required
def apply_promo_code():
    try:
        data = request.get_json()
        promo_code = data.get('promo_code')
        if not promo_code:
            return jsonify({'success': False, 'message': 'Promo code is required'}), 400
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        
        promo = PromoCode.query.filter_by(code=promo_code, active=True).first()
        if not promo:
            return jsonify({'success': False, 'message': 'Invalid promo code'}), 404
        
        is_valid, message = promo.is_valid(subtotal)
        if not is_valid:
            return jsonify({'success': False, 'message': message}), 400
        
        discount = promo.apply_discount(subtotal)
        tax = (subtotal - discount) * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal - discount + tax + shipping
        
        # Store promo code in session for checkout
        session['promo_code'] = promo_code
        session['discount'] = discount
        
        return jsonify({
            'success': True,
            'message': 'Promo code applied successfully',
            'cart_total': {
                'subtotal': subtotal,
                'discount': discount,
                'tax': tax,
                'shipping': shipping,
                'total': total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/remove_promo_code', methods=['POST'])
@login_required
def remove_promo_code():
    try:
        # Remove promo code and discount from session
        session.pop('promo_code', None)
        session.pop('discount', None)
        # Recalculate cart totals
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        discount = 0
        tax = (subtotal - discount) * 0.10
        shipping = 5.00 if cart_items else 0
        total = subtotal - discount + tax + shipping
        return jsonify({
            'success': True,
            'cart_total': {
                'subtotal': subtotal,
                'discount': discount,
                'tax': tax,
                'shipping': shipping,
                'total': total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Calculate subtotal using discounted prices if available
    subtotal = 0
    original_subtotal = 0
    for item in cart_items:
        # Use discount price if it exists and is less than regular price
        if item.product.discount_price and item.product.discount_price < item.product.price:
            price = item.product.discount_price
        else:
            price = item.product.price
        
        subtotal += price * item.quantity
        original_subtotal += item.product.price * item.quantity
    
    # Apply promo code discount if exists
    discount = session.get('discount', 0)
    discounted_subtotal = subtotal - discount
    
    # Calculate shipping
    shipping = 0 if not cart_items or discounted_subtotal >= 500 else 100.00
    total = discounted_subtotal + shipping
    
    # Calculate total savings from both product discounts and promo codes
    product_discounts = original_subtotal - subtotal
    total_savings = product_discounts + discount
    
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
                'is_default': request.form.get('setAsDefault') == 'on',
                'first_name': request.form.get('firstName'),
                'last_name': request.form.get('lastName'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email')
            }
            # Remove keys not in Address model
            address_data = {k: v for k, v in address_data.items() if hasattr(Address, k)}
            # Auto-set as default if no existing default and not explicitly set
            existing_default = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
            if not existing_default and not address_data.get('is_default'):
                address_data['is_default'] = True
            else:
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
                         discount=discount,
                         shipping=shipping,
                         total=total,
                         savings=total_savings,
                         product_discounts=product_discounts,
                         addresses=addresses,
                         default_address=default_address,
                         user=current_user)


@main.route('/get_address/<int:address_id>')
@login_required
def get_address(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
    if not address:
        return jsonify({'success': False, 'message': 'Address not found'}), 404
    
    # Get first and last name from username
    first_name = current_user.username.split()[0] if current_user.username else ''
    last_name = ' '.join(current_user.username.split()[1:]) if current_user.username and ' ' in current_user.username else ''
    
    return jsonify({
        'success': True,
        'address': {
            'id': address.id,
            'first_name': first_name,
            'last_name': last_name,
            'address_type': address.address_type,
            'company_name': address.company_name,
            'street_address': address.street_address,
            'apartment': address.apartment,
            'city': address.city,
            'state': address.state,
            'country': address.country,
            'pin_code': address.pin_code,
            'phone': current_user.phone or '',
            'email': current_user.email or '',
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

@main.route('/create_order', methods=['POST'])
@login_required
def create_order():
    try:
        # Parse request data
        data = request.json
        address_id = data.get('address_id')
        new_address_data = data.get('new_address')
        
        # Validate address information
        if not address_id and not new_address_data:
            return jsonify({'success': False, 'error': 'Address information is required'}), 400
            
        # Get cart items and calculate totals
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
            
        # Calculate subtotal using discounted prices if available
        subtotal = 0
        original_subtotal = 0
        for item in cart_items:
            price = item.product.discount_price if item.product.discount_price and item.product.discount_price < item.product.price else item.product.price
            subtotal += price * item.quantity
            original_subtotal += item.product.price * item.quantity
        
        # Get discount from session
        discount = session.get('discount', 0)
        discounted_subtotal = subtotal - discount
        
        # Calculate shipping
        shipping = 0 if not cart_items or discounted_subtotal >= 500 else 100.00
        
        # Calculate final total (without tax)
        total = discounted_subtotal + shipping
        
        # Create Razorpay order
        data = {
            'amount': int(total * 100),  # Convert to paise
            'currency': 'INR',
            'receipt': f'order_rcptid_{current_user.id}_{int(datetime.now().timestamp())}',
            'payment_capture': '1'  # Auto-capture payment
        }
        
        # Create order in Razorpay
        razorpay_order = razorpay_client.order.create(data=data)
        
        # Create order in our database
        order = Order(
            user_id=current_user.id,
            total_price=total,
            order_id=razorpay_order['id'],
            payment_status='pending'
        )
        db.session.add(order)
        
        # Add order items
        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            db.session.add(order_item)
        
        # Store address information in session for use during payment verification
        if address_id:
            session['order_address_id'] = address_id
        elif new_address_data:
            session['order_new_address'] = new_address_data
        
        db.session.commit()
        
        # Get customer information for Razorpay prefill
        customer_name = current_user.username
        customer_email = current_user.email
        customer_phone = current_user.phone
        
        return jsonify({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': data['amount'],
            'currency': data['currency'],
            'key_id': current_app.config['RAZORPAY_KEY_ID'],
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone
        })
    except Exception as e:
        db.session.rollback()
        # Log detailed error information
        import traceback
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'user_id': current_user.id if current_user.is_authenticated else 'anonymous',
            'cart_items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': str(item.product.price) if item.product else 'N/A'
            } for item in cart_items] if 'cart_items' in locals() else []
        }
        current_app.logger.error('Error creating order: %s', error_details)
        return jsonify({
            'success': False, 
            'error': 'Failed to create order',
            'details': str(e) if current_app.debug else 'An error occurred while processing your order.'
        }), 500

# Handle both /payment_callback and /payment/callback for backward compatibility
@main.route('/payment_callback', methods=['POST'])
@main.route('/payment/callback', methods=['POST'])
def payment_callback():
    try:
        # Get payment details from the request
        payment_id = request.form.get('razorpay_payment_id')
        order_id = request.form.get('razorpay_order_id')
        signature = request.form.get('razorpay_signature')
        
        if not all([payment_id, order_id, signature]):
            current_app.logger.error(f'Missing payment details in callback: {request.form}')
            return jsonify({'success': False, 'error': 'Missing payment details'}), 400
        
        # Verify the payment signature
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            })
        except Exception as e:
            current_app.logger.error(f'Invalid payment signature: {str(e)}')
            return jsonify({'success': False, 'error': 'Invalid payment signature'}), 400
        
        # Find the order in database
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            current_app.logger.error(f'Order not found: {order_id}')
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        # Update order status
        order.payment_status = 'completed'
        order.payment_id = payment_id
        
        # Clear the user's cart if authenticated
        if current_user.is_authenticated:
            CartItem.query.filter_by(user_id=current_user.id).delete()
        
        # Clear any session data
        if 'discount' in session:
            session.pop('discount', None)
            
        db.session.commit()
        
        current_app.logger.info(f'Payment verified successfully for order {order_id}')
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'order_id': order.id
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in payment_callback: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your payment',
            'details': str(e) if current_app.debug else None
        }), 500
    except Exception as e:
        db.session.rollback()
        print(f"Payment verification error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    try:
        data = request.json
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        
        if not all([payment_id, order_id, signature]):
            current_app.logger.error(f'Missing payment details: {data}')
            return jsonify({'success': False, 'error': 'Missing payment details'}), 400
        
        # Find the order in our database first
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            current_app.logger.error(f'Order not found: {order_id}')
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        # Check if order is already marked as completed
        if order.payment_status == 'completed':
            current_app.logger.info(f'Order {order_id} is already marked as completed')
            return jsonify({
                'success': True,
                'message': 'Payment already verified',
                'order_id': order.id,
                'redirect': url_for('main.order_confirmation', order_id=order.id)
            })
            
        try:
            # Verify payment with Razorpay
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            
            # Double check payment status with Razorpay
            payment = razorpay_client.payment.fetch(payment_id)
            
            if payment['status'] != 'captured':
                raise Exception(f'Payment status is {payment["status"]}, expected captured')
            
            # Start a transaction
            with db.session.begin_nested():
                # Update order status
                order.payment_status = 'completed'
                order.payment_id = payment_id
                
                # Process address information
                address_id = session.get('order_address_id')
                new_address_data = session.get('order_new_address')
                
                # If new address data was provided, create a new address
                if new_address_data and not address_id:
                    try:
                        address = Address(
                            user_id=current_user.id,
                            address_type=new_address_data.get('address_type', 'home'),
                            company_name=new_address_data.get('company_name', ''),
                            street_address=new_address_data.get('street_address', ''),
                            apartment=new_address_data.get('apartment', ''),
                            city=new_address_data.get('city', ''),
                            state=new_address_data.get('state', ''),
                            country=new_address_data.get('country', 'India'),
                            pin_code=new_address_data.get('pin_code', ''),
                            is_default=False  # Don't make it default automatically
                        )
                        db.session.add(address)
                        db.session.flush()  # Get the ID without committing
                    except Exception as e:
                        current_app.logger.error(f'Error creating address: {str(e)}')
                        # Continue with order processing even if address creation fails
                
                # Clear the user's cart
                CartItem.query.filter_by(user_id=current_user.id).delete()
                
                # Clear any session data
                if 'discount' in session:
                    session.pop('discount', None)
                if 'order_address_id' in session:
                    session.pop('order_address_id', None)
                if 'order_new_address' in session:
                    session.pop('order_new_address', None)
            
            # Commit the transaction
            db.session.commit()
            
            current_app.logger.info(f'Payment verified successfully for order {order_id}')
            
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully',
                'order_id': order.id,
                'redirect': url_for('main.order_confirmation', order_id=order.id)
            })
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Payment verification failed: {str(e)}')
            
            # Update order status to failed
            order.payment_status = 'failed'
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Payment verification failed',
                'details': str(e) if current_app.debug else None
            }), 400
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in verify_payment: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your payment',
            'details': str(e) if current_app.debug else None
        }), 500

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
    try:
        # Get products with high ratings and reviews
        loved_products = db.session.query(
            Product,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).join(
            Review, Product.id == Review.product_id
        ).group_by(
            Product.id
        ).having(
            func.count(Review.id) >= 3,
            func.avg(Review.rating) >= 4.0  # Only highly rated products
        ).order_by(
            func.avg(Review.rating).desc()
        ).limit(10).all()

        return jsonify([{
            'id': p.Product.id,
            'name': p.Product.name,
            'price': float(p.Product.price),
            'image_url': p.Product.image_url if p.Product.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
            'category': p.Product.category.name if p.Product.category else None,
            'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
            'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
            'review_count': p.review_count
        } for p in loved_products])
    except Exception as e:
        current_app.logger.error(f"Pet parent loves error: {str(e)}")
        return jsonify([])

@main.route('/api/best_sellers')
def best_sellers():
    try:
        # Get products with highest purchase count
        best_sellers = db.session.query(
            Product,
            func.coalesce(func.sum(ProductAnalytics.purchase_count), 0).label('total_purchases'),
            func.avg(Review.rating).label('avg_rating'),
            func.coalesce(func.count(func.distinct(Review.id)), 0).label('review_count')
        ).outerjoin(
            ProductAnalytics, Product.id == ProductAnalytics.product_id
        ).outerjoin(
            Review, Product.id == Review.product_id
        ).group_by(
            Product.id
        ).having(
            func.sum(ProductAnalytics.purchase_count) > 0
        ).order_by(
            func.sum(ProductAnalytics.purchase_count).desc()
        ).limit(10).all()

        return jsonify([{
            'id': p.Product.id,
            'name': p.Product.name,
            'price': float(p.Product.price),
            'image_url': p.Product.image_url if p.Product.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
            'category': p.Product.category.name if p.Product.category else None,
            'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
            'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
            'review_count': p.review_count
        } for p in best_sellers])
    except Exception as e:
        current_app.logger.error(f"Best sellers error: {str(e)}")
        return jsonify({'error': 'Failed to fetch best sellers'}), 500

# Updated edit_profile route with case-insensitive checks and CSRF validation
@main.route('/edit-profile', methods=['POST'])
@login_required
def edit_profile():
    try:
        # Validate CSRF token
        csrf_token = request.headers.get('X-CSRFToken')
        if not csrf_token:
            return jsonify({
                'success': False,
                'message': 'CSRF token missing'
            }), 403
        
        validate_csrf(csrf_token)

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip() if data.get('phone') else None

        if not username or not email:
            return jsonify({
                'success': False,
                'message': 'Username and email are required.'
            }), 400

        # Case-insensitive check for username
        existing_user = User.query.filter(
            func.lower(User.username) == func.lower(username), 
            User.id != current_user.id
        ).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username already exists. Please choose a different one.'
            }), 400

        # Case-insensitive check for email
        existing_email = User.query.filter(
            func.lower(User.email) == func.lower(email), 
            User.id != current_user.id
        ).first()
        if existing_email:
            return jsonify({
                'success': False,
                'message': 'Email already exists. Please use a different email address.'
            }), 400

        current_user.username = username
        current_user.email = email
        current_user.phone = phone
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully!',
            'user': {
                'username': current_user.username,
                'email': current_user.email,
                'phone': current_user.phone
            }
        })

    except CSRFError:
        return jsonify({
            'success': False,
            'message': 'Invalid CSRF token. Please refresh the page and try again.'
        }), 403
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating profile for user {current_user.id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred while updating your profile: {str(e)}'
        }), 500

@main.route('/api/product_review_stats/<int:product_id>')
def product_review_stats(product_id):
    from .models import Product, Review
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    total_reviews = len(reviews)
    avg_rating = round(sum(r.rating for r in reviews) / total_reviews, 1) if total_reviews > 0 else 0
    return jsonify({
        'avg_rating': avg_rating,
        'total_reviews': total_reviews
    })

@main.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    # Get the order details
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    # Get order items
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    
    return render_template('order_confirmation.html', 
                           order=order, 
                           order_items=order_items,
                           title="Order Confirmation")

@main.route('/api/home_products')
def home_products():
    try:
        # Get all product IDs to avoid repeats
        used_ids = set()
        # Best Sellers
        best_sellers_query = db.session.query(
            Product,
            func.coalesce(func.sum(ProductAnalytics.purchase_count), 0).label('total_purchases'),
            func.avg(Review.rating).label('avg_rating'),
            func.coalesce(func.count(func.distinct(Review.id)), 0).label('review_count')
        ).outerjoin(
            ProductAnalytics, Product.id == ProductAnalytics.product_id
        ).outerjoin(
            Review, Product.id == Review.product_id
        ).group_by(
            Product.id
        ).having(
            func.sum(ProductAnalytics.purchase_count) > 0
        ).order_by(
            func.sum(ProductAnalytics.purchase_count).desc()
        ).limit(20).all()
        best_sellers = []
        for p in best_sellers_query:
            if len(best_sellers) >= 8:
                break
            best_sellers.append({
                'id': p.Product.id,
                'name': p.Product.name,
                'price': float(p.Product.price),
                'discount_price': float(p.Product.discount_price) if p.Product.discount_price else None,  # ✅ ADD THIS
                'image_url': p.Product.image_url if p.Product.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
                'category': p.Product.category.name if p.Product.category else None,
                'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
                'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
                'review_count': p.review_count
            })
            used_ids.add(p.Product.id)
        # Pet Parent Loves
        pet_parent_loves_query = db.session.query(
            Product,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).join(
            Review, Product.id == Review.product_id
        ).group_by(
            Product.id
        ).having(
            func.count(Review.id) >= 3,
            func.avg(Review.rating) >= 4.0
        ).order_by(
            func.avg(Review.rating).desc()
        ).limit(20).all()
        pet_parent_loves = []
        for p in pet_parent_loves_query:
            if len(pet_parent_loves) >= 8:
                break
            if p.Product.id in used_ids:
                continue
            pet_parent_loves.append({
                'id': p.Product.id,
                'name': p.Product.name,
                'price': float(p.Product.price),
                'discount_price': float(p.Product.discount_price) if p.Product.discount_price else None,  # ✅ ADD THIS
                'image_url': p.Product.image_url if p.Product.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
                'category': p.Product.category.name if p.Product.category else None,
                'pet_type': p.Product.pet_type.name if p.Product.pet_type else None,
                'rating': round(p.avg_rating, 1) if p.avg_rating else 0,
                'review_count': p.review_count
            })
            used_ids.add(p.Product.id)
        # If no products meet the criteria, fill with any products not already used
        if len(pet_parent_loves) == 0:
            all_products = Product.query.all()
            for p in all_products:
                if p.id not in used_ids:
                    pet_parent_loves.append({
                        'id': p.id,
                        'name': p.name,
                        'price': float(p.price),
                        'discount_price': float(p.discount_price) if p.discount_price else None,  # ✅ ADD THIS
                        'image_url': p.image_url if p.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
                        'category': p.category.name if p.category else None,
                        'pet_type': p.pet_type.name if p.pet_type else None,
                        'rating': round(sum(r.rating for r in p.reviews) / len(p.reviews), 1) if p.reviews else 0,
                        'review_count': len(p.reviews)
                    })
                    used_ids.add(p.id)
                    if len(pet_parent_loves) >= 8:
                        break
        # Recommendations (random, not in above)
        recommendations_query = Product.query.filter(~Product.id.in_(used_ids)).order_by(func.random()).limit(20).all()
        recommendations = []
        for p in recommendations_query:
            if len(recommendations) >= 8:
                break
            recommendations.append({
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'discount_price': float(p.discount_price) if p.discount_price else None,  # ✅ ADD THIS
                'image_url': p.image_url if p.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
                'category': p.category.name if p.category else None,
                'pet_type': p.pet_type.name if p.pet_type else None,
                'rating': round(sum(r.rating for r in p.reviews) / len(p.reviews), 1) if p.reviews else 0,
                'review_count': len(p.reviews)
            })
            used_ids.add(p.id)
        # Fill any section with random products if < 8
        all_products = Product.query.all()
        def fill_section(section):
            while len(section) < 8:
                for p in all_products:
                    if p.id not in used_ids:
                        section.append({
                            'id': p.id,
                            'name': p.name,
                            'price': float(p.price),
                            'discount_price': float(p.discount_price) if p.discount_price else None,  # ✅ ADD THIS
                            'image_url': p.image_url if p.image_url else 'https://placehold.co/200x200/46f27a/ffffff?text=Product',
                            'category': p.category.name if p.category else None,
                            'pet_type': p.pet_type.name if p.pet_type else None,
                            'rating': round(sum(r.rating for r in p.reviews) / len(p.reviews), 1) if p.reviews else 0,
                            'review_count': len(p.reviews)
                        })
                        used_ids.add(p.id)
                        if len(section) >= 8:
                            break
                else:
                    break  # Prevent infinite loop if not enough products
        fill_section(best_sellers)
        fill_section(pet_parent_loves)
        fill_section(recommendations)
        return jsonify({
            'best_sellers': best_sellers,
            'pet_parent_loves': pet_parent_loves,
            'recommendations': recommendations
        })
    except Exception as e:
        current_app.logger.error(f"Home products error: {str(e)}")
        return jsonify({'best_sellers': [], 'pet_parent_loves': [], 'recommendations': []})