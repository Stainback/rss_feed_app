from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, QScrollArea, QLabel, QPushButton
from feed import Feed, EntryParser


class App(QMainWindow):
    def __init__(self, feeds: list[Feed], width: int = 520, height: int = 1040):
        super().__init__()

        self.setWindowTitle("RSS Feed")
        self.setFixedSize(QSize(width, height))

        self.layout = QVBoxLayout()
        self.content = ContentWidget(feeds)

        self.setLayout(self.layout)
        self.layout.addWidget(self.content)

        self.setCentralWidget(self.content)


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
        pass


class EntryFrame(QFrame):
    def __init__(self, entry: EntryParser = None):
        super().__init__()

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText(f"{entry.title} - {entry.link}" if entry else "No Entry")
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.collapse_button = QPushButton("Collapse")
        self.layout.addWidget(self.collapse_button)

        self.description_label = QLabel()
        self.description_label.setText(entry.description if entry else "No Description")
        self.description_label.setWordWrap(True)
        self.layout.addWidget(self.description_label)

    def collapse(self):
        pass

    def expand(self):
        pass
