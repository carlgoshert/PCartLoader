from PySide6.QtWidgets import *
from PySide6.QtCore import *

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

class CustomLinkWidget(QWidget):
  line_type: QLineEdit = None
  line_link: QLineEdit = None
  button_delete: QPushButton = None

  def __init__(self, parent):
    super().__init__(parent=parent)
    h_layout = QHBoxLayout()
    h_layout.addWidget(QLabel("type"))
    self.line_type = QLineEdit(parent=self)
    h_layout.addWidget(self.line_type)
    h_layout.addWidget(QLabel("link"))
    self.line_link = QLineEdit(parent=self)
    h_layout.addWidget(self.line_link)
    self.button_delete = QPushButton("Delete")
    h_layout.addWidget(self.button_delete)
    self.setLayout(h_layout)

class CustomBoxWidget(QWidget):
  line_type: QLineEdit = None
  
  def __init__(self, parent, text_callback):
    super().__init__(parent=parent)
    h_layout = QHBoxLayout()
    h_layout.addWidget(QLabel("custom type"))
    self.line_type = QLineEdit(parent=self)
    self.line_type.textChanged.connect(text_callback)
    h_layout.addWidget(self.line_type)
    h_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
    self.setLayout(h_layout)

class CustomDialog(QFileDialog):

  def __init__(self, parent):
    super().__init__(parent=parent)
    self.setViewMode(QFileDialog.ViewMode.List)
    urls = self.sidebarUrls()
    urls.append(QUrl.fromLocalFile("/media"))
    urls.append(QUrl.fromLocalFile("/run/media"))
    self.setSidebarUrls(urls)
