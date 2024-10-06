import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QDialog, QDialogButtonBox, 
                             QMainWindow, QListView, QPushButton, QSizePolicy)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex
from DB import get_current_tasks
from dataModels.tasksDataModel import Tasks, Task


class EuroplastTechDesktop(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EuroplastTechDesktop")
        self.setGeometry(100, 100, 800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.mainLayout = QHBoxLayout(centralWidget)

        self.burgerButton = CustomBtn("☰")
        self.burgerButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.burgerButton.clicked.connect(self.toggle_menu)

        self.mainLayout.addWidget(self.burgerButton)

        self.menuContainer = QWidget()
        self.menuLayout = QVBoxLayout(self.menuContainer)

        self.menuLayout.setSpacing(20)
        self.menuButton1 = QPushButton("Меню 1")
        self.menuButton2 = QPushButton("Меню 2")
        self.menuButton3 = QPushButton("Меню 3")

        self.menuLayout.addWidget(self.menuButton1)
        self.menuLayout.addWidget(self.menuButton2)
        self.menuLayout.addWidget(self.menuButton3)
        self.menuLayout.addStretch(100)
        self.menuContainer.setFixedWidth(150)
        self.menuContainer.hide()

        self.mainLayout.addWidget(self.menuContainer)

        self.tasksListView = QListView()
        self.tasksModel = QStandardItemModel()
        self.tasksListView.setModel(self.tasksModel)

        self._data = get_current_tasks()
        self.tasks = [Task(**task_data) for task_data in self._data]

        for task in self.tasks:
            item = QStandardItem(task.task)
            self.tasksModel.appendRow(item)

        self.tasksListView.clicked.connect(self.on_task_selected)

        self.mainLayout.addWidget(self.tasksListView)

    def toggle_menu(self):
        if self.menuContainer.isVisible():
            self.menuContainer.hide()
        else:
            self.menuContainer.show()

    def on_task_selected(self, index: QModelIndex):
        if index.isValid():
            selected_task = self.tasks[index.row()]
            print(f"Выбрана задача: {selected_task.task}, статус: {selected_task.status}")


class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()

        self.message = message
        self.setWindowTitle("Уведомление!")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(self.message)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class CustomBtn(QPushButton): 
    def __init__(self, text: str = 'btn', width: int = 100, height: int = 50):
        super().__init__()

        self.setStyleSheet(
            "QPushButton {background-color: rgb(255, 0, 255); border-radius: 20px;}"
        )
        self.setText(text)
        self.setFixedSize(width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EuroplastTechDesktop()
    window.show()
    sys.exit(app.exec())
    