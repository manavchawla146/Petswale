from flask_admin import Admin, BaseView, expose
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask import url_for, request, flash, current_app, jsonify
from werkzeug.utils import redirect
from flask_mail import Message, Mail

# Base admin view classes with security
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.signin'))

class SecureBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.signin'))

class HomeAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.is_admin):
            return redirect(url_for('main.signin'))
        return redirect(url_for('admin_analytics.analytics_dashboard'))

# Custom formatter functions
def formatter_price(view, context, model, name):
    price_value = getattr(model, name)
    if price_value is not None:
        return f"₹{price_value:.2f}"
    return ""

# Admin views
class EmailView(SecureBaseView):
    @expose('/', methods=['GET', 'POST'])
    def send_email(self):
        # Import here to avoid circular imports
        from ..models import User
        
        mail = Mail(current_app)
        users = User.query.all()
        
        if request.method == 'POST':
            recipients = request.form.getlist('recipients')
            subject = request.form.get('subject')
            message_body = request.form.get('message')
            
            if not recipients:
                flash('You must select at least one recipient', 'error')
                return self.render('admin/email.html', users=users)
            
            # Get the recipient email addresses
            recipient_users = User.query.filter(User.id.in_(recipients)).all()
            recipient_emails = [user.email for user in recipient_users]
            
            try:
                msg = Message(
                    subject=subject,
                    recipients=recipient_emails,
                    body=message_body
                )
                mail.send(msg)
                
                flash(f'Email successfully sent to {len(recipient_emails)} users!', 'success')
            except Exception as e:
                flash(f'Error sending email: {str(e)}', 'error')
        
        return self.render('admin/email.html', users=users)

class CategoryView(SecureModelView):
    column_list = ['id', 'name', 'slug', 'image_url', 'description']
    form_columns = ['name', 'slug', 'image_url', 'description']

class AddressView(SecureModelView):
    column_list = ['user.username', 'address_type', 'city', 'state', 'is_default']
    column_searchable_list = ['city', 'state', 'pin_code']
    column_filters = ['address_type', 'city', 'state', 'is_default']
    form_columns = [
        'user', 'address_type', 'company_name', 'street_address',
        'apartment', 'city', 'state', 'country', 'pin_code', 'is_default'
    ]

class OrderView(SecureModelView):
    column_list = ['id', 'user.username', 'user.email', 'timestamp', 'total_price', 'payment_status', 'payment_id', 'order_id']
    column_searchable_list = ['payment_id', 'order_id', 'payment_status', 'user.username', 'user.email']
    column_filters = ['timestamp', 'payment_status', 'user.username']
    column_default_sort = ('timestamp', True)
    can_create = False
    column_formatters = {
        'total_price': formatter_price
    }
    
    column_labels = {
        'user.username': 'Customer Name',
        'user.email': 'Customer Email'
    }

class OrderItemView(SecureModelView):
    column_list = ['order.id', 'order.user.username', 'product.name', 'quantity', 'price_at_purchase']
    column_filters = ['order.id', 'product.name']  # Simplified filters
    column_searchable_list = ['product.name']  # Keep only direct relationships
    can_create = False
    
    column_labels = {
        'order.user.username': 'Customer Name',
        'order.id': 'Order ID',
        'product.name': 'Product',
        'quantity': 'Quantity',
        'price_at_purchase': 'Price'
    }
    
    column_formatters = {
        'price_at_purchase': formatter_price
    }

    def __init__(self, model, session, **kwargs):
        super(OrderItemView, self).__init__(model, session, **kwargs)

class ProductView(SecureModelView):
    column_list = ['name', 'price', 'stock', 'category.name', 'pet_type.name', 'weight', 'parent.name']
    column_searchable_list = ['name', 'description']
    column_filters = ['price', 'stock', 'category.name', 'pet_type.name', 'weight']
    form_columns = ['name', 'description', 'price', 'stock', 'image_url', 'category', 'pet_type', 'weight', 'parent']
    column_formatters = {
        'price': formatter_price
    }
    
    def __init__(self, model, session, **kwargs):
        # Defer importing these models to avoid circular imports
        super(ProductView, self).__init__(model, session, **kwargs)
    
    def _refresh_forms_args(self):
        # Import here to avoid circular imports
        from ..models import Category, PetType, Product
        
        self.form_args = {
            'category': {'query_factory': lambda: Category.query.order_by(Category.name)},
            'pet_type': {'query_factory': lambda: PetType.query.order_by(PetType.name)},
            'parent': {
                'query_factory': lambda: Product.query.filter_by(parent_id=None).order_by(Product.name)
            }
        }
    
    def create_form(self, obj=None):
        self._refresh_forms_args()
        form = super(ProductView, self).create_form(obj)
        self._add_conditional_field_script(form)
        return form
    
    def edit_form(self, obj=None):
        self._refresh_forms_args()
        form = super(ProductView, self).edit_form(obj)
        self._add_conditional_field_script(form)
        return form
    
    def _add_conditional_field_script(self, form):
        from ..models import Category
        # Get the food category ID
        food_category = Category.query.filter(Category.name.ilike('%food%')).first()
        food_category_id = food_category.id if food_category else -1
        
        # Add custom template for the form
        self.extra_js = [
            f"""
            $(document).ready(function() {{
                var foodCategoryId = {food_category_id};
                
                function toggleFoodFields() {{
                    var selectedCategory = $('select[name="category"]').val();
                    var weightField = $('.field-weight').closest('.form-group');
                    var parentField = $('.field-parent').closest('.form-group');
                    
                    if (selectedCategory == foodCategoryId) {{
                        weightField.show();
                        parentField.show();
                    }} else {{
                        weightField.hide();
                        parentField.hide();
                    }}
                }}
                
                // Initial toggle
                toggleFoodFields();
                
                // Toggle on category change
                $('select[name="category"]').change(function() {{
                    toggleFoodFields();
                }});
                
                // Filter parent dropdown based on category and pet type
                $('select[name="category"], select[name="pet_type"]').change(function() {{
                    var categoryId = $('select[name="category"]').val();
                    var petTypeId = $('select[name="pet_type"]').val();
                    
                    if (categoryId && petTypeId) {{
                        $.ajax({{
                            url: '/admin/admin_api/filter_parents',
                            data: {{
                                category_id: categoryId,
                                pet_type_id: petTypeId
                            }},
                            success: function(data) {{
                                var parentSelect = $('select[name="parent"]');
                                parentSelect.empty();
                                
                                // Add None (Master) option
                                parentSelect.append($('<option>', {{
                                    value: '',
                                    text: 'None (Master)'
                                }}));
                                
                                // Add filtered products
                                $.each(data.products, function(i, product) {{
                                    parentSelect.append($('<option>', {{
                                        value: product.id,
                                        text: product.name
                                    }}));
                                }});
                            }}
                        }});
                    }}
                }});
            }});
            """
        ]

class ReviewView(SecureModelView):
    column_list = ['product.name', 'reviewer.username', 'rating', 'content', 'created_at']
    column_searchable_list = ['content']
    column_filters = ['rating', 'product.name']
    form_columns = ['product', 'reviewer', 'rating', 'content']
    
    def __init__(self, model, session, **kwargs):
        # Defer imports to avoid circular references
        super(ReviewView, self).__init__(model, session, **kwargs)
    
    def _refresh_forms_args(self):
        # Import here to avoid circular imports
        from ..models import Product, User
        
        self.form_args = {
            'product': {'query_factory': lambda: Product.query.order_by(Product.name)},
            'reviewer': {'query_factory': lambda: User.query.order_by(User.username)}
        }
    
    def create_form(self, obj=None):
        self._refresh_forms_args()
        return super(ReviewView, self).create_form(obj)
    
    def edit_form(self, obj=None):
        self._refresh_forms_args()
        return super(ReviewView, self).edit_form(obj)

class ProductImageView(SecureModelView):
    column_list = ['product.name', 'image_url', 'is_primary', 'display_order']
    column_filters = ['product.name', 'is_primary']
    form_columns = ['product', 'image_url', 'is_primary', 'display_order']
    
    def __init__(self, model, session, **kwargs):
        # Defer imports to avoid circular references
        super(ProductImageView, self).__init__(model, session, **kwargs)
    
    def _refresh_forms_args(self):
        # Import here to avoid circular imports
        from ..models import Product
        
        self.form_args = {
            'product': {'query_factory': lambda: Product.query.order_by(Product.name)}
        }
    
    def create_form(self, obj=None):
        self._refresh_forms_args()
        return super(ProductImageView, self).create_form(obj)
    
    def edit_form(self, obj=None):
        self._refresh_forms_args()
        return super(ProductImageView, self).edit_form(obj)

class UserView(SecureModelView):
    column_list = ['id', 'username', 'email', 'phone', 'is_admin', 'created_at']
    column_searchable_list = ['username', 'email', 'phone']
    column_filters = ['is_admin', 'created_at']

class AdminAPI(SecureBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/api_index.html')

    @expose('/filter_parents')
    def filter_parents(self):
        from ..models import Product
        
        category_id = request.args.get('category_id', type=int)
        pet_type_id = request.args.get('pet_type_id', type=int)
        
        if not category_id or not pet_type_id:
            return jsonify({'products': []})
        
        try:
            # Get master products (parent_id is None) with matching category and pet type
            products = Product.query.filter_by(
                category_id=category_id,
                pet_type_id=pet_type_id,
                parent_id=None
            ).all()
            
            return jsonify({
                'products': [{'id': p.id, 'name': p.name} for p in products]
            })
        except Exception as e:
            current_app.logger.error(f"Error in filter_parents: {str(e)}")
            return jsonify({'error': 'Failed to fetch products', 'products': []})

class AnalyticsDashboardView(SecureBaseView):
    @expose('/')
    def analytics_dashboard(self):
        from ..models import Order, Product, User
        
        # Get some basic statistics
        total_orders = Order.query.count()
        total_products = Product.query.count()
        total_users = User.query.count()
        
        # Recent orders
        recent_orders = Order.query.order_by(Order.timestamp.desc()).limit(10).all()
        
        return self.render(
            'admin/analytics_dashboard.html',
            total_orders=total_orders,
            total_products=total_products,
            total_users=total_users,
            recent_orders=recent_orders
        )

def init_admin(app, db):
    """Initialize the Flask-Admin interface"""
    # Import models here to avoid circular imports
    from ..models import (
        User, Product, Review, ProductImage, Category, 
        PetType, Order, OrderItem, Address
    )
    
    # Initialize admin with custom index view
    admin = Admin(
        app, 
        name='PetPocket Admin', 
        template_mode='bootstrap4', 
        index_view=HomeAdminView(name='Home')
    )
    
    # Add model views
    admin.add_view(UserView(User, db.session, name='Users'))
    admin.add_view(ProductView(Product, db.session, name='Products'))
    admin.add_view(CategoryView(Category, db.session, name='Categories'))
    admin.add_view(SecureModelView(PetType, db.session, name='Pet Types'))
    admin.add_view(OrderView(Order, db.session, name='Orders'))
    admin.add_view(OrderItemView(OrderItem, db.session, name='Order Items'))
    admin.add_view(AddressView(Address, db.session, name='Addresses'))
    admin.add_view(ReviewView(Review, db.session, name='Reviews'))
    admin.add_view(ProductImageView(ProductImage, db.session, name='Product Images'))
    
    # Add custom views with unique endpoints
    admin.add_view(EmailView(name='Send Email', endpoint='admin_email'))
    admin.add_view(AdminAPI(name='API', endpoint='admin_api'))
    admin.add_view(AnalyticsDashboardView(name='Analytics', endpoint='analytics_dashboard'))
    
    return admin