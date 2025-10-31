from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

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

from wisho.core.helpers import is_japanese_text, nfkc
from wisho.models.jmdict import Gloss, Kanji, Reading, Sense

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.elements import ColumnElement


@dataclass(frozen=True)
class SearchWeights:
    """All tunable weights for ranking."""

    # Japanese weights
    reading_weight = 5.0
    kanji_weight = 5.0
    exact_reading_weight = 6.0
    exact_kanji_weight = 6.0
    length_weight = 2.0
    common_weight = 1.0

    # English weights
    gloss_weight = 2.0
    exact_word_weight = 1.5

    # Single-character multipliers
    single_char_base_mult = 0.5
    single_char_exact_mult = 1.75
    single_char_length_mult = 1.25


class WordDetails(TypedDict):
    readings: list[str]
    kanji: list[str]
    glosses: list[str]


class WordRepository:
    DEFAULT_LIMIT = 20

    def __init__(self, session: AsyncSession, weights: SearchWeights | None = None) -> None:
        self.session = session
        self.weights = weights or SearchWeights()

    @staticmethod
    def _param_is_single_char(param_name: str) -> ColumnElement[bool]:
        q = bindparam(param_name)
        return func.char_length(q) == 1

    def _length_decay_bonus(
        self,
        min_len_col: ColumnElement[int],
        param_name: str,
    ) -> ColumnElement[float]:
        """
        Reward shorter matches a bit more: weight * 1/(1+min_len).
        Boost slightly when the query is a single character.
        """
        w = literal(self.weights.length_weight) * case(
            (self._param_is_single_char(param_name), literal(self.weights.single_char_length_mult)),
            else_=literal(1.0),
        )
        # 1 / (1 + len) stays bounded and gently favors shorter forms
        return w * (literal(1.0) / (literal(1.0) + cast(min_len_col, Float)))

    def _prefix_match_stats_for(
        self,
        model: type[Reading] | type[Kanji],
        *,
        param_name: str,
    ) -> Subquery:
        """
        For a prefix query against `model.text`, return per-word:
        - min_len: the shortest matched form length
        - is_exact: whether any form exactly equals the query
        - any_common: whether any form is flagged common
        """
        q = bindparam(param_name)
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

    def _score_prefix_branch_for(
        self,
        model: type[Reading] | type[Kanji],
        *,
        param_name: str,
        base_weight: float,
        exact_weight: float,
    ) -> Select:
        """
        Score a prefix branch (readings or kanji):
        base + exact_match_bonus + length_bonus.
        """
        s = self._prefix_match_stats_for(model, param_name=param_name)

        base = literal(base_weight) * case(
            (self._param_is_single_char(param_name), literal(self.weights.single_char_base_mult)),
            else_=literal(1.0),
        )

        exact = case(
            (
                s.c.is_exact == 1,
                literal(exact_weight)
                * case(
                    (self._param_is_single_char(param_name), literal(self.weights.single_char_exact_mult)),
                    else_=literal(1.0),
                ),
            ),
            else_=literal(0.0),
        )

        score = base + exact + self._length_decay_bonus(s.c.min_len, param_name)
        return select(s.c.word_id, score.label("branch_score"), s.c.any_common)

    def _build_japanese_prefix_ranking_query(self) -> Select:
        """
        Rank by prefix matches across readings and kanji, with per-word aggregation.
        """
        reading_branch = self._score_prefix_branch_for(
            Reading,
            param_name="q_norm",
            base_weight=self.weights.reading_weight,
            exact_weight=self.weights.exact_reading_weight,
        )
        kanji_branch = self._score_prefix_branch_for(
            Kanji,
            param_name="q_norm",
            base_weight=self.weights.kanji_weight,
            exact_weight=self.weights.exact_kanji_weight,
        )

        all_hits = union_all(
            select(reading_branch.c.word_id, reading_branch.c.branch_score, reading_branch.c.any_common),
            select(kanji_branch.c.word_id, kanji_branch.c.branch_score, kanji_branch.c.any_common),
        ).subquery()

        per_word = (
            select(
                all_hits.c.word_id,
                func.sum(all_hits.c.branch_score).label("base_score"),
                func.max(all_hits.c.any_common).label("has_common"),
            ).group_by(all_hits.c.word_id)
        ).subquery()

        final_score = per_word.c.base_score + case(
            (per_word.c.has_common == 1, literal(self.weights.common_weight)),
            else_=literal(0.0),
        )

        return select(per_word.c.word_id, final_score.label("score")).order_by(final_score.desc())

    def _any_common_flag_by_word_subq(self) -> Subquery:
        """
        Whether any reading/kanji for a word is marked common (1/0).
        """
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

    def _build_english_gloss_fulltext_ranking_query(self) -> Select:
        """
        Rank by Postgres full-text match on glosses (plainto_tsquery),
        factoring in exact whole-word hits and 'common' flag.
        """
        cfg = cast(literal("english"), REGCONFIG)
        q_raw = bindparam("q_raw")

        gloss_vector = func.to_tsvector(cfg, func.coalesce(Gloss.text, literal("", String())))
        fts_query = func.plainto_tsquery(cfg, q_raw)

        rank = func.ts_rank_cd(gloss_vector, fts_query, literal(1 | 16 | 32))

        exact_pattern = func.concat(literal(r"\y"), q_raw, literal(r"\y"))
        exact_whole_word = cast(Gloss.text.op("~*")(exact_pattern), Integer)

        per_word_scores = (
            select(
                Sense.word_id.label("word_id"),
                func.max(rank).label("rank_max"),
                func.max(exact_whole_word).label("exact_any"),
            )
            .select_from(Gloss)
            .join(Sense, Sense.id == Gloss.sense_id)
            .where(gloss_vector.op("@@")(fts_query))
            .group_by(Sense.word_id)
        ).subquery()

        any_common = self._any_common_flag_by_word_subq()

        final = (
            literal(self.weights.gloss_weight) * per_word_scores.c.rank_max
            + literal(self.weights.exact_word_weight) * cast(per_word_scores.c.exact_any, Integer)
            + literal(self.weights.common_weight) * cast(func.coalesce(any_common.c.any_common, 0), Integer)
        )

        return (
            select(per_word_scores.c.word_id, final.label("score"))
            .join(any_common, any_common.c.word_id == per_word_scores.c.word_id, isouter=True)
            .order_by(final.desc())
        )

    async def rank_word_ids_for_query(self, query: str, limit: int = DEFAULT_LIMIT) -> Sequence[RowMapping]:
        query_norm = nfkc(query)
        if is_japanese_text(query_norm):
            stmt = self._build_japanese_prefix_ranking_query().limit(limit)
            params = {"q_norm": query_norm}
        else:
            stmt = self._build_english_gloss_fulltext_ranking_query().limit(limit)
            params = {"q_raw": query}
        result = await self.session.execute(stmt, params)
        return result.mappings().all()

    async def get_word_details_by_ids(
        self,
        word_ids: Sequence[int],
        max_glosses_per_word: int = 3,
    ) -> dict[int, WordDetails]:
        if not word_ids:
            return {}

        readings_rs = await self.session.execute(
            select(Reading.word_id, func.array_agg(func.distinct(Reading.text)).label("readings"))
            .where(Reading.word_id.in_(word_ids))
            .group_by(Reading.word_id)
        )
        readings_by_id = {row.word_id: row.readings for row in readings_rs}

        kanji_rs = await self.session.execute(
            select(Kanji.word_id, func.array_agg(func.distinct(Kanji.text)).label("kanji"))
            .where(Kanji.word_id.in_(word_ids))
            .group_by(Kanji.word_id)
        )
        kanji_by_id = {row.word_id: row.kanji for row in kanji_rs}

        gloss_rs = await self.session.execute(
            select(Sense.word_id, Gloss.text)
            .join(Gloss, Gloss.sense_id == Sense.id)
            .where(Sense.word_id.in_(word_ids))
            .limit(len(word_ids) * max_glosses_per_word * 2)
        )
        glosses_by_id: dict[int, list[str]] = {}
        for word_id, text in gloss_rs:
            bucket = glosses_by_id.setdefault(word_id, [])
            if len(bucket) < max_glosses_per_word:
                bucket.append(text)

        out: dict[int, WordDetails] = {}
        for wid in word_ids:
            out[wid] = WordDetails(
                readings=readings_by_id.get(wid, []),
                kanji=kanji_by_id.get(wid, []),
                glosses=glosses_by_id.get(wid, []),
            )
        return out
