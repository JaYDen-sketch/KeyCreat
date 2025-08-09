#!/usr/bin/env python3
"""
Create Admin User Script
This script creates an admin user for the GameVault system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from gamevault_backend.src.models.user import User, db
from flask import Flask

def create_admin_user():
    """Create an admin user"""
    
    # Configure Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'gamevault-backend', 'src', 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("✅ Admin user already exists!")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            return
        
        # Get admin details
        print("🔧 Creating Admin User for GameVault")
        print("=" * 40)
        
        username = input("Enter admin username (default: admin): ").strip() or "admin"
        email = input("Enter admin email (default: admin@gamevault.com): ").strip() or "admin@gamevault.com"
        password = input("Enter admin password (default: admin123): ").strip() or "admin123"
        first_name = input("Enter first name (default: Admin): ").strip() or "Admin"
        last_name = input("Enter last name (default: User): ").strip() or "User"
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=True,
            is_active=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ Admin user created successfully!")
        print("=" * 40)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Admin Access: Yes")
        print("\n🔗 Access URLs:")
        print("Main Website: http://localhost:5001/")
        print("Admin Panel: http://localhost:5001/admin")
        print("Payment Config: http://localhost:5001/admin/payments")
        print("\n📚 API Documentation: /home/ubuntu/gamevault-api-documentation.md")

if __name__ == "__main__":
    create_admin_user()

