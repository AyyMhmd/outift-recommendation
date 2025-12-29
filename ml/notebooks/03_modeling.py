import pandas as pd
import numpy as np
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# ===============================
# PATH SETUP
# ===============================
FINAL_DATASET_PATH = "ml/dataset/final/dataset_final.csv"
MODEL_DIR = "ml/model"

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "recommender.pkl")

# ===============================
# 1. LOAD DATASET FINAL
# ===============================
df = pd.read_csv(FINAL_DATASET_PATH)

print("Dataset shape:", df.shape)

# ===============================
# 2. NORMALISASI FITUR NUMERIK
# ===============================
scaler = MinMaxScaler()

numeric_cols = [
    "gender",
    "subCategory",
    "articleType",
    "baseColour",
    "usage",
    "style",
    "weather_condition",
    "trend_score",
]

df_scaled = scaler.fit_transform(df[numeric_cols])

# ===============================
# 3. COSINE SIMILARITY MATRIX
# ===============================
similarity_matrix = cosine_similarity(df_scaled)

print("Similarity matrix shape:", similarity_matrix.shape)


# ===============================
# 4. RECOMMENDATION FUNCTION
# ===============================
def recommend_outfit(input_features: dict, top_n: int = 5):
    """
    input_features = {
        'gender': int,
        'subCategory': int,
        'articleType': int,
        'baseColour': int,
        'usage': int,
        'style': int,
        'weather_condition': int,
        'trend_score': float
    }
    """

    input_vector = np.array([input_features[col] for col in numeric_cols]).reshape(
        1, -1
    )

    input_vector_scaled = scaler.transform(input_vector)

    similarity_scores = cosine_similarity(input_vector_scaled, df_scaled)[0]

    top_indices = similarity_scores.argsort()[::-1][:top_n]

    return df.iloc[top_indices]


# ===============================
# 5. SAVE MODEL
# ===============================
model_artifact = {
    "data": df,
    "scaled_data": df_scaled,
    "scaler": scaler,
    "recommend_function": recommend_outfit,
}

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model_artifact, f)

print("\n✅ MODEL & RECOMMENDER BERHASIL DISIMPAN")
print(f"Model saved to: {MODEL_PATH}")

# ===============================
# 6. TEST QUICK (OPTIONAL)
# ===============================
sample_input = {
    "gender": 1,
    "subCategory": 2,
    "articleType": 5,
    "baseColour": 3,
    "usage": 1,
    "style": 1,
    "weather_condition": 2,
    "trend_score": 0.8,
}

result = recommend_outfit(sample_input, top_n=3)
print("\nSample Recommendation:")
print(result)
