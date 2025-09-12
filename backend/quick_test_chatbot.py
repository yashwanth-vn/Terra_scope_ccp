from services.improved_chatbot import ImprovedAgriChatbot
chatbot = ImprovedAgriChatbot()

# Test classification
tests = [
    'What crops can I grow?',
    'When should I harvest tomatoes?', 
    'How far apart should I plant lettuce?',
    'Help me with seasonal advice',
    'My plants have yellow leaves',
    'What fertilizer should I use?'
]

print("Testing message classification:")
for test in tests:
    msg_type = chatbot._classify_message(test.lower())
    print(f'Message: "{test}" -> Type: {msg_type}')
