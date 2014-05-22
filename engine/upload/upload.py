# -*- coding: utf-8 -*-
# If on Python 2.X
from __future__ import print_function
import pysolr
import sys
import os
from zipfile import ZipFile
from os.path import join, splitext, exists
import xml.etree.ElementTree as ET

WORDS = ['W', 'QW']
LINE = ['L']
ZIP_PATH = "Document.zip"
FOLDER_PATH = "Document"
TOC_PATH = "TOC.xml"
PAGE = "Pg"
ARTICLE = "Ar"


class Page(object):
    def __init__(self, file_stream):
        self.METADATA = METADATA= {
                                   "Entity" : self._parse_entity,}

        self.entities = {}
        self.articles = []

        tree = ET.parse(file_stream)
        root = tree.getroot()

        for element in root.getchildren():
            if element.tag in self.METADATA:
                self.METADATA[element.tag](element)
    
    def _parse_entity(self, element):
        box = None
        ID = None

        for name, item in element.items():
            if name == 'BOX':
                box = item
            if name == 'ID':
                id_ = item

        self.entities[id_] = box
                
    def add_article(self, article):
        self.articles.append(article)

        if article.id in self.entities:
            article._info['box'] = self.entities[article.id]

    def get_articles(self):
        return [ar._info for ar in self.articles]


class Article(object):
    def _parse_META(self, element):

        doc_id = ''
        id_ = ''
        for name, item in element.items():
            if name == 'ISSUE_DATE':
                self._info['issue_date'] = item
            if name == 'PUBLICATION':
                self._info['publisher'] = item


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

        for name, item in root.items():
            if name == 'DOC_UID':
                doc_id = item
            if name == 'ID':
                id_ = item

        self.id = id_
        self._info['id'] = doc_id + id_

        for element in root.getchildren():
            if element.tag in self.METADATA:
                self.METADATA[element.tag](element)


def upload_directory(solr, path):
    '''
    Upload one direcotry to solr.
    '''

    with ZipFile(join(path, ZIP_PATH)) as zip_file:
        # Find all the pages in the current zip.
        pages = [info for info in zip_file.infolist() 
                      if (PAGE in info.filename and
                          info.filename.endswith(".xml"))]

        for page_file in pages:
            print(page_file.filename)
            # Create a page object.
            page = Page(zip_file.open(page_file.filename, "r"))
            
            page_dir = os.path.dirname(page_file.filename)
            # Find all the articles in the given page.
            article_files = [info for info in zip_file.infolist()
                                  if (page_dir in info.filename and
                                      ARTICLE in info.filename and
                                      info.filename.endswith(".xml"))]
                                     
            for article_file in article_files:
                # Create the article object.
                ar = Article(zip_file.open(article_file.filename, "r"))
                # Add it to the page.
                page.add_article(ar)
            
            # Add the articles to solr.
            solr.add(page.get_articles())


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
