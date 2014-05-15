# -*- coding: utf-8 -*-
# If on Python 2.X
from __future__ import print_function
import pysolr
import sys
from zipfile import ZipFile
from os.path import join, splitext, exists
import xml.etree.ElementTree as ET

WORDS = ['W', 'QW']
LINE = ['L']
ZIP_PATH = "Document.zip"
FOLDER_PATH = "Document"
TOC_PATH = "TOC.xml"


def get_articles_from_zip(zip_path):
    '''
    Returns the articles in the zip file, currently returns a bit 
    more than a test thingy.
    '''

    #use os.walk to iterate over all of our files

    with ZipFile(zip_path) as zip_file:
        for zip_info in zip_file.infolist():
            file_name = zip_info.filename
            if file_name.lower().endswith(".xml") and "Pg" not in file_name:
                with zip_file.open(file_name, "r") as file_stream:
                    yield file_stream


def get_articles_from_folder(folder):
    '''
    Returns the articles in the directory, currently returns a bit 
    more than a test thingy.
    '''

    #use os.walk to iterate over all of our files
    from os import walk

    for root, dirs, files in walk(folder):
        for file_name in files:
            if file_name.lower().endswith(".xml") and "Pg" not in file_name:
                with open(join(root, file_name), "rb") as file_stream:
                    yield file_stream


class Article(object):
    article_id = 0

    def _parse_META(self, element):
	doc_id = ''
        id_ = ''
        for name, item in element.items():
            if name == 'ISSUE_DATE':
                self._info['issue_date'] = item
            if name == 'PUBLICATION':
                self._info['publisher'] = item
            if name == 'DOC_ID':
                doc_id = item
            if name == 'ID':
                id_ = item
        self._info['id'] = doc_id + id_

    def _parse_Link(self, element):
        pass
    def _parse_Content(self, element):
        content = ''
        
        for primative in element.getchildren():
            for term in primative.getchildren():
                if term.tag in WORDS:
                    content += term.text
                #if term.tag in LINE:
                content += " "
                    
        self._info['content'] = content


    def __init__(self, file_stream):
        self.METADATA = METADATA= {
                                   "Meta" : self._parse_META,
                                   "Link" : self._parse_Link,
                                   "Content": self._parse_Content }
        self._info = {}
        tree = ET.parse(file_stream)
        root = tree.getroot()

        for element in root.getchildren():
            if element.tag in self.METADATA:
                self.METADATA[element.tag](element)
                
        Article.article_id += 1
        self._info['id'] = str(Article.article_id)
        
def upload_directory(solr, path):
    for article in get_articles_from_zip(join(path, ZIP_PATH)):
        ar = Article(article)
        solr.add([ar._info])

def upload_all(solr, input_folder):
    from os import walk, mkdir

    for root, dirs, files in walk(input_folder):
        if TOC_PATH in files:
            upload_directory(solr, root)

def main(argv):
    # Setup a Solr instance. The timeout is optional.
    solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)
    # You can optimize the index when it gets fragmented, for better speed.
    solr.optimize()
    upload_all(solr, argv[1])


if __name__ == "__main__":
    main(sys.argv)
