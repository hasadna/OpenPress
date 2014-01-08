import sys
import zipfile
import os.path
#import xml.etree.ElementTree as ET

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
    '''
    Index the sitemaps 
    '''
    for loc, lastmod in sitemaps:
        yield ENTRY_TEMPLATE.format(LOC=loc, LASTMOD=lastmod)
        
def get_sitemaps_from_folder(folder_path):
    from os import walk
    real_path = os.path.realpath(folder_path)
    
    for root, dirs, files in walk(real_path):
        for file_name in files:
            if file_name.lower().endswith(".xml"):
                yield get_sitemap(os.path.relpath(os.path.join(root, file_name), real_path).replace("\\", "/"))

def main(argv):
    sitemap_index = SITEMAP_INDEX_TEMPLATE.format(ENTRIES = "".join(create_entries(get_sitemaps_from_folder("."))))
    print sitemap_index



if __name__ == "__main__":
    main(sys.argv)