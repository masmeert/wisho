import xml.etree.ElementTree as ET

from wisho.jmdict.models import KanjiForm, Meaning, Reading, Word


def parse_entry(entry: ET.Element) -> Word:
    id_elem = entry.find("ent_seq")
    entry_id = int(id_elem.text) if id_elem is not None and id_elem.text else 0

    kanji_forms = []
    for k_ele in entry.findall("k_ele"):
        keb = k_ele.find("keb")
        if keb is not None and keb.text:
            ke_pri = k_ele.find("ke_pri")
            is_common = ke_pri is not None and ke_pri.text == "ichi1"
            kanji_forms.append(KanjiForm(text=keb.text, common=is_common))

    readings = []
    for r_ele in entry.findall("r_ele"):
        reb = r_ele.find("reb")
        if reb is not None and reb.text:
            re_pri = r_ele.find("re_pri")
            has_priority = (
                re_pri is not None and re_pri.text is not None and "ichi" in re_pri.text
            )
            has_common_kanji = any(kf.common for kf in kanji_forms)
            is_common = has_priority or (re_pri is None and has_common_kanji)
            readings.append(Reading(text=reb.text, common=is_common))

    meanings = []
    for sense in entry.findall("sense"):
        glosses = [gloss.text for gloss in sense.findall("gloss") if gloss.text]
        parts_of_speech = [pos.text for pos in sense.findall("pos") if pos.text]

        if glosses:
            meanings.append(Meaning(glosses=glosses, parts_of_speech=parts_of_speech))

    return Word(
        id=entry_id, kanji_forms=kanji_forms, readings=readings, meanings=meanings
    )
