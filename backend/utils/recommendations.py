from typing import Dict, List

def get_fertilizer_recommendations(soil_params: Dict, fertility_prediction: Dict) -> Dict:
    """
    Generate fertilizer recommendations based on soil parameters and fertility prediction
    """
    recommendations = {
        'primary_fertilizers': [],
        'secondary_fertilizers': [],
        'organic_amendments': [],
        'dosage_recommendations': {},
        'application_timing': [],
        'warnings': []
    }
    
    try:
        ph = soil_params.get('ph', 6.5)
        nitrogen = soil_params.get('nitrogen', 100)
        phosphorus = soil_params.get('phosphorus', 20)
        potassium = soil_params.get('potassium', 100)
        organic_carbon = soil_params.get('organic_carbon', 1.0)
        fertility_level = fertility_prediction.get('level', 'Medium')
        
        # pH corrections
        if ph < 6.0:
            recommendations['primary_fertilizers'].append({
                'name': 'Lime (Calcium Carbonate)',
                'purpose': 'Increase soil pH',
                'application_rate': f"{2-4} kg per 100 sq meters",
                'priority': 'high'
            })
            recommendations['warnings'].append("Acidic soil detected. Apply lime before other fertilizers.")
        
        elif ph > 7.5:
            recommendations['secondary_fertilizers'].append({
                'name': 'Sulfur',
                'purpose': 'Lower soil pH',
                'application_rate': f"{1-2} kg per 100 sq meters",
                'priority': 'medium'
            })
            recommendations['warnings'].append("Alkaline soil detected. Consider sulfur application.")
        
        # Nitrogen recommendations
        if nitrogen < 80:
            recommendations['primary_fertilizers'].append({
                'name': 'Urea (46-0-0)',
                'purpose': 'Increase nitrogen content',
                'application_rate': f"{15-25} kg per hectare",
                'priority': 'high'
            })
            recommendations['organic_amendments'].append({
                'name': 'Compost or Well-rotted Manure',
                'purpose': 'Slow-release nitrogen and organic matter',
                'application_rate': f"{2-3} tons per hectare",
                'priority': 'medium'
            })
        elif nitrogen > 200:
            recommendations['warnings'].append("High nitrogen levels detected. Reduce nitrogen fertilization.")
        
        # Phosphorus recommendations
        if phosphorus < 15:
            recommendations['primary_fertilizers'].append({
                'name': 'Single Super Phosphate (0-16-0)',
                'purpose': 'Increase phosphorus availability',
                'application_rate': f"{10-15} kg per hectare",
                'priority': 'high'
            })
            recommendations['organic_amendments'].append({
                'name': 'Bone Meal',
                'purpose': 'Organic phosphorus source',
                'application_rate': f"{5-8} kg per 100 sq meters",
                'priority': 'medium'
            })
        elif phosphorus > 40:
            recommendations['warnings'].append("High phosphorus levels. Avoid phosphorus-rich fertilizers.")
        
        # Potassium recommendations
        if potassium < 100:
            recommendations['primary_fertilizers'].append({
                'name': 'Muriate of Potash (0-0-60)',
                'purpose': 'Increase potassium content',
                'application_rate': f"{8-12} kg per hectare",
                'priority': 'high'
            })
            recommendations['organic_amendments'].append({
                'name': 'Wood Ash',
                'purpose': 'Natural potassium source',
                'application_rate': f"{2-4} kg per 100 sq meters",
                'priority': 'low'
            })
        elif potassium > 250:
            recommendations['warnings'].append("High potassium levels detected. Reduce potash application.")
        
        # Organic carbon recommendations
        if organic_carbon < 1.0:
            recommendations['organic_amendments'].extend([
                {
                    'name': 'Compost',
                    'purpose': 'Improve soil structure and organic matter',
                    'application_rate': f"{3-5} tons per hectare",
                    'priority': 'high'
                },
                {
                    'name': 'Green Manure Cover Crops',
                    'purpose': 'Add organic matter naturally',
                    'application_rate': "Plant during off-season",
                    'priority': 'medium'
                }
            ])
        
        # Complex fertilizer recommendations based on overall fertility
        if fertility_level == 'Low':
            recommendations['primary_fertilizers'].append({
                'name': 'NPK Complex (20-20-20)',
                'purpose': 'Balanced nutrition for low fertility soil',
                'application_rate': f"{20-30} kg per hectare",
                'priority': 'high'
            })
        elif fertility_level == 'Medium':
            recommendations['primary_fertilizers'].append({
                'name': 'NPK Complex (15-15-15)',
                'purpose': 'Maintenance fertilization',
                'application_rate': f"{15-20} kg per hectare",
                'priority': 'medium'
            })
        
        # Application timing recommendations
        recommendations['application_timing'] = [
            "Apply lime 2-3 weeks before other fertilizers if pH correction is needed",
            "Apply phosphorus fertilizers at planting time for better root establishment",
            "Split nitrogen application: 1/3 at planting, 1/3 at vegetative growth, 1/3 at flowering",
            "Apply potassium fertilizers during soil preparation",
            "Add organic amendments during off-season for better decomposition"
        ]
        
        # Calculate total dosage recommendations
        recommendations['dosage_recommendations'] = calculate_dosage_summary(recommendations)
        
        return recommendations
        
    except Exception as e:
        print(f"Error generating fertilizer recommendations: {e}")
        return get_default_fertilizer_recommendations()

def get_crop_suggestions(soil_params: Dict, season: str) -> Dict:
    """
    Suggest suitable crops based on soil parameters and season
    """
    suggestions = {
        'highly_suitable': [],
        'moderately_suitable': [],
        'not_recommended': [],
        'season_specific': [],
        'soil_improvement_crops': []
    }
    
    try:
        ph = soil_params.get('ph', 6.5)
        nitrogen = soil_params.get('nitrogen', 100)
        phosphorus = soil_params.get('phosphorus', 20)
        potassium = soil_params.get('potassium', 100)
        organic_carbon = soil_params.get('organic_carbon', 1.0)
        season = season.lower() if season else 'spring'
        
        # Define crop database with requirements
        crop_database = {
            'rice': {
                'ph_range': (5.5, 7.0),
                'nitrogen_min': 80,
                'phosphorus_min': 15,
                'potassium_min': 80,
                'seasons': ['spring', 'summer'],
                'type': 'cereal'
            },
            'wheat': {
                'ph_range': (6.0, 7.5),
                'nitrogen_min': 100,
                'phosphorus_min': 20,
                'potassium_min': 100,
                'seasons': ['autumn', 'winter', 'spring'],
                'type': 'cereal'
            },
            'corn': {
                'ph_range': (6.0, 7.0),
                'nitrogen_min': 120,
                'phosphorus_min': 25,
                'potassium_min': 120,
                'seasons': ['spring', 'summer'],
                'type': 'cereal'
            },
            'tomato': {
                'ph_range': (6.0, 7.0),
                'nitrogen_min': 100,
                'phosphorus_min': 30,
                'potassium_min': 150,
                'seasons': ['spring', 'summer'],
                'type': 'vegetable'
            },
            'potato': {
                'ph_range': (5.0, 6.5),
                'nitrogen_min': 80,
                'phosphorus_min': 20,
                'potassium_min': 200,
                'seasons': ['spring', 'autumn'],
                'type': 'tuber'
            },
            'beans': {
                'ph_range': (6.0, 7.5),
                'nitrogen_min': 40,  # Lower due to N-fixation
                'phosphorus_min': 20,
                'potassium_min': 100,
                'seasons': ['spring', 'summer'],
                'type': 'legume'
            },
            'peas': {
                'ph_range': (6.0, 7.5),
                'nitrogen_min': 30,  # Lower due to N-fixation
                'phosphorus_min': 15,
                'potassium_min': 80,
                'seasons': ['autumn', 'winter', 'spring'],
                'type': 'legume'
            },
            'carrot': {
                'ph_range': (6.0, 7.0),
                'nitrogen_min': 70,
                'phosphorus_min': 25,
                'potassium_min': 150,
                'seasons': ['spring', 'autumn'],
                'type': 'root'
            },
            'cabbage': {
                'ph_range': (6.0, 7.5),
                'nitrogen_min': 90,
                'phosphorus_min': 20,
                'potassium_min': 120,
                'seasons': ['autumn', 'winter', 'spring'],
                'type': 'leafy'
            },
            'spinach': {
                'ph_range': (6.0, 7.5),
                'nitrogen_min': 80,
                'phosphorus_min': 15,
                'potassium_min': 100,
                'seasons': ['autumn', 'winter', 'spring'],
                'type': 'leafy'
            }
        }
        
        # Evaluate each crop
        for crop_name, requirements in crop_database.items():
            suitability_score = 0
            total_factors = 4  # pH, N, P, K
            
            # pH suitability
            if requirements['ph_range'][0] <= ph <= requirements['ph_range'][1]:
                suitability_score += 1
            elif abs(ph - sum(requirements['ph_range'])/2) < 0.5:
                suitability_score += 0.5
            
            # Nutrient suitability
            if nitrogen >= requirements['nitrogen_min']:
                suitability_score += 1
            elif nitrogen >= requirements['nitrogen_min'] * 0.8:
                suitability_score += 0.5
            
            if phosphorus >= requirements['phosphorus_min']:
                suitability_score += 1
            elif phosphorus >= requirements['phosphorus_min'] * 0.8:
                suitability_score += 0.5
            
            if potassium >= requirements['potassium_min']:
                suitability_score += 1
            elif potassium >= requirements['potassium_min'] * 0.8:
                suitability_score += 0.5
            
            # Calculate suitability percentage
            suitability_percentage = (suitability_score / total_factors) * 100
            
            crop_info = {
                'name': crop_name.title(),
                'type': requirements['type'],
                'suitability_score': round(suitability_percentage, 1),
                'season_match': season in requirements['seasons']
            }
            
            # Categorize crops
            if suitability_percentage >= 80 and crop_info['season_match']:
                suggestions['highly_suitable'].append(crop_info)
            elif suitability_percentage >= 60 and crop_info['season_match']:
                suggestions['moderately_suitable'].append(crop_info)
            elif suitability_percentage >= 60 and not crop_info['season_match']:
                suggestions['season_specific'].append({
                    **crop_info,
                    'suitable_seasons': requirements['seasons']
                })
            else:
                suggestions['not_recommended'].append(crop_info)
        
        # Add soil improvement crops
        if organic_carbon < 1.5 or nitrogen < 80:
            suggestions['soil_improvement_crops'] = [
                {
                    'name': 'Clover',
                    'purpose': 'Nitrogen fixation and organic matter',
                    'type': 'cover crop'
                },
                {
                    'name': 'Alfalfa',
                    'purpose': 'Deep root system and nitrogen fixation',
                    'type': 'cover crop'
                },
                {
                    'name': 'Winter Rye',
                    'purpose': 'Prevent erosion and add organic matter',
                    'type': 'cover crop'
                }
            ]
        
        # Sort by suitability score
        suggestions['highly_suitable'].sort(key=lambda x: x['suitability_score'], reverse=True)
        suggestions['moderately_suitable'].sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return suggestions
        
    except Exception as e:
        print(f"Error generating crop suggestions: {e}")
        return get_default_crop_suggestions()

def calculate_dosage_summary(recommendations: Dict) -> Dict:
    """
    Calculate total fertilizer dosage summary
    """
    dosage_summary = {
        'nitrogen_total': '15-25 kg/ha',
        'phosphorus_total': '10-15 kg/ha',
        'potassium_total': '8-12 kg/ha',
        'organic_matter': '2-5 tons/ha',
        'lime_if_needed': '2-4 kg/100m²'
    }
    
    return dosage_summary

def get_default_fertilizer_recommendations() -> Dict:
    """
    Return default fertilizer recommendations
    """
    return {
        'primary_fertilizers': [
            {
                'name': 'NPK Complex (15-15-15)',
                'purpose': 'Balanced nutrition',
                'application_rate': '20 kg per hectare',
                'priority': 'medium'
            }
        ],
        'secondary_fertilizers': [],
        'organic_amendments': [
            {
                'name': 'Compost',
                'purpose': 'Improve soil organic matter',
                'application_rate': '3 tons per hectare',
                'priority': 'medium'
            }
        ],
        'dosage_recommendations': {
            'nitrogen_total': '15-20 kg/ha',
            'phosphorus_total': '10-15 kg/ha',
            'potassium_total': '10-15 kg/ha',
            'organic_matter': '2-3 tons/ha'
        },
        'application_timing': [
            "Apply fertilizers during soil preparation",
            "Add organic matter during off-season"
        ],
        'warnings': []
    }

def get_default_crop_suggestions() -> Dict:
    """
    Return default crop suggestions
    """
    return {
        'highly_suitable': [
            {
                'name': 'Wheat',
                'type': 'cereal',
                'suitability_score': 75.0,
                'season_match': True
            }
        ],
        'moderately_suitable': [
            {
                'name': 'Rice',
                'type': 'cereal',
                'suitability_score': 65.0,
                'season_match': True
            }
        ],
        'not_recommended': [],
        'season_specific': [],
        'soil_improvement_crops': [
            {
                'name': 'Clover',
                'purpose': 'Nitrogen fixation',
                'type': 'cover crop'
            }
        ]
    }
</function_results>

Now let me mark the ML model structure as complete and continue with creating basic React components:

<function_calls>
<invoke name="mark_todo_as_done">
<parameter name="todo_ids">["84151462-e899-4801-82b7-d73e86444f66"]
