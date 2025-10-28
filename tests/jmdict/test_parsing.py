from pathlib import Path
import pytest
from lxml import etree as ET

from wisho.jmdict.dto import EntryDTO, GlossDTO, KanjiDTO, ReadingDTO, SenseDTO
from wisho.jmdict.parser import parse_entry

DATA_DIR = Path(__file__).parent.parent / "data"

EXPECTED_PARSED_ENTRIES = [
    EntryDTO(
        id=1206730,
        kanji_forms=[
            KanjiDTO(text="学校", priorities=["ichi1", "news1", "nf01"]),
            KanjiDTO(text="學校", priorities=[]),
        ],
        readings=[
            ReadingDTO(
                text="がっこう",
                priorities=["ichi1", "news1", "nf01"],
                no_kanji=False,
                restrictions=[],
            )
        ],
        senses=[
            SenseDTO(
                pos=["n"],
                glosses=[GlossDTO(text="school", lang="eng")],
            )
        ],
    ),
    EntryDTO(
        id=1000300,
        kanji_forms=[
            KanjiDTO(text="遇う", priorities=[]),
            KanjiDTO(text="配う", priorities=[]),
        ],
        readings=[
            ReadingDTO(
                text="あしらう",
                priorities=[],
                no_kanji=False,
                restrictions=[],
            ),
        ],
        senses=[
            SenseDTO(
                pos=["v5u", "vt"],
                glosses=[
                    GlossDTO(text="to treat", lang="eng"),
                    GlossDTO(text="to handle", lang="eng"),
                    GlossDTO(text="to deal with", lang="eng"),
                ],
            ),
            SenseDTO(
                pos=["v5u", "vt"],
                glosses=[
                    GlossDTO(text="to arrange", lang="eng"),
                    GlossDTO(text="to decorate (with)", lang="eng"),
                    GlossDTO(text="to adorn (with)", lang="eng"),
                    GlossDTO(text="to dress (with)", lang="eng"),
                    GlossDTO(text="to garnish (with)", lang="eng"),
                ],
            ),
        ],
    ),
    EntryDTO(
        id=1000440,
        kanji_forms=[
            KanjiDTO(text="あの人", priorities=["spec1"]),
            KanjiDTO(text="彼の人", priorities=[]),
        ],
        readings=[
            ReadingDTO(
                text="あのひと",
                priorities=["spec1"],
                no_kanji=False,
                restrictions=[],
            ),
        ],
        senses=[
            SenseDTO(
                pos=["pn"],
                glosses=[
                    GlossDTO(text="he", lang="eng"),
                    GlossDTO(text="she", lang="eng"),
                    GlossDTO(text="that person", lang="eng"),
                ],
            ),
            SenseDTO(
                pos=["pn"],
                glosses=[
                    GlossDTO(text="you", lang="eng"),
                ],
            ),
        ],
    ),
    EntryDTO(
        id=5746823,
        kanji_forms=[
            KanjiDTO(text="ＷｉｎＲＡＲ", priorities=[]),
        ],
        readings=[
            ReadingDTO(
                text="ウィンアールエーアール",
                priorities=[],
                no_kanji=False,
                restrictions=[],
            ),
            ReadingDTO(
                text="ウィンラー", priorities=[], no_kanji=False, restrictions=[]
            ),
        ],
        senses=[
            SenseDTO(
                pos=["n"],
                glosses=[GlossDTO(text="WinRAR (file archival software)", lang="eng")],
            )
        ],
    ),
]


@pytest.fixture
def sample_entries_xml():
    parser = ET.XMLParser(load_dtd=True, resolve_entities=True)
    tree = ET.parse(DATA_DIR / "jmdicte_samples.xml", parser=parser)
    root = tree.getroot()
    return list(root.findall("entry"))


def test_correctly_parse_sample_entry(sample_entries_xml):
    entries = []
    for entry_element in sample_entries_xml:
        entry = parse_entry(entry_element)
        entries.append(entry)

    assert entries == EXPECTED_PARSED_ENTRIES


# def test_successfully_parse_jmdict_file():
#     entries = parse_jmdict_file()
#     assert len(entries) == 213906
