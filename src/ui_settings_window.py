import os
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .custom_gui import CustomLinkWidget

class SettingsWindow:
  window: QMainWindow = None
  save_button: QPushButton = None
  text_video: QLineEdit = None
  text_music: QLineEdit = None
  custom_links: list[CustomLinkWidget] = []
  app_data: AppData

  def __init__(self, app_d: AppData):
    self.app_data = app_d
    loader = QUiLoader()
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SettingsWindow.ui")
    self.window = loader.load(ui_path, None)
    self.text_video = self.window.findChild(QLineEdit, "lineEditVideo")
    self.text_music = self.window.findChild(QLineEdit, "lineEditAudio")
    self.window.findChild(QPushButton, "buttonSave").clicked.connect(self._on_save_button_click)
    self.window.findChild(QPushButton, "buttonAdd").clicked.connect(self._on_add_button_click)
    self._get_custom_links_from_settings()
  
  def _get_custom_links_from_settings(self):
    data = self.app_data.data
    if self.app_data.SECTION_APP_LINKS in data:
      if self.app_data.LINK_CUSTOM in data[self.app_data.SECTION_APP_LINKS]:
        custom = data[self.app_data.SECTION_APP_LINKS][self.app_data.LINK_CUSTOM]
        for ty, ln in custom.items():
          link_widget = CustomLinkWidget(self.window)
          link_widget.button_delete.clicked.connect(lambda : self._on_delete_button_clicked(False, link_widget.button_delete))
          link_widget.line_type.setText(ty)
          link_widget.line_link.setText(ln)
          self.custom_links.append(link_widget)
          self.window.findChild(QVBoxLayout, "vertCustom").insertWidget(0, link_widget)

  def _on_save_button_click(self):
    custom = {}
    for link_widget in self.custom_links:
      custom[link_widget.line_type.text()] = link_widget.line_link.text()
    self.app_data.save_settings(video=self.text_video.text(), music=self.text_music.text(), custom=custom)

  def _on_add_button_click(self):
    link_widget = CustomLinkWidget(self.window)
    link_widget.button_delete.clicked.connect(lambda : self._on_delete_button_clicked(False, link_widget.button_delete))
    self.custom_links.append(link_widget)
    self.window.findChild(QVBoxLayout, "vertCustom").insertWidget(0, link_widget)
  
  def _on_delete_button_clicked(self, _checked, caller):
    for link_widget in self.custom_links:
      if link_widget.button_delete == caller:
        self.custom_links.remove(link_widget)
        link_widget.hide()
        link_widget.deleteLater()
