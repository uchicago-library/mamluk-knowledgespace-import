
from os.path import exists
from os import _exit, scandir
from magic import Magic
from PyPDF2 import PdfFileReader
import re

class Parser(object):
    def __init__(self, filename, fields_to_extract):
        if exists(filename):
            self.fields = fields_to_extract
            self.file_object = PdfFileReader(open(filename, "rb"), strict=False)
            self.metadata = dict(self.file_object.getDocumentInfo())
        else:
            raise IOError("{} does not exist!".format(filename))

    def extract_a_metadata_field(self, field_name):
        field_name = field_name
        field_name = "/" + field_name[0].upper() + field_name[1:]
        if self.metadata.get(field_name, None):
            return self.metadata[field_name]
        else:
            return None

    def get_metadata(self):
        output = {}
        for n_field in self.fields:
            if n_field == 'creationDate':
                value = self.extract_a_metadata_field(n_field).split('-')[0][2:]
                matchable = re.compile('^(\d{4})(\d{2})(\d{2})').search(value)
                value = matchable.group(1) + '-' + matchable.group(2) + '-' + matchable.group(1)
            else:
                value = self.extract_a_metadata_field(n_field)
            output[n_field] = value
        return output
