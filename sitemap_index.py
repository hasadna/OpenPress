import sys
import zipfile
import os.path
from sitemap_generator import TOC_PATH, generate_document_sitemap
#import xml.etree.ElementTree as ET

#Change this according to where the sitemaps are hosted.
ROOT_PATH = "root"

SITEMAP_INDEX_TEMPLATE="""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{ENTRIES}</sitemapindex>
"""

ENTRY_TEMPLATE = """    <sitemap>
        <loc>{LOC}</loc>
        <lastmod>{LASTMOD}</lastmod>
    </sitemap>
"""

LOC_TEMPLATE = "/".join([ROOT_PATH, "{SITEMAP_PATH}"])

DEFAULT_DATE = "2013-01-01"

(SITEMAP_LOC,
 SITEMAP_LASTMOD) = range(2)

def get_loc(path):
    return LOC_TEMPLATE.format(SITEMAP_PATH=path)

def get_sitemap(path, date = DEFAULT_DATE):
    return get_loc(path), date

def create_entries(sitemaps):
    for loc, lastmod in sitemaps:
        yield ENTRY_TEMPLATE.format(LOC=loc, LASTMOD=lastmod)
        
def get_sitemaps_from_folder(folder_path):
    '''
    Walks through all xmls in a folder and returns them.
    '''
    from os import walk
    real_path = os.path.realpath(folder_path)
    
    for root, dirs, files in walk(real_path):
        for file_name in files:
            if file_name.lower().endswith(".xml"):
                yield get_sitemap(os.path.relpath(os.path.join(root, file_name), real_path).replace("\\", "/"))

                
def generate_sitemaps(input_folder, output_folder):
    '''
    Finds all articles in all publications in the input folder
    generates their sitemaps and output them in the output folder
    in the correct structure
    '''
    from os import walk, mkdir
    
    for root, dirs, files in walk(input_folder):
        if TOC_PATH in files:
            publication_name, xml_name, xml_content = generate_document_sitemap(root)
            publication_folder = os.path.join(output_folder, publication_name)
            if not os.path.exists(publication_folder):
                mkdir(publication_folder)
            output_file = open(os.path.join(output_folder, publication_name, xml_name + ".xml"), "wb")
            output_file.write(xml_content)
            output_file.close()

def generate_indices(sitemaps_root):
    '''
    Generates a sitemap index for all xmls in a target folder.
    '''
    from os import walk, sep
    
    real_path = os.path.realpath(sitemaps_root)
    
    for root, dirs, files in walk(real_path):
        for dir_name in dirs:
            publication_folder = os.path.join(root, dir_name)
            index_path = os.path.join(real_path, os.path.relpath(publication_folder, real_path).replace(sep, "_")) + ".xml"
            sitemap_index = SITEMAP_INDEX_TEMPLATE.format(ENTRIES = "".join(create_entries(get_sitemaps_from_folder(publication_folder))))
            output_file = open(index_path, "wb")
            output_file.write(sitemap_index)
            output_file.close()
            
def main(argv):
    generate_sitemaps(argv[1], argv[2])
    generate_indices(argv[2])



if __name__ == "__main__":
    main(sys.argv)