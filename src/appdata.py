import os, json
from .custom_gui import CustomPopup

class AppData:
  SECTION_APP_LINKS = "app_links"
  LINK_VIDEO = "video"
  LINK_MUSIC = "music"
  LINK_CUSTOM = "custom"
  SECTION_GENERAL = "general"
  GENERAL_AUTOSTART = "autostart"
  data = {}
  _user_path = os.path.expanduser('~')
  _share_path = os.path.join(_user_path, ".local/share/PCartLoader")
  _settings_path = os.path.join(_share_path, "settings.json")

  def __init__(self):
    self._init_folders()
    self._init_settings()

  def _init_folders(self):
    if not os.path.exists(self._share_path):
      os.makedirs(self._share_path, exist_ok=True)

  def _verify_json(self):
    print("verifying settings.json")
    fixed = False
    data = self.data
    if not "app_links" in data:
      print("app_links missing")
      data["app_links"] = {
        "video": "",
        "music": "",
        "custom": {
        }
      }
      fixed = True
    else:
      if not "video" in data["app_links"]:
        print("video missing")
        data["app_links"]["video"] = ""
        fixed = True
      if not "music" in data["app_links"]:
        print("music missing")
        data["app_links"]["music"] = ""
        fixed = True
      if not "custom" in data["app_links"]:
        print("custom missing")
        data["app_links"]["custom"] = {}
        fixed = True
    if not "general" in data:
      print("general missing")
      data["general"] = {
        "autostart": "true"
      }
      fixed = True
    else:
      if not "autostart" in data["general"]:
        print("autostart missing")
        data["general"]["autostart"] = "true"
        fixed = True
    if fixed:
      print("correcting settings.json")
      self.save_settings(data=data, suppress=True)

  def _make_default_json(self):
    print("making default settings.json")
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
      with open(self._settings_path, "x") as f:
        json.dump(default, f, indent=2)
    except Exception as ex:
      CustomPopup("Error", f"Could not initialize settings file {self._settings_path}\n{ex}").exec()

  def _init_settings(self):
    if not os.path.exists(self._settings_path):
      self._make_default_json()
      self.data = self._load_settings()
    else:
      self.data = self._load_settings()
      self._verify_json()

  def _load_settings(self) -> dict:
    try:
      with open(self._settings_path, "r") as f:
        data = json.load(f)
      print("appdata settings loaded")
      return data
    except FileNotFoundError:
      CustomPopup("Error", f"The settings file could not be found at {self._settings_path}").exec()
    except Exception as ex:
      CustomPopup("Error", f"The settings file at {self._settings_path} could not be read.\n{ex}").exec()
    return {}
    
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
        with open(self._settings_path, "w") as f:
          json.dump(data, f, indent=2)
        if not suppress:
          CustomPopup("Save Complete", "Settings saved to appdata folder").exec()
      except Exception:
        CustomPopup("Error", f"Could not update file {self._settings_path}\n{ex}").exec()
  
  def save_setting(self, section, key, value, suppress=False):
    try:
      self.data[section][key] = value
      with open(self._settings_path, "w") as f:
        json.dump(self.data, f, indent=2)
      if not suppress:
        CustomPopup("Save Complete", "Settings saved to appdata folder").exec()
    except Exception as ex:
      CustomPopup("Error", f"Could not update file {self._settings_path}\n{ex}").exec()
