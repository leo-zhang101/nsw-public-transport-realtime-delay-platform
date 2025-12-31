import os
import requests
from datetime import datetime
from pathlib import Path

GTFS_TRIP_UPDATES_URL = (
    "https://api.transport.nsw.gov.au/v1/gtfs/realtime/"
    "trip-updates"
)

OUTPUT_BASE_DIR = Path("data/raw/gtfs_realtime/trip_updates")

API_KEY = os.getenv("TFNSW_API_KEY")
if not API_KEY:
    raise RuntimeError("TFNSW_API_KEY not set")

HEADERS = {
    "Authorization": f"apikey {API_KEY}"
}


def fetch_trip_updates():
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_BASE_DIR / f"ts={ts}"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "trip_updates.pb"

    print("[INFO] Fetching GTFS Realtime Trip Updates")
    r = requests.get(GTFS_TRIP_UPDATES_URL, headers=HEADERS)
    r.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(r.content)

    print(f"[SUCCESS] Saved to {output_file}")


if __name__ == "__main__":
    fetch_trip_updates()
