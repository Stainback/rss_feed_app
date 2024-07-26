import feedparser

from datetime import datetime
from time import mktime


class Entry:
    def __init__(self, entry):
        self.id = hash(entry.title + entry.published)
        self.title = entry.title
        self.url = entry.link
        self.description = " ".join(entry.description.split()[:150])
        self.published = entry.published
        self.published_date = datetime.fromtimestamp(
            mktime(entry.published_parsed)
        )

    def __str__(self):
        return f"{self.title} - {self.published}"

    def __repr__(self):
        return self.id

    def __eq__(self, other: "Entry"):
        if not isinstance(other, Entry):
            raise TypeError("Comparison not implemented")
        return self.id == other.id


class Feed:
    def __init__(self, url):
        self.url = url
        self.feed = None
        self.etag = None
        self.modified = None
        self.entries = None
        self.refresh()

        # Debug
        print(f"{self.url} - feed created, {self.etag} / {self.modified}, {self.feed.status}")

    def __repr__(self) -> str:
        return self.feed.get("title", "No Title")

    def __eq__(self, other: "Feed") -> bool:
        if not isinstance(other, Feed):
            raise TypeError("Comparison not implemented")
        return self.url == other.url

    def __getitem__(self, index: int) -> Entry:
        return self.entries[index]

    def refresh(self):
        self.feed = feedparser.parse(
            self.url, etag=self.etag, modified=self.modified
        )
        self.etag = self.feed.get("etag")
        self.modified = self.feed.get("modified")

        if self.feed.status != 304:
            # Debug
            if self.entries:
                titles = [entry.title for entry in self.entries]
                for entry in self.feed["entries"]:
                    if entry.title not in titles:
                        print(
                            f"New entry: {entry.title} - {entry.published}"
                        )

            self.entries = [Entry(data) for data in self.feed["entries"]]
