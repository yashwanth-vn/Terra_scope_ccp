import requests
import os
from typing import Dict, Optional

def get_weather_data(location: str) -> Dict:
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        location: City name or coordinates
        
    Returns:
        Dictionary containing weather information
    """
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            print("OpenWeatherMap API key not found in environment variables")
            return get_default_weather_data()
        
        # OpenWeatherMap API endpoint for current weather
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Parameters for API request
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'  # Get temperature in Celsius
        }
        
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant weather information
        weather_info = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'location': data['name'],
            'country': data['sys']['country'],
            'rainfall': data.get('rain', {}).get('1h', 0),  # Rain in last hour (mm)
            'wind_speed': data['wind']['speed'],
            'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
            'uv_index': None  # Would need UV index API call for this
        }
        
        # Add estimated monthly rainfall (simplified calculation)
        weather_info['monthly_rainfall'] = estimate_monthly_rainfall(
            weather_info['rainfall'], 
            weather_info['humidity']
        )
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return get_default_weather_data()
    
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        return get_default_weather_data()
    
    except Exception as e:
        print(f"Unexpected error in weather data fetch: {e}")
        return get_default_weather_data()

def get_historical_weather(location: str, days: int = 30) -> Dict:
    """
    Get historical weather data for better soil analysis
    Note: This would require a paid API plan for historical data
    """
    # For now, return simulated historical data
    return {
        'avg_temperature': 25.0,
        'total_rainfall': 150.0,
        'avg_humidity': 65.0,
        'rainfall_days': 12
    }

def estimate_monthly_rainfall(current_rainfall: float, humidity: float) -> float:
    """
    Estimate monthly rainfall based on current conditions
    This is a simplified estimation - in production, you'd use historical data
    """
    # Base estimation from humidity
    base_rainfall = (humidity - 30) * 2.5  # Rough correlation
    
    # Adjust based on current rainfall
    if current_rainfall > 0:
        base_rainfall = max(base_rainfall, current_rainfall * 24 * 15)  # Scale up
    
    # Keep within reasonable bounds
    return max(0, min(base_rainfall, 500))

def get_default_weather_data() -> Dict:
    """
    Return default weather data when API is unavailable
    """
    return {
        'temperature': 25.0,
        'humidity': 60,
        'pressure': 1013,
        'description': 'moderate conditions',
        'location': 'Unknown',
        'country': 'Unknown',
        'rainfall': 0,
        'monthly_rainfall': 100,
        'wind_speed': 5.0,
        'visibility': 10.0,
        'uv_index': None
    }

def assess_weather_impact_on_soil(weather_data: Dict, soil_params: Dict) -> Dict:
    """
    Assess how weather conditions might impact soil fertility
    """
    impact_assessment = {
        'temperature_impact': 'neutral',
        'rainfall_impact': 'neutral',
        'humidity_impact': 'neutral',
        'overall_impact': 'neutral',
        'recommendations': []
    }
    
    try:
        temp = weather_data.get('temperature', 25)
        rainfall = weather_data.get('monthly_rainfall', 100)
        humidity = weather_data.get('humidity', 60)
        
        # Temperature impact assessment
        if temp < 10:
            impact_assessment['temperature_impact'] = 'negative'
            impact_assessment['recommendations'].append(
                "Low temperatures may slow nutrient availability. Consider soil warming techniques."
            )
        elif temp > 35:
            impact_assessment['temperature_impact'] = 'negative'
            impact_assessment['recommendations'].append(
                "High temperatures may accelerate nutrient loss. Ensure adequate irrigation."
            )
        else:
            impact_assessment['temperature_impact'] = 'positive'
        
        # Rainfall impact assessment
        if rainfall < 50:
            impact_assessment['rainfall_impact'] = 'negative'
            impact_assessment['recommendations'].append(
                "Low rainfall may require additional irrigation for optimal nutrient uptake."
            )
        elif rainfall > 300:
            impact_assessment['rainfall_impact'] = 'negative'
            impact_assessment['recommendations'].append(
                "Excessive rainfall may cause nutrient leaching. Consider drainage improvements."
            )
        else:
            impact_assessment['rainfall_impact'] = 'positive'
        
        # Humidity impact
        if humidity > 80:
            impact_assessment['humidity_impact'] = 'mixed'
            impact_assessment['recommendations'].append(
                "High humidity may increase disease risk but helps maintain soil moisture."
            )
        elif humidity < 40:
            impact_assessment['humidity_impact'] = 'negative'
            impact_assessment['recommendations'].append(
                "Low humidity may increase water stress. Monitor soil moisture closely."
            )
        
        # Overall impact
        impacts = [
            impact_assessment['temperature_impact'],
            impact_assessment['rainfall_impact'],
            impact_assessment['humidity_impact']
        ]
        
        positive_count = impacts.count('positive')
        negative_count = impacts.count('negative')
        
        if positive_count > negative_count:
            impact_assessment['overall_impact'] = 'positive'
        elif negative_count > positive_count:
            impact_assessment['overall_impact'] = 'negative'
        else:
            impact_assessment['overall_impact'] = 'neutral'
        
        return impact_assessment
        
    except Exception as e:
        print(f"Error in weather impact assessment: {e}")
        return impact_assessment

def get_seasonal_adjustments(season: str) -> Dict:
    """
    Get seasonal adjustments for soil fertility predictions
    """
    seasonal_factors = {
        'spring': {
            'temperature_adjustment': 0.1,
            'moisture_adjustment': 0.15,
            'nutrient_uptake_factor': 1.2,
            'recommendations': [
                "Spring is ideal for planting. Soil nutrients are becoming more available.",
                "Consider adding organic matter to prepare for the growing season."
            ]
        },
        'summer': {
            'temperature_adjustment': 0.0,
            'moisture_adjustment': -0.1,
            'nutrient_uptake_factor': 1.0,
            'recommendations': [
                "Monitor soil moisture during hot weather.",
                "Higher temperatures increase nutrient availability but also loss."
            ]
        },
        'autumn': {
            'temperature_adjustment': -0.05,
            'moisture_adjustment': 0.1,
            'nutrient_uptake_factor': 0.9,
            'recommendations': [
                "Good time for soil testing and amendments.",
                "Prepare soil for winter by adding organic matter."
            ]
        },
        'winter': {
            'temperature_adjustment': -0.15,
            'moisture_adjustment': 0.05,
            'nutrient_uptake_factor': 0.7,
            'recommendations': [
                "Soil activity is reduced in winter.",
                "Plan soil improvements for the next growing season."
            ]
        }
    }
    
    return seasonal_factors.get(season.lower(), seasonal_factors['spring'])
