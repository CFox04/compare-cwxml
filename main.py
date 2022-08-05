from pathlib import Path
from typing import Callable

from cwxml.element import Element
from cwxml.fragment import Fragment
from cwxml.drawable import Drawable, DrawableDictionary
from cwxml.bound import YBN
from cwxml.clipsdictionary import Clip
from cwxml.ymap import CMapData
from cwxml.ytyp import CMapTypes

from config import Config
from comparison import ComparisonResult


def compare_and_write(compare_func: Callable[[Element, Element], ComparisonResult]):
    """
    Compare files using the given compare function and write to output.\n
    :param compare_func: A function handle of the form
        ``compare_func(xml_a: Element, xml_b: Element) -> ComparionsResult``
    """
    Config.apply_args()

    ext_a = get_file_extension(Config.file_path_a)
    ext_b = get_file_extension(Config.file_path_b)

    if ext_a != ext_b:
        print("File types do not match!")
        quit()

    print("Loading XMLs...")
    xmls = load_xmls()
    print("Done loading XMLs.")

    print("Writing markdown file...")
    write_markdown(compare_func(*xmls))
    print("Done writing markdown.")


def load_xmls() -> tuple[Element, Element]:
    """Create xml_a and xml_b."""
    xml_type = get_cwxml_type(Config.file_path_a)
    xml_a = xml_type().from_xml_file(Config.file_path_a)
    xml_b = xml_type().from_xml_file(Config.file_path_b)

    return xml_a, xml_b


def write_markdown(result: ComparisonResult):
    """Write differences and similarities to the markdown file."""
    with open(Config.get_output_path(), mode="w") as file:
        file.write(
            f"<p>Found <span style='color: red'>{len(result.differences)}</span> differences and <span style='color: green'>{len(result.similarities)}</span> similarities.\n")

        for difference in result.differences:
            file.write("<h4 style='color: red'>Difference</h4>\n")
            file.write(difference.text())

        if Config.show_similarities:
            for similarity in result.similarities:
                file.write("<h4 style='color: green'>Similarity</h4>\n")
                file.write(similarity.text())

    print("Done writing markdown file.")


def get_file_extension(path: str):
    return "".join(Path(path).suffixes)


def get_cwxml_type(path: str):
    """Get CWXML type from path."""
    ext = get_file_extension(path)

    if ext == ".ybn.xml":
        return YBN
    elif ext == ".ydr.xml":
        return Drawable
    elif ext == ".ydd.xml":
        return DrawableDictionary
    elif ext == ".yft.xml":
        return Fragment
    elif ext == ".ycd.xml":
        return Clip
    elif ext == ".ymap.xml":
        return CMapData
    elif ext == ".ytyp.xml":
        return CMapTypes

    return Element
