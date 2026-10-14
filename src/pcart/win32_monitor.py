import logging
import win32api, win32con, win32gui
from ctypes import *

WORD = c_ushort
DWORD = c_ulong

class DEV_BROADCAST_HDR (Structure):
  _fields_ = [
    ("dbch_size", DWORD),
    ("dbch_devicetype", DWORD),
    ("dbch_reserved", DWORD)
  ]

class DEV_BROADCAST_VOLUME(Structure):
  _fields_ = [
    ("dbcv_size", DWORD),
    ("dbcv_devicetype", DWORD),
    ("dbcv_reserved", DWORD),
    ("dbcv_unitmask", DWORD),
    ("dbcv_flags", WORD)
  ]

class Win32Monitor:
  _mount_callback = None
  _unmount_callback = None

  def __init__(self, mount_cb, unmount_cb):
    self._mount_callback = mount_cb
    self._unmount_callback = unmount_cb

  def _on_mount(self, mount_point: str):
    logging.info(f"USB device connected on {mount_point}")
    self._mount_callback(mount_point, mount_point)
  
  def _on_unmount(self, mount_point: str):
    logging.info(f"USB device disconnected from {mount_point}.")
    self._unmount_callback(mount_point, mount_point)

  def _drive_letter_from_mask(self, uintmask):
    for i in range(26):
      if (uintmask & 0b1):
        break
      uintmask = uintmask >> 1
    return chr(ord('A') + i)

  def _on_device_event_observed(self, window, msg, wparam, lparam):
    if msg == win32con.WM_DEVICECHANGE:
      dbhdr = DEV_BROADCAST_HDR.from_address(lparam)
      match wparam:
        case win32con.DBT_DEVICEARRIVAL:
          logging.info("Device arrival broadcast event observed.")
          if (dbhdr.dbch_devicetype == win32con.DBT_DEVTYP_VOLUME):
            dbvolume = DEV_BROADCAST_VOLUME.from_address(lparam)
            letter = self._drive_letter_from_mask(dbvolume.dbcv_unitmask)
            mount_point = drive_letter + ':'
            self._on_mount(mount_point)
        case win32con.DBT_DEVICEREMOVECOMPLETE:
          logging.info("Device removal broadcast event observed.")
          if (dbhdr.dbch_devicetype == win32con.DBT_DEVTYP_VOLUME):
            dbvolume = DEV_BROADCAST_VOLUME.from_address(lparam)
            letter = self._drive_letter_from_mask(dbvolume.dbcv_unitmask)
            mount_point = drive_letter + ':'
            self._on_unmount(mount_point)
    return 0

  def _create_window(self):
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = self.__class__.__name__
    wc.lpfnWndProc = self._on_device_event_observed
    class_atom = win32gui.RegisterClass(wc)
    win32gui.CreateWindow(class_atom, 'USBMonitor', 0, 0, 0, 0, 0, 0, 0, 0, None)

  def start(self):
    self._create_window()
    win32gui.PumpMessages()
