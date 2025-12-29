import pandas as pd
import os

# ===============================
# PATH SETUP
# ===============================
RAW_PATH = "ml/dataset/raw/season fashion dataset - multilabel.csv"
CLEAN_DIR = "ml/dataset/clean"
CLEAN_PATH = os.path.join(CLEAN_DIR, "multilabel_clean.csv")

os.makedirs(CLEAN_DIR, exist_ok=True)

# ===============================
# 1. LOAD DATASET
# ===============================
df = pd.read_csv(RAW_PATH, engine="python", encoding="utf-8", on_bad_lines="skip")

print("Raw dataset shape:", df.shape)

# ===============================
# 2. RENAME KOLOM (AMAN UNTUK KODE)
# ===============================
df.rename(
    columns={
        "Jenis Kelamin": "gender",
        "Kondisi Cuaca": "weather",
        "Suhu": "temperature",
        "Kelembapan": "humidity",
        "Lokasi": "location",
        "Aktivitas": "activity",
        "Durasi": "duration",
        "Atasan": "top",
        "Bawahan": "bottom",
        "Pakaian Luar": "outerwear",
        "Alas Kaki": "footwear",
    },
    inplace=True,
)

# ===============================
# 3. DROP MISSING KRITIS
# ===============================
df.dropna(
    subset=["gender", "weather", "activity", "top", "bottom", "footwear"], inplace=True
)

# ===============================
# 4. NORMALISASI TEKS
# ===============================
text_columns = [
    "gender",
    "weather",
    "location",
    "activity",
    "duration",
    "top",
    "bottom",
    "outerwear",
    "footwear",
]

for col in text_columns:
    df[col] = df[col].astype(str).str.lower().str.strip()

# ===============================
# 5. CLEAN MULTILABEL (SPLIT LIST)
# ===============================
multilabel_cols = ["top", "bottom", "outerwear", "footwear"]

for col in multilabel_cols:
    df[col] = df[col].apply(lambda x: [item.strip() for item in x.split(",")])

# ===============================
# 6. NUMERIC CLEANING
# ===============================
df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")

df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

df["temperature"].fillna(df["temperature"].median(), inplace=True)
df["humidity"].fillna(df["humidity"].median(), inplace=True)

# ===============================
# 7. SAVE CLEAN DATA
# ===============================
df.to_csv(CLEAN_PATH, index=False)

print("\n✅ MULTILABEL DATA CLEANING SELESAI")
print("Clean dataset saved to:", CLEAN_PATH)
print("Clean dataset shape:", df.shape)
