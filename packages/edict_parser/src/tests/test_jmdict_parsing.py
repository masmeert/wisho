from pathlib import Path

import pytest
from edict_parser.jmdict.parsing.entry import parse_jmdict_entry
from edict_parser.schemas.entry import Entry, EntryElement
from edict_parser.schemas.gloss import Gloss
from edict_parser.schemas.priority import Priority
from edict_parser.schemas.sense import Sense
from edict_parser.types.information import MiscellaneousInformation
from edict_parser.types.language import Language
from edict_parser.types.part_of_speech import PartOfSpeech
from edict_parser.types.priority import PriorityType
from lxml import etree

DATA_DIR = Path(__file__).parent / "data"

EXPECTED_PARSED_ENTRIES = [
    Entry(
        sequence=1206730,
        elements=[
            EntryElement(
                text="学校",
                is_kanji=True,
                priorities=[
                    Priority(priority_type=PriorityType.Ichi, level=1),
                    Priority(priority_type=PriorityType.News, level=1),
                    Priority(priority_type=PriorityType.Nf, level=1),
                ],
            ),
            EntryElement(text="學校", is_kanji=True, priorities=[]),
            EntryElement(
                text="がっこう",
                is_kanji=False,
                priorities=[
                    Priority(priority_type=PriorityType.Ichi, level=1),
                    Priority(priority_type=PriorityType.News, level=1),
                    Priority(priority_type=PriorityType.Nf, level=1),
                ],
            ),
        ],
        senses=[
            Sense(
                id=1,
                part_of_speech=[PartOfSpeech.N],
                glosses=[Gloss(text="school", language=Language.ENGLISH, gtype=None)],
            )
        ],
    ),
    Entry(
        sequence=1000300,
        elements=[
            EntryElement(text="遇う", is_kanji=True, priorities=[]),
            EntryElement(text="配う", is_kanji=True, priorities=[]),
            EntryElement(text="あしらう", is_kanji=False, priorities=[]),
        ],
        senses=[
            Sense(
                id=1,
                part_of_speech=[PartOfSpeech.V5U, PartOfSpeech.VT],
                glosses=[
                    Gloss(text="to treat", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to handle", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to deal with", language=Language.ENGLISH, gtype=None),
                ],
            ),
            Sense(
                id=2,
                part_of_speech=[PartOfSpeech.V5U, PartOfSpeech.VT],
                glosses=[
                    Gloss(text="to arrange", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to decorate (with)", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to adorn (with)", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to dress (with)", language=Language.ENGLISH, gtype=None),
                    Gloss(text="to garnish (with)", language=Language.ENGLISH, gtype=None),
                ],
            ),
        ],
    ),
    Entry(
        sequence=1000440,
        elements=[
            EntryElement(text="あの人", is_kanji=True, priorities=[Priority(priority_type=PriorityType.Spec, level=1)]),
            EntryElement(text="彼の人", is_kanji=True, priorities=[]),
            EntryElement(
                text="あのひと", is_kanji=False, priorities=[Priority(priority_type=PriorityType.Spec, level=1)]
            ),
        ],
        senses=[
            Sense(
                id=1,
                part_of_speech=[PartOfSpeech.PN],
                glosses=[
                    Gloss(text="he", language=Language.ENGLISH, gtype=None),
                    Gloss(text="she", language=Language.ENGLISH, gtype=None),
                    Gloss(text="that person", language=Language.ENGLISH, gtype=None),
                ],
                information="sometimes of one's spouse or partner",
            ),
            Sense(
                id=2,
                part_of_speech=[PartOfSpeech.PN],
                glosses=[
                    Gloss(text="you", language=Language.ENGLISH, gtype=None),
                ],
                misc=MiscellaneousInformation.ARCHAIC,
            ),
        ],
    ),
    Entry(
        sequence=5746823,
        elements=[
            EntryElement(text="ＷｉｎＲＡＲ", is_kanji=True, priorities=[]),  # noqa: RUF001
            EntryElement(text="ウィンアールエーアール", is_kanji=False, priorities=[]),
            EntryElement(text="ウィンラー", is_kanji=False, priorities=[]),
        ],
        senses=[
            Sense(
                id=1,
                part_of_speech=[PartOfSpeech.N],
                glosses=[Gloss(text="WinRAR (file archival software)", language=Language.ENGLISH, gtype=None)],
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
        entry = parse_jmdict_entry(entry_element)
        entries.append(entry)

    assert entries == EXPECTED_PARSED_ENTRIES  # noqa: S101
