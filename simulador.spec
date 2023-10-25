# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['simulador.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('simulador.html',"."),
        ('recursos/imagenes',"recursos/imagenes"),
        ('py',"py"),
        ('js',"js"),
        ('css',"css"),
        ('html',"html")
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='simulador',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\wasab\\Documents\\Archivos Transitorios\\SIMULADOR BALLOTAGE\\recursos\\iconos\\A.ico'],
)
