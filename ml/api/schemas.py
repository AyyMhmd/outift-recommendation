from pydantic import BaseModel


class OutfitInput(BaseModel):
    gender: str
    season: str
    activity: str
    temperature: float
    humidity: float


class OutfitResponse(BaseModel):
    recommended_outfits: list[str]
    image_urls: list[str]
