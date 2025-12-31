import pandas as pd
from pathlib import Path

DIM_DIR = Path("data/dim/gtfs_static")
FACT_DIR = Path("data/fact/gtfs_realtime")
OUTPUT_DIR = Path("data/analytics")

def run_delay_analysis():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("[INFO] Loading fact_trip_updates")
    df = pd.read_csv(FACT_DIR / "fact_trip_updates.csv")

    print("[INFO] Loading dim_routes")
    dim_routes = pd.read_csv(DIM_DIR / "dim_routes.csv")

    print("[INFO] Loading dim_stops")
    dim_stops = pd.read_csv(DIM_DIR / "dim_stops.csv")

    df["route_id"] = df["route_id"].astype(str).str.strip()
    dim_routes["route_id"] = dim_routes["route_id"].astype(str).str.strip()

    df["stop_id"] = df["stop_id"].astype(str).str.strip()
    dim_stops["stop_id"] = dim_stops["stop_id"].astype(str).str.strip()

    print("[INFO] Joining trips → routes")
    df = df.merge(
        dim_routes[["route_id", "route_short_name", "route_long_name"]],
        on="route_id",
        how="left",
        validate="m:1"
    )

    print("[INFO] Joining fact → stops")
    df = df.merge(
        dim_stops[["stop_id", "stop_name"]],
        on="stop_id",
        how="left",
        validate="m:1"
    )

    print("[INFO] Calculating delay metrics")
    df["max_delay_sec"] = df[["arrival_delay", "departure_delay"]].max(axis=1)

    output_file = OUTPUT_DIR / "delay_enriched.csv"
    df.to_csv(output_file, index=False)

    print(f"[SUCCESS] Delay analysis written to {output_file}")

if __name__ == "__main__":
    run_delay_analysis()
