
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

"""
date:.accessioned -> the date file added to the IR
date.copyright -> year of each issue
publisher -> "University of Chicago" or "University of Chicago Library"
identifier -> DOI
relation.isFormatOf -> should refer to full printed volume somehw
relation.isPartOf -> used in individual articles and should reference the volume and issue that this from
rights -> copyright statement in each file
rights.url -> MSR rights URL
rights.rightsStatement -> duplication of rights
source -> should refer to this being digital version of old printed version

creator
title
publisher
date.copyright
relation.isFormatOf OR relation.isPartOf
rights.url
rights.rightsStatement
source
type

"""

class Generator(object):
    def __init__(self, data, fields):
        for n_field in fields:
            setattr(self, n_field, data[field])

    def generate_metadata(self):
        root = Element("dublin_core")
        authors = self.data["author"].split(';')
        for n in authors:
            new_au_el = SubElement(root, 'dcvalue')
            new_au_el.set("element", "contributor")
            new_au_el.set("qualifier", "author")

        title_el = SubElement(root, 'dcvalue')
        title_el.set("element", "title")
        title_el.set("qaulifier", "none")

        mimetype_el = SubElement(root, "dcvalue")
        mimetype_el.set("element", "format")
        mimetype_el.set("qualifier", "mimetype")
        mimetype_el.text = "application/pdf"

        mimetype_el = SubElement(root, "dcvalue")
        mimetype_el.set("element", "date")
        mimetype_el.set("qualifier", "copyright")

        rights_url_el = SubElement(root, "dcvalue")
        rights_url_el.set("element", "rights")
        rights_url_el.set("qualifier", "url")

        source_el = SubElement(root, "dcvalue")
        source_el.set("element", "source")
        source_el.set("qualifier", "none")

        rights_state_el = SubElement(root, "dcvalue")
        rights_state_el.set("element", "rights")
        rights_state_el.set("qualifier", "rightsStatement")

        if self.type == 'article':
            is_part_of = SubElement(root, "dcvalue")
            rights_state_el.set("element", "relation")
            rights_state_el.set("qualifier", "isPartOf")

        if self.type == 'volume':
            is_format_of = SubElement(root, "dcvalue")
            is_format_of.set("element", "relation")
            is_format_of.set("qualifier", "isFormatOf")

        source = SubElement(root, "dcvalue")
        source.set("element", "source")
        source.set("qualifier", "none")
