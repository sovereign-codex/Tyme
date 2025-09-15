import json
import sys
from pathlib import Path

def validate_manifest(file_path: Path) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required = ["name", "version", "modules"]
        for key in required:
            if key not in data:
                print(f"[ERROR] {file_path} missing key: {key}")
                return False

        print(f"[OK] {file_path} is valid.")
        return True
    except Exception as e:
        print(f"[FAIL] Could not parse {file_path}: {e}")
        return False

if __name__ == "__main__":
    manifest_files = sys.argv[1:]
    success = True
    for mf in manifest_files:
        if not validate_manifest(Path(mf)):
            success = False
    sys.exit(0 if success else 1)
