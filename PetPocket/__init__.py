from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_login import current_user
from flask_mail import Mail
import os
import razorpay

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Mail
mail = Mail()

# Initialize Razorpay client as None first
razorpay_client = None

def create_app():
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = 'your-secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petpocket.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Add Razorpay configuration
    app.config['RAZORPAY_KEY_ID'] = 'rzp_test_QTmdq1PBiByYN9'
    app.config['RAZORPAY_KEY_SECRET'] = 'TNgY0GTvtMjHsl5pSm9Stlsy'
    
    # Initialize Razorpay client
    global razorpay_client
    razorpay_client = razorpay.Client(
        auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET'])
    )

    # Initialize Flask extensions
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main.signin'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from .routes import main
    from .auth import auth
    from .admin.analytics import admin_analytics  # Import the analytics blueprint
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin_analytics)  # Register the analytics blueprint
    
    # Import admin after initializing extensions and registering blueprints
    # This avoids circular imports
    from .admin import init_admin
    init_admin(app, db)  # Pass db as an argument
    
    @app.context_processor
    def inject_cart_count():
        from .models import CartItem
        from sqlalchemy import func
        if current_user.is_authenticated:
            # Sum the quantities of all cart items
            cart_count = db.session.query(func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
            cart_count = int(cart_count)  # Convert to int
        else:
            cart_count = 0
        return dict(cart_count=cart_count)
    
    # Configure Flask-Mail
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',  # For Gmail, or use your email provider's SMTP server
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME', 'manavchawla146@gmail.com'),  # Replace with your actual email
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', 'oagx rjac cfmn qjav'),  # Replace with your app password
        MAIL_DEFAULT_SENDER=('PetPocket Admin', 'manavchawla146gmail.com')  # Replace with your email
    )
    
    mail.init_app(app)
    
    return app