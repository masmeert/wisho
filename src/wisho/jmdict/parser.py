from pathlib import Path
from lxml import etree as ET

from wisho.jmdict.dto import EntryDTO, GlossDTO, KanjiDTO, ReadingDTO, SenseDTO


PATH = Path(__file__).resolve().parents[4] / "resources" / "JMdict_e"


def _find_text_elements(parent: ET._Element, tag: str) -> list[str]:
    return [element.text for element in parent.findall(tag) if element.text is not None]


def _parse_kanji_forms(entry: ET._Element) -> list[KanjiDTO]:
    kanji_forms: list[KanjiDTO] = []
    for kanji_element in entry.findall("k_ele"):
        text = kanji_element.findtext("keb")
        if not text:
            continue

        priorities = _find_text_elements(kanji_element, "ke_pri")

        kanji = KanjiDTO(text=text, priorities=priorities)
        kanji_forms.append(kanji)
    return kanji_forms


def _parse_readings(entry: ET._Element) -> list[ReadingDTO]:
    readings: list[ReadingDTO] = []
    for reading_element in entry.findall("r_ele"):
        text = reading_element.findtext("reb")
        if not text:
            continue

        priorities = _find_text_elements(reading_element, "re_pri")
        restrictions = _find_text_elements(reading_element, "re_restr")

        reading = ReadingDTO(
            text=text, priorities=priorities, restrictions=restrictions
        )
        readings.append(reading)
    return readings


def _parse_senses(entry: ET._Element) -> list[SenseDTO]:
    senses: list[SenseDTO] = []
    for sense_element in entry.findall("sense"):
        parts_of_speech = _find_text_elements(sense_element, "pos")
        glosses: list[GlossDTO] = []
        for index, gloss_element in enumerate(sense_element.findall("gloss"), start=1):
            if gloss_element.text is None:
                continue

            gloss_lang = gloss_element.get("lang") or "eng"
            gloss_element = GlossDTO(
                text=gloss_element.text,
                lang=gloss_lang,
            )
            glosses.append(gloss_element)
        sense = SenseDTO(
            pos=parts_of_speech,
            glosses=glosses,
        )
        senses.append(sense)
    return senses


def parse_entry(jmdict_entry: ET._Element) -> EntryDTO:
    entry_sequence = jmdict_entry.findtext("ent_seq")
    if not entry_sequence:
        # Should never happen
        raise ValueError("Missing <ent_seq>")

    entry_id = int(entry_sequence)

    kanji_forms = _parse_kanji_forms(jmdict_entry)
    readings = _parse_readings(jmdict_entry)
    senses = _parse_senses(jmdict_entry)

    return EntryDTO(
        id=entry_id,
        kanji_forms=kanji_forms,
        readings=readings,
        senses=senses,
    )
