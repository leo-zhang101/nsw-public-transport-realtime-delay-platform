import requests
import json
from pathlib import Path
from datetime import date

CATALOGUE_API = "https://opendata.transport.nsw.gov.au/api/3/action/package_search"
QUERY = "gtfs"
OUTPUT_DIR = Path("data/catalogue_snapshots")

def fetch_catalogue():
    snapshot_date = date.today().isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"datasets_gtfs_{snapshot_date}.json"

    params = {
        "q": QUERY,
        "rows": 100
    }

    print("[INFO] Fetching dataset catalogue from NSW Transport Open Data")

    response = requests.get(CATALOGUE_API, params=params)
    response.raise_for_status()

    data = response.json()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[SUCCESS] Catalogue saved to {output_file}")
    print(f"[INFO] Total datasets found: {data['result']['count']}")

if __name__ == "__main__":
    fetch_catalogue()
