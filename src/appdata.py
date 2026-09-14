import os, json

class AppData:
  SECTION_APP_LINKS = "app_links"
  LINK_VIDEO = "video"
  LINK_MUSIC = "music"
  SECTION_CUSTOM_LINKS = "custom"
  
  user_path = os.path.expanduser('~')
  share_path = os.path.join(user_path, ".local/share/PCartLoader")
  settings_path = os.path.join(share_path, "settings.json")

  def init_folders(self):
    if not os.path.exists(self.share_path):
      os.makedirs(self.share_path)

  def init_settings(self):
    if not os.path.exists(self.settings_path):
      data = {
        "app_links": {
          "video": "",
          "music": ""
        }
      }
      with open(self.settings_path, "x") as f:
        json.dump(data, f, indent=2)

  def load_settings(self):
    with open(self.settings_path, "r") as f:
      data = json.load(f)
    print("loaded settings from settings.json")
    return data

  def save_settings(self, video = "", music = ""):
    old_settings_json = self.load_settings()
    settings_json = {
      "app_links": {
        "video": video if video != "" else old_settings_json["app_links"]["video"],
        "music": music if music != "" else old_settings_json["app_links"]["music"]
      }
    }
    with open(self.settings_path, "w") as f:
      json.dump(settings_json, f, indent=2)
    print("saved settings to settings.json")