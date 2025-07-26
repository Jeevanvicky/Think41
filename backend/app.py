from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock E-commerce Dataset - In production, this would come from a database
ECOMMERCE_DATA = {
    "products": [
        {"id": 1, "name": "Classic T-Shirt", "category": "shirts", "price": 29.99, "stock": 45, "sales": 1250},
        {"id": 2, "name": "Denim Jeans", "category": "pants", "price": 79.99, "stock": 32, "sales": 980},
        {"id": 3, "name": "Summer Dress", "category": "dresses", "price": 59.99, "stock": 18, "sales": 756},
        {"id": 4, "name": "Hoodie Sweatshirt", "category": "sweatshirts", "price": 49.99, "stock": 28, "sales": 642},
        {"id": 5, "name": "Running Shorts", "category": "shorts", "price": 24.99, "stock": 55, "sales": 534},
        {"id": 6, "name": "Polo Shirt", "category": "shirts", "price": 39.99, "stock": 41, "sales": 423},
        {"id": 7, "name": "Maxi Dress", "category": "dresses", "price": 69.99, "stock": 12, "sales": 389},
        {"id": 8, "name": "Cargo Pants", "category": "pants", "price": 64.99, "stock": 25, "sales": 287}
    ],
    "orders": [
        {"id": 12345, "status": "shipped", "tracking": "TRK123456789", "date": "2024-07-20", "total": 89.98},
        {"id": 12346, "status": "processing", "tracking": None, "date": "2024-07-25", "total": 129.97},
        {"id": 12347, "status": "delivered", "tracking": "TRK987654321", "date": "2024-07-18", "total": 59.99}
    ]
}

class ChatbotService:
    def __init__(self):
        self.products = ECOMMERCE_DATA["products"]
        self.orders = ECOMMERCE_DATA["orders"]
    
    def process_message(self, message):
        """Main function to process user messages and return appropriate responses"""
        message_lower = message.lower()
        
        # Check for different types of queries
        if "top" in message_lower and ("product" in message_lower or "sold" in message_lower):
            return self.get_top_products(message)
        
        elif "order" in message_lower and ("status" in message_lower or "id" in message_lower):
            return self.get_order_status(message)
        
        elif "stock" in message_lower or "left" in message_lower:
            return self.check_stock(message)
        
        elif "price" in message_lower:
            return self.get_price_info(message)
        
        elif "help" in message_lower or "support" in message_lower:
            return self.get_help_menu()
        
        elif any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return {
                "response": "Hello! Welcome to our clothing store support chat. I can help you with:\n\n• Product information and stock levels\n• Order status updates\n• Top selling items\n• Pricing information\n\nWhat can I help you with today?",
                "type": "greeting"
            }
        
        else:
            return self.handle_general_query(message)
    
    def get_top_products(self, message):
        """Get top selling products"""
        # Extract number if specified
        num_match = re.search(r'\d+', message)
        num_products = int(num_match.group()) if num_match else 5
        num_products = min(num_products, len(self.products))
        
        # Sort products by sales
        top_products = sorted(self.products, key=lambda x: x['sales'], reverse=True)[:num_products]
        
        response = f"Here are the top {num_products} most sold products:\n\n"
        for i, product in enumerate(top_products, 1):
            response += f"{i}. {product['name']} - {product['sales']} sold (${product['price']})\n"
        
        return {
            "response": response,
            "type": "product_list",
            "data": top_products
        }
    
    def get_order_status(self, message):
        """Get order status by ID"""
        # Extract order ID from message
        order_id_match = re.search(r'\b\d{5}\b', message)
        
        if not order_id_match:
            return {
                "response": "Please provide a valid 5-digit order ID to check the status. For example: 'What's the status of order 12345?'",
                "type": "error"
            }
        
        order_id = int(order_id_match.group())
        order = next((o for o in self.orders if o['id'] == order_id), None)
        
        if not order:
            return {
                "response": f"Sorry, I couldn't find an order with ID {order_id}. Please check your order number and try again.",
                "type": "error"
            }
        
        status = order['status'].title()
        date = order['date']
        total = order['total']
        
        response = f"Order #{order_id} Status: {status}\n"
        response += f"Order Date: {date}\n"
        response += f"Total: ${total}\n"
        
        if order['tracking']:
            response += f"Tracking Number: {order['tracking']}\n"
        
        if status == "Shipped":
            response += "\nYour order is on its way! You should receive it within 3-5 business days."
        elif status == "Processing":
            response += "\nYour order is being prepared for shipment. We'll send you a tracking number once it ships."
        elif status == "Delivered":
            response += "\nYour order has been delivered! If you have any issues, please contact our support team."
        
        return {
            "response": response,
            "type": "order_status",
            "data": order
        }
    
    def check_stock(self, message):
        """Check stock levels for products"""
        # Try to find product name in message
        product_found = None
        for product in self.products:
            if product['name'].lower() in message.lower():
                product_found = product
                break
        
        if not product_found:
            # If no specific product found, show all stock levels
            response = "Here are the current stock levels:\n\n"
            for product in self.products:
                status = "In Stock" if product['stock'] > 10 else "Low Stock" if product['stock'] > 0 else "Out of Stock"
                response += f"• {product['name']}: {product['stock']} units ({status})\n"
            
            return {
                "response": response,
                "type": "stock_list",
                "data": self.products
            }
        
        stock = product_found['stock']
        name = product_found['name']
        
        if stock > 10:
            status_msg = f"Good news! We have {stock} {name}s in stock."
        elif stock > 0:
            status_msg = f"We have {stock} {name}s left in stock (limited quantity)."
        else:
            status_msg = f"Sorry, {name}s are currently out of stock. Check back soon!"
        
        return {
            "response": status_msg,
            "type": "stock_check",
            "data": product_found
        }
    
    def get_price_info(self, message):
        """Get pricing information"""
        product_found = None
        for product in self.products:
            if product['name'].lower() in message.lower():
                product_found = product
                break
        
        if not product_found:
            response = "Here are our current prices:\n\n"
            for product in sorted(self.products, key=lambda x: x['price']):
                response += f"• {product['name']}: ${product['price']}\n"
            
            return {
                "response": response,
                "type": "price_list",
                "data": self.products
            }
        
        return {
            "response": f"The {product_found['name']} is priced at ${product_found['price']}.",
            "type": "price_info",
            "data": product_found
        }
    
    def get_help_menu(self):
        """Return help menu"""
        response = """I can help you with the following:

🛍️ **Product Information**
• "What are the top 5 most sold products?"
• "How many Classic T-Shirts are left in stock?"
• "What's the price of Summer Dress?"

📦 **Order Support**
• "Show me the status of order ID 12345"
• "Track my order 12346"

💰 **Pricing & Stock**
• "Show me all prices"
• "Check stock levels"

Just ask me anything about our products or your orders!"""
        
        return {
            "response": response,
            "type": "help"
        }
    
    def handle_general_query(self, message):
        """Handle general queries that don't match specific patterns"""
        return {
            "response": "I'm not sure I understand that request. Here are some things I can help you with:\n\n• Check product stock levels\n• Get order status updates\n• Show top selling products\n• Provide pricing information\n\nTry asking something like 'What are the top 5 products?' or 'Check stock for Classic T-Shirt'",
            "type": "general"
        }

# Initialize chatbot service
chatbot = ChatbotService()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400
        
        # Process the message
        response_data = chatbot.process_message(message)
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            **response_data
        })
    
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({
        "success": True,
        "data": ECOMMERCE_DATA["products"]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)