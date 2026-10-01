import importlib.metadata, os
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

class AboutWindow:
  window: QMainWindow = None
  label_version: QLabel = None
  label_icon: QLabel = None

  def __init__(self):
    loader = QUiLoader()
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AboutWindow.ui")
    self.window = loader.load(ui_path, None)
    self.label_version = self.window.findChild(QLabel, "labelVersion")
    v_number = importlib.metadata.version("PCartLoader")
    self.label_version.setText(f"version {v_number}")
    pixmap = QPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"))
    self.label_icon = self.window.findChild(QLabel, "labelIcon")
    self.label_icon.setPixmap(pixmap)
    self.label_icon.resize(pixmap.width(), pixmap.height())