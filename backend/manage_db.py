#!/usr/bin/env python3
"""
Database management script for Terra Scope
This script provides utilities to inspect and manage the SQLite database
"""

import os
import sys
from database import db
from models.user import User
from models.soil_data import SoilData
from app import app
import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database and create all tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database initialized successfully!")
        print(f"📍 Database location: {os.path.abspath('terra_scope.db')}")

def show_db_info():
    """Show basic database information"""
    db_path = "instance/terra_scope.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file doesn't exist yet. Run 'init_db' first or create a user account.")
        return
    
    print(f"📍 Database location: {os.path.abspath(db_path)}")
    print(f"📊 Database size: {os.path.getsize(db_path)} bytes")
    print(f"🕒 Last modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    
    # Connect and show tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📋 Tables in database:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  • {table_name}: {count} records")
    
    conn.close()

def show_users():
    """Display all users in the database"""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("👥 No users found in database")
            return
        
        print(f"\n👥 Users ({len(users)} total):")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.first_name} {user.last_name}")
            print(f"Email: {user.email}")
            print(f"Location: {user.location or 'Not specified'}")
            print(f"Created: {user.created_at}")
            print("-" * 80)

def show_soil_data():
    """Display all soil data records"""
    with app.app_context():
        soil_records = SoilData.query.all()
        
        if not soil_records:
            print("🧪 No soil data found in database")
            return
        
        print(f"\n🧪 Soil Data ({len(soil_records)} total):")
        print("-" * 80)
        for record in soil_records:
            user = User.query.get(record.user_id)
            print(f"ID: {record.id}")
            print(f"User: {user.first_name} {user.last_name} ({user.email})")
            print(f"pH: {record.ph}")
            print(f"NPK: N={record.nitrogen}, P={record.phosphorus}, K={record.potassium}")
            print(f"Organic Carbon: {record.organic_carbon}%")
            print(f"Moisture: {record.moisture}%")
            print(f"Crop Type: {record.crop_type or 'Not specified'}")
            print(f"Season: {record.season or 'Not specified'}")
            print(f"Fertility Level: {record.fertility_level or 'Not analyzed'}")
            print(f"Created: {record.created_at}")
            print("-" * 80)

def create_sample_user():
    """Create a sample user for testing"""
    with app.app_context():
        from werkzeug.security import generate_password_hash
        
        # Check if user already exists
        existing_user = User.query.filter_by(email='demo@terrascope.com').first()
        if existing_user:
            print("👤 Demo user already exists!")
            return
        
        sample_user = User(
            first_name='Demo',
            last_name='Farmer',
            email='demo@terrascope.com',
            password=generate_password_hash('demo123'),
            location='New Delhi, India',
            contact_number='+91 9876543210'
        )
        
        db.session.add(sample_user)
        db.session.commit()
        
        print("✅ Sample user created!")
        print("📧 Email: demo@terrascope.com")
        print("🔑 Password: demo123")

def create_sample_soil_data():
    """Create sample soil data for the demo user"""
    with app.app_context():
        user = User.query.filter_by(email='demo@terrascope.com').first()
        if not user:
            print("❌ Demo user not found. Create sample user first.")
            return
        
        # Check if soil data already exists
        existing_data = SoilData.query.filter_by(user_id=user.id).first()
        if existing_data:
            print("🧪 Sample soil data already exists!")
            return
        
        sample_soil = SoilData(
            user_id=user.id,
            ph=6.8,
            nitrogen=120,
            phosphorus=25,
            potassium=150,
            organic_carbon=1.8,
            moisture=28,
            crop_type='Wheat',
            season='Spring',
            fertility_level='High',
            fertility_score=78.5
        )
        
        db.session.add(sample_soil)
        db.session.commit()
        
        print("✅ Sample soil data created!")

def drop_all_tables():
    """Drop all tables (USE WITH CAUTION!)"""
    confirm = input("⚠️  This will delete ALL data! Type 'DELETE ALL' to confirm: ")
    if confirm != 'DELETE ALL':
        print("❌ Operation cancelled.")
        return
    
    with app.app_context():
        db.drop_all()
        print("🗑️  All tables dropped!")

def backup_database():
    """Create a backup of the database"""
    db_path = "instance/terra_scope.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file doesn't exist yet.")
        return
    
    backup_name = f"terra_scope_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    import shutil
    shutil.copy2(db_path, backup_name)
    
    print(f"✅ Database backed up to: {backup_name}")

def execute_sql(sql_query):
    """Execute a custom SQL query"""
    db_path = "instance/terra_scope.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file doesn't exist yet.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        
        if sql_query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            if results:
                # Get column names
                columns = [description[0] for description in cursor.description]
                print(f"\n📊 Query Results ({len(results)} rows):")
                print("-" * 80)
                print(" | ".join(columns))
                print("-" * 80)
                for row in results:
                    print(" | ".join(str(cell) for cell in row))
            else:
                print("📊 No results found.")
        else:
            conn.commit()
            print("✅ Query executed successfully!")
            
    except Exception as e:
        print(f"❌ Error executing query: {e}")
    finally:
        conn.close()

def main():
    """Main menu for database management"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        commands = {
            'init': init_db,
            'info': show_db_info,
            'users': show_users,
            'soil': show_soil_data,
            'sample-user': create_sample_user,
            'sample-soil': create_sample_soil_data,
            'backup': backup_database,
            'drop': drop_all_tables
        }
        
        if command in commands:
            commands[command]()
        elif command == 'sql':
            if len(sys.argv) > 2:
                execute_sql(' '.join(sys.argv[2:]))
            else:
                print("Usage: python manage_db.py sql 'SELECT * FROM users'")
        else:
            print(f"Unknown command: {command}")
    else:
        print("🗄️  Terra Scope Database Manager")
        print("=" * 40)
        print("Available commands:")
        print("  init         - Initialize database")
        print("  info         - Show database info")
        print("  users        - Show all users")
        print("  soil         - Show all soil data")
        print("  sample-user  - Create demo user")
        print("  sample-soil  - Create sample soil data")
        print("  backup       - Backup database")
        print("  drop         - Drop all tables")
        print("  sql 'query'  - Execute custom SQL")
        print("\nUsage: python manage_db.py <command>")

if __name__ == "__main__":
    main()
