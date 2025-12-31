import json
from pathlib import Path

CATALOGUE_FILE = Path("data/catalogue_snapshots/datasets_gtfs_2025-12-30.json")

KEYWORDS = [
    "Timetables Complete GTFS",
    "Timetables - Complete - GTFS"
]

def extract_gtfs_static_url():
    with open(CATALOGUE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data["result"]["results"]

    for dataset in results:
        title = dataset.get("title", "")
        if any(k.lower() in title.lower() for k in KEYWORDS):
            print(f"[FOUND DATASET] {title}")

            for res in dataset.get("resources", []):
                if res.get("format", "").lower() == "zip":
                    print("[FOUND ZIP]")
                    print("Name :", res.get("name"))
                    print("URL  :", res.get("url"))
                    return

    print("[ERROR] GTFS Static ZIP not found")

if __name__ == "__main__":
    extract_gtfs_static_url()
