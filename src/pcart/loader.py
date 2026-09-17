from .cart_finder import CartManager
from .classes import Cartridge
from .mounter import UdevMonitor

class Loader:
  _mounter = None
  _manager = None

  def __init__(self):
    self._mounter = UdevMonitor(self._on_mount)
    self._manager = CartManager()

  def _on_mount(self, mount_point):
    cart = self._manager.check_dir(mount_point)
    if cart:
      self._manager.run_cart(cart)
  
  def start(self):
    self._mounter.start()
  
  def run_cart(self, cart: Cartridge):
    self._manager.run_cart(cart)

  def get_attached(self) -> list[Cartridge]:
    return self._manager.get_attached()
