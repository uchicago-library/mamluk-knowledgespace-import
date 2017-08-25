

from argparse import ArgumentParser
import re
import json
from json.decoder import JSONDecodeError
from os.path import join
from os import _exit, scandir
from sys import stdout, stderr
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
    if ';' in value_string:
        a_list = value_string.split(';')
    elif isinstance(value_string, list):
        a_list = value_string
    else:
        a_list = [value_string]
    for n_term in a_list:
        n_term = n_term.lstrip().strip()
        val = None
        if n_term != "":
            val = n_term
            item_count += 1
        if val:
            output[item_count] = n_term
    return output

def _return_generic_string(a_string):
    return expand_list_of_terms("University of Chicago")

def _force_convert_to_list(a_string):
    return expand_list_of_terms([a_string])

def _extract_list_of_terms(some_original_input):
    return some_original_input

def _extract_copyright(rights_statement):
    test = rights_statement.split(' ')[0].encode('utf-8')
    test = test.split(b'\xc2\xa9')
    if len(test) == 2:
        return expand_list_of_terms(test[1].decode('utf-8'))
    else:
        return _return_generic_string("no copyright")

def _extract_volume_information(some_original_input):
    msr_pattern = re.compile('MSR').search(some_original_input)
    vol_pattern = re.compile('Vol.').search(some_original_input)
    output = re.sub('\)', '', re.sub('\(', '', some_original_input))

    exception_volumes = {
        "Mamluk Studies Review XVI (2012)": {"volume":"XVI (2012)"},
        "Mamluk Studies Review XV (2011)": {"volume": "XVI (2011)"},
    }

    exceptions = [
       "Ibn Tulun (d. 955/1548): Life and Works",
        "The Four Madrasahs in the Complex of Sultan Hasan (1356-61): The Complete Survey",
        "The al-Nashw Episode: A Case Study of \"Moral Economy\"",
        "Notes on the Contemporary Sources of the Year 793",
        "The Publications of Donald P. Little",
        "Ibn Tulun d. 955/1548: Life and Works",
        "Ceramic Evidence for Political Transformations in Early Mamluk Egypt",
        "Some Remarks on Ibn Tawq's Journal Al-Ta'liq, vol. 1",
        "The Four Madrasahs in the Complex of Sultan Hasan 1356-61: The Complete Survey",
        "Women and Gender in Mamluk Society: An Overview",
        "Idealism and Intransigence: A Christian-Muslim Encounter in Early Mamluk Times",
        "Editorial: Open Access and Copyright",
        "In Memoriam: David C. Reisman June 21, 1969-January 2, 2011",
    ]
    if (some_original_input in exceptions) or ((not 'MSR' in some_original_input) and (not 'Vol.' in some_original_input)):
        # stderr.write("could not determine volume information from title {}\n".format(some_original_input))
        if some_original_input not in exceptions and  exception_volumes.keys():
            stderr.write("{} is not accounted for\n".format(some_original_input))
    else:
        if 'MSR' in some_original_input:
            title, volume_info = output.split('MSR')
        elif 'Vol.' in some_original_input:
            title, volume_info = output.split('Vol.')
        return (title.lstrip().strip(), volume_info.lstrip().strip())

"""
exceptions:

The al-Nashw Episode: A Case Study of "Moral Economy"
Notes on the Contemporary Sources of the Year 793
The Publications of Donald P. Little
Ibn Tulun d. 955/1548: Life and Works
Ceramic Evidence for Political Transformations in Early Mamluk Egypt
Some Remarks on Ibn Tawq's Journal Al-Ta'liq, vol. 1
The Four Madrasahs in the Complex of Sultan Hasan 1356-61: The Complete Survey
Women and Gender in Mamluk Society: An Overview
Idealism and Intransigence: A Christian-Muslim Encounter in Early Mamluk Times
Editorial: Open Access and Copyright
In Memoriam: David C. Reisman June 21, 1969-January 2, 2011
"""

    # if msr_pattern:
    #     volume = data["Title"][data["Title"][0:]
    #     .index('MSR') + 3:].lstrip().strip()
    #        title = data["Title"][0:data["Title"].index('MSR')]
    #     elif vol_pattern:
    #         volume = data["Title"][1][data["Title"].index('Vol.') + 4:].lstrip().strip()
    #         title = data["Title"][0:data["Title"].index('Vol.')]
    #     else:
    #         volume = "none"
    #         title = title.lstrip().strip()
    #     first_check = title[-1]
    #     if first_check == '(':
    #         title = title[0:-1].strip().lstrip()
    #     second_check = title[-1]
    #     if second_check == ":":
    #         title = title[0:-1].strip().lstrip()
    #     if volume:
    #         volume = re.sub(r'\)', '', re.sub(r'\(', '', volume))
    #         if 'MamlukStudiesReview' in data["FileName"]:
    #             output["formatof"] = expand_list_of_terms(volume)
    #             output["source"] = expand_list_of_terms("printed " + volume)
    #         else:
    #             output["part"] = expand_list_of_terms(volume)
    #             output["source"] = expand_list_of_terms(volume)

def _check_for_webstatement(some_dict):
    if some_dict.get("WebStatement", None):
        output = some_dict.get("WebStatement")
    else:
        output = "http://mamluk.uchicago.edu/msr.html"
    return _return_generic_string(output)

def create_input(iterable, total_files, outputs):
    for n_file in iterable:
        try:
            data = json.load(open(n_file, encoding='utf-8'))[0]
            total_files += 1
        except JSONDecodeError:
            continue
        output = {}
        output["publisher"] = _return_generic_string("University of Chicago")
        output["creator"] = _return_generic_string(data["Creator"])
        output["rights"] = _force_convert_to_list(data["Rights"])
        output["copyright"] = _extract_copyright(data["Rights"])
        output["keywords"] = _extract_list_of_terms(data["Keywords"])
        output["subjects"] = _extract_list_of_terms(data["Subject"])
        output["filename"] = _return_generic_string(data["FileName"])
        output["volumme"] = _extract_volume_information(data["Title"])
        output["title"] = _return_generic_string(data["Title"])
        output["webstatement"] = _check_for_webstatement(data)
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
