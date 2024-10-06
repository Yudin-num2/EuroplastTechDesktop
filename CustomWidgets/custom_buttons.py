from PyQt5.QtWidgets import QPushButton


class CustomBtn(QPushButton): 
    def __init__(self, text: str = 'btn', width: int = 100, height: int = 50):
        super().__init__()

        self.setStyleSheet(
            "QPushButton {background-color: rgb(255, 0, 255); border-radius: 20px;}"
        )
        self.setText(text)
        self.setFixedSize(width, height)