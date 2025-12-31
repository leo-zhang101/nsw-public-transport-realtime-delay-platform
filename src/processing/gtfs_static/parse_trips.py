import csv
import os
from datetime import date


def parse_trips(dt: str | None = None):
    if dt is None:
        dt = str(date.today())

    in_path = f"data/raw/gtfs_static_full/dt={dt}/extracted/trips.txt"
    out_dir = "data/dim/gtfs_static"
    out_path = f"{out_dir}/dim_trips.csv"

    os.makedirs(out_dir, exist_ok=True)

    print(f"[INFO] Reading {in_path}")

    with open(in_path, "r", encoding="utf-8-sig", newline="") as f_in:
        reader = csv.DictReader(f_in)

        required = {"trip_id", "route_id", "service_id"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"Missing columns: {missing}")

        print(f"[INFO] Writing {out_path}")
        with open(out_path, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.DictWriter(
                f_out,
                fieldnames=[
                    "trip_id",
                    "route_id",
                    "service_id",
                    "direction_id",
                    "shape_id",
                ],
            )
            writer.writeheader()

            for row in reader:
                writer.writerow(
                    {
                        "trip_id": row["trip_id"],
                        "route_id": row["route_id"],
                        "service_id": row["service_id"],
                        "direction_id": row.get("direction_id"),
                        "shape_id": row.get("shape_id"),
                    }
                )

    print("[SUCCESS] dim_trips created")


if __name__ == "__main__":
    parse_trips("2025-12-31")
