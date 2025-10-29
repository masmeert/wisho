from pydantic import BaseModel, ConfigDict, Field, field_validator

from jmdict_parser.errors import MissingReadingError, MissingSenseError
from jmdict_parser.schemas.kanji import Kanji
from jmdict_parser.schemas.reading import Reading
from jmdict_parser.schemas.sense import Sense


class Entry(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int = Field(...)
    kanji_forms: list[Kanji] = Field(default_factory=list)
    readings: list[Reading] = Field(default_factory=list)
    senses: list[Sense] = Field(default_factory=list)

    @field_validator("readings")
    @classmethod
    def _must_have_at_least_one_reading(cls, v: list[Reading]) -> list[Reading]:
        if not v:
            raise MissingReadingError()
        return v

    @field_validator("senses")
    @classmethod
    def _must_have_at_least_one_sense(cls, v: list[Sense]) -> list[Sense]:
        if not v:
            raise MissingSenseError()
        return v
