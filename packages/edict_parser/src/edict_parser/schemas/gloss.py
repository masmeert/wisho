from pydantic import BaseModel, Field

from edict_parser.types.gloss import GlossType
from edict_parser.types.language import Language


class Gloss(BaseModel):
    language: Language = Field(...)
    gtype: GlossType | None = Field(default=None)
    text: str = Field(...)
