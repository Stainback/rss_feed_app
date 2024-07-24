import webbrowser

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, \
    QScrollArea, QToolBar, QLabel, QPushButton, QHBoxLayout, QLineEdit, \
    QDialog, QDialogButtonBox

from feed import Feed
from db import DBManager


class App(QMainWindow):
    def __init__(
            self,
            db: DBManager,
            width: int = 520,
            height: int = 1040
    ):
        super().__init__()

        self.db = db

        self.setWindowTitle("RSS Feed")
        self.setFixedSize(QSize(width, height))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.content = ContentWidget(self.db.retrieve_all_feeds())
        self.layout.addWidget(self.content)
        self.setCentralWidget(self.content)

        self.toolbar = ActionsWidget()
        self.toolbar.action_add.triggered.connect(lambda: self.dialog.exec())
        self.toolbar.action_refresh.triggered.connect(self.refresh)
        self.addToolBar(self.toolbar)

        self.dialog = UrlDialog(self)
        self.dialog.submitted_url.connect(self.add_rss)

    def add_rss(self, url: str):
        try:
            self.db.create_feed(url)
            self.refresh()
        except ValueError as err:
            print(f"Error: {err}")

    def refresh(self):
        # get feeds of active folder from db
        # check for updates
        # update active folder if needed
        self.content.update_content(self.db.retrieve_all_feeds())


class ActionsWidget(QToolBar):
    def __init__(self):
        super().__init__()

        self.action_add = QAction("Add RSS", self)
        self.addAction(self.action_add)

        self.action_refresh = QAction("Refresh", self)
        self.addAction(self.action_refresh)


class UrlDialog(QDialog):
    submitted_url = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Insert feed URL")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.url_box = QLineEdit()
        self.layout.addWidget(self.url_box)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def accept(self):
        self.submitted_url.emit(self.url_box.text())
        super().accept()


class ContentWidget(QScrollArea):
    def __init__(self, feeds: list[Feed]):
        super().__init__()

        self.layout = QVBoxLayout()
        self.widget = QWidget()

        self.widget.setLayout(self.layout)

        self.content = []
        self.update_content(feeds)

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    def update_content(self, feeds: list[Feed]):
        for feed in feeds:
            for entry in feed:
                entry_widget = EntryFrame(entry)
                if entry_widget.id not in map(
                        lambda item: item.id, self.content
                ):
                    self.content.append(entry_widget)
                    self.layout.addWidget(entry_widget)


class EntryFrame(QFrame):
    def __init__(self, entry=None):
        super().__init__()

        self.id = hash(entry.title + entry.published)
        self.url = entry.link

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText(entry.title if entry else "No Title")
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.button_widget = QWidget()
        self.layout.addWidget(self.button_widget)

        self.button_layout = QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        self.link_button = QPushButton()
        self.link_button.setObjectName("EntryLinkButton")
        self.link_button.setText("Read it")
        self.button_layout.addWidget(self.link_button)
        self.link_button.clicked.connect(self.open_link)

        self.expand_button = QPushButton("Expand")
        self.expand_button.setObjectName("EntryExpandButton")
        self.button_layout.addWidget(self.expand_button)
        self.expand_button.clicked.connect(self.change_description_state)

        self.description_label = QLabel()
        self.description_label.setText(
            " ".join(entry.description.split()[:150])
            if entry else "No Description"
        )
        self.description_label.setWordWrap(True)
        self.expand_flag = False
        self.change_description_state()
        self.layout.addWidget(self.description_label)

    def change_description_state(self):
        state = {True: (500, "⌃"), False: (0, "⌄")}
        self.description_label.setMaximumHeight(state[self.expand_flag][0])
        self.expand_button.setText(state[self.expand_flag][1])
        self.expand_flag = not self.expand_flag

    def open_link(self):
        wb = webbrowser.get()
        wb.open_new_tab(self.url)
