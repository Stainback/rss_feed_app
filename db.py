from __future__ import annotations

import sqlite3
from validators import url as url_validator

from feed import Feed


class DBManager:
    DB_PATH = "db/app_db.sqlite"

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def configure_db(self):
        pass

    def create_feed(self, url: str) -> None:
        if not isinstance(url, str):
            raise TypeError("URL must be a string.")
        elif not url_validator(url):
            raise ValueError("URL is not valid.")
        elif self.find_feed(url):
            raise ValueError("This URL already exists in database.")
        else:
            self.cursor.execute(
                """
                    INSERT INTO feeds (url) 
                    VALUES (?)
                """,
                (url,)
            )
            self.conn.commit()

    def create_folder(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        elif name.strip() == "":
            raise ValueError("Name must not be empty.")
        elif self.find_folder(name):
            raise ValueError(
                "Folder with this name already exists in database"
            )
        else:
            self.cursor.execute(
                """
                    INSERT INTO folders (name) 
                    VALUES (?)
                """,
                (name,)
            )
            self.conn.commit()

    def find_feed(self, url: str) -> int:
        if not isinstance(url, str):
            raise TypeError("URL must be a string.")
        else:
            query = self.conn.execute(
                "SELECT pk FROM feeds WHERE url = ?",
                (url, )
            ).fetchone()
            return query[0] if query else None

    def find_folder(self, name: str) -> int:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        else:
            query = self.conn.execute(
                "SELECT pk FROM folders WHERE name = ?",
                (name, )
            ).fetchone()
            return query(0) if query else None

    def retrieve_all_feeds(self) -> list[Feed]:
        return [
            Feed(row["url"])
            for row in self.conn.execute(
                "SELECT url FROM feeds"
            ).fetchall()
        ]

    def retrieve_folders_names(self) -> list[str]:
        return [
            row["name"]
            for row in self.conn.execute(
                "SELECT name FROM folders"
            ).fetchall()
        ]

    def retrieve_folder(self, folder: str) -> list[Feed]:
        if not isinstance(folder, str):
            raise TypeError("Folder name must be a string.")
        elif not self.find_folder(folder):
            raise ValueError(
                "Folder with this name does not exist in database."
            )
        else:
            urls_rows = self.conn.execute(
                """
                    SELECT url 
                    FROM main.feeds_folders ff
                    LEFT JOIN main.feeds f 
                    ON ff.feed_fk = f.pk
                    WHERE folder_fk = ?
                """,
                (folder, )
            ).fetchall()
            return [Feed(row["url"]) for row in urls_rows]

    def add_to_folder(self, url: str, folder: str) -> None:
        self.cursor.execute(
            """
                INSERT INTO feeds_folders (feed_fk, folder_fk) 
                VALUES (?, ?)
            """,
            (self.find_feed(url), self.find_folder(folder))
        )
        self.conn.commit()

    def delete_feed(self, url: str) -> None:
        if not isinstance(url, str):
            raise TypeError("URL must be a string.")

        feed_pk = self.find_feed(url)
        if feed_pk is None:
            raise ValueError("URL is not found in the database.")

        self.cursor.execute(
            """
                DELETE FROM feeds  
                WHERE pk = ?
            """,
            (feed_pk,)
        )

        self.cursor.execute(
            """
                DELETE FROM feeds_folders  
                WHERE feed_fk = ?
            """,
            (feed_pk,)
        )

        self.conn.commit()

    def delete_folder(self, folder: str) -> None:
        if not isinstance(folder, str):
            raise TypeError("Folder name must be a string.")

        folder_pk = self.find_folder(folder)
        if folder_pk is None:
            raise ValueError("Folder is not found in the database.")

        self.cursor.execute(
            """
                DELETE FROM folders 
                WHERE pk = ?
            """,
            (folder_pk,)
        )

        self.cursor.execute(
            """
                DELETE FROM feeds_folders  
                WHERE folder_fk = ?
            """,
            (folder_pk,)
        )

        self.conn.commit()
