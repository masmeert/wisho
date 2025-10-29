from lxml import etree

from jmdict_parser.errors import InvalidEntitySequenceError
from jmdict_parser.parsing.helpers import get_first_child_text
from jmdict_parser.parsing.kanji import parse_kanji_forms
from jmdict_parser.parsing.reading import parse_readings
from jmdict_parser.parsing.sense import parse_senses
from jmdict_parser.schemas import Entry


def parse_entry(jmdict_entry: etree._Element) -> Entry:
    """
    Parse a single <entry> element from JMdict_e into an EntryDTO.

    Raises:
        ValueError: If the entry is missing <ent_seq> or if <ent_seq> is not a valid integer.
    """
    entity_sequence = get_first_child_text(jmdict_entry, "ent_seq")
    if entity_sequence is None:
        raise InvalidEntitySequenceError()

    try:
        entry_id = int(entity_sequence)
    except ValueError as exc:
        raise InvalidEntitySequenceError() from exc

    kanji_forms = parse_kanji_forms(jmdict_entry)
    readings = parse_readings(jmdict_entry)
    senses = parse_senses(jmdict_entry)

    return Entry(id=entry_id, kanji_forms=kanji_forms, readings=readings, senses=senses)
