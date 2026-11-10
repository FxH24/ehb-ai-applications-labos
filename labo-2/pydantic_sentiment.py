from typing import Literal

from pydantic import BaseModel


class Sentiment(BaseModel):
    sentiment: Literal["positief", "negatief"]
    confidence: float | None
