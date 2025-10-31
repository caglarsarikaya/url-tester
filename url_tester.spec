# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['url_tester.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pandas', 'numpy', 'matplotlib', 'scipy', 'PIL', 'Pillow',
        'tk', 'tkinter', 'PyQt5', 'PyQt6', 'wx', 'IPython', 
        'notebook', 'jupyter', 'pytest', 'unittest', 'psutil'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='url_tester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

