# NSW Transit Sentinel: Real-time Public Transport Delay Platform
End-to-end data platform for analysing public transport delays in Sydney using GTFS Realtime feeds, Spark, and AWS-style data lake architecture.


## Project Overview

This project simulates a real-world data engineering scenario by ingesting high-frequency GTFS Realtime (Protocol Buffers) and GTFS Static data from Transport for NSW (TfNSW).

The system transforms raw telemetry into structured datasets to support delay analysis, operational monitoring, and decision-making.

### Key Business Questions
The platform is designed to answer practical analytics questions:
	Which routes are consistently delayed?
	Which stations experience the highest congestion?
	How do delays vary across time (peak vs off-peak)?
  What are the worst-case delay scenarios in the network?

### Key Metrics (KPIs)
Route-level average delay (avg_delay_sec)
Route-level peak delay (max_delay_sec)
Delay event frequency per route
Station-level congestion indicators
Trip-level historical delay records

  
### System Architecture
The pipeline follows a Medallion Architecture (Bronze → Silver → Gold) to ensure data quality and lineage.
1.Ingestion: Automated fetching of GTFS Static ZIPs and Realtime Protobuf streams via Python.
2.Processing: PySpark jobs for decoding binary entities and joining high-velocity facts with static dimensions.
3.Analytics: Aggregation layer (delay_kpis.py) generating business-ready metrics with built-in schema validation.
4.Orchestration: Fully containerized workflow using Docker Compose and Apache Airflow for task scheduling and error handling.

### Data Pipeline
  Ingestion
Python-based ingestion of GTFS Static ZIP files and Realtime Protobuf streams
  Processing
PySpark jobs for decoding binary Protobuf messages and joining with static metadata
  Analytics
Aggregation logic implemented in delay_kpis.py to generate business-ready metrics
  Orchestration
Airflow + Docker Compose for scheduling, retry handling, and pipeline automation

### Engineering Highlights & Observations
Implemented Protobuf decoding logic to process high-frequency GTFS Realtime data
Built scalable Spark-based transformations for large-volume event processing
Designed a modular Medallion architecture to improve data quality and lineage
Added schema validation to prevent failures caused by upstream API changes
Containerised the pipeline using Docker for reproducibility and deployment

###  Example Output 

| route_id     | route_short_name | avg_delay_sec | max_delay_sec | events |
|-------------|------------------|---------------|---------------|--------|
| 1-10M-sj2-2 | 10M              | 30            | 120           | 2      |

### Insights & Analysis

Route 10M shows moderate average delay (~30 seconds) but extreme peak delays (up to 120 seconds)
Delay events are concentrated around major interchange stations such as Central Station
This suggests congestion bottlenecks during peak transfer periods
High variance between average and max delay indicates unstable service reliability

### Tech Stack
Python, PySpark, AWS S3 (logical), Airflow, Docker, GTFS Realtime (Protobuf), Parquet

### Optional Visualisation

Delay distribution by route
Peak vs off-peak delay comparison
Top congested stations
Delay trend over time
