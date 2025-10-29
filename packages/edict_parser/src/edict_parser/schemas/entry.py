from pydantic import BaseModel, Field, ValidationInfo, field_validator

from edict_parser.schemas.priority import Priority
from edict_parser.schemas.sense import Sense
from edict_parser.types.information import Information
from edict_parser.types.priority import PriorityType


class EntryElement(BaseModel):
    text: str = Field(...)
    is_kanji: bool = Field(default=False)
    priorities: list[Priority] = Field(default_factory=list)
    reading_info: list[Information] = Field(default_factory=list)
    no_true_reading: bool = Field(default=False)


class Entry(BaseModel):
    sequence: int = Field(...)
    elements: list[EntryElement] = Field(default_factory=list)
    senses: list[Sense] = Field(default_factory=list)

    is_common: bool = Field(default=False)

    @field_validator("is_common", mode="before")
    @classmethod
    def calculate_commonality(cls, value: bool | None, info: ValidationInfo) -> bool:  # noqa: FBT001
        if value is not None:
            return value

        all_priorities = []
        for element in info.data.get("elements", []):
            if hasattr(element, "priorities"):
                all_priorities.extend(element.priorities)

        return cls.determine_commonality(all_priorities)

    @staticmethod
    def determine_commonality(priorities: list[Priority]) -> bool:
        for priority in priorities:
            # Ichinamen top words: strongest indicator
            if priority.priority_type == PriorityType.Ichi and priority.level <= 2:  # noqa: PLR2004
                return True

            # High frequency in newspapers
            if priority.priority_type == PriorityType.News and priority.level <= 3:  # noqa: PLR2004
                return True

            # Top specialized frequency
            if priority.priority_type == PriorityType.Spec and priority.level == 1:
                return True

        return False
