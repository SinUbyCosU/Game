# game.spec

import os
from PyInstaller.utils.hooks import collect_data_files

# You might want to change the location based on where your assets are
asset_files = collect_data_files('pygame')

a = Analysis(
    ['game.py'],  # Your main game script
    pathex=[],
    binaries=[],
    datas=[
        ('font.ttf', '.'),  # Include the font file
        ('background.png', '.'),  # Include the background image
        ('planet-ringed.png', '.'),  # Include the icon
        ('spaceship.png', '.'),  # Include the spaceship image
        ('bullet.png', '.'),  # Include the bullet image
        ('background.wav', '.'),  # Include the background music
        ('explosion.wav', '.'),  # Include the explosion sound
        ('laser.wav', '.'),  # Include the laser sound
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
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='game',
)

