import os, configparser, subprocess, json
from .classes import Cartridge
from ..appdata import AppData
from ..custom_gui import CustomPopup

class CartManager:

  def run_cart(self, cartridge: Cartridge, app_data):
    settings_dict = app_data.load_settings()
    target_path = '"' + os.path.join(cartridge.path, cartridge.target) + '"'
    print(cartridge.target_type)
    try:
      match cartridge.target_type:
        case "exe":
          print("process started")
          cmd = cartridge.path + cartridge.target
          args = cartridge.args
          subprocess.run([cmd, args], env=os.environ.copy(), shell=True)
          return
        case "video":
          video_link = settings_dict["app_links"]["video"]
          subprocess.run(video_link + " " + target_path, shell=True)
          return
        case "music":
          music_link = settings_dict["app_links"]["music"]
          subprocess.run(music_link + " " + target_path, shell=True)
          return
        case _:
          print("custom link selected")
          matches_custom = False
          custom_types = settings_dict["app_links"]["custom"]
          for ty, ln in custom_types.items():
            if cartridge.target_type == ty:
              matches_custom = True
              print(f'launching {ln} {target_path}')
              subprocess.run(ln + ' ' + target_path, shell=True)
              return
          if not matches_custom:
            print("cartridge target_type not recognized")
    except Exception as ex:
      CustomPopup("Error", f"Cartridge could not be loaded. {ex}")

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
    skip = []
    for root, dirs, files in os.walk("/run/media"):
      dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(s) for s in skip) and os.path.join(root, d).count('/') <= 4]
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
