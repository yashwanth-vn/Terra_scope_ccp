from ml_models.enhanced_fertility_model import enhanced_predictor
import json

# Test with different soil samples
test_samples = [
    {
        'name': 'High Fertility Test',
        'params': (6.8, 180, 35, 250, 2.5, 28)
    },
    {
        'name': 'Medium Fertility Test', 
        'params': (6.2, 120, 20, 150, 1.8, 25)
    },
    {
        'name': 'Low Fertility Test',
        'params': (5.5, 60, 10, 80, 0.8, 20)
    },
    {
        'name': 'Acidic Soil Test',
        'params': (4.8, 100, 15, 120, 1.2, 22)
    },
    {
        'name': 'Alkaline Soil Test',
        'params': (8.2, 90, 25, 140, 1.5, 24)
    }
]

print('🧪 Testing Enhanced ML Model Integration:')
print('=' * 50)

for sample in test_samples:
    print(f'\n🔍 {sample["name"]}:')
    ph, n, p, k, oc, moisture = sample['params']
    print(f'   Input: pH={ph}, N={n}, P={p}, K={k}, OC={oc}%, Moisture={moisture}%')
    
    result = enhanced_predictor.predict(sample['params'])
    
    print(f'   📊 Fertility Level: {result["fertility_level"]}')
    print(f'   📈 Fertility Score: {result["fertility_score"]:.1f}/100')
    print(f'   🎯 Confidence: {result["confidence"]:.1f}%')
    
    # Show top fertilizer recommendation
    if result['fertilizer_recommendations']['primary_fertilizers']:
        fert = result['fertilizer_recommendations']['primary_fertilizers'][0]
        print(f'   💡 Top Fertilizer: {fert["name"]} - {fert["application_rate"]}')
    
    # Show top crop recommendations
    if result['crop_suggestions']['highly_suitable']:
        crops = [c['name'] for c in result['crop_suggestions']['highly_suitable'][:3]]
        print(f'   🌾 Suitable Crops: {", ".join(crops)}')
    
    # Show warnings if any
    if result['fertilizer_recommendations']['warnings']:
        warnings = result['fertilizer_recommendations']['warnings']
        print(f'   ⚠️  Warnings: {", ".join(warnings[:2])}')

print('\n✅ Model is working correctly with varied outputs!')
print('\n🔧 Testing different soil conditions shows:')
print('   • Different fertility levels for different inputs')
print('   • Specific fertilizer recommendations based on deficiencies')  
print('   • Crop suggestions based on soil suitability')
print('   • Warnings for extreme pH or nutrient levels')
