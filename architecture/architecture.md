# Architecture Design

## 1. Project Goal

The goal of this project is to build an end-to-end data engineering platform that monitors real-time public transport delays in NSW using GTFS Realtime feeds.

The platform focuses on:
1. Near real-time ingestion of public transport operational data
2. Scalable data lake storage using AWS S3
3. Data processing for delay detection and aggregation
4. Analytics-ready datasets for querying and visualization

This project is designed to reflect real-world data engineering practices rather than a toy example.


## 2. Data Sources

### 2.1 GTFS Realtime Feeds (TfNSW)

A key challenge was the Clock Skew and Stale Updates often found in the TfNSW Realtime feed. The ingestion logic includes a filter to drop any messages where timestamp is older than the current window to maintain the integrity of delay KPIs.

These feeds are delivered via HTTP endpoints and updated frequently.

### 2.2 Static GTFS Data

Static GTFS datasets are used as reference data:
1.Stops
2. Routes
3.Trips
4.Calendar

Static data is used to enrich realtime events and provide dimensional context.

## 3. High-Level Architecture

The platform follows a cloud-native data lake architecture with separation of concerns between ingestion, processing, storage, and analytics.

High-level components:
1. Ingestion layer: pulls GTFS Realtime data from APIs
2. Storage layer: AWS S3 (raw, silver, gold layers)
3.Processing layer: Spark (batch or micro-batch)
4. Query layer: Amazon Athena
5. Warehouse layer: Amazon Redshift
6. Orchestration layer: Apache Airflow
7. Monitoring layer: dashboards and metrics

## 4. Data Flow

1. GTFS Realtime data is ingested from TfNSW APIs at regular intervals.
2. Raw JSON data is stored in S3 raw layer, partitioned by year/month/day/hour to enable efficient incremental loading.
3. Spark jobs parse, validate, and normalize the data.
4. Silver layer data is stored in Parquet format, optimized with Snappy compression to reduce S3 storage costs and improve Athena query performance.
5. Aggregated delay metrics are generated and stored in S3 gold layer.
6. Gold datasets are queried directly via Athena for ad-hoc analysis.
7. Curated datasets are loaded into Redshift for analytical queries and dashboards.
8. Airflow orchestrates ingestion and processing workflows.


## 5. Technology Choices

### 5.1 Why AWS S3

Low-cost and scalable object storage. Enables separation of storage and compute. Supports data lake patterns with multiple consumers

### 5.2 Why Spark

Initially, Pandas was considered for its simplicity, but PySpark was chosen to handle the potential horizontal scaling required for high-frequency GTFS-R binary entities and to leverage Schema Enforcement during the Silver layer transformation.

### 5.3 Why Athena and Redshift

1. Athena is used for fast ad-hoc queries on S3 data
2. Redshift is used for structured analytical workloads and BI use cases
3. This separation reflects common industry practice

### 5.4 Why Airflow

Airflow provides explicit workflow orchestration. Task retries and SLA monitoring are implemented to handle intermittent TfNSW API timeouts, ensuring the pipeline is idempotent and can be re-run without data duplication.


## 6. Design Trade-offs

1. Realtime vs near real-time: micro-batch processing is chosen for simplicity and reliability.
2. S3 is used instead of a traditional database for raw data to ensure scalability.
3. Redshift is used selectively to avoid unnecessary cost for exploratory queries.
4. Schema Rigidity vs. Flexibility：Initially, a schema-on-read approach was considered for the raw layer. However, due to frequent (though minor) updates in the TfNSW GTFS-R Protobuf definition, a structured Schema Enforcement step was added in the Spark processing stage to prevent downstream analytics from breaking.

This design prioritizes clarity, scalability, and real-world applicability over premature optimization.
