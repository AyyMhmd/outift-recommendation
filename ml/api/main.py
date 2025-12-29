from fastapi import FastAPI
from schemas import OutfitInput
from predict import predict_outfit

app = FastAPI(title="Outfit Recommendation API")


@app.post("/predict")
def predict(data: OutfitInput):
    outfits = predict_outfit(data.dict())
    return {"city": data.city, "recommended_outfits": outfits}
