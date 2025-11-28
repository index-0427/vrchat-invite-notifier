import PyInstaller.__main__
import sys
from pathlib import Path

project_root = Path(__file__).parent
main_script = project_root / "run_gui.py"

PyInstaller.__main__.run([
    str(main_script),
    "--name=vrchat-invite-notifier-gui",
    "--onefile",
    "--windowed",
    "--clean",
    f"--distpath={project_root / 'dist'}",
    f"--workpath={project_root / 'build'}",
    f"--specpath={project_root}",
])

print("\nGUI版ビルド完了！")
print(f"実行ファイル: {project_root / 'dist' / 'vrchat-invite-notifier-gui.exe'}")
