import sys, atexit, subprocess, time, os
from usbx import usb, Device

def arr_diff(arr1, arr2):
  return [x for x in arr2 if x not in arr1]

def run_lsblk():
  cmd = "lsblk -p -o NAME | grep sd | awk '/[0-9]/' | sed 's/[^a-z0-9/]//g'"
  return subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)

def get_stdout(proc):
  return list(filter(None, proc.stdout.read().decode().split("\n")))

class USBMounter:
  _lsblk_list = []
  _mount_callback = None

  def __init__(self, mount_cb):
    if mount_cb == None:
      raise Exception("mount callback required for automount")
    self._mount_callback = mount_cb

  def _mount(self, devices: list):
    print("mounting...")
    for i in range(0, len(devices)):
      print(devices[i])
      cmd = "udisksctl mount -b " + devices[i]
      proc = subprocess.run([cmd], capture_output=True, text=True, shell=True)
      mount_point = proc.stdout.split(" at ")[-1].strip()
      os.chmod(mount_point, 0o755)
      print(mount_point)
      self._mount_callback(mount_point)
  
  def _unmount(self, mount_point: str):
    cmd = "output=$(fuser -mv " + mount_point + " 2>&1); echo \"$output\" | awk -v u=\"$USER\" '$1 == u'"
    while (subprocess.run([cmd], capture_output=True, text=True, shell=True).stdout):
      time.sleep(1)
    print("unmounting " + mount_point)
    cmd = "findmnt -n -o SOURCE " + mount_point
    proc = subprocess.run([cmd], capture_output=True, text=True, shell=True)
    device = proc.stdout
    cmd = "udisksctl unmount -b " + device
    subprocess.run([cmd], text=True, shell=True)

  def _connected(self, device: Device) -> None:
    print(f'Connected:    {device}')
    time.sleep(3)
    lsblk_proc = run_lsblk()
    lsblk_output = get_stdout(lsblk_proc)
    print(lsblk_output)
    new_devices = arr_diff(self._lsblk_list, lsblk_output)
    if new_devices:
      self._lsblk_list = lsblk_output
      print(new_devices)
      self._mount(new_devices)

  def _disconnected(self, device: Device) -> None:
    print(f'Disconnected: {device}')
    time.sleep(3)
    lsblk_proc = run_lsblk()
    self._lsblk_list = get_stdout(lsblk_proc)
    print(self._lsblk_list)

  # if __name__ == "__main__":
  def start(self):
    usb.on_connected(self._connected)
    usb.on_disconnected(self._disconnected)
    for dev in usb.find_devices():
      print(f'Present:      {dev}')

    lsblk_proc = run_lsblk()
    self._lsblk_list = get_stdout(lsblk_proc)
    print(self._lsblk_list)
