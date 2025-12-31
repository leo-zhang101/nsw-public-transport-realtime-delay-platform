"""
Extract GTFS Static ZIP into raw structured files.

Responsibilities:
- Locate latest GTFS static ZIP (by dt partition)
- Extract files into extracted/ directory
- Do NOT modify filenames or contents
"""

import zipfile
from pathlib import Path


RAW_BASE_DIR = Path("data/raw/gtfs_static_full")


def find_latest_dt_dir():
    dt_dirs = sorted(
        [d for d in RAW_BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("dt=")],
        reverse=True
    )
    if not dt_dirs:
        raise RuntimeError("No dt=YYYY-MM-DD directory found")
    return dt_dirs[0]


def extract_gtfs_static():
    dt_dir = find_latest_dt_dir()
    zip_path = dt_dir / "gtfs_static.zip"

    if not zip_path.exists():
        raise FileNotFoundError(f"{zip_path} not found")

    extract_dir = dt_dir / "extracted"
    extract_dir.mkdir(exist_ok=True)

    print(f"[INFO] Extracting {zip_path}")
    print(f"[INFO] Output dir: {extract_dir}")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    print("[SUCCESS] GTFS static files extracted")


if __name__ == "__main__":
    extract_gtfs_static()
