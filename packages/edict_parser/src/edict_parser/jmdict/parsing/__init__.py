from pathlib import Path

from edict_parser.jmdict.parsing.entry import parse_jmdict_entry
from edict_parser.schemas.entry import Entry
from lxml import etree

JMDICT_PATH = Path(__file__).resolve().parents[3] / "resources" / "JMdict_e"


def parse_jmdict_file() -> list[Entry]:
    """Parse the JMdict file and return a list of Entry objects."""
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True, huge_tree=True)
    tree = etree.parse(JMDICT_PATH, parser=parser)
    root = tree.getroot()

    entries: list[Entry] = []
    for jmdict_entry in root.iterfind("entry"):
        entry_dto = parse_jmdict_entry(jmdict_entry)
        entries.append(entry_dto)

    return entries
