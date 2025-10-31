from collections.abc import Sequence

from sqlalchemy import (
    Float,
    Integer,
    RowMapping,
    Select,
    String,
    Subquery,
    bindparam,
    case,
    cast,
    func,
    literal,
    select,
    union_all,
)
from sqlalchemy.dialects.postgresql import REGCONFIG
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from wisho.core.helpers import is_japanese_text, nfkc
from wisho.models.jmdict import Gloss, Kanji, Reading, Sense


class WordRepository:
    # JP weights
    READING_WEIGHT = 5.0
    KANJI_WEIGHT = 5.0
    EXACT_READING_WEIGHT = 6.0
    EXACT_KANJI_WEIGHT = 6.0
    LENGTH_WEIGHT = 2.0
    COMMON_WEIGHT = 1.0

    # EN weights
    GLOSS_WEIGHT = 2.0
    EXACT_WORD_WEIGHT = 1.5

    # Limits
    QUERY_LIMIT = 20

    # Single-char multipliers
    SINGLE_CHAR_BASE_MULT = 0.5
    SINGLE_CHAR_EXACT_MULT = 1.75
    SINGLE_CHAR_LENGTH_MULT = 1.25

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _is_single_char(q_param: str) -> ColumnElement[bool]:
        q = bindparam(q_param)
        return func.char_length(q) == 1

    def _length_bonus(self, min_len_col: ColumnElement[int], q_param: str) -> ColumnElement[float]:
        w = literal(self.LENGTH_WEIGHT) * case(
            (self._is_single_char(q_param), literal(self.SINGLE_CHAR_LENGTH_MULT)), else_=literal(1.0)
        )
        return w * (literal(1.0) / (literal(1.0) + cast(min_len_col, Float)))

    def _jp_prefix_stats(self, model: type[Reading] | type[Kanji], q_param: str) -> Subquery:
        q = bindparam(q_param)
        prefix = func.concat(q, literal("%"))
        return (
            select(
                model.word_id.label("word_id"),
                func.min(func.char_length(model.text)).label("min_len"),
                func.max(case((model.text == q, literal(1)), else_=literal(0))).label("is_exact"),
                func.max(case((model.is_common.is_(True), literal(1)), else_=literal(0))).label("any_common"),
            )
            .where(model.text.ilike(prefix))
            .group_by(model.word_id)
        ).subquery()

    def _jp_branch(self, model: type[Reading] | type[Kanji], *, q_param: str, base_w: float, exact_w: float) -> Select:
        s = self._jp_prefix_stats(model, q_param)
        base = literal(base_w) * case(
            (self._is_single_char(q_param), literal(self.SINGLE_CHAR_BASE_MULT)), else_=literal(1.0)
        )
        exact = case(
            (
                s.c.is_exact == 1,
                literal(exact_w)
                * case((self._is_single_char(q_param), literal(self.SINGLE_CHAR_EXACT_MULT)), else_=literal(1.0)),
            ),
            else_=literal(0.0),
        )
        score = base + exact + self._length_bonus(s.c.min_len, q_param)
        return select(s.c.word_id, score.label("branch_score"), s.c.any_common)

    def _build_japanese_prefix_search_query(self) -> Select:
        reading = self._jp_branch(
            Reading, q_param="q_norm", base_w=self.READING_WEIGHT, exact_w=self.EXACT_READING_WEIGHT
        )
        kanji = self._jp_branch(Kanji, q_param="q_norm", base_w=self.KANJI_WEIGHT, exact_w=self.EXACT_KANJI_WEIGHT)

        all_hits = union_all(
            select(reading.c.word_id, reading.c.branch_score, reading.c.any_common),
            select(kanji.c.word_id, kanji.c.branch_score, kanji.c.any_common),
        ).subquery()

        scored = (
            select(
                all_hits.c.word_id,
                func.sum(all_hits.c.branch_score).label("base_score"),
                func.max(all_hits.c.any_common).label("has_common"),
            ).group_by(all_hits.c.word_id)
        ).subquery()

        final_score = scored.c.base_score + case(
            (scored.c.has_common == 1, literal(self.COMMON_WEIGHT)), else_=literal(0.0)
        )

        return select(scored.c.word_id, final_score.label("score")).order_by(final_score.desc()).limit(self.QUERY_LIMIT)

    def _any_common_subq(self) -> Subquery:
        return (
            select(
                Sense.word_id.label("word_id"),
                func.greatest(
                    func.coalesce(
                        func.max(cast(Reading.is_common, Integer)).filter(Reading.word_id == Sense.word_id), 0
                    ),
                    func.coalesce(func.max(cast(Kanji.is_common, Integer)).filter(Kanji.word_id == Sense.word_id), 0),
                ).label("any_common"),
            )
            .select_from(Sense)
            .join(Reading, Reading.word_id == Sense.word_id, isouter=True)
            .join(Kanji, Kanji.word_id == Sense.word_id, isouter=True)
            .group_by(Sense.word_id)
        ).subquery()

    def _build_english_fulltext_search_query(self) -> Select:
        cfg = cast(literal("english"), REGCONFIG)
        q_raw = bindparam("q_raw")

        gloss_vector = func.to_tsvector(cfg, func.coalesce(Gloss.text, literal("", String())))
        fts_query = func.plainto_tsquery(cfg, q_raw)
        rank = func.ts_rank_cd(gloss_vector, fts_query, literal(1 | 16 | 32))

        exact_pattern = func.concat(literal(r"\y"), q_raw, literal(r"\y"))
        exact_hit = cast(Gloss.text.op("~*")(exact_pattern), Integer)

        scores = (
            select(
                Sense.word_id.label("word_id"),
                func.max(rank).label("rank_max"),
                func.max(exact_hit).label("exact_any"),
            )
            .select_from(Gloss)
            .join(Sense, Sense.id == Gloss.sense_id)
            .where(gloss_vector.op("@@")(fts_query))
            .group_by(Sense.word_id)
        ).subquery()

        any_common = self._any_common_subq()

        final = (
            literal(self.GLOSS_WEIGHT) * scores.c.rank_max
            + literal(self.EXACT_WORD_WEIGHT) * cast(scores.c.exact_any, Integer)
            + literal(self.COMMON_WEIGHT) * cast(func.coalesce(any_common.c.any_common, 0), Integer)
        )

        return (
            select(scores.c.word_id, final.label("score"))
            .join(any_common, any_common.c.word_id == scores.c.word_id, isouter=True)
            .order_by(final.desc())
            .limit(self.QUERY_LIMIT)
        )

    async def search_and_score_words(self, query: str, limit: int = 20) -> Sequence[RowMapping]:
        q_norm = nfkc(query)
        if is_japanese_text(q_norm):
            stmt = self._build_japanese_prefix_search_query().limit(limit)
            params = {"q_norm": q_norm}
        else:
            stmt = self._build_english_fulltext_search_query().limit(limit)
            params = {"q_raw": query}
        result = await self.session.execute(stmt, params)
        return result.mappings().all()

    async def fetch_word_details(
        self, word_ids: Sequence[int], max_glosses: int = 3
    ) -> tuple[dict[int, list[str]], dict[int, list[str]], dict[int, list[str]]]:
        if not word_ids:
            return {}, {}, {}

        rd = await self.session.execute(
            select(Reading.word_id, func.array_agg(func.distinct(Reading.text)).label("readings"))
            .where(Reading.word_id.in_(word_ids))
            .group_by(Reading.word_id)
        )
        readings_by_id = {r.word_id: r.readings for r in rd}

        kj = await self.session.execute(
            select(Kanji.word_id, func.array_agg(func.distinct(Kanji.text)).label("kanjis"))
            .where(Kanji.word_id.in_(word_ids))
            .group_by(Kanji.word_id)
        )
        kanji_by_id = {k.word_id: k.kanjis for k in kj}

        gl = await self.session.execute(
            select(Sense.word_id, Gloss.text)
            .join(Gloss, Gloss.sense_id == Sense.id)
            .where(Sense.word_id.in_(word_ids))
            .limit(len(word_ids) * max_glosses * 2)
        )
        glosses_by_id: dict[int, list[str]] = {}
        for row in gl:
            bucket = glosses_by_id.setdefault(row.word_id, [])
            if len(bucket) < max_glosses:
                bucket.append(row.text)

        return readings_by_id, kanji_by_id, glosses_by_id
