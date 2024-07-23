import sys

from PyQt6.QtWidgets import QApplication

from app import App
from db import DBManager


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("css/styles.css", "r") as styles_file:
        styles = styles_file.read()
        app.setStyleSheet(styles)

    with DBManager() as db:
        window = App(
            db=db,
            height=app.primaryScreen().availableSize().height()
        )

        window.show()
        app.exec()
