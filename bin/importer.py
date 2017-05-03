
from argparse import ArgumentParser
from magic import Magic
from os import _exit, scandir

from mamlukimport.parser import Parser

def read_directory(a_directory):
    items = scandir(a_directory)
    for n_item in items:
        if n_item.is_dir():
            yield from read_directory(n_item.path)
        elif n_item.is_file():
            file_mime_reader = Magic()
            mime_type = file_mime_reader.from_file(n_item, mime=True)
            if mime_type == "application/pdf":
                yield n_item

def main():
    try:
        parser = ArgumentParser(description="Process a directory of PDFs for the metadata in each PDF")
        parser.add_argument("pdf_directory", help="A directory that contains a bunch of PDF files.")
        args = parser.parse_args()
        a_generator = read_directory(args.pdf_directory)
        total_files = 0
        for n in a_generator:
            parsed = Parser(n_file)
            total_files += 1
            print(n)
        return 0
    except KeyboardInterrupt:
        return 131


if __name__ == "__main__":
    _exit(main())
