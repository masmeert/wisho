from pathlib import Path

from lxml import etree

from jmdict_parser.parsing.entry import parse_entry
from jmdict_parser.schemas import Entry

PATH = Path(__file__).resolve().parents[2] / "resources" / "JMdict_e"


def parse_jmdict_file() -> list[Entry]:
    """
    Parse the JMdict_e XML file and return a list of EntryDTOs.
    """
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True, huge_tree=True)
    tree = etree.parse(PATH, parser=parser)
    root = tree.getroot()

    entries: list[Entry] = []
    for jmdict_entry in root.iterfind("entry"):
        entry_dto = parse_entry(jmdict_entry)
        entries.append(entry_dto)

    return entries
