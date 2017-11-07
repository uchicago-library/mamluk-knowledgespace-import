"""
        "identifier": "",
        "filename": "MSR_X-2_2006-Darling.pdf",
        "description": "Maml\u016bk Studies Review is an annual (bi-annual from 2003 to 2009), Open Access, refereed journal devoted to the Mamluk Sultanate of Egypt and Syria (1250-1517). See http://mamluk.uchicago.edu for further information.",
        "last page": "17",
        "publisher": "The Middle East Documentation Center (MEDOC)",
        "createdate": "2012:02:07 23:35:04-06:00",
        "page range": "1-17",
        "keywords": "mamluk; Egypt; Syria; sultanate; Middle East; history; justice; law; ",
        "first page": "1",
        "title": "Medieval Egyptian Society and the Concept of the Circle of Justice (MSR X.2, 2006)",
        "relation.isPartOf": "doi:10.6082/M1JH3J9R",
        "relation.isFormatOf": "Digital version of an article published (pp. 1-17) in Maml\u016bk Studies Review, Vol. X, no. 2, 2006. ISSN for print volumes: 1086-170X.",
        "identifier.uri": "",
        "date.copyright": "2006",
        "source": "doi:10.6082/M1JH3J9R",
        "webstatement": "http://mamluk.uchicago.edu/msr.html",
        "identifier.issn": "1947-2404",
        "creator": "Linda T. Darling",
        "rights": "\u00a92006 by Linda T. Darling. This work is made available under a Creative Commons Attribution 4.0 International license (CC-BY). Maml\u016bk Studies Review is an Open Access journal. See http://mamluk.uchicago.edu/msr.html for more information.",
        "volume #": "10.2",
        "subject": "mamluk, Egypt, Syria, Middle East, history, justice, law"
"""

from xml.etree import ElementTree
from os import _exit, mkdir
from os.path import join, exists
import re
import json
from shutil import copyfile

def main():
    data = json.load(open("mamluk_volume_10-2.json", "r", encoding="utf-8"))
    for row in data:
        root = ElementTree.Element("metadata")
        for key in row:
            if key == "identifier":
                print(key)
            elif key != "":
                if key == "subject" or key == "keyword":
                    element_name = ElementTree.SubElement(root, key + "s")
                    for n in re.split(";|,", row[key]):
                        el = ElementTree.SubElement(element_name, key)
                        el.text = n
                else:
                    element_name = key.replace(' ', '_')
                    new_element = ElementTree.SubElement(root, element_name)
                    new_element.text = row[key]
        tree = ElementTree.ElementTree(root)
        new_dir = join("out", row["filename"].split(".pdf")[0])
        xml_filename = join(new_dir, row["filename"].replace(".pdf", "_DATA.xml"))
        tree.write(xml_filename, xml_declaration=True, encoding="utf-8")
        pdf_filepath = join("input_pdfs", row["filename"])
        copyfile(pdf_filepath, join(new_dir, row["filename"]))
    return 0

if __name__ == "__main__":
    _exit(main())
