import os, json

class AppData:
  SECTION_APP_LINKS = "app_links"
  LINK_VIDEO = "video"
  LINK_MUSIC = "music"
  LINK_CUSTOM = "custom"
  
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
          "music": "",
          "custom": {
          }
        }
      }
      with open(self.settings_path, "x") as f:
        json.dump(data, f, indent=2)

  def load_settings(self):
    with open(self.settings_path, "r") as f:
      data = json.load(f)
    return data

  def save_settings(self, video = "", music = "", custom = {}):
    old_settings_json = self.load_settings()
    settings_json = {
      "app_links": {
        "video": video,
        "music": music,
        "custom": custom
      }
    }
    with open(self.settings_path, "w") as f:
      json.dump(settings_json, f, indent=2)