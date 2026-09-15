from PySide6.QtWidgets import *

class CustomPopup(QDialog):
  def __init__(self, title, msg):
    super().__init__()
    self.setWindowTitle(title)
    button_ok = QPushButton()
    button_ok.setText("Okay")
    button_ok.clicked.connect(self.close)
    layout = QVBoxLayout()
    layout.addWidget(QLabel(msg))
    layout.addWidget(button_ok)
    self.setLayout(layout)