import feedparser


class Entry:
    def __init__(self, entry):
        self.id = hash(entry.title + entry.published)
        self.title = entry.title
        self.url = entry.link
        self.description = " ".join(entry.description.split()[:150])
        self.published = entry.published
        self.published_date = entry.published_parsed

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
        self.feed = feedparser.parse(self.url)
        self.etag = self.feed.get("etag")
        self.modified = self.feed.get("modified")
        self.entries = [Entry(data) for data in self.feed["entries"]]

        print(f"{self.url} - feed created, {self.etag} / {self.modified}, {self.feed.status}")

    def __repr__(self) -> str:
        return self.feed.get("title", "No Title")

    def __eq__(self, other: "Feed") -> bool:
        if not isinstance(other, Feed):
            raise TypeError("Comparison not implemented")
        return self.url == other.url

    def __getitem__(self, index: int) -> dict:
        return self.entries[index]

    def refresh(self):
        self.feed = feedparser.parse(
            self.url, etag=self.etag, modified=self.modified
        )
        if self.feed.status != 304:
            print(f"{self.url} - HTTP status: {self.feed.status}")
            titles = [entry.title for entry in self.entries]
            for entry in self.feed["entries"]:
                if entry.title not in titles:
                    print(
                        f"New entry: {entry.title} - {entry.published}"
                    )
            self.entries = [Entry(data) for data in self.feed["entries"]]
        else:
            print(f"{self.url} - no updates, HTTP status: {self.feed.status}")
