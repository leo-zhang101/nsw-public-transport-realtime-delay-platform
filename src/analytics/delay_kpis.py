"""
delay_metrics.py
Author: leo-zhang101
    Calculates operational KPIs (Route/Stop latency) for the NSW Transport platform.
    Integrated with Airflow/Docker environment.
"""


import pandas as pd
from pathlib import Path



INPUT_FILE = Path("data/analytics/delay_enriched.csv")
OUTPUT_DIR = Path("data/analytics/kpis")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



def run_kpis():
    print("[INFO] Loading delay_enriched.csv")

    df = pd.read_csv(INPUT_FILE)


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
    route_kpi.to_csv(route_output, index=False
                    
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


if __name__ == "__main__":
    run_kpis()
