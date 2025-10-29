from lxml import etree

XML_LANGUAGE_NAMESPACE = "{http://www.w3.org/XML/1998/namespace}lang"


def get_children_texts(parent: etree._Element, tag: str) -> list[str]:
    """
    Return the stripped text content of all child elements named `tag` under `parent`.
    Skips empty or whitespace-only text.
    """
    return [node.text.strip() for node in parent.iterfind(tag) if node.text and node.text.strip()]


def get_first_child_text(parent: etree._Element, tag: str) -> str | None:
    """
    Return the stripped text of the first child named `tag`, or None if missing/empty.
    """
    if (node := parent.find(tag)) is None or node.text is None:
        return None
    text = node.text.strip()
    return text if text else None


def get_language_attribute(element: etree._Element) -> str:
    """
    Extract the language attribute from an element, checking both standard and XML namespace versions.
    """
    return element.get("lang") or element.get(XML_LANGUAGE_NAMESPACE) or "eng"
