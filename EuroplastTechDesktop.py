import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QLabel, QPushButton, QFileDialog, QGridLayout,
                             QDialog, QDialogButtonBox)
from parseExcel import plot_histogram_to_excel

class EuroplastTechDesktop(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None

        self.setWindowTitle("EuroplastTechDesktop")

        self.podrazdelenie = QComboBox()
        self.podrazdelenie.setCurrentText("")
        self.podrazdelenie.addItems(["Цех 5", "ОГЭ"])

        self.label = QLabel("Podrazdelenie")
        self.label.setMaximumWidth(200)

        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.open_file_dialog)

        self.file_label = QLabel("Выберите файл")
        self.file_label.setMaximumWidth(200)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.podrazdelenie, 0, 1)
        layout.addWidget(self.file_label, 1, 0)
        layout.addWidget(self.file_button, 1, 1)

        self.setLayout(layout)
        self.resize(900, 600)
        self.move(500, 300)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "*.xlsx", options=options)
        if file_name:
            self.selected_file = file_name
            try:
                plot_histogram_to_excel(self.selected_file)
                dialog = AlertDialog("""
Файл успешно изменён!
Графики добавлены на новый лист в Вашем файле!""")
                dialog.exec()
            except Exception as e:
                dialog = AlertDialog(f"Ошибка! {e}")
                dialog.exec()


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

app = QApplication(sys.argv)
window = EuroplastTechDesktop()
window.show()
sys.exit(app.exec())
