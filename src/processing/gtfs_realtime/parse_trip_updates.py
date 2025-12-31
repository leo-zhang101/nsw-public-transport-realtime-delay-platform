from datetime import datetime
import json
import csv
from pathlib import Path

INPUT_FILE = Path("data/raw/gtfs_realtime_mock/trip_updates.json")
OUTPUT_DIR = Path("data/fact/gtfs_realtime")
OUTPUT_FILE = OUTPUT_DIR / "fact_trip_updates.csv"

def parse_trip_updates():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE) as f:
        data = json.load(f)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "trip_id",
                "route_id",
                "direction_id",
                "stop_id",
                "arrival_delay",
                "departure_delay",
                "event_ts"
            ]
        )
        writer.writeheader()

        for entity in data.get("entity", []):
            tu = entity.get("trip_update")
            if not tu:
                continue

            trip = tu.get("trip", {})
            for stu in tu.get("stop_time_update", []):
                writer.writerow({
                    "trip_id": trip.get("trip_id"),
                    "route_id": trip.get("route_id"),
                    "direction_id": trip.get("direction_id"),
                    "stop_id": stu.get("stop_id"),
                    "arrival_delay": stu.get("arrival", {}).get("delay"),
                    "departure_delay": stu.get("departure", {}).get("delay"),
                    "event_ts": datetime.utcnow().isoformat()
                })

    print("[SUCCESS] fact_trip_updates created")

if __name__ == "__main__":
    parse_trip_updates()
