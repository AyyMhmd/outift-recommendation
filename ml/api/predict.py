import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "outfit_recommendation_model.pkl")
X_COLUMNS_PATH = os.path.join(BASE_DIR, "..", "dataset", "final", "X_multilabel.csv")

model = joblib.load(MODEL_PATH)
X_columns = pd.read_csv(X_COLUMNS_PATH).columns.tolist()

# mapping outfit -> gambar (bisa diganti URL CDN)
OUTFIT_IMAGES = {
    "tshirt": "https://example.com/images/tshirt.png",
    "jacket": "https://example.com/images/jacket.png",
    "hoodie": "https://example.com/images/hoodie.png",
    "dress": "https://example.com/images/dress.png",
    "shorts": "https://example.com/images/shorts.png",
}


def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])

    df = pd.get_dummies(df)

    # samakan feature dengan training
    for col in X_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[X_columns]
    return df


def predict_outfit(data: dict):
    X = preprocess_input(data)
    preds = model.predict(X)[0]

    labels = model.classes_
    recommended = [labels[i] for i, v in enumerate(preds) if v == 1]

    images = [OUTFIT_IMAGES.get(o, "") for o in recommended]

    return recommended, images
