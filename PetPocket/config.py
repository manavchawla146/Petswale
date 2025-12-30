import os

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-go-here'
    
    # Database config
    # Update the following URI with your MySQL username, password, host, and database name
    # Example: 'mysql+pymysql://username:password@localhost/dbname'
    # Using Aiven Cloud MySQL with SSL CA
    # Using relative path for SSL CA; must run app from PetPocket directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://avnadmin:YOUR_PASSWORD@mysql-8812813-manavdodani2005-1c65.g.aivencloud.com:26262/petswale?ssl_ca=./ca.pem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database connection pooling settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,  # Recycle connections after 5 minutes (300 seconds)
        'pool_timeout': 30,   # 30 seconds
        'pool_size': 10,      # Maintain up to 10 connections in the pool
        'max_overflow': 20,   # Allow up to 20 connections to be created beyond pool_size
        'pool_pre_ping': True,  # Enable connection health checks
        'pool_use_lifo': True,  # Use last-in-first-out for better connection reuse
    }
    
    # CSRF config
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    WTF_CSRF_SSL_STRICT = False  # Set to True in production
    
    # Razorpay config
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_live_RGkEP4XjZZVrxv'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'LR0Iqe9U0XVEPzsxYo78MmOe'
    
    # Session config
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security headers
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'your-password-salt'

    # Google OAuth config
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or '1047039162052-7e0fgrt2prvkcl2ta0ojao471ifs0c01.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or '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'
    
    # File upload config
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    DEBUG = False
    # Production database URI and security settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Enable secure cookies for production
    SESSION_COOKIE_SECURE = True
    # Enable CSRF SSL strict for production
    WTF_CSRF_SSL_STRICT = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --------------------------------------------------
    # FLASK CORE
    # --------------------------------------------------
    SECRET_KEY = "petswale_super_secret_key_2025"

    DEBUG = False
    TESTING = False

    # --------------------------------------------------
    # DATABASE (LOCAL MYSQL ON SAME VPS)
    # --------------------------------------------------
    # Make sure this DB + user exists in MySQL
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://petswale_user:StrongPassword123!@localhost/petswale_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_timeout": 30,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
    }

    # --------------------------------------------------
    # SESSION / SECURITY
    # --------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False   # set TRUE only after HTTPS

    SECURITY_PASSWORD_SALT = "petswale_password_salt"

    # --------------------------------------------------
    # CSRF
    # --------------------------------------------------
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = False     # enable after HTTPS

    # --------------------------------------------------
    # RAZORPAY
    # --------------------------------------------------
    RAZORPAY_KEY_ID = "rzp_live_RGkEP4XjZZVrxv"
    RAZORPAY_KEY_SECRET = "LR0Iqe9U0XVEPzsxYo78MmOe"

    # --------------------------------------------------
    # GOOGLE OAUTH
    # --------------------------------------------------
    GOOGLE_CLIENT_ID = (
        "1047039162052-7e0fgrt2prvkcl2ta0ojao471ifs0c01.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET = "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"

    # --------------------------------------------------
    # FILE UPLOADS
    # --------------------------------------------------
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
