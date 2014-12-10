from upload import upload_all
from whoosh.index import create_in
from datetime import datetime, timedelta
from whoosh import fields, index
import sys
import os


FIELDS = {
           'id': fields.TEXT(stored=True),
           'box': fields.TEXT(stored=True),
           'headline': fields.TEXT(stored=True),
           'issue_date': fields.DATETIME(stored=True),
           'publication_day': fields.NUMERIC(stored=True),
           'publication_month': fields.NUMERIC(stored=True),
           'publication_year': fields.NUMERIC(stored=True),
           'newspaper_code':  fields.TEXT(stored=True),
           'original_project_link': fields.TEXT(stored=True),
           'location_in_page': fields.TEXT(stored=True),
           'language': fields.TEXT(stored=True),
           'page_in_paper': fields.NUMERIC(stored=True),
           'original_project_ID': fields.TEXT(stored=True),
           'content': fields.TEXT(stored=True),
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
            #print str(article)
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
