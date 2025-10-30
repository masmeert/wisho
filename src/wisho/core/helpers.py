import re
import unicodedata

JR_CHAR_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]")


def nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text).strip()


def is_japanese_text(text: str) -> bool:
    return bool(JR_CHAR_RE.search(text))
