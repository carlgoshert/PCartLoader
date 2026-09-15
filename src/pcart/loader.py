from .cart_finder import CartManager
from .classes import Cartridge
from .mounter import UdevMonitor

class Loader:
  mounter = None
  manager = None

  def __init__(self):
    self.mounter = UdevMonitor(self._on_mount)
    self.manager = CartManager()

  def _on_mount(self, mount_point):
    cart = self.manager.check_dir(mount_point)
    if cart:
      self.manager.run_cart(cart)
      self.attached_cb(cart, self)
  
  def start(self):
    self.mounter.start()
  
  def run_cart(self, cart: Cartridge):
    self.manager.run_cart(cart)

  def get_attached(self) -> list[Cartridge]:
    return self.manager.get_attached()
