from pydantic import BaseModel


class OutfitInput(BaseModel):
    gender: str
    season: str
    activity: str
    city: str
