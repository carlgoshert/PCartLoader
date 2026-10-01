import subprocess, time, os
import pyudev

class UdevMonitor:
  _mount_callback = None
  _unmount_callback = None

  def __init__(self, mount_cb, unmount_cb):
    self._mount_callback = mount_cb
    self._unmount_callback = unmount_cb

  def _on_mount(self, node_path: str):
    try:
      print(f"mounting {node_path}")
      timeout = 60
      start = time.time()
      waiting = True
      while (waiting):
        cmd = f"udisksctl info -b {node_path} | grep MountPoints | awk '{{print $2}}'"
        proc = subprocess.run([cmd], capture_output=True, text=True, shell=True)
        mount_point = proc.stdout.replace('\n', '')
        if mount_point != "":
          waiting = False
        if time.time() >= start + timeout:
          raise Exception("timeout exceeded waiting for device to be mounted")
      if mount_point != "":
        os.chmod(mount_point, 0o755)
        print(mount_point)
        self._mount_callback(mount_point, node_path)
    except Exception as ex:
      print(f"unable to find mountpoint for {node_path}\n{ex}")
  
  def _on_unmount(self, node_path: str):
    print(f'unmounting {node_path}')
    self._unmount_callback(node_path)

  def _on_udev_event_observed(self, action, device):
    print(f'{action} {device.device_node}')
    match action:
      case "add":
        print(f'Connected: {device.device_node}')
        self._on_mount(device.device_node)
      case "remove":
        print(f'Disconnected: {device.device_node}')
        self._on_unmount(device.device_node)

  def start(self):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block', device_type='partition')
    observer = pyudev.MonitorObserver(monitor, self._on_udev_event_observed)
    observer.start()
