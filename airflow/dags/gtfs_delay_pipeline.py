from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_DIR = "/opt/airflow/project"
DATA_DIR = "/opt/airflow/data"

with DAG(
    dag_id="gtfs_delay_pipeline",
    start_date=datetime(2025, 1, 1),
    # take on by hand
    schedule_interval=None,   
    catchup=False,
    tags=["gtfs", "analytics"],
) as dag:

    # 1.Ingest and parse real-time Protobuf feed from TfNSW
    # 2.Logical join between Real-time updates and GTFS Static schedule
    parse_trip_updates = BashOperator(
        task_id="parse_trip_updates",
        bash_command=f"""
        python {PROJECT_DIR}/src/processing/gtfs_realtime/parse_trip_updates.py \
          --input {DATA_DIR}/raw/gtfs_realtime_mock/trip_updates_expanded.json
        """
    )

    # 2.Join realtime + static → delay_enriched
    join_delay_analysis = BashOperator(
        task_id="join_delay_analysis",
        bash_command=f"""
        python {PROJECT_DIR}/src/analytics/join_delay_analysis.py
        """
    )

    # 3.KPI 
    delay_kpis = BashOperator(
        task_id="delay_kpis",
        bash_command=f"""
        python {PROJECT_DIR}/src/analytics/delay_kpis.py
        """
    )

    # DAG 
    parse_trip_updates >> join_delay_analysis >> delay_kpis
