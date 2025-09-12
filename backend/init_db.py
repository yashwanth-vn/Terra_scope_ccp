#!/usr/bin/env python3
"""
Database initialization script for Terra Scope
This script creates all database tables and sets up the initial database structure.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.user import User
from models.soil_data import SoilData
from models.chat import ChatSession, ChatMessage
from models.history import AnalysisHistory, UserActivity

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("- users")
        print("- soil_data")
        print("- chat_sessions")
        print("- chat_messages")
        print("- analysis_history")
        print("- user_activity")
        
        # Optional: Create a test user for development
        try:
            existing_user = User.query.filter_by(email='admin@terrascope.com').first()
            if not existing_user:
                test_user = User(
                    first_name='Terra',
                    last_name='Admin',
                    email='admin@terrascope.com',
                    password='hashed_password_here',  # In real app, this would be properly hashed
                    location='Test Location'
                )
                db.session.add(test_user)
                db.session.commit()
                print("\n✅ Test admin user created: admin@terrascope.com")
            else:
                print("\n✅ Test admin user already exists")
        except Exception as e:
            print(f"\n⚠️  Could not create test user: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()
