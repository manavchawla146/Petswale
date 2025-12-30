import sqlite3
import re
from PetPocket import create_app, db
from PetPocket.models import User, Product, Category, PetType, Order, OrderItem, Address, Review, ProductImage, ProductAttribute, PromoCode

def extract_insert_statements(mysql_file):
    """Extract only INSERT statements from MySQL dump"""
    with open(mysql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all INSERT statements
    insert_pattern = r"INSERT INTO `([^`]+)`\s*(.*?)VALUES\s*(.*?);"
    matches = re.findall(insert_pattern, content, re.DOTALL | re.IGNORECASE)
    
    return matches

def clean_mysql_values(values_str):
    """Clean MySQL values for SQLite"""
    # Remove MySQL-specific escaping
    values_str = re.sub(r'\\n', ' ', values_str)
    values_str = re.sub(r'\\r', ' ', values_str)
    values_str = re.sub(r'\\\'', "'", values_str)
    values_str = re.sub(r'\\"', '"', values_str)
    values_str = re.sub(r'\\', '', values_str)  # Remove remaining backslashes
    
    return values_str

def import_data():
    app = create_app()
    
    with app.app_context():
        mysql_file = "instance/manv.sql"
        insert_statements = extract_insert_statements(mysql_file)
        
        print(f"Found {len(insert_statements)} INSERT statements")
        
        for table_name, columns, values in insert_statements:
            print(f"Processing table: {table_name}")
            
            # Clean the values
            values = clean_mysql_values(values)
            
            try:
                if table_name == 'users':
                    # Handle users table
                    user_data = []
                    for row in re.findall(r'\((.*?)\)', values):
                        parts = [p.strip().strip("'\"") for p in row.split(',')]
                        if len(parts) >= 6:
                            user_data.append({
                                'id': int(parts[0]) if parts[0] else None,
                                'username': parts[1],
                                'email': parts[2],
                                'phone': parts[3] if parts[3] else None,
                                'password_hash': parts[4] if parts[4] else None,
                                'is_admin': int(parts[5]) if parts[5] else 0
                            })
                    
                    for user in user_data:
                        try:
                            existing_user = User.query.get(user['id'])
                            if not existing_user:
                                new_user = User(**user)
                                db.session.add(new_user)
                        except Exception as e:
                            print(f"Error inserting user: {e}")
                
                elif table_name == 'categories':
                    # Handle categories table
                    category_data = []
                    for row in re.findall(r'\((.*?)\)', values):
                        parts = [p.strip().strip("'\"") for p in row.split(',')]
                        if len(parts) >= 4:
                            category_data.append({
                                'id': int(parts[0]) if parts[0] else None,
                                'name': parts[1],
                                'slug': parts[2],
                                'image_url': parts[3] if parts[3] else None
                            })
                    
                    for cat in category_data:
                        try:
                            existing_cat = Category.query.get(cat['id'])
                            if not existing_cat:
                                new_cat = Category(**cat)
                                db.session.add(new_cat)
                        except Exception as e:
                            print(f"Error inserting category: {e}")
                
                elif table_name == 'pet_types':
                    # Handle pet_types table
                    pet_type_data = []
                    for row in re.findall(r'\((.*?)\)', values):
                        parts = [p.strip().strip("'\"") for p in row.split(',')]
                        if len(parts) >= 3:
                            pet_type_data.append({
                                'id': int(parts[0]) if parts[0] else None,
                                'name': parts[1],
                                'image_url': parts[2] if parts[2] else None
                            })
                    
                    for pet_type in pet_type_data:
                        try:
                            existing_pet = PetType.query.get(pet_type['id'])
                            if not existing_pet:
                                new_pet = PetType(**pet_type)
                                db.session.add(new_pet)
                        except Exception as e:
                            print(f"Error inserting pet type: {e}")
                
                elif table_name == 'products':
                    # Handle products table
                    product_data = []
                    for row in re.findall(r'\((.*?)\)', values):
                        parts = [p.strip().strip("'\"") for p in row.split(',')]
                        if len(parts) >= 12:
                            product_data.append({
                                'id': int(parts[0]) if parts[0] else None,
                                'name': parts[1],
                                'description': parts[2] if parts[2] else None,
                                'price': float(parts[3]) if parts[3] else 0.0,
                                'category_id': int(parts[4]) if parts[4] else None,
                                'pet_type_id': int(parts[5]) if parts[5] else None,
                                'stock_quantity': int(parts[6]) if parts[6] else 0,
                                'image_url': parts[7] if parts[7] else None,
                                'is_featured': bool(parts[8]) if parts[8] else False,
                                'rating': float(parts[9]) if parts[9] else 0.0,
                                'created_at': parts[10] if parts[10] else None,
                                'updated_at': parts[11] if parts[11] else None
                            })
                    
                    for product in product_data:
                        try:
                            existing_product = Product.query.get(product['id'])
                            if not existing_product:
                                new_product = Product(**product)
                                db.session.add(new_product)
                        except Exception as e:
                            print(f"Error inserting product: {e}")
                
                # Add more table handlers as needed...
                
            except Exception as e:
                print(f"Error processing table {table_name}: {e}")
        
        try:
            db.session.commit()
            print("Data imported successfully!")
        except Exception as e:
            print(f"Error committing data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    import_data()
