from pathlib import Path


def get_jmdict_path() -> Path:
    return Path(__file__).resolve().parents[4] / "resources" / "JMdict_e"
