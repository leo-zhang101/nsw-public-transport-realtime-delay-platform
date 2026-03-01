# NSW Transit Sentinel: Real-time Public Transport Delay Platform
End-to-end Data Lakehouse for monitoring Sydney's transit reliability using GTFS Realtime feeds, AWS, and Spark.


## Project Overview

This platform ingests high-velocity GTFS Realtime (Protocol Buffers) and GTFS Static data from Transport for NSW (TfNSW) to provide actionable insights into network delays. It transforms raw telemetry into a structured semantic layer for bottleneck analysis.

-Key Performance Indicators (KPIs)
1.Route-level Reliability: Aggregated mean/peak latency per route.
2.Station Bottleneck Analysis: Identification of high-congestion stops (e.g., Central Station).
3.Trip-level Fact Table: Enriched historical delay records for deep-dive diagnostics.

### System Architecture
The pipeline follows a Medallion Architecture (Bronze → Silver → Gold) to ensure data quality and lineage.
1.Ingestion: Automated fetching of GTFS Static ZIPs and Realtime Protobuf streams via Python.
2.Processing: PySpark jobs for decoding binary entities and joining high-velocity facts with static dimensions.
3.Analytics: Aggregation layer (delay_kpis.py) generating business-ready metrics with built-in schema validation.
4.Orchestration: Fully containerized workflow using Docker Compose and Apache Airflow for task scheduling and error handling.

### skill
Category,Technology
Language,"Python 3.x (Pandas, PySpark)"
Data Source,TfNSW Open Data API (GTFS/GTFS-R)
Orchestration,Apache Airflow
Infrastructure,"Docker, Docker Compose"
Storage/Format,"AWS S3 (Logical), Parquet, CSV"

### Engineering Highlights & Observations
1.Binary Decoding: Implemented robust logic to handle Protobuf entities, ensuring sub-second parsing of vehicle positions and trip updates.
2.Schema Enforcement: Integrated a custom validation layer in delay_kpis.py to prevent pipeline crashes from upstream API changes.

###  Example Output 

| route_id     | route_short_name | avg_delay_sec | max_delay_sec | events |
|-------------|------------------|---------------|---------------|--------|
| 1-10M-sj2-2 | 10M              | 30            | 120           | 2      |

### Observations

- Route 10M shows an average delay of 30 seconds, with peak delays reaching 120 seconds
- Delay events are concentrated at major interchange stops such as Central Station
- This suggests congestion impact during peak interchange periods
