class InvalidEntitySequenceError(Exception):
    def __init__(self) -> None:
        super().__init__("JMdict entry must contain a valid integer entity sequence")


class UnknownPriorityTypeError(Exception):
    def __init__(self, priority_str: str) -> None:
        super().__init__(f"Unknown priority type in string: {priority_str}")
