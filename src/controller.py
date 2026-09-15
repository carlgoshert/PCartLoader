from .cart_finder import CartManager, Cartridge
# from .automount import USBMounter
from .automount import UdevMonitor

class Controller:
  mounter = None
  manager = None

  def _on_mount(self, mount_point):
    cart = self.manager.check_dir(mount_point)
    if cart:
      self.manager.run_cart(cart)
  
  def start(self):
    #TODO: add initial check for mounted or unmounted carts and add to list
    self.mounter = UdevMonitor(self._on_mount)
    self.mounter.start()
    self.manager = CartManager()

