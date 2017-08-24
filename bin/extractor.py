

from argparse import ArgumentParser
import re
import json
from json.decoder import JSONDecodeError
from os.path import join
from os import _exit, scandir
from sys import stdout
from xml.etree.ElementTree import tostring
from xml.dom import minidom

from mamlukimport.mapper import Mapper

def read_directory(a_directory):
    items = scandir(a_directory)
    for n_item in items:
        if n_item.is_dir():
            yield from read_directory(n_item.path)
        elif n_item.is_file():
            if '.json' in n_item.path:
                yield n_item.path

def expand_list_of_terms(value_string):
    item_count = 0
    output = {}
    for n_term in value_string.split(';'):
        n_term = n_term.lstrip().strip()
        val = None
        if n_term != "":
            val = n_term
            item_count += 1
        if val:
            output[item_count] = n_term
    return output

def create_input(iterable, total_files, outputs):
    for n_file in iterable:
        try:
            data = json.load(open(n_file, encoding='utf-8'))[0]
            total_files += 1
        except JSONDecodeError:
            continue
        output = {}
        output["publisher"] = expand_list_of_terms("University of Chicago")
        output["creator"] = expand_list_of_terms(data["Creator"])
        output["rights"] = expand_list_of_terms(data["Rights"])
        if not isinstance(data["Keywords"], list):
            output["keywords"] = expand_list_of_terms(data["Keywords"])
        else:
            output["keywords"] = expand_list_of_terms(data["Keywords"][0])
        if not isinstance(data["Subject"], list):
            output["subject"] = expand_list_of_terms(data["Subjects"])
        else:
            output["subject"] = expand_list_of_terms(data["Subjects"][0])
        output["createdate"] = expand_list_of_terms(data["CreateDate"])
        output["filename"] = expand_list_of_terms(data["FileName"])
        volume = data["FileName"].split('_')[2]
        temp = volume.split('-')
        if len(temp) >= 2:
            head = [temp[0]]
            tail = temp[1:]
            tail = [x for x in tail if re.compile(r'\d{1,}$').match(x)]
            output["copyrightdate"] = expand_list_of_terms(
                '-'.join(head + tail))
        else:
            output["copyrightdate"] = expand_list_of_terms('-'.join([re.sub(r'[a-z]', '',
                                                                            re.sub(r'\.', '', x))
                                                                     for x in temp]))
        msr_pattern = re.compile('MSR').search(data["Title"])
        vol_pattern = re.compile('Vol.').search(data["Title"])
        if msr_pattern:
            volume = data["Title"][data["Title"][
                1].index('MSR') + 3:].lstrip().strip()
            title = {1: data["Title"][0:data["Title"].index('MSR')]}
        elif vol_pattern:
            volume = data["Title"][1][
                data["Title"].index('Vol.') + 4:].lstrip().strip()
            title = data["Title"][0:data["Title"].index('Vol.')]
        else:
            volume = "none"
            title = expand_list_of_terms(title[1].lstrip().strip())
        first_check = title[1][-1]
        if first_check == '(':
            title = title[0:-1].strip().lstrip()
            second_check = title[-1]
        if second_check == ":":
            title = title[0:-1].strip().lstrip()
        if volume:
            volume = re.sub(r'\)', '', re.sub(r'\(', '', volume))
            if 'MamlukStudiesReview' in data["FileName"]:
                output["formatof"] = expand_list_of_terms(volume)
            else:
                output["part"] = expand_list_of_terms(volume)
        output["title"] = expand_list_of_terms(title)
        try:
            output["webstatement"] = expand_list_of_terms(
                data["WebStatement"])
        except KeyError:
            pass
        outputs.append(output)
    return outputs, total_files

def create_output(inputs):
   for n_record in inputs:
       filename = n_record["filename"]
       new_mapper = Mapper(n_record)
       new_filename = re.sub(r'.pdf', '.xml', filename[1])
       xml_string = tostring(new_mapper.out)
       xml_string = minidom.parseString(xml_string).toprettyxml()
       yield (xml_string, new_filename)

def main():
    try:
        parser = ArgumentParser(
            description="Process a directory of PDFs for the metadata in each PDF")
        parser.add_argument(
            "pdf_directory",
            help="A directory that contains a bunch of PDF files.")
        parser.add_argument(
            "output_directory",
            help="A directory to write the results of the metadata extraction")
        args = parser.parse_args()
        a_generator = read_directory(args.pdf_directory)
        total_files = 0
        inputs = []
        inputs, total_files = create_input(a_generator, total_files, inputs)
        stdout.write(
            "There were {} files processed completely".format(total_files))

        input_generator = create_output(inputs)
        for n_input in input_generator:
            with open(join(args.output_directory,
                           n_input[1]), "w", encoding="utf-8") as write_file:
                write_file.write(n_input[0])

        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
