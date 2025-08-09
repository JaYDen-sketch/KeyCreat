#!/usr/bin/env python3
"""
GameVault API Testing Script
This script demonstrates how to use the GameVault API endpoints.
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://localhost:5001/api"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*50}")

def test_health_check():
    """Test API health check"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def test_user_registration():
    """Test user registration"""
    user_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_response(response, "User Registration")
    
    if response.status_code == 201:
        return response.json().get('user', {}).get('id')
    return None

def test_user_login():
    """Test user login"""
    login_data = {
        "username": "testuser123",
        "password": "password123"
    }
    
    # Create session to maintain cookies
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "User Login")
    
    if response.status_code == 200:
        return session
    return None

def test_create_order(session, user_id):
    """Test order creation"""
    order_data = {
        "user_id": user_id,
        "product_type": "steam_key",
        "product_name": "Cyberpunk 2077",
        "product_price": 29.99,
        "original_price": 59.99,
        "discount_percentage": 50,
        "payment_method": "stripe"
    }
    
    response = session.post(f"{BASE_URL}/orders", json=order_data)
    print_response(response, "Create Order")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_process_payment(session, order_id):
    """Test payment processing"""
    payment_data = {
        "payment_provider": "stripe"
    }
    
    response = session.post(f"{BASE_URL}/orders/{order_id}/process-payment", json=payment_data)
    print_response(response, "Process Payment")
    return response.status_code == 200

def test_create_support_ticket(session, user_id, order_id=None):
    """Test support ticket creation"""
    ticket_data = {
        "user_id": user_id,
        "subject": "Payment Issue",
        "category": "payment",
        "priority": "medium",
        "description": "I'm having trouble with my payment for Cyberpunk 2077",
        "sender_name": "Test User"
    }
    
    if order_id:
        ticket_data["order_id"] = order_id
    
    response = session.post(f"{BASE_URL}/support/tickets", json=ticket_data)
    print_response(response, "Create Support Ticket")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_add_support_message(session, ticket_id):
    """Test adding message to support ticket"""
    message_data = {
        "sender_type": "admin",
        "sender_name": "Support Agent",
        "message": "Thank you for contacting us. We'll help you resolve this payment issue right away."
    }
    
    response = session.post(f"{BASE_URL}/support/tickets/{ticket_id}/messages", json=message_data)
    print_response(response, "Add Support Message")
    return response.status_code == 201

def test_get_user_orders(session, user_id):
    """Test getting user orders"""
    response = session.get(f"{BASE_URL}/orders/user/{user_id}")
    print_response(response, "Get User Orders")
    return response.status_code == 200

def test_get_support_categories(session):
    """Test getting support categories"""
    response = session.get(f"{BASE_URL}/support/categories")
    print_response(response, "Get Support Categories")
    return response.status_code == 200

def main():
    """Run all API tests"""
    print("🚀 Starting GameVault API Tests")
    print("=" * 60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("❌ API is not running. Please start the Flask server first.")
        return
    
    print("✅ API is healthy!")
    
    # Test 2: User Registration
    user_id = test_user_registration()
    if not user_id:
        print("❌ User registration failed")
        return
    
    print(f"✅ User registered with ID: {user_id}")
    
    # Test 3: User Login
    session = test_user_login()
    if not session:
        print("❌ User login failed")
        return
    
    print("✅ User logged in successfully")
    
    # Test 4: Create Order
    order_id = test_create_order(session, user_id)
    if not order_id:
        print("❌ Order creation failed")
        return
    
    print(f"✅ Order created with ID: {order_id}")
    
    # Test 5: Process Payment
    if test_process_payment(session, order_id):
        print("✅ Payment processed successfully")
    else:
        print("❌ Payment processing failed")
    
    # Test 6: Get User Orders
    if test_get_user_orders(session, user_id):
        print("✅ Retrieved user orders successfully")
    else:
        print("❌ Failed to retrieve user orders")
    
    # Test 7: Create Support Ticket
    ticket_id = test_create_support_ticket(session, user_id, order_id)
    if ticket_id:
        print(f"✅ Support ticket created with ID: {ticket_id}")
        
        # Test 8: Add Support Message
        if test_add_support_message(session, ticket_id):
            print("✅ Support message added successfully")
        else:
            print("❌ Failed to add support message")
    else:
        print("❌ Support ticket creation failed")
    
    # Test 9: Get Support Categories
    if test_get_support_categories(session):
        print("✅ Retrieved support categories successfully")
    else:
        print("❌ Failed to retrieve support categories")
    
    print("\n🎉 API Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

