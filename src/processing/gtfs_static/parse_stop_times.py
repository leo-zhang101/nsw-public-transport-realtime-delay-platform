import csv
from pathlib import Path

RAW_BASE_DIR = Path("data/raw/gtfs_static_full")
FACT_BASE_DIR = Path("data/fact/gtfs_static")

def parse_stop_times():
    # 自动找最新 dt= 目录
    dt_dirs = sorted([p for p in RAW_BASE_DIR.iterdir() if p.is_dir() and p.name.startswith("dt=")])
    if not dt_dirs:
        raise RuntimeError("No dt= directories found in raw GTFS static data")

    latest_dt = dt_dirs[-1]
    input_file = latest_dt / "extracted" / "stop_times.txt"

    if not input_file.exists():
        raise FileNotFoundError(f"stop_times.txt not found: {input_file}")

    FACT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    output_file = FACT_BASE_DIR / "fact_stop_times.csv"

    print(f"[INFO] Reading {input_file}")
    print(f"[INFO] Writing {output_file}")

    with open(input_file, "r", encoding="utf-8-sig") as f_in, \
         open(output_file, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = [
            "trip_id",
            "stop_id",
            "stop_sequence",
            "arrival_time",
            "departure_time"
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            writer.writerow({
                "trip_id": row["trip_id"],
                "stop_id": row["stop_id"],
                "stop_sequence": row["stop_sequence"],
                "arrival_time": row.get("arrival_time"),
                "departure_time": row.get("departure_time")
            })

    print("[SUCCESS] fact_stop_times created")

if __name__ == "__main__":
    parse_stop_times()
