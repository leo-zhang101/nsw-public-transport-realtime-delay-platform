"""
Parse GTFS routes.txt into dim_routes table.
"""

import csv
from pathlib import Path

RAW_BASE_DIR = Path("data/raw/gtfs_static_full")
OUTPUT_BASE_DIR = Path("data/dim/gtfs_static")


def find_latest_extracted_dir():
    dt_dirs = sorted(
        [d for d in RAW_BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("dt=")],
        reverse=True
    )
    extracted = dt_dirs[0] / "extracted"
    if not extracted.exists():
        raise RuntimeError("Extracted directory not found")
    return extracted


def parse_routes():
    extracted_dir = find_latest_extracted_dir()
    input_file = extracted_dir / "routes.txt"

    OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_BASE_DIR / "dim_routes.csv"

    print(f"[INFO] Reading {input_file}")
    print(f"[INFO] Writing {output_file}")

    with open(input_file, newline="", encoding="utf-8-sig") as f_in, \
         open(output_file, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)

        fieldnames = [
            "route_id",
            "agency_id",
            "route_short_name",
            "route_long_name",
            "route_type"
        ]

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            writer.writerow({
                "route_id": row["route_id"],
                "agency_id": row.get("agency_id"),
                "route_short_name": row.get("route_short_name"),
                "route_long_name": row.get("route_long_name"),
                "route_type": row.get("route_type"),
            })

    print("[SUCCESS] dim_routes created")


if __name__ == "__main__":
    parse_routes()
