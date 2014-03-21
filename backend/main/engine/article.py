from datetime import datetime

class Article(object):
    def __init__(self, name, date=None, content=None, content_loc=None):
        self._content = content
        self._date = date
        self._content_loc = content_loc

    def reload_content(self):
        pass

    @property
    def content(self):
        if self._content is not None:
            return self._content

        self.reload_content()
        return content
        
    @content.setter
    def content(self, value):
        # FIXME: should we add a check?
        self._content = value

