
from argparse import ArgumentParser
import csv
from magic import Magic
from os.path import basename
from os import _exit, scandir

from mamlukimport.parser import Parser

def read_directory(a_directory):
    items = scandir(a_directory)
    for n_item in items:
        if n_item.is_dir():
            yield from read_directory(n_item.path)
        elif n_item.is_file():
            file_mime_reader = Magic(mime=True)
            mime_type = file_mime_reader.from_file(n_item.path)
            if mime_type == "application/pdf":
                yield n_item.path

def main():
    try:
        parser = ArgumentParser(description="Process a directory of PDFs for the metadata in each PDF")
        parser.add_argument("pdf_directory", help="A directory that contains a bunch of PDF files.")
        parser.add_argument("output_file", help="A file to write the results of the metadata extration")
        args = parser.parse_args()
        a_generator = read_directory(args.pdf_directory)
        total_files = 0

        with open(args.output_file, "w", encoding="utf-8") as csv_file:
            csvfieldnames = ["title", "author", "creationDate", "subject",  "filePath"]
            writer = csv.DictWriter(csv_file, fieldnames=csvfieldnames)
            writer.writeheader()
            for n_file in a_generator:
                parsed = Parser(n_file, ['author', 'subject', 'title', 'creationDate'])
                total_files += 1
                info = parsed.get_metadata()
                info["filePath"] = basename(n_file)
                writer.writerow(info)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
