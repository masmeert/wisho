class UnknownPriorityTypeError(Exception):
    def __init__(self, priority_str: str) -> None:
        super().__init__(f"Unknown priority type in string: {priority_str}")
