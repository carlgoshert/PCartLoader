import sys, os, subprocess, threading, atexit
from queue import Queue
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

from .appdata import AppData
from .ui_settings_window import SettingsWindow
from .ui_config_window import ConfigWindow
from .ui_about_window import AboutWindow
from .pcart.cart_loader import CartLoader
from .pcart.classes import Cartridge, LoadedCart, QueueWorker
from .pcart.cart_finder import CartManager

class TopMenu(QMenu):
  carts_menu: QMenu = None
  toggle_action: QAction = None
  config_action: QAction = None
  settings_action: QAction = None
  quit_action: QAction = None
  c_window: ConfigWindow = None
  s_window: SettingsWindow = None
  a_window: AboutWindow = None

  def __init__(self, app: QApplication, app_data: AppData, save_cb):
    super().__init__()
    self.toggle_action = QAction('Disable Autostart')
    self.config_action = QAction('Create Config')
    self.c_window = ConfigWindow(save_cb)
    self.config_action.triggered.connect(lambda: self.c_window.window.show())
    self.settings_action = QAction('Settings')
    self.s_window = SettingsWindow(app_data)
    self.settings_action.triggered.connect(lambda : self.s_window.window.show())
    self.a_window = AboutWindow()
    self.about_action = QAction("About")
    self.about_action.triggered.connect(lambda : self.a_window.window.show())
    self.quit_action = QAction('Quit')
    self.quit_action.triggered.connect(app.quit)

    self.addAction(self.toggle_action)
    self.carts_menu = self.addMenu('PCarts')
    self.addAction(self.config_action)
    self.addAction(self.settings_action)
    self.addAction(self.about_action)
    self.addAction(self.quit_action)

class SystemTrayIcon(QSystemTrayIcon):
  base_dir = os.path.dirname(os.path.abspath(__file__))
  menu: TopMenu = None
  loader: CartLoader = None
  loader_thread: threading.Thread = None
  queue_thread: QThread = None
  queue: Queue = None
  worker: QueueWorker = None
  app_data = AppData()

  def __init__(self, app: QApplication):
    super().__init__()
    self.app_data.init_folders()
    self.app_data.init_settings()
    self.setIcon(QIcon(os.path.join(self.base_dir, 'icon.png')))
    self.setVisible(True)
    self.setToolTip('PCart Loader')
    self.menu = TopMenu(app, self.app_data, self._on_config_saved)
    self.setContextMenu(self.menu)
    self.menu.toggle_action.triggered.connect(self._toggle_autostart)
    self.queue = Queue()
    self.loader = CartLoader(self.queue, self.app_data)
    self.worker = QueueWorker(self.queue)
    self.worker.item_received.connect(self._on_item_received)
    self.queue_thread = QThread()
    self._get_autostart_setting()
    atexit.register(self._on_exit)
  
  def _toggle_autostart(self):
    if "Disable" in self.menu.toggle_action.text():
      self.loader.autostart_enabled = False
      self.menu.toggle_action.setText("Enable Autostart")
      self.app_data.save_setting(AppData.SECTION_GENERAL, AppData.GENERAL_AUTOSTART, "false", suppress=True)
    else:
      self.loader.autostart_enabled = True
      self.menu.toggle_action.setText("Disable Autostart")
      self.app_data.save_setting(AppData.SECTION_GENERAL, AppData.GENERAL_AUTOSTART, "true", suppress=True)
  
  def _get_autostart_setting(self):
    data = self.app_data.data
    if data[AppData.SECTION_GENERAL][AppData.GENERAL_AUTOSTART] == "false":
      self.loader.autostart_enabled = False
      self.menu.toggle_action.setText("Enable Autostart")

  def _on_exit(self):
    self.worker.stop()
    self.queue_thread.quit()
    self.queue_thread.wait()
  
  def _on_config_saved(self):
    self.menu.carts_menu.clear()
    self._get_attached_carts()

  def _on_item_received(self, item: dict):
    match item["action"]:
      case "add":
        print("adding cart")
        self._on_cart_added(item["cart"])
      case "remove":
        print("removing cart")
        self._on_cart_removed(item["cart"])

  def _on_cart_added(self, lcart):
    print("add item received from queue")
    cart_action = self.menu.carts_menu.addAction(lcart.cart.name)
    cart_action.triggered.connect(lcart.run)
  
  def _on_cart_removed(self, lcart):
    print("remove item received from queue")
    cart_action: QAction = None
    for action in self.menu.carts_menu.actions():
      if action.text() == lcart.cart.name:
        cart_action = action
        break
    if cart_action:
      self.menu.carts_menu.removeAction(cart_action)
  
  def _setup_settings_window(self):
    data = self.app_data.data
    self.menu.s_window.text_video.setText(data[self.app_data.SECTION_APP_LINKS][self.app_data.LINK_VIDEO])
    self.menu.s_window.text_music.setText(data[self.app_data.SECTION_APP_LINKS][self.app_data.LINK_MUSIC])
  
  def _get_attached_carts(self):
    self.loader.clear_attached()
    for lcart in self.loader.get_attached():
      cart_action = self.menu.carts_menu.addAction(lcart.cart.name)
      cart_action.triggered.connect(lcart.run)

  def start(self):
    self._setup_settings_window()
    self.loader_thread = threading.Thread(target=self.loader.start)
    self.loader_thread.start()
    self._get_attached_carts()
    self.worker.moveToThread(self.queue_thread)
    self.queue_thread.started.connect(self.worker.start)
    self.queue_thread.start()

tray = SystemTrayIcon(app)
tray.start()
sys.exit(app.exec())
