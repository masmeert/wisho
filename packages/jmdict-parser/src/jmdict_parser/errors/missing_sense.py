class MissingSenseError(Exception):
    def __init__(self) -> None:
        super().__init__("Entry must have at least one sense")
