from edict_parser.errors.invalid_entity_sequence import InvalidEntitySequenceError
from edict_parser.jmdict.parsing.kanji import parse_kanji_forms
from edict_parser.jmdict.parsing.reading import parse_readings
from edict_parser.jmdict.parsing.sense import parse_senses
from edict_parser.schemas.entry import Entry, EntryElement
from lxml import etree


def parse_entry_element(entry_element: etree._Element) -> list[EntryElement]:
    """
    Parse both <k_ele> (kanji) and <r_ele> (reading) blocks into unified EntryElement objects.
    """
    elements: list[EntryElement] = []

    elements.extend(parse_kanji_forms(entry_element))
    elements.extend(parse_readings(entry_element))

    return elements


def parse_jmdict_entry(jmdict_entry_element: etree._Element) -> Entry:
    """
    Parse a <entry> element into an Entry object.
    """
    entity_sequence_text = jmdict_entry_element.findtext("ent_seq")
    if entity_sequence_text is None:
        raise InvalidEntitySequenceError()
    try:
        entity_sequence = int(entity_sequence_text)
    except ValueError as exc:
        raise InvalidEntitySequenceError() from exc

    elements = parse_entry_element(jmdict_entry_element)
    senses = parse_senses(jmdict_entry_element)

    return Entry(sequence=entity_sequence, elements=elements, senses=senses)
