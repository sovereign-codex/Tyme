import os
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

def rebuild_structure():
    print("[INFO] Starting reconstruction...")
    
    dirs = ["docs", "chronicle"]
    for d in dirs:
        path = BASE_DIR / d
        if path.exists():
            shutil.rmtree(path)
        path.mkdir()
        print(f"[OK] Rebuilt {d}/")

    with open(BASE_DIR / "chronicle/curious-agent.log", "w") as log:
        log.write("Reconstruction cycle initialized.\n")

if __name__ == "__main__":
    rebuild_structure()
