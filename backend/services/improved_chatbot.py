import random
import re
from datetime import datetime
from models.soil_data import SoilData
from models.user import User
from services.enhanced_predictor import enhanced_predictor
import json

class ImprovedAgriChatbot:
    def __init__(self):
        self.knowledge_base = {
            'greetings': [
                "Hello! I'm Terra Bot, your AI agricultural assistant. 🌱 I can help you with soil analysis, crop recommendations, and farming advice. What would you like to know?",
                "Hi there! Welcome to Terra Scope! 🚜 I'm here to help with your soil testing, fertilizer recommendations, and farming questions. How can I assist you?",
                "Greetings, farmer! 🌾 I'm your dedicated agricultural AI. I can analyze your soil data, suggest crops, and provide farming guidance. What's on your mind today?"
            ],
            
            'soil_analysis': {
                'ph_ranges': {
                    'very_acidic': (0, 5.0, "Very acidic soil. Most crops struggle. Consider lime application. Good for blueberries, azaleas."),
                    'acidic': (5.0, 6.0, "Acidic soil. Add lime to raise pH. Suitable for potatoes, sweet potatoes, berries."),
                    'optimal': (6.0, 7.5, "Excellent pH range! Most crops thrive here. This is ideal for vegetables and grains."),
                    'alkaline': (7.5, 8.5, "Alkaline soil. Consider sulfur to lower pH. Good for asparagus, cabbage, spinach."),
                    'very_alkaline': (8.5, 14, "Very alkaline. Nutrient lockup likely. Use sulfur, organic matter. Limited crop options.")
                },
                'nutrient_thresholds': {
                    'nitrogen': {'low': 80, 'optimal': 200, 'unit': 'mg/kg', 'deficiency_symptoms': 'yellowing leaves, stunted growth'},
                    'phosphorus': {'low': 15, 'optimal': 40, 'unit': 'mg/kg', 'deficiency_symptoms': 'purple leaves, poor root development'},
                    'potassium': {'low': 100, 'optimal': 200, 'unit': 'mg/kg', 'deficiency_symptoms': 'brown leaf edges, weak stems'}
                }
            },
            
            'crop_database': {
                'vegetables': {
                    'Tomatoes': {'ph_range': (6.0, 7.0), 'fertility_need': 'high', 'season': 'warm', 'spacing': '18-24 inches'},
                    'Lettuce': {'ph_range': (6.0, 7.0), 'fertility_need': 'medium', 'season': 'cool', 'spacing': '6-8 inches'},
                    'Carrots': {'ph_range': (6.0, 7.0), 'fertility_need': 'low', 'season': 'cool', 'spacing': '2-3 inches'},
                    'Peppers': {'ph_range': (6.0, 7.0), 'fertility_need': 'high', 'season': 'warm', 'spacing': '12-18 inches'},
                    'Spinach': {'ph_range': (6.5, 7.5), 'fertility_need': 'medium', 'season': 'cool', 'spacing': '4-6 inches'},
                    'Onions': {'ph_range': (6.0, 7.0), 'fertility_need': 'medium', 'season': 'cool', 'spacing': '4-6 inches'},
                    'Potatoes': {'ph_range': (4.8, 6.5), 'fertility_need': 'high', 'season': 'cool', 'spacing': '12-15 inches'},
                    'Cabbage': {'ph_range': (6.0, 7.5), 'fertility_need': 'high', 'season': 'cool', 'spacing': '12-18 inches'}
                },
                'grains': {
                    'Wheat': {'ph_range': (6.0, 7.5), 'fertility_need': 'medium', 'season': 'cool'},
                    'Corn': {'ph_range': (6.0, 6.8), 'fertility_need': 'high', 'season': 'warm'},
                    'Rice': {'ph_range': (5.5, 7.0), 'fertility_need': 'high', 'season': 'warm'},
                    'Barley': {'ph_range': (6.0, 8.0), 'fertility_need': 'medium', 'season': 'cool'}
                },
                'fruits': {
                    'Blueberries': {'ph_range': (4.5, 5.5), 'fertility_need': 'low', 'season': 'perennial'},
                    'Strawberries': {'ph_range': (5.5, 6.5), 'fertility_need': 'medium', 'season': 'cool'}
                }
            },
            
            'fertilizer_guide': {
                'nitrogen_sources': {
                    'Urea': {'n_content': 46, 'release': 'quick', 'best_for': 'vegetative growth'},
                    'Ammonium Sulfate': {'n_content': 21, 'release': 'medium', 'best_for': 'acidic soils'},
                    'Calcium Nitrate': {'n_content': 15, 'release': 'quick', 'best_for': 'alkaline soils'},
                    'Compost': {'n_content': 2, 'release': 'slow', 'best_for': 'organic matter improvement'}
                },
                'phosphorus_sources': {
                    'DAP': {'p_content': 18, 'best_for': 'general use'},
                    'Superphosphate': {'p_content': 16, 'best_for': 'acidic soils'},
                    'Bone Meal': {'p_content': 12, 'best_for': 'organic gardening'}
                },
                'potassium_sources': {
                    'Muriate of Potash': {'k_content': 60, 'best_for': 'most crops'},
                    'Sulfate of Potash': {'k_content': 50, 'best_for': 'salt-sensitive crops'},
                    'Wood Ash': {'k_content': 5, 'best_for': 'organic gardening'}
                }
            },
            
            'seasonal_guide': {
                'spring': {
                    'tasks': ['soil testing', 'bed preparation', 'cool-season planting', 'fertilizer application'],
                    'crops': ['lettuce', 'spinach', 'peas', 'carrots', 'onions'],
                    'tips': 'Test soil pH and nutrients. Prepare beds with compost. Plant cool-season crops.'
                },
                'summer': {
                    'tasks': ['watering management', 'pest control', 'harvesting', 'succession planting'],
                    'crops': ['tomatoes', 'peppers', 'corn', 'beans', 'squash'],
                    'tips': 'Focus on consistent watering. Monitor for pests. Harvest regularly.'
                },
                'autumn': {
                    'tasks': ['winter prep', 'cover crops', 'soil amendments', 'tool maintenance'],
                    'crops': ['winter wheat', 'cover crops', 'late vegetables'],
                    'tips': 'Plant cover crops. Add organic matter. Prepare for winter.'
                },
                'winter': {
                    'tasks': ['planning', 'seed ordering', 'equipment maintenance', 'soil planning'],
                    'crops': ['plan next season', 'greenhouse crops'],
                    'tips': 'Plan crop rotation. Order seeds. Maintain equipment.'
                }
            },
            
            'problem_solving': {
                'yellowing_leaves': {
                    'causes': ['nitrogen deficiency', 'overwatering', 'disease', 'natural aging'],
                    'solutions': ['apply nitrogen fertilizer', 'improve drainage', 'disease management', 'normal if lower leaves']
                },
                'poor_growth': {
                    'causes': ['nutrient deficiency', 'wrong pH', 'compacted soil', 'inadequate water'],
                    'solutions': ['soil test and fertilize', 'adjust pH', 'aerate soil', 'irrigation management']
                },
                'pest_problems': {
                    'prevention': ['crop rotation', 'beneficial insects', 'healthy soil', 'resistant varieties'],
                    'organic_control': ['neem oil', 'beneficial bacteria', 'companion planting', 'physical barriers']
                }
            }
        }
        
        self.question_patterns = {
            r'\b(hello|hi|hey|greetings|good morning|good afternoon)\b': 'greeting',
            r'\b(ph|acidity|alkaline|acidic)\b': 'ph_question', 
            r'\b(nitrogen|yellow.*leaves?)\b': 'nitrogen_question',
            r'\b(phosphorus|phosphate|purple.*leaves?)\b': 'phosphorus_question',
            r'\b(potassium|potash|brown.*edges?)\b': 'potassium_question',
            r'\b(fertilizer|fertiliser|nutrient|feed)\b': 'fertilizer_question',
            r'\b(crop|what.*grow|which.*crop|what.*plant)\b': 'crop_question',
            r'\b(season|seasonal|when.*plant|timing)\b': 'seasonal_question',
            r'\b(weather|rain|drought|irrigation|water)\b': 'weather_question',
            r'\b(help|assist|what.*can.*do)\b': 'help_question',
            r'\b(soil.*test|test.*soil|analyze|analysis|interpret)\b': 'soil_analysis_question',
            r'\b(problem|disease|pest|issue|wrong|sick)\b': 'problem_solving',
            r'\b(spacing|distance|how.*far|plant.*apart)\b': 'spacing_question',
            r'\b(harvest|when.*harvest|ready|pick)\b': 'harvest_question'
        }

    def generate_response(self, message, user_id=None, context_data=None):
        """Generate intelligent response based on message and context"""
        message_lower = message.lower().strip()
        
        # Determine message type
        message_type = self._classify_message(message_lower)
        
        # Get user's soil data for personalized responses
        user_soil_data = None
        if user_id:
            try:
                user = User.query.get(user_id)
                if user:
                    user_soil_data = SoilData.query.filter_by(user_id=user_id).order_by(SoilData.created_at.desc()).first()
            except Exception as e:
                print(f"Error fetching user data: {e}")
        
        # Generate response based on message type and context
        response = self._generate_contextualized_response(message_type, message, user_soil_data, context_data)
        
        return {
            'response': response,
            'message_type': message_type,
            'suggestions': self._generate_suggestions(message_type, user_soil_data)
        }
    
    def _classify_message(self, message):
        """Classify message type based on patterns with priority"""
        # Order patterns by specificity (most specific first)
        priority_patterns = [
            (r'\b(spacing|distance|how.*far|plant.*apart)\b', 'spacing_question'),
            (r'\b(harvest|when.*harvest|ready|pick)\b', 'harvest_question'),
            (r'\b(yellow.*leaves?)\b', 'nitrogen_question'),
            (r'\b(purple.*leaves?)\b', 'phosphorus_question'), 
            (r'\b(brown.*edges?)\b', 'potassium_question'),
            (r'\b(soil.*test|test.*soil|analyze|analysis|interpret)\b', 'soil_analysis_question'),
            (r'\b(what.*grow|which.*crop|what.*plant)\b', 'crop_question'),
            (r'\b(when.*plant|timing)\b', 'seasonal_question'),
            (r'\b(problem|disease|pest|issue|wrong|sick)\b', 'problem_solving'),
            (r'\b(nitrogen)\b', 'nitrogen_question'),
            (r'\b(phosphorus|phosphate)\b', 'phosphorus_question'),
            (r'\b(potassium|potash)\b', 'potassium_question'),
            (r'\b(ph|acidity|alkaline|acidic)\b', 'ph_question'),
            (r'\b(fertilizer|fertiliser|nutrient|feed)\b', 'fertilizer_question'),
            (r'\b(crop)\b', 'crop_question'),
            (r'\b(season|seasonal)\b', 'seasonal_question'),
            (r'\b(weather|rain|drought|irrigation|water)\b', 'weather_question'),
            (r'\b(help|assist|what.*can.*do)\b', 'help_question'),
            (r'\b(hello|hi|hey|greetings|good morning|good afternoon)\b', 'greeting')
        ]
        
        # Check patterns in priority order
        for pattern, msg_type in priority_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return msg_type
        return 'general'
    
    def _generate_contextualized_response(self, message_type, original_message, soil_data, context_data):
        """Generate response with user context and soil data"""
        
        if message_type == 'greeting':
            greeting = random.choice(self.knowledge_base['greetings'])
            if soil_data:
                greeting += f"\n\nI see you have soil data available (pH: {soil_data.ph}, Fertility: {soil_data.fertility_level or 'Not analyzed'}). I can help interpret your results!"
            return greeting
        
        elif message_type == 'ph_question':
            return self._get_ph_analysis(soil_data, original_message)
        
        elif message_type == 'nitrogen_question':
            return self._get_nutrient_analysis('nitrogen', soil_data, original_message)
        
        elif message_type == 'phosphorus_question':
            return self._get_nutrient_analysis('phosphorus', soil_data, original_message)
        
        elif message_type == 'potassium_question':
            return self._get_nutrient_analysis('potassium', soil_data, original_message)
        
        elif message_type == 'fertilizer_question':
            return self._get_smart_fertilizer_recommendation(soil_data, original_message)
        
        elif message_type == 'crop_question':
            return self._get_intelligent_crop_recommendations(soil_data, original_message)
        
        elif message_type == 'seasonal_question':
            return self._get_seasonal_advice(original_message)
        
        elif message_type == 'weather_question':
            return self._get_weather_advice(original_message)
        
        elif message_type == 'help_question':
            return self._get_comprehensive_help()
        
        elif message_type == 'soil_analysis_question':
            return self._get_soil_analysis_interpretation(soil_data)
        
        elif message_type == 'problem_solving':
            return self._get_problem_solving_advice(original_message, soil_data)
        
        elif message_type == 'spacing_question':
            return self._get_spacing_advice(original_message)
        
        elif message_type == 'harvest_question':
            return self._get_harvest_advice(original_message)
        
        else:
            return self._get_intelligent_general_response(original_message, soil_data)

    def _get_ph_analysis(self, soil_data, message):
        """Provide detailed pH analysis"""
        if soil_data and soil_data.ph:
            ph_value = soil_data.ph
            
            # Determine pH category
            ph_category = None
            for category, (min_ph, max_ph, description) in self.knowledge_base['soil_analysis']['ph_ranges'].items():
                if min_ph <= ph_value < max_ph:
                    ph_category = category
                    ph_description = description
                    break
            
            response = f"🧪 **Your Soil pH Analysis:**\n\n"
            response += f"**pH Level:** {ph_value} ({ph_category.replace('_', ' ').title()})\n\n"
            response += f"**Analysis:** {ph_description}\n\n"
            
            # Add specific recommendations
            if ph_value < 6.0:
                response += "**Recommendations:**\n• Apply agricultural lime (2-4 lbs per 100 sq ft)\n• Add wood ash in small amounts\n• Consider dolomitic lime for magnesium boost\n• Test again in 6 months"
            elif ph_value > 7.5:
                response += "**Recommendations:**\n• Apply elemental sulfur (1-2 lbs per 100 sq ft)\n• Add organic matter like peat moss\n• Use acidifying fertilizers\n• Improve soil drainage"
            else:
                response += "**Great news!** Your pH is in the optimal range for most crops. Maintain with regular organic matter additions."
                
            return response
        else:
            return "I'd love to analyze your soil pH! 🧪 Please run a soil test first. The optimal pH range for most crops is 6.0-7.5. Would you like to know how to test your soil pH or learn about pH adjustment methods?"

    def _get_nutrient_analysis(self, nutrient, soil_data, message):
        """Provide detailed nutrient analysis"""
        if not soil_data:
            thresholds = self.knowledge_base['soil_analysis']['nutrient_thresholds'][nutrient]
            return f"I'd love to analyze your {nutrient} levels! 📊 Please run a soil test first. {nutrient.title()} deficiency signs include: {thresholds['deficiency_symptoms']}. Would you like tips on soil testing?"
        
        # Get nutrient value
        nutrient_value = getattr(soil_data, nutrient, None)
        if nutrient_value is None:
            return f"I don't see {nutrient} data in your soil test. Please ensure your soil analysis includes {nutrient} levels for accurate recommendations."
        
        thresholds = self.knowledge_base['soil_analysis']['nutrient_thresholds'][nutrient]
        unit = thresholds['unit']
        
        # Determine nutrient status
        if nutrient_value < thresholds['low']:
            status = 'Low'
            recommendation = self._get_nutrient_deficiency_solution(nutrient, nutrient_value)
        elif nutrient_value < thresholds['optimal']:
            status = 'Adequate'
            recommendation = f"Your {nutrient} levels are adequate but could be improved. Consider light fertilization."
        else:
            status = 'High'
            recommendation = f"Excellent {nutrient} levels! Focus on maintaining balance with other nutrients."
        
        response = f"🌱 **{nutrient.title()} Analysis:**\n\n"
        response += f"**Level:** {nutrient_value} {unit} ({status})\n"
        response += f"**Optimal Range:** {thresholds['low']}-{thresholds['optimal']} {unit}\n\n"
        response += f"**Recommendation:** {recommendation}\n\n"
        response += f"**Deficiency Signs:** {thresholds['deficiency_symptoms']}"
        
        return response

    def _get_nutrient_deficiency_solution(self, nutrient, current_value):
        """Get specific solutions for nutrient deficiencies"""
        fertilizers = self.knowledge_base['fertilizer_guide'][f'{nutrient}_sources']
        
        solutions = []
        for fertilizer, details in fertilizers.items():
            if nutrient == 'nitrogen' and current_value < 50:
                if fertilizer in ['Urea', 'Calcium Nitrate']:
                    solutions.append(f"• {fertilizer}: Apply 1-2 lbs per 1000 sq ft ({details['best_for']})")
            elif nutrient == 'phosphorus' and current_value < 10:
                if fertilizer in ['DAP', 'Superphosphate']:
                    solutions.append(f"• {fertilizer}: Apply as directed ({details['best_for']})")
            elif nutrient == 'potassium' and current_value < 75:
                solutions.append(f"• {fertilizer}: {details['best_for']}")
        
        return "Apply one of these options:\n" + "\n".join(solutions[:3])

    def _get_smart_fertilizer_recommendation(self, soil_data, message):
        """Provide intelligent fertilizer recommendations"""
        if not soil_data:
            return "🧪 For personalized fertilizer recommendations, I need your soil test results! Here are general guidelines:\n\n**Spring:** Balanced fertilizer (10-10-10)\n**Growing Season:** Higher nitrogen for leafy crops\n**Fall:** Low nitrogen, higher phosphorus/potassium\n\nWould you like to run a soil test first?"
        
        # Use ML model for recommendations if available
        try:
            soil_params = {
                'ph': soil_data.ph,
                'nitrogen': soil_data.nitrogen,
                'phosphorus': soil_data.phosphorus,
                'potassium': soil_data.potassium,
                'organic_matter': soil_data.organic_carbon,
                'moisture': soil_data.moisture or 25
            }
            
            ml_prediction = enhanced_predictor.predict_fertility(soil_params)
            fertilizer_recs = ml_prediction.get('fertilizer_recommendations', [])
            
            response = "🌟 **Personalized Fertilizer Recommendations:**\n\n"
            response += f"**Soil Fertility:** {ml_prediction.get('fertility_level', 'Unknown')} ({ml_prediction.get('fertility_score', 0)}/100)\n\n"
            
            if fertilizer_recs:
                response += "**Recommended Fertilizers:**\n"
                for i, fertilizer in enumerate(fertilizer_recs[:4], 1):
                    response += f"{i}. {fertilizer}\n"
            
            response += f"\n**Application Timing:**\n• Spring: Apply before planting\n• Split applications for better uptake\n• Water in thoroughly after application"
            
            return response
            
        except Exception as e:
            print(f"Error getting ML recommendations: {e}")
            return self._get_basic_fertilizer_recommendation(soil_data)

    def _get_basic_fertilizer_recommendation(self, soil_data):
        """Fallback fertilizer recommendation"""
        recommendations = []
        
        if soil_data.nitrogen < 100:
            recommendations.append("Nitrogen-rich fertilizer (Urea or Blood Meal)")
        if soil_data.phosphorus < 15:
            recommendations.append("Phosphorus supplement (Bone Meal or Superphosphate)")
        if soil_data.potassium < 100:
            recommendations.append("Potassium source (Muriate of Potash or Wood Ash)")
        
        if not recommendations:
            return "🎉 Your soil nutrient levels look good! Maintain with:\n• Balanced fertilizer (10-10-10) in spring\n• Compost annually\n• Regular soil testing"
        
        return f"Based on your soil test, apply:\n• " + "\n• ".join(recommendations) + "\n\nRetest soil in 3-6 months to monitor improvement."

    def _get_intelligent_crop_recommendations(self, soil_data, message):
        """Provide intelligent crop recommendations"""
        if not soil_data:
            return "🌱 I'd love to recommend crops for your specific soil! Please run a soil test first. In general:\n\n**High Fertility Soil:** Tomatoes, Corn, Peppers\n**Medium Fertility:** Carrots, Beans, Onions\n**Low Fertility:** Herbs, Radishes, Cover Crops\n\nWhat type of crops interest you most?"
        
        try:
            # Get ML-based crop recommendations
            soil_params = {
                'ph': soil_data.ph,
                'nitrogen': soil_data.nitrogen,
                'phosphorus': soil_data.phosphorus,
                'potassium': soil_data.potassium,
                'organic_matter': soil_data.organic_carbon,
                'moisture': soil_data.moisture or 25
            }
            
            ml_prediction = enhanced_predictor.predict_fertility(soil_params)
            crop_recs = ml_prediction.get('crop_recommendations', [])
            
            response = f"🌾 **Personalized Crop Recommendations for Your Soil:**\n\n"
            response += f"**Soil pH:** {soil_data.ph} | **Fertility:** {ml_prediction.get('fertility_level', 'Unknown')}\n\n"
            
            if crop_recs:
                response += "**Recommended Crops:**\n"
                for i, crop in enumerate(crop_recs[:6], 1):
                    crop_info = self._get_crop_info(crop)
                    response += f"{i}. **{crop}** - {crop_info}\n"
            
            # Add seasonal advice
            current_season = self._get_current_season()
            seasonal_crops = self.knowledge_base['seasonal_guide'][current_season]['crops']
            response += f"\n**Current Season ({current_season.title()}) Suggestions:**\n"
            response += f"Perfect time for: {', '.join(seasonal_crops[:4])}"
            
            return response
            
        except Exception as e:
            print(f"Error getting crop recommendations: {e}")
            return self._get_basic_crop_recommendations(soil_data)

    def _get_crop_info(self, crop_name):
        """Get crop information from database"""
        # Search in all crop categories
        for category in self.knowledge_base['crop_database'].values():
            if crop_name in category:
                info = category[crop_name]
                ph_range = info['ph_range']
                return f"pH {ph_range[0]}-{ph_range[1]}, {info['fertility_need']} fertility, {info['season']} season"
        return "Good choice for your soil conditions"

    def _get_seasonal_advice(self, message):
        """Provide seasonal farming advice"""
        current_season = self._get_current_season()
        season_info = self.knowledge_base['seasonal_guide'][current_season]
        
        response = f"🍂 **{current_season.title()} Farming Guide:**\n\n"
        response += f"**Key Tasks:** {', '.join(season_info['tasks'])}\n\n"
        response += f"**Recommended Crops:** {', '.join(season_info['crops'])}\n\n"
        response += f"**Expert Tip:** {season_info['tips']}"
        
        return response

    def _get_current_season(self):
        """Determine current season"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        else:
            return 'winter'

    def _get_comprehensive_help(self):
        """Provide comprehensive help information"""
        return """🤖 **Terra Bot Help Center**

I'm your AI agricultural assistant! Here's how I can help:

**🧪 Soil Analysis**
• Interpret pH levels and nutrient content
• Explain soil test results
• Recommend soil improvements

**🌱 Crop Guidance** 
• Suggest crops for your soil type
• Provide planting and spacing advice
• Seasonal crop recommendations

**💡 Fertilizer Advice**
• Personalized fertilizer recommendations
• Application timing and rates
• Organic vs synthetic options

**🌾 Farming Tips**
• Seasonal farming calendar
• Problem-solving for plant issues
• Weather and irrigation advice

**🎯 How to Ask Questions:**
• "What's my soil pH status?"
• "What crops can I grow?"
• "How to fix nitrogen deficiency?"
• "When should I plant tomatoes?"

Just ask me anything about farming, and I'll provide personalized advice based on your soil data!"""

    def _get_intelligent_general_response(self, message, soil_data):
        """Generate intelligent general responses"""
        
        # Look for specific keywords and provide targeted responses
        keywords = {
            'plant': "I can help you choose the right plants for your soil! What type of crops interest you?",
            'grow': "Growing success starts with healthy soil! What would you like to grow?",
            'test': "Soil testing is crucial for good farming! I can help interpret your results.",
            'improve': "There are many ways to improve soil health! What specific aspect concerns you?",
            'organic': "Organic farming is great! I can suggest organic fertilizers and practices.",
            'water': "Proper irrigation is key to success! What's your watering situation?",
            'disease': "Plant diseases can be tricky. What symptoms are you seeing?",
            'yield': "Want to increase yields? It starts with soil health and proper nutrition!"
        }
        
        for keyword, response in keywords.items():
            if keyword in message.lower():
                if soil_data:
                    response += f" Based on your soil data (pH: {soil_data.ph}), I can give specific advice!"
                return response
        
        # Default intelligent response
        responses = [
            "That's a great farming question! Can you provide more details so I can give you the best advice?",
            "I'd love to help with that! Could you be more specific about your farming situation?",
            "Interesting question! What specific aspect of farming or soil health would you like to focus on?",
        ]
        
        if soil_data:
            responses.append(f"I see you have soil data available. How can I help you make the most of your soil conditions?")
        
        return random.choice(responses)

    def _generate_suggestions(self, message_type, soil_data):
        """Generate intelligent follow-up suggestions"""
        base_suggestions = [
            "What crops should I plant for my soil?",
            "How can I improve my soil fertility?",
            "When is the best time to apply fertilizer?",
            "What's causing my plant problems?"
        ]
        
        if soil_data:
            personalized_suggestions = [
                f"Explain my pH level of {soil_data.ph}",
                f"Best crops for my {soil_data.fertility_level or 'current'} fertility soil",
                "How to improve my soil nutrients?",
                "Seasonal advice for my area"
            ]
            return random.sample(personalized_suggestions + base_suggestions, 3)
        
        return random.sample(base_suggestions, 3)

    def generate_session_title(self, first_message):
        """Generate descriptive titles for chat sessions"""
        message_lower = first_message.lower()
        
        title_keywords = {
            'ph': "Soil pH Analysis",
            'nitrogen': "Nitrogen Management",
            'phosphorus': "Phosphorus Discussion", 
            'potassium': "Potassium Guidance",
            'crop': "Crop Selection Help",
            'plant': "Planting Advice",
            'fertilizer': "Fertilizer Consultation",
            'season': "Seasonal Planning",
            'problem': "Problem Solving",
            'disease': "Plant Health Issues",
            'organic': "Organic Farming Chat",
            'yield': "Yield Improvement Tips"
        }
        
        for keyword, title in title_keywords.items():
            if keyword in message_lower:
                return title
        
        return f"Farm Chat - {datetime.now().strftime('%b %d')}"

    def _get_weather_advice(self, message):
        """Provide weather and irrigation advice"""
        advice = [
            "🌧️ **Weather & Irrigation Tips:**\n\n",
            "• Check weather forecasts before fertilizing - rain can wash away nutrients\n",
            "• Avoid working wet soil to prevent compaction\n",
            "• During drought: Focus on mulching and efficient irrigation\n",
            "• Cold weather slows nutrient uptake - adjust fertilization timing\n",
            "• Water deeply but less frequently to encourage deep roots\n",
            "• Morning watering reduces disease risk"
        ]
        return "".join(advice)

    def _get_soil_analysis_interpretation(self, soil_data):
        """Provide comprehensive soil analysis interpretation"""
        if not soil_data:
            return "I'd love to interpret your soil analysis! 📊 Please run a soil test first, then I can explain what all the numbers mean and provide specific recommendations."
        
        response = "🔍 **Complete Soil Analysis Interpretation:**\n\n"
        
        # pH Analysis
        ph_status = "Optimal" if 6.0 <= soil_data.ph <= 7.5 else ("Acidic" if soil_data.ph < 6.0 else "Alkaline")
        response += f"**pH:** {soil_data.ph} ({ph_status})\n"
        
        # Nutrient Analysis
        nutrients = {
            'Nitrogen': soil_data.nitrogen,
            'Phosphorus': soil_data.phosphorus,
            'Potassium': soil_data.potassium
        }
        
        response += "\n**Nutrient Levels:**\n"
        for nutrient, value in nutrients.items():
            thresholds = self.knowledge_base['soil_analysis']['nutrient_thresholds'][nutrient.lower()]
            if value < thresholds['low']:
                status = "Low ⚠️"
            elif value < thresholds['optimal']:
                status = "Adequate ✓"
            else:
                status = "High ✅"
            response += f"• {nutrient}: {value} mg/kg ({status})\n"
        
        # Fertility Summary
        if soil_data.fertility_level:
            response += f"\n**Overall Fertility:** {soil_data.fertility_level}"
            if soil_data.fertility_score:
                response += f" ({soil_data.fertility_score}/100)"
        
        return response

    def _get_problem_solving_advice(self, message, soil_data):
        """Provide problem-solving advice for plant issues"""
        problem_keywords = {
            'yellow': 'yellowing_leaves',
            'growth': 'poor_growth', 
            'pest': 'pest_problems',
            'slow': 'poor_growth',
            'disease': 'pest_problems'
        }
        
        detected_problem = None
        for keyword, problem in problem_keywords.items():
            if keyword in message.lower():
                detected_problem = problem
                break
        
        if detected_problem and detected_problem in self.knowledge_base['problem_solving']:
            problem_info = self.knowledge_base['problem_solving'][detected_problem]
            response = f"🩺 **Problem Diagnosis: {detected_problem.replace('_', ' ').title()}**\n\n"
            
            if 'causes' in problem_info:
                response += f"**Possible Causes:** {', '.join(problem_info['causes'])}\n\n"
            
            if 'solutions' in problem_info:
                response += f"**Solutions:** {', '.join(problem_info['solutions'])}\n\n"
            
            if soil_data:
                response += f"**Based on your soil (pH: {soil_data.ph}):** "
                if soil_data.nitrogen < 80 and 'yellow' in message.lower():
                    response += "Low nitrogen likely causing yellowing. Apply nitrogen fertilizer."
                else:
                    response += "Check the causes above against your soil conditions."
            
            return response
        
        return "🔍 I can help diagnose plant problems! Can you describe the symptoms you're seeing? (e.g., yellowing leaves, slow growth, pest damage)"

    def _get_spacing_advice(self, message):
        """Provide plant spacing advice"""
        spacing_guide = {
            'tomato': '18-24 inches apart',
            'lettuce': '6-8 inches apart', 
            'carrot': '2-3 inches apart',
            'pepper': '12-18 inches apart',
            'onion': '4-6 inches apart',
            'potato': '12-15 inches apart',
            'cabbage': '12-18 inches apart'
        }
        
        found_crop = None
        for crop in spacing_guide:
            if crop in message.lower():
                found_crop = crop
                break
        
        if found_crop:
            return f"🌱 **{found_crop.title()} Spacing:** {spacing_guide[found_crop]}\n\nProper spacing ensures good air circulation, reduces disease, and allows optimal growth!"
        
        return "🌱 **General Spacing Guidelines:**\n\n• Small plants (lettuce, spinach): 4-6 inches\n• Medium plants (carrots, onions): 6-12 inches\n• Large plants (tomatoes, peppers): 18-24 inches\n• Very large plants (corn, squash): 24-36 inches\n\nWhat specific crop spacing do you need help with?"

    def _get_harvest_advice(self, message):
        """Provide harvest timing advice"""
        harvest_guide = {
            'tomato': 'When fruits are fully colored but still firm',
            'lettuce': 'Cut outer leaves when 4-6 inches long',
            'carrot': 'When shoulders are 3/4 inch diameter',
            'pepper': 'When fruits reach full size and color',
            'potato': '2-3 weeks after flowers appear',
            'onion': 'When tops begin to yellow and fall over'
        }
        
        found_crop = None
        for crop in harvest_guide:
            if crop in message.lower():
                found_crop = crop
                break
        
        if found_crop:
            return f"🚜 **{found_crop.title()} Harvest Guide:**\n\n{harvest_guide[found_crop]}\n\n**Best Time:** Early morning when plants are crisp and full of moisture."
        
        return "🚜 **General Harvest Tips:**\n\n• Harvest in early morning for best quality\n• Use clean, sharp tools\n• Handle gently to avoid bruising\n• Harvest regularly to encourage production\n\nWhat specific crop harvest timing do you need help with?"

    def _get_basic_crop_recommendations(self, soil_data):
        """Fallback crop recommendations"""
        if not soil_data:
            return "Please run a soil test for personalized crop recommendations!"
        
        ph = soil_data.ph
        fertility = soil_data.fertility_level or 'medium'
        
        recommendations = []
        
        if ph < 6.0:
            recommendations.extend(['Blueberries', 'Potatoes', 'Sweet Potatoes'])
        elif ph > 7.5:
            recommendations.extend(['Asparagus', 'Cabbage', 'Spinach'])
        else:
            recommendations.extend(['Tomatoes', 'Lettuce', 'Carrots'])
        
        if fertility.lower() == 'high':
            recommendations.extend(['Corn', 'Peppers'])
        elif fertility.lower() == 'low':
            recommendations.extend(['Herbs', 'Radishes'])
        
        return f"Based on your soil conditions: {', '.join(set(recommendations[:5]))}"

# Create global instance
improved_chatbot = ImprovedAgriChatbot()
