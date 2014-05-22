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

define("port", default=8888, help="run on the given port", type=int)

g_solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument("query", default=None, strip=False)
        if query is None:
            self.render("index.html")
        else:
            results = g_solr.search(query)
            results = results.docs[:100]
            self.render("results.html", results=results)


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
