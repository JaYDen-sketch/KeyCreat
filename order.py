from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    product_type = db.Column(db.String(50), nullable=False)  # 'steam_key', 'ott_service', 'subscription'
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    transaction_id = db.Column(db.String(100), nullable=True)
    product_key = db.Column(db.String(500), nullable=True)  # For steam keys or account details
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.order_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_number': self.order_number,
            'product_type': self.product_type,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'original_price': self.original_price,
            'discount_percentage': self.discount_percentage,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'transaction_id': self.transaction_id,
            'product_key': self.product_key,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

