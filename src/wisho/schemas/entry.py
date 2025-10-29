from pydantic import BaseModel
from pydantic.config import ConfigDict


class GetGloss(BaseModel):
    text: str
    lang: str


class GetSense(BaseModel):
    pos: list[str]
    glosses: list[GetGloss]


class GetKanji(BaseModel):
    text: str
    priorities: list[str]


class GetReading(BaseModel):
    text: str
    priorities: list[str]
    no_kanji: bool


class GetEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kanji_forms: list[GetKanji]
    readings: list[GetReading]
    senses: list[GetSense]
