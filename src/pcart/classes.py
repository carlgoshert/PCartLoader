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