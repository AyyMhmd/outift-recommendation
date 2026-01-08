import pandas as pd
import os
import pickle
import ast
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

# ===============================
# PATH SETUP
# ===============================
CLEAN_PATH = "ml/dataset/clean/multilabel_clean.csv"
FINAL_DIR = "ml/dataset/final"
MODEL_DIR = "ml/model"

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

X_PATH = os.path.join(FINAL_DIR, "X_multilabel.csv")
Y_PATH = os.path.join(FINAL_DIR, "y_multilabel.csv")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoders.pkl")

# ===============================
# 1. LOAD CLEAN DATA
# ===============================
df = pd.read_csv(CLEAN_PATH)

# Parse stringified lists back to python lists
multilabel_cols = ["top", "bottom", "outerwear", "footwear"]
for col in multilabel_cols:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

print("Clean dataset shape:", df.shape)

# ===============================
# 2. INPUT FEATURES (X)
# ===============================
input_cols = [
    "gender",
    "weather",
    "temperature",
    "humidity",
    "location",
    "activity",
    "duration",
]

X = df[input_cols].copy()

# ===============================
# 3. LABEL ENCODING INPUT
# ===============================
encoders = {}

categorical_cols = ["gender", "weather", "location", "activity", "duration"]

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# ===============================
# 4. OUTPUT MULTILABEL (y)
# ===============================
output_cols = ["top", "bottom", "outerwear", "footwear"]

# Gabungkan semua label outfit
df["outfit_labels"] = df["top"] + df["bottom"] + df["outerwear"] + df["footwear"]

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df["outfit_labels"])

# ===============================
# 5. SAVE OUTPUT
# ===============================
pd.DataFrame(X).to_csv(X_PATH, index=False)
pd.DataFrame(y, columns=mlb.classes_).to_csv(Y_PATH, index=False)

with open(ENCODER_PATH, "wb") as f:
    pickle.dump({"input_encoders": encoders, "output_encoder": mlb}, f)

print("\n✅ FEATURE ENGINEERING MULTILABEL SELESAI")
print("X saved to:", X_PATH)
print("y saved to:", Y_PATH)
print("Encoder saved to:", ENCODER_PATH)
