
from os.path import exists
from os import _exit, scandir
from magic import Magic
from PyPDF2 import PdfFileReader

class Parser(object):
    def __init__(self, filename, fields_to_extract):
        if exists(filename):
            self.fields = fields_to_extract
            self.file_object = PdfFileReader(open(filename, "rb"), strict=False)
            self.metadata = dict(self.file_object.getDocumentInfo())
        else:
            raise IOError("{} does not exist!".format(filename))

    def extract_a_metadata_field(self, field_name):
        field_name = field_name.lower()
        field_name = "/" + field_name[0].upper() + field_name[1:]
        if self.metadata.get(field_name, None):
            return self.metadata[field_name]
        else:
            return None

    def extract_core_metadata(self):
        output = {}
        for n_field in core_fields:
            field_value = self.metadata.get(n_field, None)
            if field_value != None:
                output[n_field.replace('/').lower()] = field_value
        return output

    def get_metadata(self):
        output = {}
        for n_field in self.fields:
            value = self.extract_a_metadata_field(n_field)
            output[n_field] = value
        return output
