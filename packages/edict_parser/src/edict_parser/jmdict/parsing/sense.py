from enum import Enum
from typing import TypeVar

from edict_parser.helpers.xml import get_children_texts, get_first_child_text, get_language_attribute
from edict_parser.schemas.gloss import Gloss
from edict_parser.schemas.sense import Sense
from edict_parser.types.dialect import Dialect
from edict_parser.types.field import SubjectField
from edict_parser.types.gloss import GlossType
from edict_parser.types.information import MiscellaneousInformation
from edict_parser.types.language import Gairaigo, Language
from edict_parser.types.part_of_speech import PartOfSpeech
from lxml import etree

T = TypeVar("T", bound=Enum)


def _safe_enum_parse(value: str | None, enum_class: type[T]) -> T | None:
    """Safely parse a string into an enum, returning None on failure."""
    if not value:
        return None
    try:
        return enum_class(value)
    except ValueError:
        return None


def _parse_part_of_speech(sense_element: etree._Element) -> list[PartOfSpeech]:
    """Parse part of speech tags into PartOfSpeech enum values."""
    pos_strings = get_children_texts(sense_element, "pos")
    return [pos for pos_str in pos_strings if (pos := _safe_enum_parse(pos_str, PartOfSpeech)) is not None]


def _parse_gloss(gloss_element: etree._Element) -> Gloss | None:
    """Parse a single gloss element."""
    if (text := gloss_element.text) is None:
        return None

    language = _safe_enum_parse(get_language_attribute(gloss_element), Language) or Language.ENGLISH
    gtype = _safe_enum_parse(gloss_element.get("g_type"), GlossType)

    return Gloss(language=language, gtype=gtype, text=text.strip())


def _parse_glosses(sense_element: etree._Element) -> list[Gloss]:
    """Parse gloss elements with language and type support."""
    return [
        gloss for gloss_element in sense_element.iterfind("gloss") if (gloss := _parse_gloss(gloss_element)) is not None
    ]


def _parse_gairaigo(sense_element: etree._Element) -> Gairaigo | None:
    """Parse gairaigo (loanword source) from lsource elements."""
    for lsource_element in sense_element.iterfind("lsource"):
        lang_attr = get_language_attribute(lsource_element)
        if gairaigo := _safe_enum_parse(lang_attr, Gairaigo):
            return gairaigo
    return None


def parse_senses(entry: etree._Element) -> list[Sense]:
    """Parse <sense> blocks from an entry element."""
    senses: list[Sense] = []
    for index, sense_element in enumerate(entry.iterfind("sense"), start=1):
        glosses = _parse_glosses(sense_element)
        pos = _parse_part_of_speech(sense_element)
        gairaigo = _parse_gairaigo(sense_element)
        xref = get_first_child_text(sense_element, "xref")
        antonym = get_first_child_text(sense_element, "ant")
        information = get_first_child_text(sense_element, "s_inf")

        misc_str = get_first_child_text(sense_element, "misc")
        misc = _safe_enum_parse(misc_str, MiscellaneousInformation)

        field_str = get_first_child_text(sense_element, "field")
        field = _safe_enum_parse(field_str, SubjectField)

        dialect_str = get_first_child_text(sense_element, "dial")
        dialect = _safe_enum_parse(dialect_str, Dialect)

        sense = Sense(
            id=index,
            glosses=glosses,
            part_of_speech=pos,
            misc=misc,
            field=field,
            dialect=dialect,
            gairaigo=gairaigo,
            xref=xref,
            antonym=antonym,
            information=information,
        )
        senses.append(sense)

    return senses
