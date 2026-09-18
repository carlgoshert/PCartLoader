import threading
from queue import Queue
from PySide6.QtCore import QObject, Signal

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

class LoadedCart:
  cart: Cartridge = None
  loader: Loader = None
  node_path = ""

  def __init__(self, cart, loader, node_path):
    self.cart = cart
    self.loader = loader
    self.node_path = node_path
  
  def run(self):
    self.loader.run_cart(self.cart)

class QueueWorker(QObject):
  item_received = Signal(object)
  _queue: Queue = None
  _is_running = True

  def __init__(self, q):
    super().__init__()
    self._queue = q

  def stop(self):
    self._is_running = False
    
  def start(self):
    while self._is_running:
      if not self._queue.empty():
        try:
          item: dict = self._queue.get()
          print("found item in queue")
          self.item_received.emit(item)
          self._queue.task_done()
        except:
          print("Exception raised while accessing cartridge queue")