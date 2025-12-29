import pandas as pd
import numpy as np
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score

# ===============================
# PATH SETUP
# ===============================
X_PATH = "ml/dataset/final/X_multilabel.csv"
Y_PATH = "ml/dataset/final/y_multilabel.csv"
MODEL_DIR = "ml/model"

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "multilabel_model.pkl")

# ===============================
# 1. LOAD DATASET
# ===============================
X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH)

print("X shape:", X.shape)
print("y shape:", y.shape)

# ===============================
# 2. TRAIN TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 3. MODEL DEFINITION
# ===============================
base_model = RandomForestClassifier(
    n_estimators=150, max_depth=None, random_state=42, n_jobs=-1
)

model = MultiOutputClassifier(base_model)

# ===============================
# 4. TRAIN MODEL
# ===============================
print("\nTraining model...")
model.fit(X_train, y_train)

# ===============================
# 5. EVALUATION (SUBSET ACCURACY)
# ===============================
y_pred = model.predict(X_test)

subset_accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Model training selesai")
print("Subset accuracy:", subset_accuracy)

# ===============================
# 6. SAVE MODEL
# ===============================
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("\n✅ MODEL MULTILABEL DISIMPAN")
print("Model path:", MODEL_PATH)

# ===============================
# 7. TEST PREDIKSI (SIMULASI)
# ===============================
sample_input = X.iloc[[0]]
sample_pred = model.predict(sample_input)

print("\nSample prediction (binary vector):")
print(sample_pred)
