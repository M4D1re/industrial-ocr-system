import importlib.metadata
import subprocess
import sys


main_file = "main.py"

installed_packages = sorted(
    {
        dist.metadata["Name"]
        for dist in importlib.metadata.distributions()
        if dist.metadata.get("Name")
    }
)

cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    main_file,
    "--noconfirm",
    "--windowed",
    "--name",
    "IndustrialOCRRecorder",

    "--collect-all",
    "paddlex",

    "--collect-all",
    "paddleocr",

    "--collect-binaries",
    "paddle",

    "--add-data",
    "app/database/migrations/001_initial_schema.sql;app/database/migrations",

    "--hidden-import",
    "cv2",

    "--hidden-import",
    "numpy",

    "--hidden-import",
    "PySide6",
]

for package_name in installed_packages:
    cmd.extend(
        [
            "--copy-metadata",
            package_name,
        ]
    )

print("Running PyInstaller...")
subprocess.run(cmd, check=True)