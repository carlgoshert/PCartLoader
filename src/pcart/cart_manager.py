import os, configparser, subprocess, json, shlex, logging
from pathlib import Path
from .classes import Cartridge
from ..appdata import AppData
from ..custom_gui import CustomPopup

class CartManager:
  KEYWORD_CART_DIR = '$CARTDIR'

  def run_cart(self, cartridge: Cartridge, app_data):
    settings_dict = app_data.data
    target_path = os.path.join(cartridge.path, cartridge.target) if cartridge.target != "" else ""
    logging.debug(f"Cartridge target filepath: {target_path}")
    logging.debug(f"Cartridge target type: {cartridge.target_type}")
    try:
      cmd = []
      args = shlex.split(cartridge.args.replace(self.KEYWORD_CART_DIR, cartridge.path))
      match cartridge.target_type:
        case "exe":
          if target_path != "":
            cmd = [target_path] + args
          else:
            raise Exception("target_path was empty.")
        case "video":
          if target_path != "":
            video_link = shlex.split(settings_dict["app_links"]["video"])
            cmd = video_link + args + [target_path]
          else:
            raise Exception("target_path was empty.")
        case "music":
          if target_path != "":
            music_link = shlex.split(settings_dict["app_links"]["music"])
            cmd = music_link + args + [target_path]
          else:
            raise Exception("target_path was empty.")
        case _:
          matches_custom = False
          custom_types = settings_dict["app_links"]["custom"]
          for ty, ln in custom_types.items():
            if cartridge.target_type == ty:
              matches_custom = True
              if target_path != "":
                cmd = shlex.split(ln) + args + [target_path]
              else:
                cmd = shlex.split(ln) + args
              break
          if not matches_custom:
            logging.info("Cartridge target_type not recognized.")
            return
      logging.info("Launching cartridge.")
      logging.debug(f"Subprocess cmd: {cmd}")
      subprocess.run(cmd, check=True)
    except Exception as ex:
      CustomPopup("Error", f"Cartridge could not be loaded.\n{ex}")
      logging.error(f"Cartridge could not be louded. {ex}")

  def check_dir(self, mount_dir: str):
    logging.info(f"Searching {mount_dir} for cartridge.ini.")
    for file in os.listdir(mount_dir):
      if file == "cartridge.ini":
        logging.info("Found cartridge.ini")
        cart_path = mount_dir
        conf_path = os.path.join(cart_path, "cartridge.ini")
        config = configparser.ConfigParser()
        config.read(conf_path)
        cart_name = config["cartridge"]["name"]
        cart_target = config["cartridge"]["target"]
        cart_args = config["cartridge"]["args"]
        cart_type = config["cartridge"]["type"]
        return Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type)

  def get_attached(self) -> list[Cartridge]:
    carts = []
    skip = []
    mountpoints = {"/media": 3, "/run/media": 4}
    if Path("/media").resolve() == Path("/run/media").resolve():
      if Path("/media").is_symlink():
        mountpoints.pop("/media")
      elif Path("/run/media").is_symlink():
        mountpoints.pop("/run/media")
    for path, depth in mountpoints.items():
      for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(s) for s in skip) and os.path.join(root, d).count('/') <= depth]
        if "cartridge.ini" in files and not "Trash" in root:
          cart_path = root
          conf_path = os.path.join(cart_path, "cartridge.ini")
          config = configparser.ConfigParser()
          config.read(conf_path)
          cart_name = config["cartridge"]["name"]
          cart_target = config["cartridge"]["target"]
          cart_args = config["cartridge"]["args"]
          cart_type = config["cartridge"]["type"]
          logging.info(f'Cartridge found already attached at {cart_path}.')
          carts.append(Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type))
          skip.append(root)
    return carts
