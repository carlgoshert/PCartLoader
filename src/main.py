import sys, os, subprocess, threading
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from .controller import Controller
from .appdata import AppData
from .ui_settings_window import SettingsWindow
from .ui_config_window import ConfigWindow

## App Working Directory
base_dir = os.path.dirname(os.path.abspath(__file__))

## Subprocesses
c = Controller()
t = threading.Thread(target=c.start)
t.start()

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
menu.addAction(configAction)
menu.addAction(settingsAction)
menu.addAction(quitAction)
tray.setContextMenu(menu)

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

## Run App
_app_init()
sys.exit(app.exec())
