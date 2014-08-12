#!/usr/bin/env python
from cgi import parse_qs, escape
from re import match
from django.core.wsgi import get_wsgi_application
import urllib2
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openpress.settings")
GOOGLE_USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

LAYOUT_HOST = 'localhost:9980'
IMAGE_HOST = 'www.jpress.nli.org.il'
 
BOT_AGENTS = {GOOGLE_USER_AGENT}
PATH_PATTERN = r'/article/([A-Z]{3})_(\d{4})(\d{2})(\d{2})_([a-zA-Z]{2}\d{5})'
TEXT_PATTERN = 'http://www.jpress.nli.org.il/Olive/APA/NLI_heb/get/Article.ashx?href=%s%%2F%s%%2F%s%%2F%s&id=%s&mode=text'
IMAGE_PATTERN = 'http://' + IMAGE_HOST + '/Olive/APA/NLI_heb/get/Article.ashx?href=%s%%2F%s%%2F%s%%2F%s&id=%s&mode=image'
(PATH_GROUP_PUBLICATION,
 PATH_GROUP_YEAR,
 PATH_GROUP_MONTH,
 PATH_GROUP_DAY,
 PATH_GROUP_ARTICLE_ID) = range(5)

def application(env, start_response):
    path_match = match(PATH_PATTERN, env['PATH_INFO'])
    if path_match is None: #TODO: or article doesn't exist
        # status = '404 Not Found'
        # response_headers = [('Content-Type', 'text/plain')]
        # text = "Not Found"
        django_app = get_wsgi_application()
        return django_app(env, start_response)
    else:
        groups = path_match.groups()
        user_agent = env['HTTP_USER_AGENT']
        print user_agent
        if user_agent in BOT_AGENTS:
            status = '302 Found'
            # status = '200 OK'
            # response_headers = [('Content-Type', 'text/plain')]
            # text = '%s\n%s\n%s\n' % (user_agent, path, repr(GLOBAL_DICT))
            response_headers = [('Location', TEXT_PATTERN % groups)]
            text = ""
        else:
            proxied = urllib2.urlopen(IMAGE_PATTERN % groups).read().replace('src="',
                       'src="' + 'http://%s/Olive/APA/NLI_heb/get/' % (IMAGE_HOST,))
            status = '200 OK'
            # status = '200 OK'
            # response_headers = [('Content-Type', 'text/plain')]
            # text = '%s\n%s\n%s\n' % (user_agent, path, repr(GLOBAL_DICT))
            response_headers = [] #('Location', TEXT_PATTERN % groups)] # IMAGE_PATTERN % groups)]
            text = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8" />
</head>
<body>
%s
</body>
</html>""" % (proxied,)
    start_response(status, response_headers)
    return [text]
    #start_response('302 Found', [('Location','http://www.cnn.com')])
#def application(env, start_response):
#    start_response('200 OK', [('Content-Type','text/html')])
#    return ["Hello World"]
