from upload import upload_all
from whoosh.index import create_in
from datetime import datetime, timedelta
from whoosh import fields, index
import sys
import os


FIELDS = {
           'id': fields.TEXT,
           'box': fields.TEXT,
           'headline': fields.TEXT,
           'issue_date': fields.DATETIME,
           'publication_day': fields.NUMERIC,
           'publication_month': fields.NUMERIC,
           'publication_year': fields.NUMERIC,
           'newspaper_code':  fields.TEXT,
           'original_project_link': fields.TEXT,
           'location_in_page': fields.TEXT,
           'language': fields.TEXT,
           'page_in_paper': fields.NUMERIC,
           'original_project_ID': fields.TEXT,
           'content': fields.TEXT,
         }

class DemoSolr(object):
    def __init__(self):
        schema = fields.Schema(**FIELDS)
        ix = index.create_in("indexdir", schema)
        self.writer = ix.writer()

    def add(self, articles):
        ''' this is an hack so we wouldn't have to copy alot of code'''
        for article in articles:
            for key, item in article.items():
                print key
                if isinstance(item, str):
                    article[key] = unicode(item, "UTF-8")

            article['issue_date'] = datetime.strptime(article['issue_date'], "%d/%m/%Y")
            print str(article)
            self.writer.add_document(**article)

    def close(self):
        self.writer.commit()


def main(path):
    solr = DemoSolr()
    upload_all(solr, path)
    solr.close()

def usage():
    print "python %s <path_to_archive>" %(sys.argv[0],)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        main(*sys.argv[1:])
