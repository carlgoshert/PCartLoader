import subprocess
from queue import Queue
from .cart_manager import CartManager
from .classes import Cartridge, LoadedCart
from .udev_monitor import UdevMonitor
from ..appdata import AppData

class CartLoader:
  _monitor = None
  _manager = None
  _loaded_carts: list[LoadedCart] = []
  _queue: Queue = None
  _app_data = None

  def __init__(self, q, app_data):
    self._monitor = UdevMonitor(self._on_mount, self._on_unmount)
    self._manager = CartManager()
    self._queue = q
    self._app_data = app_data

  def _on_mount(self, mount_point, node_path):
    cart = self._manager.check_dir(mount_point)
    if cart:
      cart.node_path = node_path
      lcart = LoadedCart(cart, self, node_path)
      self._loaded_carts.append(lcart)
      self._queue.put({"cart": lcart, "action": "add"})
      self._manager.run_cart(cart, self._app_data)
  
  def _on_unmount(self, node_path):
    unloaded: LoadedCart = None
    for lcart in self._loaded_carts:
      if node_path == lcart.node_path:
        unloaded = lcart
        break
    if unloaded:
      self._loaded_carts.remove(unloaded)
      self._queue.put({"cart": unloaded, "action": "remove"})

  def start(self):
    self._monitor.start()
  
  def run_cart(self, cart: Cartridge):
    self._manager.run_cart(cart, self._app_data)

  def get_attached(self) -> list[LoadedCart]:
    try:
      carts = self._manager.get_attached()
      for cart in carts:
        cmd = f"mount | grep '{cart.path}' | awk '{{print $1}}'"
        proc = subprocess.run([cmd], capture_output=True, text=True, shell=True)
        node_path = proc.stdout
        self._loaded_carts.append(LoadedCart(cart, self, node_path))
      return self._loaded_carts
    except Exception:
      return None
