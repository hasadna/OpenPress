from upload import upload_all
from os.path import join, splitext, exists
from zipfile import ZipFile
import sys
import os

import json
import urllib2


SERVER = "opa.org.il"

class ArticleError(Exception): pass


def validate_article(article):
    

    # Set the request URL
    url = 'http://%s/api/v1/?articleId=%s' %(SERVER, article['id'])

    req = urllib2.Request(url)

    # Read the response
    resp = urllib2.urlopen(req).read()

    # Interpret the JSON response 
    data = json.loads(resp.decode('utf8'))
    if data['count'] != 1:
        articles = []
        for article in  data['results']:
            articles.append(article['id'])
        raise ArticleError("The count for %s is different then one the list - %s" %(article['id'],str(articles)))

def validate_articles(articles):
    for article in articles:
        validate_article(article)


class DemoSolr(object):
    def add(self, articles):
        ''' this is an hack so we wouldn't have to copy alot of code'''
        validate_articles(articles)



def main(argv):
    solr = DemoSolr()
    upload_all(solr, argv[1])


if __name__ == "__main__":
    main(sys.argv)
