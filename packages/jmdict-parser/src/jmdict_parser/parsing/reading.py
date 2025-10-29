from lxml import etree

from jmdict_parser.parsing.helpers import get_children_texts, get_first_child_text
from jmdict_parser.schemas import Reading


def parse_readings(entry: etree._Element) -> list[Reading]:
    """
    Parse <r_ele> blocks into ReadingDTOs.
    """
    readings: list[Reading] = []
    for reading_element in entry.iterfind("r_ele"):
        if (text := get_first_child_text(reading_element, "reb")) is None:
            continue
        priorities = get_children_texts(reading_element, "re_pri")
        restrictions = get_children_texts(reading_element, "re_restr")
        no_kanji = reading_element.find("re_nokanji") is not None
        readings.append(
            Reading(
                text=text,
                priorities=priorities,
                restrictions=restrictions,
                no_kanji=no_kanji,
            )
        )
    return readings
