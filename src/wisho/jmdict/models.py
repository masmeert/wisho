from typing import Optional
from pydantic import BaseModel


class KanjiForm(BaseModel):
    text: str
    common: bool = False


class Reading(BaseModel):
    text: str
    common: bool = False
    applies_to_kanji: Optional[list[str]] = None


class Meaning(BaseModel):
    glosses: list[str]
    parts_of_speech: list[str]
    applies_to_kanji: Optional[list[str]] = None
    applies_to_reading: Optional[list[str]] = None


class Word(BaseModel):
    id: int

    kanji_forms: list[KanjiForm]
    readings: list[Reading]
    meanings: list[Meaning]
    common: bool = False
