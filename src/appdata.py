import os, json
from .custom_gui import CustomPopup

class AppData:
  SECTION_APP_LINKS = "app_links"
  LINK_VIDEO = "video"
  LINK_MUSIC = "music"
  LINK_CUSTOM = "custom"
  user_path = os.path.expanduser('~')
  share_path = os.path.join(user_path, ".local/share/PCartLoader")
  settings_path = os.path.join(share_path, "settings.json")
  data = {}

  def __init__(self):
    self.data = self.load_settings()

  def load_settings(self):
    try:
      with open(self.settings_path, "r") as f:
        data = json.load(f)
      print("appdata settings loaded")
      return data
    except FileNotFoundError:
      CustomPopup("Error", f"The settings file could not be found at {self.settings_path}").exec()
    except Exception:
      CustomPopup("Error", f"The settings file at {self.settings_path} could not be read.").exec()
    return {}

  def init_folders(self):
    if not os.path.exists(self.share_path):
      os.makedirs(self.share_path, exist_ok=True)

  def init_settings(self):
    if not os.path.exists(self.settings_path):
      data = {
        "app_links": {
          "video": "",
          "music": "",
          "custom": {
          }
        }
      }
      try:
        with open(self.settings_path, "x") as f:
          json.dump(data, f, indent=2)
      except Exception:
        CustomPopup("Error", f"Could not initialize settings file {self.settings_path}").exec()

  def save_settings(self, video = "", music = "", custom = {}):
    settings_json = {
      "app_links": {
        "video": video,
        "music": music,
        "custom": custom
      }
    }
    try:
      with open(self.settings_path, "w") as f:
        json.dump(settings_json, f, indent=2)
      CustomPopup("Save Complete", "Settings saved to appdata folder").exec()
    except Exception:
      CustomPopup("Error", f"Could not update file {self.settings_path}").exec()