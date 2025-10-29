from edict_parser.helpers.xml import get_children_texts, get_first_child_text
from edict_parser.jmdict.parsing.priority import parse_priorities
from edict_parser.schemas.entry import EntryElement
from edict_parser.types.information import Information
from lxml import etree


def parse_kanji_forms(entry: etree._Element) -> list[EntryElement]:
    """
    Parse <k_ele> (kanji) blocks.
    """
    kanji_forms: list[EntryElement] = []

    for kanji_element in entry.iterfind("k_ele"):
        if (text := get_first_child_text(kanji_element, "keb")) is None:
            continue

        priority_strings = get_children_texts(kanji_element, "ke_pri")
        priorities = parse_priorities(priority_strings)

        informations = get_children_texts(kanji_element, "ke_inf")
        kanji_informations = []
        for information in informations:
            try:
                kanji_informations.append(Information(information))
            except ValueError:
                continue

        kanji_forms.append(
            EntryElement(
                text=text,
                is_kanji=True,
                priorities=priorities,
                reading_info=kanji_informations,
            )
        )

    return kanji_forms
