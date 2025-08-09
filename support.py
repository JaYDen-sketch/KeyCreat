from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'payment', 'technical', 'account', 'refund', 'general'
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), nullable=False, default='open')  # open, in_progress, resolved, closed
    description = db.Column(db.Text, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('support_tickets', lazy=True))
    order = db.relationship('Order', backref=db.backref('support_tickets', lazy=True))

    def __repr__(self):
        return f'<SupportTicket {self.ticket_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ticket_number': self.ticket_number,
            'subject': self.subject,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'description': self.description,
            'order_id': self.order_id,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

class SupportMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_ticket.id'), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'user', 'admin'
    sender_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship
    ticket = db.relationship('SupportTicket', backref=db.backref('messages', lazy=True, order_by='SupportMessage.created_at'))

    def __repr__(self):
        return f'<SupportMessage {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'sender_type': self.sender_type,
            'sender_name': self.sender_name,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

