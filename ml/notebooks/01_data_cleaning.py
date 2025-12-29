import pandas as pd
import os

# ===============================
# PATH SETUP
# ===============================
RAW_DIR = "ml/dataset/raw"
CLEAN_DIR = "ml/dataset/clean"

os.makedirs(CLEAN_DIR, exist_ok=True)

STYLES_PATH = os.path.join(RAW_DIR, "styles.csv")
TREND_PATH = os.path.join(RAW_DIR, "Fashion(Data Points) - Form responses 1.csv")

# ===============================
# 1. LOAD DATASET (AMAN CSV RUSAK)
# ===============================
styles_df = pd.read_csv(
    STYLES_PATH, engine="python", encoding="latin1", on_bad_lines="skip"
)

trend_df = pd.read_csv(TREND_PATH, engine="python", encoding="utf-8")

print("Styles dataset shape (raw):", styles_df.shape)
print("Trend dataset shape (raw):", trend_df.shape)

# ===============================
# 2. CLEANING DATASET FASHION
# ===============================

# Pastikan kolom yang dibutuhkan ada
required_columns = [
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "usage",
]

styles_df = styles_df[required_columns]

# Filter hanya Apparel
styles_df = styles_df[styles_df["masterCategory"] == "Apparel"]

# Drop kolom masterCategory (tidak dipakai lagi)
styles_df.drop(columns=["masterCategory"], inplace=True)

# Drop missing values
styles_df.dropna(inplace=True)

# Drop duplicate rows
styles_df.drop_duplicates(inplace=True)

# Normalisasi teks
for col in styles_df.columns:
    styles_df[col] = styles_df[col].astype(str).str.lower().str.strip()

print("Styles dataset shape (clean):", styles_df.shape)

# Simpan hasil cleaning fashion
fashion_clean_path = os.path.join(CLEAN_DIR, "fashion_clean.csv")
styles_df.to_csv(fashion_clean_path, index=False)

# ===============================
# 3. CLEANING DATASET TREND (SURVEY)
# ===============================

print("\nKolom dataset trend:")
print(trend_df.columns)

# Ambil kolom gaya berpakaian (asumsi kolom ke-2)
STYLE_COLUMN = trend_df.columns[1]

trend_style_df = trend_df[[STYLE_COLUMN]].copy()
trend_style_df.columns = ["style"]

# Drop missing
trend_style_df.dropna(inplace=True)

# Normalisasi teks
trend_style_df["style"] = trend_style_df["style"].astype(str).str.lower().str.strip()

# Hitung frekuensi style
style_count = trend_style_df["style"].value_counts().reset_index()
style_count.columns = ["style", "count"]

# Normalisasi skor tren (0–1)
style_count["trend_score"] = style_count["count"] / style_count["count"].max()

print("\nTrend score result:")
print(style_count.head())

# Simpan hasil cleaning trend
trend_clean_path = os.path.join(CLEAN_DIR, "trend_clean.csv")
style_count.to_csv(trend_clean_path, index=False)

# ===============================
# 4. DONE
# ===============================
print("\n✅ DATA CLEANING SELESAI")
print(f"Fashion clean saved to: {fashion_clean_path}")
print(f"Trend clean saved to: {trend_clean_path}")
