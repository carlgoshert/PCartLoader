import subprocess, time, os
import pyudev

class UdevMonitor:
  _mount_callback = None
  # _devices = []

  def __init__(self, mount_cb):
    if mount_cb == None:
      raise Exception("mount callback required for automount")
    self._mount_callback = mount_cb

  def _mount(self, device: str):
    print(f"mounting {device}")
    cmd = "udisksctl mount -b " + device
    proc = subprocess.run([cmd], capture_output=True, text=True, shell=True)
    mount_point = proc.stdout.split(" at ")[-1].strip()
    os.chmod(mount_point, 0o755)
    print(mount_point)
    self._mount_callback(mount_point)

  def _on_udev_event_observed(self, action, device):
    print(f'{action} {device.device_node}')
    match action:
      case "add":
        print(f'Connected: {device.device_node}')
        # self._devices.append(device.device_node)
        self._mount(device.device_node)
      case "remove":
        print(f'Disconnected: {device.device_node}')
        # self._devices.append(device.device_node)

  def start(self):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block', device_type='partition')
    observer = pyudev.MonitorObserver(monitor, self._on_udev_event_observed)
    observer.start()
