# PCartLoader

This is a simple python Qt app for Linux built on PySide6 and pyudev that automatically mounts newly connected devices and, if a PCart config file is found, launches the application targeted by the config file.

When launched, the application immediately minimizes to the system tray. Right click to close the application or access the settings menu. In the settings menu, you can specificy what local applications to use with various cartridge target types.

## PCart Config File

A PCart config file should be named "cartridge.ini" and exist at the top-level of the device filesystem. Below is the expected config layout.

*note: custom target types are not yet supported*

```
[cartridge]
name = "cartridge name"     ; Whatever you want to name it
target = "application.exe"  ; The file or folder you would like it to open on when loaded
args = ""                   ; Any arguments needed for a command-line launch. Leave blank if none
type = ""                   ; "music", "video", or "exe" by default. Anything else must be added to the list of custom options in the settings menu
```

## Compile & Install

PCartLoader is distributed as an AppImage built using [pyproject-appimage](https://pypi.org/project/pyproject-appimage/). Simply download the latest version from the Releases page, or build from source using:
```
curl -L -o pcartloader.zip https://github.com/carlgoshert/PCartLoader/archive/refs/heads/main.zip
unzip pcartloader.zip
cd PCartLoader-main
pyproject-appimage
```
I recommend using [Gear Lever](https://flathub.org/en/apps/it.mijorus.gearlever) to install and manage the AppImage file.

## Usage

Simply launch PCartLoader.AppImage and allow it to run in the background. Plug in a PCart Reader and slot in a cartridge.

Configuration settings for PCartLoader can be found in ~/.local/share/PCartLoader/settings.json. The current json schema is below.
```
{
  "app_links": {
    "video": "/path/to/video/player",
    "music": "/path/to/music/player"
  }
}
```

PCartLoader will use the app_links to launch any target whose type is not "exe". All "exe" targets are treated as standalone executable applications.

For instance, you could have the following cartridge.ini, which tells PCartLoader to launch `openMSX.AppImage` as a standalone application:
```
[cartridge]
name = "openMSX"
target = "content/openMSX.AppImage"
args = ""                   
type = "exe"  
```

But if you had a cartridge containing a folder of mp4 videos:
```
[cartridge]
name = "movies"
target = "movies/"
args = ""                   
type = "video"
```
You would then need to make sure the "video" app_link is set in your settings.json, either by manually editing the file, or by right-clicking the system tray icon and opening the settings menu. A video app_link for VLC might look like this:
```
"video": "flatpak run --branch=stable --arch=x86_64 --command=/app/bin/vlc --file-forwarding org.videolan.VLC --started-from-file"
```
