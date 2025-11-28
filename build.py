import PyInstaller.__main__
import sys
from pathlib import Path

project_root = Path(__file__).parent
main_script = project_root / "src" / "main.py"

PyInstaller.__main__.run([
    str(main_script),
    "--name=vrchat-invite-notifier",
    "--onefile",
    "--console",
    "--clean",
    f"--paths={project_root / 'src'}",
    "--hidden-import=config.loader",
    "--hidden-import=vrchat.auth",
    "--hidden-import=vrchat.websocket",
    "--hidden-import=discord.webhook",
    f"--distpath={project_root / 'dist'}",
    f"--workpath={project_root / 'build'}",
    f"--specpath={project_root}",
])

print("\nビルド完了！")
print(f"実行ファイル: {project_root / 'dist' / 'vrchat-invite-notifier.exe'}")
