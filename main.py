import feedparser
from entry import EntryParser


urls = [
    "https://dou.ua/feed/",
    "https://www.nasa.gov/aeronautics/feed/",
    "https://kotaku.com/rss"
]

if __name__ == "__main__":
    for url in urls:
        rss = feedparser.parse(url)
        for data in rss['entries']:
            entry = EntryParser(data)
            print(f"{entry.title} - {entry.link}")
            print(entry.section)
            print("****************************************")
