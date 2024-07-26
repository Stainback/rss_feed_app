import sys
import webbrowser

from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QFont, QFontDatabase, QPalette
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, \
    QScrollArea, QToolBar, QLabel, QPushButton, QHBoxLayout, QLineEdit, \
    QDialog, QDialogButtonBox, QApplication, QToolButton, QTabWidget

from feed import Entry
from manager import AppManager


class App(QApplication):
    TIMER_REFRESH = 60  # in seconds

    def __init__(self):
        super().__init__(sys.argv)

        QFontDatabase.addApplicationFont("fonts/UbuntuMono-Regular.ttf")
        default_font = QFont("Ubuntu Mono")
        default_font.setPixelSize(16)
        self.setFont(default_font)

        with open("css/styles.css", "r") as styles_file:
            self.setStyleSheet(styles_file.read())

        self.manager = AppManager()

        self.window = AppWindow(
            app=self,
            width=self.primaryScreen().availableSize().width() * 0.25,
            height=self.primaryScreen().availableSize().height() * 0.97
        )

        self.window.show()

        timer = QTimer(self)
        timer.timeout.connect(self.window.refresh)
        timer.start(self.TIMER_REFRESH * 1000)

        self.exec()


class AppWindow(QMainWindow):
    def __init__(
            self,
            app: App,
            width: int,
            height: int
    ):
        super().__init__()

        self.app = app

        self.setWindowTitle("RSS Feed")
        self.setFixedSize(QSize(width, height))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.content = ContentWidget(self.app.manager.get_entries(), self)
        self.refresh()
        self.layout.addWidget(self.content)
        self.setCentralWidget(self.content)

        self.toolbar = ActionsWidget()
        self.toolbar.action_add.triggered.connect(lambda: self.dialog.exec())
        self.toolbar.action_refresh.triggered.connect(self.refresh)
        self.addToolBar(self.toolbar)

        self.dialog = UrlDialog(self)
        self.dialog.submitted_url.connect(self.add_rss)

    def add_rss(self, url: str):
        self.app.manager.add_feed_to_db(url)
        self.refresh()

    def refresh(self):
        self.app.manager.update_feeds()
        self.content.update_content(self.app.manager.get_entries())


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.initial_pos = None

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        self.layout.addWidget(self.title)

        self.min_button = QToolButton(self)
        self.min_button.clicked.connect(self.window().showMinimized)

        self.close_button = QToolButton(self)
        self.close_button.clicked.connect(self.window().close)

        for button in (self.min_button, self.close_button):
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 28))
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
            self.layout.addWidget(button)


class ActionsWidget(QToolBar):
    def __init__(self):
        super().__init__()

        self.action_add = QAction("Add RSS", self)
        self.addAction(self.action_add)

        self.action_refresh = QAction("Refresh", self)
        self.addAction(self.action_refresh)


class FoldersBar(QTabWidget):
    def __init__(self, folders: list[str]):
        super().__init__()

        self.setTabBarAutoHide(True)
        self.setUsesScrollButtons(True)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)


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
        self.url_box.clear()
        super().accept()


class ContentWidget(QScrollArea):
    def __init__(self, entries: list[Entry], parent=None):
        super().__init__(parent)
        self.setObjectName("ContentWidget")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.parent = parent
        self.layout = QVBoxLayout()

        self.widget = QWidget()
        self.widget.setObjectName("ContentWidget")
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.content = []
        self.update_content(entries)

    def update_content(self, entries: list[Entry]):
        ids = [entry.id for entry in self.content]
        for i in range(len(entries)):
            if entries[i].id not in ids:
                entry_widget = EntryFrame(entries[i], self)
                self.content.append(entry_widget)
                self.layout.insertWidget(i, entry_widget)


class EntryFrame(QFrame):
    def __init__(self, entry: Entry = None, parent=None):
        super().__init__(parent)

        self.id = entry.id
        self.url = entry.url

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText(
            str(entry) if entry else "No Title"
        )
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.button_widget = QWidget()
        self.layout.addWidget(self.button_widget)

        self.button_layout = QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        self.link_button = QPushButton()
        self.link_button.setObjectName("EntryLinkButton")
        self.link_button.setFlat(True)
        self.link_button.setText("Read it")
        self.button_layout.addWidget(self.link_button)
        self.link_button.clicked.connect(self.open_link)

        self.expand_button = QPushButton("Expand")
        self.expand_button.setObjectName("EntryExpandButton")
        self.expand_button.setFlat(True)
        self.button_layout.addWidget(self.expand_button)
        self.expand_button.clicked.connect(self.change_description_state)

        self.description_label = QLabel()
        self.description_label.setObjectName("EntryDescriptionLabel")
        self.description_label.setText(
            entry.description if entry else "No Description"
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
