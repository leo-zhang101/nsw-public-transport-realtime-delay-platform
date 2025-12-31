import csv
from pathlib import Path

RAW_BASE = Path("data/raw/gtfs_static_full")
DIM_BASE = Path("data/dim/gtfs_static")


def latest_snapshot():
    return sorted(RAW_BASE.glob("dt=*"))[-1]


def parse_stops():
    snapshot_dir = latest_snapshot()
    input_file = snapshot_dir / "extracted/stops.txt"
    output_file = DIM_BASE / "dim_stops.csv"

    print(f"[INFO] Reading {input_file}")
    DIM_BASE.mkdir(parents=True, exist_ok=True)

    with open(input_file, newline="", encoding="utf-8-sig") as f_in, \
         open(output_file, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(
            f_out,
            fieldnames=[
                "stop_id",
                "stop_name",
                "stop_lat",
                "stop_lon",
                "location_type",
                "parent_station"
            ]
        )

        writer.writeheader()

        for row in reader:
            writer.writerow({
                "stop_id": row["stop_id"],
                "stop_name": row["stop_name"],
                "stop_lat": row.get("stop_lat"),
                "stop_lon": row.get("stop_lon"),
                "location_type": row.get("location_type"),
                "parent_station": row.get("parent_station"),
            })

    print("[SUCCESS] dim_stops created")


if __name__ == "__main__":
    parse_stops()
