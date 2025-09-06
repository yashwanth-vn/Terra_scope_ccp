#!/usr/bin/env python3
"""
Quick database query script
Usage: python quick_query.py
"""

import sqlite3
import os

def connect_db():
    """Connect to the Terra Scope database"""
    db_path = "instance/terra_scope.db"
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return None
    return sqlite3.connect(db_path)

def main():
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Example queries
    print("📊 Users Summary:")
    cursor.execute("SELECT id, first_name, last_name, email, location FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"  ID: {user[0]} | {user[1]} {user[2]} | {user[3]} | {user[4] or 'No location'}")
    
    print("\n🧪 Soil Data Summary:")
    cursor.execute("""
        SELECT s.id, u.first_name, u.last_name, s.ph, s.nitrogen, 
               s.phosphorus, s.potassium, s.fertility_level, s.created_at
        FROM soil_data s 
        JOIN users u ON s.user_id = u.id
    """)
    soil_data = cursor.fetchall()
    for data in soil_data:
        print(f"  ID: {data[0]} | User: {data[1]} {data[2]} | pH: {data[3]} | NPK: {data[4]}/{data[5]}/{data[6]} | Level: {data[7]} | Date: {data[8]}")
    
    conn.close()

if __name__ == "__main__":
    main()
