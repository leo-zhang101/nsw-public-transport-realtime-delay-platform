"""
Module: analytics/delay_kpis.py
Author: leo-zhang101
Function: Computes Route and Station level latency KPIs from enriched GTFS-R data.
"""

import logging
import sys
import pandas as pd
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "data/analytics/delay_enriched.csv"
OUTPUT_DIR = BASE_DIR / "data/analytics/kpis"

def run_kpis():

    
    try:
      
        if not INPUT_FILE.exists():
            logger.error(f"Missing input telemetry: {INPUT_FILE}")
            return

        logger.info(f"Ingesting enriched data: {INPUT_FILE.name}")
        df = pd.read_csv(INPUT_FILE)

       
        if "max_delay_sec" not in df.columns:
            logger.error("Data Quality Error: Column 'max_delay_sec' not found.")
            return

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


        logger.info("Calculating route-level performance metrics...")
        route_kpi = (
            df.groupby(["route_id", "route_short_name", "route_long_name"], dropna=False)
            .agg(
                avg_delay_sec=("max_delay_sec", "mean"),
                max_delay_sec=("max_delay_sec", "max"),
                sample_count=("max_delay_sec", "count"), 
            )
            .round(2) 
            .reset_index()
        )

        route_output = OUTPUT_DIR / "kpi_route_delay.csv"
        route_kpi.to_csv(route_output, index=False)


        logger.info("Calculating stop-level bottleneck metrics...")
        stop_kpi = (
            df.groupby(["stop_id", "stop_name"], dropna=False)
            .agg(
                avg_delay_sec=("max_delay_sec", "mean"),
                max_delay_sec=("max_delay_sec", "max"),
                sample_count=("max_delay_sec", "count"),
            )
            .round(2)
            .reset_index()
        )

        stop_output = OUTPUT_DIR / "kpi_stop_delay.csv"
        stop_kpi.to_csv(stop_output, index=False)

        logger.info(f"[SUCCESS] Metrics generated at: {OUTPUT_DIR}")

    except Exception as e:
       
        logger.exception(f"Pipeline failed unexpectedly: {e}")
        sys.exit(1) 

if __name__ == "__main__":
    run_kpis()
