import os
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .custom_gui import CustomPopup

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

class SettingsWindow:
  window: QMainWindow = None
  save_button: QPushButton = None
  text_video: QLineEdit = None
  text_music: QLineEdit = None
  custom_links: dict[CustomLinkWidget] = []

  def __init__(self):
    loader = QUiLoader()
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SettingsWindow.ui")
    self.window = loader.load(ui_path, None)
    self.text_video = self.window.findChild(QLineEdit, "lineEditVideo")
    self.text_music = self.window.findChild(QLineEdit, "lineEditAudio")
    self.window.findChild(QPushButton, "buttonSave").clicked.connect(self._on_save_button_click)
    self.window.findChild(QPushButton, "buttonAdd").clicked.connect(self._on_add_button_click)
    self._get_custom_links_from_settings()
  
  def _get_custom_links_from_settings(self):
    app_data = AppData()
    data = app_data.load_settings()
    if app_data.LINK_CUSTOM in data[app_data.SECTION_APP_LINKS]:
      custom = data[app_data.SECTION_APP_LINKS][app_data.LINK_CUSTOM]
      for ty, ln in custom.items():
        link_widget = CustomLinkWidget(self.window)
        link_widget.button_delete.clicked.connect(lambda : self._on_delete_button_clicked(False, link_widget.button_delete))
        link_widget.line_type.setText(ty)
        link_widget.line_link.setText(ln)
        self.custom_links.append(link_widget)
        self.window.findChild(QVBoxLayout, "vertCustom").insertWidget(0, link_widget)

  def _on_save_button_click(self):
    app_data = AppData()
    custom = {}
    for link_widget in self.custom_links:
      custom[link_widget.line_type.text()] = link_widget.line_link.text()
    app_data.save_settings(video=self.text_video.text(), music=self.text_music.text(), custom=custom)
    popup = CustomPopup("Settings", "Settings saved to appdata folder")
    popup.exec()

  def _on_add_button_click(self):
    link_widget = CustomLinkWidget(self.window)
    link_widget.button_delete.clicked.connect(lambda : self._on_delete_button_clicked(False, link_widget.button_delete))
    self.custom_links.append(link_widget)
    self.window.findChild(QVBoxLayout, "vertCustom").insertWidget(0, link_widget)
  
  def _on_delete_button_clicked(self, _checked, caller):
    for link_widget in self.custom_links:
      print(caller)
      print(link_widget)
      print(link_widget.button_delete)
      if link_widget.button_delete == caller:
        print(True)
        self.custom_links.remove(link_widget)
        link_widget.hide()
        link_widget.deleteLater()
