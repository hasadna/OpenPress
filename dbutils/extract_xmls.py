#!/usr/bin/env python

from os import walk, makedirs, remove
from os.path import splitext, join, split, exists, relpath
from zipfile import ZipFile, ZIP_DEFLATED
from logging import error, info
from traceback import format_exc

def report_exception(e):
    error(e)
    error(format_exc)

def process_zip_file(zip_file_name):
    try:
        with ZipFile(zip_file_name, 'r') as zip_file_obj:
            namelist = zip_file_obj.namelist()
            for compressed_file_name in namelist:
                (_comp_file_name, comp_file_ext) = splitext(compressed_file_name)
                if comp_file_ext.lower() == '.xml':
                    with zip_file_obj.open(compressed_file_name, 'r') as xml_file_obj:
                        xml_contents = xml_file_obj.read()
                        yield (compressed_file_name, xml_contents)
    except BaseException, be:
        report_exception(be)
    

def main(starting_path, result_path):
    output_zip_path = join(result_path, "XMLS.zip")
    with ZipFile(output_zip_path, 'a', ZIP_DEFLATED, True) as output_zip:
        current_files = set(s.replace('/','\\') for s in output_zip.namelist())
        for (root, _dirs, files) in walk(starting_path):
            new_dir_name = relpath(root, starting_path)
            for file_name in files:
                (stem, ext) = splitext(file_name)
                if ext.lower() == '.zip' and stem[0] != '.':
                    info('Processing %s' % (file_name,))
                    for (inner_file_path, inner_contents) in process_zip_file(join(root, file_name)):
                        new_file_name = join(new_dir_name, stem, inner_file_path)
                        if new_file_name.replace('/','\\') not in current_files:
                            try:
                                output_zip.writestr(new_file_name, inner_contents)
                            except BaseException, be:
                                report_exception(be)
                                continue
                elif ext.lower() == '.xml' and stem[0] != '.':
                    info('Processing %s' % (file_name,))
                    with open(join(root, file_name)) as xml_file:
                        xml_contents = xml_file.read()
                        new_file_name = join(new_dir_name, file_name)
                        if new_file_name.replace('/','\\') not in current_files:
                            try:
                                output_zip.writestr(new_file_name, xml_contents)
                            except BaseException, be:
                                report_exception(be)
                                continue

if __name__ == '__main__':
    from sys import argv
    main(argv[1], argv[2])