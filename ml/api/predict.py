from weather import get_weather
import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "outfit_recommendation_model.pkl")
X_COLUMNS_PATH = os.path.join(BASE_DIR, "..", "dataset", "final", "X_multilabel.csv")

model = joblib.load(MODEL_PATH)
X_columns = pd.read_csv(X_COLUMNS_PATH).columns.tolist()


def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    df = pd.get_dummies(df)

    for col in X_columns:
        if col not in df.columns:
            df[col] = 0

    return df[X_columns]


def predict_outfit(data: dict):
    weather = get_weather(data["city"])

    input_data = {
        "gender": data["gender"],
        "season": data["season"],
        "activity": data["activity"],
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
    }

    X = preprocess_input(input_data)
    preds = model.predict(X)[0]

    labels = model.classes_
    return [labels[i] for i, v in enumerate(preds) if v == 1]
