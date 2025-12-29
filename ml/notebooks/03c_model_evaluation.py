import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# =========================
# BASE DIR
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

X_PATH = os.path.join(BASE_DIR, "..", "dataset", "final", "X_multilabel.csv")
Y_PATH = os.path.join(BASE_DIR, "..", "dataset", "final", "y_multilabel.csv")

MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "outfit_recommendation_model.pkl")

# =========================
# LOAD DATA
# =========================
X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH)

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================
model = OneVsRestClassifier(LogisticRegression(max_iter=1000, solver="lbfgs"))

# =========================
# TRAIN
# =========================
model.fit(X_train, y_train)

# =========================
# SAVE MODEL (INI KUNCI!)
# =========================
joblib.dump(model, MODEL_PATH)

print(f"Model berhasil disimpan di: {MODEL_PATH}")
