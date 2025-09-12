import random
import re
from datetime import datetime
from models.soil_data import SoilData
from models.user import User
from services.enhanced_predictor import enhanced_predictor
import json

class AgriChatbot:
    def __init__(self):
        self.knowledge_base = {
            'greetings': [
                "Hello! I'm Terra Bot, your AI agricultural assistant. 🌱 I can help you with soil analysis, crop recommendations, and farming advice. What would you like to know?",
                "Hi there! Welcome to Terra Scope! 🚜 I'm here to help with your soil testing, fertilizer recommendations, and farming questions. How can I assist you?",
                "Greetings, farmer! 🌾 I'm your dedicated agricultural AI. I can analyze your soil data, suggest crops, and provide farming guidance. What's on your mind today?"
            ],
            
            'soil_ph': {
                'acidic': "Your soil is acidic (pH < 6.0). Consider adding lime to raise pH. Crops like blueberries, potatoes, and azaleas prefer acidic soil.",
                'neutral': "Great! Your soil has optimal pH (6.0-7.5). Most crops will thrive in this range.",
                'alkaline': "Your soil is alkaline (pH > 7.5). You can add sulfur or organic matter to lower pH if needed."
            },
            
            'nutrients': {
                'nitrogen': {
                    'low': "Nitrogen deficiency detected. Consider using nitrogen-rich fertilizers like urea or compost. Symptoms include yellowing leaves.",
                    'optimal': "Good nitrogen levels! This supports healthy leaf and stem growth.",
                    'high': "High nitrogen levels. Reduce nitrogen fertilizers to prevent excessive leaf growth at the expense of fruits."
                },
                'phosphorus': {
                    'low': "Low phosphorus can affect root development and flowering. Consider bone meal or rock phosphate.",
                    'optimal': "Excellent phosphorus levels for strong root systems and flower/fruit production.",
                    'high': "High phosphorus levels. Monitor to prevent nutrient imbalance."
                },
                'potassium': {
                    'low': "Potassium deficiency can affect disease resistance. Consider potash or wood ash.",
                    'optimal': "Good potassium levels support disease resistance and fruit quality.",
                    'high': "High potassium levels. Balance with other nutrients for optimal growth."
                }
            },
            
            'seasonal_advice': {
                'spring': "Spring is perfect for soil testing and preparation. Plant cool-season crops and prepare beds for summer planting.",
                'summer': "Focus on watering, pest management, and harvesting. Monitor soil moisture regularly.",
                'autumn': "Great time for planting winter crops and preparing soil amendments for next season.",
                'winter': "Plan for next season, maintain equipment, and consider cover crops to protect soil."
            },
            
            'crop_recommendations': {
                'high_fertility': ['Corn', 'Tomatoes', 'Peppers', 'Lettuce', 'Spinach'],
                'medium_fertility': ['Beans', 'Carrots', 'Onions', 'Potatoes', 'Cabbage'],
                'low_fertility': ['Radishes', 'Turnips', 'Herbs', 'Cover crops']
            },
            
            'weather_tips': [
                "Check weather forecasts before applying fertilizers - rain can wash away nutrients.",
                "Avoid working wet soil to prevent compaction.",
                "Drought conditions? Focus on mulching and efficient irrigation.",
                "Cold weather slows nutrient uptake - adjust fertilization accordingly."
            ]
        }
        
        self.question_patterns = {
            r'hello|hi|hey|greetings': 'greeting',
            r'ph|acidity|alkaline': 'ph_question',
            r'nitrogen|n\b': 'nitrogen_question',
            r'phosphorus|phosphate|p\b': 'phosphorus_question',
            r'potassium|potash|k\b': 'potassium_question',
            r'fertilizer|fertiliser': 'fertilizer_question',
            r'crop|plant|grow': 'crop_question',
            r'season|when|time': 'seasonal_question',
            r'weather|rain|drought': 'weather_question',
            r'help|assist': 'help_question'
        }
    
    def generate_response(self, message, user_id=None, context_data=None):
        """Generate intelligent response based on message and context"""
        message_lower = message.lower()
        
        # Determine message type
        message_type = self._classify_message(message_lower)
        
        # Get user's soil data for personalized responses
        user_soil_data = None
        if user_id:
            user_soil_data = SoilData.query.filter_by(user_id=user_id).order_by(SoilData.created_at.desc()).first()
        
        # Generate response based on message type and context
        response = self._generate_contextualized_response(message_type, message, user_soil_data, context_data)
        
        return {
            'response': response,
            'message_type': message_type,
            'suggestions': self._generate_suggestions(message_type, user_soil_data)
        }
    
    def _classify_message(self, message):
        """Classify message type based on patterns"""
        for pattern, msg_type in self.question_patterns.items():
            if re.search(pattern, message):
                return msg_type
        return 'general'
    
    def _generate_contextualized_response(self, message_type, original_message, soil_data, context_data):
        """Generate response with user context"""
        
        if message_type == 'greeting':
            return random.choice(self.knowledge_base['greetings'])
        
        elif message_type == 'ph_question':
            if soil_data:
                ph = soil_data.ph
                if ph < 6.0:
                    return f"Based on your recent soil test (pH: {ph}), {self.knowledge_base['soil_ph']['acidic']}"
                elif 6.0 <= ph <= 7.5:
                    return f"Your soil pH is {ph} - {self.knowledge_base['soil_ph']['neutral']}"
                else:
                    return f"Your soil pH is {ph} - {self.knowledge_base['soil_ph']['alkaline']}"
            return "Soil pH is crucial for nutrient availability. Ideal range is 6.0-7.5 for most crops. Would you like to test your soil?"
        
        elif message_type == 'nitrogen_question':
            return self._get_nutrient_advice('nitrogen', soil_data)
        
        elif message_type == 'phosphorus_question':
            return self._get_nutrient_advice('phosphorus', soil_data)
        
        elif message_type == 'potassium_question':
            return self._get_nutrient_advice('potassium', soil_data)
        
        elif message_type == 'fertilizer_question':
            return self._get_fertilizer_recommendation(soil_data)
        
        elif message_type == 'crop_question':
            return self._get_crop_recommendations(soil_data)
        
        elif message_type == 'seasonal_question':
            return self._get_seasonal_advice()
        
        elif message_type == 'weather_question':
            return random.choice(self.knowledge_base['weather_tips'])
        
        elif message_type == 'help_question':
            return self._get_help_response()
        
        else:
            return self._get_general_response(original_message, soil_data)
    
    def _get_nutrient_advice(self, nutrient, soil_data):
        """Get nutrient-specific advice"""
        if not soil_data:
            return f"I'd love to give you personalized {nutrient} advice! Please run a soil test first so I can analyze your specific needs."
        
        if nutrient == 'nitrogen':
            value = soil_data.nitrogen
            if value < 100:
                level = 'low'
            elif value < 200:
                level = 'optimal'
            else:
                level = 'high'
        elif nutrient == 'phosphorus':
            value = soil_data.phosphorus
            if value < 15:
                level = 'low'
            elif value < 25:
                level = 'optimal'
            else:
                level = 'high'
        else:  # potassium
            value = soil_data.potassium
            if value < 100:
                level = 'low'
            elif value < 150:
                level = 'optimal'
            else:
                level = 'high'
        
        return f"Your {nutrient} level is {value} mg/kg. {self.knowledge_base['nutrients'][nutrient][level]}"
    
    def _get_fertilizer_recommendation(self, soil_data):
        """Get fertilizer recommendations"""
        if not soil_data:
            return "For personalized fertilizer recommendations, please run a soil analysis first. I can then suggest the perfect fertilizer blend for your soil!"
        
        recommendations = []
        
        # Check each nutrient and recommend accordingly
        if soil_data.nitrogen < 100:
            recommendations.append("Add nitrogen-rich fertilizer (urea or ammonium sulfate)")
        if soil_data.phosphorus < 15:
            recommendations.append("Add phosphorus (bone meal or rock phosphate)")
        if soil_data.potassium < 100:
            recommendations.append("Add potassium (muriate of potash or wood ash)")
        
        if not recommendations:
            return "Your soil nutrient levels look good! Focus on maintaining with balanced fertilizer and organic matter."
        
        return f"Based on your soil analysis: {', '.join(recommendations)}. Apply according to package directions and retest in 3-6 months."
    
    def _get_crop_recommendations(self, soil_data):
        """Get crop recommendations based on soil fertility"""
        if not soil_data:
            return "I can suggest crops based on your soil condition! Please run a soil test first for personalized recommendations."
        
        fertility_level = soil_data.get_fertility_category().lower()
        
        if fertility_level == 'high':
            crops = self.knowledge_base['crop_recommendations']['high_fertility']
            return f"With your high-fertility soil, you can grow nutrient-demanding crops like: {', '.join(random.sample(crops, min(3, len(crops))))}."
        elif fertility_level == 'medium':
            crops = self.knowledge_base['crop_recommendations']['medium_fertility']
            return f"Your medium-fertility soil is perfect for crops like: {', '.join(random.sample(crops, min(3, len(crops))))}."
        else:
            crops = self.knowledge_base['crop_recommendations']['low_fertility']
            return f"For your current soil condition, start with hardy crops like: {', '.join(random.sample(crops, min(3, len(crops))))}. These will help build soil health."
    
    def _get_seasonal_advice(self):
        """Get seasonal farming advice"""
        current_month = datetime.now().month
        
        if current_month in [3, 4, 5]:  # Spring
            return self.knowledge_base['seasonal_advice']['spring']
        elif current_month in [6, 7, 8]:  # Summer
            return self.knowledge_base['seasonal_advice']['summer']
        elif current_month in [9, 10, 11]:  # Autumn
            return self.knowledge_base['seasonal_advice']['autumn']
        else:  # Winter
            return self.knowledge_base['seasonal_advice']['winter']
    
    def _get_help_response(self):
        """Get help information"""
        return """I can help you with:
        
🧪 Soil Analysis - Interpret your pH and nutrient levels
🌱 Crop Recommendations - Suggest best crops for your soil
💡 Fertilizer Advice - Recommend specific fertilizers
🌾 Seasonal Tips - Timing for planting and care
🌦️ Weather Considerations - Farm planning advice
        
Just ask me anything about farming, soil health, or crops!"""
    
    def _get_general_response(self, message, soil_data):
        """Generate general response for unclassified messages"""
        responses = [
            "That's an interesting question! Can you tell me more about your specific farming situation?",
            "I'm here to help with your agricultural needs. Could you provide more details?",
            "Let me help you with that farming question. What specific aspect would you like to know about?",
        ]
        
        if soil_data:
            responses.extend([
                f"Based on your recent soil test, I can provide more specific advice. What would you like to know?",
                f"I see you have soil data available. How can I help you interpret your results for better farming decisions?"
            ])
        
        return random.choice(responses)
    
    def _generate_suggestions(self, message_type, soil_data):
        """Generate suggested follow-up questions"""
        base_suggestions = [
            "What crops should I plant?",
            "How can I improve my soil?",
            "When should I apply fertilizer?",
            "What's the best pH for my crops?"
        ]
        
        if soil_data:
            personalized_suggestions = [
                f"Explain my pH level ({soil_data.ph})",
                f"How to improve my {soil_data.get_fertility_category().lower()} fertility soil?",
                "Show me my soil analysis summary"
            ]
            return random.sample(personalized_suggestions + base_suggestions, 3)
        
        return random.sample(base_suggestions, 3)

    def generate_session_title(self, first_message):
        """Generate a title for chat session based on first message"""
        message_lower = first_message.lower()
        
        if 'ph' in message_lower:
            return "Soil pH Discussion"
        elif any(word in message_lower for word in ['nitrogen', 'phosphorus', 'potassium', 'npk']):
            return "Nutrient Analysis Chat"
        elif 'crop' in message_lower or 'plant' in message_lower:
            return "Crop Recommendations"
        elif 'fertilizer' in message_lower:
            return "Fertilizer Guidance"
        elif any(word in message_lower for word in ['season', 'weather', 'time']):
            return "Seasonal Farming Advice"
        else:
            return f"Farming Chat - {datetime.now().strftime('%b %d')}"
