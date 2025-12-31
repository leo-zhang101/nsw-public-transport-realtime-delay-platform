import csv
from pathlib import Path

FACT_DIR = Path("data/fact/gtfs_static")
INPUT_FILE = FACT_DIR / "fact_stop_times.csv"
OUTPUT_FILE = FACT_DIR / "fact_stop_times_normalized.csv"


def time_to_seconds(t):
    """
    Convert HH:MM:SS (possibly >24h) to seconds since service day start
    """
    if not t:
        return None

    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s


def normalize_stop_times():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    print(f"[INFO] Reading {INPUT_FILE}")
    print(f"[INFO] Writing {OUTPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + [
            "arrival_secs",
            "departure_secs"
        ]

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["arrival_secs"] = time_to_seconds(row.get("arrival_time"))
            row["departure_secs"] = time_to_seconds(row.get("departure_time"))
            writer.writerow(row)

    print("[SUCCESS] stop_times normalized")


if __name__ == "__main__":
    normalize_stop_times()
