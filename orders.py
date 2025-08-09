from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.models.order import Order
from src.models.payment import Payment
import uuid
import random
import string
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def generate_order_number():
    """Generate a unique order number"""
    return f"GV{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"

def generate_product_key(product_type, product_name):
    """Generate a mock product key or account details"""
    if product_type == 'steam_key':
        # Generate a mock Steam key
        key_parts = [''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(3)]
        return f"{'-'.join(key_parts)}"
    elif product_type == 'ott_service':
        # Generate mock account details
        username = f"user_{random.randint(1000, 9999)}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"Username: {username}\nPassword: {password}\nService: {product_name}"
    else:
        return "Subscription activated successfully"

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['user_id', 'product_type', 'product_name', 'product_price', 'original_price', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new order
        order = Order(
            user_id=data['user_id'],
            order_number=generate_order_number(),
            product_type=data['product_type'],
            product_name=data['product_name'],
            product_price=float(data['product_price']),
            original_price=float(data['original_price']),
            discount_percentage=data.get('discount_percentage', 0),
            payment_method=data['payment_method'],
            status='pending',
            payment_status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify(order.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/process-payment', methods=['POST'])
def process_payment(order_id):
    """Process payment for an order"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.json
        
        # Generate transaction ID
        transaction_id = f"txn_{uuid.uuid4().hex[:16]}"
        
        # Create payment record
        payment = Payment(
            order_id=order.id,
            user_id=order.user_id,
            payment_method=order.payment_method,
            payment_provider=data.get('payment_provider', 'stripe'),
            transaction_id=transaction_id,
            amount=order.product_price,
            status='completed',  # Mock successful payment
            completed_at=datetime.utcnow()
        )
        
        # Update order status
        order.payment_status = 'completed'
        order.status = 'completed'
        order.transaction_id = transaction_id
        order.product_key = generate_product_key(order.product_type, order.product_name)
        order.updated_at = datetime.utcnow()
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'order': order.to_dict(),
            'payment': payment.to_dict(),
            'message': 'Payment processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a specific user"""
    try:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders', methods=['GET'])
def get_all_orders():
    """Get all orders (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        orders = Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/refund', methods=['POST'])
def refund_order(order_id):
    """Process a refund for an order"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.json
        
        if order.status != 'completed':
            return jsonify({'error': 'Only completed orders can be refunded'}), 400
        
        # Update order status
        order.status = 'refunded'
        order.updated_at = datetime.utcnow()
        
        # Update payment record
        payment = Payment.query.filter_by(order_id=order.id).first()
        if payment:
            payment.status = 'refunded'
            payment.refund_amount = order.product_price
            payment.refund_reason = data.get('reason', 'Customer request')
            payment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'order': order.to_dict(),
            'message': 'Refund processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

