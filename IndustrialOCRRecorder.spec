# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()

paddlex_version_file = (
    project_root
    / ".venv"
    / "Lib"
    / "site-packages"
    / "paddlex"
    / ".version"
)

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (
            "app/database/migrations/001_initial_schema.sql",
            "app/database/migrations",
        ),
        (
            str(paddlex_version_file),
            "paddlex",
        ),
    ],
    hiddenimports=[
        "paddle",
        "paddleocr",
        "paddlex",
        "cv2",
        "numpy",
        "PySide6",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="IndustrialOCRRecorder",
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="IndustrialOCRRecorder",
)