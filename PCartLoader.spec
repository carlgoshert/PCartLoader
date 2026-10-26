# -*- mode: python ; coding: utf-8 -*-
import os, tomllib

with open(os.path.join(SPECPATH, "pyproject.toml"), "rb") as f:
    project = tomllib.load(f)["project"]

#version_file = os.path.join(SPECPATH, "src", "_version.py")
#with open(version_file, "w") as f:
#    f.write(f'__version__ = "{project["version"]}"\n')

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/icon.ico', 'src'),
		('src/icon-black.ico', 'src'),
        ('src/icon.png', 'src'),
        ('src/ui/AboutWindow.ui', 'src/ui'),
        ('src/ui/ConfigWindowStart.ui', 'src/ui'),
        ('src/ui/ConfigWindowPlatform.ui', 'src/ui'),
        ('src/ui/ConfigWindowDefault.ui', 'src/ui'),
        ('src/ui/ConfigWindowMulti.ui', 'src/ui'),
        ('src/ui/SettingsWindow.ui', 'src/ui'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PCartLoader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=project["name"],
)
