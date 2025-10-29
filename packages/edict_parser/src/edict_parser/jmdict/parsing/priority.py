from edict_parser.errors.unknown_priority import UnknownPriorityTypeError
from edict_parser.schemas.priority import Priority


def parse_priorities(priority_strings: list[str]) -> list[Priority]:
    """
    Parse priority strings into Priority objects, skipping invalid ones.
    """
    priorities = []
    for priority_str in priority_strings:
        try:
            priorities.append(Priority.from_string(priority_str))
        except UnknownPriorityTypeError:
            continue
    return priorities
