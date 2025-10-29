from pydantic import BaseModel, ConfigDict, Field


class Kanji(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    priorities: list[str] = Field(default_factory=list)
