#!/usr/bin/env python
import os
import xml.etree.ElementTree as ET
from os.path import join, dirname, exists
from os import makedirs
import zipfile
import xml_to_html
from os.path import expanduser


def main(toc_path, output_path):
    tree = ET.parse(join(toc_path, "TOC.xml"))
    root = tree.getroot()
#output file
    if not exists(output_path):
         makedirs(output_path)
    filePath = join(output_path, root.attrib['RELEASE_NO'])
    with open(filePath, 'w+') as output_file:

        publication =  root.attrib["PUBLICATION"]
        print root.attrib
        Meta = root.findall("./Head_np/Meta")
        publication_date= Meta[0].attrib["BASE_HREF"]
        sections = root.findall("./Body_np/Section")
        u = [("publication_date","entity_id")]
        for section in sections:
            pages = section.findall('Page')
            for page in pages:
                href = page.attrib['HREF']
                page_path = join(toc_path, href[1:] + '.xml')
                page_xml = ET.parse(page_path)
                entities = page_xml.findall('Entity')
                for entity in entities:
                    entity_ID = entity.attrib['ID']
                    entity_path = join(publication_date, entity_ID)
                    entity_tuple=(publication_date,entity_ID)
                    u.append(entity_tuple)

    print u

if __name__ == '__main__':
    home = expanduser("~")
    from sys import argv
    main(*argv[1:])
