from pydantic import BaseModel, Field

from edict_parser.schemas.gloss import Gloss
from edict_parser.types.dialect import Dialect
from edict_parser.types.field import SubjectField
from edict_parser.types.information import MiscellaneousInformation
from edict_parser.types.language import Gairaigo
from edict_parser.types.part_of_speech import PartOfSpeech


class Sense(BaseModel):
    id: int = Field(...)
    glosses: list[Gloss] = Field(default_factory=list)
    misc: MiscellaneousInformation | None = Field(default=None)
    part_of_speech: list[PartOfSpeech] = Field(default_factory=list)
    antonym: str | None = Field(default=None)
    field: SubjectField | None = Field(default=None)
    xref: str | None = Field(default=None)
    dialect: Dialect | None = Field(default=None)
    information: str | None = Field(default=None)
    gairaigo: Gairaigo | None = Field(default=None)
