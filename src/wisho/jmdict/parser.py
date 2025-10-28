from __future__ import annotations

from pathlib import Path

from lxml import etree

from wisho.jmdict.dto import EntryDTO, GlossDTO, KanjiDTO, ReadingDTO, SenseDTO

PATH = Path(__file__).resolve().parents[2] / "resources" / "JMdict_e"

XmlElement = etree._Element  # noqa: SLF001


class MalformedJMDictEntryError(Exception):
    def __init__(self) -> None:
        super().__init__("Malformed JMdict entry")


def _text_list(parent: XmlElement, tag: str) -> list[str]:
    """
    Return the stripped text content of all child elements named `tag` under `parent`.
    Skips empty or whitespace-only text.
    """
    return [node.text.strip() for node in parent.iterfind(tag) if node.text and node.text.strip()]


def _first_text(parent: XmlElement, tag: str) -> str | None:
    """
    Return the stripped text of the first child named `tag`, or None if missing/empty.
    """
    if (node := parent.find(tag)) is None or node.text is None:
        return None
    text = node.text.strip()
    return text if text else None


def _parse_kanji_forms(entry: XmlElement) -> list[KanjiDTO]:
    """
    Parse <k_ele> blocks into KanjiDTOs.
    """
    kanji_forms: list[KanjiDTO] = []
    for kanji_element in entry.iterfind("k_ele"):
        if (text := _first_text(kanji_element, "keb")) is None:
            continue
        priorities = _text_list(kanji_element, "ke_pri")
        kanji_forms.append(KanjiDTO(text=text, priorities=priorities))
    return kanji_forms


def _parse_readings(entry: XmlElement) -> list[ReadingDTO]:
    """
    Parse <r_ele> blocks into ReadingDTOs.
    """
    readings: list[ReadingDTO] = []
    for reading_element in entry.iterfind("r_ele"):
        if (text := _first_text(reading_element, "reb")) is None:
            continue
        priorities = _text_list(reading_element, "re_pri")
        restrictions = _text_list(reading_element, "re_restr")
        no_kanji = reading_element.find("re_nokanji") is not None
        readings.append(
            ReadingDTO(
                text=text,
                priorities=priorities,
                restrictions=restrictions,
                no_kanji=no_kanji,
            )
        )
    return readings


def _get_lang_attr(element: XmlElement) -> str:
    """
    Extract the language attribute from an element, checking both standard and XML namespace versions.
    Defaults to "eng" if not found.
    """
    return element.get("lang") or element.get("{http://www.w3.org/XML/1998/namespace}lang") or "eng"


def _parse_senses(entry: XmlElement) -> list[SenseDTO]:
    """
    Parse <sense> blocks into SenseDTOs, keeping all gloss languages.
    """
    senses: list[SenseDTO] = []

    for sense_element in entry.iterfind("sense"):
        parts_of_speech = _text_list(sense_element, "pos")

        glosses: list[GlossDTO] = []
        for gloss_element in sense_element.iterfind("gloss"):
            if (text := gloss_element.text) is None:
                continue
            lang = _get_lang_attr(gloss_element)
            glosses.append(GlossDTO(text=text.strip(), lang=lang))

        senses.append(SenseDTO(pos=parts_of_speech, glosses=glosses))

    return senses


def parse_entry(jmdict_entry: XmlElement) -> EntryDTO:
    """
    Parse a single <entry> element from JMdict_e into an EntryDTO.

    Raises:
        ValueError: If the entry is missing <ent_seq> or if <ent_seq> is not a valid integer.
    """
    entity_sequence = _first_text(jmdict_entry, "ent_seq")
    if entity_sequence is None:
        raise MalformedJMDictEntryError()

    try:
        entry_id = int(entity_sequence)
    except ValueError as exc:
        raise MalformedJMDictEntryError() from exc

    kanji_forms = _parse_kanji_forms(jmdict_entry)
    readings = _parse_readings(jmdict_entry)
    senses = _parse_senses(jmdict_entry)

    return EntryDTO(id=entry_id, kanji_forms=kanji_forms, readings=readings, senses=senses)


def parse_jmdict_file() -> list[EntryDTO]:
    """
    Parse the JMdict_e XML file and return a list of EntryDTOs.
    """
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True, huge_tree=True)
    tree = etree.parse(PATH, parser=parser)
    root = tree.getroot()

    entries: list[EntryDTO] = []
    for jmdict_entry in root.iterfind("entry"):
        entry_dto = parse_entry(jmdict_entry)
        entries.append(entry_dto)

    return entries
