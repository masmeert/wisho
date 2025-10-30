from wisho.repositories.word import WordRepository


class SearchController:
    def __init__(self, word_repository: WordRepository) -> None:
        self.word_repository = word_repository
