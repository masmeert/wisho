from pathlib import Path

import pytest
from jmdict_parser.parsing.entry import parse_entry
from jmdict_parser.schemas import Entry, Gloss, Kanji, Reading, Sense
from lxml import etree

DATA_DIR = Path(__file__).parent / "data"

EXPECTED_PARSED_ENTRIES = [
    Entry(
        id=1206730,
        kanji_forms=[
            Kanji(text="学校", priorities=["ichi1", "news1", "nf01"]),
            Kanji(text="學校", priorities=[]),
        ],
        readings=[
            Reading(
                text="がっこう",
                priorities=["ichi1", "news1", "nf01"],
                no_kanji=False,
                restrictions=[],
            )
        ],
        senses=[
            Sense(
                pos=["n"],
                glosses=[Gloss(text="school", lang="eng")],
            )
        ],
    ),
    Entry(
        id=1000300,
        kanji_forms=[
            Kanji(text="遇う", priorities=[]),
            Kanji(text="配う", priorities=[]),
        ],
        readings=[
            Reading(
                text="あしらう",
                priorities=[],
                no_kanji=False,
                restrictions=[],
            ),
        ],
        senses=[
            Sense(
                pos=["v5u", "vt"],
                glosses=[
                    Gloss(text="to treat", lang="eng"),
                    Gloss(text="to handle", lang="eng"),
                    Gloss(text="to deal with", lang="eng"),
                ],
            ),
            Sense(
                pos=["v5u", "vt"],
                glosses=[
                    Gloss(text="to arrange", lang="eng"),
                    Gloss(text="to decorate (with)", lang="eng"),
                    Gloss(text="to adorn (with)", lang="eng"),
                    Gloss(text="to dress (with)", lang="eng"),
                    Gloss(text="to garnish (with)", lang="eng"),
                ],
            ),
        ],
    ),
    Entry(
        id=1000440,
        kanji_forms=[
            Kanji(text="あの人", priorities=["spec1"]),
            Kanji(text="彼の人", priorities=[]),
        ],
        readings=[
            Reading(
                text="あのひと",
                priorities=["spec1"],
                no_kanji=False,
                restrictions=[],
            ),
        ],
        senses=[
            Sense(
                pos=["pn"],
                glosses=[
                    Gloss(text="he", lang="eng"),
                    Gloss(text="she", lang="eng"),
                    Gloss(text="that person", lang="eng"),
                ],
            ),
            Sense(
                pos=["pn"],
                glosses=[
                    Gloss(text="you", lang="eng"),
                ],
            ),
        ],
    ),
    Entry(
        id=5746823,
        kanji_forms=[
            Kanji(text="ＷｉｎＲＡＲ", priorities=[]),  # noqa: RUF001
        ],
        readings=[
            Reading(
                text="ウィンアールエーアール",
                priorities=[],
                no_kanji=False,
                restrictions=[],
            ),
            Reading(text="ウィンラー", priorities=[], no_kanji=False, restrictions=[]),
        ],
        senses=[
            Sense(
                pos=["n"],
                glosses=[Gloss(text="WinRAR (file archival software)", lang="eng")],
            )
        ],
    ),
]


@pytest.fixture
def sample_entries_xml() -> list[etree._Element]:
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
    tree = etree.parse(DATA_DIR / "jmdicte_samples.xml", parser=parser)
    root = tree.getroot()
    return list(root.findall("entry"))


def test_correctly_parse_sample_entry(sample_entries_xml: list[etree._Element]) -> None:
    entries = []
    for entry_element in sample_entries_xml:
        entry = parse_entry(entry_element)
        entries.append(entry)

    assert entries == EXPECTED_PARSED_ENTRIES  # noqa: S101
