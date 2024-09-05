import feedparser
from feedparser import sanitizer

from datetime import datetime
from time import mktime


for tag in ("a", "img"):
    sanitizer._HTMLSanitizer.acceptable_elements.remove(tag)


class Entry:
    def __init__(self, entry):
        self.id = hash(entry.title)
        self.title = entry.title
        self.url = entry.link
        self.description = " ".join(entry.description.split()[:150])
        self.published = datetime.utcfromtimestamp(
            mktime(entry.published_parsed)
        )

    def __str__(self):
        return f"{self.title} - {self.published.isoformat()}"

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other: "Entry"):
        if not isinstance(other, Entry):
            raise TypeError("Comparison not implemented")
        return self.id == other.id


class Feed:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.etag = None
        self.modified = None
        self.entries = None
        self.refresh()

    def __repr__(self) -> str:
        return self.title

    def __eq__(self, other: "Feed") -> bool:
        if not isinstance(other, Feed):
            raise TypeError("Comparison not implemented")
        return self.url == other.url

    def __getitem__(self, index: int) -> Entry:
        return self.entries[index]

    def refresh(self):
        feed = feedparser.parse(
            self.url, etag=self.etag, modified=self.modified
        )
        self.title = feed.get("title", "No Title")
        self.etag = feed.get("etag")
        self.modified = feed.get("modified")

        if feed.status != 304:
            self.entries = [Entry(data) for data in feed["entries"]]
