import os, configparser, logging
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from ..custom_gui import CustomPopup, CustomBoxWidget, CustomDialog

class StartWidget:
  widget: QWidget = None
  _button_new: QPushButton = None
  _button_load: QPushButton = None
  _file_callback = None
  _folder_callback = None

  def __init__(self, file_cb, folder_cb):
    self._file_callback = file_cb
    self._folder_callback = folder_cb
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ConfigWindowStart.ui")
    self.widget = QUiLoader().load(ui_path, None)
    self._button_new = self.widget.findChild(QPushButton, "buttonNew")
    self._button_new.clicked.connect(self._on_drive_button_clicked)
    self._button_load = self.widget.findChild(QPushButton, "buttonLoad")
    self._button_load.clicked.connect(self._on_load_button_clicked)
      
  def _open_folder_dialog(self):
    dialog = CustomDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_drive_button_clicked(self):
    folder = self._open_folder_dialog()
    if folder:
      logging.info(f"Starting new config file at {folder}")
      self._cart_dir = folder
      self._folder_callback(folder)
    else:
      logging.warning(F"Folder selection canceled or could not be completed. {folder}")
    
  def _open_file_dialog(self):
    dialog = QFileDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_load_button_clicked(self):
    file = self._open_file_dialog()
    if file:
      config = configparser.ConfigParser()
      if config.read(file):
        logging.info("config file loaded succesfully.")
        # self._cart_dir = os.path.dirname(file)
        # self._update_controls(config)
        # self._update_preview()
        self._file_callback(file)
      else:
        logging.error(f"Selected file {file} could not be read.")
    else:
      logging.warning(f"File selection canceled or file {file} could not be opened.")

class PlatformWidget:
  widget: QWidget = None
  _picked_callback = None
  _button_single: QPushButton = None
  _button_multi: QPushButton = None

  def __init__(self, picked_cb):
    self._picked_callback = picked_cb
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ConfigWindowPlatform.ui")
    self.widget = QUiLoader().load(ui_path, None)
    self._button_single = self.widget.findChild(QPushButton, "buttonSingle")
    self._button_single.clicked.connect(self._on_single_button_clicked)
    self._button_multi = self.widget.findChild(QPushButton, "buttonMulti")
    self._button_multi.clicked.connect(self._on_multi_button_clicked)
  
  def _on_single_button_clicked(self):
    self._picked_callback("single")
  
  def _on_multi_button_clicked(self):
    self._picked_callback("multi")

class DefaultWidget:
  widget: QWidget = None
  _save_callback = None
  _restart_callback = None
  _config_path: str = ""
  _cart_dir: str = ""
  _button_save: QPushButton = None
  _button_file: QPushButton = None
  _button_folder: QPushButton = None
  _text_preview: QTextEdit = None
  _line_name: QLineEdit = None
  _line_target: QLineEdit = None
  _line_args: QLineEdit = None
  _combo_type: QComboBox = None
  _custom_box: CustomBoxWidget = None
  _label_dir: QLabel = None
  _button_restart: QPushButton = None

  def __init__(self, save_cb, restart_cb, file):
    self._save_callback = save_cb
    self._restart_callback = restart_cb
    self._config_path = file
    self._cart_dir = os.path.split(file)[0]
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ConfigWindowDefault.ui")
    self.widget = QUiLoader().load(ui_path, None)
    self._text_preview = self.widget.findChild(QTextEdit, "textEditPreview")
    self._line_name = self.widget.findChild(QLineEdit, "lineEditName")
    self._line_name.textChanged.connect(self._on_text_changed)
    self._line_target = self.widget.findChild(QLineEdit, "lineEditTarget")
    self._line_target.textChanged.connect(self._on_text_changed)
    self._line_args = self.widget.findChild(QLineEdit, "lineEditArgs")
    self._line_args.textChanged.connect(self._on_text_changed)
    self._combo_type = self.widget.findChild(QComboBox, "comboType")
    self._combo_type.addItems(["exe", "video", "music", "custom"])
    self._combo_type.currentTextChanged.connect(self._on_type_changed)
    self._button_save = self.widget.findChild(QPushButton, "buttonSave")
    self._button_save.clicked.connect(self._on_save_button_clicked)
    self._button_file = self.widget.findChild(QPushButton, "buttonFile")
    self._button_file.clicked.connect(self._on_file_button_clicked)
    self._button_folder = self.widget.findChild(QPushButton, "buttonFolder")
    self._button_folder.clicked.connect(self._on_folder_button_clicked)
    self._custom_box = CustomBoxWidget(self.widget, self._on_text_changed)
    self.widget.findChild(QVBoxLayout, "verticalLayout").addWidget(self._custom_box)
    self._label_dir = self.widget.findChild(QLabel, "labelDir")
    self._custom_box.hide()
    self._button_restart = self.widget.findChild(QPushButton, "buttonRestart")
    self._button_restart.clicked.connect(self._on_restart_button_clicked)
    self._update_controls()
  
  def _on_text_changed(self, text):
    self._update_preview()
  
  def _on_type_changed(self, text):
    self._update_preview()
    if text == "custom":
      self._custom_box.show()
    else:
      self._custom_box.hide()
  
  def _update_controls(self):
    config = configparser.ConfigParser()
    if config.read(self._config_path):
      self._label_dir.setText(self._cart_dir)
      if "cartridge" in config:
        self._line_name.setText(config["cartridge"]["name"])
        self._line_target.setText(config["cartridge"]["target"])
        self._line_args.setText(config["cartridge"]["args"])
        if "type" in config["cartridge"]:
          match config["cartridge"]["type"]:
            case "exe":
              self._combo_type.setCurrentIndex(0)
            case "video":
              self._combo_type.setCurrentIndex(1)
            case "music":
              self._combo_type.setCurrentIndex(2)
            case _:
              self._combo_type.setCurrentIndex(3)
              self._custom_box.show()
              self._custom_box.line_type.setText(config["cartridge"]["type"])
  
  def _update_preview(self):
    cart_name = self._line_name.text()
    cart_target = self._line_target.text()
    cart_args = self._line_args.text()
    cart_type = self._combo_type.currentText() if self._combo_type.currentText() != "custom" else self._custom_box.line_type.text()
    preview = f'''
    [cartridge]
    name = {cart_name}
    target = {cart_target}
    args = {cart_args}
    type = {cart_type}
    '''
    self._text_preview.setText(preview)
  
  def _on_save_button_clicked(self):
    cart_name = self._line_name.text()
    cart_target = self._line_target.text()
    cart_args = self._line_args.text()
    cart_type = self._combo_type.currentText() if self._combo_type.currentText() != "custom" else self._custom_box.line_type.text()
    out_path = self._config_path
    config = configparser.ConfigParser()
    config.add_section("cartridge")
    config.set("cartridge", "name", cart_name)
    config.set("cartridge", "target", cart_target)
    config.set("cartridge", "args", cart_args)
    config.set("cartridge", "type", cart_type)
    try:
      mode = 'x' if not os.path.exists(out_path) else 'w'
      with open(out_path, mode) as f:
        config.write(f)
      CustomPopup("config File Creator", "config file has been saved: cartridge.ini").exec()
      logging.info(f"config file saved to {out_path}")
    except Exception as ex:
      CustomPopup("Error", f"Could not write to config file {out_path}.\n{ex}")
      logging.error(f"Could not write to config file at {out_path}")
    self._save_callback()
  
  def _open_file_dialog(self):
    dialog = CustomDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setDirectory(self._cart_dir)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_file_button_clicked(self):
    target = self._open_file_dialog()
    if target:
      target = target.replace(self._cart_dir, '')
      if target[0] == '/':
        target = target[1:]
      self._line_target.setText(target)
  
  def _open_folder_dialog(self):
    dialog = CustomDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_folder_button_clicked(self):
    target = self._open_folder_dialog()
    if target:
      target = target.replace(self._cart_dir, '')
      if target[0] == '/':
        target = target[1:]
      self._line_target.setText(target)

  def _on_restart_button_clicked(self):
    self._restart_callback()

class MultiWidget:
  widget: QWidget = None
  _save_callback = None
  _restart_callback = None
  _config_path: str = ""
  _cart_dir: str = ""
  _button_file_lin: QPushButton = None
  _button_file_win: QPushButton = None
  _button_folder_lin: QPushButton = None
  _button_folder_win: QPushButton = None
  _line_name_lin: QLineEdit = None
  _line_name_win: QLineEdit = None
  _line_target_lin: QLineEdit = None
  _line_target_win: QLineEdit = None
  _line_args_lin: QLineEdit = None
  _line_args_win: QLineEdit = None
  _combo_type_lin: QComboBox = None
  _combo_type_win: QComboBox = None
  _custom_box_lin: CustomBoxWidget = None
  _custom_box_win: CustomBoxWidget = None
  _button_save: QPushButton = None
  _text_preview: QTextEdit = None
  _label_dir: QLabel = None
  _button_restart: QPushButton = None

  def __init__(self, save_cb, restart_cb, file):
    self._save_callback = save_cb
    self._restart_callback = restart_cb
    self._config_path = file
    self._cart_dir = os.path.split(file)[0]
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ConfigWindowMulti.ui")
    self.widget = QUiLoader().load(ui_path, None)

    self._line_name_lin = self.widget.findChild(QLineEdit, "lineEditName")
    self._line_name_lin.textChanged.connect(self._on_text_changed)
    self._line_name_win = self.widget.findChild(QLineEdit, "lineEditName_2")
    self._line_name_win.textChanged.connect(self._on_text_changed)
    self._line_target_lin = self.widget.findChild(QLineEdit, "lineEditTarget")
    self._line_target_lin.textChanged.connect(self._on_text_changed)
    self._line_target_win = self.widget.findChild(QLineEdit, "lineEditTarget_2")
    self._line_target_win.textChanged.connect(self._on_text_changed)
    self._line_args_lin = self.widget.findChild(QLineEdit, "lineEditArgs")
    self._line_args_lin.textChanged.connect(self._on_text_changed)
    self._line_args_win = self.widget.findChild(QLineEdit, "lineEditArgs_2")
    self._line_args_win.textChanged.connect(self._on_text_changed)
    self._combo_type_lin = self.widget.findChild(QComboBox, "comboType")
    self._combo_type_lin.addItems(["exe", "video", "music", "custom"])
    self._combo_type_win = self.widget.findChild(QComboBox, "comboType_2")
    self._combo_type_win.addItems(["exe", "video", "music", "custom"])
    self._combo_type_lin.currentTextChanged.connect(self._on_type_changed)
    self._combo_type_win.currentTextChanged.connect(self._on_type_changed)
    self._button_file_lin = self.widget.findChild(QPushButton, "buttonFile")
    self._button_file_lin.clicked.connect(self._on_file_button_clicked)
    self._button_file_win = self.widget.findChild(QPushButton, "buttonFile_2")
    self._button_file_win.clicked.connect(self._on_file_button_clicked)
    self._button_folder_lin = self.widget.findChild(QPushButton, "buttonFolder")
    self._button_folder_lin.clicked.connect(self._on_folder_button_clicked)
    self._button_folder_win = self.widget.findChild(QPushButton, "buttonFolder_2")
    self._button_folder_win.clicked.connect(self._on_folder_button_clicked)
    self._custom_box_lin = CustomBoxWidget(self.widget, self._on_text_changed)
    self.widget.findChild(QVBoxLayout, "verticalLayout").addWidget(self._custom_box_lin)
    self._custom_box_win = CustomBoxWidget(self.widget, self._on_text_changed)
    self.widget.findChild(QVBoxLayout, "verticalLayout_2").addWidget(self._custom_box_win)

    self._text_preview = self.widget.findChild(QTextEdit, "textEditPreview")
    self._button_save = self.widget.findChild(QPushButton, "buttonSave")
    self._button_save.clicked.connect(self._on_save_button_clicked)
    self._label_dir = self.widget.findChild(QLabel, "labelDir")
    self._custom_box_lin.hide()
    self._button_restart = self.widget.findChild(QPushButton, "buttonRestart")
    self._button_restart.clicked.connect(self._on_restart_button_clicked)
    self._update_controls()
  
  def _on_text_changed(self, text):
    self._update_preview()
  
  def _on_type_changed(self, text):
    self._update_preview()
    box = self._custom_box_lin if self.widget.findChild(QTabWidget, "tabWidget").currentIndex() == 0 else self._custom_box_win
    if text == "custom":
      box.show()
    else:
      box.hide()
  
  def _update_controls(self):
    config = configparser.ConfigParser()
    if config.read(self._config_path):
      self._label_dir.setText(self._cart_dir)
      if "linux" in config:
        self._line_name_lin.setText(config["linux"]["name"])
        self._line_target_lin.setText(config["linux"]["target"])
        self._line_args_lin.setText(config["linux"]["args"])
        if "type" in config["linux"]:
          match config["linux"]["type"]:
            case "exe":
              self._combo_type_lin.setCurrentIndex(0)
            case "video":
              self._combo_type_lin.setCurrentIndex(1)
            case "music":
              self._combo_type_lin.setCurrentIndex(2)
            case _:
              self._combo_type_lin.setCurrentIndex(3)
              self._custom_box_lin.show()
              self._custom_box_lin.line_type.setText(config["linux"]["type"])
      if "windows" in config:
        self._line_name_win.setText(config["windows"]["name"])
        self._line_target_win.setText(config["windows"]["target"])
        self._line_args_win.setText(config["windows"]["args"])
        if "type" in config["windows"]:
          match config["windows"]["type"]:
            case "exe":
              self._combo_type_win.setCurrentIndex(0)
            case "video":
              self._combo_type_win.setCurrentIndex(1)
            case "music":
              self._combo_type_win.setCurrentIndex(2)
            case _:
              self._combo_type_win.setCurrentIndex(3)
              self._custom_box_win.show()
              self._custom_box_win.line_type.setText(config["windows"]["type"])
  
  def _update_preview(self):
    lin_name = self._line_name_lin.text()
    win_name = self._line_name_win.text()
    lin_target = self._line_target_lin.text()
    win_target = self._line_target_win.text()
    lin_args = self._line_args_lin.text()
    win_args = self._line_args_win.text()
    lin_type = self._combo_type_lin.currentText() if self._combo_type_lin.currentText() != "custom" else self._custom_box_lin.line_type.text()
    win_type = self._combo_type_win.currentText() if self._combo_type_win.currentText() != "custom" else self._custom_box_win.line_type.text()
    preview = f'''
    [linux]
    name = {lin_name}
    target = {lin_target}
    args = {lin_args}
    type = {lin_type}

    [windows]
    name = {win_name}
    target = {win_target}
    args = {win_args}
    type = {win_type}
    '''
    self._text_preview.setText(preview)
  
  def _on_save_button_clicked(self):
    lin_name = self._line_name_lin.text()
    win_name = self._line_name_win.text()
    lin_target = self._line_target_lin.text()
    win_target = self._line_target_win.text()
    lin_args = self._line_args_lin.text()
    win_args = self._line_args_win.text()
    lin_type = self._combo_type_lin.currentText() if self._combo_type_lin.currentText() != "custom" else self._custom_box_lin.line_type.text()
    win_type = self._combo_type_win.currentText() if self._combo_type_win.currentText() != "custom" else self._custom_box_win.line_type.text()
    out_path = self._config_path
    config = configparser.ConfigParser()
    config.add_section("linux")
    config.set("linux", "name", lin_name)
    config.set("linux", "target", lin_target)
    config.set("linux", "args", lin_args)
    config.set("linux", "type", lin_type)
    config.add_section("windows")
    config.set("windows", "name", win_name)
    config.set("windows", "target", win_target)
    config.set("windows", "args", win_args)
    config.set("windows", "type", win_type)
    try:
      mode = 'x' if not os.path.exists(out_path) else 'w'
      with open(out_path, mode) as f:
        config.write(f)
      CustomPopup("Config File Creator", "config file has been saved: cartridge.ini").exec()
      logging.info(f"config file saved to {out_path}")
    except Exception as ex:
      CustomPopup("Error", f"Could not write to config file {out_path}.\n{ex}")
      logging.error(f"Could not write to config file at {out_path}")
    self._save_callback()
  
  def _open_file_dialog(self):
    dialog = CustomDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setDirectory(self._cart_dir)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_file_button_clicked(self):
    target = self._open_file_dialog()
    if target:
      target = target.replace(self._cart_dir, '')
      if target[0] == '/':
        target = target[1:]
      match self.widget.findChild(QTabWidget, "tabWidget").currentIndex():
        case 0:
          self._line_target_lin.setText(target)
        case 1:
          self._line_target_win.setText(target)
  
  def _open_folder_dialog(self):
    dialog = CustomDialog(self.widget)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    if dialog.exec():
      return dialog.selectedFiles()[0]

  def _on_folder_button_clicked(self):
    target = self._open_folder_dialog()
    if target:
      target = target.replace(self._cart_dir, '')
      if target[0] == '/':
        target = target[1:]
      match self.widget.findChild(QTabWidget, "tabWidget").currentIndex():
        case 0:
          self._line_target_lin.setText(target)
        case 1:
          self._line_target_win.setText(target)

  def _on_restart_button_clicked(self):
    self._restart_callback()

class ConfigWindow:
  window: QMainWindow = None
  _start_widget: StartWidget = None
  _platform_widget: PlatformWidget = None
  _default_widget: DefaultWidget = None
  _multi_widget: MultiWidget = None
  _save_callback = None
  _folder_path: str = ""

  def __init__(self, save_cb):
    self._save_callback = save_cb
    self.window = QMainWindow()
    self.window.setFixedSize(800, 560)

    self._start_widget = StartWidget(self._on_file_picked, self._on_folder_picked)
    self.window.setCentralWidget(self._start_widget.widget)

  def _on_file_picked(self, file: str):
    config = configparser.ConfigParser()
    if config.read(file):
      if config.has_section("linux") or config.has_section("windows"):
        self._multi_widget = MultiWidget(self._save_callback, self._on_restart_clicked, file)
        self.window.setCentralWidget(self._multi_widget.widget)
      else:
        self._default_widget = DefaultWidget(self._save_callback, self._on_restart_clicked, file)
        self.window.setCentralWidget(self._default_widget.widget)
  
  def _on_folder_picked(self, folder: str):
    self._folder_path = folder
    self._platform_widget = PlatformWidget(self._on_platform_picked)
    self.window.setCentralWidget(self._platform_widget.widget)
  
  def _on_platform_picked(self, platform: str):
    match(platform):
      case "single":
        self._default_widget = DefaultWidget(self._save_callback, self._on_restart_clicked, os.path.join(self._folder_path, "cartridge.ini"))
        self.window.setCentralWidget(self._default_widget.widget)
      case "multi":
        self._multi_widget = MultiWidget(self._save_callback, self._on_restart_clicked, os.path.join(self._folder_path, "cartridge.ini"))
        self.window.setCentralWidget(self._multi_widget.widget)
  
  def _on_restart_clicked(self):
    self._start_widget = StartWidget(self._on_file_picked, self._on_folder_picked)
    self.window.setCentralWidget(self._start_widget.widget)
