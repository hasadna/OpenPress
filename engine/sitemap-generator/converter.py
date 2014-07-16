#!/usr/bin/env python
'''
@author: user
'''

import xml.etree.ElementTree as ET
from os.path import join, dirname, exists
from os import makedirs

def main(toc_path, output_path):
    tree = ET.parse(join(toc_path, "TOC.xml"))
    root = tree.getroot()
    sections = root.findall("./Body_np/Section")
    for section in sections:
        pages = section.findall('Page')
        for page in pages:
            #print page.attrib
            href = page.attrib['HREF']
            assert href[0] == '/'
            page_path = join(toc_path, href[1:] + '.xml')
            page_xml = ET.parse(page_path)
            page_directory = dirname(page_path)
            entities = page_xml.findall('Entity')
            for entity in entities:
                entity_ID = entity.attrib['ID']
                entity_path = join(page_directory, entity_ID + '.xml')

    #output file
    if not exists(output_path):
         makedirs(output_path)
    filePath = join(output_path, root.attrib['RELEASE_NO'])
    with open(filePath, 'w+'):
        pass  # TODO something?


if __name__ == '__main__':
    from sys import argv
    main(*argv[1:])
    main(*argv[1:])
