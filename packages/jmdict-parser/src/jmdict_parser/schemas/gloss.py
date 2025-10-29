from pydantic import BaseModel, ConfigDict, Field


class Gloss(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    lang: str = Field(default="eng")
