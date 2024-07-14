from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, QScrollArea, QToolBar, QLabel, QPushButton
from feed import Feed, EntryParser


class App(QMainWindow):
    def __init__(self, feeds: list[Feed], width: int = 520, height: int = 1040):
        super().__init__()

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
        #self.toolbar.action_settings.triggered.connect(settings)
        self.addToolBar(self.toolbar)

    def add_rss(self):
        print("Calling 'add_rss' function")


class ActionsWidget(QToolBar):
    def __init__(self):
        super().__init__()

        self.action_add = QAction("Add RSS", self)
        self.addAction(self.action_add)

        self.action_refresh = QAction("Refresh", self)
        self.addAction(self.action_refresh)

        self.action_settings = QAction("Settings", self)
        self.addAction(self.action_settings)


class ContentWidget(QScrollArea):
    def __init__(self, feeds: list[Feed]):
        super().__init__()

        self.layout = QVBoxLayout()
        self.widget = QWidget()

        for feed in feeds:
            for entry in feed:
                self.layout.addWidget(EntryFrame(entry))

        self.widget.setLayout(self.layout)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    def refresh(self):
        print("Calling 'refresh' function")


class EntryFrame(QFrame):
    def __init__(self, entry: EntryParser = None):
        super().__init__()

        self.url = QUrl(entry.link)

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText(entry.title if entry else "No Entry")
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
        #print("Opening link")
        QDesktopServices.openUrl(self.url)

