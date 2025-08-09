from flask import Blueprint, jsonify, request, session
from src.models.user import User, db
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create session
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'Registration successful'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username']) | (User.email == data['username'])
        ).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create session
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/change-password', methods=['POST'])
def change_password():
    """Change user password"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.json
        user = User.query.get(session['user_id'])
        
        if not user.check_password(data.get('current_password', '')):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Validate new password
        is_valid, message = validate_password(data.get('new_password', ''))
        if not is_valid:
            return jsonify({'error': message}), 400
        
        user.set_password(data['new_password'])
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/update-profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.json
        user = User.query.get(session['user_id'])
        
        # Update allowed fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.updated_at = datetime.utcnow()
        
        # Update email if provided and different
        if data.get('email') and data['email'] != user.email:
            if not validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already exists'}), 400
            
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/subscribe', methods=['POST'])
def subscribe():
    """Subscribe user to a plan"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.json
        user = User.query.get(session['user_id'])
        
        plan = data.get('plan')
        if plan not in ['starter', 'pro', 'ultimate']:
            return jsonify({'error': 'Invalid subscription plan'}), 400
        
        # Set subscription
        user.subscription_plan = plan
        user.subscription_expires = datetime.utcnow() + timedelta(days=30)  # 30 days subscription
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'user': user.to_dict(),
            'message': f'Successfully subscribed to {plan} plan'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

