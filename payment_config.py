from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class PaymentConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(50), nullable=False)  # 'stripe', 'paypal', 'bank', 'crypto'
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Stripe Configuration
    stripe_publishable_key = db.Column(db.String(200), nullable=True)
    stripe_secret_key = db.Column(db.String(200), nullable=True)
    stripe_webhook_secret = db.Column(db.String(200), nullable=True)
    stripe_account_id = db.Column(db.String(100), nullable=True)
    
    # PayPal Configuration
    paypal_client_id = db.Column(db.String(200), nullable=True)
    paypal_client_secret = db.Column(db.String(200), nullable=True)
    paypal_email = db.Column(db.String(100), nullable=True)
    paypal_sandbox = db.Column(db.Boolean, nullable=False, default=True)
    
    # Bank Account Configuration
    bank_name = db.Column(db.String(100), nullable=True)
    bank_account_number = db.Column(db.String(50), nullable=True)
    bank_routing_number = db.Column(db.String(20), nullable=True)
    bank_account_holder = db.Column(db.String(100), nullable=True)
    bank_swift_code = db.Column(db.String(20), nullable=True)
    bank_iban = db.Column(db.String(50), nullable=True)
    
    # Cryptocurrency Configuration
    crypto_wallet_address = db.Column(db.String(200), nullable=True)
    crypto_currency = db.Column(db.String(20), nullable=True)  # 'BTC', 'ETH', 'USDT', etc.
    crypto_network = db.Column(db.String(50), nullable=True)  # 'Bitcoin', 'Ethereum', 'BSC', etc.
    
    # Additional Settings
    commission_percentage = db.Column(db.Float, nullable=False, default=0.0)
    minimum_payout = db.Column(db.Float, nullable=False, default=10.0)
    payout_frequency = db.Column(db.String(20), nullable=False, default='weekly')  # 'daily', 'weekly', 'monthly'
    
    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship
    creator = db.relationship('User', backref=db.backref('payment_configs', lazy=True))

    def __repr__(self):
        return f'<PaymentConfig {self.payment_method}>'

    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'payment_method': self.payment_method,
            'is_active': self.is_active,
            'commission_percentage': self.commission_percentage,
            'minimum_payout': self.minimum_payout,
            'payout_frequency': self.payout_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            # Only include sensitive data for admin users
            if self.payment_method == 'stripe':
                data.update({
                    'stripe_publishable_key': self.stripe_publishable_key,
                    'stripe_secret_key': self.stripe_secret_key,
                    'stripe_webhook_secret': self.stripe_webhook_secret,
                    'stripe_account_id': self.stripe_account_id
                })
            elif self.payment_method == 'paypal':
                data.update({
                    'paypal_client_id': self.paypal_client_id,
                    'paypal_client_secret': self.paypal_client_secret,
                    'paypal_email': self.paypal_email,
                    'paypal_sandbox': self.paypal_sandbox
                })
            elif self.payment_method == 'bank':
                data.update({
                    'bank_name': self.bank_name,
                    'bank_account_number': self.bank_account_number,
                    'bank_routing_number': self.bank_routing_number,
                    'bank_account_holder': self.bank_account_holder,
                    'bank_swift_code': self.bank_swift_code,
                    'bank_iban': self.bank_iban
                })
            elif self.payment_method == 'crypto':
                data.update({
                    'crypto_wallet_address': self.crypto_wallet_address,
                    'crypto_currency': self.crypto_currency,
                    'crypto_network': self.crypto_network
                })
        else:
            # Public data only
            if self.payment_method == 'paypal':
                data['paypal_email'] = self.paypal_email
            elif self.payment_method == 'crypto':
                data.update({
                    'crypto_currency': self.crypto_currency,
                    'crypto_network': self.crypto_network
                })
        
        return data

class PayoutRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_config_id = db.Column(db.Integer, db.ForeignKey('payment_config.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'processing', 'completed', 'failed'
    payout_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=True)
    payout_date = db.Column(db.DateTime, nullable=True)
    failure_reason = db.Column(db.String(500), nullable=True)
    
    # Period covered by this payout
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    payment_config = db.relationship('PaymentConfig', backref=db.backref('payouts', lazy=True))

    def __repr__(self):
        return f'<PayoutRecord {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'payment_config_id': self.payment_config_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payout_method': self.payout_method,
            'transaction_id': self.transaction_id,
            'payout_date': self.payout_date.isoformat() if self.payout_date else None,
            'failure_reason': self.failure_reason,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

