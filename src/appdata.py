import os, json, logging
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

  def init_folders(self):
    if not os.path.exists(self._share_path):
      os.makedirs(self._share_path, exist_ok=True)

  def _verify_json(self):
    logging.info("Verifying settings.json file.")
    fixed = False
    data = self.data
    if not "app_links" in data:
      logging.warning("Section app_links missing. Creating.")
      data["app_links"] = {
        "video": "",
        "music": "",
        "custom": {
        }
      }
      fixed = True
    else:
      if not "video" in data["app_links"]:
        logging.warning("Key video missing. Creating.")
        data["app_links"]["video"] = ""
        fixed = True
      if not "music" in data["app_links"]:
        logging.warning("Key music missing. Creating.")
        data["app_links"]["music"] = ""
        fixed = True
      if not "custom" in data["app_links"]:
        logging.warning("Key custom missing. Creating.")
        data["app_links"]["custom"] = {}
        fixed = True
    if not "general" in data:
      logging.warning("Section general missing. Creating")
      data["general"] = {
        "autostart": "true"
      }
      fixed = True
    else:
      if not "autostart" in data["general"]:
        logging.warning("Key autostart missing. Creating.")
        data["general"]["autostart"] = "true"
        fixed = True
    if fixed:
      logging.info("Saving corrections to settings.json file.")
      self.save_settings(data=data, suppress=True)
    else:
      logging.info("settings.json file verified.")

  def _make_default_json(self):
    logging.info("Making default settings.json file.")
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
      logging.error(f"Could not initialize settings.json file. {ex}")

  def init_settings(self):
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
      logging.info("The settings.json file loaded from appdata folder.")
      return data
    except FileNotFoundError:
      CustomPopup("Error", f"The settings file could not be found at {self._settings_path}. Please verify this location exists.").exec()
      logging.error(f"The settings.json file could not be found at {self._settings_path}, despite just being created/verified. Please verify this location exists.")
    except Exception as ex:
      CustomPopup("Error", f"The settings file at {self._settings_path} could not be read.\n{ex}").exec()
      logging.error(f"The settings.json file could not be read. {ex}")
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
          CustomPopup("Save Complete", f"Settings saved to settings.json.").exec()
        logging.info(f"The settings.json file saved to {self._settings_path}.")
      except Exception:
        CustomPopup("Error", f"Could not update settings.json file.\n{ex}").exec()
        logging.error(f"Could not update settings.json file. {ex}")
  
  def save_setting(self, section, key, value, suppress=False):
    try:
      self.data[section][key] = value
      with open(self._settings_path, "w") as f:
        json.dump(self.data, f, indent=2)
      if not suppress:
        CustomPopup("Save Complete", f"Settings saved to settings.json.").exec()
      logging.info(f"The settings.json file saved to {self._settings_path}.")
    except Exception as ex:
      CustomPopup("Error", f"Could not update settings.json file.\n{ex}").exec()
      logging.error(f"Could not update settings.json file. {ex}")
