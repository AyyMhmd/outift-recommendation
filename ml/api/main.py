from fastapi import FastAPI
from schemas import OutfitInput, OutfitResponse
from predict import predict_outfit

app = FastAPI(
    title="Outfit Recommendation API",
    description="Rekomendasi outfit harian berdasarkan cuaca & aktivitas",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Outfit Recommendation API is running"}


@app.post("/predict", response_model=OutfitResponse)
def predict(data: OutfitInput):
    outfits, images = predict_outfit(data.dict())
    return {"recommended_outfits": outfits, "image_urls": images}
