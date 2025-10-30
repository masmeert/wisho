from collections.abc import Sequence
from typing import Any

from sqlalchemy import (
    Float,
    Integer,
    RowMapping,
    Select,
    String,
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
    """
    Central search logic for Wisho dictionary entries.

    Ranks Japanese (prefix-based) and English (full-text) searches

    Weight Strategy:
    - Base weights (5.0): Reward prefix matches in readings/kanji
    - Exact match bonus (6.0): Prioritize perfect matches
    - Length penalty (2.0): Favor shorter forms
    - Common bonus (1.0): Slightly boost common dictionary entries
    - Single-char adjustments: Prevent compounds from dominating standalone entries
    """

    # JP weights
    READING_WEIGHT = 5.0
    KANJI_WEIGHT = 5.0
    EXACT_READING_WEIGHT = 6.0
    EXACT_KANJI_WEIGHT = 6.0
    LENGTH_WEIGHT = 2.0
    COMMON_WEIGHT = 1.0

    # English weights
    GLOSS_WEIGHT = 2.0
    EXACT_WORD_WEIGHT = 1.5

    # Result limits
    QUERY_LIMIT = 20
    CANDIDATES_LIMIT = 200

    # Single-char multipliers
    SINGLE_CHAR_BASE_MULT = 0.5
    SINGLE_CHAR_EXACT_MULT = 1.75
    SINGLE_CHAR_LENGTH_MULT = 1.25

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _adjust_weight_for_single_char_query(
        self, base_weight: float, *, for_exact_match: bool
    ) -> ColumnElement[float]:
        q = bindparam("q_norm")
        is_single_char = func.char_length(q) == 1
        multiplier = self.SINGLE_CHAR_EXACT_MULT if for_exact_match else self.SINGLE_CHAR_BASE_MULT
        return literal(base_weight) * case((is_single_char, literal(multiplier)), else_=literal(1.0))

    def _calculate_length_score_bonus(self, min_length_column: ColumnElement[int]) -> ColumnElement[float]:
        q = bindparam("q_norm")
        is_single_char = func.char_length(q) == 1
        effective_weight = literal(self.LENGTH_WEIGHT) * case(
            (is_single_char, literal(self.SINGLE_CHAR_LENGTH_MULT)), else_=literal(1.0)
        )
        return effective_weight * (literal(1.0) / (literal(1.0) + cast(min_length_column, Float)))

    def _create_prefix_match_stats(
        self, model: type[Reading] | type[Kanji], query_param: str
    ) -> Select[tuple[int, int, int, int]]:
        q = bindparam(query_param)
        prefix_pattern = func.concat(q, literal("%"))
        return (
            select(
                model.word_id.label("word_id"),
                func.min(func.char_length(model.text)).label("min_len"),
                func.max(case((model.text == q, literal(1)), else_=literal(0))).label("is_exact"),
                func.max(case((model.is_common.is_(True), literal(1)), else_=literal(0))).label("any_common"),
            )
            .where(model.text.ilike(prefix_pattern))
            .group_by(model.word_id)
        )

    def _calculate_weighted_score(
        self, stats_cte: Any, base_weight: float, exact_weight: float
    ) -> ColumnElement[float]:
        base_score = self._adjust_weight_for_single_char_query(base_weight, for_exact_match=False)
        exact_bonus = self._adjust_weight_for_single_char_query(exact_weight, for_exact_match=True)
        exact_match_score = case((stats_cte.c.is_exact == 1, exact_bonus), else_=literal(0.0))
        length_bonus = self._calculate_length_score_bonus(stats_cte.c.min_len)
        return base_score + exact_match_score + length_bonus

    def _build_japanese_prefix_search_query(self) -> Select[tuple[int, float]]:
        reading_stats = self._create_prefix_match_stats(Reading, "q_norm").cte("reading_stats")
        reading_score = self._calculate_weighted_score(reading_stats, self.READING_WEIGHT, self.EXACT_READING_WEIGHT)
        reading_hits = select(
            reading_stats.c.word_id,
            reading_score.label("branch_score"),
            reading_stats.c.any_common,
        ).cte("reading_hits")

        kanji_stats = self._create_prefix_match_stats(Kanji, "q_norm").cte("kanji_stats")
        kanji_score = self._calculate_weighted_score(kanji_stats, self.KANJI_WEIGHT, self.EXACT_KANJI_WEIGHT)
        kanji_hits = select(
            kanji_stats.c.word_id,
            kanji_score.label("branch_score"),
            kanji_stats.c.any_common,
        ).cte("kanji_hits")

        all_hits = union_all(
            select(reading_hits.c.word_id, reading_hits.c.branch_score, reading_hits.c.any_common),
            select(kanji_hits.c.word_id, kanji_hits.c.branch_score, kanji_hits.c.any_common),
        ).cte("all_hits")

        scored = (
            select(
                all_hits.c.word_id,
                func.sum(all_hits.c.branch_score).label("base_score"),
                func.max(all_hits.c.any_common).label("has_common"),
            )
            .group_by(all_hits.c.word_id)
            .cte("scored")
        )

        final_score = scored.c.base_score + case(
            (scored.c.has_common == 1, literal(self.COMMON_WEIGHT)), else_=literal(0.0)
        )

        return select(scored.c.word_id, final_score.label("score")).order_by(final_score.desc()).limit(self.QUERY_LIMIT)

    def _check_word_has_common_forms(self) -> Select[tuple[int, int]]:
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
        )

    def _build_english_fulltext_search_query(self) -> Select[tuple[int, float]]:
        cfg = cast(literal("english"), REGCONFIG)
        q_raw = bindparam("q_raw")

        gloss_vector = func.to_tsvector(cfg, func.coalesce(Gloss.text, literal("", String())))
        fts_query = func.plainto_tsquery(cfg, q_raw)
        norm_flags = literal(1 | 16 | 32)
        rank = func.ts_rank_cd(gloss_vector, fts_query, norm_flags)

        exact_pattern = func.concat(literal(r"\y"), q_raw, literal(r"\y"))
        exact_hit = cast(Gloss.text.op("~*")(exact_pattern), Integer)

        gloss_scores = (
            select(
                Sense.word_id.label("word_id"),
                func.max(rank).label("rank_max"),
                func.max(exact_hit).label("exact_any"),
            )
            .select_from(Gloss)
            .join(Sense, Sense.id == Gloss.sense_id)
            .where(gloss_vector.op("@@")(fts_query))
            .group_by(Sense.word_id)
            .cte("gloss_scores")
        )

        any_common = self._check_word_has_common_forms().cte("any_common")
        final_score = (
            literal(self.GLOSS_WEIGHT) * gloss_scores.c.rank_max
            + literal(self.EXACT_WORD_WEIGHT) * cast(gloss_scores.c.exact_any, Integer)
            + literal(self.COMMON_WEIGHT) * cast(func.coalesce(any_common.c.any_common, 0), Integer)
        )

        return (
            select(gloss_scores.c.word_id, final_score.label("score"))
            .join(any_common, any_common.c.word_id == gloss_scores.c.word_id, isouter=True)
            .order_by(final_score.desc())
            .limit(self.QUERY_LIMIT)
        )

    async def search_and_score_words(self, query: str, limit: int = 20) -> Sequence[RowMapping]:
        normalized_query = nfkc(query)

        if is_japanese_text(normalized_query):
            stmt = self._build_japanese_prefix_search_query().limit(limit)
            params = {"q_norm": normalized_query}
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
            select(
                Reading.word_id,
                func.array_agg(func.distinct(Reading.text)).label("readings"),
            )
            .where(Reading.word_id.in_(word_ids))
            .group_by(Reading.word_id)
        )
        readings_by_id = {r.word_id: r.readings for r in rd}

        kj = await self.session.execute(
            select(
                Kanji.word_id,
                func.array_agg(func.distinct(Kanji.text)).label("kanjis"),
            )
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
