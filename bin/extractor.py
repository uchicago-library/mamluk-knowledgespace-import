

from argparse import ArgumentParser
from collections import namedtuple
import re
import csv
import json
from json.decoder import JSONDecodeError
from os.path import basename, join
from os import _exit, scandir
from xml.etree.ElementTree import tostring
from xml.dom import minidom

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
                publisher = {1: "University of Chicago"}
                if not isinstance(data["Creator"], list):
                    creator = {1: data["Creator"]}
                else:
                    crtr_count = 1
                    creator_dict = {}
                    for n_creator in data["Creator"]:
                        creator_dict[crtr_count] = n_creator
                        crtr_count += 1
                    creator = creator_dict
                title = {1: data["Title"]}
                rights = {1: data["Rights"]}

                if not isinstance(data["Keywords"], list):
                   kw_count = 1
                   kw_dict = {}
                   for n_keyw in data["Keywords"].split(';'):
                        n_keyw = n_keyw.lstrip().strip()
                        if n_keyw != "":
                            kw_dict[kw_count] = n_keyw
                            kw_count += 1
                   keywords = kw_dict
                else:
                    kw_count = 1
                    kw_dict = {}
                    for n_keyw in data["Keywords"][0].split(';'):
                        n_keyw = n_keyw.lstrip().strip()
                        if n_keyw != "":
                            kw_dict[kw_count] = n_keyw
                            kw_count += 1
                    keywords = kw_dict

                if not isinstance(data["Subject"], list):
                    subj_count = 1
                    subj_dict = {}
                    for n_subj in data["Subject"].split(';'):
                        n_subj = n_keyw.lstrip().strip()
                        if n_subj != "":
                            subj_dict[subj_count] = n_subj
                            subj_count += 1
                    subject = subj_dict

                else:
                    subj_count = 1
                    subj_dict = {}
                    for n_subj in data["Subject"][0].split(';'):
                        n_subj = n_keyw.lstrip().strip()
                        if n_subj != "":
                            subj_dict[subj_count] = n_subj
                            subj_count += 1
                    subject = subj_dict

                createdate = {1: data["CreateDate"]}
                filename = {1: data["FileName"]}
                volume = filename[1].split('_')[2]
                temp = volume.split('-')

                if len(temp) >= 2:
                    head = [temp[0]]
                    tail = temp[1:]
                    tail = [x for x in tail if re.compile('\d{1,}$').match(x)]
                    copyrightdate = head + tail
                else:
                    copyrightdate = [re.sub(r'[a-z]', '', re.sub(r'\.', '', x))
                                     for x in temp]
                copyrightdate = {1: '-'.join(copyrightdate)}

                msr_pattern = re.compile('MSR').search(title[1])
                vol_pattern = re.compile('Vol.').search(title[1])
                volume_option = re.compile('(\(MSR .*\))').search(title[1])
                volume_option2 = re.compile('(Vol. .*)').search(title[1])
                if msr_pattern:
                    volume = title[1][title[1].index('MSR')+3:].lstrip().strip()
                    title = {1: title[1][0:title[1].index('MSR')]}
                    print(title)
                elif vol_pattern:
                    volume = title[1][title[1].index('Vol.')+4:].lstrip().strip()
                    title = {1: title[1][0:title[1].index('Vol.')]}
                else:
                    volume = "none"
                title = {1: title[1].lstrip().strip()}

                first_check = title[1][-1]
                if first_check == '(':
                    title[1] = title[1][0:-1].strip().lstrip()
                second_check = title[1][-1]
                if second_check == ":":
                    title[1] = title[1][0:-1].strip().lstrip()
                try:
                    webstatement = data["WebStatement"]
                except KeyError:
                    webstatement = ""
                webstatement = {1: webstatement}
                str_filen = filename[1]
                output = {'creator': creator,
                          'title': title,
                          'rights': rights,
                          'keyword': keywords,
                          'subject': subject,
                          'createdate': copyrightdate,
                          'filename': filename,
                          'webstatement': webstatement,
                          'publisher': publisher,
                         }
                if volume:
                    volume = re.sub(r'\)', '', re.sub(r'\(', '', volume))
                    volume = {1: volume}
                    if 'MamlukStudiesReview' in filename[1]:
                        output["formatof"] = volume
                    else:
                        output["part"] = volume
                outputs.append(output)
            except JSONDecodeError:
                pass
        # with open(args.output_file, "w", encoding="utf-8") as csv_file:
        #     csvfieldnames = ["filename", "creator", "title", "rights", "webstatement", "subject", "keywords", "publisher",  "createdate"]
        #     writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, quotechar="\"")
        #     writer.writerow(csvfieldnames)
        #     for n_row in rows:
        #         total_files += 1
        #         writer.writerow(n_row)
        for n_record in outputs:
            filename = n_record["filename"]
            del n_record["filename"]
            new_mapper = Mapper(n_record)

            new_filename = re.sub(r'.pdf', '.xml', filename[1])
            xml_string = tostring(new_mapper.out)
            xml_string = minidom.parseString(xml_string).toprettyxml()
            with open(join('./out', new_filename), "w", encoding="utf-8") as write_file:
                write_file.write(xml_string)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
