from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QDialogButtonBox



class AlertDialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.message = message
        self.title = title
        self.setWindowTitle(self.title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(self.message)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)