from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RSS Feed")


class Content(QMainWindow):
    def __init__(self):
        super().__init__()


class SettingsButton(QPushButton):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()

    window.show()
    app.exec()

