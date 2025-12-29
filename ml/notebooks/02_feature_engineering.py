import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

# ===============================
# PATH SETUP
# ===============================
CLEAN_DIR = "ml/dataset/clean"
FINAL_DIR = "ml/dataset/final"

os.makedirs(FINAL_DIR, exist_ok=True)

FASHION_CLEAN_PATH = os.path.join(CLEAN_DIR, "fashion_clean.csv")
TREND_CLEAN_PATH = os.path.join(CLEAN_DIR, "trend_clean.csv")

# ===============================
# 1. LOAD CLEAN DATA
# ===============================
fashion_df = pd.read_csv(FASHION_CLEAN_PATH)
trend_df = pd.read_csv(TREND_CLEAN_PATH)

print("Fashion clean shape:", fashion_df.shape)
print("Trend clean shape:", trend_df.shape)

# ===============================
# 2. MAP STYLE KE TREND SCORE
# ===============================
# Mapping sederhana: usage ↔ style
# (bisa dikembangkan nanti)

style_mapping = {
    "casual": "casual",
    "formal": "formal",
    "sports": "sporty",
    "ethnic": "ethnic",
    "party": "party",
}

fashion_df["style"] = fashion_df["usage"].map(style_mapping)

# Isi yang tidak ter-mapping
fashion_df["style"].fillna("casual", inplace=True)

# Gabungkan trend score
fashion_df = fashion_df.merge(
    trend_df[["style", "trend_score"]], on="style", how="left"
)

# Jika style tidak ada di trend → skor default
fashion_df["trend_score"].fillna(0.3, inplace=True)

# ===============================
# 3. FEATURE CUACA (SIMULASI TERKONTROL)
# ===============================
# 0 = dingin, 1 = normal, 2 = panas

weather_mapping = {"winter": 0, "fall": 1, "spring": 1, "summer": 2}

fashion_df["weather_condition"] = fashion_df["season"].map(weather_mapping)

# Default jika season tidak dikenal
fashion_df["weather_condition"].fillna(1, inplace=True)

# ===============================
# 4. ENCODING FITUR KATEGORIKAL
# ===============================
encoder = LabelEncoder()

categorical_cols = [
    "gender",
    "subCategory",
    "articleType",
    "baseColour",
    "usage",
    "style",
]

for col in categorical_cols:
    fashion_df[col] = encoder.fit_transform(fashion_df[col])

# ===============================
# 5. SELECT FINAL FEATURES
# ===============================
final_df = fashion_df[
    [
        "gender",
        "subCategory",
        "articleType",
        "baseColour",
        "usage",
        "style",
        "weather_condition",
        "trend_score",
    ]
]

print("Final dataset shape:", final_df.shape)

# ===============================
# 6. SAVE FINAL DATASET
# ===============================
final_path = os.path.join(FINAL_DIR, "dataset_final.csv")
final_df.to_csv(final_path, index=False)

print("\n✅ FEATURE ENGINEERING SELESAI")
print(f"Final dataset saved to: {final_path}")
