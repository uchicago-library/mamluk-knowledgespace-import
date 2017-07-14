
from xml.etree.ElementTree import Element, SubElement
from sys import stderr

class Mapper(object):
    def __init__(self, input):
        self._in = input
        self._lookup = {'title': {'element':'title', 'qualifier':'none'},
                       'createdate': {'element': 'date', 'qualifier':'copyright'},
                       'creator': {'element':'contributor', 'qualifiier':'author'},
                       'rights': {'element': 'rights', 'qualifier': 'statement'},
                       'webstatement': {'element': 'rights', 'qualifier': 'url'},
                       'subject': {'element': 'subject', 'qualifier': 'none'},
                       'keyword': {'element': 'subject', 'qualifier': 'keyword'},
                       'source': {'element': 'source', 'qualifier': 'none'},
                       'isPartOf': {'element': 'relation', 'qualifier' :'isPartOf'},
                       'isFormatOf': {'element': 'relation', 'qualifier': 'isPartOf'},
                      }
        self.out = self._transform()

    def _transform(self):
        root = Element("dublin_core")
        for n_key in self._in:
            try:
                instructions = self._lookup.get(n_key)
                new_element = SubElement(root, "dc_value")
                new_element.set("element", instructions["element"])
                new_element.set("qualifier", instructions["qualifier"])
                new_element.text = self._in[n_key]
            except KeyError:
                stderr.write("{} is an invalid field for this mapping.".format(n_key))
        self.out = root

    def get_output(self):
        return self.out