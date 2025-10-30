from wisho.repositories.word import WordRepository


class SearchController:
    def __init__(self, word_repository: WordRepository) -> None:
        self.word_repository = word_repository

    async def search(self, query: str, limit: int = 20) -> list:
        ranked = await self.word_repository.search_and_score_words(query, limit)
        word_ids = [row["word_id"] for row in ranked]
        if not word_ids:
            return []

        readings_map, kanji_map, gloss_map = await self.word_repository.fetch_word_details(word_ids)
        score_map = {row["word_id"]: float(row["score"]) for row in ranked}
        results = []
        for wid in word_ids:
            results.append(
                {
                    "id": wid,
                    "headwords": kanji_map.get(wid, []),
                    "readings": readings_map.get(wid, []),
                    "glosses": gloss_map.get(wid, []),
                    "score": score_map[wid],
                }
            )

        return results
