#!/usr/bin/env python3

from services.improved_chatbot import ImprovedAgriChatbot
from app import app
from models.user import User
from models.soil_data import SoilData

def test_improved_chatbot():
    """Test the improved chatbot functionality"""
    
    with app.app_context():
        # Initialize chatbot
        chatbot = ImprovedAgriChatbot()
        
        # Get demo user for testing
        user = User.query.filter_by(email='demo@terrascope.com').first()
        user_id = user.id if user else None
        
        # Test cases with expected better responses
        test_cases = [
            "Hello!",
            "What's my soil pH?", 
            "How much nitrogen do I need?",
            "What crops can I grow?",
            "My plants have yellow leaves",
            "When should I harvest tomatoes?",
            "How far apart should I plant lettuce?",
            "What fertilizer should I use?",
            "Help me with seasonal advice"
        ]
        
        print("🤖 Testing Improved Terra Bot Responses:")
        print("=" * 60)
        
        for i, test_message in enumerate(test_cases, 1):
            print(f"\n{i}. User: \"{test_message}\"")
            print("-" * 40)
            
            # Get chatbot response
            response_data = chatbot.generate_response(
                message=test_message,
                user_id=user_id
            )
            
            print(f"Bot: {response_data['response']}")
            print(f"Type: {response_data['message_type']}")
            print(f"Suggestions: {response_data['suggestions']}")
            
        print("\n" + "=" * 60)
        print("✅ Chatbot test completed!")

if __name__ == "__main__":
    test_improved_chatbot()
