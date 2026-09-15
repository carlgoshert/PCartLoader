import os
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .custom_gui import CustomPopup

class SettingsWindow:
  window: QMainWindow = None
  save_button: QPushButton = None
  text_video: QLineEdit = None
  text_music: QLineEdit = None

  def __init__(self):
    loader = QUiLoader()
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SettingsWindow.ui")
    self.window = loader.load(ui_path, None)
    self.text_video = self.window.findChild(QLineEdit, "lineEditVideo")
    self.text_music = self.window.findChild(QLineEdit, "lineEditAudio")
    self.window.findChild(QPushButton, "buttonSave").clicked.connect(self._on_save_button_click)

  def _on_save_button_click(self):
    app_data = AppData()
    app_data.save_settings(video=self.text_video.text(), music=self.text_music.text())
    popup = CustomPopup("Settings", "Settings saved to appdata folder")
    popup.exec()
