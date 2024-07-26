from feed import Feed, Entry
from db import DBManager


class AppManager:
    def __init__(self):
        with DBManager() as db:
            self.feeds = [Feed(url) for url in db.retrieve_all_feeds()]

    @staticmethod
    def add_feed_to_db(url: str) -> None:
        try:
            with DBManager() as db:
                db.create_feed(url)
        except ValueError as err:
            print(f"Error: {err}")

    def get_entries(self, folder: str = None) -> list[Entry]:
        entries = []

        with (DBManager() as db):
            urls = (
                db.retrieve_all_feeds()
                if not folder
                else db.retrieve_folder(folder)
            )

        for feed in self.feeds:
            if feed.url in urls:
                entries.extend(feed.entries)

        return sorted(entries, key=lambda e: e.published_date, reverse=True)

    def update_feeds(self, folder: str = None) -> None:
        with (DBManager() as db):
            urls = (
                db.retrieve_all_feeds()
                if not folder
                else db.retrieve_folder(folder)
            )

        existing = [feed.url for feed in self.feeds]

        for url in urls:
            if url in existing:
                self.feeds[existing.index(url)].refresh()
            else:
                self.feeds.append(Feed(url))
