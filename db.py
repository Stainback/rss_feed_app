from __future__ import annotations

import sqlite3

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

    def create_feed(self, url: str) -> int:
        feed = self.find_feed(url)
        if not feed:
            self.cursor.execute(
                """
                    INSERT INTO feeds (url) 
                    VALUES (?)
                """,
                (url, url)
            )
            self.conn.commit()

            return self.cursor.execute(
                "SELECT CAST(last_insert_rowid() AS int)"
            ).fetchone()[0]
        else:
            return feed

    def create_folder(self, name: str) -> int:
        folder = self.find_folder(name)
        if not folder:
            self.cursor.execute(
                """
                    INSERT INTO folders (name) 
                    VALUES (?)
                """,
                (name,)
            )
            self.conn.commit()

            return self.cursor.execute(
                "SELECT CAST(last_insert_rowid() AS int)"
            ).fetchone()[0]
        else:
            return folder

    def find_feed(self, url: str) -> int:
        query = self.conn.execute(
            "SELECT pk FROM feeds WHERE url = ?",
            (url, )
        ).fetchone()
        return query[0] if query else None

    def find_folder(self, name: str) -> int:
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
        feed_pk = self.find_feed(url)
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
        folder_pk = self.find_folder(folder)

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
