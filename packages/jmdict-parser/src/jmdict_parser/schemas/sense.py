from pydantic import BaseModel, ConfigDict, Field

from jmdict_parser.schemas.gloss import Gloss


class Sense(BaseModel):
    model_config = ConfigDict(frozen=True)

    pos: list[str] = Field(default_factory=list)
    glosses: list[Gloss] = Field(default_factory=list)
