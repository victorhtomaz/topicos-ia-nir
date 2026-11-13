# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['executar_sistema.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('preprocessamento_nir.py', '.'),
        ('primeira-etapa/primeira_etapa.py', 'primeira-etapa'),
        ('segunda-etapa/segunda_etapa.py', 'segunda-etapa'),
        ('terceira-etapa/teorema-bayes.py', 'terceira-etapa'),
        ('terceira-etapa/kmeans-reduzido.py', 'terceira-etapa'),
    ],
    hiddenimports=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy',
        'sklearn',
        'openpyxl',
    ],
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
    a.binaries,
    a.datas,
    [],
    name='executar_sistema',
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
)
