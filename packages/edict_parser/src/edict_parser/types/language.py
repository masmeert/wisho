from enum import Enum


class Language(str, Enum):
    """Language codes for glosses - ISO 639-2 three-letter codes"""

    ENGLISH = "eng"
    GERMAN = "ger"
    FRENCH = "fre"
    RUSSIAN = "rus"
    DUTCH = "dut"


class Gairaigo(str, Enum):
    """Loanword source language"""

    ENGLISH = "en"
    GERMAN = "de"
    FRENCH = "fr"
    PORTUGUESE = "pt"
    DUTCH = "nl"
