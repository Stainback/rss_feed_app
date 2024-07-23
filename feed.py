import feedparser


class EntryHandler:
    def __init__(self, data):
        self.title = data.title
        self.description = data.description
        self.link = data.link


class Feed:
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)

    def __getitem__(self, index: int) -> EntryHandler:
        return EntryHandler(self.feed['entries'][index])
