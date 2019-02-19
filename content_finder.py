from html.parser import HTMLParser
from urllib import parse


class ContentFinder(HTMLParser):

    def __init__(self):
        super().__init__()
        self.content = {}
        self.content_required = 0
        self.content_label = ''

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attributes):
        if tag == 'th':
            for name, value in attributes:
                if name == 'class' and value in ['drawDate', 'drawNumber']:
                    self.content_required = 1
                    self.content_label = value
                else:
                    continue
        elif tag == 'td':
            for name, value in attributes:
                if name == 'class' and value in ['win1','win2','win3','win4','win5','win6','additional']:
                    self.content_required = 1
                    self.content_label = value
                else:
                    continue
        else:
            return

    def handle_endtag(self, tag):
        if tag in ['th', 'td'] and self.content_required:
            self.content_required = 0
            self.content_label = ''

    def handle_data(self, data):
        if self.content_required:
            self.content[self.content_label] = data

    def get_data(self):
        return self.content

    def error(self, message):
        pass
