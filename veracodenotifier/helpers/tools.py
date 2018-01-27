import xml.etree.ElementTree as ETree
from io import BytesIO


def parse_and_remove_xml_namespaces(xml_string):
    it = ETree.iterparse(BytesIO(xml_string))
    for _, el in it:
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
    return it.root


def diff(first, second, comparator):
    second = set(item.attrib[comparator] for item in second)
    return [item for item in first if item.attrib[comparator] not in second]
