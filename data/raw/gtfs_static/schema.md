# GTFS Static Schema (Timetables Complete GTFS) — Production Template

> Dataset: Transport for NSW — **Timetables Complete GTFS (Static)**
>
> Purpose in this project:
> - Provide **dimension/reference tables** for joining GTFS Realtime data (Trip Updates / Vehicle Positions)
> - Build a stable **semantic layer** (routes, trips, stops, service calendars)
>
> Storage guideline:
> - Full GTFS ZIP/CSVs are **NOT stored in GitHub** (size + update frequency)
> - Repo contains only: schema + small samples (10–50 rows)

---

## 1. Files Included (GTFS Static Standard)

Typical files inside the GTFS ZIP (not all are always present, but NSW usually includes most):

### Core (must-have for this project)
- `agency.txt`
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`
- `calendar.txt` and/or `calendar_dates.txt`

### Common optional files (useful but not required initially)
- `shapes.txt` (route geometry)
- `fare_attributes.txt`, `fare_rules.txt` (fares)
- `transfers.txt` (transfer rules)
- `frequencies.txt` (headway-based services)
- `feed_info.txt` (feed metadata)
- `pathways.txt`, `levels.txt` (station pathways extension)
- `translations.txt` (multilingual)

---

## 2. Key Concepts (Interview-ready)

### 2.1 Dimensions vs Facts (in this project)
- **Dimensions (static):** routes, trips, stops, calendars
- **Facts (realtime):** trip updates (delays), vehicle positions (locations)

### 2.2 Primary join keys to Realtime
- `trip_id` (GTFS Static `trips.txt`) ↔ Realtime Trip Updates `trip.trip_id`
- `route_id` (GTFS Static `routes.txt`) used for aggregation/reporting
- `stop_id` (GTFS Static `stops.txt`) ↔ Trip Updates `stop_time_update.stop_id`
- `service_id` (calendar) determines operating days for a trip

### 2.3 Grain (Data granularity)
- `trips.txt`: **1 row = 1 scheduled trip**
- `stop_times.txt`: **1 row = 1 scheduled stop time within a trip**
- `stops.txt`: **1 row = 1 stop/station**
- Realtime Trip Updates: **1 message contains updates for a trip, often multiple stops**

---

## 3. Table Schemas (Core)

> Notes:
> - Data types below are “logical types” for your Silver layer (Parquet/Glue Catalog).
> - Raw CSVs are strings; cast in processing.

---

### 3.1 `agency` (from `agency.txt`)
**Role:** Reference dimension (operator/agency)

| Column | Type | Required | Meaning / How used |
|---|---:|---:|---|
| `agency_id` | string | optional* | Agency identifier (required if multiple agencies) |
| `agency_name` | string | yes | Operator name |
| `agency_url` | string | yes | Operator URL |
| `agency_timezone` | string | yes | Timezone (important for schedule interpretation) |
| `agency_lang` | string | no | Language code |
| `agency_phone` | string | no | Contact phone |
| `agency_fare_url` | string | no | Fare info URL |

**Keys**
- PK: `agency_id` (if present), else `agency_name`

---

### 3.2 `routes` (from `routes.txt`)
**Role:** Dimension — high-level route/line (bus route, train line)

| Column | Type | Required | Meaning / How used |
|---|---:|---:|---|
| `route_id` | string | yes | **Route key** (join from `trips.route_id`) |
| `agency_id` | string | no | Join to `agency` |
| `route_short_name` | string | no | Display short name |
| `route_long_name` | string | no | Display long name |
| `route_desc` | string | no | Description |
| `route_type` | int | yes | Mode (bus/train/ferry etc.) used for grouping |
| `route_url` | string | no | URL |
| `route_color` | string | no | UI |
| `route_text_color` | string | no | UI |

**Keys**
- PK: `route_id`

**Important usage in this project**
- Used to aggregate delays by route and mode (bus/train/metro)
- Often used for dashboard dimensions

---

### 3.3 `stops` (from `stops.txt`)
**Role:** Dimension — stop/station

| Column | Type | Required | Meaning / How used |
|---|---:|---:|---|
| `stop_id` | string | yes | **Stop key** (join from realtime `stop_id`) |
| `stop_code` | string | no | Public code |
| `stop_name` | string | yes | Stop name |
| `stop_desc` | string | no | Description |
| `stop_lat` | double | no | Latitude |
| `stop_lon` | double | no | Longitude |
| `zone_id` | string | no | Fare zone |
| `stop_url` | string | no | URL |
| `location_type` | int | no | 0=stop, 1=station, etc. |
| `parent_station` | string | no | Parent station for platforms |
| `stop_timezone` | string | no | Rare |
| `wheelchair_boarding` | int | no | Accessibility |

**Keys**
- PK: `stop_id`

**Important usage in this project**
- Delay by stop/station, heatmaps, top delayed stops
- Join vehicle positions to nearest stop (later enhancement)

---

### 3.4 `trips` (from `trips.txt`)
**Role:** Dimension-ish (trip is scheduled entity; serves as join bridge)

| Column | Type | Required | Meaning / How used |
|---|---:|---:|---|
| `route_id` | string | yes | Join to `routes` |
| `service_id` | string | yes | Join to calendar |
| `trip_id` | string | yes | **Primary join key to realtime** |
| `trip_headsign` | string | no | Destination display |
| `trip_short_name` | string | no | Short name |
| `direction_id` | int | no | 0/1 direction |
| `block_id` | string | no | Vehicle block (useful for operations) |
| `shape_id` | string | no | Join to `shapes` if used |
| `wheelchair_accessible` | int | no | Accessibility |
| `bikes_allowed` | int | no | Bikes policy |

**Keys**
- PK: `trip_id`
- FK: `route_id`, `service_id`, `shape_id`

**Important usage in this project**
- Realtime Trip Updates reference `trip_id` → join to get `route_id`/`service_id`
- Enables route-level delay aggregation

---

### 3.5 `stop_times` (from `stop_times.txt`)
**Role:** Bridge + schedule reference (enables planned vs actual comparisons)

| Column | Type | Required | Meaning / How used |
|---|---:|---:|---|
| `trip_id` | string | yes | Join to `trips` |
| `arrival_time` | string | yes | Scheduled arrival (HH:MM:SS; may exceed 24h) |
| `departure_time` | string | yes | Scheduled departure |
| `stop_id` | string | yes | Join to `stops` |
| `stop_sequence` | int | yes | Stop order within trip |
| `stop_headsign` | string | no | Per-stop headsign |
| `pickup_type` | int | no | Pickup rules |
| `drop_off_type` | int | no | Drop-off rules |
| `shape_dist_traveled` | double | no | Distance along shape |
| `timepoint` | int | no | Timing point indicator |

**Keys**
- Composite PK: (`trip_id`, `stop_sequence`)  
- Alternate uniqueness: (`trip_id`, `stop_id`, `stop_sequence`)

**Important usage in this project**
- Compare realtime stop_time_update against scheduled times
- Compute delay metrics at stop-level (e.g., planned vs actual)

**Time handling warning**
- GTFS times can be `25:10:00` etc. (service after midnight).  
  In Silver layer, store:
  - `arrival_time_str` (original)
  - `arrival_seconds` (int) for analytics

---

## 4. Service Calendar (Operating Days)

### 4.1 `calendar` (from `calendar.txt`)
**Role:** Dimension — weekly service pattern

| Column | Type | Required | Meaning |
|---|---:|---:|---|
| `service_id` | string | yes | Join key to `trips.service_id` |
| `monday`...`sunday` | int | yes | 0/1 flags |
| `start_date` | string | yes | YYYYMMDD |
| `end_date` | string | yes | YYYYMMDD |

**Keys**
- PK: `service_id`

### 4.2 `calendar_dates` (from `calendar_dates.txt`)
**Role:** Overrides — exceptions/holidays

| Column | Type | Required | Meaning |
|---|---:|---:|---|
| `service_id` | string | yes | Join key |
| `date` | string | yes | YYYYMMDD |
| `exception_type` | int | yes | 1=added, 2=removed |

**Usage**
- If both `calendar` and `calendar_dates` exist, you must apply exceptions to derive “service runs on date D”.

---

## 5. Optional Geometry (for maps later)

### `shapes` (from `shapes.txt`)
**Role:** Polyline geometry for routes/trips (optional initially)

| Column | Type | Required | Meaning |
|---|---:|---:|---|
| `shape_id` | string | yes | Join from `trips.shape_id` |
| `shape_pt_lat` | double | yes | Lat |
| `shape_pt_lon` | double | yes | Lon |
| `shape_pt_sequence` | int | yes | Order |
| `shape_dist_traveled` | double | no | Distance |

---

## 6. Recommended Silver Layer (Parquet) Table Design

> Goal: convert raw CSV → clean typed Parquet tables with stable schema.

### 6.1 Tables (Silver)
- `dim_agency`
- `dim_routes`
- `dim_stops`
- `dim_trips`
- `bridge_stop_times`
- `dim_service_calendar` (derived from calendar + calendar_dates)
- `dim_shapes` (optional)

### 6.2 Partition strategy (optional)
Static GTFS is periodic snapshots, so partition by:
- `feed_date` (YYYY-MM-DD) or `ingestion_date`
Example:
- `s3://.../silver/gtfs_static/dim_routes/feed_date=2025-12-30/`

---

## 7. Data Quality Rules (must-have for production style)

### 7.1 Completeness
- `routes.route_id` NOT NULL
- `trips.trip_id` NOT NULL
- `stops.stop_id` NOT NULL
- `stop_times.trip_id` and `stop_times.stop_id` NOT NULL

### 7.2 Referential Integrity
- `trips.route_id` must exist in `routes.route_id`
- `stop_times.trip_id` must exist in `trips.trip_id`
- `stop_times.stop_id` must exist in `stops.stop_id`
- `trips.service_id` must exist in calendar tables

### 7.3 Uniqueness
- `routes.route_id` unique
- `stops.stop_id` unique
- `trips.trip_id` unique
- `stop_times (trip_id, stop_sequence)` unique

### 7.4 Valid ranges
- `stop_lat` in [-90, 90], `stop_lon` in [-180, 180]
- `route_type` within GTFS allowed values

### 7.5 Time parsing
- Convert `HH:MM:SS` possibly > 24h into `seconds_since_service_day_start`
- Keep original string for traceability

---

## 8. How This Joins with Realtime (Project Integration)

### 8.1 Trip Updates → Static
- Realtime `trip.trip_id` → `dim_trips.trip_id`
- Realtime `stop_time_update.stop_id` → `dim_stops.stop_id`
- Derive `route_id`, `direction_id`, `service_id` from `dim_trips`

### 8.2 Vehicle Positions → Static
- Realtime `trip.trip_id` → `dim_trips.trip_id` (if included)
- Use `route_id` for grouping
- Optionally map lat/lon to nearest stop (later)

---

## 9. Notes / Decisions (fill during project)
- Source snapshot date:
- Feed version (if available):
- Any missing GTFS files:
- Any dataset-specific quirks:

---
