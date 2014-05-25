# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid
import pysolr

from tornado import gen
from tornado.options import define, options, parse_command_line

PUBLI = { 'HZT':     ,
          'HZV':     ,
          'MGD':     }
          

define("port", default=8888, help="run on the given port", type=int)

g_solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)

def id_to_url(article_id):
    '''
    this is really hacky... 
    TODO: FIXME!!!
    '''
    article_id = article_id.replace(r"/", "")
    url =  r"http://opa.org.il/article/"
    url += (article_id[:4] + article_id[8:12] +
            article_id[6:8] + article_id[4:6] + "_" + article_id[12:])
    return url


def convert_result(result):
    result['url'] = id_to_url(result['id'])
    result['year'] = result['issue_date'][6:] # TODO
    result['publisher'] = PUBLI[result['publisher']]
    result['issue'] = '' # TODO
    result['image'] = '' # TODO

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument("query", default=None, strip=False)
        if query is None:
            self.render("index.html")
        else:
            results = g_solr.search(query, rows=20)
            results = results.docs
            # Add the url to the article for every result.
            for result in results:
                convert_result(result)
            self.render("results.html", results=results, query=query)

            # TODO: self.render("timeline.html", results=results, query=query, start_date=start_date)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
