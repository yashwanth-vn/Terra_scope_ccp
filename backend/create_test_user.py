#!/usr/bin/env python3
"""
Create a test user for Terra Scope application
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash

def create_test_user():
    """Create a test user for development"""
    with app.app_context():
        try:
            # Check if test user already exists
            existing_user = User.query.filter_by(email='test@terrascope.com').first()
            if existing_user:
                print("✅ Test user already exists: test@terrascope.com")
                print("Password: test123")
                return

            # Create new test user with hashed password
            hashed_password = generate_password_hash('test123')
            test_user = User(
                first_name='Test',
                last_name='User',
                email='test@terrascope.com',
                password=hashed_password,
                location='Test Location'
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created successfully!")
            print("Email: test@terrascope.com")
            print("Password: test123")
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_test_user()
