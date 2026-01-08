import pickle
import joblib
import os
import sys

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCODERS_PATH = os.path.join(BASE_DIR, "encoders.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "multilabel_model.pkl")

print(f"Loading encoders from {ENCODERS_PATH}...")
try:
    with open(ENCODERS_PATH, "rb") as f:
        encoders = pickle.load(f)
    print("\n✅ Encoders loaded.")
    # print("Keys/Content:", encoders.keys())
    
    if "input_encoders" in encoders:
        print("\nInput Encoders:")
        for k, v in encoders["input_encoders"].items():
            print(f"  - {k}: {v.classes_}")

    if "target_encoder" in encoders: # Assuming separate label encoder
         print("\nTarget Encoder Classes:", encoders["target_encoder"].classes_)
    elif "mlb" in encoders:
         print("\nMultiLabelBinarizer Classes:", encoders["mlb"].classes_)
    elif "output_encoder" in encoders:
         print("\nOutput Encoder Classes (MultiLabelBinarizer):", encoders["output_encoder"].classes_)
    else:
         print("\nPrinting full Content to find target labels:\n", encoders)
    
except Exception as e:
    print(f"❌ Failed to load encoders: {e}")

print(f"\nLoading model from {MODEL_PATH}...")
try:
    model = joblib.load(MODEL_PATH)
    print("\n✅ Model loaded.")
    if hasattr(model, "estimators_"):
        print("Model has estimators. Number of output classes:", len(model.estimators_))
    if hasattr(model, "classes_"):
        print("Model classes (if available):", model.classes_)
        
except Exception as e:
    print(f"❌ Failed to load model: {e}")
