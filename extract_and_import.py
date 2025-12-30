import sqlite3
import re

def extract_mysql_data(mysql_file):
    """Extract table structures and data from MySQL dump"""
    with open(mysql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by CREATE TABLE statements
    table_sections = re.split(r'CREATE TABLE `([^`]+)`', content, flags=re.IGNORECASE)
    
    tables = {}
    
    for i in range(1, len(table_sections), 2):
        table_name = table_sections[i]
        table_content = table_sections[i+1]
        
        # Extract table structure
        structure_match = re.search(r'\((.*?)\)\s*ENGINE', table_content, re.DOTALL)
        if structure_match:
            structure = structure_match.group(1)
            
            # Convert to SQLite format
            structure = re.sub(r'`([^`]+)`', r'\1', structure)  # Remove backticks
            structure = re.sub(r'int NOT NULL AUTO_INCREMENT', 'INTEGER PRIMARY KEY AUTOINCREMENT', structure)
            structure = re.sub(r'int NOT NULL', 'INTEGER', structure)
            structure = re.sub(r'\bint\b', 'INTEGER', structure)
            structure = re.sub(r'\bvarchar\(\d+\)', 'TEXT', structure)
            structure = re.sub(r'\btext\b', 'TEXT', structure)
            structure = re.sub(r'\bdatetime\b', 'TEXT', structure)
            structure = re.sub(r'\bdate\b', 'TEXT', structure)
            structure = re.sub(r'\btinyint\(1\)', 'INTEGER', structure)
            structure = re.sub(r'\bfloat\b', 'REAL', structure)
            structure = re.sub(r',\s*CONSTRAINT[^)]*\)', '', structure)  # Remove foreign key constraints
            structure = re.sub(r'CHARACTER SET \w+', '', structure)
            structure = re.sub(r'COLLATE \w+', '', structure)
            
            tables[table_name] = {
                'structure': structure,
                'data': []
            }
            
            # Extract INSERT statements
            insert_pattern = rf"INSERT INTO `{table_name}` (.*?)VALUES\s*(.*?);"
            insert_matches = re.findall(insert_pattern, table_content, re.DOTALL | re.IGNORECASE)
            
            for columns, values in insert_matches:
                # Clean up the values
                values = re.sub(r'\\n', ' ', values)
                values = re.sub(r'\\r', ' ', values)
                values = re.sub(r'\\\'', "'", values)
                values = re.sub(r'\\"', '"', values)
                
                tables[table_name]['data'].append(values)
    
    return tables

def create_sqlite_database(tables, db_file):
    """Create SQLite database with extracted data"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    for table_name, table_info in tables.items():
        try:
            # Create table
            create_sql = f"CREATE TABLE {table_name} ({table_info['structure']})"
            cursor.execute(create_sql)
            print(f"Created table: {table_name}")
            
            # Insert data
            for data_values in table_info['data']:
                insert_sql = f"INSERT INTO {table_name} VALUES {data_values}"
                try:
                    cursor.execute(insert_sql)
                except Exception as e:
                    print(f"Error inserting data into {table_name}: {e}")
                    print(f"Data: {data_values[:100]}...")
            
            print(f"Inserted data into: {table_name}")
            
        except Exception as e:
            print(f"Error with table {table_name}: {e}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    mysql_file = "instance/manv.sql"
    sqlite_file = "instance/petswale_complete.db"
    
    print("Extracting data from MySQL dump...")
    tables = extract_mysql_data(mysql_file)
    
    print(f"Found {len(tables)} tables")
    for table_name in tables.keys():
        print(f"  - {table_name}")
    
    print("Creating SQLite database...")
    create_sqlite_database(tables, sqlite_file)
    
    print(f"Database created: {sqlite_file}")
