from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QMainWindow


class ActionsWidget(QToolBar):
    def __init__(self, app: QMainWindow):
        super().__init__(app)

        self.position = None

        self.actions = {
            "close": QAction("X", self),
            "minimize": QAction("_", self),
            "refresh": QAction("R", self),
            "manage": QAction("M", self),
            "expand": QAction("⌄", self),
            "collapse": QAction("⌃", self)
        }

        for action in self.actions.values():
            self.addAction(action)

        self.setOrientation(Qt.Orientation.Vertical)
        self.setMovable(False)
        app.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self)

    def connect_widget(self, commands: dict):
        for command in commands.keys():
            action = self.actions.get(command)
            if action:
                action.triggered.connect(commands.get(command))

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.position = a0.position().toPoint()
        super().mousePressEvent(a0)
        a0.accept()

    def mouseMoveEvent(self, a0):
        if self.position is not None:
            delta = a0.position().toPoint() - self.position
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y()
            )
        super().mouseMoveEvent(a0)
        a0.accept()

    def mouseReleaseEvent(self, a0):
        self.position = None
        super().mouseReleaseEvent(a0)
        a0.accept()
