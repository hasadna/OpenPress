from parser import parse_path

class Press(object):
    def __init__(self, name):
        self.name = name
        self._articles = []

    def add_articles(self, articles):
        self._articles.expend(article)

class Database(object):
    def __init__(self):
        pass
    @classmethod
    def load_path(cls, path):
        return cls(parse_path(path))
        
    def iter_press(self):
        for press in self:
            yield press

    def __iter__(self):
        for press in self
