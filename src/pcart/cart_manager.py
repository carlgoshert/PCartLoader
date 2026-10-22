import os, configparser, subprocess, json, shlex, logging, psutil, platform
from pathlib import Path
from .classes import Cartridge
from ..appdata import AppData
from ..custom_gui import CustomPopup

class CartManager:
  KEYWORD_CART_DIR = '$CARTDIR'
  KEYWORD_HOME = "$HOME"

  def run_cart(self, cartridge: Cartridge, app_data):
    settings_dict = app_data.data
    target_path = os.path.join(cartridge.path, cartridge.target) if cartridge.target != "" else ""
    logging.debug(f"Cartridge target filepath: {target_path}")
    logging.debug(f"Cartridge target type: {cartridge.target_type}")
    try:
      cmd = []
      args = cartridge.args.replace(self.KEYWORD_CART_DIR, cartridge.path)
      args = args.replace(self.KEYWORD_HOME, os.path.expanduser('~'))
      args = shlex.split(args)
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
      logging.error(f"Cartridge could not be loaded. {ex}")

  def check_dir(self, mount_dir: str):
    logging.info(f"Searching {mount_dir} for cartridge.ini.")
    for file in os.listdir(mount_dir):
      if file == "cartridge.ini":
        logging.info("Found cartridge.ini")
        conf_path = os.path.join(mount_dir, "cartridge.ini")
        return self._parse_config(conf_path)
  
  def _has_section(self, conf_path, section):
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config.has_section(section)
  
  def _parse_config(self, conf_path):
    match platform.system():
      case "Linux":
        section = "linux" if self._has_section(conf_path, "linux") else "cartridge"
        return self._parse_config_section(conf_path, section)
      case "Windows":
        section = "windows" if self._has_section(conf_path, "windows") else "cartridge"
        return self._parse_config_section(conf_path, section)

  def _parse_config_section(self, conf_path, section):
    config = configparser.ConfigParser()
    config.read(conf_path)
    if config.has_section(section):
      cart_path = os.path.split(conf_path)[0]
      cart_name = config[section]["name"]
      cart_target = config[section]["target"]
      cart_args = config[section]["args"]
      cart_type = config[section]["type"]
      return Cartridge(cart_path, cart_name, cart_target, cart_args, cart_type)
    else:
      logging.error(f"Could not parse cartridge.ini. Missing section header {section}.")
      return None

  def get_attached(self) -> dict[str, Cartridge]:
    carts = {}
    skip = []
    partitions = psutil.disk_partitions()
    for part in partitions:
      path = part[1]
      depth = path.count(os.sep) + 1
      for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(s) for s in skip) and os.path.join(root, d).count(os.sep) <= depth]
        if "cartridge.ini" in files and not "Trash" in root:
          conf_path = os.path.join(root, "cartridge.ini")
          cart = self._parse_config(conf_path)
          logging.info(f'Cartridge found already attached at {cart.path}.')
          carts[part[0]] = cart
          skip.append(root)
    return carts
