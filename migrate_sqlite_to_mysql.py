import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from PetPocket.models import db, User, PetType, Category, Product, ProductImage, ProductAttribute, Review, CartItem, WishlistItem, Order, OrderItem, ProductAnalytics, PromoCode
from PetPocket import config

# Update these URIs:
SQLITE_URI = 'sqlite:///instance/petpocket.db'  # Path to your old SQLite DB
MYSQL_URI = 'mysql+pymysql://avnadmin:YOUR_PASSWORD@mysql-petswale-manavdodani2005-1c65.f.aivencloud.com:26262/petswale?ssl_ca=ca.pem'  # Update with your MySQL credentials

# Source (SQLite) engine/session
sqlite_engine = create_engine(SQLITE_URI)
SqliteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SqliteSession()

# Target (MySQL) engine/session
mysql_engine = create_engine(MYSQL_URI)
MysqlSession = sessionmaker(bind=mysql_engine)
mysql_session = MysqlSession()

# List all your models here
MODELS = [
    User, PetType, Category, Product, ProductImage, ProductAttribute, Review, CartItem, WishlistItem, Order, OrderItem, ProductAnalytics, PromoCode
]

def migrate_table(Model):
    print(f"Migrating {Model.__tablename__}...")
    records = sqlite_session.query(Model).all()
    for record in records:
        # Detach from old session, attach to new
        mysql_session.merge(record)
    mysql_session.commit()
    print(f"Migrated {len(records)} records from {Model.__tablename__}.")

def main():
    for Model in MODELS:
        migrate_table(Model)
    print("Migration complete!")

if __name__ == "__main__":
    main()
