from wisho.repositories.word import WordRepository


class SearchController:
    def __init__(self, word_repository: WordRepository) -> None:
        self.word_repository = word_repository

    async def search(self, query: str, limit: int = 20) -> list:
        ranked_rows = await self.word_repository.rank_word_ids_for_query(query, limit)
        word_ids = [row["word_id"] for row in ranked_rows]
        if not word_ids:
            return []

        score_by_id = {row["word_id"]: float(row["score"]) for row in ranked_rows}
        details_by_id = await self.word_repository.get_word_details_by_ids(word_ids)

        results = []
        for wid in word_ids:
            details = details_by_id.get(wid, {"readings": [], "kanji": [], "glosses": []})
            results.append(
                {
                    "id": wid,
                    "kanjis": details.get("kanji", []),
                    "readings": details.get("readings", []),
                    "glosses": details.get("glosses", []),
                    "score": score_by_id.get(wid, 0.0),
                }
            )

        return results
