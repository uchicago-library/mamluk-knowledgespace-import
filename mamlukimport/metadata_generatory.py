
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class Generator(object):
    def __init__(self, data, fields):
        for n_field in fields:
            setattr(self, n_field, data[field])

    def generate_metadata(self):
        root = Element("dublin_core")
        author_el = SubElement(root, 'dcvalue')
        author_el.set("element", "contributor")
        author_el.set("qualifier", "author")
        author_el.text = self.author

        date_el = SubElemet(root, "dcvalue")
        date_el.set("element", "date")
        date_el.set("qualifier", "issued")
        date_el.text = self.creationDate

        title_el = SubElement(root, "dcvalue")
        title_el.set("element", "title")
        title_el.set("qualifier", "none")
        title_el.text = self.title

        mimetype_el = SubElement(root, "dcvalue")
        mimetype_el.set("element", "format")
        mimetype_el.set("qualifier", "mimetype")
        mimetype_el.text = "application/pdf"

        for n_keyw in self.keywords.split(';'):
            subj_el = SubElement(root, "dcvalue")
            subj_el.set("element", "subject")
            subj_el.set("qualifier", "none")
            subj_el.text = n_keyw

        subj_el = SubElement(root, "dcvalue")
        subj_el.set("element", "subject")
        subj_el.set("qualifier", "none")
        subj_el.text = self.subject
