import pickle
import os
import sys

# Path to encoders
ENCODER_PATH = "ml/model/encoders.pkl"

def verify_encoders():
    if not os.path.exists(ENCODER_PATH):
        print(f"Error: {ENCODER_PATH} not found.")
        return

    try:
        with open(ENCODER_PATH, "rb") as f:
            data = pickle.load(f)
            
        encoders = data.get("input_encoders", {})
        
        print("\n=== ENCODER CLASSES VERIFICATION ===")
        
        for col, le in encoders.items():
            print(f"\n[{col.upper()}] LabelEncoder Classes:")
            for idx, label in enumerate(le.classes_):
                print(f"  {idx}: {label}")
                
    except Exception as e:
        print(f"Error loading encoders: {e}")

if __name__ == "__main__":
    verify_encoders()
