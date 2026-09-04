from typing import Literal
from pydantic import BaseModel, Field, validator

class ObservationIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    location: str = Field(min_length=1, max_length=100)
    category: Literal["flora", "fauna", "weather", "terrain"] = "flora"
    condition: Literal["stable", "watch", "critical"] = "stable"
    notes: str = Field(default="", max_length=1200)
    temperature: float | None = Field(default=None, ge=-80, le=80)

    @validator("title", "location")
    def strip_required(cls, value: str) -> str:
        if not (clean := value.strip()):
            raise ValueError("must not be blank")
        return clean
