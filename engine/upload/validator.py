from upload import upload_all
from os.path import join, splitext, exists
from zipfile import ZipFile
import sys
import os

import json
import urllib2


SERVER = "opa.org.il"
g_logfile = None

class ArticleError(Exception): pass

def write_to_log(message):
    g_logfile.write(message + '\n')

def validate_article(article):
    
    print article['id']
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
        write_to_log("The count for %s is different then one the list - %s" %(article['id'],str(articles)))

def validate_articles(articles):
    for article in articles:
        validate_article(article)


class DemoSolr(object):
    def add(self, articles):
        ''' this is an hack so we wouldn't have to copy alot of code'''
        validate_articles(articles)



def main(path, log_filename):
    global g_logfile

    g_logfile = open(log_filename, 'a')
    solr = DemoSolr()
    upload_all(solr, path)

def usage():
    print "python %s <path_to_archive> <log_filename>" %(sys.argv[0],)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    else:
        main(*sys.argv[1:])
