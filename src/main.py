import sys, os, subprocess, threading, atexit
from queue import Queue
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .appdata import AppData
from .ui_settings_window import SettingsWindow
from .ui_config_window import ConfigWindow
from .pcart.loader import Loader
from .pcart.classes import Cartridge, LoadedCart, QueueWorker
from .pcart.cart_finder import CartManager

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
  menu: QMenu = None
  loader: Loader = None
  loader_thread: threading.Thread = None
  queue_thread: QThread = None
  queue: Queue = None
  worker: QueueWorker = None

  def __init__(self, app: QApplication):
    super().__init__()
    self.setIcon(QIcon(os.path.join(self.base_dir, 'icon.png')))
    self.setVisible(True)
    self.setToolTip('PCart Loader')
    self.menu = TopMenu(app)
    self.setContextMenu(self.menu)
    self.queue = Queue()
    self.loader = Loader(self.queue)
    self.worker = QueueWorker(self.queue)
    self.worker.item_received.connect(self.on_item_received)
    self.queue_thread = QThread()
    atexit.register(self.on_exit)
  
  def on_exit(self):
    self.worker.stop()
    self.queue_thread.quit()
    self.queue_thread.wait()
  
  def on_item_received(self, item: dict):
    match item["action"]:
      case "add":
        print("adding cart")
        self.on_cart_added(item["cart"])
      case "remove":
        print("removing cart")
        self.on_cart_removed(item["cart"])

  def on_cart_added(self, lcart):
    print("add item received from queue")
    cart_action = self.menu.carts_menu.addAction(lcart.cart.name)
    cart_action.triggered.connect(lcart.run)
  
  def on_cart_removed(self, lcart):
    print("remove item received from queue")
    cart_action: QAction = None
    for action in self.menu.carts_menu.actions():
      if action.text() == lcart.cart.name:
        cart_action = action
        break
    if cart_action:
      self.menu.carts_menu.removeAction(cart_action)
  
  def _init_settings(self):
    app_data = AppData()
    app_data.init_folders()
    app_data.init_settings()
    return app_data
  
  def _setup_settings_window(self, app_data):
    data = app_data.load_settings()
    self.menu.s_window.text_video.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_VIDEO])
    self.menu.s_window.text_music.setText(data[app_data.SECTION_APP_LINKS][app_data.LINK_MUSIC])
  
  def _get_loaded_carts(self):
    for lcart in self.loader.get_loaded():
      cart_action = self.menu.carts_menu.addAction(lcart.cart.name)
      cart_action.triggered.connect(lcart.run)

  def start(self):
    app_data = self._init_settings()
    self._setup_settings_window(app_data)
    self._get_loaded_carts()
    self.loader_thread = threading.Thread(target=self.loader.start)
    self.loader_thread.start()
    # self.thread2 = threading.Thread(target=self.worker.start)
    # self.thread2.start()
    self.worker.moveToThread(self.queue_thread)
    self.queue_thread.started.connect(self.worker.start)
    self.queue_thread.start()

# if __name__ == "__main__":
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
tray = SystemTrayIcon(app)
tray.start()
sys.exit(app.exec())

## TODO: for v1.1.0
## - still need to automount and add carts that are plugged in but not mounted at start
## - make Windows executable
## - make appimage auto updating
