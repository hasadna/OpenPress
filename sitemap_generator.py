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

LOC_TEMPLATE = "http://jpress.nli.org.il/Olive/APA/NLI_heb/get/Article.ashx?href={PAPER_ID}&id={ARTICLE_ID}&mode=text"

ATTRIBUTE_TEMPLATE = """                <Attribute name="{KEY}">{VALUE}</Attribute>
"""

(URL_LOC,
 URL_LASTMOD,
 URL_ATTRIBUTES) = range(3)

(ARTICLE_PAPER_ID,
 ARTICLE_ARTICLE_ID,
 ARTICLE_ATTRIBUTES) = range(3)

def create_urls_block(url_list):
    nodes = []
    for loc, lastmod, attributes in iter(url_list):
        attributes_list = []
        for key, value in attributes.iteritems():
            attributes_list.append(ATTRIBUTE_TEMPLATE.format(KEY=key, VALUE=value))
        nodes.append(URL_TEMPLATE.format(LOC=loc, LASTMOD="date", ATTRIBUTES="".join(attributes_list)))
    return "".join(nodes)


def get_loc(paper_id, article_id):
    return LOC_TEMPLATE.format(PAPER_ID=paper_id.replace("/","%2F"), ARTICLE_ID=article_id)

def get_url(article, date=DEFAULT_DATE):
    return (get_loc(article[ARTICLE_PAPER_ID], article[ARTICLE_ARTICLE_ID]), date, article[ARTICLE_ATTRIBUTES])

def main(argv):
    articles = [("MAR/1987/01/02","Ar00108", {"Attribute1" : "value 1"})]
    urls = [get_url(article) for article in articles]
    urls_block = create_urls_block(urls)
    print SITEMAP_TEMPLATE.format(URLS = urls_block)
    


if __name__ == "__main__":
    main(sys.argv)