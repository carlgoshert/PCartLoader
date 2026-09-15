import sys, os, subprocess, threading
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .ui_settings_window import SettingsWindow
from .ui_config_window import ConfigWindow
from .pcart.loader import Loader
from .pcart.classes import Cartridge
from .pcart.cart_finder import CartManager

## App Working Directory
base_dir = os.path.dirname(os.path.abspath(__file__))

## Background process
l = Loader()
t1 = threading.Thread(target=l.start)
t1.start()

## Application Instance
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

## System Tray Icon
if not QSystemTrayIcon.isSystemTrayAvailable():
  print("System tray is not available")
  sys.exit(1)
icon = QIcon(base_dir + "/icon.png")
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
tray.setToolTip("PCart Loader")

#Settings menu option
settingsAction = QAction("Settings")
s_window = SettingsWindow()
show_settings = lambda : s_window.window.show()
settingsAction.triggered.connect(show_settings)

#Config menu option
configAction = QAction("Create Config")
c_window = ConfigWindow()
show_configurator = lambda : c_window.window.show()
configAction.triggered.connect(show_configurator)

#Quit menu option
quitAction = QAction("Quit")
quitAction.triggered.connect(app.quit)

#System tray menu
menu = QMenu()
cartsMenu = menu.addMenu("PCarts")
menu.addAction(configAction)
menu.addAction(settingsAction)
menu.addAction(quitAction)
tray.setContextMenu(menu)

#Submenu list of preloaded cartridges
class LoadedCart:
  cart: Cartridge = None
  loader: Loader = None
  def __init__(self, cart, loader):
    self.cart = cart
    self.loader = loader
  def run(self):
    self.loader.run_cart(self.cart)

loaded_carts: list[LoadedCart] = []

## Do on app start
def _app_init():
  # make folders and settings.json if none exist
  app_data = AppData()
  app_data.init_folders()
  app_data.init_settings()
  # load settings into textboxes
  data = app_data.load_settings()
  s_window.text_video.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_VIDEO])
  s_window.text_music.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_MUSIC])
  # get carts already attached
  for cart in l.get_attached():
    lcart = LoadedCart(cart, l)
    cartAction = cartsMenu.addAction(cart.name)
    cartAction.triggered.connect(lcart.run)
    loaded_carts.append(lcart) # holding objects in memory

## Run App
_app_init()
sys.exit(app.exec())

## TODO: for v1.1.0
## - remove pcarts from dropdown when disconnected
## - add pcarts to dropdown when connected
## - make Windows executable
## - make appimage auto updating
