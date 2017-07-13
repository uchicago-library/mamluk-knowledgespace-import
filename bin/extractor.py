

from argparse import ArgumentParser
from collections import namedtuple
import re
import csv
import json
from json.decoder import JSONDecodeError
from os.path import basename
from os import _exit, scandir

from mamlukimport.parser import Parser
from mamlukimport.mapper import Mapper

def read_directory(a_directory):
    items = scandir(a_directory)

    for n_item in items:
        if n_item.is_dir():
            yield from read_directory(n_item.path)
        elif n_item.is_file():
            if '.json' in n_item.path:
                yield n_item.path

def main():
    try:
        parser = ArgumentParser(description="Process a directory of PDFs for the metadata in each PDF")
        parser.add_argument("pdf_directory", help="A directory that contains a bunch of PDF files.")
        parser.add_argument("output_file", help="A file to write the results of the metadata extration")
        args = parser.parse_args()
        a_generator = read_directory(args.pdf_directory)
        total_files = 0
        rows = []
        outputs = []
        for n in a_generator:
            try:
                data = json.load(open(n, encoding='utf-8'))[0]
                output = namedtuple("data", "creator title rights keywords subject createdate filename")
                creator = data["Creator"] if not isinstance(data["Creator"], list) else ', '.join(data["Creator"])
                title = data["Title"]
                rights = data["Rights"]
                print(rights.split(' ')[0])
                keywords = data["Keywords"] if not isinstance(data["Keywords"], list) else ', '.join([re.sub(';', '', x) for x in data["Keywords"]])
                subject = data["Subject"] if not isinstance(data["Subject"], list) else ', '.join([re.sub(';', '', x) for x in data["Subject"]])
                createdate = data["CreateDate"]
                filename = data["FileName"]
                volume = filename.split('_')[2]
                temp = volume.split('-')

                if len(temp) == 2:
                    if '.pdf' in temp[1]:
                        volume = temp[0]
                    else:
                        volume = volume
                publisher = "University of Chicago"
                try:
                    webstatement = data["WebStatement"]
                except KeyError:
                    webstatement = ""
                output.creator = creator
                output.title = title
                output.rights = rights
                output.keywords = keywords
                output.subject = subject
                output.createdate = createdate
                output.filename = filename
                outputs.append(output)
                row = [filename, creator, title, re.sub(r'\n', ' ', rights), webstatement, subject, keywords, createdate, publisher]
                rows.append(row)
            except JSONDecodeError:
                pass
        with open(args.output_file, "w", encoding="utf-8") as csv_file:
            csvfieldnames = ["filename", "creator", "title", "rights", "webstatement", "subject", "keywords", "publisher",  "createdate"]
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, quotechar="\"")
            writer.writerow(csvfieldnames)
            for n_row in rows:
                total_files += 1
                writer.writerow(n_row)
        for n_record in outputs:
            new_mapper = Mapper(n_record)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
