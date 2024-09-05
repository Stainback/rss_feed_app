from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QLineEdit, QDialog,
                             QDialogButtonBox)


class RSSManagerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
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
