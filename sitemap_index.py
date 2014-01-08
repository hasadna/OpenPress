import sys
import zipfile
import os
#import xml.etree.ElementTree as ET

path="????"
date='datattttt'


INDEX ='<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="{PATH}/sitemap/0.9">'

PREFIX="""
   <sitemap>

      <loc>"""
     
POSTFIX = """ </loc>
     <lastmod>{DATE}</lastmod>

   </sitemap>
"""

DEFAULT_DATE = "2013-01-01"
DEFAULT_CHANGEFREQ = "monthly"

def index_sitemaps(sitemaps):
    '''
    Index the sitemaps 
    '''
    global INDEX
  
    for sitemap in sitemaps:
        INDEX+= PREFIX+os.path.join('{PATH}',sitemap)+POSTFIX
        
    INDEX.format(PATH=path , DATE = date)
        
    INDEX+="""</sitemapindex>"""    
    print (INDEX)
        
        

def main(argv):
    
    INDEX = (index_sitemaps(argv[1:]))
    print INDEX



if __name__ == "__main__":
    main(sys.argv)