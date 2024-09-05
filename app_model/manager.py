from app_model.feed import Feed, Entry
from app_model.db import DBManager


class Manager:
    def __init__(self):
        with DBManager() as db:
            self.feeds = {url: Feed(url) for url in db.retrieve_all_feeds()}

    def add_feed(self, url: str) -> None:
        try:
            with DBManager() as db:
                db.create_feed(url)
            self.feeds[url] = Feed(url)
        except ValueError as err:
            print(f"Error: {err}")

    def remove_feed(self, url: str) -> None:
        try:
            with DBManager() as db:
                db.delete_feed(url)
            self.feeds.pop(url)
        except ValueError as err:
            print(f"Error: {err}")

    def get_feeds(self, folder: str = None) -> list[Feed]:
        if folder:
            with DBManager() as db:
                urls = db.retrieve_folder(folder)
            return [feed for (url, feed) in self.feeds.items() if url in urls]
        else:
            return list(self.feeds.values())

    def get_entries(self, folder: str = None) -> list[Entry]:
        entries = []

        for feed in self.get_feeds(folder):
            entries.extend(feed.entries)

        return sorted(entries, key=lambda e: e.published, reverse=True)

    def get_folders(self) -> dict:
        folders = {"All feeds": self.get_entries()}

        with DBManager() as db:
            for name in db.retrieve_folders_names():
                folders.update({name: self.get_entries(name)})

        return folders


if __name__ == "__main__":
    manager = Manager()
    print(manager.get_folders().values())
