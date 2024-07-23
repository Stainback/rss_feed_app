import webbrowser

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, \
    QScrollArea, QToolBar, QLabel, QPushButton, QHBoxLayout, QLineEdit, \
    QDialog, QDialogButtonBox

from feed import Feed, EntryHandler
from db import DBManager


class App(QMainWindow):
    def __init__(
            self,
            feeds: list[Feed],
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

        self.content = ContentWidget(feeds)
        self.layout.addWidget(self.content)
        self.setCentralWidget(self.content)

        self.toolbar = ActionsWidget()
        self.toolbar.action_add.triggered.connect(self.add_rss)
        self.toolbar.action_refresh.triggered.connect(self.content.refresh)
        self.addToolBar(self.toolbar)

    def add_rss(self):
        # create a form
        self.dialog = UrlDialog()
        self.dialog.exec()
        # read url and check its validity
        # pass to db.create_feed
        # refresh active folder
        raise NotImplemented("Calling 'add_rss' function")


class ActionsWidget(QToolBar):
    def __init__(self):
        super().__init__()

        self.action_add = QAction("Add RSS", self)
        self.addAction(self.action_add)

        self.action_refresh = QAction("Refresh", self)
        self.addAction(self.action_refresh)


class UrlDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert feed URL")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.url_box = QLineEdit()
        self.layout.addWidget(self.url_box)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(QBtn)
        self.layout.addWidget(self.button_box)


class ContentWidget(QScrollArea):
    def __init__(self, feeds: list[Feed]):
        super().__init__()

        self.feeds = feeds

        self.layout = QVBoxLayout()
        self.widget = QWidget()

        for feed in self.feeds:
            for entry in feed:
                self.layout.addWidget(EntryFrame(entry))

        self.widget.setLayout(self.layout)

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    def refresh(self):
        # get feeds of active folder from db
        # check for updates
        # update active folder if needed
        raise NotImplemented("Calling 'refresh' function")


class EntryFrame(QFrame):
    def __init__(self, entry: EntryHandler = None):
        super().__init__()

        self.url = entry.link

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText(entry.title if entry else "No Title")
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.link_button = QPushButton()
        self.link_button.setObjectName("EntryLinkButton")
        self.link_button.setText("Read it")
        self.layout.addWidget(self.link_button)
        self.link_button.clicked.connect(self.open_link)

        self.expand_button = QPushButton("Expand")
        self.expand_button.setObjectName("EntryExpandButton")
        self.layout.addWidget(self.expand_button)
        self.expand_button.clicked.connect(self.change_description_state)

        self.description_label = QLabel()
        self.description_label.setText(" ".join(entry.description.split()[:150]) if entry else "No Description")
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
