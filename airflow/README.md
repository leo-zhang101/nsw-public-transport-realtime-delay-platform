# Airflow – GTFS Delay Pipeline

This directory contains a fully reproducible Apache Airflow setup
for orchestrating the NSW Public Transport GTFS delay analytics pipeline.

## Architecture

Airflow orchestrates the following steps:

1. Parse GTFS Realtime Trip Updates
2. Join realtime delays with GTFS static data
3. Generate route-level and stop-level delay KPIs

## Prerequisites

- Docker
- Docker Compose

## Start Airflow

From the `airflow/` directory:

```bash
docker compose up -d

# Airflow Pipeline

This project uses **Apache Airflow (Docker-based)** to orchestrate a GTFS realtime delay analytics pipeline.

---

## Architecture
