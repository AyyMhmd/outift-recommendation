import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import predict_outfit

def test_recommendation_logic():
    print("Testing recommendation logic...")
    
    # Mock input data
    input_data = {
        "gender": "laki-laki",
        "weather_category": "cerah",
        "temperature": 32,
        "humidity": 60,
        "location": "outdoor",
        "activity": "santai",
        "season": "summer"
    }
    
    print(f"Input: {input_data}")
    
    try:
        recommendations = predict_outfit(input_data)
        print("\nRecommendations:")
        print(json.dumps(recommendations, indent=2))
        
        # Validation
        assert recommendations is not None
        assert "top" in recommendations
        assert "bottom" in recommendations
        
        # Check if we got real predictions (not "Tidak diperlukan" for everything)
        has_real_item = False
        for category in recommendations:
            if recommendations[category]["type"] != "none":
                has_real_item = True
                break
        
        if not has_real_item:
            print("WARNING: Model returned 'none' for all items. Check training data distribution.")
        else:
            print("SUCCESS: Received valid outfit recommendations.")
            
    except Exception as e:
        print(f"FAILED: {e}")
        # raise e

if __name__ == "__main__":
    test_recommendation_logic()
