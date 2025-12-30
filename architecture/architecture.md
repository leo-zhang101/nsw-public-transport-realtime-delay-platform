# Architecture Design

## 1. Project Goal

The goal of this project is to build an end-to-end data engineering platform that monitors real-time public transport delays in NSW using GTFS Realtime feeds.

The platform focuses on:
- Near real-time ingestion of public transport operational data
- Scalable data lake storage using AWS S3
- Data processing for delay detection and aggregation
- Analytics-ready datasets for querying and visualization

This project is designed to reflect real-world data engineering practices rather than a toy example.

---

## 2. Data Sources

### 2.1 GTFS Realtime Feeds (TfNSW)

The project consumes the following GTFS Realtime data sources provided by Transport for NSW:
- Trip Updates: provides delay and schedule deviation information
- Vehicle Positions: provides real-time vehicle location data
- Alerts: provides service disruption and incident information

These feeds are delivered via HTTP endpoints and updated frequently.

### 2.2 Static GTFS Data

Static GTFS datasets are used as reference data:
- Stops
- Routes
- Trips
- Calendar

Static data is used to enrich realtime events and provide dimensional context.

---

## 3. High-Level Architecture

The platform follows a cloud-native data lake architecture with separation of concerns between ingestion, processing, storage, and analytics.

High-level components:
- Ingestion layer: pulls GTFS Realtime data from APIs
- Storage layer: AWS S3 (raw, silver, gold layers)
- Processing layer: Spark (batch or micro-batch)
- Query layer: Amazon Athena
- Warehouse layer: Amazon Redshift
- Orchestration layer: Apache Airflow
- Monitoring layer: dashboards and metrics

---

## 4. Data Flow

1. GTFS Realtime data is ingested from TfNSW APIs at regular intervals.
2. Raw JSON data is stored in S3 raw layer without modification.
3. Spark jobs parse, validate, and normalize the data.
4. Cleaned and structured data is written to S3 silver layer in Parquet format.
5. Aggregated delay metrics are generated and stored in S3 gold layer.
6. Gold datasets are queried directly via Athena for ad-hoc analysis.
7. Curated datasets are loaded into Redshift for analytical queries and dashboards.
8. Airflow orchestrates ingestion and processing workflows.

---

## 5. Technology Choices

### 5.1 Why AWS S3

- Low-cost and scalable object storage
- Enables separation of storage and compute
- Supports data lake patterns with multiple consumers

### 5.2 Why Spark

- Handles semi-structured GTFS data efficiently
- Supports both batch and near real-time processing
- Scales horizontally for large data volumes

### 5.3 Why Athena and Redshift

- Athena is used for fast ad-hoc queries on S3 data
- Redshift is used for structured analytical workloads and BI use cases
- This separation reflects common industry practice

### 5.4 Why Airflow

- Provides explicit workflow orchestration
- Enables monitoring, retries, and scheduling
- Widely used in production data platforms

---

## 6. Design Trade-offs

- Realtime vs near real-time: micro-batch processing is chosen for simplicity and reliability.
- S3 is used instead of a traditional database for raw data to ensure scalability.
- Redshift is used selectively to avoid unnecessary cost for exploratory queries.

This design prioritizes clarity, scalability, and real-world applicability over premature optimization.