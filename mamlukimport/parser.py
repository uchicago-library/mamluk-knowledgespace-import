
from os.path import exists
from PyPDF2 import PdfFileReader

class Parser(object):
    def __init__(self, filename):
        if exists(filename):
            self.data = PdfFileReader(open(filename, "r")).getDocumentInf()
        else:
            raise IOError("{} does not exist!".format(filename))
