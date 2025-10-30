from pathlib import Path

import pytest
from edict.core.helpers import load_json_file

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def sample_entries() -> list[dict]:
    file_path = DATA_DIR / "jmdict_samples.json"
    json = load_json_file(file_path)
    return json["samples"]
