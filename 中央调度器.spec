# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Python文件\\中央调度器.py'],
    pathex=[],
    binaries=[],
    datas=[('model','model'),('ziyuanwenjian','ziyuanwenjian'),
    ('venv/Lib/site-packages/uiautomator2/assets', 'uiautomator2/assets')],
    hiddenimports=['ultralytics','torch','uiautomator2','cv2'],
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
    name='测试exe名',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name='文件夹测试名',
)
