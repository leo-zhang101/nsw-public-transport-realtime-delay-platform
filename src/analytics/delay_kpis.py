"""
Calculate delay KPIs from enriched GTFS realtime delay data.

Outputs:
- KPI per route
- KPI per stop
"""

import pandas as pd
from pathlib import Path


# =========================
# Config
# =========================
INPUT_FILE = Path("data/analytics/delay_enriched.csv")
OUTPUT_DIR = Path("data/analytics/kpis")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Main Logic
# =========================
def run_kpis():
    print("[INFO] Loading delay_enriched.csv")

    df = pd.read_csv(INPUT_FILE)

    # -------------------------
    # Route-level KPIs
    # -------------------------
    print("[INFO] Calculating route delay KPIs")

    route_kpi = (
        df.groupby(
            ["route_id", "route_short_name", "route_long_name"],
            dropna=False
        )
        .agg(
            avg_delay_sec=("max_delay_sec", "mean"),
            max_delay_sec=("max_delay_sec", "max"),
            events=("max_delay_sec", "count"),
        )
        .reset_index()
    )

    route_output = OUTPUT_DIR / "kpi_route_delay.csv"
    route_kpi.to_csv(route_output, index=False)

    # -------------------------
    # Stop-level KPIs
    # -------------------------
    print("[INFO] Calculating stop delay KPIs")

    stop_kpi = (
        df.groupby(
            ["stop_id", "stop_name"],
            dropna=False
        )
        .agg(
            avg_delay_sec=("max_delay_sec", "mean"),
            max_delay_sec=("max_delay_sec", "max"),
            events=("max_delay_sec", "count"),
        )
        .reset_index()
    )

    stop_output = OUTPUT_DIR / "kpi_stop_delay.csv"
    stop_kpi.to_csv(stop_output, index=False)

    print("[SUCCESS] KPI files created")
    print(f"[OUTPUT] {route_output}")
    print(f"[OUTPUT] {stop_output}")


# =========================
# Entrypoint
# =========================
if __name__ == "__main__":
    run_kpis()
