import sys, os, subprocess, threading, atexit
from queue import Queue
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .ui_settings_window import SettingsWindow
from .ui_config_window import ConfigWindow
from .pcart.loader import Loader
from .pcart.classes import Cartridge
from .pcart.cart_finder import CartManager

class LoadedCart:
  cart: Cartridge = None
  loader: Loader = None

  def __init__(self, cart, loader):
    self.cart = cart
    self.loader = loader
  
  def run(self):
    self.loader.run_cart(self.cart)

class TopMenu(QMenu):
  carts_menu: QMenu = None
  config_action: QAction = None
  settings_action: QAction = None
  quit_action: QAction = None
  c_window: ConfigWindow = None
  s_window: SettingsWindow = None

  def __init__(self, app: QApplication):
    super().__init__()
    self.config_action = QAction('Create Config')
    self.c_window = ConfigWindow()
    self.config_action.triggered.connect(lambda: self.c_window.window.show())
    self.settings_action = QAction('Settings')
    self.s_window = SettingsWindow()
    self.settings_action.triggered.connect(lambda : self.s_window.window.show())
    self.quit_action = QAction('Quit')
    self.quit_action.triggered.connect(app.quit)

    self.carts_menu = self.addMenu('PCarts')
    self.addAction(self.config_action)
    self.addAction(self.settings_action)
    self.addAction(self.quit_action)

class SystemTrayIcon(QSystemTrayIcon):
  base_dir = os.path.dirname(os.path.abspath(__file__))
  loaded_carts: list[LoadedCart] = []
  menu: QMenu = None
  loader = Loader()
  thread1: threading.Thread = None

  def __init__(self, app: QApplication):
    super().__init__()
    self.setIcon(QIcon(os.path.join(self.base_dir, 'icon.png')))
    self.setVisible(True)
    self.setToolTip('PCart Loader')
    self.menu = TopMenu(app)
    self.setContextMenu(self.menu)
  
  def _init_settings(self):
    app_data = AppData()
    app_data.init_folders()
    app_data.init_settings()
    return app_data
  
  def _setup_settings_window(self, app_data):
    data = app_data.load_settings()
    self.menu.s_window.text_video.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_VIDEO])
    self.menu.s_window.text_music.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_MUSIC])

  def _get_attached_carts(self):
    for cart in self.loader.get_attached():
      lcart = LoadedCart(cart, self.loader)
      cart_action = self.menu.carts_menu.addAction(cart.name)
      cart_action.triggered.connect(lcart.run)
      self.loaded_carts.append(lcart)

  def start(self):
    app_data = self._init_settings()
    self._setup_settings_window(app_data)
    self._get_attached_carts()
    self.thread1 = threading.Thread(target=self.loader.start)
    self.thread1.start()

# if __name__ == "__main__":
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
tray = SystemTrayIcon(app)
tray.start()
sys.exit(app.exec())

## TODO: for v1.1.0
## - remove pcarts from dropdown when disconnected
## - add pcarts to dropdown when connected
## - still need to automount and add carts that are plugged in but not mounted
## - make Windows executable
## - make appimage auto updating
