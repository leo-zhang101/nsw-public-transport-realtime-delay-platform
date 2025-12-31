import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
import csv

def parse_trip_updates(input_path: str):
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_dir = Path("data/fact/gtfs_realtime")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "fact_trip_updates.csv"

    rows = []

    with open(input_file) as f:
        data = json.load(f)

    for entity in data.get("entity", []):
        trip_update = entity.get("trip_update")
        if not trip_update:
            continue

        trip = trip_update.get("trip", {})
        for stu in trip_update.get("stop_time_update", []):
            rows.append({
                "trip_id": trip.get("trip_id"),
                "route_id": trip.get("route_id"),
                "direction_id": trip.get("direction_id"),
                "stop_id": stu.get("stop_id"),
                "arrival_delay": stu.get("arrival", {}).get("delay"),
                "departure_delay": stu.get("departure", {}).get("delay"),
                "event_ts": datetime.now(timezone.utc).isoformat()
            })

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("[SUCCESS] fact_trip_updates created")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    parse_trip_updates(args.input)
