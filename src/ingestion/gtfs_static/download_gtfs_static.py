import requests
from pathlib import Path
from datetime import date

GTFS_STATIC_ZIP_URL = (
    "https://opendata.transport.nsw.gov.au/data/dataset/"
    "d1f68d4f-b778-44df-9823-cf2fa922e47f/resource/"
    "67974f14-01bf-47b7-bfa5-c7f2f8a950ca/download/"
    "full_greater_sydney_gtfs_static_0.zip"
)

OUTPUT_BASE_DIR = Path("data/raw/gtfs_static_full")


def download_gtfs_static():
    snapshot_date = date.today().isoformat()
    output_dir = OUTPUT_BASE_DIR / f"dt={snapshot_date}"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "gtfs_static.zip"

    print(f"[INFO] Downloading GTFS Static ZIP for {snapshot_date}")
    print(f"[INFO] Saving to {output_file}")

    response = requests.get(GTFS_STATIC_ZIP_URL, stream=True)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("[SUCCESS] GTFS Static ZIP downloaded successfully")


if __name__ == "__main__":
    download_gtfs_static()
