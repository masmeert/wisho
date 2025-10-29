from edict_parser.helpers.xml import get_children_texts, get_first_child_text
from edict_parser.jmdict.parsing.priority import parse_priorities
from edict_parser.schemas.entry import EntryElement
from edict_parser.types.information import Information
from lxml import etree


def parse_readings(entry: etree._Element) -> list[EntryElement]:
    """
    Parse <r_ele> (reading) blocks.
    """
    elements: list[EntryElement] = []

    for reading_element in entry.iterfind("r_ele"):
        if (text := get_first_child_text(reading_element, "reb")) is None:
            continue

        priority_strings = get_children_texts(reading_element, "re_pri")
        priorities = parse_priorities(priority_strings)

        info_strings = get_children_texts(reading_element, "re_inf")
        reading_info = []
        for info_str in info_strings:
            try:
                reading_info.append(Information(info_str))
            except ValueError:
                continue

        no_true_reading = reading_element.find("re_nokanji") is not None

        elements.append(
            EntryElement(
                text=text,
                is_kanji=False,
                priorities=priorities,
                reading_info=reading_info,
                no_true_reading=no_true_reading,
            )
        )

    return elements
