"""a module to generate safs for mamluk pdfs
"""

from argparse import ArgumentParser
import csv
from os import _exit, makedirs, path
import re
from xml.etree import ElementTree
from xml.dom import minidom
from sys import stderr

from shutil import copyfile

__version__ = "0.0.1"
___author__ = "tdanstrom@uchicago.edu"

def _open_csv(a_string):
    data = []
    try:
        with open(a_string, "r", encoding="utf-8") as read_file:
            csv_data = csv.DictReader(read_file)
            for row in csv_data:
                data.append(row)
    except IOError:
        stderr.write("The metadata file is invalid for some reason.\n")
        raise SystemExit
    return data

def _define_qualifer_element(an_element, qualifier_value):
    """set attribute qualifier with defined value on an elementtree object
    """
    return _define_attribute_value(an_element, "qualifier", qualifier_value)

def _make_a_new_sub_element(map_data, text_value, current_record):
    """a function to create a new subelement of a dublin core root
    """
    element = make_dublincore_element(current_record)
    if isinstance(map_data, list):
        pass
    else:
        _define_element_attribute(element, map_data.get("element"))
        _define_qualifer_element(element, map_data.get("qualifier"))
        element.text = text_value.strip()
        return element

def make_dublincore_element(root):
    """a function to make a dublin core elementtree object
    """
    return ElementTree.SubElement(root, 'dcvalue')

def _define_attribute_value(an_element, attribute_name, attribute_value):
    """an element to add an attribute to an elementtree element object
    """
    return an_element.set(attribute_name, attribute_value)

def define_qualifer_element(an_element, qualifier_value):
    """set attribute qualifier with defined value on an elementtree object
    """
    return _define_attribute_value(an_element, "qualifier", qualifier_value)

def _default_qualifier_attribute(an_element):
    """set attribute qualifier with value none on an elementtree object
    """
    return _define_attribute_value(an_element, "qualifier", "none")

def _define_element_attribute(an_element, element_name):
    """set attribute element with defined value on an elementtree object
    """
    return _define_attribute_value(an_element, "element", element_name)

def _map_to_saf_dublincore(record):
    title = record["title"]
    creator = record["creator"]
    publisher = record["creator"]
    description = record["description"]
    copyrightdate = record["date.copyright"]
    issn = record["identifier.issn"]
    rights = record["rights"]
    subjects = [x.strip().lower() for x in re.split(';|,', record["subject"])]
    keywords = [x.strip().lower() for x in re.split(';|,', record["keywords"]) if not re.compile('^\s{1}Middle|East').search(x)]
    keywords.append('middle east')
    isformatof = record["relation.isFormatOf"]

    root = ElementTree.Element("dublin_core")
    start_list = [("title", "none", title),
                  ("creator", "none", creator),
                  ("publisher", "none", publisher),
                  ("description", "none", description),
                  ("date", "copyright", copyrightdate),
                  ("identifier", "issn", issn),
                  ("rights", "none", rights),
                  ("relation", "isFormatOf", isformatof)]
    keyword_list = [("subject", "keyword", keyword) for keyword in keywords]
    final_list = (start_list + keyword_list)
    for n in final_list:
        _make_a_new_sub_element({'element':n[0], 'qualifier':n[1]}, n[2], root)
    return root

def _generate_safs(metadata_file, input_dir):
    csv_data = _open_csv(metadata_file)
    for record in csv_data:
        filename = record["filename"]
    counter = 0
    for r in csv_data:
        counter += 1
        item_path = path.join('./SimpleArchiveFormat', 'item_' + str(counter).zfill(3))
        makedirs(item_path)
        dc_path = path.join(item_path, 'dublin_core.xml')

        new_metadata = _map_to_saf_dublincore(r)

        xml_string = ElementTree.tostring(new_metadata)
        xml_string = minidom.parseString(xml_string).toprettyxml()
        with open(dc_path, "w", encoding="utf-8") as write_file:
            write_file.write(xml_string)
        contents_path = path.join(item_path, 'contents')
        copyfile(path.join("./pdfs", r["filename"]), path.join(item_path, r["filename"]))
        with open(contents_path, "w", encoding="utf-8") as write_file:
            write_file.write(r["filename"])

def _main():
    parser = ArgumentParser(description="A cli module to process Mamluk files into SAFs")
    parser.add_argument("metadata_file", action="store", type=str, help="a csv file containing the metadata for the pdfs")
    parser.add_argument("pdf_directory", action="store", type=str, help="A directory containing the PDF files")
    parameters = parser.parse_args()
    try:
        _generate_safs(parameters.metadata_file, parameters.pdf_directory)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(_main())