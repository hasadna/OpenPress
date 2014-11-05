# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os.path
import uuid
import pysolr
import json
import re

from newspaper_codes import NewspaperCodes

from tornado import gen
from tornado.options import define, options, parse_command_line
          

ROWS_DEFAULT=20
NUMBER_REGEX = '^[0-9]{1,4}$'
COMPLETE_DATE_REGEX = ""
MONTH_YEAR_DATE_REGEX = ""
YEAR_DATE_REGEX = "^(19[0-9]{2})$|^(20[0-9]{2})$"

DATE_REGEX = YEAR_DATE_REGEX+"|"+MONTH_YEAR_DATE_REGEX+"|"+COMPLETE_DATE_REGEX



define("port", default=8888, help="run on the given port", type=int)

g_solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)
g_api_versions = ["v1"]

def id_to_url(article_id):
    '''
    this is really hacky... 
    TODO: FIXME!!!
    '''
    id_info = article_id.split("_")
    url =  r"http://opa.org.il/article/"
    
    id_info[2] = "0"+id_info[2] if len(id_info[2]) < 2 else id_info[2]
    id_info[3] = "0"+id_info[3] if len(id_info[3]) < 2 else id_info[3]
    
    # Still very much hacky!
    url += id_info[0]+"_"+"".join(id_info[1:4])+"_"+id_info[4]
    
    #url += (article_id[0] + article_id[8:12] +
    #        article_id[6:8] + article_id[4:6] + "_" + article_id[12:])
    return url

def validate_date(date):
    match_object = re.compile(DATE_REGEX).match(rows_string)
    if not match_object:
        return False
    return True


def get_rows(rows_string):
    match_object = re.compile(NUMBER_REGEX).match(rows_string)
    if not match_object:
        return ROWS_DEFAULT
    return int(match_object.group(0))

def get_image(result):
    """
    Hacky as always... (please FIXME)
    """
    
    id_fields = result['id'].split('_')
    id_ = id_fields[4]                  #article_id[14:]
    href = "/".join(id_fields[0:4])     #article_id[:14]

    image_url = "http://www.jpress.nli.org.il/Olive/APA/NLI_heb/get/GetImage.ashx?kind=block&href=%s&id=%s&ext=.png" %(href, id_)
    
    return image_url

def find_start_date(results):
    '''
    FIXME: this is a hack please fixme
    '''
    min_date = 0
    for result in results:
         year = int(result['publication_year'])
         if year < min_date:
            min_date = year
    return min_date
        
# link to image,url, 
def convert_result(result):
    result['url'] = id_to_url(result['id'])
    # FIXME:
    result['newspaper_full_name'] = NewspaperCodes.get_code(result['newspaper_code'])
    
    result.pop('original_project_link')
    
    # FIXME:
    if 'headline' not in result:
        result['headline'] = "Undefined"
        
    issue_date  = result['issue_date'].split("/")   
    
    
    result['issue_date_sortable'] = '-'.join(issue_date[::-1])
    result['issue'] = '' # TODO
    result['image'] = get_image(result)


def get_results(query, rows):
    ''' get results from solr service for a given query '''

    results = g_solr.search(query, rows=rows)
    results = results.docs
    # Add the url to the article for every result.
    for result in results:
        convert_result(result)

    return results

def findWholeWord(w):
    return re.compile(ur'\b({0})\b'.format(w), flags=re.IGNORECASE|re.UNICODE).search

def get_statistics(query, results):
    stats = {word: 0 for word in query.split(" ")}

    stats[query] = 0
    for result in results:
        querySearch = findWholeWord(query)
        if querySearch(result['content'][0]) or querySearch(result['headline']):
            stats[query] += 1

        else:
            for word in stats:
                wordsSearch = findWholeWord(query)
                stats[word] += 1 if wordsSearch(result['content'][0]) or wordsSearch(result['headline']) else 0

    return stats

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument("query", default=None, strip=False)
        rows = self.get_argument("rows", default='20', strip=True)

        rows = get_rows(rows)

        if query is None:
            self.render("index.html")
        else:

            results = get_results(query, rows)
            
            stats = get_statistics(query, results)

            start_date = find_start_date(results)  # for the timeline!!

            #self.render("timeline.html", results=results, query=query, start_date=start_date)
            self.render("results.html", results=results, query=query, start_date=start_date, stats=stats)

class ApiHandler(tornado.web.RequestHandler):

	ORDER_DATE_ACCENDING = "dateAccending"
    ORDER_DATE_DECENDING = "dateDecending"
    ORDER_RELEVENCE = "relevance"
	
	g_api_orders = [ORDER_DATE_ACCENDING, ORDER_DATE_DECENDING, ORDER_RELEVENCE]
	
	DATE_RANGE_LEQ = "dateLeq"
	DATE_RANGE_GEQ = "dateGeq"
	g_api_date_range = [DATE_RANGE_LEQ, DATE_RANGE_GEQ]
	
    def send_json(self, d):
        response_json = tornado.escape.json_encode(d)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(response_json)

    def get(self,apiId):

        if apiId not in g_api_versions:
            err_msg = {'Error': 'Unsupported Version',
                        'supported versions': g_api_versions}
            self.write(err_msg)
            return
        
        if apiId == "v1":
            self.get_api_v1()

    def get_api_v1(self):
        
        articleId = self.get_argument("articleId", default=None, strip=False)

        if articleId:
            results = g_solr.search('id:%s' % articleId, rows=rows)
            
            for result in results:
            	convert_result(result)
            
            results = results.docs
            response = { 'count' : len(results), 'results': results}
            self.send_json(response)
        
        elif query:
            order_by = self.get_argument("odrderBy", default=None, strip=True)
                    
            if order_by and not order_by in g_api_orders:
                err_msg = {'Error': 'Unsupported Date Order Type',
                            'supported types': g_api_orders}
                self.write(err_msg)
                return
                
            query = self.get_argument("query", default=None, strip=False)
            dateLeq = self.get_argument("dateLeq", default=None, strip=False)
            dateGeq = self.get_argument("dateGeq", default=None, strip=False)
            rows = self.get_argument("rows", default='20', strip=True)
            
            if dateLeq and not validate_date(dateLeq):
                err_msg = {'Error': 'Invalid date inserted for range operation'}
                self.write(err_msg)
                return
                
            if dateGeq and not validate_date(dateGeq):
                err_msg = {'Error': 'Invalid date inserted for range operation'}
                self.write(err_msg)
                return 
            
            rows = get_rows(rows)
        
            results = get_results(query, rows, dateLeq, dateGeq)
            results = self.sort_results(results, order_by)
            response = { 'count' : len(results), 'results': results}
            self.send_json(response)
            
        else:
            welcome = {'welcome_msg': ' Welcome to Open Press API',
                       'usage': ' See Docs @ openpress.readthedocs.org/en/latest/api.html '}
            self.write(welcome)
   
    	
    def sort_results(self, results, order):
        # Every item in the results is a dictionary in itself
        from operator import itemgetter
        
        if not order:
            return
        
        elif order == ORDER_DATE_ACCENDING:
            return sorted(results, key=it("issue_date_sortable"))
        
        elif order == ORDER_DATE_DECENDING:
            return sorted(results, key=it("issue_date_sortable"), reverse=True)

        elif order == ORDER_RELEVENCE:
            pass
    

def create_app(app_class):
    app = app_class(

        [(r"/", MainHandler), (r"/api/(v[0-9]+)/", ApiHandler)],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),

        )
    return app

def application(env, start_response):
    wsgi_app = create_app(tornado.wsgi.WSGIApplication)
    return wsgi_app(env, start_response)
    
def main():
    parse_command_line()
    app = create_app(tornado.web.Application)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
