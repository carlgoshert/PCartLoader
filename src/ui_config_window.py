import os, configparser
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .custom_gui import CustomPopup

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

class ConfigWindow:
  cart_dir: str = ""
  window: QMainWindow = None
  button_save: QPushButton = None
  button_target: QPushButton = None
  text_preview: QTextEdit = None
  line_name: QLineEdit = None
  line_target: QLineEdit = None
  line_args: QLineEdit = None
  combo_type: QComboBox = None
  custom_box: CustomBoxWidget = None

  def __init__(self):
    loader = QUiLoader()
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ConfigWindow.ui")
    self.window = loader.load(ui_path, None)
    self.text_preview = self.window.findChild(QTextEdit, "textEditPreview")
    self.line_name = self.window.findChild(QLineEdit, "lineEditName")
    self.line_name.textChanged.connect(self._on_text_changed)
    self.line_target = self.window.findChild(QLineEdit, "lineEditTarget")
    self.line_target.textChanged.connect(self._on_text_changed)
    self.line_args = self.window.findChild(QLineEdit, "lineEditArgs")
    self.line_args.textChanged.connect(self._on_text_changed)
    self.combo_type = self.window.findChild(QComboBox, "comboType")
    self.combo_type.addItems(["exe", "video", "music", "custom"])
    self.combo_type.currentTextChanged.connect(self._on_type_changed)
    self.window.findChild(QPushButton, "buttonDrive").clicked.connect(self._on_drive_button_clicked)
    self.window.findChild(QPushButton, "buttonLoad").clicked.connect(self._on_load_button_clicked)
    self.button_save = self.window.findChild(QPushButton, "buttonSave")
    self.button_save.clicked.connect(self._on_save_button_clicked)
    self.button_target = self.window.findChild(QPushButton, "buttonTarget")
    self.button_target.clicked.connect(self._on_target_button_clicked)
    self.custom_box = CustomBoxWidget(self.window, self._on_text_changed)
    self.window.findChild(QVBoxLayout, "vertLineEdits").addWidget(self.custom_box)
    self.custom_box.hide()
  
  def _on_text_changed(self, text):
    self._update_preview()
  
  def _on_type_changed(self, text):
    self._update_preview()
    if text == "custom":
      self.custom_box.show()
    else:
      self.custom_box.hide()

  def _unlock_controls(self):
    self.button_save.setEnabled(True)
    self.button_target.setEnabled(True)
    self.line_name.setEnabled(True)
    self.line_args.setEnabled(True)
    self.combo_type.setEnabled(True)
  
  def _open_folder_dialog(self):
    dialog = QFileDialog(self.window)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_drive_button_clicked(self):
    folder = self._open_folder_dialog()
    if folder:
      print(folder)
      self._unlock_controls()
      self.cart_dir = folder
    
  def _open_load_dialog(self):
    dialog = QFileDialog(self.window)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    if dialog.exec():
      file = dialog.selectedFiles()[0]
      folder = os.path.dirname(file)
      return file, folder
  
  def _update_controls(self, config):
    self.line_name.setText(config["cartridge"]["name"].replace("\"", ""))
    self.line_target.setText(config["cartridge"]["target"].replace("\"", ""))
    self.line_args.setText(config["cartridge"]["args"].replace("\"", ""))
    match config["cartridge"]["type"].replace("\"", ""):
      case "exe":
        self.combo_type.setCurrentIndex(0)
      case "video":
        self.combo_type.setCurrentIndex(1)
      case "music":
        self.combo_type.setCurrentIndex(2)
      case _:
        self.combo_type.setCurrentIndex(3)
        self.custom_box.show()
        self.custom_box.line_type.setText(config["cartridge"]["type"].replace("\"", ""))
  
  def _update_preview(self):
    cart_name = self.line_name.text()
    cart_target = self.line_target.text()
    cart_args = self.line_args.text()
    cart_type = self.combo_type.currentText() if self.combo_type.currentText() != "custom" else self.custom_box.line_type.text()
    preview = '''
    [cartridge]
    name = {name}
    target = {target}
    args = {args}
    type = {type}
    '''.format(name=cart_name, target=cart_target, args=cart_args, type=cart_type)
    self.text_preview.setText(preview)

  def _on_load_button_clicked(self):
    file, folder = self._open_load_dialog()
    if file:
      config = configparser.ConfigParser()
      config.read(file)
      self._unlock_controls()
      self._update_controls(config)
      self._update_preview()
      self.cart_dir = folder
  
  def _on_save_button_clicked(self):
    cart_name = self.line_name.text()
    cart_target = self.line_target.text()
    cart_args = self.line_args.text()
    cart_type = self.combo_type.currentText() if self.combo_type.currentText() != "custom" else self.custom_box.line_type.text()
    out_path = os.path.join(self.cart_dir, "cartridge.ini")
    config = configparser.ConfigParser()
    config.add_section("cartridge")
    config.set("cartridge", "name", cart_name)
    config.set("cartridge", "target", cart_target)
    config.set("cartridge", "args", cart_args)
    config.set("cartridge", "type", cart_type)
    if not os.path.exists(out_path):
      with open(out_path, 'x') as f:
        config.write(f)
    else:
      with open(out_path, 'w') as f:
        config.write(f)
    popup = CustomPopup("Config File Creator", "Config file has been saved: cartridge.ini")
    popup.exec()
  
  def _open_file_dialog(self):
    dialog = QFileDialog(self.window)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    dialog.setDirectory(self.cart_dir)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_target_button_clicked(self):
    target = self._open_file_dialog()
    if target:
      target = target.replace(self.cart_dir, '')
      self.line_target.setText(target)
