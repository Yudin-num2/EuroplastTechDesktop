import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, 
                             QMainWindow, QListView, QAction)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex
from CustomWidgets.custom_buttons import CustomBtn
from CustomWidgets.custom_dialogs import AlertDialog
from DB import get_current_tasks
from dataModels.tasksDataModel import Tasks, Task


class EuroplastTechDesktop(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EuroplastTechDesktop")
        self.setGeometry(100, 100, 800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Отчеты')

        tasks_action = QAction('Задачи', self)
        open_action = QAction('Открыть', self)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)

        # Создаем меню "Вставка"
        insert_menu = menubar.addMenu('Вставка')

        # Добавляем действия в меню "Вставка"
        paste_action = QAction('Вставить', self)
        copy_action = QAction('Копировать', self)
        insert_menu.addAction(paste_action)
        insert_menu.addAction(copy_action)

        self.statusBar().showMessage("Ready")

        self.mainLayout = QHBoxLayout(centralWidget)

        self.tasksListView = QListView()
        self.tasksModel = QStandardItemModel()
        self.tasksListView.setModel(self.tasksModel)

        self._data = get_current_tasks()
        self.tasks = [Task(**task_data) for task_data in self._data]

        for task in self.tasks:
            item = QStandardItem(f'Задача: {task.task}, статус: {task.status}')
            self.tasksModel.appendRow(item)

        self.tasksListView.clicked.connect(self.on_task_selected)

        self.mainLayout.addWidget(self.tasksListView)

    def on_task_selected(self, index: QModelIndex):
        if index.isValid():
            selected_task = self.tasks[index.row()]
            print(f"Выбрана задача: {selected_task.task}, статус: {selected_task.status}")



class FullTaskInfo(QWidget):
    def __init__(self, task: Task):
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EuroplastTechDesktop()
    window.show()
    sys.exit(app.exec())
    