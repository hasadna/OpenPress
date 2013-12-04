import sys
#import xml.etree.ElementTree as ET
SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{URLS}
</urlset>
"""
DEFAULT_DATE = "2013-01-01"
DEFAULT_CHANGEFREQ = "monthly"
URL_TEMPLATE = """    <url>
        <loc>{LOC}</loc>
        <lastmod>{LASTMOD}</lastmod>
        <PageMap xmlns="http://www.google.com/schemas/sitemap-pagemap/1.0">
            <DataObject type="document">
{ATTRIBUTES}
            </DataObject>
        </PageMap>
    </url>"""

#adding &mode=text at the end will get us textual results
LOC_TEMPLATE = "http://jpress.nli.org.il/Olive/APA/NLI_heb/get/Article.ashx?href={PAPER_ID}&id={ARTICLE_ID}&mode=text"

ATTRIBUTE_TEMPLATE = """                <Attribute name="{KEY}">{VALUE}</Attribute>
"""

(URL_LOC,
 URL_LASTMOD,
 URL_ATTRIBUTES) = range(3)

(ARTICLE_PAPER_ID,
 ARTICLE_ARTICLE_ID,
 ARTICLE_ATTRIBUTES) = range(3)


def parse_urls(urls):
    '''
    Parses the urls, it should be a generator expression (as created by get_articles)
    This is a generator which generates the url in template form.
    '''
    for loc, lastmod, attributes in urls:
        attributes_list = []

        for key, value in attributes.iteritems():
            attributes_list.append(ATTRIBUTE_TEMPLATE.format(KEY=key, VALUE=value))
        yield URL_TEMPLATE.format(LOC=loc, LASTMOD=lastmod, ATTRIBUTES="".join(attributes_list))


def get_loc(paper_id, article_id):
    return LOC_TEMPLATE.format(PAPER_ID=paper_id.replace("/","%2F"), ARTICLE_ID=article_id)


def get_url(article, date=DEFAULT_DATE):
    return get_loc(article[ARTICLE_PAPER_ID], article[ARTICLE_ARTICLE_ID]), date, article[ARTICLE_ATTRIBUTES]


def parse_xml_file(filePath, fileName):
    '''
    Parses an xml file. currently only greps the base path and no attributes.
    We should actually parse the XML to get the attributes.
    '''
    attributes = {}
    import re
    with open(filePath) as file_:
        lines = file_.read()
        base_href = re.search("BASE_HREF=\"([^\"]+)", lines)

    return base_href.group(1), fileName, attributes



def get_articles_from_folder(folder):
    '''
    Returns the articles in the directory, currently returns only a test thingy.
    '''

    #use os.walk to iterate over all of our files
    from os import walk
    from os.path import join

    for root, dirs, files in walk(folder):
        for fileName in files:
            if fileName.endswith(".xml") and "Pg" not in fileName:
                yield parse_xml_file(join(root, fileName), fileName)


def main(argv):
    urls = (get_url(article) for article in get_articles_from_folder("./Document"))
    print SITEMAP_TEMPLATE.format(URLS="".join(parse_urls(urls)))



if __name__ == "__main__":
    main(sys.argv)