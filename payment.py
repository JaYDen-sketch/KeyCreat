from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'stripe', 'paypal', 'crypto'
    payment_provider = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, failed, refunded
    gateway_response = db.Column(db.Text, nullable=True)
    refund_amount = db.Column(db.Float, nullable=True, default=0.0)
    refund_reason = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.transaction_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'payment_method': self.payment_method,
            'payment_provider': self.payment_provider,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'gateway_response': self.gateway_response,
            'refund_amount': self.refund_amount,
            'refund_reason': self.refund_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

