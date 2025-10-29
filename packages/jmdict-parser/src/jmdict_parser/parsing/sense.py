from lxml import etree

from jmdict_parser.parsing.helpers import get_children_texts, get_language_attribute
from jmdict_parser.schemas import Gloss, Sense


def parse_senses(entry: etree._Element) -> list[Sense]:
    """
    Parse <sense> blocks into SenseDTOs, keeping all gloss languages.
    """
    senses: list[Sense] = []

    for sense_element in entry.iterfind("sense"):
        parts_of_speech = get_children_texts(sense_element, "pos")

        glosses: list[Gloss] = []
        for gloss_element in sense_element.iterfind("gloss"):
            if (text := gloss_element.text) is None:
                continue
            lang = get_language_attribute(gloss_element)
            glosses.append(Gloss(text=text.strip(), lang=lang))

        senses.append(Sense(pos=parts_of_speech, glosses=glosses))

    return senses
