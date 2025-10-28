from pydantic import BaseModel, ConfigDict, Field, field_validator


class MissingReadingError(Exception):
    def __init__(self) -> None:
        super().__init__("Entry must have at least one reading")


class MissingSenseError(Exception):
    def __init__(self) -> None:
        super().__init__("Entry must have at least one sense")


class KanjiDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    priorities: list[str] = Field(default_factory=list)


class ReadingDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    no_kanji: bool = Field(default=False)
    priorities: list[str] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)


class GlossDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = Field(...)
    lang: str = Field(default="eng")


class SenseDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    pos: list[str] = Field(default_factory=list)
    glosses: list[GlossDTO] = Field(default_factory=list)


class EntryDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int = Field(...)
    kanji_forms: list[KanjiDTO] = Field(default_factory=list)
    readings: list[ReadingDTO] = Field(default_factory=list)
    senses: list[SenseDTO] = Field(default_factory=list)

    @field_validator("readings")
    def _must_have_at_least_one_reading(self, v: list[ReadingDTO]) -> list[ReadingDTO]:
        if not v:
            raise MissingReadingError()
        return v

    @field_validator("senses")
    def _must_have_at_least_one_sense(self, v: list[SenseDTO]) -> list[SenseDTO]:
        if not v:
            raise MissingSenseError()
        return v
