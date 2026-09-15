import os, configparser, subprocess, json
from .classes import Cartridge

class CartManager:
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
        cart_path = mount_dir
        conf_path = os.path.join(cart_path, "cartridge.ini")
        config = configparser.ConfigParser()
        config.read(conf_path)
        cart_name = config["cartridge"]["name"].replace("\"", "")
        cart_target = config["cartridge"]["target"].replace("\"", "")
        cart_args = config["cartridge"]["args"].replace("\"", "")
        cart_type = config["cartridge"]["type"].replace("\"", "")
        print(cart_path + cart_target)
        return Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type)

  def get_attached(self) -> list[Cartridge]:
    carts = []
    mntpnts = ["/mnt", "/media"]
    skip = []
    for start in mntpnts:
      for root, dirs, files in os.walk(start):
        dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(s) for s in skip)]
        if "cartridge.ini" in files and not "Trash" in root:
          cart_path = root
          conf_path = os.path.join(cart_path, "cartridge.ini")
          config = configparser.ConfigParser()
          config.read(conf_path)
          cart_name = config["cartridge"]["name"].replace("\"", "")
          cart_target = config["cartridge"]["target"].replace("\"", "")
          cart_args = config["cartridge"]["args"].replace("\"", "")
          cart_type = config["cartridge"]["type"].replace("\"", "")
          print(f'cart found already attached at {cart_path}')
          carts.append(Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type))
          skip.append(root)
    return carts
