import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLayout, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QScrollArea,
    QTabWidget, QLabel, QPushButton, QApplication, QMainWindow
)

from app_model.feed import Entry, Feed
from app_model.manager import Manager

"""
    Basic components
"""


class EntryButton(QPushButton):
    def __init__(
            self,
            layout: QLayout,
            name: str = "EntryButton",
            text: str = "",
    ):
        super().__init__()

        self.setObjectName(name)
        self.setFlat(True)
        self.setText(text)
        layout.addWidget(self)


class EntryLabel(QLabel):
    def __init__(
            self,
            layout: QLayout,
            name: str = "EntryLabel",
            text: str = ""
    ):
        super().__init__()

        self.setObjectName(name)
        self.setWordWrap(True)
        self.setText(text)
        layout.addWidget(self)


"""
    Content components
"""


class EntryFrame(QFrame):
    def __init__(self, entry: Entry, parent=None):
        super().__init__(parent)

        self.id = entry.id
        self.url = entry.url

        self.setObjectName("Entry")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = EntryLabel(layout=self.layout, text=str(entry))

        self.button_widget = QWidget()
        self.layout.addWidget(self.button_widget)

        self.button_layout = QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        self.link_button = EntryButton(
            layout=self.button_layout, name="EntryLinkButton", text="Read it"
        )
        self.link_button.clicked.connect(self.open_link)

        self.expand_button = EntryButton(
            layout=self.button_layout, name="EntryExpandButton"
        )
        self.expand_button.clicked.connect(
            lambda: self.set_description_state()
        )

        self.description_label = EntryLabel(
            layout=self.layout, name="EntryDescriptionLabel",
            text=entry.description
        )
        self.is_expanded = None
        self.set_description_state(False)

    def set_description_state(self, state: bool = None):
        if state is None:
            self.is_expanded = not self.is_expanded
        else:
            self.is_expanded = state
        self.description_label.setMaximumHeight(500 if self.is_expanded else 0)
        self.expand_button.setText("⌃" if self.is_expanded else "⌄")

    def open_link(self):
        wb = webbrowser.get()
        wb.open_new_tab(self.url)


class ContentWidget(QScrollArea):
    def __init__(self, entries: list[Entry], parent=None):
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

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

    def set_all_descriptions_state(self, state: bool):
        for entry in self.content:
            entry.set_description_state(state)


class FoldersWidget(QTabWidget):
    def __init__(self, manager: Manager, parent=None):
        super().__init__(parent)

        self.manager = manager

        for folder, entries in self.manager.get_folders().items():
            self.addTab(ContentWidget(entries), folder)

        self.currentChanged.connect(self.refresh_active)

    def refresh_active(self):
        active = self.tabText(self.currentIndex())
        self.currentWidget().update_content(
            self.manager.get_entries(active if active != "All feeds" else None)
        )

    def add_folder(self, folder: str):
        self.addTab(ContentWidget(self.manager.get_entries(folder)), folder)

    def remove_folder(self, folder: str):
        for i in range(self.count()):
            if self.tabText(i) == folder:
                self.removeTab(i)
                return
