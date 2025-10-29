from pydantic import BaseModel, ConfigDict, Field


class Reading(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    no_kanji: bool = Field(default=False)
    priorities: list[str] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)
