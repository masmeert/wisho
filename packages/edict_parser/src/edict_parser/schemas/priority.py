from pydantic import BaseModel, Field

from edict_parser.errors.unknown_priority import UnknownPriorityTypeError
from edict_parser.types.priority import PriorityType


class Priority(BaseModel):
    priority_type: PriorityType = Field(...)
    level: int = Field(...)

    @classmethod
    def from_string(cls, priority_str: str) -> "Priority":
        for ptype in PriorityType:
            if priority_str.startswith(ptype.value):
                level_string = priority_str[len(ptype.value) :]
                if level_string.isdigit():
                    return cls(priority_type=ptype, level=int(level_string))

        raise UnknownPriorityTypeError(priority_str)
