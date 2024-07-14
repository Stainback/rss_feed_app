import sys

from PyQt6.QtWidgets import QApplication

from app import App
from feed import Feed


urls = [
    "https://dou.ua/feed/",
    "https://www.nasa.gov/aeronautics/feed/",
    "https://kotaku.com/rss"
]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    feeds = [Feed(url) for url in urls]

    with open("css/styles.css", "r") as styles_file:
        styles = styles_file.read()
        app.setStyleSheet(styles)

    window = App(feeds)

    window.show()
    app.exec()
