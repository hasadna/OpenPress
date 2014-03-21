from article import Article
from datetime import datetime
from copy import deepcopy

def parse_articles_from_PDF(path, date):
    pass

def parse_articles_from_TOC(path, date):
    pass

def create_articles(press, path):
    articles = []
    for year in os.listdir(path):
        year_path = os.path.join(path, year)
        for mounth in os.listdir(year_path):
            mounth_path = os.path.join(path, year, mounth)
            for day in os.listdir(mounth_path):
                articles_path = os.path.join(mounth_path, day)
                date = datetime(int(year), int(mounth), int(day))
                articles.expend(parse_articles_from_TOC(articles_path, 
                                                        date))
    
def create_presses(path):
    presses = []
    for press_name in in os.listdir(path):
        # Check if this is a direcotry.
        if os.isdir(os.path.join(path, press_name)):
            presses.append(Press(press_name))
    return presses
        
def parse_path(path):
    presses = create_presses(path)
    for press in presses:
        articles = create_articles(press, os.path.join(path, press.name))
        press.add_articles(articles)

