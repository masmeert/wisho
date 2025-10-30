from pydantic import BaseModel, Field

from edict.types.jmdict import Dialect, GlossType, MiscInformation, PartOfSpeech, SubjectField


class Kanji(BaseModel):
    """Orthographic form (kanji)."""

    text: str = Field(..., description="Kanji spelling")
    is_common: bool = Field(..., description="Marked as common in the source")
    tags: list[str] = Field(default_factory=list, description="Extra labels for this kanji")

    @classmethod
    def from_json(cls, json: dict) -> "Kanji":
        return cls(
            text=json["text"],
            is_common=json["common"],
            tags=json["tags"],
        )


class Reading(BaseModel):
    """Kana reading for an entry."""

    text: str = Field(..., description="Reading in kana")
    is_common: bool = Field(..., description="Marked as common in the source")
    tags: list[str] = Field(default_factory=list, description="Extra labels for this reading")
    applies_to_kanji: list[str] = Field(
        default_factory=list,
        description="Kanji spellings this reading applies to (empty = all)",
    )

    @classmethod
    def from_json(cls, json: dict) -> "Reading":
        return cls(
            text=json["text"],
            is_common=json["common"],
            tags=json["tags"],
            applies_to_kanji=json["appliesToKanji"],
        )


class SenseExample(BaseModel):
    """Example sentence pair illustrating a sense."""

    source: str = Field(..., description="Provenance of the example (tatoeba)")
    text: str = Field(..., description="Target form this example illustrates (kanji/reading)")

    jpn: str = Field(..., description="Japanese sentence")
    eng: str = Field(..., description="English translation")

    @classmethod
    def from_json(cls, json: dict) -> "SenseExample":
        def _get_sentence_by_lang(sentences: list[dict], lang: str) -> str:
            for item in sentences:
                if item["land"] == lang:
                    return item["text"]
            return ""

        sentences = json["sentences"]
        source = json["source"]["type"]
        return cls(
            source=source,
            text=json["text"],
            jpn=_get_sentence_by_lang(sentences, "jpn"),
            eng=_get_sentence_by_lang(sentences, "eng"),
        )


class Gloss(BaseModel):
    """A single definition/gloss string."""

    type: GlossType | None = Field(default=None, description="Semantic role of this gloss")
    text: str = Field(..., description="Definition text")

    @classmethod
    def from_json(cls, json: dict) -> "Gloss":
        gloss_type = json["type"]
        return cls(
            type=GlossType(gloss_type) if gloss_type else None,
            text=json["text"],
        )


class Sense(BaseModel):
    """A distinct meaning of the entry."""

    part_of_speech: list[PartOfSpeech] = Field(default_factory=list, description="POS tags for this sense")
    applies_to_kanji: list[str] = Field(default_factory=list, description="Kanji spellings this sense targets")
    applies_to_reading: list[str] = Field(default_factory=list, description="Readings this sense targets")
    fields: list[SubjectField] = Field(default_factory=list, description="Domain/subject labels")
    dialects: list[Dialect] = Field(default_factory=list, description="Dialectal labels")
    misc: list[MiscInformation] = Field(default_factory=list, description="Misc. usage/register flags")
    infos: list[str] = Field(default_factory=list, description="Free-form notes for this sense")

    examples: list[SenseExample] = Field(default_factory=list, description="Usage examples")
    glosses: list[Gloss] = Field(default_factory=list, description="Definitions for this sense")

    @classmethod
    def from_json(cls, json: dict) -> "Sense":
        return cls(
            part_of_speech=[PartOfSpeech(pos) for pos in json["partOfSpeech"]],
            applies_to_kanji=json["appliesToKanji"],
            applies_to_reading=json["appliesToKana"],
            fields=[SubjectField(field) for field in json["field"]],
            dialects=[Dialect(dialect) for dialect in json["dialect"]],
            misc=[MiscInformation(m) for m in json["misc"]],
            infos=json["info"],
            glosses=[Gloss.from_json(g) for g in json["gloss"]],
            examples=[SenseExample.from_json(e) for e in json["examples"]],
        )


class Word(BaseModel):
    """Complete dictionary entry."""

    id: int = Field(..., description="JMDict sequence ID")

    kanjis: list[Kanji] = Field(default_factory=list, description="Orthographic variants")
    readings: list[Reading] = Field(default_factory=list, description="Reading variants")
    senses: list[Sense] = Field(default_factory=list, description="List of senses (meanings)")

    @classmethod
    def from_json(cls, json: dict) -> "Word":
        return cls(
            id=json["id"],
            kanjis=[Kanji.from_json(k) for k in json["kanji"]],
            readings=[Reading.from_json(r) for r in json["kana"]],
            senses=[Sense.from_json(s) for s in json["sense"]],
        )
