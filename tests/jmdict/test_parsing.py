from pathlib import Path
import pytest

from wisho.jmdict.models import KanjiForm, Meaning, Reading, Word
from wisho.jmdict.parser import parse_entry

DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def sample_entry_xml():
    from xml.etree import ElementTree as ET

    entry = ET.parse(DATA_DIR / "sample_entry.xml").getroot()
    return entry


def test_correctly_parse_sample_entry(sample_entry_xml):
    excepted = Word(
        id=1206730,
        kanji_forms=[KanjiForm(text="学校", common=True)],
        readings=[Reading(text="がっこう", common=True)],
        meanings=[
            Meaning(
                glosses=["school", "educational institution"],
                parts_of_speech=["noun (common) (futsu-meishi)"],
            )
        ],
    )

    parsed_entry = parse_entry(sample_entry_xml)

    assert parsed_entry == excepted
