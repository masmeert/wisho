from lxml import etree

from jmdict_parser.parsing.helpers import get_children_texts, get_first_child_text
from jmdict_parser.schemas import Kanji


def parse_kanji_forms(entry: etree._Element) -> list[Kanji]:
    """
    Parse <k_ele> blocks into `Kanji`.
    """
    kanji_forms: list[Kanji] = []
    for kanji_element in entry.iterfind("k_ele"):
        if (text := get_first_child_text(kanji_element, "keb")) is None:
            continue
        priorities = get_children_texts(kanji_element, "ke_pri")
        kanji_forms.append(Kanji(text=text, priorities=priorities))
    return kanji_forms
