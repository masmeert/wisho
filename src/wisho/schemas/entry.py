from pydantic import BaseModel, field_validator
from pydantic.config import ConfigDict


class GetGloss(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    lang: str


class GetSense(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pos: list[str]
    glosses: list[GetGloss]

    @field_validator("pos", mode="before")
    @classmethod
    def extract_pos_tags(cls, v: list | str) -> list[str]:
        """Convert SensePOS objects to strings."""
        if isinstance(v, list) and v and hasattr(v[0], "tag"):
            return [item.tag for item in v]
        if isinstance(v, list):
            return v
        return []


class GetKanji(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    priorities: list[str]

    @field_validator("priorities", mode="before")
    @classmethod
    def extract_priority_strings(cls, v: list | str) -> list[str]:
        """Convert EntryPriority objects to strings."""
        if isinstance(v, list) and v and hasattr(v[0], "raw"):
            return [item.raw for item in v]
        if isinstance(v, list):
            return v
        return []


class GetReading(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    no_kanji: bool
    priorities: list[str]

    @field_validator("priorities", mode="before")
    @classmethod
    def extract_priority_strings(cls, v: list | str) -> list[str]:
        """Convert EntryPriority objects to strings."""
        if isinstance(v, list) and v and hasattr(v[0], "raw"):
            return [item.raw for item in v]
        if isinstance(v, list):
            return v
        return []


class GetEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kanji_forms: list[GetKanji]
    readings: list[GetReading]
    senses: list[GetSense]
