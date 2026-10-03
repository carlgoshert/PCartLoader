import os, json
from .custom_gui import CustomPopup

class AppData:
  SECTION_APP_LINKS = "app_links"
  LINK_VIDEO = "video"
  LINK_MUSIC = "music"
  LINK_CUSTOM = "custom"
  SECTION_GENERAL = "general"
  GENERAL_AUTOSTART = "autostart"
  user_path = os.path.expanduser('~')
  share_path = os.path.join(user_path, ".local/share/PCartLoader")
  settings_path = os.path.join(share_path, "settings.json")
  data = {}

  def __init__(self):
    self.data = self._load_settings()

  def _load_settings(self) -> dict:
    try:
      with open(self.settings_path, "r") as f:
        data = json.load(f)
      print("appdata settings loaded")
      return data
    except FileNotFoundError:
      CustomPopup("Error", f"The settings file could not be found at {self.settings_path}. A new one will be created.").exec()
      self.init_folders()
      self._make_default_json()
      try:
        with open(self.settings_path, "r") as f:
          data = json.load(f)
        print("appdata settings loaded")
        return data
      except Exception:
        return {}
    except Exception:
      CustomPopup("Error", f"The settings file at {self.settings_path} could not be read.").exec()
    return {}

  def init_folders(self):
    if not os.path.exists(self.share_path):
      os.makedirs(self.share_path, exist_ok=True)

  def _make_default_json(self):
    default = {
      "app_links": {
        "video": "",
        "music": "",
        "custom": {
        }
      },
      "general": {
        "autostart": "true"
      }
    }
    try:
      with open(self.settings_path, "x") as f:
        json.dump(default, f, indent=2)
    except Exception:
      CustomPopup("Error", f"Could not initialize settings file {self.settings_path}").exec()

  def _check_json_integrity(self):
    fixed = False
    data = self.data
    if not "app_links" in data:
      self._make_default_json()
    if not "general" in data:
      data["general"] = {
        "autostart": "true"
      }
      fixed = True
    if fixed:
      self.save_settings(data=data, suppress=True)

  def init_settings(self):
    if not os.path.exists(self.settings_path):
      self._make_default_json()
    else:
      self._check_json_integrity()
    
  def _save_applinks(self, video, music, custom):
    data = self._load_settings()
    if "app_links" in data:
      data["app_links"] = {
        "video": video,
        "music": music,
        "custom": custom
      }
      self.save_settings(data=data)

  def save_settings(self, video = "", music = "", custom = {}, data={}, suppress=False):
    if not data:
      self._save_applinks(video, music, custom)
    else:
      try:
        self.data = data
        with open(self.settings_path, "w") as f:
          json.dump(data, f, indent=2)
        if not suppress:
          CustomPopup("Save Complete", "Settings saved to appdata folder").exec()
      except Exception:
        CustomPopup("Error", f"Could not update file {self.settings_path}\n{ex}").exec()
  
  def save_setting(self, section, key, value, suppress=False):
    try:
      self.data[section][key] = value
      with open(self.settings_path, "w") as f:
        json.dump(self.data, f, indent=2)
      if not suppress:
        CustomPopup("Save Complete", "Settings saved to appdata folder").exec()
    except Exception as ex:
      CustomPopup("Error", f"Could not update file {self.settings_path}\n{ex}").exec()
