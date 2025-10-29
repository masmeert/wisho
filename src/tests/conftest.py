from unittest.mock import MagicMock

import pytest

from wisho.models.entry import Entry


@pytest.fixture
def sample_entry() -> Entry:
    entry = MagicMock(spec=Entry)
    entry.id = 1206730
    entry.kanji_forms = [
        {"text": "学校", "priorities": ["ichi1", "news1", "nf01"]},
        {"text": "學校", "priorities": []},
    ]
    entry.readings = [{"text": "がっこう", "priorities": ["ichi1", "news1", "nf01"], "no_kanji": False}]
    entry.senses = [{"pos": ["n"], "glosses": [{"text": "school", "lang": "eng"}]}]
    return entry


@pytest.fixture
def sample_multiple_entries() -> list[Entry]:
    entries = []

    entry1 = MagicMock(spec=Entry)
    entry1.id = 1206730
    entry1.kanji_forms = [{"text": "学校", "priorities": ["ichi1", "news1", "nf01"]}]
    entry1.readings = [{"text": "がっこう", "priorities": ["ichi1", "news1", "nf01"], "no_kanji": False}]
    entry1.senses = [{"pos": ["n"], "glosses": [{"text": "school", "lang": "eng"}]}]
    entries.append(entry1)

    entry2 = MagicMock(spec=Entry)
    entry2.id = 1000300
    entry2.kanji_forms = [{"text": "遇う", "priorities": []}, {"text": "配う", "priorities": []}]
    entry2.readings = [{"text": "あしらう", "priorities": [], "no_kanji": False}]
    entry2.senses = [
        {
            "pos": ["v5u", "vt"],
            "glosses": [
                {"text": "to treat", "lang": "eng"},
                {"text": "to handle", "lang": "eng"},
                {"text": "to deal with", "lang": "eng"},
            ],
        }
    ]
    entries.append(entry2)

    return entries
