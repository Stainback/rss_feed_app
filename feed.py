import feedparser
from html.parser import HTMLParser


class EntryParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)

        self.title = data.title
        self.description = ""
        self.link = data.link

        self.feed(data.description)

    def handle_data(self, data):
        self.description += data.strip("\n")


class Feed:
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)

    def __getitem__(self, index: int) -> EntryParser:
        return EntryParser(self.feed['entries'][index])
