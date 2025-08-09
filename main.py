import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.models.order import Order
from src.models.payment import Payment
from src.models.support import SupportTicket, SupportMessage
from src.models.payment_config import PaymentConfig, PayoutRecord
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.orders import orders_bp
from src.routes.support import support_bp
from src.routes.payment_config import payment_config_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(orders_bp, url_prefix='/api')
app.register_blueprint(support_bp, url_prefix='/api')
app.register_blueprint(payment_config_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# API health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'message': 'GameVault API is running'}, 200

# Admin routes
@app.route('/admin')
def admin_redirect():
    return send_from_directory(app.static_folder, 'admin-payment-setup.html')

@app.route('/admin/payments')
def admin_payments():
    return send_from_directory(app.static_folder, 'admin-payment-setup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
