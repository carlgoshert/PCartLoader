import os, configparser, subprocess, json

class Cartridge:
  name = ""
  path = ""
  target = ""
  args = ""
  target_type = ""

  def __init__(self, path, name, target, args, t_type):
    self.path = path
    self.name = name
    self.target = target
    self.args = args
    self.target_type = t_type

class CartManager:
  #TODO add list of active carts to dropdown in system tray icon to relaunch connected carts, remove from list when disconnected

  def _load_settings_json(self):
    user_path = os.path.expanduser('~')
    share_path = os.path.join(user_path, ".local/share/PCartLoader")
    settings_path = os.path.join(share_path, "settings.json")
    data = []
    with open(settings_path, "r") as f:
      data = json.load(f)
    return data

  def run_cart(self, cartridge: Cartridge):
    settings_dict = self._load_settings_json()
    print(cartridge.target_type)
    match cartridge.target_type:
      case "exe":
        print("process started")
        # cmd = os.path.join(cartridge.path, cartridge.target)
        cmd = cartridge.path + cartridge.target
        args = cartridge.args
        subprocess.run([cmd, args], env=os.environ.copy(), shell=True)
        return
      case "video":
        video_link = settings_dict["app_links"]["video"]
        subprocess.run(video_link + " " + cartridge.target, shell=True)
        return
      case "music":
        music_link = settings_dict["app_links"]["music"]
        subprocess.run(music_link + " " + cartridge.target, shell=True)
        return
      case _:
        matches_custom = False
        # custom_types = []
        # for custom_type, link in custom_types:
        #   if custom_type == cartridge.target_type:
        #     subprocess.run(link + " " + cartridge.target, shell=True)
        if not matches_custom:
          print("cartridge target_type not recognized")

  def check_dir(self, mount_dir: str):
    print("searching...")
    for file in os.listdir(mount_dir):
      if file == "cartridge.ini":
        print("found it!")
        print(mount_dir)
        print(file)
        conf_path = mount_dir + "/cartridge.ini"
        cart_path = mount_dir
        config = configparser.ConfigParser()
        config.read(conf_path)
        cart_name = config["cartridge"]["name"].replace("\"", "")
        cart_target = config["cartridge"]["target"].replace("\"", "")
        cart_args = config["cartridge"]["args"].replace("\"", "")
        cart_type = config["cartridge"]["type"].replace("\"", "")
        print(cart_path + cart_target)
        return Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type)
