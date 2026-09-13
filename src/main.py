import sys, os, subprocess, threading
from .controller import Controller
from .userdata import UserData
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

user_data = UserData()

## Do on app start
def _app_init():
  # make folders and settings.json if none exist
  user_data.init_folders()
  user_data.init_settings()
  # load settings into textboxes
  global text_video
  global text_music
  data = user_data.load_settings()
  text_video.setText(data[user_data.SECTION_APP_LINKS][user_data.LINK_VIDEO])
  text_music.setText(data[user_data.SECTION_APP_LINKS][user_data.LINK_MUSIC])

def _save_button_on_click():
  global text_music
  global text_video
  user_data.save_settings(video=text_video.text(), music=text_music.text())

## Change Directory
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
loader = QUiLoader()
ui_path = os.path.join(base_dir, "SettingsWindow.ui")
window = loader.load(ui_path, None)
showWindow = lambda : window.show()
settingsAction.triggered.connect(showWindow)
save_button = window.findChild(QPushButton, "buttonSave")
save_button.clicked.connect(_save_button_on_click)
text_video = window.findChild(QLineEdit, "lineEditVideo")
text_music = window.findChild(QLineEdit, "lineEditAudio")

#Quit menu option
quitAction = QAction("Quit")
quitAction.triggered.connect(app.quit)

#System tray menu
menu = QMenu()
menu.addAction(settingsAction)
menu.addAction(quitAction)
tray.setContextMenu(menu)

## Run App
_app_init()
sys.exit(app.exec())
