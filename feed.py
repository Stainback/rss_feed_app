import feedparser


class Feed:
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)

    def __repr__(self):
        return self.feed.get("title", "No Title")

    def __getitem__(self, index: int):
        return self.feed['entries'][index]
