import sys, os, subprocess, threading
from .controller import Controller
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
import json

def _app_init():
  user_path = os.path.expanduser('~')
  share_path = os.path.join(user_path, ".local/share/PCartLoader")
  if not os.path.exists(share_path):
    os.makedirs(share_path)
  settings_path = os.path.join(share_path, "settings.json")
  if not os.path.exists(settings_path):
    data = {
      "app_links": {
        "video": "",
        "music": ""
      }
    }
    with open(settings_path, "x") as f:
      json.dump(data, f, indent=2)
  else:
    global text_music
    global text_video
    with open(settings_path, "r") as f:
      data = json.load(f)
      text_music.setText(data["app_links"]["music"])
      text_video.setText(data["app_links"]["video"])

def _save_to_user_folder(file_json_dict: dict):
  user_path = os.path.expanduser('~')
  share_path = os.path.join(user_path, ".local/share/PCartLoader")
  for file in file_json_dict.keys():
    with open(os.path.join(share_path, file), "w") as f:
      json.dump(file_json_dict[file], f, indent=2)

def _save_button_on_click():
  global text_music
  global text_video
  settings_file = "settings.json"
  data = {
    "app_links": {
      "video": text_video.text(),
      "music": text_music.text()
    }
  }
  _save_to_user_folder({settings_file: data})
  print("saved settings to settings.json")

## Change Directory
base_dir = os.path.dirname(os.path.abspath(__file__))

## Subprocesses
c = Controller()
t = threading.Thread(target=c.start)
t.start()

## Application Window
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
