from edict.schemas.jmdict import (
    Gloss,
    Kanji,
    MiscInformation,
    PartOfSpeech,
    Reading,
    Sense,
    SenseExample,
    SubjectField,
    Word,
)

PARSED_SAMPLES = [
    Word(
        id=1005390,
        kanjis=[],
        readings=[Reading(text="ざっと", is_common=True, tags=[], applies_to_kanji=["*"])],
        senses=[
            Sense(
                part_of_speech=[PartOfSpeech.ADVERB],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[],
                dialects=[],
                misc=[MiscInformation.ONOMATOPOEIA],
                infos=[],
                examples=[
                    SenseExample(
                        source="tatoeba",
                        text="ざっと",
                        jpn="私はパンフレットにざっと目をとおした。",
                        eng="I glanced through the brochure.",
                    )
                ],
                glosses=[
                    Gloss(type=None, text="roughly"),
                    Gloss(type=None, text="approximately"),
                    Gloss(type=None, text="round about"),
                    Gloss(type=None, text="more or less"),
                ],
            ),
            Sense(
                part_of_speech=[PartOfSpeech.ADVERB],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[],
                dialects=[],
                misc=[MiscInformation.ONOMATOPOEIA],
                infos=[],
                examples=[],
                glosses=[
                    Gloss(type=None, text="cursorily"),
                    Gloss(type=None, text="briefly"),
                    Gloss(type=None, text="quickly"),
                    Gloss(type=None, text="lightly"),
                    Gloss(type=None, text="roughly"),
                ],
            ),
        ],
    ),
    Word(
        id=1191730,
        kanjis=[Kanji(text="家", is_common=True, tags=[])],
        readings=[Reading(text="いえ", is_common=True, tags=[], applies_to_kanji=["*"])],
        senses=[
            Sense(
                part_of_speech=[PartOfSpeech.NOUN],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[],
                dialects=[],
                misc=[],
                infos=[],
                examples=[
                    SenseExample(
                        source="tatoeba", text="家", jpn="木立の間に家が見える。", eng="I see a house among the trees."
                    )
                ],
                glosses=[
                    Gloss(type=None, text="house"),
                    Gloss(type=None, text="residence"),
                    Gloss(type=None, text="dwelling"),
                    Gloss(type=None, text="home"),
                ],
            ),
            Sense(
                part_of_speech=[PartOfSpeech.NOUN],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[],
                dialects=[],
                misc=[],
                infos=[],
                examples=[
                    SenseExample(
                        source="tatoeba",
                        text="家",
                        jpn="あの家の繁栄は大戦中からのことだ。",
                        eng="The prosperity of the family dates from the Great War.",
                    )
                ],
                glosses=[Gloss(type=None, text="family"), Gloss(type=None, text="household")],
            ),
            Sense(
                part_of_speech=[PartOfSpeech.NOUN],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[],
                dialects=[],
                misc=[],
                infos=[],
                examples=[],
                glosses=[Gloss(type=None, text="lineage"), Gloss(type=None, text="family name")],
            ),
        ],
    ),
    Word(
        id=1261570,
        kanjis=[Kanji(text="原子", is_common=True, tags=[])],
        readings=[Reading(text="げんし", is_common=True, tags=[], applies_to_kanji=["*"])],
        senses=[
            Sense(
                part_of_speech=[PartOfSpeech.NOUN],
                applies_to_kanji=["*"],
                applies_to_reading=["*"],
                fields=[SubjectField.PHYSICS, SubjectField.CHEMISTRY],
                dialects=[],
                misc=[],
                infos=[],
                examples=[
                    SenseExample(
                        source="tatoeba",
                        text="原子",
                        jpn="鉄の原子番号は26です。",
                        eng="The atomic number of iron is 26.",
                    )
                ],
                glosses=[Gloss(type=None, text="atom")],
            )
        ],
    ),
]


def test_correctly_parses_words(sample_entries: list[dict]) -> None:
    words = [Word.from_json(entry) for entry in sample_entries]
    assert words == PARSED_SAMPLES
