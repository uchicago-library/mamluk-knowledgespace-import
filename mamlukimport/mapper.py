
from xml.etree.ElementTree import Element, ElementTree, SubElement
from sys import stderr

class Mapper(object):
    def __init__(self, input):
        self._in = input
        self._lookup = {'title': {'element':'title', 'qualifier':'none'},
                       'copyright': {'element': 'date', 'qualifier':'copyright'},
                       'creator': {'element':'contributor', 'qualifier':'author'},
                       'rights': {'element': 'rights', 'qualifier': 'statement'},
                       'webstatement': {'element': 'rights', 'qualifier': 'url'},
                       'subject': {'element': 'subject', 'qualifier': 'none'},
                       'keyword': {'element': 'subject', 'qualifier': 'keyword'},
                       'source': {'element': 'source', 'qualifier': 'none'},
                       'part': {'element': 'relation', 'qualifier' :'isPartOf'},
                       'formatof': {'element': 'relation', 'qualifier' :'isFormatOf'},
                       'publisher': {'element': 'publisher', 'qualifier': 'none'},
                      }
        self.out = self._transform()

    def _transform(self):
        root = Element("dublin_core")
        for n_key in self._in:
            try:
                instructions = self._lookup.get(n_key)
            except KeyError:
                instructions = None
                stderr.write("{} is an invalid field for this mapping.\n".format(n_key))
            if instructions:
                for n_value in self._in[n_key]:
                    new_element = SubElement(root, "dc_value")
                    new_element.set("element", instructions["element"])
                    new_element.set("qualifier", instructions["qualifier"])
                    if n_value == 'subject':
                        print(new_element)
                    if isinstance(self._in[n_key], str):
                        new_element.text = self._in[n_key]
                    else:
                        new_element.text = str(self._in[n_key][n_value])
        return root

    def get_output(self):
        return self.out