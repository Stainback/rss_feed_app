import sys

from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from config import (FONT_PATH, FONT_FAMILY, FONT_SIZE, STYLES_PATH,
                    TIMER_REFRESH)
from app_model.manager import Manager
from app_view.toolbar import ActionsWidget
from app_view.content import FoldersWidget


class App(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        QFontDatabase.addApplicationFont(FONT_PATH)
        default_font = QFont(FONT_FAMILY)
        default_font.setPixelSize(FONT_SIZE)
        self.setFont(default_font)

        with open(STYLES_PATH, "r") as styles:
            self.setStyleSheet(styles.read())

        self.manager = Manager()

        self.window = AppWindow(
            app=self,
            width=self.primaryScreen().availableSize().width() * 0.25,
            height=self.primaryScreen().availableSize().height() * 0.97
        )

        self.window.show()

        timer = QTimer(self)
        timer.timeout.connect(self.window.content.refresh_active)
        timer.start(TIMER_REFRESH * 1000)

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

        self.setFixedSize(QSize(width, height))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.content = FoldersWidget(app.manager)
        self.setCentralWidget(self.content)

        self.toolbar = ActionsWidget(self)
        self.toolbar.connect_widget(
            {
                "close": self.close,
                "minimize": self.showMinimized,
                "refresh": self.content.refresh_active,
                "expand":
                    (
                        lambda: self.content.currentWidget().
                        set_all_descriptions_state(True)
                    ),
                "collapse":
                    (
                        lambda: self.content.currentWidget().
                        set_all_descriptions_state(False)
                    )
            }
        )
