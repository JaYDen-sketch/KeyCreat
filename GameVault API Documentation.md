# GameVault API Documentation

## Base URL
```
http://localhost:5001/api
```

## Authentication
The API uses session-based authentication. After login, the session is maintained automatically.

---

## 🔐 Authentication Endpoints

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required, min 8 chars)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "phone": "string (optional)"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "phone": null,
    "is_active": true,
    "is_admin": false,
    "subscription_plan": null,
    "subscription_expires": null,
    "created_at": "2025-08-06T10:30:00",
    "updated_at": "2025-08-06T10:30:00"
  },
  "message": "Registration successful"
}
```

### Login User
**POST** `/auth/login`

Login with username/email and password.

**Request Body:**
```json
{
  "username": "string (username or email)",
  "password": "string"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "subscription_plan": "pro",
    "subscription_expires": "2025-09-06T10:30:00"
  },
  "message": "Login successful"
}
```

### Logout User
**POST** `/auth/logout`

Logout current user and clear session.

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

### Get Current User
**GET** `/auth/me`

Get current logged-in user information.

**Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "subscription_plan": "pro",
  "subscription_expires": "2025-09-06T10:30:00"
}
```

### Change Password
**POST** `/auth/change-password`

Change user password (requires authentication).

**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string (min 8 chars)"
}
```

### Update Profile
**PUT** `/auth/update-profile`

Update user profile information (requires authentication).

**Request Body:**
```json
{
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)"
}
```

### Subscribe to Plan
**POST** `/auth/subscribe`

Subscribe user to a plan (requires authentication).

**Request Body:**
```json
{
  "plan": "string (starter|pro|ultimate)"
}
```

---

## 🛒 Order Management Endpoints

### Create Order
**POST** `/orders`

Create a new order for a product.

**Request Body:**
```json
{
  "user_id": 1,
  "product_type": "string (steam_key|ott_service|subscription)",
  "product_name": "string",
  "product_price": 29.99,
  "original_price": 59.99,
  "discount_percentage": 50,
  "payment_method": "string (stripe|paypal|crypto)"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "order_number": "GV202508061234",
  "product_type": "steam_key",
  "product_name": "Cyberpunk 2077",
  "product_price": 29.99,
  "original_price": 59.99,
  "discount_percentage": 50,
  "status": "pending",
  "payment_method": "stripe",
  "payment_status": "pending",
  "transaction_id": null,
  "product_key": null,
  "created_at": "2025-08-06T10:30:00",
  "updated_at": "2025-08-06T10:30:00"
}
```

### Process Payment
**POST** `/orders/{order_id}/process-payment`

Process payment for an order.

**Request Body:**
```json
{
  "payment_provider": "string (stripe|paypal)"
}
```

**Response (200):**
```json
{
  "order": {
    "id": 1,
    "order_number": "GV202508061234",
    "status": "completed",
    "payment_status": "completed",
    "transaction_id": "txn_abc123def456",
    "product_key": "ABCDE-FGHIJ-KLMNO"
  },
  "payment": {
    "id": 1,
    "transaction_id": "txn_abc123def456",
    "amount": 29.99,
    "status": "completed",
    "completed_at": "2025-08-06T10:35:00"
  },
  "message": "Payment processed successfully"
}
```

### Get User Orders
**GET** `/orders/user/{user_id}`

Get all orders for a specific user.

**Response (200):**
```json
[
  {
    "id": 1,
    "order_number": "GV202508061234",
    "product_type": "steam_key",
    "product_name": "Cyberpunk 2077",
    "product_price": 29.99,
    "status": "completed",
    "product_key": "ABCDE-FGHIJ-KLMNO",
    "created_at": "2025-08-06T10:30:00"
  }
]
```

### Get Order Details
**GET** `/orders/{order_id}`

Get details of a specific order.

### Get All Orders (Admin)
**GET** `/orders?page=1&per_page=20`

Get all orders with pagination (admin only).

**Response (200):**
```json
{
  "orders": [...],
  "total": 150,
  "pages": 8,
  "current_page": 1
}
```

### Refund Order
**POST** `/orders/{order_id}/refund`

Process a refund for an order.

**Request Body:**
```json
{
  "reason": "string (optional)"
}
```

---

## 🎧 Customer Support Endpoints

### Create Support Ticket
**POST** `/support/tickets`

Create a new support ticket.

**Request Body:**
```json
{
  "user_id": 1,
  "subject": "string",
  "category": "string (payment|technical|account|refund|general)",
  "priority": "string (low|medium|high|urgent)",
  "description": "string",
  "order_id": 1,
  "sender_name": "string"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "ticket_number": "TKT202508061234",
  "subject": "Payment Issue",
  "category": "payment",
  "priority": "medium",
  "status": "open",
  "description": "I'm having trouble with my payment",
  "order_id": 1,
  "assigned_to": null,
  "created_at": "2025-08-06T10:30:00",
  "updated_at": "2025-08-06T10:30:00",
  "resolved_at": null
}
```

### Get User Tickets
**GET** `/support/tickets/user/{user_id}`

Get all tickets for a specific user.

### Get Ticket Details
**GET** `/support/tickets/{ticket_id}`

Get ticket details with all messages.

**Response (200):**
```json
{
  "id": 1,
  "ticket_number": "TKT202508061234",
  "subject": "Payment Issue",
  "category": "payment",
  "priority": "medium",
  "status": "open",
  "description": "I'm having trouble with my payment",
  "messages": [
    {
      "id": 1,
      "sender_type": "user",
      "sender_name": "Test User",
      "message": "I'm having trouble with my payment",
      "created_at": "2025-08-06T10:30:00"
    },
    {
      "id": 2,
      "sender_type": "admin",
      "sender_name": "Support Agent",
      "message": "We'll help you resolve this issue",
      "created_at": "2025-08-06T10:35:00"
    }
  ]
}
```

### Get All Tickets (Admin)
**GET** `/support/tickets?page=1&per_page=20&status=open&category=payment&priority=high`

Get all tickets with filtering and pagination (admin only).

### Add Message to Ticket
**POST** `/support/tickets/{ticket_id}/messages`

Add a message to a support ticket.

**Request Body:**
```json
{
  "sender_type": "string (user|admin)",
  "sender_name": "string",
  "message": "string"
}
```

### Update Ticket Status
**PUT** `/support/tickets/{ticket_id}/status`

Update ticket status and assignment.

**Request Body:**
```json
{
  "status": "string (open|in_progress|resolved|closed)",
  "priority": "string (low|medium|high|urgent)",
  "assigned_to": "string"
}
```

### Get Support Statistics (Admin)
**GET** `/support/stats`

Get support statistics and analytics.

**Response (200):**
```json
{
  "total_tickets": 150,
  "open_tickets": 25,
  "in_progress_tickets": 30,
  "resolved_tickets": 80,
  "closed_tickets": 15,
  "categories": {
    "payment": 45,
    "technical": 35,
    "account": 25,
    "refund": 20,
    "general": 25
  },
  "priorities": {
    "low": 30,
    "medium": 80,
    "high": 35,
    "urgent": 5
  }
}
```

### Get Support Categories
**GET** `/support/categories`

Get available support categories.

**Response (200):**
```json
[
  {"value": "payment", "label": "Payment Issues"},
  {"value": "technical", "label": "Technical Support"},
  {"value": "account", "label": "Account Issues"},
  {"value": "refund", "label": "Refund Request"},
  {"value": "general", "label": "General Inquiry"}
]
```

---

## 👥 User Management Endpoints

### Get All Users (Admin)
**GET** `/users`

Get all users.

### Create User (Admin)
**POST** `/users`

Create a new user.

### Get User Details
**GET** `/users/{user_id}`

Get specific user details.

### Update User (Admin)
**PUT** `/users/{user_id}`

Update user information.

### Delete User (Admin)
**DELETE** `/users/{user_id}`

Delete a user account.

---

## 🏥 Health Check

### API Health Check
**GET** `/health`

Check if the API is running.

**Response (200):**
```json
{
  "status": "healthy",
  "message": "GameVault API is running"
}
```

---

## Error Responses

All endpoints may return these error responses:

**400 Bad Request:**
```json
{
  "error": "Missing required field: username"
}
```

**401 Unauthorized:**
```json
{
  "error": "Not authenticated"
}
```

**404 Not Found:**
```json
{
  "error": "User not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Database connection failed"
}
```

---

## Example Usage

### Complete Purchase Flow

1. **Register/Login User**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "gamer123", "email": "gamer@example.com", "password": "password123"}'
```

2. **Create Order**
```bash
curl -X POST http://localhost:5001/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_type": "steam_key", "product_name": "Cyberpunk 2077", "product_price": 29.99, "original_price": 59.99, "discount_percentage": 50, "payment_method": "stripe"}'
```

3. **Process Payment**
```bash
curl -X POST http://localhost:5001/api/orders/1/process-payment \
  -H "Content-Type: application/json" \
  -d '{"payment_provider": "stripe"}'
```

### Support Ticket Flow

1. **Create Ticket**
```bash
curl -X POST http://localhost:5001/api/support/tickets \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "subject": "Payment Issue", "category": "payment", "description": "My payment failed", "sender_name": "John Doe"}'
```

2. **Add Response**
```bash
curl -X POST http://localhost:5001/api/support/tickets/1/messages \
  -H "Content-Type: application/json" \
  -d '{"sender_type": "admin", "sender_name": "Support Agent", "message": "We will help you resolve this issue"}'
```

---

## Database Schema

### Users Table
- id, username, email, password_hash
- first_name, last_name, phone
- is_active, is_admin
- subscription_plan, subscription_expires
- created_at, updated_at

### Orders Table
- id, user_id, order_number
- product_type, product_name, product_price, original_price
- discount_percentage, status, payment_method, payment_status
- transaction_id, product_key
- created_at, updated_at

### Payments Table
- id, order_id, user_id
- payment_method, payment_provider, transaction_id
- amount, currency, status
- gateway_response, refund_amount, refund_reason
- created_at, updated_at, completed_at

### Support Tickets Table
- id, user_id, ticket_number
- subject, category, priority, status
- description, order_id, assigned_to
- created_at, updated_at, resolved_at

### Support Messages Table
- id, ticket_id, sender_type, sender_name
- message, created_at



---

## 💰 Payment Configuration Endpoints (Admin Only)

### Create/Update Payment Configuration
**POST** `/payment-config`

Configure payment methods for receiving customer payments.

**Request Body (Stripe):**
```json
{
  "payment_method": "stripe",
  "stripe_publishable_key": "pk_live_...",
  "stripe_secret_key": "sk_live_...",
  "stripe_webhook_secret": "whsec_...",
  "stripe_account_id": "acct_...",
  "is_active": true,
  "commission_percentage": 2.5,
  "minimum_payout": 10.0,
  "payout_frequency": "weekly"
}
```

**Request Body (PayPal):**
```json
{
  "payment_method": "paypal",
  "paypal_client_id": "your_client_id",
  "paypal_client_secret": "your_client_secret",
  "paypal_email": "your@paypal.com",
  "paypal_sandbox": false,
  "is_active": true,
  "commission_percentage": 2.5,
  "minimum_payout": 10.0,
  "payout_frequency": "weekly"
}
```

**Request Body (Bank Account):**
```json
{
  "payment_method": "bank",
  "bank_name": "Your Bank Name",
  "bank_account_number": "1234567890",
  "bank_routing_number": "123456789",
  "bank_account_holder": "Your Full Name",
  "bank_swift_code": "ABCDUS33",
  "bank_iban": "US12345678901234567890",
  "is_active": true,
  "commission_percentage": 0.0,
  "minimum_payout": 50.0,
  "payout_frequency": "monthly"
}
```

**Request Body (Cryptocurrency):**
```json
{
  "payment_method": "crypto",
  "crypto_wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "crypto_currency": "BTC",
  "crypto_network": "Bitcoin",
  "is_active": true,
  "commission_percentage": 1.0,
  "minimum_payout": 25.0,
  "payout_frequency": "weekly"
}
```

**Response (201/200):**
```json
{
  "config": {
    "id": 1,
    "payment_method": "stripe",
    "is_active": true,
    "commission_percentage": 2.5,
    "minimum_payout": 10.0,
    "payout_frequency": "weekly",
    "stripe_publishable_key": "pk_live_...",
    "stripe_secret_key": "sk_live_...",
    "created_at": "2025-08-06T10:30:00",
    "updated_at": "2025-08-06T10:30:00"
  },
  "message": "Stripe configuration saved successfully"
}
```

### Get All Payment Configurations
**GET** `/payment-config`

Get all configured payment methods (admin only).

**Response (200):**
```json
[
  {
    "id": 1,
    "payment_method": "stripe",
    "is_active": true,
    "commission_percentage": 2.5,
    "minimum_payout": 10.0,
    "payout_frequency": "weekly",
    "stripe_publishable_key": "pk_live_...",
    "created_at": "2025-08-06T10:30:00"
  },
  {
    "id": 2,
    "payment_method": "paypal",
    "is_active": true,
    "commission_percentage": 2.5,
    "paypal_email": "your@paypal.com",
    "created_at": "2025-08-06T10:35:00"
  }
]
```

### Get Specific Payment Configuration
**GET** `/payment-config/{payment_method}`

Get configuration for a specific payment method.

### Delete Payment Configuration
**DELETE** `/payment-config/{payment_method}`

Delete a payment method configuration.

### Toggle Payment Configuration
**POST** `/payment-config/{payment_method}/toggle`

Enable or disable a payment method.

### Get Public Payment Methods
**GET** `/payment-methods/public`

Get available payment methods for customers (public endpoint).

**Response (200):**
```json
[
  {
    "method": "stripe",
    "name": "Stripe"
  },
  {
    "method": "paypal",
    "name": "PayPal",
    "email": "your@paypal.com"
  },
  {
    "method": "crypto",
    "name": "Crypto",
    "currency": "BTC",
    "network": "Bitcoin"
  }
]
```

### Get Payout History
**GET** `/payouts?page=1&per_page=20`

Get payout history with pagination (admin only).

**Response (200):**
```json
{
  "payouts": [
    {
      "id": 1,
      "payment_config_id": 1,
      "amount": 150.75,
      "currency": "USD",
      "status": "completed",
      "payout_method": "stripe",
      "transaction_id": "po_1234567890",
      "payout_date": "2025-08-06T10:30:00",
      "period_start": "2025-07-30T00:00:00",
      "period_end": "2025-08-06T00:00:00",
      "created_at": "2025-08-06T10:30:00"
    }
  ],
  "total": 25,
  "pages": 2,
  "current_page": 1
}
```

### Get Payout Summary
**GET** `/payouts/summary`

Get payout summary and statistics (admin only).

**Response (200):**
```json
{
  "total_revenue": 2500.75,
  "total_payouts": 2000.50,
  "pending_payouts": 150.25,
  "available_balance": 350.00,
  "recent_payouts": [
    {
      "id": 1,
      "amount": 150.75,
      "status": "completed",
      "payout_method": "stripe",
      "payout_date": "2025-08-06T10:30:00"
    }
  ]
}
```

### Request Manual Payout
**POST** `/payouts/request`

Request a manual payout (admin only).

**Request Body:**
```json
{
  "payment_method": "stripe",
  "amount": 100.00
}
```

**Response (201):**
```json
{
  "payout": {
    "id": 2,
    "payment_config_id": 1,
    "amount": 100.00,
    "currency": "USD",
    "status": "pending",
    "payout_method": "stripe",
    "period_start": "2025-07-06T10:30:00",
    "period_end": "2025-08-06T10:30:00",
    "created_at": "2025-08-06T10:30:00"
  },
  "message": "Payout request created successfully"
}
```

---

## 🔧 Payment Configuration Features

### Supported Payment Methods
1. **Stripe**: Credit/debit cards, digital wallets
2. **PayPal**: PayPal accounts, credit/debit cards
3. **Bank Transfer**: Direct bank account transfers
4. **Cryptocurrency**: Bitcoin, Ethereum, USDT, etc.

### Configuration Options
- **Commission Percentage**: Platform fee (0-100%)
- **Minimum Payout**: Minimum amount for payouts
- **Payout Frequency**: Daily, weekly, or monthly
- **Active Status**: Enable/disable payment methods

### Security Features
- **Encrypted Storage**: Sensitive data is securely stored
- **Admin Only Access**: Only admin users can configure payments
- **Validation**: Input validation for all payment details
- **Audit Trail**: Track all configuration changes

### Payout Management
- **Automatic Payouts**: Based on frequency settings
- **Manual Payouts**: Request payouts on demand
- **Payout History**: Track all payout transactions
- **Balance Tracking**: Monitor available balance
- **Multi-method Support**: Use multiple payment methods

---

## 📊 Updated Database Schema

### Payment Config Table
- id, payment_method, is_active
- stripe_publishable_key, stripe_secret_key, stripe_webhook_secret, stripe_account_id
- paypal_client_id, paypal_client_secret, paypal_email, paypal_sandbox
- bank_name, bank_account_number, bank_routing_number, bank_account_holder, bank_swift_code, bank_iban
- crypto_wallet_address, crypto_currency, crypto_network
- commission_percentage, minimum_payout, payout_frequency
- created_at, updated_at, created_by

### Payout Records Table
- id, payment_config_id, amount, currency, status
- payout_method, transaction_id, payout_date, failure_reason
- period_start, period_end
- created_at, updated_at

