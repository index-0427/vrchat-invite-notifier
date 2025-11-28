import sys
from pathlib import Path

project_root = Path(__file__).parent
src_dir = project_root / "src"

sys.path.insert(0, str(src_dir))

from gui import main

if __name__ == "__main__":
    main()
