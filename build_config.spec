# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for URL Tester Application
Optimized for minimal file size

Usage:
    pyinstaller build_config.spec

Output:
    dist/url_tester.exe
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('urls_to_test.xlsx', '.'),
        ('sitemaps.xlsx', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'setuptools',
        'pip',
        'wheel',
        '_pytest',
        'PIL',
        'pydoc',
        'unittest',
        'test',
        'tests',
        'distutils',
        'email',
        'html',
        'http.server',
        'xmlrpc',
        'pydoc_data',
        'pkg_resources',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='url_tester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols (reduces size)
    upx=True,    # Use UPX compression (reduces size significantly)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application (not GUI)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon='icon.ico' if you have one
)

