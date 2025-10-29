class InvalidEntitySequenceError(Exception):
    def __init__(self) -> None:
        super().__init__("JMdict entry must contain a valid integer entity sequence")
